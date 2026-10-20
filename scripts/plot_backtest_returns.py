"""Render docs/images/backtest_returns.png from strategy/data/results/measurements.csv.

    uv run --project strategy --with matplotlib python scripts/plot_backtest_returns.py docs/images/backtest_returns.png
"""
import pandas as pd, numpy as np, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
out = sys.argv[1]
d = pd.read_csv("strategy/data/results/measurements.csv", low_memory=False)
d = d[(d.state == "confirmed") & (d.primary == True) & (d.first_mention == True) & d.abn_ret.notna() & d.stance_dir.isin(["up", "down"])].copy()
d["signed"] = d.abn_ret * d.stance_dir.map({"up": 1.0, "down": -1.0})
HORIZONS = ["+10m", "+1h", "close_d1", "close_d2", "close_d5", "close_d21"]
LABELS = {"+10m": "+10 min", "+1h": "+1 h", "close_d1": "day +1", "close_d2": "day +2", "close_d5": "day +5", "close_d21": "day +21"}
hard = {"investment", "deal", "sanction", "regulation", "subsidy", "tariff"}
g_all = d.groupby("horizon").signed.mean().reindex(HORIZONS) * 100
sub = d[(d.kind == "company") & d.action.isin(hard)]
g_sub = sub.groupby("horizon").signed.mean().reindex(HORIZONS) * 100
n_all = d[d.horizon == "close_d1"].shape[0]; n_sub = sub[sub.horizon == "close_d1"].shape[0]

act = d[d.horizon == "close_d1"].groupby("action").agg(ret=("signed", "mean"), n=("signed", "size"))
act = act[act.n >= 30].sort_values("ret"); act["ret"] *= 100

SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=SURF, gridspec_kw={"width_ratios": [1.1, 1], "wspace": 0.35})
for a in (a1, a2):
    a.set_facecolor(SURF)
    for s in ("top", "right", "left"): a.spines[s].set_visible(False)
    a.tick_params(length=0)

# left: grouped bars by horizon, two series (legend + direct label)
x = np.arange(len(HORIZONS)); w = 0.34
b1 = a1.bar(x - w/2 - 0.01, g_all.values, w, color=INK2, alpha=0.55, label=f"all stance-labelled alerts (n={n_all})", zorder=3)
b2 = a1.bar(x + w/2 + 0.01, g_sub.values, w, color=BLUE, label=f"company + hard action (n={n_sub})", zorder=3)
a1.axhline(0, color=INK2, lw=0.8, zorder=2)
a1.set_xticks(x, [LABELS[h] for h in HORIZONS])
a1.yaxis.set_major_formatter(PercentFormatter(decimals=1)); a1.yaxis.grid(True, color=GRID, lw=0.8, zorder=1)
a1.set_title("Sign-adjusted abnormal return after a mention", loc="left", fontsize=11, fontweight="bold", color=INK)
for bars, dx in ((b1, -3), (b2, 3)):
    for r in bars:
        v = r.get_height(); a1.annotate(f"{v:+.2f}", (r.get_x() + r.get_width()/2, v), xytext=(dx, 3 if v >= 0 else -10),
                                        textcoords="offset points", ha="center", fontsize=7, color=INK2)
a1.legend(frameon=False, fontsize=8.5, loc="upper left")

# right: day+1 by action label, polarity colored
cols = [BLUE if v >= 0 else ORANGE for v in act.ret]
a2.barh(act.index, act.ret, color=cols, height=0.6, zorder=3)
a2.axvline(0, color=INK2, lw=0.8, zorder=2)
a2.xaxis.set_major_formatter(PercentFormatter(decimals=1)); a2.xaxis.grid(True, color=GRID, lw=0.8, zorder=1)
a2.set_title("Day +1 by action label (n ≥ 30)", loc="left", fontsize=11, fontweight="bold", color=INK)
for i, (lab, row) in enumerate(act.iterrows()):
    a2.annotate(f"{row.ret:+.2f}%  (n={int(row.n)})", (row.ret, i), xytext=(5 if row.ret >= 0 else -5, 0),
                textcoords="offset points", va="center", ha="left" if row.ret >= 0 else "right", fontsize=8, color=INK2)
lim = max(abs(act.ret.min()), abs(act.ret.max())) * 1.9; a2.set_xlim(-lim, lim)
fig.text(0.01, 0.01, f"Abnormal return = ticker return − SPY over the same window; long for positive stance, short for negative; neutral mentions excluded. "
         "{d.video_id.nunique()} White House videos, Jan 2025 – Sep 2026, Yahoo prices.", fontsize=7.5, color=INK2)
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURF)
print(g_all.round(3).to_dict()); print(g_sub.round(3).to_dict()); print(act.round(3))
