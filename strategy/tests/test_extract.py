import pytest
from speechalerts.extract.dictionary import Dictionary
from speechalerts.models import Entity, EntityKind, Mention
from speechalerts.stt.text_replay import parse_transcript

from backtest.extract import OfflineExtractor
from backtest.models import Transcript, Utterance, VideoMeta
from backtest.transcribe import write_transcript


class FakeConfirmer:
    def __init__(self, verdicts):
        self.verdicts = verdicts  # entity name -> Mention or None
        self.calls = []

    async def confirm(self, batch, context):
        self.calls.append((sorted(c.entity.name for c in batch), context))
        out = []
        for c in batch:
            m = self.verdicts.get(c.entity.name)
            if m:
                out.append(m)
        return out


def _dict():
    ents = [
        Entity(id="intc", name="Intel", kind=EntityKind.COMPANY, tickers=["INTC"], aliases=["intel"]),
        Entity(id="aapl", name="Apple", kind=EntityKind.COMPANY, tickers=["AAPL"], aliases=["apple"]),
        Entity(id="oil", name="Oil", kind=EntityKind.SECTOR, tickers=["XLE"], aliases=["oil"], needs_context=True),
    ]
    return Dictionary(ents, ["tariff", "invest", "billion"])


def _transcript(utts, t0=1_000_000.0):
    meta = VideoMeta(id="vid", url="u", title="t", t0=t0, t0_source="release_timestamp", duration=100)
    return Transcript(video=meta, main_speaker=0, utterances=[Utterance(start=s, end=e, text=x, speaker=spk) for s, e, x, spk in utts])


@pytest.mark.asyncio
async def test_confirm_retract_and_cooldown():
    fc = FakeConfirmer({"Intel": Mention(entity="Intel", tickers=["INTC"], stance="positive", action="investment", confidence=0.9,
                                         quote="Intel is investing", summary="Intel invests")})
    ex = OfflineExtractor(_dict(), fc, cooldown_seconds=600, context_seconds=30)
    t = _transcript([
        (0, 4, "Intel is going to invest 100 billion dollars.", 0),
        (5, 8, "I had an apple pie for lunch.", 1),
        (300, 304, "And Intel again, great company.", 0),
        (700, 704, "Intel one more time.", 0),
    ])
    sf = await ex.run(t)
    states = [(s.entity, s.state, s.count, s.t_audio) for s in sf.signals]
    assert states[0][:2] == ("Intel", "confirmed")
    assert states[1][:2] == ("Apple", "retracted")
    assert sf.signals[0].count == 2  # the 300 s repeat folded in (within 600 s cooldown)
    assert states[2][:2] == ("Intel", "confirmed") and states[2][3] >= 700
    assert sf.counts == {"headsups": 3, "confirmed": 2, "retracted": 1, "unconfirmed": 0, "llm_calls": 4}
    s0 = sf.signals[0]
    assert s0.llm.tickers == ["INTC"] and s0.speaker_is_main is True and s0.t_wall == pytest.approx(1_000_000 + s0.t_audio)
    assert sf.signals[1].speaker_is_main is False
    assert sf.signals[1].llm_attempts == 2  # apple pie: deferred once, then retracted


@pytest.mark.asyncio
async def test_deferred_recheck_extends_context():
    class Late(FakeConfirmer):
        async def confirm(self, batch, context):
            self.calls.append((sorted(c.entity.name for c in batch), context))
            if "next sentence" in context:
                return [Mention(entity="Apple", tickers=["AAPL"], stance="positive", action="deal", confidence=0.8, quote="", summary="")]
            return []

    fc = Late({})
    ex = OfflineExtractor(_dict(), fc, context_seconds=30, fresh_seconds=4.0, recheck_seconds=3.0)
    t = _transcript([(0, 3, "We spoke with Apple", 0), (4, 7, "and the next sentence says they will build here.", 0), (20, 22, "Unrelated.", 0)])
    sf = await ex.run(t)
    assert len(fc.calls) == 2
    assert "next sentence" not in fc.calls[0][1] and "next sentence" in fc.calls[1][1]
    assert sf.signals[0].state == "confirmed" and sf.signals[0].llm_attempts == 2


@pytest.mark.asyncio
async def test_context_gating_and_no_llm():
    ex = OfflineExtractor(_dict(), None)
    t = _transcript([(0, 3, "I like oil paintings.", 0), (10, 13, "We will drill for oil and invest billions.", 0)])
    sf = await ex.run(t)
    assert [s.entity for s in sf.signals] == ["Oil"] and sf.signals[0].t_audio >= 10
    assert sf.signals[0].state == "headsup"


def test_transcript_txt_roundtrip(tmp_path):
    t = _transcript([(1.5, 3, "Hello there.", 0), (4, 6, "Second line.", 0)])
    txt, js = write_transcript(t, tmp_path)
    parsed = parse_transcript(txt.read_text())
    assert [p[0] for p in parsed] == [1.5, 4.0]
    assert [p[2] for p in parsed] == ["Hello there.", "Second line."]
    assert Transcript.model_validate_json(js.read_text()).utterances[1].text == "Second line."
