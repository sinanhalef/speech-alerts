"""US equity market clock: ET conversion, trading-day calendar, market state and horizon anchors.

The calendar is derived from the dates present in SPY daily bars (see prices.py), so no
exchange-calendar dependency is needed. Regular session: 09:30-16:00 ET. Early closes are handled
downstream by "last bar of the session"; the session end used here is always 16:00.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from bisect import bisect_left, bisect_right

from backtest.models import ET

OPEN = time(9, 30)
CLOSE = time(16, 0)


def to_et(epoch: float) -> datetime:
    return datetime.fromtimestamp(epoch, ET)


def parse_event_start(text: str) -> datetime:
    """ISO datetime; naive values are taken as ET."""
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ET)
    return dt.astimezone(ET)


class TradingCalendar:
    def __init__(self, days: list[date]) -> None:
        self.days = sorted(set(days))
        if not self.days:
            raise ValueError("empty trading calendar")

    def is_trading_day(self, d: date) -> bool:
        i = bisect_left(self.days, d)
        return i < len(self.days) and self.days[i] == d

    def next_session(self, d: date, *, inclusive: bool = False) -> date | None:
        """First trading day > d (or >= d when inclusive)."""
        i = bisect_left(self.days, d) if inclusive else bisect_right(self.days, d)
        return self.days[i] if i < len(self.days) else None

    def prev_session(self, d: date, *, inclusive: bool = False) -> date | None:
        """Last trading day < d (or <= d when inclusive)."""
        i = bisect_right(self.days, d) if inclusive else bisect_left(self.days, d)
        return self.days[i - 1] if i > 0 else None

    def offset(self, d: date, n: int) -> date | None:
        """Trading day n sessions after d (d must be a trading day)."""
        i = bisect_left(self.days, d)
        if i >= len(self.days) or self.days[i] != d:
            raise ValueError(f"{d} is not a trading day")
        j = i + n
        return self.days[j] if 0 <= j < len(self.days) else None


def session_open(d: date) -> datetime:
    return datetime.combine(d, OPEN, tzinfo=ET)


def session_close(d: date) -> datetime:
    return datetime.combine(d, CLOSE, tzinfo=ET)


def market_state(dt: datetime, cal: TradingCalendar) -> str:
    dt = dt.astimezone(ET)
    if not cal.is_trading_day(dt.date()):
        return "closed"
    return "open" if OPEN <= dt.time() < CLOSE else "closed"


@dataclass(frozen=True)
class Anchor:
    """Where the measurement clock starts for a mention.

    state:          "open" (mention during the regular session) or "closed".
    session:        the session used for intraday horizons (mention day, or the next session).
    origin:         intraday clock origin: mention time (open) or that session's 09:30 (closed).
    baseline_day:   session whose close is the baseline when closed (previous session).
    """

    state: str
    session: date
    origin: datetime
    baseline_day: date | None


def anchor_for(dt: datetime, cal: TradingCalendar) -> Anchor | None:
    dt = dt.astimezone(ET)
    state = market_state(dt, cal)
    if state == "open":
        return Anchor(state="open", session=dt.date(), origin=dt, baseline_day=None)
    # Closed: pre-market on a trading day -> that day's open; otherwise next trading day.
    if cal.is_trading_day(dt.date()) and dt.time() < OPEN:
        session = dt.date()
    else:
        session = cal.next_session(dt.date())
    if session is None:
        return None
    baseline_day = cal.prev_session(session)
    if baseline_day is None:
        return None
    return Anchor(state="closed", session=session, origin=session_open(session), baseline_day=baseline_day)


def days_ago(d: date, today: date | None = None) -> int:
    return ((today or datetime.now(ET).date()) - d).days


def finest_interval_for(d: date, today: date | None = None) -> list[str]:
    """Intraday intervals Yahoo can still serve for a session date, finest first."""
    age = days_ago(d, today)
    out: list[str] = []
    if age <= 28:
        out.append("1m")
    if age <= 58:
        out.append("5m")
    if age <= 725:
        out.append("60m")
    return out


INTERVAL_MINUTES = {"1m": 1, "5m": 5, "60m": 60}


def week_later(d: date) -> date:
    return d + timedelta(days=7)
