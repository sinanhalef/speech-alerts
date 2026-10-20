"""Sagas: how the market treated repeated threats/promises over time (pharma MFN, country tariffs, chips, steel, oil, crypto).

For each theme, lists every confirmed mention in time order with the first reaction and next-day
abnormal returns of the primary ticker, so the "threat fatigue" / "relief on the concrete action"
pattern can be seen. Writes out/sagas.md.
"""

from __future__ import annotations

import pandas as pd

from common import OUT, fmt_pct, fmt_z, md_table

THEMES = {
    "Pharma / drug prices / MFN": {"entities": ["Pharmaceuticals", "Pfizer", "Eli Lilly", "Novo Nordisk", "Merck", "Johnson & Johnson", "AstraZeneca", "Vaccine makers", "Moderna"],
                                    "tickers": ["XPH", "PFE", "LLY", "NVO", "MRK", "JNJ", "AZN", "MRNA"]},
    "Health insurers": {"entities": ["Health insurers", "UnitedHealth", "Cigna", "Humana", "Elevance", "CVS"], "tickers": ["UNH", "CI", "HUM", "ELV", "CVS"]},
    "Semiconductors / Nvidia / chips": {"entities": ["Semiconductors", "Nvidia", "TSMC", "Taiwan", "Intel", "Micron"], "tickers": ["SMH", "SOXX", "NVDA", "TSM", "INTC", "MU"]},
    "Steel / aluminum": {"entities": ["Steel", "U.S. Steel", "Aluminum", "Nucor", "Cleveland-Cliffs"], "tickers": ["SLX", "NUE", "STLD", "CLF", "X", "AA", "CENX"]},
    "China": {"entities": ["China"], "tickers": ["FXI", "KWEB", "MCHI"]},
    "Canada / Mexico": {"entities": ["Canada", "Mexico"], "tickers": ["EWC", "EWW"]},
    "European Union": {"entities": ["European Union", "Germany", "United Kingdom"], "tickers": ["VGK", "EZU", "FEZ", "EWG", "EWU"]},
    "Japan / South Korea / India": {"entities": ["Japan", "South Korea", "India"], "tickers": ["EWJ", "EWY", "INDA", "EPI"]},
    "Oil / gas": {"entities": ["Oil", "Natural gas / LNG", "Refiners", "Cheniere", "Exxon", "Chevron"], "tickers": ["XLE", "USO", "UNG", "LNG", "VLO", "XOM", "CVX"]},
    "Coal": {"entities": ["Coal"], "tickers": ["BTU", "AMR", "ARCH"]},
    "Automakers / EV": {"entities": ["Automakers", "Electric vehicles", "Tesla", "Ford", "General Motors", "Stellantis", "Toyota", "Honda"], "tickers": ["CARZ", "TSLA", "F", "GM", "STLA", "TM", "HMC"]},
    "Crypto": {"entities": ["Bitcoin", "Crypto", "Coinbase", "Stablecoins"], "tickers": ["IBIT", "COIN", "MSTR", "HOOD", "CRCL"]},
    "Defense": {"entities": ["Defense", "Lockheed Martin", "Northrop Grumman", "RTX (Raytheon)", "Boeing", "General Dynamics", "Shipbuilders (Navy)"], "tickers": ["ITA", "LMT", "NOC", "RTX", "BA", "GD", "HII"]},
    "Federal Reserve / rates": {"entities": ["Federal Reserve", "Jerome Powell"], "tickers": ["TLT", "KRE", "XLF"]},
    "Stock market (macro)": {"entities": ["Stock market"], "tickers": ["SPY", "DIA", "QQQ"]},
}


def main() -> None:
    df = pd.read_csv(OUT / "mentions_z.csv", low_memory=False)
    L = ["# Sagas: repeated themes over time, first reaction and next day", "",
         "Each row is one confirmed mention; of the theme's tickers attached to that mention, the one with the largest |z_first| is shown. "
         "`first` = opening gap (closed) or +1 h (open); z = / the ticker's abnormal daily vol. "
         "Read down a theme to see how the market treated the n-th repetition of a threat or promise.", ""]
    for theme, spec in THEMES.items():
        cand = df[(df["entity"].isin(spec["entities"]) | df["ticker"].isin(spec["tickers"])) & df["z_first"].notna()].copy()
        if cand.empty:
            continue
        cand["absz"] = cand["z_first"].abs()
        sub = cand.sort_values("absz", ascending=False).drop_duplicates("signal_id").sort_values("t_wall_et")
        L.append(f"## {theme} — {len(sub)} mentions, {sub['video_id'].nunique()} videos")
        L.append("")
        z = sub["z_first"].dropna()
        adj = (sub["z_first"] * sub["exp_sign"])[sub["exp_sign"] != 0].dropna()
        L.append(f"- share |z_first| ≥ 1: {(z.abs() >= 1).mean() * 100:.0f}%; ≥ 2: {(z.abs() >= 2).mean() * 100:.0f}%; "
                 f"directional hit {(adj > 0).mean() * 100:.0f}% (n={len(adj)}), mean adj z {adj.mean():+.2f}")
        L.append("")
        rows = []
        for _, r in sub.iterrows():
            rows.append({"when (ET)": str(r["t_wall_et"])[:16], "st": "C" if r["market_state"] == "closed" else "O", "entity": r["entity"][:22], "tk": r["ticker"],
                         "stance/action": f"{r['stance']}/{r['action']}", "judge": f"{r['judge_dir']}/{r['novelty']}",
                         "first": fmt_pct(r["first"], 1), "z": fmt_z(r["z_first"]), "d1": fmt_pct(r["d1"], 1), "d2": fmt_pct(r["d2"], 1),
                         "quote": (r["quote"] or "")[:75]})
        L.append(md_table(rows, list(rows[0].keys())))
        L.append("")
    (OUT / "sagas.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
