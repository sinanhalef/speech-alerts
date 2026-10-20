from speechalerts.sources.discovery import title_matches
from speechalerts.sources.youtube import pick_format


def _fmt(url, protocol, vcodec="none", acodec="mp4a", abr=0, **extra):
    return {"url": url, "protocol": protocol, "vcodec": vcodec, "acodec": acodec, "abr": abr, **extra}


def test_pick_format_vod_prefers_https_audio():
    info = {
        "is_live": False,
        "url": "top",
        "formats": [
            _fmt("hls-audio", "m3u8_native", abr=128),
            _fmt("https-low", "https", abr=48),
            _fmt("https-high", "https", abr=128),
            _fmt("video", "https", vcodec="avc1", abr=128),
        ],
    }
    assert pick_format(info) == "https-high"


def test_pick_format_live_prefers_hls_audio():
    info = {
        "is_live": True,
        "url": "top",
        "formats": [_fmt("https-audio", "https", abr=128), _fmt("hls-audio", "m3u8_native", abr=96)],
    }
    assert pick_format(info) == "hls-audio"


def test_pick_format_falls_back_to_top_level_url():
    assert pick_format({"is_live": True, "url": "top", "formats": []}) == "top"


def test_title_matching():
    pats = ["the president", "cabinet meeting"]
    assert title_matches("LIVE: The President Delivers Remarks", pats)
    assert not title_matches("Press Secretary Briefing", pats)


def test_pick_format_prefers_original_language_over_dubs():
    info = {
        "is_live": False,
        "url": "top",
        "formats": [
            _fmt("arabic-dub", "https", abr=129.5, language="ar", format_note="Arabic, medium", language_preference=-1),
            _fmt("german-dub", "https", abr=129.5, language="de-DE", format_note="German (DE), medium", language_preference=-1),
            _fmt("english-orig", "https", abr=129.4, language="en-US", format_note="English (US) original (default), medium", language_preference=10),
        ],
    }
    assert pick_format(info) == "english-orig"


def test_pick_format_live_keeps_unknown_acodec():
    info = {"is_live": True, "url": "top", "formats": [_fmt("hls-audio", "m3u8_native", acodec=None)]}
    assert pick_format(info) == "hls-audio"


def test_video_id_from_url():
    from speechalerts.sources.youtube import canonical_watch_url, video_id_from_url

    assert video_id_from_url("https://www.youtube.com/watch?v=SE_aiQ4tBbc") == "SE_aiQ4tBbc"
    assert video_id_from_url("https://www.youtube.com/watch?v=SE_aiQ4tBbc&t=10") == "SE_aiQ4tBbc"
    assert video_id_from_url("https://youtu.be/K3_mcCs8Z8I?si=x") == "K3_mcCs8Z8I"
    assert video_id_from_url("https://www.youtube.com/live/K3_mcCs8Z8I") == "K3_mcCs8Z8I"
    assert video_id_from_url("https://www.youtube.com/@WhiteHouse/live") is None
    assert canonical_watch_url("SE_aiQ4tBbc") == "https://www.youtube.com/watch?v=SE_aiQ4tBbc"


def test_stream_from_info_pins_video_and_status():
    from speechalerts.sources.youtube import stream_from_info

    info = {
        "id": "SE_aiQ4tBbc", "title": "LIVE: The President", "is_live": True, "live_status": "is_live",
        "extractor_key": "Youtube", "url": "top",
        "formats": [_fmt("hls-audio", "m3u8_native", abr=96)],
    }
    s = stream_from_info(info, "https://www.youtube.com/@WhiteHouse/live")
    assert s.video_id == "SE_aiQ4tBbc"
    assert s.watch_url == "https://www.youtube.com/watch?v=SE_aiQ4tBbc"
    assert s.live_status == "is_live" and s.is_live
    assert s.page_url.endswith("/live")  # original page kept for logs

    ended = stream_from_info({**info, "is_live": False, "live_status": "post_live"}, "x")
    assert ended.live_status == "post_live" and not ended.is_live


async def test_probe_live_skips_post_live_and_upcoming(monkeypatch):
    from speechalerts.sources import youtube

    async def fake_resolve(url):
        return youtube.ResolvedStream(url, "m", "t", is_live=False, video_id="a" * 11, live_status=status)

    monkeypatch.setattr(youtube, "resolve", fake_resolve)
    for status in ("post_live", "is_upcoming", "was_live"):
        assert await youtube.probe_live("https://www.youtube.com/@x/live") is None

    async def live_resolve(url):
        return youtube.ResolvedStream(url, "m", "t", is_live=True, video_id="a" * 11, live_status="is_live")

    monkeypatch.setattr(youtube, "resolve", live_resolve)
    assert (await youtube.probe_live("https://www.youtube.com/@x/live")).video_id == "a" * 11
