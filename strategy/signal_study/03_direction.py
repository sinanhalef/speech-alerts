"""Direction, relief rallies, sector-level and in-session fine-grained reactions.

Reads out/mentions_z.csv (from 02_movers.py). Writes out/direction.md.
"""

from __future__ import annotations

import math
import re
from datetime import date

import pandas as pd

from common import OUT, abn_vol, daily, fmt_pct, fmt_z, load_signals, md_table, spy_daily, wide

LIB = "VFRsYs1VYMg"  # Liberation Day: one macro shock, dominates any country/sector table


def pre_move(ticker: str, baseline_day: date) -> float | None:
    """Abnormal return of the ticker on the baseline session itself (prev close -> close), i.e. was the news already out?"""
    d = daily(ticker)
    s = spy_daily()
    if d.empty or baseline_day not in d.index:
        return None
    idx = list(d.index)
    i = idx.index(baseline_day)
    if i == 0:
        return None
    prev = idx[i - 1]
    if prev not in s.index or baseline_day not in s.index:
        return None
    r = d.loc[baseline_day, "Close"] / d.loc[prev, "Close"] - 1
    b = s.loc[baseline_day, "Close"] / s.loc[prev, "Close"] - 1
    return float(r - b)


def calib_rows(df: pd.DataFrame, by: str, zcol: str, sign_col: str) -> list[dict]:
    rows = []
    for val, g in df.groupby(by, dropna=False):
        gz = g[g[zcol].notna() & (g[sign_col] != 0)]
        adj = gz[zcol] * gz[sign_col]
        if len(gz) == 0:
            continue
        rows.append({by: str(val), "n": len(gz), "mean adj z": f"{adj.mean():+.2f}", "hit": f"{(adj > 0).mean() * 100:.0f}%",
                     "right ≥1σ": f"{(adj >= 1).mean() * 100:.0f}%", "wrong ≥1σ": f"{(adj <= -1).mean() * 100:.0f}%",
                     "right ≥2σ": f"{(adj >= 2).mean() * 100:.0f}%", "wrong ≥2σ": f"{(adj <= -2).mean() * 100:.0f}%"})
    return rows


