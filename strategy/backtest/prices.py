"""Yahoo Finance price loader with an on-disk CSV cache and retry.

Yahoo limits (verified 2026-09-15): 1m bars for the last ~30 days, 5m for ~60 days, 60m for
~730 days, daily unlimited. Intraday frames are indexed by tz-aware ET timestamps (bar start),
daily frames by date. Regular session only (prepost=False), unadjusted closes.
"""

from __future__ import annotations

import logging
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

from backtest.marketclock import TradingCalendar
from backtest.models import ET

log = logging.getLogger(__name__)

DAILY_START = date(2024, 11, 1)
COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


class NoData(Exception):
    pass


class PriceStore:
    def __init__(self, cache_dir: Path, *, today: date | None = None, sleep: float = 0.5) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.today = today or datetime.now(ET).date()
        self.sleep = sleep
        self._mem: dict[str, pd.DataFrame] = {}
        self._calendar: TradingCalendar | None = None

    # ---------- public ----------

    def daily(self, ticker: str) -> pd.DataFrame:
        """Daily bars from DAILY_START to today, indexed by date."""
        key = f"{ticker}_1d_{DAILY_START}_{self.today}"
        if key in self._mem:
            return self._mem[key]
        path = self.cache_dir / f"{key}.csv"
        if path.exists():
            df = self._read(path, intraday=False)
        else:
            df = self._fetch(ticker, start=DAILY_START, end=self.today + timedelta(days=1), interval="1d")
            df = self._normalize_daily(df)
            self._write(path, df)
        self._mem[key] = df
        if df.empty:
            raise NoData(f"{ticker}: no daily data")
        return df

    def intraday(self, ticker: str, day: date, interval: str) -> pd.DataFrame:
        """Regular-session bars for one date at the given interval (1m/5m/60m), ET index."""
        key = f"{ticker}_{interval}_{day}"
        if key in self._mem:
            return self._mem[key]
        path = self.cache_dir / f"{key}.csv"
        if path.exists():
            df = self._read(path, intraday=True)
        else:
            df = self._fetch(ticker, start=day, end=day + timedelta(days=1), interval=interval)
            df = self._normalize_intraday(df, day)
            self._write(path, df)
        self._mem[key] = df
        return df

    def calendar(self) -> TradingCalendar:
        if self._calendar is None:
            spy = self.daily("SPY")
            self._calendar = TradingCalendar(list(spy.index))
        return self._calendar

    # ---------- fetch ----------

    def _fetch(self, ticker: str, *, start: date, end: date, interval: str) -> pd.DataFrame:
        import yfinance as yf

        delays = [3, 10, 30, 60]
        last: Exception | None = None
        for attempt in range(len(delays) + 1):
            try:
                df = yf.Ticker(ticker).history(
                    start=start.isoformat(), end=end.isoformat(), interval=interval,
                    prepost=False, auto_adjust=False, actions=False, raise_errors=True,
                )
                time.sleep(self.sleep)
                return df
            except Exception as exc:  # noqa: BLE001
                msg = str(exc)
                last = exc
                # Yahoo reports "no data" style problems as exceptions too; only retry on limits/network.
                transient = any(s in msg.lower() for s in ("too many", "rate", "timed out", "timeout", "connection", "429", "5xx"))
                if not transient or attempt == len(delays):
                    if not transient:
                        log.info("%s %s %s..%s: %s", ticker, interval, start, end, msg[:120])
                        return pd.DataFrame(columns=COLUMNS)
                    break
                log.warning("yahoo transient error for %s (%s); retry in %ss", ticker, msg[:80], delays[attempt])
                time.sleep(delays[attempt])
        raise RuntimeError(f"yahoo fetch failed for {ticker} {interval}: {last}")

    # ---------- normalize / io ----------

    @staticmethod
    def _normalize_daily(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)
        out = df[COLUMNS].copy()
        idx = pd.to_datetime(out.index)
        out.index = pd.Index([d.date() for d in idx], name="date")
        out = out[~out.index.duplicated(keep="last")]
        return out.dropna(subset=["Close"])

    @staticmethod
    def _normalize_intraday(df: pd.DataFrame, day: date) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)
        out = df[COLUMNS].copy()
        idx = pd.to_datetime(out.index)
        if idx.tz is None:
            idx = idx.tz_localize("UTC")
        out.index = idx.tz_convert(ET)
        out.index.name = "t"
        out = out[[t.date() == day for t in out.index]]
        return out.dropna(subset=["Close"])

    @staticmethod
    def _write(path: Path, df: pd.DataFrame) -> None:
        df.to_csv(path)

    @staticmethod
    def _read(path: Path, *, intraday: bool) -> pd.DataFrame:
        df = pd.read_csv(path, index_col=0)
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)
        if intraday:
            df.index = pd.to_datetime(df.index, utc=True).tz_convert(ET)
            df.index.name = "t"
        else:
            df.index = pd.Index([d.date() for d in pd.to_datetime(df.index)], name="date")
        return df[COLUMNS]
