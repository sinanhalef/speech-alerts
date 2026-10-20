"""Dump transcript context (±75 s, speaker-tagged) for movers and for duds, for reading.

Movers: unique (video, ticker) with |z_first| >= 2 after hours, or |+1h| >= 1 daily-sigma in session.
Duds: cases where an analyst would have expected a move (judge new + conf >= 0.6 or magnitude medium,
or positive company investment/deal after hours) and the first reaction was < 0.5 sigma.
Writes out/contexts_movers.md and out/contexts_duds.md.
"""

from __future__ import annotations

import pandas as pd

from common import OUT, context, fmt_pct, fmt_z, load_signals


def block(b: pd.Series, s: pd.Series, others: pd.DataFrame) -> str:
    L = [f"### {str(b['t_wall_et'])[:16]} · {b['video_label']} · **{b['ticker']}** ({b['entity']}, {b['kind']}) · state={b['market_state']}",
         "",
         f"- outcome: first {fmt_pct(b['first'], 1)} ({fmt_z(b['z_first'])}, {b['first_kind']}), d1 {fmt_pct(b['d1'], 1)}, d2 {fmt_pct(b['d2'], 1)}; SPY first {fmt_pct(b['spy_first'], 1)}",
         f"- live label: stance={b['stance']} action={b['action']} conf={b['llm_conf']} count={b['count']} | judge: {b['judge_dir']} {b['judge_mag']} {b['novelty']} c={b['judge_conf']}",
         f"- quote: \"{b['quote']}\" — {b['summary']}",
         f"- judge rationale: {b['judge_rationale']}"]
    if len(others):
        L.append("- other mentions of this ticker in the video: " + "; ".join(
            f"{str(o['t_wall_et'])[11:16]} {o['entity']} [{o['stance']}/{o['action']}] \"{(o['quote'] or '')[:50]}\"" for _, o in others.iterrows()))
    L.append("")
    L.append("> " + context(b["video_id"], b["t_audio"], 75, 75).replace("\n", " "))
    L.append("")
    return "\n".join(L)


def main() -> None:
    df = pd.read_csv(OUT / "mentions_z.csv", low_memory=False)
    sig = load_signals().set_index("signal_id")

    # ---- movers
    mv = df[((df["market_state"] == "closed") & (df["z_first"].abs() >= 2)) | ((df["market_state"] == "open") & (df["z_first"].abs() >= 1))]
    out = ["# Transcript context of the movers", "", f"{mv.groupby(['video_id', 'ticker']).ngroups} unique (video, ticker) cases.", ""]
    for (vid, tk), g in sorted(mv.groupby(["video_id", "ticker"]), key=lambda kv: str(kv[1]["t_wall_et"].min())):
        g = g.sort_values(["judge_conf", "llm_conf"], ascending=False)
        b = g.iloc[0]
        others = g.iloc[1:]
        out.append(block(b, sig.loc[b["signal_id"]], others))
    (OUT / "contexts_movers.md").write_text("\n".join(out))
    print("movers:", mv.groupby(["video_id", "ticker"]).ngroups, "cases,", len("\n".join(out).split()), "words")

    # ---- duds
    exp = df[(df["z_first"].notna()) & (df["z_first"].abs() < 0.5) & (
        ((df["novelty"] == "new") & ((df["judge_conf"] >= 0.6) | (df["judge_mag"] == "medium")))
        | ((df["market_state"] == "closed") & (df["kind"] == "company") & (df["stance"] == "positive") & df["action"].isin(["investment", "deal"]) & (df["novelty"] == "new"))
    )]
    out = ["# Transcript context of the duds (expected a move, got < 0.5σ)", "", f"{exp.groupby(['video_id', 'ticker']).ngroups} unique (video, ticker) cases.", ""]
    for (vid, tk), g in sorted(exp.groupby(["video_id", "ticker"]), key=lambda kv: str(kv[1]["t_wall_et"].min())):
        g = g.sort_values(["judge_conf", "llm_conf"], ascending=False)
        b = g.iloc[0]
        out.append(block(b, sig.loc[b["signal_id"]], g.iloc[1:]))
    (OUT / "contexts_duds.md").write_text("\n".join(out))
    print("duds:", exp.groupby(["video_id", "ticker"]).ngroups, "cases,", len("\n".join(out).split()), "words")


if __name__ == "__main__":
    main()
