"""Price reaction per signal x ticker x horizon, SPY-adjusted.

Baseline P0: during the session, the close of the last *completed* bar before the mention (no
look-ahead); outside the session, the previous session's close. Intraday horizons use the finest
bar interval Yahoo still serves that is no coarser than the horizon; daily horizons use closes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta

import pandas as pd

from backtest.marketclock import (
    INTERVAL_MINUTES, Anchor, TradingCalendar, anchor_for, finest_interval_for, session_close, to_et,
)
from backtest.models import DAILY_OFFSETS, HORIZONS, INTRADAY_MINUTES, Signal, SignalFile
from backtest.prices import NoData, PriceStore

log = logging.getLogger(__name__)

BENCH = "SPY"


@dataclass
class Px:
    price: float | None
    when: str | None
    resolution: str | None
    reason: str | None = None


class Measurer:
    def __init__(self, store: PriceStore) -> None:
        self.store = store
        self.cal: TradingCalendar = store.calendar()
        self._aligned: dict[tuple, pd.DataFrame] = {}

    # ---------- bar helpers ----------

    def _bars(self, ticker: str, day: date, interval: str) -> pd.DataFrame:
        """Intraday bars aligned to the daily (split-adjusted) price basis.

        Yahoo's daily closes are adjusted for later splits, its historical intraday bars are not;
        a closed-market baseline (daily) compared with next-morning bars would then show the split
        as a return. If the day's last bar and the daily close disagree by more than 2 %, the bars
        are rescaled by the exact ratio."""
        key = (ticker, day, interval)
        if key in self._aligned:
            return self._aligned[key]
        try:
            df = self.store.intraday(ticker, day, interval)
        except Exception as exc:  # noqa: BLE001
            log.warning("%s %s %s: %s", ticker, interval, day, exc)
            df = pd.DataFrame()
        if not df.empty:
            daily = self.daily_close(ticker, day)
            last = float(df.iloc[-1]["Close"])
            if daily.price and last and abs(daily.price / last - 1) > 0.02:
                ratio = daily.price / last
                log.info("%s %s: intraday bars rescaled by %.4f to the split-adjusted daily basis", ticker, day, ratio)
                df = df.copy()
                for c in ("Open", "High", "Low", "Close"):
                    df[c] = df[c] * ratio
        self._aligned[key] = df
        return df

    def price_at(self, ticker: str, t: datetime, *, max_interval_min: int | None, prefer: list[str]) -> Px:
        """Close of the last completed bar at or before t, using the finest usable interval."""
        if t > session_close(t.date()):
            return Px(None, None, None, "after_close")
        gap: Px | None = None
        for interval in prefer:
            mins = INTERVAL_MINUTES[interval]
            if max_interval_min is not None and mins > max_interval_min:
                continue
            df = self._bars(ticker, t.date(), interval)
            if df.empty:
                continue
            done = df[df.index <= t - timedelta(minutes=mins)]
            if done.empty:
                # Before the first completed bar (e.g. 09:31 with 5m bars): fall back to the day's open.
                first = df.index[0]
                if first <= t:
                    return Px(float(df.iloc[0]["Open"]), first.isoformat(), interval + "/open")
                continue
            last = done.index[-1]
            if t - last > timedelta(minutes=3 * mins) + timedelta(minutes=5):
                gap = Px(None, last.isoformat(), interval, "gap")
                continue  # thin ticker: try the next coarser interval
            return Px(float(done.iloc[-1]["Close"]), last.isoformat(), interval)
        return gap if gap else Px(None, None, None, "no_intraday")

    def daily_close(self, ticker: str, day: date) -> Px:
        try:
            df = self.store.daily(ticker)
        except NoData:
            return Px(None, None, None, "no_data")
        if day not in df.index:
            return Px(None, str(day), "1d", "no_bar")
        return Px(float(df.loc[day, "Close"]), str(day), "1d")

    def daily_open(self, ticker: str, day: date) -> Px:
        try:
            df = self.store.daily(ticker)
        except NoData:
            return Px(None, None, None, "no_data")
        if day not in df.index:
            return Px(None, str(day), "1d", "no_bar")
        return Px(float(df.loc[day, "Open"]), str(day), "1d/open")

    # ---------- per signal ----------

    def rows_for(self, sf: SignalFile, sig: Signal, ticker: str, *, primary: bool, source: str, first_mention: bool) -> list[dict]:
        base = {
            "video_id": sf.video.id, "video_label": sf.video.label or sf.video.title[:60], "group": sf.video.group,
            "signal_id": sig.signal_id, "entity": sig.entity, "kind": sig.kind, "ticker": ticker, "primary": primary,
            "ticker_source": source, "first_mention": first_mention, "t_audio": round(sig.t_audio, 1),
            "t_wall_et": sig.t_wall_et, "speaker_is_main": sig.speaker_is_main,
            "stance": sig.llm.stance if sig.llm else None, "action": sig.llm.action if sig.llm else None,
            "llm_confidence": sig.llm.confidence if sig.llm else None,
            "stance_dir": sig.stance_direction(), "judge_dir": sig.judge_direction(ticker),
        }
        je = sig.judge_entry(ticker)
        base.update({
            "judge_confidence": je.confidence if je else None, "novelty": je.novelty if je else None,
            "magnitude": je.magnitude if je else None,
        })
        if sig.t_wall is None:
            return [dict(base, horizon=h, reason="no_wall_clock") for h in HORIZONS]
        t = to_et(sig.t_wall)
        anchor = anchor_for(t, self.cal)
        if anchor is None:
            return [dict(base, horizon=h, reason="no_session") for h in HORIZONS]
        base.update({"market_state": anchor.state, "session": str(anchor.session), "origin_et": anchor.origin.isoformat()})
        prefer = finest_interval_for(anchor.session, self.store.today)
        try:
            self.store.daily(ticker)
        except NoData:
            return [dict(base, horizon=h, reason="no_data") for h in HORIZONS]

        rows = []
        for h in HORIZONS:
            rows.append(dict(base, horizon=h, **self._horizon(ticker, anchor, h, prefer)))
        return rows

    def _baseline(self, ticker: str, anchor: Anchor, prefer: list[str], *, max_interval_min: int | None) -> tuple[Px, str]:
        if anchor.state == "open":
            px = self.price_at(ticker, anchor.origin, max_interval_min=max_interval_min, prefer=prefer)
            if px.price is not None:
                return px, "last_completed_bar"
            prev = self.cal.prev_session(anchor.session)
            return (self.daily_close(ticker, prev) if prev else Px(None, None, None, "no_prev")), "prev_close_fallback"
        assert anchor.baseline_day is not None
        return self.daily_close(ticker, anchor.baseline_day), "prev_close"

    def _horizon(self, ticker: str, anchor: Anchor, h: str, prefer: list[str]) -> dict:
        out: dict = {}
        if h == "open":
            if anchor.state != "closed":
                return {"reason": "n/a_open_state"}
            p0, kind = self._baseline(ticker, anchor, prefer, max_interval_min=None)
            ph = self.daily_open(ticker, anchor.session)
            b0, _ = self._baseline(BENCH, anchor, prefer, max_interval_min=None)
            bh = self.daily_open(BENCH, anchor.session)
            return self._fill(out, p0, ph, b0, bh, kind, ph.resolution or "1d/open")
        if h in INTRADAY_MINUTES:
            mins = INTRADAY_MINUTES[h]
            usable = [i for i in prefer if INTERVAL_MINUTES[i] <= mins]
            if not usable:
                return {"reason": "no_bars_fine_enough"}
            t_h = anchor.origin + timedelta(minutes=mins)
            p0, kind = self._baseline(ticker, anchor, usable, max_interval_min=mins)
            ph = self.price_at(ticker, t_h, max_interval_min=mins, prefer=usable)
            b0, _ = self._baseline(BENCH, anchor, usable, max_interval_min=mins)
            bh = self.price_at(BENCH, t_h, max_interval_min=mins, prefer=usable)
            return self._fill(out, p0, ph, b0, bh, kind, ph.resolution)
        n = DAILY_OFFSETS[h]
        day = self.cal.offset(anchor.session, n)
        if day is None or day > self.store.today:
            return {"reason": "not_yet"}
        p0, kind = self._baseline(ticker, anchor, prefer, max_interval_min=None)
        ph = self.daily_close(ticker, day)
        b0, _ = self._baseline(BENCH, anchor, prefer, max_interval_min=None)
        bh = self.daily_close(BENCH, day)
        return self._fill(out, p0, ph, b0, bh, kind, "1d")

    @staticmethod
    def _fill(out: dict, p0: Px, ph: Px, b0: Px, bh: Px, baseline_kind: str, resolution: str | None) -> dict:
        out.update({
            "baseline_kind": baseline_kind, "baseline_resolution": p0.resolution, "resolution": resolution,
            "p0": p0.price, "p0_at": p0.when, "p_h": ph.price, "p_h_at": ph.when,
            "spy_p0": b0.price, "spy_p_h": bh.price,
        })
        if p0.price is None or ph.price is None:
            out["reason"] = p0.reason or ph.reason or "missing"
            return out
        ret = ph.price / p0.price - 1
        out["ret"] = ret
        if b0.price and bh.price:
            spy_ret = bh.price / b0.price - 1
            out["spy_ret"] = spy_ret
            out["abn_ret"] = ret - spy_ret
        else:
            out["spy_ret"] = None
            out["abn_ret"] = None
            out["reason"] = "no_benchmark"
        return out


def _hit(direction: str, value: float | None) -> bool | None:
    if value is None or direction not in ("up", "down") or pd.isna(value):
        return None
    return (value > 0) if direction == "up" else (value < 0)


def measure_files(files: list[SignalFile], store: PriceStore, *, include_retracted: bool = False) -> pd.DataFrame:
    m = Measurer(store)
    rows: list[dict] = []
    for sf in files:
        seen_first: set[tuple[str, str]] = set()
        sigs = sorted(sf.signals, key=lambda s: s.t_audio)
        for sig in sigs:
            if sig.state != "confirmed" and not include_retracted:
                continue
            primary = sig.primary_ticker
            llm_t = {t.upper() for t in (sig.llm.tickers if sig.llm else [])}
            dict_t = {t.upper() for t in sig.dict_tickers}
            for ticker in sig.all_tickers():
                src = "llm" if ticker in llm_t else ("dict" if ticker in dict_t else "judge")
                key = (sf.video.id, ticker)
                first = key not in seen_first
                seen_first.add(key)
                for row in m.rows_for(sf, sig, ticker, primary=(ticker == primary), source=src, first_mention=first):
                    row["state"] = sig.state
                    row["hit_stance"] = _hit(row.get("stance_dir", "none"), row.get("abn_ret"))
                    row["hit_judge"] = _hit(row.get("judge_dir", "none"), row.get("abn_ret"))
                    rows.append(row)
    cols = [
        "video_id", "video_label", "group", "signal_id", "entity", "kind", "ticker", "primary", "ticker_source",
        "first_mention", "state", "t_audio", "t_wall_et", "speaker_is_main", "market_state", "session", "origin_et",
        "stance", "action", "llm_confidence", "stance_dir", "judge_dir", "judge_confidence", "novelty", "magnitude",
        "horizon", "baseline_kind", "baseline_resolution", "resolution", "p0", "p0_at", "p_h", "p_h_at",
        "spy_p0", "spy_p_h", "ret", "spy_ret", "abn_ret", "hit_stance", "hit_judge", "reason",
    ]
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns:
            df[c] = None
    return df[cols]
