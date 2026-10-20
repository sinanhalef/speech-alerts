"""Sink protocol: receives alerts and transcript segments."""

from __future__ import annotations

from typing import Protocol

from speechalerts.models import Alert, TranscriptSegment


class Sink(Protocol):
    async def alert(self, alert: Alert) -> None: ...

    async def segment(self, seg: TranscriptSegment) -> None: ...

    async def close(self) -> None: ...
