"""Shared read-only loaders for the signal study (strategy/data is never written).

Run every script from the strategy/ directory with its venv:
    .venv/bin/python signal_study/01_events.py
"""

from __future__ import annotations

import glob
import json
import math
import re
from datetime import date, datetime, timedelta
from functools import lru_cache
from pathlib import Path

import pandas as pd

from backtest.marketclock import INTERVAL_MINUTES, TradingCalendar, anchor_for, finest_interval_for, session_close, to_et
from backtest.models import ET

ROOT = Path(__file__).resolve().parent.parent  # strategy/
DATA = ROOT / "data"
OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)

HORIZONS = ["open", "+10m", "+30m", "+1h", "+2h", "close_d0", "close_d1", "close_d2", "close_d5", "close_d21"]


# ---------------------------------------------------------------- videos / signals

@lru_cache(maxsize=1)
def load_videos() -> dict[str, dict]:
    vids = {}
    for p in sorted(DATA.glob("signals/*.json")):
        d = json.load(open(p))
        vids[d["video"]["id"]] = d["video"]
    return vids


def video_start_et(v: dict) -> datetime | None:
    return datetime.fromtimestamp(v["t0"], ET) if v.get("t0") else None


@lru_cache(maxsize=1)
def load_signals() -> pd.DataFrame:
    """One row per dictionary signal (all states) with llm + judge (primary ticker) flattened."""
    rows = []
    for p in sorted(DATA.glob("signals/*.json")):
        d = json.load(open(p))
        v = d["video"]
        for s in d["signals"]:
            llm = s.get("llm") or {}
            judge = s.get("judge") or {}
            tickers = [t.upper() for t in (llm.get("tickers") or [])] or [t.upper() for t in s.get("dict_tickers") or []]
            primary = tickers[0] if tickers else None
            je = next((j for j in judge.get("tickers", []) if j["ticker"].upper() == primary), None) if primary else None
            rows.append({
                "signal_id": s["signal_id"], "video_id": v["id"], "video_label": v.get("label") or v.get("title", "")[:60],
                "group": v.get("group"), "entity_id": s["entity_id"], "entity": s["entity"], "kind": s["kind"],
                "text_span": s.get("text_span"), "t_audio": s["t_audio"], "t_wall": s.get("t_wall"), "t_wall_et": s.get("t_wall_et"),
                "speaker_is_main": s.get("speaker_is_main"), "state": s["state"], "count": s.get("count", 1),
                "dict_tickers": s.get("dict_tickers") or [], "llm_tickers": llm.get("tickers") or [], "tickers": tickers,
                "primary": primary, "n_tickers": len(tickers),
                "stance": llm.get("stance"), "action": llm.get("action"), "llm_conf": llm.get("confidence"),
                "quote": llm.get("quote", ""), "summary": llm.get("summary", ""), "segment_text": s.get("segment_text", ""),
                "context": s.get("context", ""),
                "judge_dir": je["direction"] if je else None, "judge_conf": je["confidence"] if je else None,
                "judge_mag": je["magnitude"] if je else None, "novelty": je["novelty"] if je else None,
                "judge_horizon": je["horizon"] if je else None, "judge_rationale": je["rationale"] if je else "",
                "judge_summary": judge.get("summary", ""),
                "judge_all": judge.get("tickers", []),
            })
    df = pd.DataFrame(rows)
    df["stance_dir"] = df["stance"].map({"positive": "up", "negative": "down"}).fillna("none")
    return df


@lru_cache(maxsize=1)
def load_measurements() -> pd.DataFrame:
    return pd.read_csv(DATA / "results" / "measurements.csv", low_memory=False)


@lru_cache(maxsize=1)
def wide() -> pd.DataFrame:
    """One row per confirmed (signal, ticker) with abnormal and raw returns per horizon as columns."""
    m = load_measurements()
    m = m[m["state"] == "confirmed"].copy()
    key = ["signal_id", "ticker"]
    meta_cols = ["video_id", "video_label", "group", "entity", "kind", "primary", "ticker_source", "first_mention", "t_audio",
                 "t_wall_et", "speaker_is_main", "market_state", "session", "origin_et", "stance", "action", "llm_confidence",
                 "stance_dir", "judge_dir", "judge_confidence", "novelty", "magnitude"]
    meta = m.drop_duplicates(key).set_index(key)[meta_cols]
    abn = m.pivot_table(index=key, columns="horizon", values="abn_ret", aggfunc="first")
    raw = m.pivot_table(index=key, columns="horizon", values="ret", aggfunc="first").add_prefix("raw_")
    spy = m.pivot_table(index=key, columns="horizon", values="spy_ret", aggfunc="first").add_prefix("spy_")
    w = meta.join(abn).join(raw).join(spy).reset_index()
    return w


# ---------------------------------------------------------------- prices

@lru_cache(maxsize=None)
def daily(ticker: str) -> pd.DataFrame:
    files = sorted(glob.glob(str(DATA / "prices" / f"{ticker}_1d_*.csv")))
    if not files:
        return pd.DataFrame()
    df = pd.read_csv(files[-1], index_col=0)
    if df.empty:
        return df
    df.index = pd.to_datetime(df.index).date
    return df


