"""Alert engine: dedupe, cooldown, two-tier (heads-up then confirmed/retracted) alerts."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from speechalerts.config import settings
from speechalerts.models import Alert, AlertState, Candidate, Mention
from speechalerts.sinks.base import Sink

log = logging.getLogger(__name__)


@dataclass(slots=True)
class _Recent:
    alert: Alert
    t: float  # audio time of the mention: cooldowns follow the speech, so replays at any speed behave alike
    emitted: bool = True  # False: a silent heads-up (spoken by someone other than the figure)


class AlertEngine:
    def __init__(
        self,
        sinks: list[Sink],
        *,
        figure: str | None = None,
        source: str = "",
        cooldown_seconds: float | None = None,
        min_confidence: float | None = None,
        retract_cooldown_seconds: float = 60.0,
    ) -> None:
        self.sinks = sinks
        self.figure = figure or settings.figure
        self.source = source
        self.cooldown = cooldown_seconds if cooldown_seconds is not None else settings.cooldown_seconds
        self.min_confidence = min_confidence if min_confidence is not None else settings.llm_min_confidence
        self.retract_cooldown = retract_cooldown_seconds
        self._headsup: dict[str, _Recent] = {}  # entity key -> last heads-up
        self._confirmed: dict[str, _Recent] = {}  # entity key -> last confirmed
        self.alerts: list[Alert] = []

    # ---------- tier 1: dictionary ----------

    async def on_candidates(self, candidates: list[Candidate]) -> list[Alert]:
        """Emit a heads-up for each entity not already alerted within the cooldown."""
        emitted: list[Alert] = []
        now = time.time()
        for cand in candidates:
            recent = self._headsup.get(cand.entity.key)
            silent = cand.speaker_role == "other"
            if recent:
                window = self.retract_cooldown if recent.alert.state == AlertState.RETRACTED else self.cooldown
                # A silent entry (reporter speech, shown to nobody) never mutes the figure: when the
                # figure says it, a real heads-up fires regardless of the cooldowns.
                upgrade = not recent.emitted and not silent
                if cand.t_audio - recent.t < window and not upgrade:
                    recent.alert.count += 1
                    continue
            alert = Alert(
                figure=self.figure,
                state=AlertState.HEADSUP,
                entity=cand.entity.name,
                tickers=list(cand.entity.tickers),
                quote=cand.segment_text[-200:],
                t_audio=cand.t_audio,
                t_spoken=cand.t_wall_spoken,
                t_stt=cand.t_stt,
                t_alert=now,
                source=self.source,
                action=",".join(cand.triggers_nearby[:3]) or "other",
                summary=f"{cand.entity.name} mentioned ({cand.entity.kind.value}: \"{cand.text_span}\")",
                speaker=cand.speaker_role,
                word_confidence=cand.word_confidence,
            )
            self._headsup[cand.entity.key] = _Recent(alert=alert, t=cand.t_audio, emitted=not silent)
            if silent:
                # Named by another speaker (a reporter's question): no heads-up, but the LLM still
                # gets to judge the figure's answer.
                log.info("question: %s named by another speaker (%r)", cand.entity.name, cand.text_span)
                continue
            emitted.append(alert)
            await self._emit(alert)
        return emitted

    def candidates_needing_confirmation(self, candidates: list[Candidate], max_age: float = 20.0) -> list[Candidate]:
        """Candidates whose heads-up is recent and not yet confirmed: worth sending to the LLM."""
        out = []
        for cand in candidates:
            recent = self._headsup.get(cand.entity.key)
            if recent and cand.t_audio - recent.t <= max_age and recent.alert.state == AlertState.HEADSUP:
                out.append(cand)
        return out

    # ---------- tier 2: LLM ----------

    async def on_confirmation(
        self,
        mentions: list[Mention],
        batch: list[Candidate],
        t_llm: float,
        defer: set[str] | None = None,
    ) -> list[Alert]:
        """Apply the model's verdict. Entity ids in `defer` are left as heads-ups if unconfirmed
        (their mention sat at the very end of the context and deserves a second look)."""
        emitted: list[Alert] = []
        now = time.time()
        defer = defer or set()
        matched_headsups: set[str] = set()
        for m in mentions:
            if m.confidence < self.min_confidence or m.speaker != "figure":
                continue
            cand = self._match_candidate(m, batch)
            if cand is None:
                continue  # the model was asked for candidates only; stray entries are ignored
            parent = self._headsup.get(cand.entity.key)
            key = cand.entity.key  # per dictionary entity: a sector alert must not mask a company one
            recent = self._confirmed.get(key)
            if recent and cand.t_audio - recent.t < self.cooldown and not _stance_flipped(recent.alert.stance, m.stance):
                recent.alert.count += 1
                if parent:
                    parent.alert.state = AlertState.CONFIRMED
                    matched_headsups.add(cand.entity.key)
                continue
            alert = Alert(
                figure=self.figure,
                state=AlertState.CONFIRMED,
                entity=m.entity,
                tickers=[t.upper() for t in m.tickers][:4] or (list(cand.entity.tickers) if cand else []),
                quote=m.quote,
                summary=m.summary,
                stance=m.stance,
                action=m.action,
                confidence=m.confidence,
                speaker=m.speaker,
                word_confidence=cand.word_confidence if cand else 1.0,
                t_audio=cand.t_audio if cand else (batch[0].t_audio if batch else 0.0),
                t_spoken=cand.t_wall_spoken if cand else (batch[0].t_wall_spoken if batch else now),
                t_stt=cand.t_stt if cand else (batch[0].t_stt if batch else now),
                t_llm=t_llm,
                t_alert=now,
                source=self.source,
                parent_id=parent.alert.id if parent else None,
            )
            if parent:
                parent.alert.state = AlertState.CONFIRMED
                matched_headsups.add(cand.entity.key)
            self._confirmed[key] = _Recent(alert=alert, t=cand.t_audio)
            emitted.append(alert)
            await self._emit(alert)

        # Heads-ups in this batch that the model did not confirm get retracted.
        for cand in batch:
            if cand.entity.key in matched_headsups or cand.entity.key in defer:
                continue
            parent = self._headsup.get(cand.entity.key)
            if not parent or parent.alert.state != AlertState.HEADSUP:
                continue
            parent.alert.state = AlertState.RETRACTED
            parent.t = cand.t_audio  # start the (shorter) retraction cooldown
            if not parent.emitted:
                continue  # nothing was shown, nothing to retract
            retraction = Alert(
                figure=self.figure,
                state=AlertState.RETRACTED,
                entity=cand.entity.name,
                tickers=list(cand.entity.tickers),
                quote=cand.segment_text[-200:],
                summary=f"Not a market-relevant mention of {cand.entity.name}",
                t_audio=cand.t_audio,
                t_spoken=cand.t_wall_spoken,
                t_stt=cand.t_stt,
                t_llm=t_llm,
                t_alert=now,
                source=self.source,
                parent_id=parent.alert.id,
                speaker=cand.speaker_role,
                word_confidence=cand.word_confidence,
            )
            emitted.append(retraction)
            await self._emit(retraction)
        return emitted

    # ---------- helpers ----------


    @staticmethod
    def _match_candidate(m: Mention, batch: list[Candidate]) -> Candidate | None:
        name = m.entity.lower()
        tickers = {t.upper() for t in m.tickers}
        best: Candidate | None = None
        for cand in batch:
            cname = cand.entity.name.lower()
            if cname == name or cname in name or name in cname:
                return cand
            if tickers and tickers & set(cand.entity.tickers):
                best = best or cand
            elif any(a.lower() in name for a in cand.entity.aliases if len(a) > 3):
                best = best or cand
        return best

    async def _emit(self, alert: Alert) -> None:
        self.alerts.append(alert)
        for sink in self.sinks:
            try:
                await sink.alert(alert)
            except Exception as exc:  # noqa: BLE001
                log.error("sink %s failed: %s", type(sink).__name__, exc)


def _stance_flipped(old: str, new: str) -> bool:
    """Only a positive<->negative reversal justifies a second confirmed alert inside the cooldown."""
    return {old, new} == {"positive", "negative"}
