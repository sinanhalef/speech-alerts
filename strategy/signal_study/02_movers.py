"""Mention-level view: every (signal, ticker) pair z-scored on the ticker's own abnormal volatility.

Produces:
  out/mentions_z.csv   one row per confirmed (signal, ticker) with z_first, z_d1, z_d2 and all labels/quotes
  out/movers.md        the movers (|z| >= 2), the "expected big, got nothing" list, and judge/stance calibration tables
"""

from __future__ import annotations

from datetime import date

import pandas as pd

from common import OUT, abn_vol, fmt_pct, fmt_z, load_signals, md_table, other_speaker_seconds, wide


def build() -> pd.DataFrame:
    w = wide()
    sig = load_signals().set_index("signal_id")
    rows = []
    for _, r in w.iterrows():
        sess = date.fromisoformat(str(r["session"])) if pd.notna(r["session"]) else None
        if sess is None:
            continue
        av = abn_vol(r["ticker"], sess)
        first = r["open"] if r["market_state"] == "closed" else r["+1h"]
        first_kind = "open_gap" if r["market_state"] == "closed" else "+1h"
        if pd.isna(first) and r["market_state"] == "open":
            first = r["+2h"] if pd.notna(r["+2h"]) else r["close_d0"]
            first_kind = "+2h" if pd.notna(r["+2h"]) else "close_d0"
        s = sig.loc[r["signal_id"]]
        # per-ticker judge verdict
        je = next((j for j in s["judge_all"] if j["ticker"].upper() == r["ticker"]), None)
        rows.append({
            "signal_id": r["signal_id"], "video_id": r["video_id"], "video_label": r["video_label"], "group": r["group"],
            "entity": r["entity"], "kind": r["kind"], "ticker": r["ticker"], "primary": bool(r["primary"]),
            "ticker_source": r["ticker_source"], "first_mention": bool(r["first_mention"]), "t_audio": r["t_audio"],
            "t_wall_et": r["t_wall_et"], "market_state": r["market_state"], "session": sess,
            "stance": r["stance"], "action": r["action"], "llm_conf": r["llm_confidence"], "stance_dir": r["stance_dir"],
            "judge_dir": je["direction"] if je else "none", "judge_conf": je["confidence"] if je else None,
            "judge_mag": je["magnitude"] if je else None, "novelty": je["novelty"] if je else None,
            "judge_rationale": je["rationale"] if je else "",
            "count": s["count"], "n_tickers": s["n_tickers"], "quote": s["quote"], "summary": s["summary"],
            "speaker_is_main": s["speaker_is_main"],
            "vol": av, "first": first, "first_kind": first_kind,
            "d1": r["close_d1"], "d2": r["close_d2"], "d5": r["close_d5"], "raw_first": (r["raw_open"] if r["market_state"] == "closed" else r["raw_+1h"]),
            "spy_first": (r["spy_open"] if r["market_state"] == "closed" else r["spy_+1h"]),
            "z_first": first / av if (av and pd.notna(first)) else None,
            "z_d1": r["close_d1"] / av if (av and pd.notna(r["close_d1"])) else None,
            "z_d2": r["close_d2"] / av if (av and pd.notna(r["close_d2"])) else None,
            "guest_sec": other_speaker_seconds(r["video_id"], r["t_audio"]),
        })
    df = pd.DataFrame(rows)
    df["exp_sign"] = df["judge_dir"].map({"up": 1, "down": -1}).fillna(df["stance_dir"].map({"up": 1, "down": -1})).fillna(0)
    df["stance_sign"] = df["stance_dir"].map({"up": 1, "down": -1}).fillna(0)
    df["judge_sign"] = df["judge_dir"].map({"up": 1, "down": -1}).fillna(0)
    return df


def calib(df: pd.DataFrame, col: str, zcol: str = "z_first", sign_col: str = "judge_sign") -> list[dict]:
    rows = []
    for val, g in df.groupby(col, dropna=False):
        gz = g[g[zcol].notna()]
        adj = gz[zcol] * gz[sign_col]
        directional = gz[gz[sign_col] != 0]
        adj_d = directional[zcol] * directional[sign_col]
        rows.append({col: str(val), "n": len(gz), "mean |z|": f"{gz[zcol].abs().mean():.2f}" if len(gz) else "n/a",
                     "share |z|≥1": f"{(gz[zcol].abs() >= 1).mean() * 100:.0f}%" if len(gz) else "n/a",
                     "share |z|≥2": f"{(gz[zcol].abs() >= 2).mean() * 100:.0f}%" if len(gz) else "n/a",
                     "n directional": len(adj_d),
                     "mean adj z": f"{adj_d.mean():+.2f}" if len(adj_d) else "n/a",
                     "hit": f"{(adj_d > 0).mean() * 100:.0f}%" if len(adj_d) else "n/a",
                     "share adj z≥1": f"{(adj_d >= 1).mean() * 100:.0f}%" if len(adj_d) else "n/a",
                     "share adj z≤-1": f"{(adj_d <= -1).mean() * 100:.0f}%" if len(adj_d) else "n/a"})
    return rows


