"""Always-on cycle: poll channels, attach to a live stream, alert, return to polling.

State machine (status is mirrored to the web page and, when enabled, Firestore `status/current`):

    polling ──(live, title matches, id not handled)──▶ attaching ──▶ listening ──▶ ended ──▶ polling
                                                            ▲             │
                                                            └─(crashed but still live: retry)─┘

A video id that ended (or that we gave up on) is ignored for `watch_ignore_ended_hours`, because
YouTube keeps reporting a just-finished broadcast for a while and the channel /live page may still
point at it.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal

from speechalerts.config import settings
from speechalerts.sources import youtube
from speechalerts.sources.discovery import probe_channels
from speechalerts.sources.youtube import ResolvedStream

log = logging.getLogger(__name__)

RETRY_BACKOFF = (10.0, 30.0, 60.0)


@dataclass(slots=True)
class AttachResult:
    outcome: Literal["ended", "error", "unknown"]
    reason: str
    segments: int = 0
    alerts: int = 0


class WatchDaemon:
    def __init__(
        self,
        *,
        channels: list[str] | None = None,
        require_match: bool = True,
        use_llm: bool = True,
        web: bool = True,
        quiet: bool = False,
        show_interim: bool = False,
        once: bool = False,
        poll_seconds: float | None = None,
        ignore_hours: float | None = None,
        attach_retries: int | None = None,
        # Injection points for tests.
        probe: Callable[..., Awaitable[ResolvedStream | None]] = probe_channels,
        attach: Callable[[ResolvedStream], Awaitable[AttachResult]] | None = None,
        resolve: Callable[[str], Awaitable[ResolvedStream]] = youtube.resolve,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        clock: Callable[[], float] = time.monotonic,
        sinks=None,
    ) -> None:
        self.channels = channels or settings.watch_channels
        self.require_match = require_match
        self.use_llm = use_llm
        self.web = web
        self.quiet = quiet
        self.show_interim = show_interim
        self.once = once
        self.poll_seconds = poll_seconds if poll_seconds is not None else settings.watch_poll_seconds
        ignore_hours = ignore_hours if ignore_hours is not None else settings.watch_ignore_ended_hours
        self.ignore_seconds = ignore_hours * 3600
        self.attach_retries = attach_retries if attach_retries is not None else settings.watch_attach_retries
        self.probe = probe
        self.attach = attach or self._attach
        self.resolve = resolve
        self.sleep = sleep
        self.clock = clock
        self.sinks = sinks
        self.dictionary = None
        self.handled: dict[str, float] = {}  # video id -> clock() when it was marked done
        self.status_log: list[str] = []  # state transitions, newest last (tests + /api/status)
        self.streams_handled = 0

    # ---------- bookkeeping ----------

    def _set_status(self, state: str, **fields: object) -> None:
        self.status_log.append(state)
        if self.sinks is not None:
            self.sinks.set_status(state=state, **fields)

    def _mark_done(self, video_id: str, reason: str) -> None:
        if video_id:
            self.handled[video_id] = self.clock()
        log.info("stream %s done: %s", video_id or "?", reason)

    def _ignored_ids(self) -> set[str]:
        now = self.clock()
        self.handled = {vid: t for vid, t in self.handled.items() if now - t < self.ignore_seconds}
        return set(self.handled)

    # ---------- main loop ----------

    async def run(self) -> None:
        if self.sinks is None:
            from speechalerts.cli import build_sinks
            from speechalerts.extract.dictionary import Dictionary

            self.dictionary = Dictionary.load()
            self.sinks = await build_sinks(quiet=self.quiet, show_interim=self.show_interim)
        web_task = None
        if self.web:
            from speechalerts.web.app import create_app, serve

            web_task = asyncio.create_task(serve(create_app(self.sinks.broadcast, self.sinks.db)))
        log.info("watching %d channels every %.0fs: %s", len(self.channels), self.poll_seconds, ", ".join(self.channels))
        try:
            while True:
                self._set_status("polling", title="", source="", video_id="", channels=self.channels,
                                 last_poll=time.time())
                stream = await self.probe(self.channels, require_match=self.require_match, ignore_ids=self._ignored_ids())
                if stream is None:
                    await self.sleep(self.poll_seconds)
                    continue
                await self.handle_stream(stream)
                self.streams_handled += 1
                if self.once:
                    return
                log.info("back to polling every %.0fs", self.poll_seconds)
        finally:
            self._set_status("stopped")
            if web_task:
                web_task.cancel()
            await self.sinks.close()

    async def handle_stream(self, stream: ResolvedStream) -> AttachResult:
        """Attach to one broadcast, retrying while it is still live, then record how it ended."""
        video_id = stream.video_id
        fb = self.sinks.firebase if self.sinks is not None else None
        if fb is not None:
            fb.stream_started(video_id, stream.title, stream.watch_url or stream.page_url)
        result = AttachResult("unknown", "not attempted")
        try:
            result = await self._attach_with_retries(stream, result)
        except asyncio.CancelledError:
            # Daemon stopped (SIGTERM) mid-stream: say so in the feed. A restarted daemon re-attaches
            # to the same video if it is still live, because the handled set is per process.
            if fb is not None:
                fb.stream_ended(video_id, "daemon stopped", segments=result.segments, alerts=result.alerts)
            raise
        self._set_status("ended", title=stream.title, video_id=video_id, reason=result.reason)
        if fb is not None:
            fb.stream_ended(video_id, result.reason, segments=result.segments, alerts=result.alerts)
        return result

    async def _attach_with_retries(self, stream: ResolvedStream, result: AttachResult) -> AttachResult:
        video_id = stream.video_id
        for attempt in range(1 + self.attach_retries):
            self._set_status("attaching", title=stream.title, source=stream.watch_url or stream.page_url,
                             video_id=video_id, attempt=attempt + 1)
            result = await self.attach(stream)
            if result.outcome == "ended":
                self._mark_done(video_id, result.reason)
                break
            # Crashed, or ended without saying why: is the broadcast still on?
            still_live = await self._still_live(stream)
            if still_live is None:
                result.reason = f"{result.reason}; not live on re-probe"
                self._mark_done(video_id, result.reason)
                break
            if attempt == self.attach_retries:
                result.reason = f"{result.reason}; gave up after {attempt + 1} attempts"
                log.error("stream %s: %s", video_id, result.reason)
                self._mark_done(video_id, result.reason)
                break
            delay = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
            log.warning("stream %s still live after %s (%s); re-attaching in %.0fs",
                        video_id, result.outcome, result.reason, delay)
            await self.sleep(delay)
            stream = still_live
        return result

    async def _still_live(self, stream: ResolvedStream) -> ResolvedStream | None:
        try:
            fresh = await self.resolve(stream.watch_url or stream.page_url)
        except Exception as exc:  # noqa: BLE001
            log.warning("re-probe of %s failed: %s", stream.video_id, exc)
            return None
        if not fresh.is_live or fresh.live_status != "is_live":
            return None
        if stream.video_id and fresh.video_id and fresh.video_id != stream.video_id:
            return None
        return fresh

    # ---------- one attach ----------

    async def _attach(self, stream: ResolvedStream) -> AttachResult:
        from speechalerts.cli import run_pipeline
        from speechalerts.sources.youtube_live import YoutubeLiveSource
        from speechalerts.stt.deepgram_stream import DeepgramTranscriber

        assert self.sinks is not None and self.dictionary is not None
        target = stream.watch_url or stream.page_url
        # `resolved=stream` reuses the probe's yt-dlp result: no second resolve before audio starts.
        source = YoutubeLiveSource(target, name=stream.title[:60], resolved=stream)
        transcriber = DeepgramTranscriber(keyterms=self.dictionary.keyterms())
        if self.sinks.firebase is not None:
            self.sinks.firebase.set_stream(stream.video_id, stream.title)
        segments = alerts = 0
        try:
            pipeline, engine = await run_pipeline(
                mode="watch", target=target, title=stream.title, source=source, transcriber=transcriber,
                dictionary=self.dictionary, sinks=self.sinks, use_llm=self.use_llm,
            )
            segments, alerts = pipeline.segments, len(engine.alerts)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            log.error("listener failed: %s", exc, exc_info=True)
            return AttachResult("error", f"listener failed: {exc}", segments, alerts)
        reason = source.end_reason or (str(source.error) if source.error else "pipeline finished without a reason")
        return AttachResult(source.outcome, reason, segments, alerts)
