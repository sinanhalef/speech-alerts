"""Wires source -> STT -> window -> dictionary -> engine (+ LLM confirmer) -> sinks."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator

from speechalerts.alerts.engine import AlertEngine
from speechalerts.config import settings
from speechalerts.extract.dictionary import Dictionary
from speechalerts.extract.llm_confirm import Confirmer
from speechalerts.models import AudioChunk, TranscriptSegment
from speechalerts.sinks.base import Sink
from speechalerts.sources.base import AudioSource
from speechalerts.stt.base import Transcriber
from speechalerts.transcript import AudioClock, RollingWindow, SpeakerTracker

log = logging.getLogger(__name__)


class Pipeline:
    def __init__(
        self,
        *,
        source: AudioSource,
        transcriber: Transcriber,
        dictionary: Dictionary,
        engine: AlertEngine,
        sinks: list[Sink],
        use_llm: bool | None = None,
        confirmer: Confirmer | None = None,
    ) -> None:
        self.source = source
        self.transcriber = transcriber
        self.dictionary = dictionary
        self.engine = engine
        self.sinks = sinks
        self.window = RollingWindow(settings.window_seconds)
        self.clock = AudioClock()
        self.speakers = SpeakerTracker(settings.speaker_window_seconds, settings.speaker_min_words)
        use_llm = settings.llm_enabled if use_llm is None else use_llm
        self.confirmer = confirmer if confirmer is not None else (Confirmer(engine.on_confirmation) if use_llm else None)
        if self.confirmer:
            self.confirmer.still_needed = engine.candidates_needing_confirmation
            self.confirmer.context_provider = lambda: (self._context_text(), self.window.latest_audio_time)
        self.segments = 0

    def _context_text(self) -> str:
        assert self.confirmer is not None
        return self.window.text_with_speakers(self.confirmer.context_seconds, dominant=self.speakers.dominant())

    async def _audio(self) -> AsyncIterator[AudioChunk]:
        async for chunk in self.source.chunks():
            self.clock.observe(chunk.t_audio, chunk.t_wall)
            yield chunk

    async def _on_segment(self, seg: TranscriptSegment) -> None:
        self.segments += 1
        prior_text = self.window.text(last_seconds=10, include_interim=False)
        self.window.add(seg)
        self.speakers.add(seg)
        seg.speaker_label = self.speakers.label(seg)
        for sink in self.sinks:
            try:
                await sink.segment(seg)
            except Exception as exc:  # noqa: BLE001
                log.error("sink %s segment failed: %s", type(sink).__name__, exc)
        candidates = self.dictionary.match(seg, self.clock, prior_text=prior_text, speakers=self.speakers)
        if not candidates:
            return
        await self.engine.on_candidates(candidates)
        if self.confirmer:
            to_confirm = self.engine.candidates_needing_confirmation(candidates)
            if to_confirm:
                self.confirmer.submit(to_confirm, self._context_text(), self.window.latest_audio_time)

    async def _heartbeat(self) -> None:
        """Detects a blocked event loop: logs whenever a 2 s sleep takes noticeably longer."""
        while True:
            t0 = time.monotonic()
            await asyncio.sleep(2)
            late = time.monotonic() - t0 - 2
            if late > 0.5:
                log.warning("event loop was blocked for ~%.1fs", late)

    async def run(self) -> None:
        hb = asyncio.create_task(self._heartbeat())
        try:
            async for seg in self.transcriber.transcribe(self._audio()):
                await self._on_segment(seg)
        finally:
            hb.cancel()
            if self.confirmer:
                try:
                    await asyncio.wait_for(self.confirmer.flush(), timeout=30)
                except asyncio.TimeoutError:
                    log.warning("llm confirmer did not flush in time")
            await self.source.close()
