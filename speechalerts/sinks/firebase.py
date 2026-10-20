"""Firebase sink: Firestore alert feed + FCM pushes (dry-run until a client exists).

Every write runs on one worker thread fed by an asyncio queue, so the alert path never blocks
and writes stay ordered (a heads-up document exists before its confirmation merges into it).
Final transcript segments go to `streams/{video_id}/segments/{t_wall_ms}` when
`FIREBASE_TRANSCRIPTS` is on (private dev feed; the public product must not redistribute them).
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from collections.abc import Callable
from typing import Any

from speechalerts.config import settings
from speechalerts.models import Alert, AlertState, TranscriptSegment

log = logging.getLogger(__name__)

PUSH_STATES = {AlertState.HEADSUP.value, AlertState.CONFIRMED.value}


class FirebaseSink:
    def __init__(
        self,
        *,
        project_id: str | None = None,
        topic: str | None = None,
        dry_run: bool | None = None,
        push_on_live: bool | None = None,
        transcripts: bool | None = None,
        figure: str | None = None,
        db: Any = None,
        messaging: Any = None,
        server_timestamp: Any = None,
    ) -> None:
        self.project_id = project_id or settings.firebase_project_id
        self.topic = topic or settings.fcm_topic
        self.dry_run = settings.fcm_dry_run if dry_run is None else dry_run
        self.push_on_live = settings.fcm_push_on_live if push_on_live is None else push_on_live
        self.transcripts = settings.firebase_transcripts if transcripts is None else transcripts
        self.figure = (figure or settings.figure).title()
        self.stream_id = ""
        self.stream_title = ""
        self._queue: asyncio.Queue[Callable[[], None] | None] = asyncio.Queue()
        self._worker: asyncio.Task | None = None
        self.written = 0
        self.failed = 0
        if db is not None or messaging is not None:
            self._db, self._messaging, self._ts = db, messaging, server_timestamp or (lambda: time.time())
        else:
            self._db, self._messaging, self._ts = self._init_firebase()

    # ---------- setup ----------

    def _init_firebase(self) -> tuple[Any, Any, Any]:
        import firebase_admin  # imported lazily: non-Firebase runs never load gRPC
        from firebase_admin import credentials, firestore, messaging

        if settings.firebase_credentials and not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.firebase_credentials
        cred = (
            credentials.Certificate(settings.firebase_credentials)
            if settings.firebase_credentials
            else credentials.ApplicationDefault()
        )
        options = {"projectId": self.project_id} if self.project_id else None
        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(cred, options)
        log.info("firebase sink: project %s, topic %r, %s", app.project_id, self.topic,
                 "dry-run pushes" if self.dry_run else "LIVE pushes")
        return firestore.client(app), messaging, (lambda: firestore.SERVER_TIMESTAMP)

    async def start(self) -> None:
        if self._worker is None:
            self._worker = asyncio.create_task(self._run(), name="firebase-sink")

    async def _run(self) -> None:
        while True:
            job = await self._queue.get()
            if job is None:
                return
            try:
                await asyncio.to_thread(job)
                self.written += 1
            except Exception as exc:  # noqa: BLE001
                self.failed += 1
                log.error("firebase write failed: %s", exc)

    def _submit(self, job: Callable[[], None]) -> None:
        if self._worker is None:
            # Not started (e.g. a bare `listen` without the daemon): run inline on the loop thread.
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None
            if loop is not None:
                self._worker = loop.create_task(self._run(), name="firebase-sink")
        self._queue.put_nowait(job)

    # ---------- Sink protocol ----------

    async def alert(self, alert: Alert) -> None:
        # Snapshot now: the engine later mutates a heads-up's `state` in place when it is confirmed
        # or retracted, and the worker may run after that.
        snapshot = alert.to_dict()
        self._submit(lambda: self._write_alert(snapshot))

    async def segment(self, seg: TranscriptSegment) -> None:
        if not (self.transcripts and seg.is_final and self.stream_id and seg.text.strip()):
            return
        stream_id = self.stream_id
        doc = {
            "text": seg.text,
            "t_audio_start": seg.t_audio_start,
            "t_audio_end": seg.t_audio_end,
            "t_wall": seg.t_wall,
            "confidence": seg.confidence,
            "speaker_label": seg.speaker_label,
        }
        doc_id = f"{int(seg.t_wall * 1000):016d}"  # wall-clock keyed: stays ordered across re-attaches
        self._submit(lambda: self._db.collection("streams").document(stream_id)
                     .collection("segments").document(doc_id).set(doc))

    async def close(self, drain_seconds: float = 30.0) -> None:
        if self._worker is None:
            return
        self._queue.put_nowait(None)
        try:
            await asyncio.wait_for(self._worker, timeout=drain_seconds)
        except asyncio.TimeoutError:
            log.warning("firebase sink: %d writes still pending at close", self._queue.qsize())
            self._worker.cancel()
        except asyncio.CancelledError:
            pass
        self._worker = None

    # ---------- daemon hooks ----------

    def set_stream(self, stream_id: str, title: str = "") -> None:
        self.stream_id, self.stream_title = stream_id, title

    def set_status(self, **fields: object) -> None:
        data = {**fields, "updated_at": self._ts()}
        self._submit(lambda: self._db.collection("status").document("current").set(data, merge=True))

    def stream_started(self, video_id: str, title: str, watch_url: str) -> None:
        self.set_stream(video_id, title)
        data = {"title": title, "watch_url": watch_url, "state": "live", "started_at": self._ts(),
                "figure": self.figure}

        def job() -> None:
            self._db.collection("streams").document(video_id).set(data, merge=True)
            if self.push_on_live:
                self._push(
                    title=f"{self.figure} is live",
                    body=title[:150],
                    data={"kind": "stream", "stream_id": video_id, "title": title[:200]},
                    label=f"[live] {title[:80]}",
                )

        self._submit(job)

    def stream_ended(self, video_id: str, reason: str, *, segments: int = 0, alerts: int = 0) -> None:
        data = {"state": "ended", "ended_at": self._ts(), "end_reason": reason,
                "segments": segments, "alerts": alerts}
        self._submit(lambda: self._db.collection("streams").document(video_id).set(data, merge=True))

    # ---------- writes (worker thread) ----------

    def _write_alert(self, a: dict) -> None:
        """`a` is an Alert.to_dict() snapshot taken when the alert was emitted."""
        state = a["state"]
        doc = {**a, "stream_id": self.stream_id, "stream_title": self.stream_title, "created_at": self._ts()}
        alerts = self._db.collection("alerts")
        alerts.document(a["id"]).set(doc)
        if a.get("parent_id") and state in (AlertState.CONFIRMED.value, AlertState.RETRACTED.value):
            alerts.document(a["parent_id"]).set(
                {"state": state, "resolved_by": a["id"], "resolved_at": self._ts()}, merge=True
            )
        if state in PUSH_STATES:
            title, body = self._wording(a)
            self._push(title=title, body=body, data=self._push_data(a), label=f"[{state}] {title}: {body[:60]!r}")

    def _wording(self, a: dict) -> tuple[str, str]:
        """Factual only: who mentioned what, with the labelled stance. Never a recommendation."""
        tickers = ", ".join(a["tickers"][:3])
        if a["state"] == AlertState.HEADSUP.value:
            title = f"{self.figure} mentioned {a['entity']}" + (f" ({tickers})" if tickers else "")
            body = a["quote"][:150]
        else:
            title = f"{self.figure} on {a['entity']}: {a['stance']} · {a['action']}"
            body = (a["summary"] or a["quote"])[:150]
        return title, body

    def _push_data(self, a: dict) -> dict[str, str]:
        return {
            "kind": "alert",
            "id": a["id"],
            "parent_id": a.get("parent_id") or "",
            "state": a["state"],
            "entity": a["entity"],
            "tickers": ",".join(a["tickers"]),
            "stance": a["stance"],
            "action": a["action"],
            "confidence": f"{a['confidence']:.2f}",
            "stream_id": self.stream_id,
            "t_alert": f"{a['t_alert']:.3f}",
        }

    def _push(self, *, title: str, body: str, data: dict[str, str], label: str) -> None:
        m = self._messaging
        message = m.Message(
            topic=self.topic,
            notification=m.Notification(title=title, body=body),
            data=data,
        )
        message_id = m.send(message, dry_run=self.dry_run)
        if self.dry_run:
            log.info("would push %s", label)
        else:
            log.info("pushed %s (%s)", label, message_id)
