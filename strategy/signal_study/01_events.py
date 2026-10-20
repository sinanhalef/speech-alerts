"""Event-level view: for each video, how did the market (SPY/QQQ/TLT) and the sector ETFs move?

Answers: which of the 78 videos were market events at all, regardless of individual mentions.
For a video that starts in the session: SPY from the last completed bar before the start to +1 h,
to the close, and to the next close. For after-hours videos: previous close -> next open -> next close.
Also: how many of the tickers named in the video moved beyond 2σ of their own abnormal volatility.
"""

from __future__ import annotations

from datetime import timedelta

import pandas as pd

from backtest.marketclock import anchor_for, session_close
from common import (OUT, abn_vol, calendar, daily_close, daily_open, fmt_pct, load_videos, md_table, price_at, price_before,
                    raw_vol, ret, video_start_et, wide)

MARKET = ["SPY", "QQQ", "DIA", "TLT"]
SECTORS = ["XLE", "XLF", "XLV", "XHB", "XRT", "ITA", "SMH", "SLX", "KRE", "IYT", "XPH", "TAN", "URA", "COPX", "REMX", "DBA",
           "USO", "UNG", "IBIT", "FXI", "EWJ", "EWC", "EWW", "VGK", "EWY", "INDA", "EWZ"]


def event_reaction(ticker: str, start, end):
    """Returns dict of reactions for a video that spans [start, end] (ET datetimes)."""
    cal = calendar()
    a = anchor_for(start, cal)
    if a is None:
        return {}
    out = {"state": a.state, "session": a.session}
    if a.state == "open":
        p0, _ = price_before(ticker, start)
        if p0 is None:
            p0 = daily_close(ticker, cal.prev_session(a.session)) if cal.prev_session(a.session) else None
            out["p0_kind"] = "prev_close"
        else:
            out["p0_kind"] = "bar"
        p1h, _ = price_at(ticker, start + timedelta(hours=1))
        pend, _ = price_at(ticker, min(end, session_close(a.session)))
        out["+1h"] = ret(p0, p1h)
        out["end"] = ret(p0, pend)
        out["d0"] = ret(p0, daily_close(ticker, a.session))
        d1 = cal.offset(a.session, 1)
        out["d1"] = ret(p0, daily_close(ticker, d1)) if d1 else None
        out["d1_only"] = ret(daily_close(ticker, a.session), daily_close(ticker, d1)) if d1 else None
        out["prev_close_to_d0"] = ret(daily_close(ticker, cal.prev_session(a.session)), daily_close(ticker, a.session))
    else:
        p0 = daily_close(ticker, a.baseline_day)
        out["p0_kind"] = "prev_close"
        out["open"] = ret(p0, daily_open(ticker, a.session))
        out["d0"] = ret(p0, daily_close(ticker, a.session))
        d1 = cal.offset(a.session, 1)
        out["d1"] = ret(p0, daily_close(ticker, d1)) if d1 else None
        out["d1_only"] = ret(daily_close(ticker, a.session), daily_close(ticker, d1)) if d1 else None
    return out


