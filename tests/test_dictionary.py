from speechalerts.models import EntityKind


def names(cands):
    return sorted({c.entity.name for c in cands})


def test_company_hit(dictionary, make_seg):
    cands = dictionary.match(make_seg("We're going to take a 10 percent stake in Intel, a great company."))
    assert "Intel" in names(cands)
    intel = next(c for c in cands if c.entity.name == "Intel")
    assert "stake" in intel.triggers_nearby
    assert "percent" in intel.triggers_nearby
    assert intel.entity.tickers == ["INTC"]


def test_word_boundaries(dictionary, make_seg):
    # "amdocs" must not match "amd"; "format" must not match "ford".
    cands = dictionary.match(make_seg("Amdocs reported results and the format was good."))
    assert "AMD" not in names(cands)
    assert "Ford" not in names(cands)


def test_needs_context_blocks_common_words(dictionary, make_seg):
    cands = dictionary.match(make_seg("Our target is to win big in November."))
    assert "Target" not in names(cands)
    cands = dictionary.match(make_seg("Target and Walmart will eat the tariffs, they have plenty of margin."))
    assert "Target" in names(cands)
    assert "Walmart" in names(cands)


def test_country_requires_trigger(dictionary, make_seg):
    assert "China" not in names(dictionary.match(make_seg("I spoke with the president of China yesterday.")))
    cands = dictionary.match(make_seg("We are putting a 100 percent tariff on China starting Monday."))
    assert "China" in names(cands)


def test_longest_alias_wins(dictionary, make_seg):
    cands = dictionary.match(make_seg("Nippon Steel and US Steel made a tremendous deal."))
    assert "U.S. Steel" in names(cands)
    # generic "steel" sector should not duplicate because the longer alias consumed the span
    assert cands[0].entity.kind == EntityKind.COMPANY


def test_person_alias_maps_to_company(dictionary, make_seg):
    cands = dictionary.match(make_seg("I had a great meeting with Jensen Huang, he's doing an incredible job."))
    assert "Nvidia" in names(cands)
    # A bare first name is context-gated: only near a trigger word.
    assert "Nvidia" not in names(dictionary.match(make_seg("I had a great meeting with Jensen yesterday.")))
    assert "Nvidia" in names(dictionary.match(make_seg("Jensen is investing 500 billion in America.")))


def test_new_aliases_and_gating(dictionary, make_seg):
    assert "Northrop Grumman" in names(dictionary.match(make_seg("The B 2 bombers are unbelievable. We ordered 25 more.")))
    assert "Refiners" in names(dictionary.match(make_seg("It's brought to the refineries. It's being refined.")))
    assert "Venezuela" in names(dictionary.match(make_seg("We've taken out 100,000,000 barrels of oil. Great for Venezuela.")))
    assert "Oil" in names(dictionary.match(make_seg("We've taken out 100,000,000 barrels of oil.")))
    assert "Stock market" in names(dictionary.match(make_seg("The stock market hit another all-time high today.")))
    assert "Federal Reserve" in names(dictionary.match(make_seg("Too Late Powell should cut rates now.")))
    # Reporter self-introductions do not fire; a media attack with a trigger does.
    assert names(dictionary.match(make_seg("Mark Meredith, Fox News."))) == []
    assert "Fox Corporation" in names(dictionary.match(make_seg("Fox News ratings are terrible, they should lose their license.")))
    # STT-fragile aliases are gated.
    assert "Coal" not in names(dictionary.match(make_seg("Even the SS Coal where they were involved.")))
    assert "RTX (Raytheon)" not in names(dictionary.match(make_seg("The RTX artificial intelligence, we're way ahead.")))
    assert "RTX (Raytheon)" in names(dictionary.match(make_seg("We bought thousands of Patriot missiles."))) 


def test_timestamp_interpolation(dictionary, make_seg):
    seg = make_seg("Boeing is building the new plane. " * 3, start=100.0, end=112.0)
    cands = dictionary.match(seg)
    assert len(cands) == 1  # one candidate per entity per segment
    assert 100.0 <= cands[0].t_audio <= 112.0


def test_keyterms_are_company_names(dictionary):
    kt = dictionary.keyterms()
    assert "Nvidia" in kt and "Intel" in kt
    assert all(isinstance(k, str) for k in kt)


def test_trigger_in_prior_text_unlocks_context_entity(dictionary, make_seg):
    seg = make_seg("Not in India. I had a wonderful lunch.")
    assert "India" not in names(dictionary.match(seg))
    prior = "Tim Cook is investing six hundred billion dollars in America. Apple is going to build the plants here."
    cands = dictionary.match(seg, prior_text=prior)
    assert "India" in names(cands)
    india = next(c for c in cands if c.entity.name == "India")
    assert "plants" in india.triggers_nearby


def test_apostrophe_boundary(dictionary, make_seg):
    # Possessive still matches; a mis-heard name with an apostrophe inside does not.
    assert "Apple" in names(dictionary.match(make_seg("Apple's plants are coming to Texas.")))
    assert "Boeing" in names(dictionary.match(make_seg("Boeing' planes are great.")))
    assert "Dell" not in names(dictionary.match(make_seg("We have a woman, Dell'sy, who has been president.")))


def test_candidate_speaker_and_word_confidence(dictionary):
    from speechalerts.models import TranscriptSegment
    from speechalerts.transcript import SpeakerTracker, words_for_text

    text = "Mister president, what about Intel? Intel is a great company."
    words = words_for_text(text, 0, 6)
    for i, w in enumerate(words):
        w.speaker = 1 if i < 5 else 0
        w.confidence = 0.8 if i < 5 else 1.0
    seg = TranscriptSegment(text=text, t_audio_start=0, t_audio_end=6, t_wall=0, is_final=True, words=words)
    tracker = SpeakerTracker(min_words=1)
    tracker.add(TranscriptSegment(text="a b c", t_audio_start=0, t_audio_end=1, t_wall=0, is_final=True,
                                  words=[w for w in words_for_text("a b c", 0, 1, speaker=0)]))
    cands = dictionary.match(seg, speakers=tracker)
    intel = next(c for c in cands if c.entity.name == "Intel")
    # First occurrence of "Intel" is inside the reporter's question (speaker 1).
    assert intel.speaker == 1 and intel.speaker_role == "other"
    assert intel.word_confidence < 0.9
    # Without a tracker the role is unknown.
    assert dictionary.match(seg)[0].speaker_role == "unknown"
