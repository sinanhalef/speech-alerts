"""Compare tonight's speech mentions with prices: after-hours tape now, next-session gap later.

    cd strategy
    uv run python live_check.py --since "2026-10-05 19:45" --extra BDX,JBHT,KNX,ODFL,DE,AGCO,VLO,MPC,PSX
    uv run python live_check.py --since "2026-10-05 19:45" --next-open      # run after the next 9:30 ET open

Reads confirmed alerts from ../data/alerts.sqlite3 (first mention per ticker after --since), adds
--extra tickers for statements the dictionary missed, pulls 1-minute bars with pre/post market
from Yahoo and prints, per ticker: regular close, last trade before the mention, last after-hours
trade, and (with --next-open) the next session's open and +30 min price.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

ET = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "alerts.sqlite3"


def mentions_since(since: datetime) -> dict[str, dict]:
    """First confirmed mention per ticker at or after `since` (ET)."""
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT t_spoken, entity, tickers, stance, action FROM alerts "
        "WHERE state = 'confirmed' AND t_spoken >= ? ORDER BY t_spoken",
        (since.timestamp(),),
    ).fetchall()
    out: dict[str, dict] = {}
    for t_spoken, entity, tickers, stance, action in rows:
        for tk in json.loads(tickers or "[]"):
            out.setdefault(tk, {"t": datetime.fromtimestamp(t_spoken, ET), "entity": entity,
                                "stance": stance, "action": action, "source": "alert"})
    return out


def bars(ticker: str, start: date, end: date) -> pd.DataFrame:
    df = yf.download(ticker, start=start.isoformat(), end=(end + timedelta(days=1)).isoformat(),
                     interval="1m", prepost=True, auto_adjust=False, progress=False, threads=False)
    if df.empty:
        return df
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = df.index.tz_convert(ET)
    return df[["Close", "Volume"]]


def last_before(df: pd.DataFrame, t: datetime) -> tuple[float | None, datetime | None]:
    sub = df[df.index <= t]
    if sub.empty:
        return None, None
    return float(sub["Close"].iloc[-1]), sub.index[-1].to_pydatetime()


def first_at_or_after(df: pd.DataFrame, t: datetime) -> tuple[float | None, datetime | None]:
    sub = df[df.index >= t]
    if sub.empty:
        return None, None
    return float(sub["Close"].iloc[0]), sub.index[0].to_pydatetime()


def pct(a: float | None, b: float | None) -> str:
    if a is None or b is None or a == 0:
        return "   n/a"
    return f"{(b / a - 1) * 100:+6.2f}%"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help='ET, e.g. "2026-10-05 19:45"')
    ap.add_argument("--extra", default="", help="comma-separated tickers to add (dictionary misses)")
    ap.add_argument("--benchmark", default="SPY")
    ap.add_argument("--next-open", action="store_true", help="also show the next session's open and +30m")
    args = ap.parse_args()

    since = datetime.strptime(args.since, "%Y-%m-%d %H:%M").replace(tzinfo=ET)
    day = since.date()
    ment = mentions_since(since)
    for tk in filter(None, (t.strip().upper() for t in args.extra.split(","))):
        ment.setdefault(tk, {"t": since, "entity": "(manual)", "stance": "", "action": "", "source": "extra"})
    if args.benchmark and args.benchmark not in ment:
        ment[args.benchmark] = {"t": since, "entity": "(benchmark)", "stance": "", "action": "", "source": "bench"}

    close_t = datetime.combine(day, datetime.min.time(), ET).replace(hour=16)
    ah_end = close_t.replace(hour=20)
    next_day = day + timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    open_t = datetime.combine(next_day, datetime.min.time(), ET).replace(hour=9, minute=30)

    hdr = f"{'ticker':7} {'entity':28} {'mention':8} {'close':>9} {'pre':>9} {'ah_last':>9} {'pre→ah':>8} {'cls→ah':>8} {'ah_vol':>8}"
    if args.next_open:
        hdr += f" {'open':>9} {'cls→open':>9} {'+30m':>9}"
    print(hdr)
    print("-" * len(hdr))
    for tk, m in sorted(ment.items(), key=lambda kv: kv[1]["t"]):
        try:
            df = bars(tk, day, next_day if args.next_open else day)
        except Exception as exc:  # noqa: BLE001
            print(f"{tk:7} fetch failed: {str(exc)[:80]}", file=sys.stderr)
            continue
        if df.empty:
            print(f"{tk:7} {m['entity'][:28]:28} {m['t']:%H:%M:%S} {'no bars':>9}")
            continue
        close, _ = last_before(df, close_t + timedelta(minutes=1))
        pre, _ = last_before(df, m["t"])
        ah, ah_t = last_before(df, ah_end + timedelta(minutes=1))
        ah_vol = int(df[(df.index > m["t"]) & (df.index <= ah_end)]["Volume"].sum())
        line = (f"{tk:7} {m['entity'][:28]:28} {m['t']:%H:%M:%S} {close or 0:9.2f} {pre or 0:9.2f} "
                f"{ah or 0:9.2f} {pct(pre, ah):>8} {pct(close, ah):>8} {ah_vol:8d}")
        if args.next_open:
            op, _ = first_at_or_after(df, open_t)
            p30, _ = first_at_or_after(df, open_t + timedelta(minutes=30))
            line += f" {op or 0:9.2f} {pct(close, op):>9} {pct(op, p30):>9}"
        print(line)
    print(f"\nclose = last regular-session trade {day}; pre = last trade before the mention; "
          f"ah_last = last after-hours trade (≤ 20:00 ET); ah_vol = shares traded after the mention.")


if __name__ == "__main__":
    main()