@lru_cache(maxsize=1)
def spy_daily() -> pd.DataFrame:
    return daily("SPY")


@lru_cache(maxsize=1)
def calendar() -> TradingCalendar:
    return TradingCalendar(list(spy_daily().index))


@lru_cache(maxsize=None)
def abn_vol(ticker: str, day: date, window: int = 60) -> float | None:
    """Std of daily (ticker - SPY) returns over the `window` sessions before `day`."""
    df = daily(ticker)
    if df.empty:
        return None
    r = df["Close"].pct_change()
    s = spy_daily()["Close"].pct_change()
    ab = (r - s.reindex(r.index)).dropna()
    win = ab[ab.index < day].tail(window)
    return float(win.std()) if len(win) >= 20 else None


@lru_cache(maxsize=None)
def raw_vol(ticker: str, day: date, window: int = 60) -> float | None:
    df = daily(ticker)
    if df.empty:
        return None
    r = df["Close"].pct_change().dropna()
    win = r[r.index < day].tail(window)
    return float(win.std()) if len(win) >= 20 else None


@lru_cache(maxsize=None)
def intraday(ticker: str, day: date, interval: str) -> pd.DataFrame:
    p = DATA / "prices" / f"{ticker}_{interval}_{day}.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p, index_col=0)
    if df.empty:
        return df
    df.index = pd.to_datetime(df.index, utc=True).tz_convert(ET)
    return df


def intraday_any(ticker: str, day: date) -> tuple[pd.DataFrame, str | None]:
    for iv in ("1m", "5m", "60m"):
        df = intraday(ticker, day, iv)
        if not df.empty:
            return df, iv
    return pd.DataFrame(), None


def price_before(ticker: str, t: datetime) -> tuple[float | None, str | None]:
    """Close of the last completed bar before t (finest interval available), or None."""
    df, iv = intraday_any(ticker, t.date())
    if df.empty:
        return None, None
    mins = INTERVAL_MINUTES[iv]
    done = df[df.index <= t - timedelta(minutes=mins)]
    if done.empty:
        first = df.index[0]
        return (float(df.iloc[0]["Open"]), iv + "/open") if first <= t else (None, None)
    return float(done.iloc[-1]["Close"]), iv


def price_at(ticker: str, t: datetime) -> tuple[float | None, str | None]:
    """Close of the last completed bar at or before t; the session close if t is past 16:00."""
    if t.time() >= session_close(t.date()).time():
        d = daily(ticker)
        return (float(d.loc[t.date(), "Close"]), "1d") if t.date() in d.index else (None, None)
    return price_before(ticker, t)


def ret(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or a == 0 or (isinstance(a, float) and math.isnan(a)) or (isinstance(b, float) and math.isnan(b)):
        return None
    return b / a - 1


def daily_close(ticker: str, day: date) -> float | None:
    d = daily(ticker)
    return float(d.loc[day, "Close"]) if (not d.empty and day in d.index) else None


def daily_open(ticker: str, day: date) -> float | None:
    d = daily(ticker)
    return float(d.loc[day, "Open"]) if (not d.empty and day in d.index) else None


# ---------------------------------------------------------------- transcripts

@lru_cache(maxsize=None)
def transcript(video_id: str) -> dict:
    return json.load(open(DATA / "transcripts" / f"{video_id}.json"))


def utterances(video_id: str) -> list[dict]:
    return transcript(video_id)["utterances"]


def main_speaker(video_id: str) -> int | None:
    return transcript(video_id).get("main_speaker")


def context(video_id: str, t: float, before: float = 60.0, after: float = 60.0, *, speakers: bool = True) -> str:
    ms = main_speaker(video_id)
    parts = []
    last = None
    for u in utterances(video_id):
        if u["end"] >= t - before and u["start"] <= t + after:
            spk = u.get("speaker")
            tag = ""
            if speakers and spk != last:
                tag = "[T] " if spk == ms else f"[S{spk}] "
                last = spk
            parts.append(tag + u["text"])
    return " ".join(parts).strip()


def other_speaker_seconds(video_id: str, t: float, before: float = 120.0, after: float = 120.0) -> float:
    """Seconds spoken by non-main speakers within the window (a proxy for guests/executives at the podium)."""
    ms = main_speaker(video_id)
    tot = 0.0
    for u in utterances(video_id):
        if u["end"] >= t - before and u["start"] <= t + after and u.get("speaker") != ms:
            tot += max(0.0, min(u["end"], t + after) - max(u["start"], t - before))
    return tot


def fmt_pct(x, digits: int = 2) -> str:
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x * 100:+.{digits}f}%"


def fmt_z(x) -> str:
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:+.1f}σ"


def md_table(rows: list[dict], cols: list[str], align: dict | None = None) -> str:
    align = align or {}
    head = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join("---:" if align.get(c) == "r" else "---" for c in cols) + "|"
    body = ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |" for r in rows]
    return "\n".join([head, sep] + body)
