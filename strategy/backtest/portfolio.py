"""$10k portfolio simulation: buy what the President mentioned positively, sell five sessions later.

Entry rules
  instant:   market open at the mention -> last completed bar before the mention;
             market closed -> the next session's opening print.
  next_open: always the first opening print after the mention (in-hours mentions wait for the
             next morning).
Exit: close of the 5th trading session after the entry session.

Portfolio accounting is calendar-time with daily equal-weight rebalancing: each trading day the
equity is split evenly across the positions open that day, so overlapping trades share the money
and there is never more than 100 % invested. Days with no open position earn nothing. Costs and
slippage are ignored. A second, naive figure ("equal split") puts $10k / N into each of the N
trades independently and sums the profits (no compounding, no capital constraint).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, datetime

import pandas as pd

from backtest.marketclock import anchor_for, finest_interval_for, to_et
from backtest.measure import Measurer
from backtest.models import ET, Signal, SignalFile
from backtest.prices import NoData, PriceStore

HOLD_SESSIONS = 5
START_CASH = 10_000.0


@dataclass
class Trade:
    signal_id: str
    video: str
    ticker: str
    entity: str
    quote: str
    mention_et: str
    entry_rule: str
    entry_day: date
    entry_price: float
    entry_kind: str
    exit_day: date
    exit_price: float
    path: list[tuple[date, float]] = field(default_factory=list)  # closes from entry day to exit day

    @property
    def ret(self) -> float:
        return self.exit_price / self.entry_price - 1


def _entry(m: Measurer, sig: Signal, ticker: str, rule: str) -> tuple[date, float, str] | None:
    if sig.t_wall is None:
        return None
    t = to_et(sig.t_wall)
    anchor = anchor_for(t, m.cal)
    if anchor is None:
        return None
    if rule == "instant" and anchor.state == "open":
        prefer = finest_interval_for(anchor.session, m.store.today)
        px = m.price_at(ticker, anchor.origin, max_interval_min=None, prefer=prefer)
        if px.price is not None:
            return anchor.session, px.price, f"mention ({px.resolution})"
        # no intraday bars: fall back to the next open like the closed case
    session = anchor.session if anchor.state == "closed" else m.cal.next_session(anchor.session)
    if session is None:
        return None
    px = m.daily_open(ticker, session)
    if px.price is None:
        return None
    return session, px.price, "next open"


def build_trades(files: list[SignalFile], store: PriceStore, *, select: str, rule: str) -> tuple[list[Trade], dict]:
    """select: stance_up | judge_up | judge_up_new"""
    m = Measurer(store)
    trades: list[Trade] = []
    skipped = {"no_data": 0, "not_yet": 0, "no_entry": 0}
    for sf in files:
        seen: set[str] = set()
        for sig in sorted(sf.signals, key=lambda s: s.t_audio):
            if sig.state != "confirmed":
                continue
            ticker = sig.primary_ticker
            if not ticker or ticker in seen:
                continue
            if select == "stance_up" and sig.stance_direction() != "up":
                continue
            if select == "company_invest" and not (sig.stance_direction() == "up" and sig.kind == "company"
                                                   and sig.llm and sig.llm.action in ("investment", "deal")):
                continue
            if select == "company_invest_closed":
                from backtest.marketclock import anchor_for, to_et
                ok = sig.stance_direction() == "up" and sig.kind == "company" and sig.llm and sig.llm.action in ("investment", "deal")
                if ok and sig.t_wall is not None:
                    a = anchor_for(to_et(sig.t_wall), m.cal)
                    ok = a is not None and a.state == "closed"
                if not ok:
                    continue
            if select == "present":
                from backtest.influence import PRESENT
                if not (sig.stance_direction() == "up" and PRESENT.search(sig.context or "")):
                    continue
            if select in ("judge_up", "judge_up_new") and sig.judge_direction(ticker) != "up":
                continue
            if select == "judge_up_new":
                je = sig.judge_entry(ticker)
                if not je or je.novelty != "new":
                    continue
            seen.add(ticker)
            try:
                daily = store.daily(ticker)
            except NoData:
                skipped["no_data"] += 1
                continue
            ent = _entry(m, sig, ticker, rule)
            if ent is None:
                skipped["no_entry"] += 1
                continue
            entry_day, entry_price, kind = ent
            exit_day = m.cal.offset(entry_day, HOLD_SESSIONS)
            if exit_day is None or exit_day > store.today or exit_day not in daily.index:
                skipped["not_yet"] += 1
                continue
            path = [(d, float(daily.loc[d, "Close"])) for d in m.cal.days if entry_day <= d <= exit_day and d in daily.index]
            if len(path) < 2:
                skipped["no_data"] += 1
                continue
            trades.append(Trade(
                signal_id=sig.signal_id, video=sf.video.label or sf.video.title[:50], ticker=ticker, entity=sig.entity,
                quote=(sig.llm.quote if sig.llm else "")[:80], mention_et=sig.t_wall_et or "", entry_rule=rule,
                entry_day=entry_day, entry_price=entry_price, entry_kind=kind, exit_day=exit_day, exit_price=path[-1][1], path=path,
            ))
    return trades, skipped


def simulate(trades: list[Trade], store: PriceStore, start_cash: float = START_CASH) -> dict:
    """Calendar-time, daily equal-weight rebalanced equity curve plus naive equal-split profit."""
    if not trades:
        return {"trades": 0}
    cal = store.calendar()
    first = min(t.entry_day for t in trades)
    last = max(t.exit_day for t in trades)
    days = [d for d in cal.days if first <= d <= last]
    # daily return of each trade on each day it is open
    per_day: dict[date, list[float]] = {d: [] for d in days}
    for t in trades:
        prev = t.entry_price
        for d, close in t.path:
            per_day[d].append(close / prev - 1)
            prev = close
    equity = start_cash
    curve = []
    peak, max_dd = start_cash, 0.0
    invested_days = 0
    for d in days:
        rets = per_day[d]
        if rets:
            equity *= 1 + sum(rets) / len(rets)
            invested_days += 1
        peak = max(peak, equity)
        max_dd = max(max_dd, 1 - equity / peak)
        curve.append((d, equity))
    spy = store.daily("SPY")
    spy_first = float(spy.loc[first, "Open"]) if first in spy.index else float(spy["Close"][spy.index >= first].iloc[0])
    spy_last = float(spy.loc[last, "Close"])
    rets = [t.ret for t in trades]
    n = len(rets)
    mean = sum(rets) / n
    std = math.sqrt(sum((r - mean) ** 2 for r in rets) / (n - 1)) if n > 1 else 0.0
    return {
        "trades": n,
        "start": str(first), "end": str(last), "trading_days": len(days), "days_invested": invested_days,
        "final_equity": equity, "profit": equity - start_cash, "return": equity / start_cash - 1,
        "max_drawdown": max_dd,
        "spy_return_same_span": spy_last / spy_first - 1,
        "equal_split_profit": start_cash * mean, "mean_trade_return": mean, "median_trade_return": sorted(rets)[n // 2],
        "win_rate": sum(1 for r in rets if r > 0) / n, "t_stat": (mean / (std / math.sqrt(n))) if (n > 1 and std > 0) else None,
        "best": max(trades, key=lambda t: t.ret), "worst": min(trades, key=lambda t: t.ret),
        "curve": curve,
    }


def _money(x: float) -> str:
    return f"${x:,.0f}"


def _pct(x: float | None) -> str:
    return "n/a" if x is None else f"{x * 100:+.1f}%"


def build_portfolio_report(files: list[SignalFile], store: PriceStore) -> tuple[str, dict]:
    L = ["# $10,000 portfolio: buy what the President mentioned positively, sell one week later", "",
         f"_Generated {datetime.now(ET).strftime('%Y-%m-%d %H:%M %Z')} from {len(files)} videos._", "",
         "One position per (video, ticker): the primary ticker of each confirmed signal, first mention only. "
         "Sold at the close five trading sessions after entry. Equity is rebalanced equally across open positions "
         "every day (overlapping trades share the $10k). No costs, no slippage, dividends ignored. `equal split` is "
         "the naive alternative: $10k / N in every trade independently, profits summed.", ""]
    out: dict = {}
    L.append("| selection | entry | trades | final equity | profit | return | max DD | SPY same span | equal-split profit | mean trade | win rate | t |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    detail_blocks = []
    for select, slabel in (("stance_up", "stance = positive (what the app labels today)"),
                           ("judge_up", "judge expects up"),
                           ("judge_up_new", "judge expects up AND new information"),
                           ("company_invest", "positive & company & action investment/deal"),
                           ("company_invest_closed", "positive & company & investment/deal & market closed"),
                           ("present", "positive & executives present at the event")):
        for rule, rlabel in (("instant", "at the mention (or next open if closed)"), ("next_open", "next market open")):
            trades, skipped = build_trades(files, store, select=select, rule=rule)
            res = simulate(trades, store)
            out[f"{select}/{rule}"] = {k: v for k, v in res.items() if k not in ("best", "worst", "curve")} | {"skipped": skipped}
            if res["trades"] == 0:
                L.append(f"| {slabel} | {rlabel} | 0 | · | · | · | · | · | · | · | · | · |")
                continue
            L.append(f"| {slabel} | {rlabel} | {res['trades']} | {_money(res['final_equity'])} | {_money(res['profit'])} | "
                     f"{_pct(res['return'])} | {_pct(-res['max_drawdown'])} | {_pct(res['spy_return_same_span'])} | "
                     f"{_money(res['equal_split_profit'])} | {_pct(res['mean_trade_return'])} | {res['win_rate'] * 100:.0f}% | "
                     f"{res['t_stat']:.1f} |" if res["t_stat"] is not None else
                     f"| {slabel} | {rlabel} | {res['trades']} | {_money(res['final_equity'])} | {_money(res['profit'])} | "
                     f"{_pct(res['return'])} | {_pct(-res['max_drawdown'])} | {_pct(res['spy_return_same_span'])} | "
                     f"{_money(res['equal_split_profit'])} | {_pct(res['mean_trade_return'])} | {res['win_rate'] * 100:.0f}% | n/a |")
            if select == "stance_up":
                b, w = res["best"], res["worst"]
                detail_blocks.append((f"{slabel}, entry {rlabel}", res, trades, skipped))
    L.append("")
    L.append("Span = first entry to last exit; SPY is buy-and-hold over that span for comparison. The account sits in cash on days with no open position.")
    L.append("")
    for title, res, trades, skipped in detail_blocks:
        L.append(f"## {title}")
        L.append("")
        L.append(f"- {res['trades']} trades from {res['start']} to {res['end']} ({res['days_invested']} of {res['trading_days']} trading days invested); "
                 f"skipped: {skipped['no_data']} without price data, {skipped['not_yet']} not yet closed, {skipped['no_entry']} no entry price.")
        L.append(f"- Best trade: {res['best'].ticker} {_pct(res['best'].ret)} ({res['best'].video}); worst: {res['worst'].ticker} {_pct(res['worst'].ret)} ({res['worst'].video}).")
        L.append("")
        by_video = pd.DataFrame([{"video": t.video, "ret": t.ret} for t in trades]).groupby("video")["ret"].agg(["count", "mean"]).sort_values("count", ascending=False)
        L.append("| video | trades | mean trade return |")
        L.append("|---|---:|---:|")
        for v, r in by_video.iterrows():
            L.append(f"| {v} | {int(r['count'])} | {_pct(r['mean'])} |")
        L.append("")
        L.append("<details><summary>All trades</summary>")
        L.append("")
        L.append("| mention (ET) | ticker | entity | entry | entry px | exit | exit px | return | quote |")
        L.append("|---|---|---|---|---:|---|---:|---:|---|")
        for t in sorted(trades, key=lambda t: t.mention_et):
            L.append(f"| {t.mention_et[:16]} | {t.ticker} | {t.entity} | {t.entry_kind} {t.entry_day} | {t.entry_price:.2f} | {t.exit_day} | {t.exit_price:.2f} | {_pct(t.ret)} | {t.quote.replace('|', '/')} |")
        L.append("")
        L.append("</details>")
        L.append("")
    return "\n".join(L), out
