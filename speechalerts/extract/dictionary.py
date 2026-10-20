"""Fast dictionary matcher: Aho-Corasick over entity aliases and trigger words."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

import ahocorasick
import yaml

from speechalerts.config import settings
from speechalerts.models import Candidate, Entity, EntityKind, TranscriptSegment
from speechalerts.transcript import AudioClock, SpeakerTracker

log = logging.getLogger(__name__)

_WORD = re.compile(r"[a-z0-9]")


class Dictionary:
    def __init__(self, entities: list[Entity], triggers: list[str], *, context_chars: int = 140) -> None:
        self.entities = {e.id: e for e in entities}
        self.triggers = [t.lower() for t in triggers]
        self.context_chars = context_chars
        self._auto = ahocorasick.Automaton()
        for ent in entities:
            for alias in ent.aliases:
                key = alias.lower()
                existing = self._auto.get(key, None)
                payload = ("entity", ent.id, alias)
                if existing is None:
                    self._auto.add_word(key, [payload])
                else:
                    existing.append(payload)
        for trig in self.triggers:
            existing = self._auto.get(trig, None)
            payload = ("trigger", trig, trig)
            if existing is None:
                self._auto.add_word(trig, [payload])
            else:
                existing.append(payload)
        self._auto.make_automaton()

    # ---------- construction ----------

    @classmethod
    def load(cls, entities_path: Path | None = None, sec_path: Path | None = None) -> "Dictionary":
        entities_path = entities_path or settings.entities_path
        sec_path = sec_path or settings.sec_tickers_path
        raw = yaml.safe_load(entities_path.read_text())
        entities: list[Entity] = []
        for item in raw.get("entities", []):
            entities.append(
                Entity(
                    id=item["id"],
                    name=item["name"],
                    kind=EntityKind(item.get("kind", "company")),
                    tickers=[str(t) for t in item.get("tickers", [])],
                    aliases=[str(a) for a in item.get("aliases", [])],
                    needs_context=bool(item.get("needs_context", False)),
                    notes=item.get("notes", ""),
                )
            )
        known_aliases = {a.lower() for e in entities for a in e.aliases}
        if sec_path and sec_path.exists():
            added = 0
            for item in json.loads(sec_path.read_text()):
                aliases = [a for a in item["aliases"] if a.lower() not in known_aliases]
                if not aliases:
                    continue
                entities.append(
                    Entity(
                        id=f"sec_{item['ticker'].lower()}",
                        name=item["name"],
                        kind=EntityKind.COMPANY,
                        tickers=[item["ticker"]],
                        aliases=aliases,
                        needs_context=bool(item.get("needs_context", True)),
                        notes="sec",
                    )
                )
                added += 1
            log.info("dictionary: %d curated + %d SEC entities", len(entities) - added, added)
        return cls(entities, raw.get("triggers", []))

    def keyterms(self, limit: int = 100) -> list[str]:
        """Names worth boosting in the STT model (multi-word, unambiguous company names first)."""
        out: list[str] = []
        for ent in self.entities.values():
            if ent.kind in (EntityKind.COMPANY,) and not ent.needs_context and ent.notes != "sec":
                out.append(ent.name)
        return out[:limit]

    # ---------- matching ----------

    def _is_word_boundary(self, text: str, start: int, end: int) -> bool:
        before = text[start - 1] if start > 0 else " "
        after = text[end] if end < len(text) else " "
        if _WORD.match(before) or _WORD.match(after):
            return False
        if after == "'":
            # A trailing apostrophe only ends the word when it is a possessive ("Apple's plants");
            # "Dell'sy" (a mis-heard name) must not match Dell.
            rest = text[end + 1 : end + 3]
            if rest[:1] and _WORD.match(rest[:1]) and not (rest[:1] == "s" and not _WORD.match(rest[1:2] or " ")):
                return False
        return True

    def scan(self, text: str) -> tuple[list[tuple[Entity, str, int, int]], list[tuple[str, int]]]:
        """Return (entity hits as (entity, alias, start, end), trigger hits as (word, position))."""
        lowered = text.lower()
        entity_hits: list[tuple[Entity, str, int, int]] = []
        trigger_hits: list[tuple[str, int]] = []
        for end_idx, payloads in self._auto.iter(lowered):
            for kind, ident, alias in payloads:
                start = end_idx - len(alias) + 1
                end = end_idx + 1
                if not self._is_word_boundary(lowered, start, end):
                    continue
                if kind == "trigger":
                    trigger_hits.append((alias, start))
                else:
                    entity_hits.append((self.entities[ident], alias, start, end))
        # Prefer longer aliases when spans overlap (e.g. "us steel" over "steel").
        entity_hits.sort(key=lambda h: (h[2], -(h[3] - h[2])))
        kept: list[tuple[Entity, str, int, int]] = []
        last_end = -1
        for hit in entity_hits:
            if hit[2] < last_end:
                continue
            kept.append(hit)
            last_end = hit[3]
        return kept, trigger_hits

    def match(
        self,
        seg: TranscriptSegment,
        clock: AudioClock | None = None,
        prior_text: str = "",
        speakers: SpeakerTracker | None = None,
    ) -> list[Candidate]:
        """Match entities in `seg`. Trigger words are also looked for in the tail of `prior_text`
        (recent transcript before this segment) so "investing $600B ... not in India" fires even
        when the sentence spans two segments. With `speakers`, each candidate is attributed to
        the diarization speaker of its words and labelled figure/other/unknown."""
        hits, triggers = self.scan(seg.text)
        if not hits:
            return []
        if prior_text:
            tail = prior_text[-self.context_chars :]
            _, prior_triggers = self.scan(tail)
            offset = len(tail) + 1
            triggers = [(w, pos - offset) for w, pos in prior_triggers] + triggers
        out: list[Candidate] = []
        seen: set[str] = set()
        span = max(seg.t_audio_end - seg.t_audio_start, 0.0)
        for ent, alias, start, end in hits:
            nearby = [w for w, pos in triggers if abs(pos - start) <= self.context_chars]
            if ent.needs_context and not nearby:
                continue
            if ent.key in seen:
                continue
            seen.add(ent.key)
            frac = start / max(len(seg.text), 1)
            t_audio = seg.t_audio_start + frac * span
            t_spoken = clock.wall_for(t_audio) if clock else seg.t_wall
            speaker, word_conf = _words_at(seg, start, end)
            out.append(
                Candidate(
                    entity=ent,
                    alias=alias,
                    text_span=seg.text[start:end],
                    t_audio=t_audio,
                    t_wall_spoken=t_spoken,
                    t_stt=seg.t_wall,
                    triggers_nearby=sorted(set(nearby)),
                    segment_text=seg.text,
                    is_final=seg.is_final,
                    speaker=speaker,
                    speaker_role=speakers.role_of(speaker) if speakers else "unknown",
                    word_confidence=word_conf,
                )
            )
        return out


def _words_at(seg: TranscriptSegment, start: int, end: int, margin: int = 3) -> tuple[int | None, float]:
    """Speaker (majority) and mean confidence of the words covering text[start:end] +- margin.

    Words align with whitespace tokens of the segment text (Deepgram's transcript is the join of
    its punctuated words). Falls back to the segment's majority speaker when counts differ.
    """
    if not seg.words:
        return None, seg.confidence or 1.0
    toks = seg.text.split()
    if len(toks) != len(seg.words):
        confs = [w.confidence for w in seg.words]
        return seg.majority_speaker, sum(confs) / len(confs)
    first = len(seg.text[:start].split()) - (0 if start == 0 or seg.text[start - 1].isspace() else 1)
    last = len(seg.text[:end].split()) - 1
    first, last = max(first, 0), min(max(last, first), len(seg.words) - 1)
    hit = seg.words[first : last + 1]
    counts: dict[int, int] = {}
    for w in hit:
        if w.speaker is not None:
            counts[w.speaker] = counts.get(w.speaker, 0) + 1
    speaker = max(counts, key=counts.__getitem__) if counts else None
    around = seg.words[max(first - margin, 0) : last + 1 + margin]
    conf = sum(w.confidence for w in around) / len(around)
    return speaker, round(conf, 3)
