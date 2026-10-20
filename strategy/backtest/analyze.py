"""Product analysis: alert volume, and which filters keep the signals that carried a price drift.

Works on results/measurements.csv plus the signal files. Headline unit = confirmed signal,
primary ticker, first mention of that ticker in the video. Direction = judge (with the stance
rule as the fallback when no judge verdict exists) or stance only.
"""

from __future__ import annotations

import json
import math
from datetime import datetime

import pandas as pd

from backtest.models import ET, SignalFile
from backtest.report import binom_p_two_sided

KEY_H = ["+10m", "+1h", "close_d1", "close_d2", "close_d5"]
HARD_ACTIONS = {"tariff", "investment", "deal", "subsidy", "sanction", "regulation"}


def _pct(x):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x * 100:+.2f}%"


def _rate(x):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x * 100:.0f}%"


def signal_frame(df: pd.DataFrame, files: list[SignalFile]) -> pd.DataFrame:
    """One row per (signal, ticker, horizon) enriched with per-signal attributes."""
    attrs = {}
    for sf in files:
        for s in sf.signals:
            attrs[s.signal_id] = {
                "entity_id": s.entity_id, "n_tickers": len(s.all_tickers()), "n_dict_tickers": len(s.dict_tickers),
                "repeat_count": s.count, "has_judge": bool(s.judge and s.judge.tickers), "video_group": sf.video.group,
                "video_hours": (sf.video.duration or 0) / 3600,
            }
    a = pd.DataFrame.from_dict(attrs, orient="index")
    out = df.merge(a, left_on="signal_id", right_index=True, how="left")
    out["dir_judge"] = out["judge_dir"].where(out["has_judge"], out["stance_dir"])
    out["dir_stance"] = out["stance_dir"]
    return out


def _adj(sub: pd.DataFrame, dir_col: str) -> pd.Series:
    s = sub[sub[dir_col].isin(["up", "down"]) & sub["abn_ret"].notna()]
    return s["abn_ret"] * s[dir_col].map({"up": 1.0, "down": -1.0})


def ladder_row(name: str, sub: pd.DataFrame, base_n: int, dir_col: str) -> dict:
    row = {"filter": name, "signals": int(sub["signal_id"].nunique()), "share": sub["signal_id"].nunique() / max(base_n, 1)}
    for h in KEY_H:
        adj = _adj(sub[sub["horizon"] == h], dir_col)
        n = int(len(adj))
        hits = int((adj > 0).sum())
        std = float(adj.std(ddof=1)) if n > 1 else None
        mean = float(adj.mean()) if n else None
        row[f"{h}_n"] = n
        row[f"{h}_hit"] = hits / n if n else None
        row[f"{h}_mean"] = mean
        row[f"{h}_t"] = (mean / (std / math.sqrt(n))) if (n > 1 and std) else None
        row[f"{h}_p"] = binom_p_two_sided(hits, n) if n else None
    return row


def filters(df: pd.DataFrame) -> list[tuple[str, pd.Series]]:
    conf = df["llm_confidence"].fillna(0)
    jconf = df["judge_confidence"].fillna(0)
    return [
        ("all confirmed signals", pd.Series(True, index=df.index)),
        ("kind = company", df["kind"] == "company"),
        ("kind = sector", df["kind"] == "sector"),
        ("kind = country", df["kind"] == "country"),
        ("kind = asset/person", df["kind"].isin(["asset", "person"])),
        ("stance != neutral", df["stance"] != "neutral"),
        ("LLM confidence >= 0.85", conf >= 0.85),
        ("LLM confidence >= 0.9", conf >= 0.9),
        ("action in hard set (tariff/investment/deal/subsidy/sanction/regulation)", df["action"].isin(HARD_ACTIONS)),
        ("action in praise/criticism/other", ~df["action"].isin(HARD_ACTIONS)),
        ("single ticker (1 dictionary ticker)", df["n_dict_tickers"] <= 1),
        ("basket (>= 3 dictionary tickers)", df["n_dict_tickers"] >= 3),
        ("main speaker only", df["speaker_is_main"] == True),  # noqa: E712
        ("market open at mention", df["market_state"] == "open"),
        ("market closed at mention", df["market_state"] == "closed"),
        ("judge: direction != none", df["judge_dir"].isin(["up", "down"])),
        ("judge: novelty = new", df["novelty"] == "new"),
        ("judge: novelty = repeat", df["novelty"] == "repeat"),
        ("judge: confidence >= 0.6", jconf >= 0.6),
        ("judge: magnitude medium/large", df["magnitude"].isin(["medium", "large"])),
        ("company & stance != neutral", (df["kind"] == "company") & (df["stance"] != "neutral")),
        ("company & hard action", (df["kind"] == "company") & df["action"].isin(HARD_ACTIONS)),
        ("company & hard action & conf >= 0.85", (df["kind"] == "company") & df["action"].isin(HARD_ACTIONS) & (conf >= 0.85)),
        ("hard action & single ticker", df["action"].isin(HARD_ACTIONS) & (df["n_dict_tickers"] <= 1)),
        ("judge new & direction != none", (df["novelty"] == "new") & df["judge_dir"].isin(["up", "down"])),
        ("judge new & company", (df["novelty"] == "new") & (df["kind"] == "company")),
        ("judge new & hard action", (df["novelty"] == "new") & df["action"].isin(HARD_ACTIONS)),
    ]


