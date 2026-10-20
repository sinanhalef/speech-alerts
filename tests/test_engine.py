import pytest

from speechalerts.alerts.engine import AlertEngine
from speechalerts.models import Alert, AlertState, Mention, TranscriptSegment


class Collect:
    def __init__(self):
        self.alerts: list[Alert] = []

    async def alert(self, a):
        self.alerts.append(a)

    async def segment(self, s: TranscriptSegment):
        pass

    async def close(self):
        pass


@pytest.fixture
def engine():
    sink = Collect()
    eng = AlertEngine([sink], source="test", cooldown_seconds=600, min_confidence=0.6)
    return eng, sink


def cands(dictionary, text, start=10.0):
    return dictionary.match(TranscriptSegment(text=text, t_audio_start=start, t_audio_end=start + 4, t_wall=1000.0, is_final=True))


async def test_headsup_then_confirm(dictionary, engine):
    eng, sink = engine
    c = cands(dictionary, "We're taking a 10 percent stake in Intel.")
    emitted = await eng.on_candidates(c)
    assert [a.state for a in emitted] == [AlertState.HEADSUP]
    assert emitted[0].tickers == ["INTC"]

    # Same entity again inside the cooldown: no new alert, counter bumps.
    again = await eng.on_candidates(cands(dictionary, "Intel, great company, Intel."))
    assert again == []
    assert emitted[0].count == 2

    m = Mention(entity="Intel", tickers=["INTC"], stance="positive", action="investment", confidence=0.95, quote="taking a 10 percent stake in Intel", summary="The President says the US is taking a stake in Intel.")
    confirmed = await eng.on_confirmation([m], c, t_llm=1002.0)
    assert [a.state for a in confirmed] == [AlertState.CONFIRMED]
    assert confirmed[0].parent_id == emitted[0].id
    assert emitted[0].state == AlertState.CONFIRMED
    assert sink.alerts[-1].summary.startswith("The President says")


async def test_retraction_when_llm_rejects(dictionary, engine):
    eng, sink = engine
    c = cands(dictionary, "Walmart should eat the tariffs.")
    heads = await eng.on_candidates(c)
    assert heads and heads[0].entity == "Walmart"
    out = await eng.on_confirmation([], c, t_llm=1001.0)
    assert [a.state for a in out] == [AlertState.RETRACTED]
    assert out[0].parent_id == heads[0].id
    # After retraction the entity is muted for the (short) retraction cooldown.
    again = await eng.on_candidates(c)
    assert again == []
    eng.retract_cooldown = 0
    assert len(await eng.on_candidates(c)) == 1


async def test_low_confidence_counts_as_rejection(dictionary, engine):
    eng, _ = engine
    c = cands(dictionary, "Apple pie is the best, we love apple pie, with a tariff on it.")
    await eng.on_candidates(c)
    m = Mention(entity="Apple", tickers=["AAPL"], stance="neutral", action="other", confidence=0.1, quote="apple pie", summary="Fruit, not the company.")
    out = await eng.on_confirmation([m], c, t_llm=1001.0)
    assert [a.state for a in out] == [AlertState.RETRACTED]


async def test_confirmed_dedupe_by_ticker_and_action(dictionary, engine):
    eng, _ = engine
    c1 = cands(dictionary, "Big tariffs on Toyota.", start=10)
    await eng.on_candidates(c1)
    m = Mention(entity="Toyota", tickers=["TM"], stance="negative", action="tariff", confidence=0.9, quote="Big tariffs on Toyota", summary="s")
    first = await eng.on_confirmation([m], c1, t_llm=1001.0)
    assert len(first) == 1
    # Same ticker again inside the cooldown, even with a different action label: no new alert.
    m2 = m.model_copy(update={"action": "criticism"})
    second = await eng.on_confirmation([m2], c1, t_llm=1005.0)
    assert second == []
    assert first[0].count == 2
    # A positive<->negative reversal does re-alert.
    m3 = m.model_copy(update={"stance": "positive", "action": "praise"})
    third = await eng.on_confirmation([m3], c1, t_llm=1006.0)
    assert len(third) == 1


