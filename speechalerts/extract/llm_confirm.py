"""LLM confirmation: turns dictionary candidates plus transcript context into structured mentions.

Uses prompt-guided JSON rather than schema-constrained output: on Haiku the constrained decoder
roughly doubles latency for this payload size, and the pydantic validation below catches the
rare malformed reply.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from collections.abc import Awaitable, Callable

import anthropic
import pydantic

from speechalerts.config import settings
from speechalerts.models import Candidate, ConfirmResult, Mention

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """You analyse a live, automatically transcribed speech by {figure} for a market-alert service.

You receive the last ~{context}s of transcript with the candidate names marked like [[Intel]], plus a candidate list. Decide which candidates are genuine, market-relevant mentions and describe each one briefly.

Rules:
- Only report what the transcript actually says. It is machine-generated and may contain recognition errors. Leave out common-word false positives ("apple" the fruit, "target" the verb, "ford" a river crossing).
- The event may include questions from reporters and remarks by other people. Only what {figure} says counts. Speaker labels like [main speaker] / [speaker 2] (when present) come from automatic diarization: the main speaker is {figure}. Textual cues also mark a questioner: "Mr. President, ...", "Thank you, Mr. President", a name followed by an outlet ("John Smith, Fox News"), "go ahead". If a candidate is named only inside a question or by another speaker, set speaker to "questioner" or "other" and reject it (low confidence), unless {figure}'s own answer makes a market-relevant statement about it; then confirm with the answer as the quote.
- Each candidate line gives a word confidence: values below 0.9 usually mean an off-microphone speaker or a recognition error ("SS Coal" for USS Cole), so be sceptical of those.
- Market-relevant means a trader in that company, sector, or country ETF would want to know: tariffs, investments, deals, contracts, bans, sanctions, subsidies, regulation, price demands, executive hiring/firing, plant openings or closings, and praise or attacks on a company or media outlet by name.
- Output exactly one entry per listed candidate, in the order listed, and nothing else: rejected candidates get a low confidence rather than being left out. Other names in the transcript were handled by earlier calls; never include them.
- If the transcript ends mid-sentence right after a candidate, judge it on what is there; do not invent the rest.
- stance: the speaker's attitude toward the entity. action: one of tariff, investment, praise, criticism, regulation, deal, subsidy, sanction, military, other. speaker: figure, questioner, or other.
- tickers: main US-listed tickers or ETFs affected, uppercase, at most 4, empty for private companies.
- quote: verbatim, at most 15 words. summary: one factual sentence, at most 12 words, no advice. For a rejected candidate keep quote and summary to a few words.
- confidence: probability this is a genuine, market-relevant mention of that entity by {figure}. Use a low value (below 0.5) for candidates you reject.

