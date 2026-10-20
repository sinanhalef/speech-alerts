"""In-process broadcast sink feeding server-sent-event subscribers (the web page)."""

from __future__ import annotations

import asyncio
import json
from collections import deque

from speechalerts.models import Alert, TranscriptSegment


class BroadcastSink:
    def __init__(self, history: int = 200) -> None:
        self._subscribers: set[asyncio.Queue[str]] = set()
        self.recent_alerts: deque[dict] = deque(maxlen=history)
        self.recent_segments: deque[dict] = deque(maxlen=50)
        self.status: dict = {"state": "idle", "title": "", "source": ""}

    def subscribe(self) -> asyncio.Queue[str]:
        q: asyncio.Queue[str] = asyncio.Queue(maxsize=500)
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[str]) -> None:
        self._subscribers.discard(q)

    def _publish(self, event: str, data: dict) -> None:
        payload = json.dumps({"event": event, "data": data})
        for q in list(self._subscribers):
            try:
                q.put_nowait(payload)
            except asyncio.QueueFull:
                self._subscribers.discard(q)

    def set_status(self, **fields: object) -> None:
        self.status.update(fields)
        self._publish("status", self.status)

    async def alert(self, alert: Alert) -> None:
        data = alert.to_dict()
        self.recent_alerts.appendleft(data)
        self._publish("alert", data)

    async def segment(self, seg: TranscriptSegment) -> None:
        data = {
            "text": seg.text,
            "t_audio_start": seg.t_audio_start,
            "t_audio_end": seg.t_audio_end,
            "t_wall": seg.t_wall,
            "is_final": seg.is_final,
            "speaker_label": seg.speaker_label,
        }
        if seg.is_final:
            self.recent_segments.append(data)
        self._publish("segment", data)

    async def close(self) -> None:
        self._publish("status", {**self.status, "state": "stopped"})