def main() -> None:
    vids = load_videos()
    w = wide()
    rows = []
    for vid, v in vids.items():
        start = video_start_et(v)
        if start is None:
            continue
        end = start + timedelta(seconds=v.get("duration") or 0)
        spy = event_reaction("SPY", start, end)
        if not spy:
            continue
        sess = spy["session"]
        spy_vol = raw_vol("SPY", sess)
        r = {"video_id": vid, "label": (v.get("label") or v.get("title"))[:60], "group": v.get("group"),
             "start_et": start.strftime("%Y-%m-%d %a %H:%M"), "state": spy["state"], "session": str(sess),
             "spy_vol": spy_vol}
        for k in ("open", "+1h", "end", "d0", "d1", "d1_only"):
            r[f"spy_{k}"] = spy.get(k)
        r["spy_z_first"] = (spy.get("open") if spy["state"] == "closed" else spy.get("+1h"))
        r["spy_z_first"] = r["spy_z_first"] / spy_vol if (r["spy_z_first"] is not None and spy_vol) else None
        r["spy_z_d0"] = spy["d0"] / spy_vol if (spy.get("d0") is not None and spy_vol) else None
        for tk in ("QQQ", "TLT"):
            e = event_reaction(tk, start, end)
            r[f"{tk}_first"] = e.get("open") if e.get("state") == "closed" else e.get("+1h")
            r[f"{tk}_d0"] = e.get("d0")
        # sector ETFs: raw and abnormal first reaction, z-scored on abnormal vol
        sec = []
        for tk in SECTORS:
            e = event_reaction(tk, start, end)
            if not e:
                continue
            first = e.get("open") if e.get("state") == "closed" else e.get("+1h")
            spy_first = spy.get("open") if spy["state"] == "closed" else spy.get("+1h")
            d0 = e.get("d0")
            if first is None or spy_first is None:
                continue
            av = abn_vol(tk, sess)
            abn_first = first - spy_first
            abn_d0 = (d0 - spy["d0"]) if (d0 is not None and spy.get("d0") is not None) else None
            sec.append({"tk": tk, "first": first, "abn_first": abn_first, "z_first": abn_first / av if av else None,
                        "abn_d0": abn_d0, "z_d0": abn_d0 / av if (av and abn_d0 is not None) else None})
        sec_sorted = sorted([s for s in sec if s["z_first"] is not None], key=lambda s: -abs(s["z_first"]))
        r["n_sector_2sig_first"] = sum(1 for s in sec if s["z_first"] is not None and abs(s["z_first"]) >= 2)
        r["n_sector_2sig_d0"] = sum(1 for s in sec if s["z_d0"] is not None and abs(s["z_d0"]) >= 2)
        r["top_sectors"] = ", ".join(f"{s['tk']} {fmt_pct(s['abn_first'],1)} ({s['z_first']:+.1f}σ)" for s in sec_sorted[:4])
        # named tickers in this video that moved beyond 2σ (from measurements)
        sub = w[w["video_id"] == vid]
        named = sub["ticker"].nunique()
        big = []
        for tk, g in sub.groupby("ticker"):
            g0 = g.iloc[0]
            first = g0["open"] if g0["market_state"] == "closed" else g0["+1h"]
            d1 = g0["close_d1"]
            av = abn_vol(tk, sess)
            if not av:
                continue
            zf = first / av if pd.notna(first) else None
            zd = d1 / av if pd.notna(d1) else None
            if (zf is not None and abs(zf) >= 2) or (zd is not None and abs(zd) >= 2):
                big.append(f"{tk} {fmt_pct(first,1) if zf is not None else '-'}/{fmt_pct(d1,1) if zd is not None else '-'}")
        r["n_named"] = named
        r["n_signals"] = sub["signal_id"].nunique()
        r["n_named_2sig"] = len(big)
        r["named_2sig"] = ", ".join(big[:8])
        rows.append(r)

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "events.csv", index=False)

    L = ["# Event-level reactions per video", "",
         "First reaction = opening gap (video after hours) or +1 h from the video start (in session). z = first reaction / "
         "SPY's own 60-session daily vol (market) or / the ETF's abnormal vol (sectors). `named 2σ` = tickers mentioned in the "
         "video whose first reaction or next-day abnormal return exceeded 2σ of their own abnormal vol.", ""]

    L.append("## 1. Videos ranked by the market's own first reaction (|SPY z|)")
    L.append("")
    d = df.sort_values("spy_z_first", key=lambda s: s.abs(), ascending=False)
    trows = []
    for _, r in d.iterrows():
        trows.append({"start (ET)": r["start_et"], "video": r["label"], "state": r["state"],
                      "SPY first": fmt_pct(r["spy_z_first"] * r["spy_vol"] if pd.notna(r["spy_z_first"]) else None, 1),
                      "SPY z": f"{r['spy_z_first']:+.1f}" if pd.notna(r["spy_z_first"]) else "n/a",
                      "SPY d0": fmt_pct(r["spy_d0"], 1), "SPY d1": fmt_pct(r["spy_d1"], 1),
                      "QQQ first": fmt_pct(r["QQQ_first"], 1), "TLT first": fmt_pct(r["TLT_first"], 1),
                      "sectors ≥2σ": int(r["n_sector_2sig_first"]), "top sector ETFs (abn first)": r["top_sectors"],
                      "named": int(r["n_named"]), "named ≥2σ": int(r["n_named_2sig"])})
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")

    L.append("## 2. Videos ranked by named tickers that moved ≥2σ (first reaction or next day)")
    L.append("")
    d = df.sort_values(["n_named_2sig", "n_sector_2sig_first"], ascending=False)
    trows = []
    for _, r in d.head(30).iterrows():
        trows.append({"start (ET)": r["start_et"], "video": r["label"], "state": r["state"], "signals": int(r["n_signals"]),
                      "named": int(r["n_named"]), "named ≥2σ": int(r["n_named_2sig"]), "which (first / d1)": r["named_2sig"],
                      "SPY first": fmt_pct(r["spy_z_first"] * r["spy_vol"] if pd.notna(r["spy_z_first"]) else None, 1)})
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")

    L.append("## 3. Base rates")
    L.append("")
    n = len(df)
    L.append(f"- videos with a usable market anchor: {n}")
    z = df["spy_z_first"].dropna()
    L.append(f"- SPY first reaction beyond 1σ: {(z.abs() >= 1).sum()} of {len(z)}; beyond 2σ: {(z.abs() >= 2).sum()}")
    zd = df["spy_z_d0"].dropna()
    L.append(f"- SPY move to the close of the event session beyond 2σ: {(zd.abs() >= 2).sum()} of {len(zd)}")
    L.append(f"- videos with at least one sector ETF beyond 2σ at the first reaction: {(df['n_sector_2sig_first'] >= 1).sum()}")
    L.append(f"- videos with at least one named ticker beyond 2σ: {(df['n_named_2sig'] >= 1).sum()}; with 3+: {(df['n_named_2sig'] >= 3).sum()}")
    L.append(f"- mean named tickers per video: {df['n_named'].mean():.1f}; mean named ≥2σ per video: {df['n_named_2sig'].mean():.2f} "
             f"({df['n_named_2sig'].sum() / max(df['n_named'].sum(), 1) * 100:.1f}% of named tickers)")
    L.append("")
    (OUT / "events.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
