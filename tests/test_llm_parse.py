from speechalerts.extract.llm_confirm import parse_mentions


def test_parse_plain_json():
    text = '{"mentions": [{"entity": "Intel", "tickers": ["INTC"], "stance": "positive", "action": "investment", "confidence": 0.9, "quote": "a stake in Intel", "summary": "US takes stake in Intel."}]}'
    m = parse_mentions(text)
    assert len(m) == 1 and m[0].tickers == ["INTC"]


def test_parse_strips_fences_and_prose():
    text = 'Here you go:\n```json\n{"mentions": []}\n```'
    assert parse_mentions(text) == []


def test_parse_salvages_valid_entries():
    text = '{"mentions": [{"entity": "Intel", "tickers": ["INTC"], "stance": "positive", "action": "investment", "confidence": 0.9, "quote": "q", "summary": "s"}, {"entity": "Bad", "stance": "sideways"}]}'
    m = parse_mentions(text)
    assert [x.entity for x in m] == ["Intel"]


def test_parse_garbage():
    assert parse_mentions("no json here") == []


def test_parse_repairs_truncated_reply():
    text = '{"mentions": [{"entity": "Intel", "tickers": ["INTC"], "stance": "positive", "action": "investment", "confidence": 0.9, "quote": "q", "summary": "s"}, {"entity": "Toyota", "tickers": ["TM"], "stance": "pos'
    m = parse_mentions(text)
    assert [x.entity for x in m] == ["Intel"]


def test_mark_candidates_marks_only_the_detected_mention(dictionary, make_seg):
    from speechalerts.extract.llm_confirm import _mark_candidates
    seg = make_seg("Apple is going to build the plants here.")
    batch = dictionary.match(seg)
    context = "We had apple pie. It was tremendous. Apple is going to build the plants here."
    out = _mark_candidates(context, batch)
    assert out == "We had apple pie. It was tremendous. [[Apple]] is going to build the plants here."


def test_parse_speaker_defaults_to_figure_and_accepts_questioner():
    text = '{"mentions": [{"entity": "Intel", "tickers": ["INTC"], "stance": "positive", "action": "military", "confidence": 0.9, "quote": "q", "summary": "s"}, {"entity": "Toyota", "tickers": ["TM"], "stance": "neutral", "action": "tariff", "speaker": "questioner", "confidence": 0.9, "quote": "q", "summary": "s"}]}'
    m = parse_mentions(text)
    assert [x.speaker for x in m] == ["figure", "questioner"]
    assert m[0].action == "military"


def test_user_message_carries_speaker_hints(dictionary, make_seg):
    from speechalerts.extract.llm_confirm import Confirmer

    conf = Confirmer(lambda *a: None, client=object())  # type: ignore[arg-type]
    batch = dictionary.match(make_seg("Big tariffs on Toyota."))
    batch[0].speaker_role = "other"
    batch[0].word_confidence = 0.81
    msg = conf._user_message(batch, "[main speaker] Hello. [speaker 2] Big tariffs on Toyota.")
    assert "spoken by: another speaker; word confidence: 0.81" in msg
    assert "[[Toyota]]" in msg
