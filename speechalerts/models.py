"""Shared data models for the pipeline."""

from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


@dataclass(slots=True)
class AudioChunk:
    """Raw 16 kHz mono signed-16-bit PCM plus the wall-clock time it left the source."""

    pcm: bytes
    t_audio: float  # seconds since the start of the stream, at the start of this chunk
    t_wall: float  # time.time() when the chunk was emitted


@dataclass(slots=True)
class Word:
    text: str
    start: float
    end: float
    confidence: float
    speaker: int | None = None  # diarization label, present when diarize is on


@dataclass(slots=True)
class TranscriptSegment:
    """One Deepgram result. Interim results are replaced by later ones covering the same audio."""

    text: str
    t_audio_start: float
    t_audio_end: float
    t_wall: float
    is_final: bool
    speech_final: bool = False
    confidence: float = 0.0
    words: list[Word] = field(default_factory=list)
    session: int = 0  # STT socket session; diarization labels restart per session
    speaker_label: str = ""  # set by the pipeline for display: "T" main speaker, "Q" someone else

    @property
    def speaker_counts(self) -> dict[int, int]:
        """Words per diarization speaker in this result."""
        counts: dict[int, int] = {}
        for w in self.words:
            if w.speaker is not None:
                counts[w.speaker] = counts.get(w.speaker, 0) + 1
        return counts

    @property
    def majority_speaker(self) -> int | None:
        counts = self.speaker_counts
        return max(counts, key=counts.__getitem__) if counts else None


class EntityKind(StrEnum):
    COMPANY = "company"
    SECTOR = "sector"
    PERSON = "person"
    ASSET = "asset"
    COUNTRY = "country"
    TRIGGER = "trigger"


@dataclass(slots=True)
class Entity:
    id: str
    name: str
    kind: EntityKind
    tickers: list[str]
    aliases: list[str]
    needs_context: bool = False  # ambiguous alias: only fires when a trigger word is nearby
    notes: str = ""

    @property
    def key(self) -> str:
        """Dedupe key shared by an entity and its gated/strong twins (nvda + nvda_word, oil + oil_strong)."""
        return _SPLIT_SUFFIX.sub("", self.id)


_SPLIT_SUFFIX = re.compile(r"_(word|short|strong|outlet|abc|patriot)$")


@dataclass(slots=True)
class Candidate:
    """A dictionary hit inside a transcript segment."""

    entity: Entity
    alias: str
    text_span: str
    t_audio: float
    t_wall_spoken: float  # wall-clock estimate of when the word was spoken (from the audio clock)
    t_stt: float  # wall-clock when the transcript containing it arrived
    triggers_nearby: list[str]
    segment_text: str
    is_final: bool
    attempts: int = 0
    speaker: int | None = None  # diarization label of the words that matched
    speaker_role: str = "unknown"  # "figure" (dominant speaker), "other" (e.g. a reporter), "unknown"
    word_confidence: float = 1.0  # mean STT confidence around the matched words


class Stance(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Action(StrEnum):
    TARIFF = "tariff"
    INVESTMENT = "investment"
    PRAISE = "praise"
    CRITICISM = "criticism"
    REGULATION = "regulation"
    DEAL = "deal"
    SUBSIDY = "subsidy"
    SANCTION = "sanction"
    MILITARY = "military"
    OTHER = "other"


class Mention(BaseModel):
    """Structured output from the LLM confirmation step."""

    entity: str = Field(description="Canonical company, sector, or asset name")
    tickers: list[str] = Field(description="Uppercase exchange tickers or ETFs most affected, empty if none")
    stance: Literal["positive", "negative", "neutral"]
    action: Literal[
        "tariff", "investment", "praise", "criticism", "regulation", "deal", "subsidy", "sanction", "military", "other"
    ]
    speaker: Literal["figure", "questioner", "other"] = Field(
        default="figure", description="Who said it: the figure, a questioner (reporter), or someone else"
    )
    confidence: float = Field(ge=0, le=1, description="Probability this is a genuine, market-relevant mention")
    quote: str = Field(description="Verbatim from the transcript, at most 15 words")
    summary: str = Field(description="One short factual sentence, at most 12 words")


class ConfirmResult(BaseModel):
    mentions: list[Mention]


class AlertState(StrEnum):
    HEADSUP = "headsup"
    CONFIRMED = "confirmed"
    RETRACTED = "retracted"


@dataclass(slots=True)
class Alert:
    figure: str
    state: AlertState
    entity: str
    tickers: list[str]
    quote: str
    t_audio: float
    t_spoken: float
    t_stt: float
    t_alert: float
    source: str
    stance: str = "neutral"
    action: str = "other"
    summary: str = ""
    confidence: float = 0.0
    speaker: str = "figure"  # who said it: figure / questioner / other / unknown
    word_confidence: float = 1.0
    t_llm: float | None = None
    count: int = 1
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str | None = None

    @property
    def latency_ms(self) -> int:
        return int((self.t_alert - self.t_spoken) * 1000)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "figure": self.figure,
            "state": self.state.value,
            "entity": self.entity,
            "tickers": self.tickers,
            "stance": self.stance,
            "action": self.action,
            "quote": self.quote,
            "summary": self.summary,
            "confidence": self.confidence,
            "speaker": self.speaker,
            "word_confidence": self.word_confidence,
            "t_audio": self.t_audio,
            "t_spoken": self.t_spoken,
            "t_stt": self.t_stt,
            "t_llm": self.t_llm,
            "t_alert": self.t_alert,
            "latency_ms": self.latency_ms,
            "count": self.count,
            "source": self.source,
        }


def now() -> float:
    return time.time()
