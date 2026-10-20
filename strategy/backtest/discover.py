"""List recent White House livestreams (and optional searches) as backtest candidates."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta

from speechalerts.sources import youtube

from backtest.models import ET

log = logging.getLogger(__name__)

DEFAULT_SOURCES = ["https://www.youtube.com/@WhiteHouse/streams"]
KEYWORDS = [
    "remarks", "signs", "executive order", "announcement", "roundtable", "executives", "tariff", "trade",
    "steel", "mining", "technology", "tech", "healthcare", "press conference", "cabinet", "investment",
    "ceo", "business", "economy", "energy", "oil", "auto", "pharma", "drug", "crypto", "bitcoin", "ai",
]
EXCLUDE = ["vice president", "first lady", "press secretary", "ceremony", "medal", "reception", "arrives", "arrival", "observance"]


async def _flat(url: str, limit: int) -> list[dict]:
    cmd = youtube._ytdlp_base() + ["--flat-playlist", "-j", "--playlist-end", str(limit), url]
    code, out, err = await youtube._run(cmd, timeout=180)
    if code != 0 and not out.strip():
        raise RuntimeError(f"yt-dlp failed for {url}: {err[:300]}")
    return [json.loads(line) for line in out.splitlines() if line.strip()]


async def _details(video_id: str) -> dict:
    cmd = youtube._ytdlp_base() + ["-j", f"https://www.youtube.com/watch?v={video_id}"]
    code, out, _ = await youtube._run(cmd, timeout=120)
    if code != 0 or not out.strip():
        return {}
    return json.loads(out.splitlines()[0])


def _relevant(title: str) -> bool:
    t = title.lower()
    if any(x in t for x in EXCLUDE):
        return False
    return any(re.search(rf"\b{re.escape(k)}\b", t) for k in KEYWORDS)


async def discover(*, days: int, sources: list[str] | None = None, searches: list[str] | None = None, limit: int = 60,
                   all_titles: bool = False, concurrency: int = 4) -> list[dict]:
    cutoff = datetime.now(ET) - timedelta(days=days)
    entries: list[dict] = []
    for src in sources or DEFAULT_SOURCES:
        entries += await _flat(src, limit)
    for q in searches or []:
        entries += await _flat(f"ytsearch{limit}:{q}", limit)
    seen: set[str] = set()
    picked = []
    for e in entries:
        vid = e.get("id")
        if not vid or vid in seen:
            continue
        seen.add(vid)
        if not all_titles and not _relevant(e.get("title") or ""):
            continue
        picked.append(e)
    sem = asyncio.Semaphore(concurrency)

    async def enrich(e: dict) -> dict | None:
        async with sem:
            info = await _details(e["id"])
        if not info:
            return None
        rel = info.get("release_timestamp") or info.get("timestamp")
        when = datetime.fromtimestamp(rel, ET) if rel else None
        if when and when < cutoff:
            return None
        return {
            "id": info.get("id"), "title": info.get("title"), "channel": info.get("channel"),
            "duration_min": round((info.get("duration") or 0) / 60, 1),
            "was_live": bool(info.get("was_live")) or info.get("live_status") == "was_live",
            "start_et": when.isoformat() if when else None,
            "url": f"https://www.youtube.com/watch?v={info.get('id')}",
        }

    results = [r for r in await asyncio.gather(*(enrich(e) for e in picked)) if r]
    results.sort(key=lambda r: r["start_et"] or "", reverse=True)
    return results