def main() -> None:
    df = pd.read_csv(OUT / "mentions_z.csv", low_memory=False)
    df["session"] = pd.to_datetime(df["session"]).dt.date
    sig = load_signals().set_index("signal_id")
    L = ["# Direction, relief rallies, sectors and in-session reactions", ""]

    # ---------------------------------------------------------------- 1. unique movers, deduplicated
    closed = df[df["market_state"] == "closed"]
    L.append("## 1. Unique (video, ticker) first-reaction movers after hours (|z| ≥ 2), with the day-of pre-move")
    L.append("")
    L.append("`pre-move` = the ticker's abnormal return on the session *before* the mention (was the news already out?). "
             "`best mention` = the mention of that ticker in the video with the highest judge confidence.")
    L.append("")
    mv = closed[closed["z_first"].abs() >= 2].copy()
    rows = []
    for (vid, tk), g in mv.groupby(["video_id", "ticker"]):
        g = g.sort_values(["judge_conf", "llm_conf"], ascending=False)
        b = g.iloc[0]
        base_day = b["session"]
        # baseline day = previous session for closed mentions
        idx = list(spy_daily().index)
        i = idx.index(base_day) if base_day in idx else None
        prev = idx[i - 1] if i else None
        pm = pre_move(tk, prev) if prev else None
        rows.append({"when (ET)": str(b["t_wall_et"])[:16], "video": b["video_label"][:38], "ticker": tk, "n mentions": len(g),
                     "first": fmt_pct(b["first"], 1), "z": fmt_z(b["z_first"]), "d1": fmt_pct(b["d1"], 1), "pre-move": fmt_pct(pm, 1),
                     "best mention": f"{b['entity']} [{b['stance']}/{b['action']}] judge={b['judge_dir']}/{b['novelty']}/c={b['judge_conf']}",
                     "quote": (b["quote"] or "")[:70]})
    rows.sort(key=lambda r: r["when (ET)"])
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")

    # ---------------------------------------------------------------- 2. judge down calls, ex Liberation Day
    L.append("## 2. Judge/stance direction calibration excluding Liberation Day, by market state")
    L.append("")
    ex = df[df["video_id"] != LIB].copy()
    for state in ("closed", "open"):
        sub = ex[ex["market_state"] == state]
        L.append(f"### {state} — judge direction (z_first)")
        L.append("")
        L.append(md_table(calib_rows(sub, "judge_dir", "z_first", "judge_sign"), ["judge_dir", "n", "mean adj z", "hit", "right ≥1σ", "wrong ≥1σ", "right ≥2σ", "wrong ≥2σ"]))
        L.append("")
        L.append(f"### {state} — stance direction (z_first)")
        L.append("")
        L.append(md_table(calib_rows(sub, "stance_dir", "z_first", "stance_sign"), ["stance_dir", "n", "mean adj z", "hit", "right ≥1σ", "wrong ≥1σ", "right ≥2σ", "wrong ≥2σ"]))
        L.append("")
    L.append("### closed, ex Liberation Day — judge direction by action (z_first)")
    L.append("")
    sub = ex[ex["market_state"] == "closed"].copy()
    sub["dir_action"] = sub["judge_dir"] + "/" + sub["action"].astype(str)
    rows = calib_rows(sub[sub["judge_dir"] != "none"], "dir_action", "z_first", "judge_sign")
    rows = [r for r in rows if r["n"] >= 8]
    L.append(md_table(rows, ["dir_action", "n", "mean adj z", "hit", "right ≥1σ", "wrong ≥1σ", "right ≥2σ", "wrong ≥2σ"]))
    L.append("")
    L.append("### closed, ex Liberation Day — judge direction by kind (z_first)")
    L.append("")
    sub["dir_kind"] = sub["judge_dir"] + "/" + sub["kind"].astype(str)
    L.append(md_table(calib_rows(sub[sub["judge_dir"] != "none"], "dir_kind", "z_first", "judge_sign"), ["dir_kind", "n", "mean adj z", "hit", "right ≥1σ", "wrong ≥1σ", "right ≥2σ", "wrong ≥2σ"]))
    L.append("")
    L.append("### closed, ex Liberation Day — judge direction by novelty (z_first)")
    L.append("")
    sub["dir_nov"] = sub["judge_dir"] + "/" + sub["novelty"].astype(str)
    L.append(md_table(calib_rows(sub[sub["judge_dir"] != "none"], "dir_nov", "z_first", "judge_sign"), ["dir_nov", "n", "mean adj z", "hit", "right ≥1σ", "wrong ≥1σ", "right ≥2σ", "wrong ≥2σ"]))
    L.append("")

    # ---------------------------------------------------------------- 3. negative calls: where did the stock go?
    L.append("## 3. Negative statements (judge down or stance negative), after hours, ex Liberation Day: every case with |z| ≥ 1")
    L.append("")
    neg = ex[(ex["market_state"] == "closed") & ((ex["judge_dir"] == "down") | (ex["stance"] == "negative")) & (ex["z_first"].abs() >= 1)]
    rows = []
    for (vid, tk), g in neg.groupby(["video_id", "ticker"]):
        b = g.sort_values("judge_conf", ascending=False).iloc[0]
        rows.append({"when (ET)": str(b["t_wall_et"])[:16], "video": b["video_label"][:36], "entity": b["entity"], "ticker": tk,
                     "stance/action": f"{b['stance']}/{b['action']}", "judge": f"{b['judge_dir']}/{b['novelty']}", "first": fmt_pct(b["first"], 1),
                     "z": fmt_z(b["z_first"]), "d1": fmt_pct(b["d1"], 1), "quote": (b["quote"] or "")[:70]})
    rows.sort(key=lambda r: r["when (ET)"])
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")
    up = sum(1 for r in rows if r["z"].startswith("+"))
    L.append(f"- of {len(rows)} negative-statement cases with a ≥1σ first reaction, {up} went UP and {len(rows) - up} went down.")
    L.append("")

    # ---------------------------------------------------------------- 4. sector entities
    L.append("## 4. Sector entities: how often does the sector ETF/primary move ≥1σ at the first reaction? (after hours only, ex Liberation Day)")
    L.append("")
    sec = ex[(ex["kind"] == "sector") & (ex["market_state"] == "closed") & ex["z_first"].notna()]
    rows = []
    for ent, g in sec.groupby("entity"):
        if len(g) < 6:
            continue
        adj = g["z_first"] * g["exp_sign"]
        d = adj[g["exp_sign"] != 0]
        rows.append({"entity": ent, "pairs": len(g), "videos": g["video_id"].nunique(), "mean |z|": f"{g['z_first'].abs().mean():.2f}",
                     "share |z|≥1": f"{(g['z_first'].abs() >= 1).mean() * 100:.0f}%", "share |z|≥2": f"{(g['z_first'].abs() >= 2).mean() * 100:.0f}%",
                     "mean adj z (directional)": f"{d.mean():+.2f}" if len(d) else "n/a", "hit": f"{(d > 0).mean() * 100:.0f}%" if len(d) else "n/a"})
    rows.sort(key=lambda r: -float(r["mean |z|"]))
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")

    # ---------------------------------------------------------------- 5. in-session fine-grained
    L.append("## 5. In-session mentions: +10 min and +30 min reactions scaled to the horizon (recent videos with 1-minute bars)")
    L.append("")
    w = wide()
    op = w[(w["market_state"] == "open") & w["+10m"].notna()].copy()
    op["session"] = pd.to_datetime(op["session"]).dt.date
    rows = []
    for _, r in op.iterrows():
        av = abn_vol(r["ticker"], r["session"])
        if not av:
            continue
        z10 = r["+10m"] / (av * math.sqrt(10 / 390))
        z30 = r["+30m"] / (av * math.sqrt(30 / 390)) if pd.notna(r["+30m"]) else None
        z60 = r["+1h"] / (av * math.sqrt(60 / 390)) if pd.notna(r["+1h"]) else None
        rows.append({"signal_id": r["signal_id"], "ticker": r["ticker"], "video": r["video_label"][:36], "entity": r["entity"], "kind": r["kind"],
                     "stance": r["stance"], "action": r["action"], "novelty": r["novelty"], "judge_dir": r["judge_dir"],
                     "+10m": r["+10m"], "z10": z10, "+30m": r["+30m"], "z30": z30, "+1h": r["+1h"], "z60": z60, "t": str(r["t_wall_et"])[:16]})
    fine = pd.DataFrame(rows)
    L.append(f"- pairs with a +10 min measurement: {len(fine)} ({fine['signal_id'].nunique()} signals)")
    for col in ("z10", "z30", "z60"):
        s = fine[col].dropna()
        L.append(f"- {col}: mean |z| {s.abs().mean():.2f}; share |z| ≥ 2: {(s.abs() >= 2).mean() * 100:.1f}% (normal baseline 4.6%); "
                 f"share |z| ≥ 3: {(s.abs() >= 3).mean() * 100:.1f}% (baseline 0.3%)")
    L.append("")
    L.append("Top |z10| cases:")
    L.append("")
    top = fine.sort_values("z10", key=lambda s: s.abs(), ascending=False).head(15)
    trows = [{"t": r["t"], "video": r["video"], "entity": r["entity"], "ticker": r["ticker"], "stance/action": f"{r['stance']}/{r['action']}",
              "judge": f"{r['judge_dir']}/{r['novelty']}", "+10m": fmt_pct(r["+10m"], 2), "z10": f"{r['z10']:+.1f}", "+30m": fmt_pct(r["+30m"], 2),
              "+1h": fmt_pct(r["+1h"], 2)} for _, r in top.iterrows()]
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")
    # does the sign of the 10-min move follow the stance/judge?
    d = fine[fine["judge_dir"].isin(["up", "down"])].copy()
    d["adj10"] = d["z10"] * d["judge_dir"].map({"up": 1, "down": -1})
    L.append(f"- judge-directional pairs: {len(d)}; mean adj z10 {d['adj10'].mean():+.2f}; hit {(d['adj10'] > 0).mean() * 100:.0f}%")
    d2 = fine[fine["stance"].isin(["positive", "negative"])].copy()
    d2["adj10"] = d2["z10"] * d2["stance"].map({"positive": 1, "negative": -1})
    L.append(f"- stance-directional pairs: {len(d2)}; mean adj z10 {d2['adj10'].mean():+.2f}; hit {(d2['adj10'] > 0).mean() * 100:.0f}%")
    L.append("")

    # ---------------------------------------------------------------- 6. positive company mentions after hours: what separates movers?
    L.append("## 6. Positive company mentions after hours (ex Liberation Day): features vs first reaction")
    L.append("")
    pc = ex[(ex["market_state"] == "closed") & (ex["kind"] == "company") & (ex["stance"] == "positive") & ex["z_first"].notna()].copy()
    ctx = pc["signal_id"].map(lambda s: sig.loc[s, "context"] if s in sig.index else "")
    txt = (pc["quote"].fillna("") + " " + pc["summary"].fillna(""))
    MONEY = re.compile(r"\$\s?\d|\b\d[\d,\.]*\s*(billion|million|trillion)\b", re.I)
    PRESENT = re.compile(r"\b(is here|are here|here today|with us today|joined by|thank you .{0,25}(ceo|chairman|founder)|stand up|where are you|where is)\b", re.I)
    ANN = re.compile(r"\b(announc\w*|just signed|signed|agreement|agreed|approved|stake|golden share|contract|partnership|will invest|is investing|are investing|committed|commitment)\b", re.I)
    PAST = re.compile(r"\b(biden|obama|four years ago|last year|during my first term|when i (was|came)|they had|ago)\b", re.I)
    pc["money"] = txt.str.contains(MONEY)
    pc["present"] = ctx.str.contains(PRESENT)
    pc["announce"] = txt.str.contains(ANN) | ctx.str.contains(ANN)
    pc["past"] = txt.str.contains(PAST)
    pc["new"] = pc["novelty"] == "new"
    pc["invest_deal"] = pc["action"].isin(["investment", "deal"])
    pc["repeat_count>1"] = pc["count"] > 1
    rows = []
    for feat in ["money", "present", "announce", "past", "new", "invest_deal", "repeat_count>1"]:
        for val in (True, False):
            g = pc[pc[feat] == val]
            if len(g) == 0:
                continue
            rows.append({"feature": f"{feat} = {val}", "n": len(g), "videos": g["video_id"].nunique(), "mean z": f"{g['z_first'].mean():+.2f}",
                         "share z≥1": f"{(g['z_first'] >= 1).mean() * 100:.0f}%", "share z≤-1": f"{(g['z_first'] <= -1).mean() * 100:.0f}%",
                         "share z≥2": f"{(g['z_first'] >= 2).mean() * 100:.0f}%", "mean d1": fmt_pct(g["d1"].mean(), 2)})
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")
    L.append("Cross: new × announce × money")
    L.append("")
    rows = []
    for (a, b, c), g in pc.groupby(["new", "announce", "money"]):
        rows.append({"new": a, "announce": b, "money": c, "n": len(g), "videos": g["video_id"].nunique(), "mean z": f"{g['z_first'].mean():+.2f}",
                     "share z≥1": f"{(g['z_first'] >= 1).mean() * 100:.0f}%", "share z≥2": f"{(g['z_first'] >= 2).mean() * 100:.0f}%",
                     "tickers": ", ".join(sorted(set(g[g['z_first'] >= 1]['ticker'])))[:60]})
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")

    (OUT / "direction.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
