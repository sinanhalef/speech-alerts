"""Aggregate measurements into results/summary.md and results/summary.json."""

from __future__ import annotations

import json
import math
from datetime import datetime

import pandas as pd

from backtest.models import ET, HORIZONS, SignalFile

HEADLINE_HORIZONS = ["open", "+10m", "+30m", "+1h", "+2h", "close_d0", "close_d1", "close_d2", "close_d5", "close_d21"]


def binom_p_two_sided(hits: int, n: int) -> float | None:
    """Exact two-sided binomial test against p = 0.5."""
    if n == 0:
        return None
    centre = n / 2
    dev = abs(hits - centre)
    total = sum(math.comb(n, k) for k in range(n + 1) if abs(k - centre) >= dev - 1e-9)
    return min(1.0, total / 2**n)


def _pct(x: float | None) -> str:
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x * 100:+.2f}%"


def _rate(x: float | None) -> str:
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x * 100:.0f}%"


def _pv(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.2f}"


def horizon_stats(df: pd.DataFrame, dir_col: str, direction: str, hit_col: str) -> list[dict]:
    """Per horizon: n, hit rate, mean/median abnormal, mean raw, p-value for one expected direction."""
    sub = df[(df[dir_col] == direction) & df["abn_ret"].notna()]
    out = []
    for h in HORIZONS:
        s = sub[sub["horizon"] == h]
        n = int(len(s))
        hits = int(s[hit_col].fillna(False).astype(bool).sum()) if n else 0
        directional = direction in ("up", "down")
        out.append({
            "horizon": h, "n": n,
            "hit_rate": hits / n if (n and directional) else None,
            "mean_abn": float(s["abn_ret"].mean()) if n else None,
            "median_abn": float(s["abn_ret"].median()) if n else None,
            "mean_raw": float(s["ret"].mean()) if n else None,
            "p_value": binom_p_two_sided(hits, n) if (n and directional) else None,
        })
    return out


def directional_stats(df: pd.DataFrame, dir_col: str) -> list[dict]:
    """Sign-adjusted abnormal return (long expected-up, short expected-down) per horizon."""
    sub = df[df[dir_col].isin(["up", "down"]) & df["abn_ret"].notna()].copy()
    sub["adj"] = sub["abn_ret"] * sub[dir_col].map({"up": 1.0, "down": -1.0})
    out = []
    for h in HORIZONS:
        s = sub[sub["horizon"] == h]
        n = int(len(s))
        hits = int((s["adj"] > 0).sum()) if n else 0
        std = float(s["adj"].std(ddof=1)) if n > 1 else None
        mean = float(s["adj"].mean()) if n else None
        tstat = (mean / (std / math.sqrt(n))) if (n > 1 and std and std > 0) else None
        out.append({"horizon": h, "n": n, "hit_rate": hits / n if n else None, "mean_adj": mean,
                    "median_adj": float(s["adj"].median()) if n else None, "t_stat": tstat,
                    "p_value": binom_p_two_sided(hits, n) if n else None})
    return out


def _table(stats: list[dict], value_keys: list[tuple[str, str]]) -> list[str]:
    head = "| horizon | n | hit rate | " + " | ".join(label for _, label in value_keys) + " | p (hit≠50%) |"
    sep = "|---|---:|---:|" + "---:|" * len(value_keys) + "---:|"
    lines = [head, sep]
    for s in stats:
        if s["n"] == 0:
            lines.append(f"| {s['horizon']} | 0 | n/a | " + " | ".join("n/a" for _ in value_keys) + " | n/a |")
            continue
        vals = " | ".join(_pct(s.get(k)) if k != "t_stat" else (f"{s[k]:.2f}" if s.get(k) is not None else "n/a") for k, _ in value_keys)
        lines.append(f"| {s['horizon']} | {s['n']} | {_rate(s['hit_rate'])} | {vals} | {_pv(s['p_value'])} |")
    return lines