def main() -> None:
    df = build()
    df.to_csv(OUT / "mentions_z.csv", index=False)
    L = ["# Mention-level movers (all confirmed signal × ticker pairs, z-scored)", ""]
    L.append(f"{len(df)} (signal, ticker) pairs; {df['z_first'].notna().sum()} with a first reaction; "
             f"{df['z_d1'].notna().sum()} with a next-day return. First reaction = opening gap when the market was closed, "
             f"else +1 h (fallback +2 h / close). z = abnormal return / the ticker's 60-session abnormal daily vol.")
    L.append("")

    # ---- movers
    mv = df[df["z_first"].abs() >= 2].sort_values("z_first", key=lambda s: s.abs(), ascending=False)
    L.append(f"## 1. First-reaction movers (|z_first| ≥ 2): {len(mv)} pairs, {mv['signal_id'].nunique()} signals, {mv['video_id'].nunique()} videos")
    L.append("")
    trows = []
    for _, r in mv.iterrows():
        trows.append({"when (ET)": str(r["t_wall_et"])[:16], "video": r["video_label"][:40], "entity": r["entity"], "ticker": r["ticker"],
                      "state": r["market_state"], "stance/action": f"{r['stance']}/{r['action']}", "judge": f"{r['judge_dir']} {r['judge_mag']} {r['novelty']}",
                      "first": fmt_pct(r["first"], 1), "z": fmt_z(r["z_first"]), "d1": fmt_pct(r["d1"], 1), "guest s": f"{r['guest_sec']:.0f}",
                      "quote": (r["quote"] or "")[:80]})
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")

    # ---- next-day movers not in the first-reaction list
    mv2 = df[(df["z_d1"].abs() >= 2.5) & ~(df["z_first"].abs() >= 2)].sort_values("z_d1", key=lambda s: s.abs(), ascending=False)
    L.append(f"## 2. Next-day movers (|z_d1| ≥ 2.5) that did not move at the first reaction: {len(mv2)} pairs")
    L.append("")
    trows = []
    for _, r in mv2.head(40).iterrows():
        trows.append({"when (ET)": str(r["t_wall_et"])[:16], "video": r["video_label"][:40], "entity": r["entity"], "ticker": r["ticker"],
                      "state": r["market_state"], "stance/action": f"{r['stance']}/{r['action']}", "judge": f"{r['judge_dir']} {r['judge_mag']} {r['novelty']}",
                      "first": fmt_pct(r["first"], 1), "d1": fmt_pct(r["d1"], 1), "z d1": fmt_z(r["z_d1"]), "quote": (r["quote"] or "")[:80]})
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")

    # ---- expected big, got nothing
    exp = df[(df["judge_mag"].isin(["medium", "large"])) & (df["judge_dir"] != "none") & df["z_first"].notna()]
    L.append(f"## 3. Judge expected a medium/large move: {len(exp)} pairs")
    L.append("")
    L.append(f"- mean adj z_first {(exp['z_first'] * exp['judge_sign']).mean():+.2f}; share adj z ≥ 1: {((exp['z_first'] * exp['judge_sign']) >= 1).mean() * 100:.0f}%; "
             f"share |z| ≥ 2: {(exp['z_first'].abs() >= 2).mean() * 100:.0f}%")
    L.append("")
    trows = []
    for _, r in exp.sort_values("z_first", key=lambda s: s.abs(), ascending=False).iterrows():
        trows.append({"when (ET)": str(r["t_wall_et"])[:16], "video": r["video_label"][:40], "entity": r["entity"], "ticker": r["ticker"],
                      "state": r["market_state"], "judge": f"{r['judge_dir']} {r['judge_mag']} {r['novelty']} c={r['judge_conf']}",
                      "first": fmt_pct(r["first"], 1), "z": fmt_z(r["z_first"]), "d1": fmt_pct(r["d1"], 1), "rationale": (r["judge_rationale"] or "")[:90]})
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")

    # ---- calibration tables
    L.append("## 4. Calibration of the labels against the first reaction (all pairs)")
    L.append("")
    for col in ["kind", "market_state", "stance", "action", "novelty", "judge_mag", "judge_dir", "ticker_source"]:
        L.append(f"### by {col}")
        L.append("")
        rows = calib(df, col)
        L.append(md_table(rows, list(rows[0].keys())))
        L.append("")
    # judge confidence buckets
    df["judge_conf_bucket"] = pd.cut(df["judge_conf"].fillna(0), [-0.01, 0.3, 0.5, 0.6, 0.7, 1.0], labels=["≤0.3", "0.3-0.5", "0.5-0.6", "0.6-0.7", ">0.7"])
    L.append("### by judge confidence")
    L.append("")
    rows = calib(df, "judge_conf_bucket")
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")
    df["guest_bucket"] = pd.cut(df["guest_sec"], [-1, 0, 20, 60, 10_000], labels=["0", "1-20 s", "20-60 s", ">60 s"])
    L.append("### by seconds of non-main speakers within ±2 min (guests/executives at the podium)")
    L.append("")
    rows = calib(df, "guest_bucket")
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")
    # stance-only calibration
    L.append("### stance-only direction, by market state")
    L.append("")
    rows = calib(df, "market_state", sign_col="stance_sign")
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")
    L.append("### next day (z_d1) by kind, judge direction")
    L.append("")
    rows = calib(df, "kind", zcol="z_d1")
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")

    (OUT / "movers.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
