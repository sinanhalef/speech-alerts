import pandas as pd

from backtest.judge import parse_judgement, stance_direction
from backtest.report import binom_p_two_sided, directional_stats, horizon_stats


def test_parse_judgement_salvages_and_flags_additions():
    text = '```json\n{"tickers": [{"ticker": "intc", "direction": "up", "confidence": 0.7, "magnitude": "medium", "novelty": "new", "horizon": "days", "rationale": "stake"}, {"ticker": "AMD", "direction": "down", "confidence": 0.55, "added": true}, {"ticker": "", "direction": "up"}, {"ticker": "NVDA", "direction": "sideways"}], "summary": "ok"}\n```'
    j = parse_judgement(text, "m", ["INTC"])
    assert [t.ticker for t in j.tickers] == ["INTC", "AMD", "NVDA"]
    assert j.tickers[0].direction == "up" and not j.tickers[0].added_by_judge
    assert j.tickers[1].added_by_judge and j.tickers[2].added_by_judge
    assert j.tickers[2].direction == "none" and j.tickers[2].novelty == "unclear"
    assert parse_judgement("no json here", "m", []).tickers == []
    assert stance_direction("positive") == "up" and stance_direction("neutral") == "none"


def test_binomial_p():
    assert binom_p_two_sided(5, 10) == 1.0
    assert abs(binom_p_two_sided(10, 10) - 2 / 1024) < 1e-9
    assert binom_p_two_sided(0, 0) is None


def test_stats_tables():
    rows = []
    for i, (d, h, abn) in enumerate([("up", "+1h", 0.01), ("up", "+1h", -0.02), ("down", "+1h", -0.03), ("up", "close_d1", 0.05), ("none", "+1h", 0.5)]):
        rows.append({"judge_dir": d, "hit_judge": (abn > 0) if d == "up" else ((abn < 0) if d == "down" else None), "horizon": h, "abn_ret": abn, "ret": abn})
    df = pd.DataFrame(rows)
    up = {s["horizon"]: s for s in horizon_stats(df, "judge_dir", "up", "hit_judge")}
    assert up["+1h"]["n"] == 2 and up["+1h"]["hit_rate"] == 0.5 and abs(up["+1h"]["mean_abn"] - (-0.005)) < 1e-9
    assert up["close_d1"]["n"] == 1 and up["open"]["n"] == 0
    d = {s["horizon"]: s for s in directional_stats(df, "judge_dir")}
    assert d["+1h"]["n"] == 3 and abs(d["+1h"]["mean_adj"] - (0.01 - 0.02 + 0.03) / 3) < 1e-9 and d["+1h"]["hit_rate"] == 2 / 3
