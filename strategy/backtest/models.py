"""Data models shared by the backtest stages (pydantic so they round-trip through JSON files)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

ET = ZoneInfo("America/New_York")


class VideoSpec(BaseModel):
    """One entry of videos.yaml."""

    id: str
    url: str = ""
    label: str = ""
    notes: str = ""
    # ISO datetime (with offset, or naive = ET) of the moment t_audio=0 corresponds to.
    # Only needed for plain uploads; recorded livestreams get it from yt-dlp release_timestamp.
    event_start: str | None = None
    group: str = "other"  # recent | headline | expansion | other
    skip: bool = False

    def page_url(self) -> str:
        return self.url or f"https://www.youtube.com/watch?v={self.id}"


class VideoMeta(BaseModel):
    """yt-dlp metadata we keep for a video, plus the resolved wall-clock start."""

    id: str
    url: str
    title: str = ""
    channel: str = ""
    duration: float | None = None
    was_live: bool = False
    release_timestamp: float | None = None
    upload_timestamp: float | None = None
    upload_date: str | None = None
    label: str = ""
    group: str = "other"
    notes: str = ""
    # Epoch seconds of t_audio = 0; None when it cannot be determined.
    t0: float | None = None
    t0_source: str = ""  # release_timestamp | event_start | none

    def t0_et(self) -> datetime | None:
        return datetime.fromtimestamp(self.t0, ET) if self.t0 is not None else None


class Word(BaseModel):
    w: str
    s: float
    e: float
    c: float = 0.0
    spk: int | None = None


class Utterance(BaseModel):
    start: float
    end: float
    text: str
    speaker: int | None = None
    confidence: float = 0.0
    words: list[Word] = Field(default_factory=list)


class Transcript(BaseModel):
    video: VideoMeta
    model: str = "nova-3"
    main_speaker: int | None = None
    speaker_seconds: dict[str, float] = Field(default_factory=dict)
    utterances: list[Utterance] = Field(default_factory=list)


class LlmMention(BaseModel):
    entity: str
    tickers: list[str] = Field(default_factory=list)
    stance: str = "neutral"
    action: str = "other"
    confidence: float = 0.0
    quote: str = ""
    summary: str = ""


class JudgeTicker(BaseModel):
    ticker: str
    direction: Literal["up", "down", "none"] = "none"
    confidence: float = 0.0
    magnitude: Literal["small", "medium", "large"] = "small"
    novelty: Literal["new", "repeat", "unclear"] = "unclear"
    horizon: Literal["intraday", "days", "weeks"] = "days"
    rationale: str = ""
    added_by_judge: bool = False


class Judgement(BaseModel):
    model: str
    tickers: list[JudgeTicker] = Field(default_factory=list)
    summary: str = ""
    raw: str = ""


class Signal(BaseModel):
    """One dictionary heads-up and what happened to it (mirrors the live Alert, offline)."""

    signal_id: str
    video_id: str
    entity_id: str
    entity: str
    kind: str
    alias: str
    text_span: str
    dict_tickers: list[str] = Field(default_factory=list)
    triggers_nearby: list[str] = Field(default_factory=list)
    t_audio: float
    t_wall: float | None = None  # epoch seconds
    t_wall_et: str | None = None
    segment_text: str = ""
    context: str = ""  # what the confirmer saw (last call)
    speaker: int | None = None
    speaker_is_main: bool | None = None
    state: Literal["headsup", "confirmed", "retracted"] = "headsup"
    llm: LlmMention | None = None
    llm_attempts: int = 0
    count: int = 1  # repeat mentions folded into this signal by the cooldown
    judge: Judgement | None = None

    @property
    def primary_ticker(self) -> str | None:
        if self.llm and self.llm.tickers:
            return self.llm.tickers[0].upper()
        return self.dict_tickers[0].upper() if self.dict_tickers else None

    def all_tickers(self) -> list[str]:
        """LLM tickers first, then dictionary tickers, then judge additions; de-duplicated."""
        seen: list[str] = []
        for t in (self.llm.tickers if self.llm else []) + self.dict_tickers + (
            [j.ticker for j in self.judge.tickers if j.added_by_judge] if self.judge else []
        ):
            t = t.upper()
            if t and t not in seen:
                seen.append(t)
        return seen

    def stance_direction(self) -> str:
        if not self.llm:
            return "none"
        return {"positive": "up", "negative": "down"}.get(self.llm.stance, "none")

    def judge_direction(self, ticker: str) -> str:
        if not self.judge:
            return "none"
        for j in self.judge.tickers:
            if j.ticker.upper() == ticker.upper():
                return j.direction
        return "none"

    def judge_entry(self, ticker: str) -> JudgeTicker | None:
        if not self.judge:
            return None
        return next((j for j in self.judge.tickers if j.ticker.upper() == ticker.upper()), None)


class SignalFile(BaseModel):
    video: VideoMeta
    dictionary_entities: int = 0
    llm_model: str = ""
    counts: dict[str, int] = Field(default_factory=dict)
    signals: list[Signal] = Field(default_factory=list)


HORIZONS: list[str] = ["open", "+10m", "+30m", "+1h", "+2h", "close_d0", "close_d1", "close_d2", "close_d5", "close_d21"]
INTRADAY_MINUTES: dict[str, int] = {"+10m": 10, "+30m": 30, "+1h": 60, "+2h": 120}
DAILY_OFFSETS: dict[str, int] = {"close_d0": 0, "close_d1": 1, "close_d2": 2, "close_d5": 5, "close_d21": 21}
