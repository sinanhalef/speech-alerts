"""A fake transcriber that replays a saved transcript, for testing extraction without STT cost.

Transcript file format: one utterance per line, either "12.5\tText of the utterance" (audio seconds
then a tab), "12.5\t1\tText" (seconds, diarization speaker id, text) or plain text lines (each
assumed to take ~3 s). Blank lines and lines starting with # are ignored. Audio input is drained
and ignored.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator
from pathlib import Path

from speechalerts.models import AudioChunk, TranscriptSegment
from speechalerts.transcript import words_for_text


def parse_transcript(text: str, default_gap: float = 3.0) -> list[tuple[float, float, str, int | None]]:
    """Returns (start, end, text, speaker) per utterance; speaker is None without a speaker column."""
    out: list[tuple[float, float, str, int | None]] = []
    t = 0.0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        speaker: int | None = None
        if "\t" in line:
            stamp, body = line.split("\t", 1)
            try:
                t = float(stamp)
            except ValueError:
                body = line
            else:
                if "\t" in body:
                    maybe_speaker, rest = body.split("\t", 1)
                    if maybe_speaker.strip().isdigit():
                        speaker, body = int(maybe_speaker), rest
        else:
            body = line
        words = max(len(body.split()), 1)
        dur = max(words / 2.5, 0.8)  # ~150 wpm
        out.append((t, t + dur, body, speaker))
        t += dur + 0.3
    return out


class TextReplayTranscriber:
    def __init__(self, path: Path, *, speed: float | None = 1.0, emit_interim: bool = True) -> None:
        self.utterances = parse_transcript(Path(path).read_text())
        self.speed = speed
        self.emit_interim = emit_interim

    async def transcribe(self, audio: AsyncIterator[AudioChunk]) -> AsyncIterator[TranscriptSegment]:
        drain = asyncio.create_task(self._drain(audio))
        t_wall0 = time.time()
        try:
            for start, end, text, speaker in self.utterances:
                if self.speed:
                    # Interim result mid-utterance, final at the end.
                    if self.emit_interim:
                        words = text.split()
                        half = " ".join(words[: max(len(words) // 2, 1)])
                        mid = (start + end) / 2
                        await self._sleep_until(t_wall0, mid)
                        yield TranscriptSegment(
                            text=half, t_audio_start=start, t_audio_end=mid,
                            t_wall=time.time(), is_final=False,
                            words=words_for_text(half, start, mid, speaker),
                        )
                    await self._sleep_until(t_wall0, end)
                yield TranscriptSegment(
                    text=text, t_audio_start=start, t_audio_end=end, t_wall=time.time(),
                    is_final=True, speech_final=True, confidence=1.0,
                    words=words_for_text(text, start, end, speaker),
                )
        finally:
            drain.cancel()

    async def _sleep_until(self, t_wall0: float, t_audio: float) -> None:
        due = t_wall0 + t_audio / (self.speed or 1.0)
        delay = due - time.time()
        if delay > 0:
            await asyncio.sleep(delay)

    @staticmethod
    async def _drain(audio: AsyncIterator[AudioChunk]) -> None:
        try:
            async for _ in audio:
                pass
        except Exception:  # noqa: BLE001
            pass


class SilenceSource:
    """Audio source that yields nothing; pairs with TextReplayTranscriber."""

    name = "silence"

    async def chunks(self) -> AsyncIterator[AudioChunk]:
        return
        yield  # pragma: no cover

    async def close(self) -> None:
        return None
