"""Live speech watcher: tail the transcript + alerts from the local SQLite log and the futures
tape from Yahoo (1-minute bars, ~10 min delayed), emit events while the listener is attached.

    cd strategy && uv run python live_watch.py --since "2026-10-05 19:45" \
        --events ../logs/live_watch.events --log ../logs/live_watch.log

stdout / --events (one line per event, meant for a monitor):
    ALERT   hh:mm:ss  confirmed Entity [TICKERS] stance/action  "quote"
    MOVE    hh:mm:ss  HO=F +0.62% since 19:45 (+0.31% last 5m)  <- transcript lines just before
    SUMMARY hh:mm:ss  table of every contract vs the speech-start baseline
    END     reason
--log gets everything: every new transcript line, every tick's table.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf

ET = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "alerts.sqlite3"

# contract -> (label, notable move since baseline %, notable 5-minute move %)
CONTRACTS = {
    "ES=F": ("S&P 500", 0.30, 0.20),
    "NQ=F": ("Nasdaq 100", 0.35, 0.25),
    "RTY=F": ("Russell 2000", 0.40, 0.30),
    "ZN=F": ("10y Treasury", 0.15, 0.10),
    "CL=F": ("WTI crude", 0.60, 0.40),
    "HO=F": ("Heating oil (diesel)", 0.60, 0.40),
    "RB=F": ("Gasoline", 0.60, 0.40),
    "NG=F": ("Nat gas", 1.00, 0.60),
    "ZC=F": ("Corn", 0.60, 0.40),
    "ZS=F": ("Soybeans", 0.60, 0.40),
    "ZW=F": ("Wheat", 0.60, 0.40),
    "GC=F": ("Gold", 0.40, 0.25),
    "HG=F": ("Copper", 0.60, 0.40),
    "DX=F": ("Dollar index", 0.20, 0.12),
}


class Out:
    def __init__(self, events: Path | None, log: Path | None) -> None:
        self.ev = open(events, "a", buffering=1) if events else None
        self.lg = open(log, "a", buffering=1) if log else None

    def event(self, line: str) -> None:
        print(line, flush=True)
        if self.ev:
            self.ev.write(line + "\n")
        self.log(line)

    def log(self, line: str) -> None:
        if self.lg:
            self.lg.write(line + "\n")


def listener_live(conn: sqlite3.Connection, since_ts: float) -> tuple[bool, float | None]:
    row = conn.execute("SELECT MAX(ended_at), SUM(ended_at IS NULL) FROM runs WHERE started_at >= ?", (since_ts,)).fetchone()
    return bool(row[1]), row[0]


def new_segments(conn: sqlite3.Connection, after: float, since_ts: float) -> list[tuple]:
    return conn.execute(
        "SELECT s.t_wall, COALESCE(s.speaker_label,''), s.text FROM segments s JOIN runs r ON r.id = s.run_id "
        "WHERE r.started_at >= ? AND s.t_wall > ? ORDER BY s.t_wall", (since_ts, after)).fetchall()


def new_alerts(conn: sqlite3.Connection, after: float) -> list[tuple]:
    return conn.execute(
        "SELECT t_alert, state, entity, tickers, stance, action, quote, summary FROM alerts "
        "WHERE t_alert > ? AND state IN ('confirmed','retracted') ORDER BY t_alert", (after,)).fetchall()


def fetch(symbols: list[str]) -> dict[str, pd.Series]:
    df = yf.download(symbols, period="1d", interval="1m", prepost=True, auto_adjust=False,
                     progress=False, group_by="ticker", threads=True)
    out = {}
    for s in symbols:
        try:
            ser = df[s]["Close"].dropna() if isinstance(df.columns, pd.MultiIndex) else df["Close"].dropna()
        except KeyError:
            continue
        if ser.empty:
            continue
        ser.index = ser.index.tz_convert(ET)
        out[s] = ser
    return out


def at_or_after(ser: pd.Series, t: datetime) -> float | None:
    sub = ser[ser.index >= t]
    return float(sub.iloc[0]) if not sub.empty else None


def at_or_before(ser: pd.Series, t: datetime) -> float | None:
    sub = ser[ser.index <= t]
    return float(sub.iloc[-1]) if not sub.empty else None


def pct(a: float | None, b: float | None) -> float | None:
    return None if a is None or b is None or a == 0 else (b / a - 1) * 100


def fmt(p: float | None) -> str:
    return "   n/a " if p is None else f"{p:+6.2f}%"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help='speech start, ET "YYYY-MM-DD HH:MM"')
    ap.add_argument("--interval", type=float, default=90)
    ap.add_argument("--summary-every", type=float, default=600)
    ap.add_argument("--idle-exit", type=float, default=600, help="exit this long after the listener detaches")
    ap.add_argument("--max-hours", type=float, default=4)
    ap.add_argument("--events", default=None)
    ap.add_argument("--log", default=None)
    args = ap.parse_args()

    since = datetime.strptime(args.since, "%Y-%m-%d %H:%M").replace(tzinfo=ET)
    since_ts = since.timestamp() - 1800  # runs that started up to 30 min before the speech
    out = Out(Path(args.events) if args.events else None, Path(args.log) if args.log else None)
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)

    seg_after = since.timestamp()
    alert_after = time.time()  # only alerts from now on; earlier ones were reported already
    recent_lines: list[tuple[float, str]] = []
    base: dict[str, float] = {}
    last_summary = 0.0
    flagged: dict[str, float] = {}  # contract -> last flagged move, to avoid repeating
    t_start = time.time()
    out.event(f"START   {datetime.now(ET):%H:%M:%S}  watching transcript + {len(CONTRACTS)} futures, baseline {since:%H:%M} ET")

    while True:
        now = datetime.now(ET)
        live, ended_at = listener_live(conn, since_ts)

        for t_wall, label, text in new_segments(conn, seg_after, since_ts):
            seg_after = max(seg_after, t_wall)
            line = f"{datetime.fromtimestamp(t_wall, ET):%H:%M:%S} {label or ' '} {text}"
            out.log("TXT " + line)
            recent_lines.append((t_wall, line))
        recent_lines = [(t, l) for t, l in recent_lines if t > time.time() - 900]

        for t_alert, state, entity, tickers, stance, action, quote, summary in new_alerts(conn, alert_after):
            alert_after = max(alert_after, t_alert)
            tk = " ".join(json.loads(tickers or "[]")[:4])
            if state == "confirmed":
                out.event(f"ALERT   {datetime.fromtimestamp(t_alert, ET):%H:%M:%S}  {entity} [{tk}] {stance}/{action}  \"{(quote or '')[:90]}\"  {summary or ''}")
            else:
                out.log(f"RETRACT {datetime.fromtimestamp(t_alert, ET):%H:%M:%S}  {entity} [{tk}]")

        try:
            series = fetch(list(CONTRACTS))
        except Exception as exc:  # noqa: BLE001
            out.log(f"WARN fetch failed: {str(exc)[:120]}")
            series = {}

        rows = []
        for sym, (label, thr_base, thr_5m) in CONTRACTS.items():
            ser = series.get(sym)
            if ser is None:
                continue
            if sym not in base:
                b = at_or_before(ser, since) or at_or_after(ser, since)
                if b is not None:
                    base[sym] = b
            last_t = ser.index[-1].to_pydatetime()
            last = float(ser.iloc[-1])
            prev5 = at_or_before(ser, last_t - timedelta(minutes=5))
            p_base, p_5 = pct(base.get(sym), last), pct(prev5, last)
            stale = last_t < since  # market closed since before the speech (grains before 20:00)
            rows.append((sym, label, last_t, last, p_base, p_5, stale))
            if stale or p_base is None:
                continue
            notable = abs(p_base) >= thr_base or (p_5 is not None and abs(p_5) >= thr_5m)
            if notable and abs(p_base - flagged.get(sym, 0.0)) >= thr_5m / 2:
                flagged[sym] = p_base
                ctx = [l for t, l in recent_lines if t >= (last_t - timedelta(minutes=6)).timestamp() and t <= last_t.timestamp()]
                out.event(f"MOVE    {now:%H:%M:%S}  {label} {sym} {fmt(p_base)} since {since:%H:%M} ({fmt(p_5)} last 5m) bar {last_t:%H:%M}")
                for l in ctx[-4:]:
                    out.event(f"        | {l[:140]}")

        table = "\n".join(
            f"  {label:22} {sym:6} {last:10.3f}  since {since:%H:%M} {fmt(pb)}  5m {fmt(p5)}  bar {t:%H:%M}{'  (closed)' if stale else ''}"
            for sym, label, t, last, pb, p5, stale in rows)
        out.log(f"TICK {now:%H:%M:%S} listener={'live' if live else 'detached'}\n{table}")
        if time.time() - last_summary >= args.summary_every:
            last_summary = time.time()
            out.event(f"SUMMARY {now:%H:%M:%S} listener={'live' if live else 'detached'} transcript lines in last 15m: {len(recent_lines)}\n{table}")

        if not live and ended_at and time.time() - ended_at > args.idle_exit:
            out.event(f"END     {now:%H:%M:%S}  listener detached at {datetime.fromtimestamp(ended_at, ET):%H:%M:%S}, no new stream for {args.idle_exit/60:.0f} min")
            return
        if time.time() - t_start > args.max_hours * 3600:
            out.event(f"END     {now:%H:%M:%S}  max runtime reached")
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("END     interrupted", flush=True)