Respond with only a JSON object, no prose and no code fences:
{{"mentions": [{{"entity": str, "tickers": [str], "stance": "positive"|"negative"|"neutral", "action": str, "speaker": "figure"|"questioner"|"other", "confidence": float, "quote": str, "summary": str}}]}}
Every listed candidate appears once; a rejected one looks like {{"entity": "Apple", "tickers": [], "stance": "neutral", "action": "other", "speaker": "figure", "confidence": 0.1, "quote": "apple pie", "summary": "The fruit, not the company."}}"""

_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.IGNORECASE)

ResultCallback = Callable[[list[Mention], list[Candidate], float, set[str]], Awaitable[None]]


class Confirmer:
    """Debounced LLM confirmer with concurrent calls.

    submit() collects candidates; the first submission in a quiet period starts a timer and, when
    it fires, everything collected goes to the model in one call. Calls run concurrently so a slow
    reply never delays the next batch. Results reach on_result(mentions, batch, t_done, defer_ids).

    Candidates whose mention sits within `fresh_seconds` of the end of the transcript are marked
    "deferred": the engine keeps their heads-up instead of retracting, and they are resubmitted once
    after `recheck_seconds` with more context.
    """

    def __init__(
        self,
        on_result: ResultCallback,
        *,
        figure: str | None = None,
        model: str | None = None,
        debounce_seconds: float | None = None,
        context_seconds: float | None = None,
        fresh_seconds: float = 4.0,
        recheck_seconds: float = 3.0,
        client: anthropic.AsyncAnthropic | None = None,
    ) -> None:
        self.on_result = on_result
        self.figure = figure or settings.figure
        self.model = model or settings.llm_model
        self.debounce = debounce_seconds if debounce_seconds is not None else settings.llm_debounce_seconds
        self.context_seconds = context_seconds or settings.llm_context_seconds
        self.still_needed: Callable[[list[Candidate]], list[Candidate]] | None = None
        # Returns (transcript text, latest audio time) at call time so rechecks see new speech.
        self.context_provider: Callable[[], tuple[str, float]] | None = None
        self.fresh_seconds = fresh_seconds
        self.recheck_seconds = recheck_seconds
        self.client = client or anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key or None)
        self._system = SYSTEM_PROMPT.format(figure=self.figure, context=int(self.context_seconds))
        self._pending: list[Candidate] = []
        self._inflight_ids: set[str] = set()
        self._context_text = ""
        self._context_end = 0.0
        self._timer: asyncio.Task | None = None
        self._tasks: set[asyncio.Task] = set()
        self.calls = 0
        self.errors = 0
        self.total_ms = 0.0

    # ---------- queueing ----------

    def submit(self, candidates: list[Candidate], context_text: str, context_end_t_audio: float) -> None:
        if not candidates:
            return
        known = {c.entity.key for c in self._pending} | self._inflight_ids
        for c in candidates:
            if c.entity.key not in known:
                self._pending.append(c)
                known.add(c.entity.key)
        if not self._pending:
            return
        self._context_text = context_text
        self._context_end = context_end_t_audio
        if self._timer is None or self._timer.done():
            self._timer = self._spawn(self._fire_after_delay())

    def _spawn(self, coro) -> asyncio.Task:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def _fire_after_delay(self) -> None:
        await asyncio.sleep(self.debounce)
        batch, self._pending = self._pending, []
        if batch and self.still_needed:
            batch = self.still_needed(batch)
        if batch:
            context, end = self._current_context()
            self._spawn(self._run(batch, context, end))

    async def _run(self, batch: list[Candidate], context: str, context_end: float) -> None:
        ids = {c.entity.key for c in batch}
        self._inflight_ids |= ids
        try:
            mentions = await self.confirm(batch, context)
        except Exception as exc:  # noqa: BLE001
            self.errors += 1
            log.error("llm confirm failed: %s", exc)
            return
        finally:
            self._inflight_ids -= ids
        confirmed_ids = {
            c.entity.key
            for c in batch
            if any(
                _mention_matches(m, c)
                for m in mentions
                if m.confidence >= settings.llm_min_confidence and m.speaker == "figure"
            )
        }
        defer = {
            c.entity.key
            for c in batch
            if c.entity.key not in confirmed_ids and c.attempts == 0 and context_end - c.t_audio < self.fresh_seconds
        }
        self._inflight_ids |= defer  # stay blocked until the recheck reports
        await self.on_result(mentions, batch, time.time(), defer)
        if defer:
            retry = [c for c in batch if c.entity.key in defer]
            for c in retry:
                c.attempts += 1
            self._spawn(self._recheck(retry))

    async def _recheck(self, retry: list[Candidate]) -> None:
        await asyncio.sleep(self.recheck_seconds)
        self._inflight_ids -= {c.entity.key for c in retry}
        if self.still_needed:
            retry = self.still_needed(retry)
        if not retry:
            return
        log.info("llm recheck: %s", ", ".join(c.entity.name for c in retry))
        context, end = self._current_context()
        self._spawn(self._run(retry, context, end))

    def _current_context(self) -> tuple[str, float]:
        if self.context_provider:
            return self.context_provider()
        return self._context_text, self._context_end

    async def flush(self) -> None:
        """Wait for pending and in-flight work (used at shutdown and in replay)."""
        while self._tasks:
            await asyncio.gather(*list(self._tasks), return_exceptions=True)

    # ---------- the call ----------

    def _user_message(self, batch: list[Candidate], context: str) -> str:
        marked = _mark_candidates(context.strip() or "(empty)", batch)
        lines = [f"Transcript (last ~{int(self.context_seconds)} seconds, newest last):", marked, ""]
        lines.append(f"Candidates ({len(batch)}):")
        for c in batch:
            tickers = ", ".join(c.entity.tickers) or "none"
            trig = ", ".join(c.triggers_nearby) or "none"
            spoken = {"figure": "main speaker", "other": "another speaker"}.get(c.speaker_role, "unknown speaker")
            lines.append(
                f'- "{c.text_span}" -> {c.entity.name} [{c.entity.kind}] tickers: {tickers}; nearby trigger words: {trig}; '
                f"spoken by: {spoken}; word confidence: {c.word_confidence:.2f}"
            )
        return "\n".join(lines)

    async def confirm(self, batch: list[Candidate], context: str) -> list[Mention]:
        self.calls += 1
        t0 = time.monotonic()
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=900,
            system=self._system,
            messages=[{"role": "user", "content": self._user_message(batch, context)}],
        )
        text = next((b.text for b in response.content if b.type == "text"), "")
        mentions = parse_mentions(text)
        for m in mentions:
            log.info("  mention: %s %s %s/%s by %s conf=%.2f", m.entity, m.tickers, m.stance, m.action, m.speaker, m.confidence)
        dt = (time.monotonic() - t0) * 1000
        self.total_ms += dt
        log.info(
            "llm confirm: %d candidates -> %d mentions in %.0f ms (in=%d out=%d)",
            len(batch), len(mentions), dt, response.usage.input_tokens, response.usage.output_tokens,
        )
        return mentions


def _mark_candidates(context: str, batch: list[Candidate]) -> str:
    """Wrap each candidate's mention in [[ ]] at the spot it was detected.

    Marks the span inside the candidate's own segment when that segment is present in the context,
    else the last occurrence of the span (the most recent mention). Never marks every occurrence:
    "apple pie" earlier in the window must not be flagged when the candidate is the later "Apple".
    """
    marked = context
    for c in batch:
        span_re = re.compile(rf"(?<![\w\[]){re.escape(c.text_span)}(?![\w\]])")
        seg_pos = marked.find(c.segment_text) if c.segment_text else -1
        if seg_pos >= 0:
            m = span_re.search(marked, seg_pos, seg_pos + len(c.segment_text))
        else:
            m = None
            for m in span_re.finditer(marked):
                pass
        if m:
            marked = marked[: m.start()] + "[[" + m.group(0) + "]]" + marked[m.end():]
    return marked


def parse_mentions(text: str) -> list[Mention]:
    cleaned = _FENCE.sub("", text.strip())
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        log.warning("llm reply had no JSON object: %r", text[:200])
        return []
    body = cleaned[start : end + 1]
    try:
        return ConfirmResult.model_validate_json(body).mentions
    except pydantic.ValidationError as exc:
        # Salvage the valid entries rather than dropping the whole batch.
        try:
            raw = json.loads(body)
        except json.JSONDecodeError:
            raw = _repair_truncated(cleaned[start:])
            if raw is None:
                log.warning("llm reply was not valid JSON: %s", str(exc.errors()[:1])[:200])
                return []
            log.warning("llm reply was truncated; salvaged %d complete entries", len(raw.get("mentions", [])))
        out: list[Mention] = []
        for item in raw.get("mentions", []) or []:
            try:
                out.append(Mention.model_validate(item))
            except pydantic.ValidationError:
                continue
        return out


def _repair_truncated(text: str) -> dict | None:
    """Close a JSON object cut off by max_tokens: keep entries up to the last complete '}'."""
    cut = text.rfind("}")
    while cut > 0:
        candidate = text[: cut + 1].rstrip().rstrip(",") + "]}"
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            cut = text.rfind("}", 0, cut)
    return None


def _mention_matches(m: Mention, cand: Candidate) -> bool:
    name = m.entity.lower()
    cname = cand.entity.name.lower()
    if cname == name or cname in name or name in cname:
        return True
    return bool({t.upper() for t in m.tickers} & set(cand.entity.tickers))
