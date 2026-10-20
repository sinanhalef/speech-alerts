"""Offline replay of the live extraction algorithm over a saved transcript.

Reuses the live components unchanged: `Dictionary.match` (Aho-Corasick + trigger gating),
`RollingWindow` (same 90 s window and 30 s LLM context), `Confirmer.confirm` (same Haiku prompt
and JSON parsing) and `AlertEngine._match_candidate` (same mention->candidate matching). What is
re-implemented here is only the *timing*: cooldowns run on audio time instead of wall-clock, and
the live "defer and recheck 3 s later" step is reproduced by extending the context with the
next 3 s of transcript.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Protocol

from speechalerts.alerts.engine import AlertEngine
from speechalerts.config import settings
from speechalerts.extract.dictionary import Dictionary
from speechalerts.models import Candidate, Mention, TranscriptSegment
from speechalerts.transcript import AudioClock, RollingWindow

from backtest.models import ET, LlmMention, Signal, SignalFile, Transcript, Utterance

log = logging.getLogger(__name__)


class ConfirmerLike(Protocol):
    async def confirm(self, batch: list[Candidate], context: str) -> list[Mention]: ...


class OfflineExtractor:
    def __init__(
        self,
        dictionary: Dictionary,
        confirmer: ConfirmerLike | None,
        *,
        cooldown_seconds: float | None = None,
        retract_cooldown_seconds: float = 60.0,
        min_confidence: float | None = None,
        context_seconds: float | None = None,
        fresh_seconds: float = 4.0,
        recheck_seconds: float = 3.0,
        llm_model: str = "",
    ) -> None:
        self.dictionary = dictionary
        self.confirmer = confirmer
        self.cooldown = settings.cooldown_seconds if cooldown_seconds is None else cooldown_seconds
        self.retract_cooldown = retract_cooldown_seconds
        self.min_confidence = settings.llm_min_confidence if min_confidence is None else min_confidence
        self.context_seconds = settings.llm_context_seconds if context_seconds is None else context_seconds
        self.fresh_seconds = fresh_seconds
        self.recheck_seconds = recheck_seconds
        self.llm_model = llm_model or settings.llm_model
        self.calls = 0

    async def run(self, transcript: Transcript) -> SignalFile:
        video = transcript.video
        window = RollingWindow(settings.window_seconds)
        clock = AudioClock()
        if video.t0 is not None:
            clock.observe(0.0, video.t0)
        recent: dict[str, Signal] = {}
        signals: list[Signal] = []
        utts = transcript.utterances

        for idx, u in enumerate(utts):
            seg = TranscriptSegment(
                text=u.text, t_audio_start=u.start, t_audio_end=u.end,
                t_wall=(video.t0 or 0.0) + u.end, is_final=True, speech_final=True, confidence=u.confidence,
            )
            prior_text = window.text(last_seconds=10, include_interim=False)
            window.add(seg)
            candidates = self.dictionary.match(seg, clock if video.t0 is not None else None, prior_text=prior_text)
            if not candidates:
                continue
            batch: list[tuple[Candidate, Signal]] = []
            for cand in candidates:
                prev = recent.get(cand.entity.id)
                if prev is not None:
                    win = self.retract_cooldown if prev.state == "retracted" else self.cooldown
                    if cand.t_audio - prev.t_audio < win:
                        prev.count += 1
                        continue
                sig = self._headsup(video.id, cand, u, transcript.main_speaker, video.t0)
                recent[cand.entity.id] = sig
                signals.append(sig)
                batch.append((cand, sig))
            if not batch:
                continue
            if self.confirmer is None:
                continue
            context = window.text(self.context_seconds)
            await self._confirm(batch, context, seg.t_audio_end)
            retry = [(c, s) for c, s in batch if s.state == "headsup" and seg.t_audio_end - c.t_audio < self.fresh_seconds]
            for cand, sig in [(c, s) for c, s in batch if s.state == "headsup" and (c, s) not in retry]:
                sig.state = "retracted"
            if retry:
                context2 = self._extended_context(utts, idx, seg.t_audio_end + self.recheck_seconds)
                await self._confirm(retry, context2, seg.t_audio_end + self.recheck_seconds)
                for _, sig in retry:
                    if sig.state == "headsup":
                        sig.state = "retracted"

        counts = {
            "headsups": len(signals),
            "confirmed": sum(1 for s in signals if s.state == "confirmed"),
            "retracted": sum(1 for s in signals if s.state == "retracted"),
            "unconfirmed": sum(1 for s in signals if s.state == "headsup"),
            "llm_calls": self.calls,
        }
        return SignalFile(video=video, dictionary_entities=len(self.dictionary.entities), llm_model=self.llm_model,
                          counts=counts, signals=signals)

    # ---------- helpers ----------

    def _headsup(self, video_id: str, cand: Candidate, u: Utterance, main_speaker: int | None, t0: float | None) -> Signal:
        t_wall = (t0 + cand.t_audio) if t0 is not None else None
        return Signal(
            signal_id=f"{video_id}:{int(cand.t_audio):05d}:{cand.entity.id}",
            video_id=video_id,
            entity_id=cand.entity.id,
            entity=cand.entity.name,
            kind=cand.entity.kind.value,
            alias=cand.alias,
            text_span=cand.text_span,
            dict_tickers=list(cand.entity.tickers),
            triggers_nearby=list(cand.triggers_nearby),
            t_audio=cand.t_audio,
            t_wall=t_wall,
            t_wall_et=datetime.fromtimestamp(t_wall, ET).isoformat() if t_wall is not None else None,
            segment_text=cand.segment_text,
            speaker=u.speaker,
            speaker_is_main=(u.speaker == main_speaker) if (u.speaker is not None and main_speaker is not None) else None,
        )

    async def _confirm(self, batch: list[tuple[Candidate, Signal]], context: str, context_end: float) -> None:
        assert self.confirmer is not None
        cands = [c for c, _ in batch]
        self.calls += 1
        try:
            mentions = await self.confirmer.confirm(cands, context)
        except Exception as exc:  # noqa: BLE001
            log.error("llm confirm failed at %.0fs: %s", context_end, exc)
            mentions = []
        by_id = {c.entity.id: s for c, s in batch}
        for _, s in batch:
            s.llm_attempts += 1
            s.context = context
        for m in mentions:
            if m.confidence < self.min_confidence:
                continue
            cand = AlertEngine._match_candidate(m, cands)
            if cand is None:
                continue
            sig = by_id[cand.entity.id]
            if sig.state == "confirmed":
                continue
            sig.state = "confirmed"
            sig.llm = LlmMention(
                entity=m.entity,
                tickers=[t.upper() for t in m.tickers][:4] or list(cand.entity.tickers),
                stance=m.stance, action=m.action, confidence=m.confidence, quote=m.quote, summary=m.summary,
            )

    def _extended_context(self, utts: list[Utterance], idx: int, ctx_end: float) -> str:
        start = ctx_end - self.context_seconds
        parts = [u.text for u in utts[: idx + 1] if u.end >= start]
        for u in utts[idx + 1 :]:
            if u.start > ctx_end:
                break
            parts.append(u.text)
        return " ".join(parts).strip()
