"""Transcriber protocol."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol

from speechalerts.models import AudioChunk, TranscriptSegment


class Transcriber(Protocol):
    def transcribe(self, audio: AsyncIterator[AudioChunk]) -> AsyncIterator[TranscriptSegment]: ...