def build_summary(df_all: pd.DataFrame, files: list[SignalFile]) -> tuple[str, dict]:
    videos = {sf.video.id: sf for sf in files}
    hours = sum((sf.video.duration or 0) for sf in files) / 3600
    n_headsups = sum(sf.counts.get("headsups", 0) for sf in files)
    n_conf = sum(sf.counts.get("confirmed", 0) for sf in files)
    n_retr = sum(sf.counts.get("retracted", 0) for sf in files)
    confirmed = [s for sf in files for s in sf.signals if s.state == "confirmed"]
    stance_counts = {k: sum(1 for s in confirmed if s.stance_direction() == k) for k in ("up", "down", "none")}
    judge_counts = {k: sum(1 for s in confirmed if s.primary_ticker and s.judge_direction(s.primary_ticker) == k) for k in ("up", "down", "none")}
    n_judged = sum(1 for s in confirmed if s.judge is not None)

    df = df_all[df_all["state"] == "confirmed"] if "state" in df_all.columns else df_all
    headline = df[(df["primary"] == True) & (df["first_mention"] == True)]  # noqa: E712
    measured_signals = headline[headline["abn_ret"].notna()]["signal_id"].nunique()

    L: list[str] = []
    L.append("# Do the President's stock mentions move prices? Backtest of the speechalerts signals")
    L.append("")
    L.append(f"_Generated {datetime.now(ET).strftime('%Y-%m-%d %H:%M %Z')}._")
    L.append("")
    L.append("## Headline")
    L.append("")
    L.append(f"We analysed **{len(files)} videos** ({hours:.1f} h of audio). The live algorithm (dictionary + Claude Haiku "
             f"confirmation, replayed offline) raised **{n_headsups} heads-ups**, confirmed **{n_conf} signals** and retracted "
             f"{n_retr}.")
    L.append("")
    L.append(f"Of the {n_conf} confirmed signals, the live app's stance labels {stance_counts['up']} as positive (expected up), "
             f"{stance_counts['down']} negative (expected down) and {stance_counts['none']} neutral. The Sonnet 5 judge "
             f"({n_judged} judged) expects the primary ticker to go up in {judge_counts['up']}, down in {judge_counts['down']} "
             f"and sees no price relevance in {judge_counts['none']}.")
    L.append("")
    L.append(f"{measured_signals} signals had a measurable primary ticker (first mention of that ticker in the video; "
             f"US-listed with Yahoo data). Returns below are **abnormal** = ticker return minus SPY return over the same window, "
             f"measured from the last completed bar before the mention (market open) or the previous close (market closed).")
    L.append("")

    sections = []
    for title, dir_col, hit_col in (("Judge (Sonnet 5) expectation", "judge_dir", "hit_judge"),
                                    ("Stance baseline (what the live app shows today)", "stance_dir", "hit_stance")):
        L.append(f"## {title}")
        L.append("")
        for direction, label in (("up", "Expected UP"), ("down", "Expected DOWN")):
            stats = horizon_stats(headline, dir_col, direction, hit_col)
            L.append(f"### {label} (first mentions, primary ticker)")
            L.append("")
            L += _table(stats, [("mean_abn", "mean abn"), ("median_abn", "median abn"), ("mean_raw", "mean raw")])
            L.append("")
            sections.append({"table": title, "direction": direction, "stats": stats})
        dstats = directional_stats(headline, dir_col)
        L.append("### Directional (long expected-up, short expected-down; sign-adjusted abnormal return)")
        L.append("")
        L += _table(dstats, [("mean_adj", "mean adj"), ("median_adj", "median adj"), ("t_stat", "t-stat")])
        L.append("")
        sections.append({"table": title, "direction": "directional", "stats": dstats})
        none_stats = horizon_stats(headline, dir_col, "none", hit_col)
        L.append("### Expected NONE (control: judged not price-relevant)")
        L.append("")
        L += _table(none_stats, [("mean_abn", "mean abn"), ("median_abn", "median abn")])
        L.append("")

    L.append("## Splits (judge expectation, directional, sign-adjusted abnormal return)")
    L.append("")
    splits = {}
    for name, mask in (
        ("market open at mention", headline["market_state"] == "open"),
        ("market closed at mention", headline["market_state"] == "closed"),
        ("recent videos (minute data)", headline["group"] == "recent"),
        ("2025 headline videos", headline["group"] == "headline"),
        ("expansion videos (White House, Jun 2025 - Sep 2026)", headline["group"] == "expansion"),
        ("novelty = new", headline["novelty"] == "new"),
        ("novelty = repeat", headline["novelty"] == "repeat"),
        ("judge confidence >= 0.65", headline["judge_confidence"].fillna(0) >= 0.65),
        ("main speaker only", headline["speaker_is_main"] == True),  # noqa: E712
        ("all tickers, all mentions (not just first/primary)", df["abn_ret"].notna()),
    ):
        base = df if name.startswith("all tickers") else headline
        st = directional_stats(base[mask], "judge_dir")
        splits[name] = st
        L.append(f"### {name}")
        L.append("")
        L += _table(st, [("mean_adj", "mean adj"), ("median_adj", "median adj"), ("t_stat", "t-stat")])
        L.append("")

    L.append("## Per-video signals")
    L.append("")
    for sf in files:
        v = sf.video
        when = v.t0_et().strftime("%Y-%m-%d %H:%M ET") if v.t0_et() else "unknown start"
        L.append(f"### {v.label or v.title} — `{v.id}`")
        L.append(f"_{v.title} ({v.channel}); stream start {when}; {(v.duration or 0) / 60:.0f} min; "
                 f"{sf.counts.get('headsups', 0)} heads-ups / {sf.counts.get('confirmed', 0)} confirmed / {sf.counts.get('retracted', 0)} retracted_")
        L.append("")
        L.append("| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |")
        L.append("|---|---|---|---|---|---|---|---:|---:|---:|---:|")
        for s in sorted(sf.signals, key=lambda x: x.t_audio):
            if s.state != "confirmed":
                continue
            pt = s.primary_ticker or ""
            je = s.judge_entry(pt) if pt else None
            rows = df[(df["signal_id"] == s.signal_id) & (df["ticker"] == pt)]
            def cell(h: str) -> str:
                r = rows[rows["horizon"] == h]
                if r.empty or pd.isna(r.iloc[0]["abn_ret"]):
                    return "·"
                return _pct(float(r.iloc[0]["abn_ret"]))
            t = f"{int(s.t_audio) // 60}:{int(s.t_audio) % 60:02d}"
            quote = (s.llm.quote if s.llm else "").replace("|", "/")[:70]
            L.append(f"| {t} | {s.entity} | {', '.join(s.all_tickers()[:4])} | {s.llm.stance if s.llm else ''} | "
                     f"{(je.direction + f' ({je.confidence:.2f})') if je else '·'} | {je.novelty if je else '·'} | {quote} | "
                     f"{cell('open')} | {cell('+1h')} | {cell('close_d1')} | {cell('close_d5')} |")
        L.append("")

    unjudged = sum(1 for s in confirmed if s.judge is None or not s.judge.tickers)
    delisted = sorted({r for r in df_all[df_all["reason"].isin(["no_data", "no_bar"])]["ticker"].dropna().unique()})
    L.append("## Coverage")
    L.append("")
    L.append(f"- {unjudged} of {n_conf} confirmed signals have no judge verdict (API credit ran out / unparseable reply); they count as "
             f"'none' in the judge tables and are still in the stance tables. Re-run `uv run backtest judge` to fill them.")
    L.append(f"- Tickers without usable Yahoo data: {', '.join(delisted) if delisted else 'none'} (delisted or OTC).")
    L.append("- Where Yahoo's intraday bars and split-adjusted daily closes disagreed (a later split), the bars were rescaled to the daily basis.")
    L.append("")
    L.append("## Caveats")
    L.append("")
    L += [
        "- Small sample: a handful of videos and a few dozen signals. Hit rates near 50% with p > 0.1 are noise.",
        "- Judge look-ahead: for 2025 events the judge model may remember what happened; the stance baseline cannot. Compare the 'recent videos' split, which is after the model's knowledge.",
        "- Timing: t_audio is mapped to wall clock via the livestream's start timestamp; if the recording was trimmed the mapping is off by that amount. Baseline is the mention minute, not the alert time (live latency is ~5-10 s).",
        "- Intraday horizons need bars no coarser than the horizon: Yahoo serves 1-minute bars for ~30 days, 5-minute for ~60 days and hourly for ~2 years, so +10m/+30m are blank for 2025 events.",
        "- +1h/+2h are blank when the session ended in between (see close_d0 instead). Closed-market mentions measure intraday horizons from the next session's open.",
        "- Abnormal return subtracts SPY over the identical window; sector moves are not removed.",
        "- Multi-ticker signals (sector ETFs, judge additions) are in the 'all tickers' split only; the headline tables use one primary ticker per signal.",
    ]
    L.append("")
    summary = {
        "generated": datetime.now(ET).isoformat(),
        "videos": len(files), "hours": hours, "headsups": n_headsups, "confirmed": n_conf, "retracted": n_retr,
        "stance_counts": stance_counts, "judge_counts": judge_counts, "measured_signals": int(measured_signals),
        "tables": sections, "splits": splits,
        "per_video": {sf.video.id: {"label": sf.video.label, "title": sf.video.title, "counts": sf.counts} for sf in files},
    }
    return "\n".join(L), json.loads(json.dumps(summary, default=lambda o: None if (isinstance(o, float) and math.isnan(o)) else str(o)))