def _ladder_table(rows: list[dict]) -> list[str]:
    head = "| filter | signals | share | " + " | ".join(f"{h}: n / hit / mean adj / t" for h in KEY_H) + " |"
    lines = [head, "|---|---:|---:|" + "---|" * len(KEY_H)]
    for r in rows:
        cells = []
        for h in KEY_H:
            if r[f"{h}_n"] == 0:
                cells.append("·")
            else:
                t = r[f"{h}_t"]
                cells.append(f"{r[f'{h}_n']} / {_rate(r[f'{h}_hit'])} / {_pct(r[f'{h}_mean'])} / {t:.1f}" if t is not None else
                             f"{r[f'{h}_n']} / {_rate(r[f'{h}_hit'])} / {_pct(r[f'{h}_mean'])} / n/a")
        lines.append(f"| {r['filter']} | {r['signals']} | {r['share'] * 100:.0f}% | " + " | ".join(cells) + " |")
    return lines


def build_analysis(df_all: pd.DataFrame, files: list[SignalFile]) -> tuple[str, dict]:
    df = signal_frame(df_all[df_all["state"] == "confirmed"], files)
    head = df[(df["primary"] == True) & (df["first_mention"] == True)]  # noqa: E712
    n_conf = sum(sf.counts.get("confirmed", 0) for sf in files)
    hours = sum((sf.video.duration or 0) for sf in files) / 3600
    sig_level = head.drop_duplicates("signal_id")

    L: list[str] = []
    L.append("# Product analysis: alert volume and which filters keep the useful signals")
    L.append("")
    L.append(f"_Generated {datetime.now(ET).strftime('%Y-%m-%d %H:%M %Z')} from {len(files)} videos ({hours:.1f} h), {n_conf} confirmed signals._")
    L.append("")

    # ---- volume ----
    L.append("## 1. Alert volume today")
    L.append("")
    per_video = pd.DataFrame([{"video": sf.video.label or sf.video.title[:50], "hours": (sf.video.duration or 0) / 3600,
                               "headsups": sf.counts.get("headsups", 0), "confirmed": sf.counts.get("confirmed", 0),
                               "tickers": sum(len(s.all_tickers()) for s in sf.signals if s.state == "confirmed")} for sf in files])
    L.append(f"- {n_conf / max(hours, 0.01):.1f} confirmed alerts per hour of speech (median video: "
             f"{(per_video['confirmed'] / per_video['hours'].clip(lower=0.05)).median():.1f}/h); "
             f"{per_video['tickers'].sum() / max(n_conf, 1):.1f} tickers per alert on average.")
    kinds = sig_level["kind"].value_counts()
    L.append("- By entity kind: " + ", ".join(f"{k} {v} ({v / len(sig_level) * 100:.0f}%)" for k, v in kinds.items()))
    nov = sig_level["novelty"].fillna("unjudged").value_counts()
    L.append("- Judge novelty: " + ", ".join(f"{k} {v} ({v / len(sig_level) * 100:.0f}%)" for k, v in nov.items()))
    jd = sig_level["judge_dir"].fillna("none").value_counts()
    L.append("- Judge direction (primary ticker): " + ", ".join(f"{k} {v}" for k, v in jd.items()))
    rep = sig_level["repeat_count"]
    L.append(f"- Repeat mentions folded by the 600 s cooldown: {int((rep - 1).sum())} (mean {rep.mean():.1f} mentions per alert).")
    L.append(f"- Basket alerts (3+ tickers): {int((sig_level['n_dict_tickers'] >= 3).sum())} of {len(sig_level)}.")
    L.append("")

    # ---- ladders ----
    base_n = int(head["signal_id"].nunique())
    ladders = {}
    for title, dir_col in (("judge direction (stance as fallback)", "dir_judge"), ("stance only (what the app has today)", "dir_stance")):
        rows = [ladder_row(name, head[mask], base_n, dir_col) for name, mask in filters(head)]
        ladders[dir_col] = rows
        L.append(f"## 2. Filter ladder — direction = {title}")
        L.append("")
        L.append("Sign-adjusted abnormal return (long expected-up, short expected-down), first mentions, primary ticker. "
                 "`share` = fraction of confirmed alerts the filter keeps.")
        L.append("")
        L += _ladder_table(rows)
        L.append("")

    # ---- robustness: by video group ----
    L.append("## 3. Consistency across video groups (judge direction, day +1 and day +2)")
    L.append("")
    L.append("| filter | group | n | hit d1 | mean adj d1 | n d2 | hit d2 | mean adj d2 |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|")
    checks = ["all confirmed signals", "kind = company", "judge: novelty = new", "company & hard action", "judge new & direction != none", "kind = country"]
    fl = dict(filters(head))
    for name in checks:
        for g in sorted(head["video_group"].dropna().unique()):
            sub = head[fl[name] & (head["video_group"] == g)]
            r = ladder_row(name, sub, base_n, "dir_judge")
            L.append(f"| {name} | {g} | {r['close_d1_n']} | {_rate(r['close_d1_hit'])} | {_pct(r['close_d1_mean'])} | "
                     f"{r['close_d2_n']} | {_rate(r['close_d2_hit'])} | {_pct(r['close_d2_mean'])} |")
    L.append("")

    # ---- per entity ----
    L.append("## 4. Entities that fire most (judge direction, day +1)")
    L.append("")
    L.append("| entity | kind | alerts | judged none | mean adj d1 | hit d1 | mean |abn| d1 |")
    L.append("|---|---|---:|---:|---:|---:|---:|")
    d1 = head[head["horizon"] == "close_d1"]
    ent_rows = []
    for (ent, kind), sub in d1.groupby(["entity", "kind"]):
        if len(sub) < 3:
            continue
        adj = _adj(sub, "dir_judge")
        ent_rows.append({"entity": ent, "kind": kind, "alerts": int(len(sub)), "none_share": float((sub["judge_dir"].fillna("none") == "none").mean()),
                         "mean_adj": float(adj.mean()) if len(adj) else None, "hit": float((adj > 0).mean()) if len(adj) else None,
                         "mean_abs": float(sub["abn_ret"].abs().mean()) if sub["abn_ret"].notna().any() else None})
    ent_rows.sort(key=lambda r: -r["alerts"])
    for r in ent_rows[:40]:
        L.append(f"| {r['entity']} | {r['kind']} | {r['alerts']} | {_rate(r['none_share'])} | {_pct(r['mean_adj'])} | {_rate(r['hit'])} | {_pct(r['mean_abs'])} |")
    L.append("")

    # ---- by action ----
    L.append("## 5. By LLM action label (judge direction, day +1 / day +2)")
    L.append("")
    L.append("| action | alerts | hit d1 | mean adj d1 | hit d2 | mean adj d2 |")
    L.append("|---|---:|---:|---:|---:|---:|")
    act_rows = []
    for act, sub in head.groupby("action"):
        r = ladder_row(act, sub, base_n, "dir_judge")
        act_rows.append(r)
        L.append(f"| {act} | {r['signals']} | {_rate(r['close_d1_hit'])} | {_pct(r['close_d1_mean'])} | {_rate(r['close_d2_hit'])} | {_pct(r['close_d2_mean'])} |")
    L.append("")

    summary = {"generated": datetime.now(ET).isoformat(), "videos": len(files), "hours": hours, "confirmed": n_conf,
               "ladders": ladders, "entities": ent_rows, "actions": act_rows}
    return "\n".join(L), json.loads(json.dumps(summary, default=lambda o: None if (isinstance(o, float) and math.isnan(o)) else str(o)))
