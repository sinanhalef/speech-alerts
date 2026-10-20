from __future__ import annotations

from datetime import date, datetime, timedelta

import pandas as pd
import pytest

from backtest.marketclock import TradingCalendar
from backtest.models import ET
from backtest.prices import COLUMNS, PriceStore


def make_calendar(start: date = date(2026, 8, 3), end: date = date(2026, 9, 30), holidays: set[date] | None = None) -> list[date]:
    holidays = holidays or {date(2026, 9, 7)}  # Labor Day 2026
    days = []
    d = start
    while d <= end:
        if d.weekday() < 5 and d not in holidays:
            days.append(d)
        d += timedelta(days=1)
    return days


class FakeStore(PriceStore):
    """PriceStore with synthetic bars: price = base + minutes since 09:30 * slope (intraday),
    daily close = base + day index. No network."""

    def __init__(self, today: date = date(2026, 9, 15), bases: dict[str, float] | None = None, slopes: dict[str, float] | None = None,
                 intraday_days: int = 60):
        self.today = today
        self.days = make_calendar()
        self.bases = bases or {"SPY": 500.0, "AAA": 100.0}
        self.slopes = slopes or {"SPY": 0.0, "AAA": 0.01}
        self.intraday_days = intraday_days
        self._mem = {}
        self._calendar = None
        self.calls: list[tuple] = []

    def daily(self, ticker: str) -> pd.DataFrame:
        from backtest.prices import NoData
        if ticker not in self.bases:
            raise NoData(ticker)
        base = self.bases[ticker]
        rows = []
        for i, d in enumerate(self.days):
            if d > self.today:
                break
            close = base + i
            rows.append({"Open": close - 0.5, "High": close + 1, "Low": close - 1, "Close": close, "Volume": 1000})
        df = pd.DataFrame(rows, index=pd.Index([d for d in self.days if d <= self.today], name="date"))
        return df[COLUMNS]

    def intraday(self, ticker: str, day: date, interval: str) -> pd.DataFrame:
        self.calls.append((ticker, day, interval))
        if ticker not in self.bases or day not in self.days or (self.today - day).days > self.intraday_days:
            return pd.DataFrame(columns=COLUMNS)
        step = {"1m": 1, "5m": 5, "60m": 60}[interval]
        base = self.bases[ticker] + self.days.index(day)
        slope = self.slopes[ticker]
        idx, rows = [], []
        t = datetime.combine(day, datetime.min.time(), tzinfo=ET).replace(hour=9, minute=30)
        end = t.replace(hour=16, minute=0)
        # Anchored so the day's last bar closes exactly at the daily close (base): price(m) = base + (m - 390) * slope
        while t < end:
            mins = (t - t.replace(hour=9, minute=30)).total_seconds() / 60
            open_ = base + (mins - 390) * slope
            close = base + (mins + step - 390) * slope
            rows.append({"Open": open_, "High": max(open_, close), "Low": min(open_, close), "Close": close, "Volume": 10})
            idx.append(t)
            t += timedelta(minutes=step)
        df = pd.DataFrame(rows, index=pd.DatetimeIndex(idx, name="t"))
        return df[COLUMNS]

    def calendar(self) -> TradingCalendar:
        return TradingCalendar(self.days)


@pytest.fixture
def store() -> FakeStore:
    return FakeStore()
