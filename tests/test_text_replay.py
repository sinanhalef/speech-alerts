import asyncio
from pathlib import Path

from speechalerts.stt.text_replay import SilenceSource, TextReplayTranscriber, parse_transcript


def test_parse_transcript_formats():
    text = "# comment\n0.0\tHello there.\n\nplain line without stamp\n30\tLater."
    items = parse_transcript(text)
    assert [round(i[0], 1) for i in items] == [0.0, 1.1, 30.0]
    assert items[1][2] == "plain line without stamp"


async def test_replay_yields_interim_and_final(tmp_path: Path):
    p = tmp_path / "t.txt"
    p.write_text("0\tWe love Intel.\n5\tBig tariffs on Toyota.")
    t = TextReplayTranscriber(p, speed=None)
    segs = [s async for s in t.transcribe(SilenceSource().chunks())]
    assert [s.is_final for s in segs] == [True, True]
    t2 = TextReplayTranscriber(p, speed=1000.0)
    segs2 = [s async for s in t2.transcribe(SilenceSource().chunks())]
    assert [s.is_final for s in segs2] == [False, True, False, True]


def test_parse_transcript_speaker_column():
    items = parse_transcript("0\t1\tMister president?\n3\tYes.\n6\t0\tWe love Intel.")
    assert [i[3] for i in items] == [1, None, 0]
    assert items[0][2] == "Mister president?"


async def test_replay_words_carry_speaker(tmp_path: Path):
    p = tmp_path / "t.txt"
    p.write_text("0\t1\tMister president, what about Intel?\n5\t0\tIntel is great.")
    t = TextReplayTranscriber(p, speed=None)
    segs = [s async for s in t.transcribe(SilenceSource().chunks())]
    assert {w.speaker for w in segs[0].words} == {1}
    assert {w.speaker for w in segs[1].words} == {0}
    assert len(segs[0].words) == len(segs[0].text.split())
