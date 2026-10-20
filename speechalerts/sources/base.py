"""Audio source protocol: anything that yields 16 kHz mono s16le PCM chunks."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol

from speechalerts.models import AudioChunk


class AudioSource(Protocol):
    name: str

    def chunks(self) -> AsyncIterator[AudioChunk]: ...

    async def close(self) -> None: ...


class StreamEnded(RuntimeError):
    """The broadcast finished (the platform no longer reports it live). Not an error to retry."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason
