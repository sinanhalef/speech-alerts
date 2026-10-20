"""Rule backtest: does a deterministic version of the proposed classifier separate movers from non-movers?

The rules use only what is knowable at the moment of the remark: market state, the judge's novelty and
direction (stand-ins for the classifier's own reading of "new decision/number" and "who benefits"),
entity kind, action label, text cues (announcement verbs, numbers, past-tense framing, hedges) and
whether the entity was the subject of the event (repeated mentions within the cooldown).

Label per (signal, ticker): right = adj z_first >= +1 (moved >= 1 sigma the expected way),
wrong = adj z_first <= -1, flat otherwise. Event level = unique (video, ticker), best-judged mention.
Writes out/rules.md.
"""

from __future__ import annotations

import re

import pandas as pd

from common import OUT, load_signals, load_videos, md_table

ANN = re.compile(r"\b(announc\w*|just signed|i signed|signed|agreement|agreed|approved|approve|stake|golden share|contract|"
                 r"partnership|will invest|is investing|are investing|committed|commitment|effective|imposing|impose|"
                 r"bring it (up )?from|doubling|we are going to be|formation of|purchase of|i made an? investment)\b", re.I)
NUM = re.compile(r"\$\s?\d|\b\d[\d,\.]*\s*(billion|million|trillion|percent|%)|\b\d{1,3}\s*%|\b\d{1,3}\s*to\s*\d{1,3}\s*%", re.I)
PAST = re.compile(r"\b(biden|obama|years ago|last year|my first term|when i (was|came)|they had|used to|decimated|was a bust)\b", re.I)
HEDGE = re.compile(r"\b(we're looking at|looking at that|we'll see|maybe|perhaps|i'd like to|i would like|could be|might|"
                   r"thinking about|we may|possibly|considering)\b", re.I)
LIST = re.compile(r"(\b[A-Z][A-Za-z&\.]+,\s+){2,}", re.M)  # three or more capitalised names separated by commas


def main() -> None:
    df = pd.read_csv(OUT / "mentions_z.csv", low_memory=False)
    sig = load_signals().set_index("signal_id")
    vids = load_videos()
    df = df[df["z_first"].notna()].copy()
    df["ctx"] = df["signal_id"].map(lambda s: sig.loc[s, "context"] if s in sig.index else "")
    df["txt"] = df["quote"].fillna("") + " " + df["summary"].fillna("")
    df["title"] = df["video_id"].map(lambda v: (vids[v].get("title") or "").lower())
    df["announce"] = df["txt"].str.contains(ANN) | df["ctx"].str.contains(ANN)
    df["number"] = df["txt"].str.contains(NUM)
    df["past"] = df["txt"].str.contains(PAST)
    df["hedge"] = df["txt"].str.contains(HEDGE) | df["ctx"].str[-200:].str.contains(HEDGE)
    df["subject"] = (df["count"] > 1) | df.apply(lambda r: any(w in r["title"] for w in re.split(r"[^a-z0-9]+", str(r["entity"]).lower()) if len(w) > 3), axis=1)
    df["adj"] = df["z_first"] * df["exp_sign"]
    df["right"] = df["adj"] >= 1
    df["wrong"] = df["adj"] <= -1
    df["big"] = df["z_first"].abs() >= 2
    closed = df["market_state"] == "closed"
    new = df["novelty"] == "new"
    directional = df["exp_sign"] != 0
    hard = df["action"].isin(["tariff", "regulation", "sanction", "investment", "deal", "subsidy"])
    direct = (df["kind"] == "company") | ((df["kind"] == "sector") & df["action"].isin(["tariff", "regulation", "sanction"]))
    not_macro = ~df["kind"].isin(["country", "asset"])

    tiers = {
        "A  actionable: closed & new & directional & direct instrument & hard action & (announce|number) & !past & !hedge":
            closed & new & directional & direct & hard & (df["announce"] | df["number"]) & ~df["past"] & ~df["hedge"],
        "A' same but judge up only (no down calls)":
            closed & new & (df["judge_dir"] == "up") & direct & hard & (df["announce"] | df["number"]) & ~df["past"] & ~df["hedge"],
        "B  watch: closed & directional & not macro & (new | subject of event) & !past & !hedge":
            closed & directional & not_macro & (new | df["subject"]) & ~df["past"] & ~df["hedge"],
        "C  closed & directional, everything else": closed & directional,
        "D  in session, directional (any)": ~closed & directional,
        "E  non-directional (judge none), closed": closed & ~directional,
        "baseline: judge up, closed": closed & (df["judge_dir"] == "up"),
        "baseline: judge down, closed": closed & (df["judge_dir"] == "down"),
        "baseline: stance positive, closed": closed & (df["stance"] == "positive"),
        "baseline: all closed": closed,
        "baseline: all": pd.Series(True, index=df.index),
    }

    def summarize(mask: pd.Series, name: str) -> dict:
        g = df[mask]
        d = g[g["exp_sign"] != 0]
        ev = g.sort_values("judge_conf", ascending=False).drop_duplicates(["video_id", "ticker"])
        evd = ev[ev["exp_sign"] != 0]
        return {"tier": name, "pairs": len(g), "events": len(ev), "videos": g["video_id"].nunique(),
                "right ≥1σ (pairs)": f"{d['right'].mean() * 100:.0f}%" if len(d) else "n/a",
                "wrong ≥1σ (pairs)": f"{d['wrong'].mean() * 100:.0f}%" if len(d) else "n/a",
                "|z|≥2 (pairs)": f"{g['big'].mean() * 100:.0f}%",
                "mean adj z": f"{d['adj'].mean():+.2f}" if len(d) else "n/a",
                "right ≥1σ (events)": f"{evd['right'].mean() * 100:.0f}%" if len(evd) else "n/a",
                "wrong ≥1σ (events)": f"{evd['wrong'].mean() * 100:.0f}%" if len(evd) else "n/a",
                "right events": ", ".join(sorted(set(evd[evd['right']]['ticker'])))[:80]}

    L = ["# Rule backtest: do the proposed decision rules separate movers from non-movers?", "",
         "Unit: confirmed (signal, ticker) pairs with a measurable first reaction. `right` = moved ≥ 1σ in the expected direction "
         "(judge direction, stance as fallback); `wrong` = moved ≥ 1σ the other way. Events = unique (video, ticker).", ""]
    rows = [summarize(m, n) for n, m in tiers.items()]
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")

    # robustness: tier A and B by video group, and excluding the three big announcement events
    L.append("## By video group (tier A and B)")
    L.append("")
    rows = []
    for name in list(tiers)[:3]:
        for grp in ["headline", "expansion", "recent", "other"]:
            m = tiers[name] & (df["group"] == grp)
            if m.sum() == 0:
                continue
            r = summarize(m, f"{name[:2]} / {grp}")
            rows.append(r)
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")
    big3 = {"zDo_RrzdRoQ", "DKddhD4z7UU", "J6SK7lotKZQ"}
    L.append("## Excluding Stargate, the steel rally and the Apple event")
    L.append("")
    rows = [summarize(tiers[n] & ~df["video_id"].isin(big3), n) for n in list(tiers)[:4]]
    L.append(md_table(rows, list(rows[0].keys())))
    L.append("")

    # what tier A flagged, case by case (events)
    L.append("## Tier A cases (event level)")
    L.append("")
    a = df[tiers[list(tiers)[0]]].sort_values("judge_conf", ascending=False).drop_duplicates(["video_id", "ticker"]).sort_values("t_wall_et")
    trows = [{"when": str(r["t_wall_et"])[:16], "video": r["video_label"][:34], "ticker": r["ticker"], "entity": r["entity"][:22],
              "dir": r["judge_dir"], "action": r["action"], "z_first": f"{r['z_first']:+.1f}", "adj": f"{r['adj']:+.1f}",
              "quote": (r["quote"] or "")[:70]} for _, r in a.iterrows()]
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")
    # what tier A missed: right events not in A or B
    L.append("## Movers the rules missed (right ≥1σ events not in tier A or B, closed market)")
    L.append("")
    miss = df[closed & df["right"] & ~tiers[list(tiers)[0]] & ~tiers[list(tiers)[2]]].sort_values("judge_conf", ascending=False).drop_duplicates(["video_id", "ticker"]).sort_values("t_wall_et")
    trows = [{"when": str(r["t_wall_et"])[:16], "video": r["video_label"][:34], "ticker": r["ticker"], "entity": r["entity"][:22], "kind": r["kind"],
              "dir": r["judge_dir"], "novelty": r["novelty"], "action": r["action"], "z_first": f"{r['z_first']:+.1f}",
              "past": r["past"], "hedge": r["hedge"], "quote": (r["quote"] or "")[:60]} for _, r in miss.iterrows()]
    L.append(md_table(trows, list(trows[0].keys())))
    L.append("")
    (OUT / "rules.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
