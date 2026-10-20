from speechalerts.models import TranscriptSegment
from speechalerts.transcript import AudioClock, RollingWindow


def test_audio_clock_interpolates():
    clock = AudioClock()
    clock.observe(0.0, 1000.0)
    clock.observe(1.0, 1001.0)
    clock.observe(2.0, 1002.0)
    assert clock.wall_for(1.5) == 1001.5
    assert clock.wall_for(5.0) == 1005.0  # extrapolates past last point


def test_rolling_window_trims_and_keeps_interim():
    w = RollingWindow(seconds=10)
    for i in range(5):
        w.add(TranscriptSegment(text=f"s{i}", t_audio_start=i * 4.0, t_audio_end=i * 4.0 + 3, t_wall=0, is_final=True))
    assert w.text() == "s2 s3 s4"
    w.add(TranscriptSegment(text="partial", t_audio_start=20, t_audio_end=21, t_wall=0, is_final=False))
    assert w.text().endswith("partial")
    assert w.text(include_interim=False) == "s2 s3 s4"
    assert w.text(last_seconds=5) == "s4 partial"


def _seg(text, start, speakers, session=1, final=True):
    from speechalerts.transcript import words_for_text

    words = words_for_text(text, start, start + 3.0)
    for w, spk in zip(words, speakers):
        w.speaker = spk
    return TranscriptSegment(text=text, t_audio_start=start, t_audio_end=start + 3.0, t_wall=0, is_final=final,
                             words=words, session=session)


def test_speaker_tracker_dominant_and_roles():
    from speechalerts.transcript import SpeakerTracker

    tr = SpeakerTracker(window_seconds=300, min_words=6)
    assert tr.dominant() is None and tr.role_of(0) == "unknown"
    tr.add(_seg("a b c d", 0, [0, 0, 0, 0]))
    assert tr.dominant() is None  # below min_words
    tr.add(_seg("e f g", 4, [0, 0, 1]))
    assert tr.dominant() == 0
    assert tr.role_of(0) == "figure" and tr.role_of(1) == "other" and tr.role_of(None) == "unknown"
    assert tr.label(_seg("x y", 8, [1, 1])) == "Q"
    assert tr.label(_seg("x y", 8, [0, 0])) == "T"
    # Interims do not count.
    tr.add(_seg("q r s t u v w x y z", 9, [1] * 10, final=False))
    assert tr.dominant() == 0


def test_speaker_tracker_resets_on_new_session_and_trims_window():
    from speechalerts.transcript import SpeakerTracker

    tr = SpeakerTracker(window_seconds=10, min_words=3)
    tr.add(_seg("a b c d", 0, [0, 0, 0, 0], session=1))
    assert tr.dominant() == 0
    tr.add(_seg("a b c d", 20, [1, 1, 1, 1], session=1))  # first segment fell out of the window
    assert tr.dominant() == 1
    tr.add(_seg("a b", 21, [5, 5], session=2))  # new socket: labels restart, counts reset
    assert tr.dominant() is None


def test_text_with_speakers_labels_turns():
    from speechalerts.transcript import RollingWindow

    w = RollingWindow(seconds=60)
    w.add(_seg("We love Intel.", 0, [0, 0, 0]))
    w.add(_seg("Mister president, what about Nvidia? Nvidia is great.", 4, [1, 1, 1, 1, 1, 0, 0, 0]))
    out = w.text_with_speakers(dominant=0)
    assert out == "[main speaker] We love Intel. [speaker 2] Mister president, what about Nvidia? [main speaker] Nvidia is great."
    # Without labels the plain text is returned.
    w2 = RollingWindow(seconds=60)
    w2.add(TranscriptSegment(text="plain", t_audio_start=0, t_audio_end=1, t_wall=0, is_final=True))
    assert w2.text_with_speakers() == "plain"
