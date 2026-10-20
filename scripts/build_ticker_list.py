"""Build data/entities/sec_tickers.json from the SEC's public company_tickers.json.

The SEC file is ordered roughly by market cap. We keep the top N, derive a clean alias from
the registered name (strip Inc, Corp, plc, /DE/ ...), and mark short or common-word names as
needs_context so they only fire next to a trigger word.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import httpx

SEC_URL = "https://www.sec.gov/files/company_tickers.json"
USER_AGENT = "SpeechAlerts research tool contact@example.com"

_SUFFIXES = re.compile(
    r"\b(incorporated|inc|corp|corporation|company|co|ltd|limited|plc|llc|lp|l\.p\.|holdings?|group|"
    r"international|worldwide|enterprises|technologies|technology|industries|bancorp|trust|n\.?v\.?|s\.?a\.?|ag|se)\b\.?",
    re.IGNORECASE,
)
_COMMON = {
    "target", "apple", "visa", "shell", "gap", "block", "coach", "alphabet", "meta", "ford", "united", "american",
    "general", "first", "national", "global", "energy", "capital", "financial", "digital", "health", "care",
    "realty", "income", "growth", "value", "trust", "resources", "systems", "solutions", "services", "group",
    "brands", "foods", "motors", "airlines", "bank", "power", "water", "gas", "oil", "steel", "gold", "silver",
    "copper", "uranium", "lithium", "sun", "moon", "star", "nova", "core", "prime", "next", "new", "one", "two",
    "three", "five", "ten", "best", "big", "super", "smart", "safe", "true", "fair", "free", "open", "live",
    "home", "world", "life", "time", "space", "air", "sea", "land", "city", "state", "west", "east", "north",
    "south", "central", "pacific", "atlantic", "texas", "boston", "york", "chase", "discover", "match", "snap",
    "box", "square", "circle", "cross", "arch", "bridge", "key", "lock", "post", "mail", "express", "way",
    "path", "road", "main", "street", "park", "garden", "forest", "river", "lake", "ocean", "island", "rock",
    "stone", "iron", "metal", "crown", "royal", "liberty", "freedom", "eagle", "lion", "tiger", "bear", "bull",
    "fox", "wolf", "hawk", "falcon", "phoenix", "titan", "atlas", "apollo", "mercury", "venus", "mars",
}


def clean_name(name: str) -> str:
    name = re.sub(r"/[A-Z]{2}/?$", "", name)  # /DE/
    name = re.sub(r"\(.*?\)", "", name)
    name = name.replace("&", " & ")
    name = _SUFFIXES.sub("", name)
    name = re.sub(r"[,.]+$", "", name.strip())
    name = re.sub(r"\s+", " ", name).strip(" ,.-")
    return name


def build(top_n: int = 800, out: Path = Path("data/entities/sec_tickers.json")) -> None:
    resp = httpx.get(SEC_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    raw = resp.json()
    rows = [raw[k] for k in sorted(raw, key=lambda k: int(k))][:top_n]
    items = []
    seen_aliases: set[str] = set()
    for row in rows:
        ticker = str(row["ticker"]).upper()
        if "-" in ticker or "." in ticker:
            continue  # skip preferred / warrant share classes
        title = str(row["title"]).title()
        alias = clean_name(title)
        if len(alias) < 3 or alias.lower() in seen_aliases:
            continue
        seen_aliases.add(alias.lower())
        words = alias.lower().split()
        needs_context = len(words) == 1 and (alias.lower() in _COMMON or len(alias) <= 4)
        items.append({"ticker": ticker, "name": title, "aliases": [alias], "needs_context": needs_context})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(items, indent=1))
    print(f"wrote {len(items)} entities to {out}", file=sys.stderr)


if __name__ == "__main__":
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 800)