async def test_deferred_candidate_keeps_headsup(dictionary, engine):
    eng, _ = engine
    c = cands(dictionary, "And the pharmaceutical")
    heads = await eng.on_candidates(c)
    assert heads
    out = await eng.on_confirmation([], c, t_llm=1001.0, defer={c[0].entity.id})
    assert out == []
    assert heads[0].state == AlertState.HEADSUP


async def test_stray_non_candidate_mentions_are_ignored(dictionary, engine):
    eng, _ = engine
    c = cands(dictionary, "Big tariffs on Toyota.")
    await eng.on_candidates(c)
    stray = Mention(entity="pharmaceutical companies", tickers=[], stance="negative", action="regulation",
                    confidence=0.9, quote="q", summary="s")
    good = Mention(entity="Toyota", tickers=["TM"], stance="negative", action="tariff", confidence=0.9, quote="q", summary="s")
    out = await eng.on_confirmation([stray, good], c, t_llm=1001.0)
    assert [a.entity for a in out] == ["Toyota"]


async def test_sector_alert_does_not_mask_company_alert(dictionary, engine):
    eng, _ = engine
    c = cands(dictionary, "The crypto industry is booming and Coinbase is a great company, we made a deal.")
    await eng.on_candidates(c)
    sector = Mention(entity="crypto industry", tickers=["COIN", "IBIT"], stance="positive", action="praise", confidence=0.9, quote="q", summary="s")
    company = Mention(entity="Coinbase", tickers=["COIN"], stance="positive", action="deal", confidence=0.9, quote="q", summary="s")
    out = await eng.on_confirmation([sector, company], c, t_llm=1001.0)
    assert sorted(a.entity for a in out) == ["Coinbase", "crypto industry"]


async def test_reporter_mention_is_silent_until_figure_says_it(dictionary, engine):
    eng, sink = engine
    c = cands(dictionary, "Mister president, will you put tariffs on Toyota?")
    for cand in c:
        cand.speaker_role = "other"
    assert await eng.on_candidates(c) == []  # no heads-up for a reporter
    assert sink.alerts == []
    # The LLM rejects it: nothing was shown, so nothing is retracted.
    assert await eng.on_confirmation([], c, t_llm=1001.0) == []
    # Now the figure says it: a real heads-up fires despite the cooldown.
    c2 = cands(dictionary, "Big tariffs on Toyota, they have been very unfair.", start=20)
    for cand in c2:
        cand.speaker_role = "figure"
    out = await eng.on_candidates(c2)
    assert [a.state for a in out] == [AlertState.HEADSUP]
    assert out[0].speaker == "figure"


async def test_reporter_question_confirms_when_figure_answers(dictionary, engine):
    eng, sink = engine
    c = cands(dictionary, "Mister president, will you put tariffs on Toyota?")
    for cand in c:
        cand.speaker_role = "other"
    await eng.on_candidates(c)
    m = Mention(entity="Toyota", tickers=["TM"], stance="negative", action="tariff", speaker="figure",
                confidence=0.9, quote="Yes, 25 percent on Toyota", summary="The President says 25% tariff on Toyota.")
    out = await eng.on_confirmation([m], c, t_llm=1001.0)
    assert [a.state for a in out] == [AlertState.CONFIRMED]


async def test_mention_by_questioner_is_a_rejection(dictionary, engine):
    eng, _ = engine
    c = cands(dictionary, "What about tariffs on Toyota?")
    heads = await eng.on_candidates(c)
    assert heads
    m = Mention(entity="Toyota", tickers=["TM"], stance="neutral", action="tariff", speaker="questioner",
                confidence=0.95, quote="tariffs on Toyota", summary="A reporter asked about Toyota.")
    out = await eng.on_confirmation([m], c, t_llm=1001.0)
    assert [a.state for a in out] == [AlertState.RETRACTED]
