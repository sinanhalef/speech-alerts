"""Rolling transcript window, audio-time bookkeeping, and speaker dominance tracking."""

from __future__ import annotations

import time
from collections import deque

from speechalerts.models import TranscriptSegment, Word


class AudioClock:
    """Maps audio time (seconds into the stream) to the wall-clock moment we received that audio."""

    def __init__(self) -> None:
        self._points: deque[tuple[float, float]] = deque(maxlen=2000)  # (t_audio, t_wall)

    def observe(self, t_audio: float, t_wall: float) -> None:
        self._points.append((t_audio, t_wall))

    def wall_for(self, t_audio: float) -> float:
        """Wall-clock time at which the audio at t_audio was received from the source."""
        if not self._points:
            return time.time()
        # Points are monotonic in t_audio; find the last point at or before t_audio.
        best = self._points[0]
        for pt in reversed(self._points):
            if pt[0] <= t_audio:
                best = pt
                break
        else:
            return best[1]
        return best[1] + (t_audio - best[0])


class SpeakerTracker:
    """Who talks most over the last N seconds: at a speech or press conference that is the figure.

    Diarization labels are arbitrary integers that restart on every STT socket, so counts are
    reset whenever a segment arrives from a new session. `dominant()` stays None until one
    speaker has at least `min_words`, so the first minute of a stream is "unknown" rather than
    wrongly gated.
    """

    def __init__(self, window_seconds: float = 300.0, min_words: int = 60) -> None:
        self.window = window_seconds
        self.min_words = min_words
        self._events: deque[tuple[float, int, int]] = deque()  # (t_audio_end, speaker, words)
        self._counts: dict[int, int] = {}
        self._session: int | None = None

    def reset(self) -> None:
        self._events.clear()
        self._counts.clear()

    def add(self, seg: TranscriptSegment) -> None:
        """Count a final segment's words per speaker (interims would double count)."""
        if not seg.is_final:
            return
        if self._session is not None and seg.session != self._session:
            self.reset()
        self._session = seg.session
        for spk, n in seg.speaker_counts.items():
            self._events.append((seg.t_audio_end, spk, n))
            self._counts[spk] = self._counts.get(spk, 0) + n
        cutoff = seg.t_audio_end - self.window
        while self._events and self._events[0][0] < cutoff:
            _, spk, n = self._events.popleft()
            self._counts[spk] -= n
            if self._counts[spk] <= 0:
                del self._counts[spk]

    def dominant(self) -> int | None:
        if not self._counts:
            return None
        spk = max(self._counts, key=self._counts.__getitem__)
        return spk if self._counts[spk] >= self.min_words else None

    def role_of(self, speaker: int | None) -> str:
        """'figure' for the dominant speaker, 'other' for anyone else, 'unknown' if undecidable."""
        dom = self.dominant()
        if speaker is None or dom is None:
            return "unknown"
        return "figure" if speaker == dom else "other"

    def label(self, seg: TranscriptSegment) -> str:
        role = self.role_of(seg.majority_speaker)
        return {"figure": "T", "other": "Q"}.get(role, "")


class RollingWindow:
    """Keeps final segments for the last N seconds plus the current interim text."""

    def __init__(self, seconds: float = 90.0) -> None:
        self.seconds = seconds
        self.finals: deque[TranscriptSegment] = deque()
        self.interim: TranscriptSegment | None = None

    def add(self, seg: TranscriptSegment) -> None:
        if seg.is_final:
            self.finals.append(seg)
            self.interim = None
            cutoff = seg.t_audio_end - self.seconds
            while self.finals and self.finals[0].t_audio_end < cutoff:
                self.finals.popleft()
        else:
            self.interim = seg

    @property
    def latest_audio_time(self) -> float:
        if self.interim:
            return self.interim.t_audio_end
        return self.finals[-1].t_audio_end if self.finals else 0.0

    def _segments(self, last_seconds: float | None, include_interim: bool) -> list[TranscriptSegment]:
        cutoff = self.latest_audio_time - last_seconds if last_seconds else -1.0
        segs = [s for s in self.finals if s.t_audio_end >= cutoff]
        if include_interim and self.interim:
            segs.append(self.interim)
        return segs

    def text(self, last_seconds: float | None = None, include_interim: bool = True) -> str:
        return " ".join(s.text for s in self._segments(last_seconds, include_interim)).strip()

    def text_with_speakers(
        self, last_seconds: float | None = None, dominant: int | None = None, include_interim: bool = True
    ) -> str:
        """Transcript with a label at every speaker change: [main speaker] ... [speaker 2] ...

        Falls back to plain text when no word carries a diarization label.
        """
        segs = self._segments(last_seconds, include_interim)
        if not any(w.speaker is not None for s in segs for w in s.words):
            return " ".join(s.text for s in segs).strip()
        parts: list[str] = []
        current: int | None = None
        started = False
        for s in segs:
            if not s.words or len(s.words) != len(s.text.split()):
                # Cannot align words to text; attribute the whole segment to its majority speaker.
                spk = s.majority_speaker
                if spk != current or not started:
                    parts.append(_speaker_tag(spk, dominant))
                    current, started = spk, True
                parts.append(s.text)
                continue
            for tok, w in zip(s.text.split(), s.words):
                if w.speaker != current or not started:
                    parts.append(_speaker_tag(w.speaker, dominant))
                    current, started = w.speaker, True
                parts.append(tok)
        return " ".join(parts).strip()


def _speaker_tag(speaker: int | None, dominant: int | None) -> str:
    if speaker is None:
        return "[unknown speaker]"
    if dominant is not None and speaker == dominant:
        return "[main speaker]"
    return f"[speaker {speaker + 1}]"


def words_for_text(text: str, start: float, end: float, speaker: int | None = None) -> list[Word]:
    """Synthesise per-token words with interpolated times (text replay, tests)."""
    toks = text.split()
    if not toks:
        return []
    step = max(end - start, 0.1) / len(toks)
    return [
        Word(text=t, start=start + i * step, end=start + (i + 1) * step, confidence=1.0, speaker=speaker)
        for i, t in enumerate(toks)
    ]
