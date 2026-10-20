from datetime import date, datetime

from backtest.marketclock import TradingCalendar, anchor_for, finest_interval_for, market_state, parse_event_start, to_et
from backtest.models import ET
from tests.conftest import make_calendar


def dt(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=ET)


def test_calendar_navigation():
    cal = TradingCalendar(make_calendar())
    assert cal.is_trading_day(date(2026, 9, 4))
    assert not cal.is_trading_day(date(2026, 9, 5))  # Saturday
    assert not cal.is_trading_day(date(2026, 9, 7))  # Labor Day
    assert cal.next_session(date(2026, 9, 4)) == date(2026, 9, 8)
    assert cal.next_session(date(2026, 9, 5)) == date(2026, 9, 8)
    assert cal.prev_session(date(2026, 9, 8)) == date(2026, 9, 4)
    assert cal.offset(date(2026, 9, 4), 5) == date(2026, 9, 14)
    assert cal.offset(date(2026, 9, 4), 0) == date(2026, 9, 4)


def test_market_state():
    cal = TradingCalendar(make_calendar())
    assert market_state(dt(2026, 9, 4, 9, 30), cal) == "open"
    assert market_state(dt(2026, 9, 4, 15, 59), cal) == "open"
    assert market_state(dt(2026, 9, 4, 16, 0), cal) == "closed"
    assert market_state(dt(2026, 9, 4, 9, 29), cal) == "closed"
    assert market_state(dt(2026, 9, 5, 12, 0), cal) == "closed"
    assert market_state(dt(2026, 9, 7, 12, 0), cal) == "closed"


def test_anchor_open_and_closed_variants():
    cal = TradingCalendar(make_calendar())
    a = anchor_for(dt(2026, 9, 4, 11, 7), cal)
    assert a.state == "open" and a.session == date(2026, 9, 4) and a.origin == dt(2026, 9, 4, 11, 7) and a.baseline_day is None
    # after close on Friday -> Tuesday (Monday holiday), baseline Friday close
    a = anchor_for(dt(2026, 9, 4, 17, 30), cal)
    assert a.state == "closed" and a.session == date(2026, 9, 8) and a.origin == dt(2026, 9, 8, 9, 30) and a.baseline_day == date(2026, 9, 4)
    # pre-market on a trading day -> same day's open, baseline previous session
    a = anchor_for(dt(2026, 9, 8, 8, 0), cal)
    assert a.state == "closed" and a.session == date(2026, 9, 8) and a.baseline_day == date(2026, 9, 4)
    # weekend
    a = anchor_for(dt(2026, 9, 6, 12, 0), cal)
    assert a.session == date(2026, 9, 8)


def test_utc_conversion_and_event_start():
    t = to_et(1787165378)  # 2026-08-19 18:49:38 UTC
    assert (t.year, t.month, t.day, t.hour, t.minute) == (2026, 8, 19, 14, 49)
    assert parse_event_start("2025-04-02T16:00").utcoffset().total_seconds() == -4 * 3600
    assert parse_event_start("2025-04-02T20:00+00:00").hour == 16


def test_finest_interval():
    today = date(2026, 9, 15)
    assert finest_interval_for(date(2026, 9, 10), today) == ["1m", "5m", "60m"]
    assert finest_interval_for(date(2026, 8, 1), today) == ["5m", "60m"]
    assert finest_interval_for(date(2025, 8, 1), today) == ["60m"]
    assert finest_interval_for(date(2024, 1, 1), today) == []
