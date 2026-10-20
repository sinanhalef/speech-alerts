from datetime import datetime

from backtest.models import ET, Judgement, JudgeTicker, LlmMention, Signal, SignalFile, VideoMeta
from backtest.portfolio import build_trades, simulate


def _sig(t, ticker="AAA", stance="positive", t_audio=100.0):
    return Signal(signal_id=f"v:{int(t_audio):05d}:{ticker.lower()}", video_id="v", entity_id=ticker.lower(), entity=ticker, kind="company",
                  alias=ticker, text_span=ticker, dict_tickers=[ticker], t_audio=t_audio, t_wall=t.timestamp(), t_wall_et=t.isoformat(),
                  state="confirmed", llm=LlmMention(entity=ticker, tickers=[ticker], stance=stance, confidence=0.9),
                  judge=Judgement(model="x", tickers=[JudgeTicker(ticker=ticker, direction="up", novelty="new")]))


def test_trades_and_simulation(store):
    meta = VideoMeta(id="v", url="u", title="T", duration=600, t0=0)
    # in-hours mention on Thu 2026-09-03 11:00 -> instant entry that day, exit close of 5 sessions later (2026-09-11, Labor Day skipped)
    sf = SignalFile(video=meta, counts={}, signals=[_sig(datetime(2026, 9, 3, 11, 0, tzinfo=ET)), _sig(datetime(2026, 9, 3, 11, 0, tzinfo=ET), stance="negative", t_audio=200)])
    trades, skipped = build_trades([sf], store, select="stance_up", rule="instant")
    assert len(trades) == 1 and skipped == {"no_data": 0, "not_yet": 0, "no_entry": 0}
    t = trades[0]
    assert str(t.entry_day) == "2026-09-03" and str(t.exit_day) == "2026-09-11" and t.entry_kind.startswith("mention")
    assert len(t.path) == 6  # entry day close + 5 sessions
    trades2, _ = build_trades([sf], store, select="stance_up", rule="next_open")
    assert str(trades2[0].entry_day) == "2026-09-04" and trades2[0].entry_kind == "next open"
    res = simulate(trades, store)
    # fake daily closes rise by 1 per session: exit close = entry-day close + 5
    assert res["trades"] == 1 and res["final_equity"] > 10_000 and abs(res["return"] - t.ret) < 1e-9
    assert res["win_rate"] == 1.0 and res["days_invested"] == 6
    assert build_trades([sf], store, select="judge_up_new", rule="instant")[0][0].ticker == "AAA"
