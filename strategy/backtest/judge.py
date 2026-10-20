"""Expected price direction per signal: a Claude Sonnet 5 judge plus the live app's stance rule."""

from __future__ import annotations

import json
import logging
import re

import anthropic
import pydantic
from speechalerts.config import settings

from backtest.models import ET, Judgement, JudgeTicker, Signal, Transcript

log = logging.getLogger(__name__)

JUDGE_MODEL = "claude-sonnet-5"

SYSTEM_PROMPT = """You are an equity analyst evaluating one remark made by {figure} in a live speech, transcribed automatically.

Your task: for each listed ticker, decide the direction in which the remark, on its own, should move that stock's price relative to the overall market (SPY) in the hours and days after it was spoken.

Rules:
- Reason ONLY from the transcript excerpt and general knowledge of how markets price policy. Do not use any knowledge of what the stock actually did afterwards, even if you happen to remember the event.
- Distinguish the speaker's tone from the price effect: praise for a company is usually mildly positive; tariffs hurt importers but can help domestic producers; price caps or "drug prices will fall" are negative for the sellers; government stakes, contracts, subsidies, deals and investments announced are positive for the beneficiary; threats, bans, sanctions, lawsuits and criticism are negative.
- novelty: "new" if the excerpt announces or reveals something (a decision, a number, a deal, a deadline) that a trader would not already know from the news; "repeat" if it restates already-announced policy or is general rhetoric; "unclear" otherwise. Repeated rhetoric should usually get direction "none" or low confidence.
- direction "none" when the remark is not price-relevant for that ticker or the effect is ambiguous. confidence is your probability (0-1) that the abnormal return over the next 1-5 trading days has the stated sign; use <= 0.55 for coin flips.
- You may add at most 2 extra US-listed tickers or ETFs that are clearly affected (competitors, suppliers, sector ETFs) with "added": true. Include every listed ticker exactly once.
- Keep rationales to one sentence. Never use double quotes inside string values (use single quotes or none).

Respond with only a JSON object, no prose and no code fences:
{{"tickers": [{{"ticker": str, "direction": "up"|"down"|"none", "confidence": float, "magnitude": "small"|"medium"|"large", "novelty": "new"|"repeat"|"unclear", "horizon": "intraday"|"days"|"weeks", "rationale": str, "added": bool}}], "summary": str}}"""

_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.IGNORECASE)


class _JudgeOut(pydantic.BaseModel):
    tickers: list[dict] = []
    summary: str = ""


def stance_direction(stance: str) -> str:
    return {"positive": "up", "negative": "down"}.get(stance, "none")


def context_around(transcript: Transcript, t_audio: float, before: float = 60.0, after: float = 60.0) -> str:
    return " ".join(u.text for u in transcript.utterances if u.end >= t_audio - before and u.start <= t_audio + after).strip()


def user_message(sig: Signal, transcript: Transcript) -> str:
    when = sig.t_wall_et or "unknown"
    tickers = sig.all_tickers()
    llm = sig.llm
    lines = [
        f"Event: {transcript.video.title} ({transcript.video.channel}); spoken at {when} (America/New_York).",
        f"Speaker: {settings.figure} (speaker label {sig.speaker}, main speaker: {sig.speaker_is_main}).",
        "",
        "Transcript excerpt (~60 s before and after the remark):",
        context_around(transcript, sig.t_audio),
        "",
        f"Detected mention: {sig.entity} (dictionary match \"{sig.text_span}\", kind {sig.kind}).",
    ]
    if llm:
        lines += [
            f"Live-app confirmation: stance={llm.stance}, action={llm.action}, confidence={llm.confidence:.2f}",
            f"  quote: \"{llm.quote}\"",
            f"  summary: {llm.summary}",
        ]
    lines += ["", f"Tickers to judge: {', '.join(tickers) if tickers else '(none listed; add up to 2)'}"]
    return "\n".join(lines)


def parse_judgement(text: str, model: str, listed: list[str]) -> Judgement:
    cleaned = _FENCE.sub("", text.strip())
    start, end = cleaned.find("{"), cleaned.rfind("}")
    out = Judgement(model=model, raw=text[:4000])
    if start == -1 or end == -1:
        log.warning("judge reply had no JSON: %r", text[:200])
        return out
    try:
        raw = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError as exc:
        log.warning("judge reply was not valid JSON: %s", exc)
        return out
    parsed = _JudgeOut.model_validate(raw if isinstance(raw, dict) else {})
    listed_u = {t.upper() for t in listed}
    seen: set[str] = set()
    for item in parsed.tickers:
        try:
            ticker = str(item.get("ticker", "")).upper().strip()
            if not ticker or ticker in seen:
                continue
            seen.add(ticker)
            jt = JudgeTicker(
                ticker=ticker,
                direction=item.get("direction", "none") if item.get("direction") in ("up", "down", "none") else "none",
                confidence=float(item.get("confidence", 0) or 0),
                magnitude=item.get("magnitude") if item.get("magnitude") in ("small", "medium", "large") else "small",
                novelty=item.get("novelty") if item.get("novelty") in ("new", "repeat", "unclear") else "unclear",
                horizon=item.get("horizon") if item.get("horizon") in ("intraday", "days", "weeks") else "days",
                rationale=str(item.get("rationale", ""))[:400],
                added_by_judge=bool(item.get("added", False)) or ticker not in listed_u,
            )
            out.tickers.append(jt)
        except (pydantic.ValidationError, ValueError, TypeError) as exc:
            log.warning("judge entry skipped: %s", exc)
    added = [j for j in out.tickers if j.added_by_judge]
    if len(added) > 2:
        keep = set(id(j) for j in added[:2])
        out.tickers = [j for j in out.tickers if not j.added_by_judge or id(j) in keep]
    out.summary = str(parsed.summary)[:500]
    return out


class Judge:
    def __init__(self, *, model: str = JUDGE_MODEL, client: anthropic.AsyncAnthropic | None = None, effort: str = "medium") -> None:
        self.model = model
        self.client = client or anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key or None)
        self.effort = effort
        self._system = SYSTEM_PROMPT.format(figure=settings.figure)
        self.calls = 0

    async def judge(self, sig: Signal, transcript: Transcript) -> Judgement:
        self.calls += 1
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=[{"type": "text", "text": self._system, "cache_control": {"type": "ephemeral"}}],
            output_config={"effort": self.effort},
            messages=[{"role": "user", "content": user_message(sig, transcript)}],
        )
        if response.stop_reason == "refusal":
            log.warning("judge refused for %s", sig.signal_id)
            return Judgement(model=self.model, raw="refusal")
        text = next((b.text for b in response.content if b.type == "text"), "")
        return parse_judgement(text, self.model, sig.all_tickers())
