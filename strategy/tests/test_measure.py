from datetime import date, datetime

import pytest

from backtest.measure import Measurer, measure_files
from backtest.models import ET, LlmMention, Judgement, JudgeTicker, Signal, SignalFile, VideoMeta
from tests.conftest import FakeStore


def _signal(t_wall: datetime, ticker="AAA", stance="positive", judge_dir="up", state="confirmed", t_audio=100.0):
    sig = Signal(
        signal_id=f"v:{int(t_audio):05d}:aaa", video_id="v", entity_id="aaa", entity="Triple A", kind="company", alias="aaa",
        text_span="AAA", dict_tickers=[ticker], t_audio=t_audio, t_wall=t_wall.timestamp(), t_wall_et=t_wall.isoformat(),
        state=state, llm=LlmMention(entity="Triple A", tickers=[ticker], stance=stance, confidence=0.9),
        judge=Judgement(model="x", tickers=[JudgeTicker(ticker=ticker, direction=judge_dir, confidence=0.7)]),
    )
    return sig


def _file(*sigs):
    meta = VideoMeta(id="v", url="u", title="T", duration=600, t0=0)
    return SignalFile(video=meta, counts={"headsups": len(sigs), "confirmed": len(sigs)}, signals=list(sigs))


def test_open_state_intraday_and_daily(store):
    # 2026-09-10 11:00 ET, AAA slope 0.01/min -> +10m = +0.10 on ~base
    t = datetime(2026, 9, 10, 11, 0, tzinfo=ET)
    df = measure_files([_file(_signal(t))], store)
    rows = {r["horizon"]: r for r in df[df["ticker"] == "AAA"].to_dict("records")}
    assert rows["open"]["reason"] == "n/a_open_state"
    r10 = rows["+10m"]
    assert r10["resolution"] == "1m" and r10["market_state"] == "open"
    assert r10["p_h"] - r10["p0"] == pytest.approx(0.10, abs=1e-6)
    assert r10["spy_ret"] == pytest.approx(0.0)
    assert r10["abn_ret"] == pytest.approx(r10["ret"])
    assert r10["hit_judge"] is True and r10["hit_stance"] is True
    # daily horizon uses intraday baseline and daily close; d+1 is 2026-09-11
    d1 = rows["close_d1"]
    assert d1["p_h_at"] == "2026-09-11" and d1["baseline_kind"] == "last_completed_bar"
    assert rows["close_d21"]["reason"] == "not_yet"


def test_after_close_intraday_is_blank(store):
    t = datetime(2026, 9, 10, 15, 30, tzinfo=ET)
    df = measure_files([_file(_signal(t))], store)
    rows = {r["horizon"]: r for r in df[df["ticker"] == "AAA"].to_dict("records")}
    assert rows["+10m"]["p_h"] is not None
    assert rows["+1h"]["reason"] == "after_close"
    assert rows["close_d0"]["p_h_at"] == "2026-09-10"


def test_closed_state_next_open(store):
    # Friday 2026-09-04 18:00 -> next session Tuesday 2026-09-08, baseline Friday close
    t = datetime(2026, 9, 4, 18, 0, tzinfo=ET)
    df = measure_files([_file(_signal(t, stance="negative", judge_dir="down"))], store)
    rows = {r["horizon"]: r for r in df[df["ticker"] == "AAA"].to_dict("records")}
    assert rows["open"]["market_state"] == "closed" and rows["open"]["session"] == "2026-09-08"
    assert rows["open"]["p0_at"] == "2026-09-04" and rows["open"]["baseline_kind"] == "prev_close"
    assert rows["open"]["p_h_at"] == "2026-09-08"
    # daily close of Friday = base+idx; Tuesday open = base+idx+1 - 0.5 -> +0.5 change
    assert rows["open"]["p_h"] - rows["open"]["p0"] == pytest.approx(0.5)
    assert rows["+10m"]["origin_et"].startswith("2026-09-08T09:30")
    assert rows["+10m"]["hit_judge"] is True  # Tuesday opens 3.9 below its close = below Friday close; judge said down
    assert rows["close_d0"]["p_h_at"] == "2026-09-08"
    assert rows["close_d5"]["p_h_at"] == "2026-09-15"


def test_coarse_bars_limit_horizons(store):
    store.intraday_days = 0  # only 60m allowed via finest_interval_for age gate below
    t = datetime(2025, 8, 6, 16, 40, tzinfo=ET)  # outside calendar range -> no session
    df = measure_files([_file(_signal(t))], store)
    assert set(df["reason"].dropna()) <= {"no_session"}


def test_first_mention_and_no_data(store):
    t1 = datetime(2026, 9, 10, 11, 0, tzinfo=ET)
    t2 = datetime(2026, 9, 10, 11, 30, tzinfo=ET)
    s1, s2 = _signal(t1, t_audio=100), _signal(t2, t_audio=1900)
    s3 = _signal(t1, ticker="ZZZ", t_audio=200)
    df = measure_files([_file(s1, s2, s3)], store)
    assert df[(df["signal_id"] == s1.signal_id)]["first_mention"].all()
    assert not df[(df["signal_id"] == s2.signal_id)]["first_mention"].any()
    assert (df[df["ticker"] == "ZZZ"]["reason"] == "no_data").all()


def test_price_at_uses_completed_bars_only(store):
    m = Measurer(store)
    t = datetime(2026, 9, 10, 10, 0, tzinfo=ET)
    px = m.price_at("AAA", t, max_interval_min=60, prefer=["60m"])
    # 60m bar 09:30 closes at 10:30 -> not completed at 10:00 -> fall back to day open
    assert px.resolution == "60m/open"
    px = m.price_at("AAA", t.replace(minute=45), max_interval_min=60, prefer=["60m"])
    assert px.resolution == "60m" and px.when.startswith("2026-09-10T09:30")
