"""Which mentions actually moved their stock? Immediate reaction, volatility-scaled, plus text features.

influence = the first measurable reaction: opening gap (market closed at the mention) or +1h (market
open). Both are divided by the ticker's own daily abnormal-return volatility over the 60 sessions
before the event (z-score), so a 5 % move in a coal miner is not treated like a 5 % move in Apple.
"""

from __future__ import annotations

import glob
import json
import math
import re
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from backtest.models import ET

RESULTS = Path(__file__).resolve().parent.parent / "data" / "results"
PRICES = Path(__file__).resolve().parent.parent / "data" / "prices"
SIGNALS = Path(__file__).resolve().parent.parent / "data" / "signals"

MONEY = re.compile(r"\$\s?\d|\b\d[\d,\.]*\s*(billion|million|trillion)\b|\b(billion|trillion|million)s?\b", re.I)
PERCENT = re.compile(r"\d+\s*(%|percent)", re.I)
ANNOUNCE = re.compile(r"\b(announc\w*|today we|we are (going to|gonna) (build|invest|sign)|just signed|i signed|signed|agreement|agreed|deal (with|to)|approved|approve|stake|golden share|contract|partnership|will invest|is investing|are investing)\b", re.I)
PRESENT = re.compile(r"\b(is here|are here|here today|with us today|joined by|thank you .{0,20}(ceo|chairman|founder)|stand up)\b", re.I)
FUTURE = re.compile(r"\b(will|going to|gonna|plan|plans|planning|soon|shortly|next week|next month)\b", re.I)
PAST_POLICY = re.compile(r"\b(biden|obama|four years ago|last year|during my first term|when i (was|came)|they had)\b", re.I)
NEGATIVE_WORDS = re.compile(r"\b(tariff|tariffs|ban|sanction|sue|lawsuit|fire|fired|terrible|disgrace|fake|failing|crooked|corrupt)\b", re.I)


def _daily_vol(ticker: str, day: date, spy: pd.DataFrame, cache: dict) -> float | None:
    key = (ticker, day)
    if key in cache:
        return cache[key]
    files = glob.glob(str(PRICES / f"{ticker}_1d_*.csv"))
    if not files:
        cache[key] = None
        return None
    df = pd.read_csv(files[0], index_col=0)
    if df.empty:
        cache[key] = None
        return None
    df.index = pd.to_datetime(df.index).date
    r = df["Close"].pct_change()
    s = spy["Close"].pct_change()
    ab = (r - s.reindex(r.index)).dropna()
    win = ab[ab.index < day].tail(60)
    v = float(win.std()) if len(win) >= 20 else None
    cache[key] = v
    return v


def load() -> pd.DataFrame:
    df = pd.read_csv(RESULTS / "measurements.csv")
    sig, vids = {}, {}
    for p in SIGNALS.glob("*.json"):
        d = json.load(open(p))
        v = d["video"]
        vids[v["id"]] = v
        for s in d["signals"]:
            sig[s["signal_id"]] = s
    h = df[(df.state == "confirmed") & (df.primary) & (df.first_mention)]
    piv = h.pivot_table(index="signal_id", columns="horizon", values="abn_ret")
    meta = h.drop_duplicates("signal_id").set_index("signal_id")[
        ["video_id", "video_label", "group", "entity", "kind", "ticker", "market_state", "session", "t_wall_et", "t_audio",
         "stance", "action", "llm_confidence", "judge_dir", "judge_confidence", "novelty", "magnitude", "speaker_is_main"]]
    t = meta.join(piv)
    spy_files = glob.glob(str(PRICES / "SPY_1d_*.csv"))
    spy = pd.read_csv(spy_files[0], index_col=0)
    spy.index = pd.to_datetime(spy.index).date
    cache: dict = {}
    rows = []
    for sid, r in t.iterrows():
        s = sig[sid]
        v = vids[r.video_id]
        llm = s.get("llm") or {}
        text = " ".join([llm.get("quote", ""), s.get("segment_text", "")])
        ctx = s.get("context", "")
        title = (v.get("title") or "").lower()
        ent_words = [w for w in re.split(r"[^a-z0-9]+", s["entity"].lower()) if len(w) > 3]
        day = date.fromisoformat(str(r.session)) if pd.notna(r.session) else None
        vol = _daily_vol(r.ticker, day, spy, cache) if day else None
        imm = r["open"] if r.market_state == "closed" else r["+1h"]
        rows.append({
            "signal_id": sid, "n_tickers": len(s.get("dict_tickers") or []), "count": s.get("count", 1),
            "pos_frac": (s["t_audio"] / v["duration"]) if v.get("duration") else None,
            "money": bool(MONEY.search(text)), "percent": bool(PERCENT.search(text)),
            "announce": bool(ANNOUNCE.search(text)), "announce_ctx": bool(ANNOUNCE.search(ctx)),
            "present": bool(PRESENT.search(ctx)), "future": bool(FUTURE.search(text)), "past": bool(PAST_POLICY.search(text)),
            "in_title": any(w in title for w in ent_words), "title_announce": bool(re.search(r"announce|signs|signing|roundtable|meets|meeting|summit|forum", title)),
            "quote_len": len(llm.get("quote", "").split()), "vol": vol,
            "imm": imm, "imm_kind": "open_gap" if r.market_state == "closed" else "+1h",
            "z_imm": (imm / vol) if (vol and pd.notna(imm)) else None,
            "z_d1": (r["close_d1"] / vol) if (vol and pd.notna(r["close_d1"])) else None,
            "z_d2": (r["close_d2"] / vol) if (vol and pd.notna(r["close_d2"])) else None,
            "quote": llm.get("quote", ""), "summary": llm.get("summary", ""), "title": v.get("title", ""),
        })
    f = pd.DataFrame(rows).set_index("signal_id")
    return t.join(f)


if __name__ == "__main__":
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 50); pd.set_option("display.max_colwidth", 70)
    t = load()
    t.to_csv(RESULTS / "influence_table.csv")
    print("rows", len(t), "with z_imm", t.z_imm.notna().sum(), "with z_d1", t.z_d1.notna().sum())
    print(t[["vol"]].describe().T)
