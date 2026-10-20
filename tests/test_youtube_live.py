from speechalerts.sources.youtube_live import _SQ


def test_sequence_template_round_trip():
    url = "https://rr1.googlevideo.com/videoplayback/id/x.1/itag/234/sq/283821/goap/lmt%3D36/dur/5.000/file/seg.ts"
    m = _SQ.search(url)
    assert m and int(m.group(1)) == 283821
    template = _SQ.sub("/sq/{sq}/", url, count=1)
    assert template.format(sq=283822).count("/sq/283822/") == 1


import asyncio

import pytest

from speechalerts.sources import youtube
from speechalerts.sources.base import StreamEnded
from speechalerts.sources.youtube import ResolvedStream
from speechalerts.sources.youtube_live import YoutubeLiveSource


def _stream(video_id="SE_aiQ4tBbc", status="is_live"):
    return ResolvedStream(
        page_url="https://www.youtube.com/@WhiteHouse/live", media_url="https://m3u8", title="t",
        is_live=status == "is_live", video_id=video_id, watch_url=f"https://www.youtube.com/watch?v={video_id}",
        live_status=status,
    )


async def test_source_pins_to_watch_url_from_resolved():
    src = YoutubeLiveSource("https://www.youtube.com/@WhiteHouse/live", resolved=_stream())
    assert src.video_id == "SE_aiQ4tBbc"
    assert src.page_url == "https://www.youtube.com/watch?v=SE_aiQ4tBbc"
    await src.close()


async def test_resync_raises_stream_ended_without_retrying(monkeypatch):
    calls = []

    async def fake_resolve(url):
        calls.append(url)
        return _stream(status="post_live")

    sleeps = []

    async def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(youtube, "resolve", fake_resolve)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    src = YoutubeLiveSource("https://www.youtube.com/watch?v=SE_aiQ4tBbc", resync_attempts=5)
    with pytest.raises(StreamEnded) as exc:
        await src._resync(100)
    assert exc.value.reason == "live_status=post_live"
    assert len(calls) == 1 and sleeps == []
    await src.close()


async def test_resync_rejects_a_different_video(monkeypatch):
    async def fake_resolve(url):
        return _stream(video_id="otherVideo1")

    monkeypatch.setattr(youtube, "resolve", fake_resolve)
    src = YoutubeLiveSource("https://www.youtube.com/@WhiteHouse/live", resolved=_stream())
    with pytest.raises(StreamEnded, match="replaced by video otherVideo1"):
        await src._resync()
    await src.close()


async def test_resync_retries_other_errors_then_gives_up(monkeypatch):
    async def failing_resolve(url):
        raise RuntimeError("yt-dlp failed")

    sleeps = []

    async def fake_sleep(s):
        sleeps.append(s)

    monkeypatch.setattr(youtube, "resolve", failing_resolve)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    src = YoutubeLiveSource("https://www.youtube.com/watch?v=SE_aiQ4tBbc", resync_attempts=3)
    with pytest.raises(RuntimeError, match="could not re-resolve"):
        await src._resync()
    assert sleeps == [5, 10]
    await src.close()


class _Stdin:
    def __init__(self):
        self.closed = False

    def write(self, b):
        pass

    async def drain(self):
        pass

    def close(self):
        self.closed = True


async def test_feed_records_outcome_instead_of_raising(monkeypatch):
    async def ended_resolve(url):
        return _stream(status="was_live")

    monkeypatch.setattr(youtube, "resolve", ended_resolve)
    src = YoutubeLiveSource("https://www.youtube.com/watch?v=SE_aiQ4tBbc")
    stdin = _Stdin()
    await src._feed(stdin)  # must not raise
    assert src.outcome == "ended" and src.end_reason == "live_status=was_live"
    assert stdin.closed
    await src.close()

    async def broken_resolve(url):
        raise ValueError("boom")

    monkeypatch.setattr(youtube, "resolve", broken_resolve)
    src = YoutubeLiveSource("https://www.youtube.com/watch?v=SE_aiQ4tBbc")
    await src._feed(_Stdin())
    assert src.outcome == "error" and isinstance(src.error, ValueError)
    await src.close()
