"""WatchDaemon state machine with scripted discovery and a fake attach."""

import pytest

from speechalerts.daemon import AttachResult, WatchDaemon
from speechalerts.sources.youtube import ResolvedStream


def stream(vid, title="LIVE: The President"):
    return ResolvedStream(page_url="https://www.youtube.com/@WhiteHouse/live", media_url="m", title=title,
                          is_live=True, video_id=vid, watch_url=f"https://www.youtube.com/watch?v={vid}",
                          live_status="is_live")


class FakeBroadcast:
    def __init__(self):
        self.statuses = []

    def set_status(self, **fields):
        self.statuses.append(fields)


class FakeFirebase:
    def __init__(self):
        self.calls = []

    def set_status(self, **fields):
        self.calls.append(("status", fields["state"]))

    def stream_started(self, vid, title, url):
        self.calls.append(("started", vid))

    def stream_ended(self, vid, reason, *, segments, alerts):
        self.calls.append(("ended", vid, reason, segments, alerts))

    def set_stream(self, vid, title):
        pass


class FakeSinks:
    def __init__(self, firebase=None):
        self.broadcast = FakeBroadcast()
        self.firebase = firebase
        self.closed = False
        self.all = []

    def set_status(self, **fields):
        self.broadcast.set_status(**fields)
        if self.firebase:
            self.firebase.set_status(**fields)

    async def close(self):
        self.closed = True


class Script:
    """Scripted probe/attach/resolve/sleep; the probe raises StopAsyncIteration-like exit when exhausted."""

    def __init__(self, probes, attaches, resolves=()):
        self.probes = list(probes)
        self.attaches = list(attaches)
        self.resolves = list(resolves)
        self.probe_ignores = []
        self.attached = []
        self.sleeps = []
        self.now = 0.0

    async def probe(self, channels, *, require_match, ignore_ids):
        self.probe_ignores.append(set(ignore_ids))
        if not self.probes:
            raise _Stop()
        res = self.probes.pop(0)
        if res is not None and res.video_id in ignore_ids:
            return None  # mirrors probe_channels: handled ids are filtered out
        return res

    async def attach(self, s):
        self.attached.append(s.video_id)
        return self.attaches.pop(0)

    async def resolve(self, url):
        r = self.resolves.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    async def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds

    def clock(self):
        return self.now


class _Stop(Exception):
    pass


def make(script, **kw):
    sinks = FakeSinks(firebase=kw.pop("firebase", None))
    d = WatchDaemon(channels=["c"], web=False, probe=script.probe, attach=script.attach, resolve=script.resolve,
                    sleep=script.sleep, clock=script.clock, sinks=sinks, poll_seconds=60, ignore_hours=6,
                    attach_retries=3, **kw)
    return d, sinks


async def run_until_script_ends(d):
    with pytest.raises(_Stop):
        await d.run()


async def test_same_video_attached_once_then_ignored():
    fb = FakeFirebase()
    sc = Script(probes=[None, stream("A"), stream("A"), None], attaches=[AttachResult("ended", "live_status=post_live", 40, 3)])
    d, sinks = make(sc, firebase=fb)
    await run_until_script_ends(d)
    assert sc.attached == ["A"]
    assert sc.probe_ignores[0] == set() and sc.probe_ignores[2] == {"A"}
    assert "A" in d.handled
    assert sc.sleeps == [60, 60, 60]  # idle poll, ignored repeat, idle poll: no second attach
    states = [s["state"] for s in sinks.broadcast.statuses]
    assert states[:6] == ["polling", "polling", "attaching", "ended", "polling", "polling"]
    assert ("started", "A") in fb.calls and ("ended", "A", "live_status=post_live", 40, 3) in fb.calls
    assert sinks.closed


async def test_crash_while_still_live_is_retried_with_backoff():
    sc = Script(
        probes=[stream("A")],
        attaches=[AttachResult("error", "ffmpeg died"), AttachResult("unknown", "no reason"), AttachResult("ended", "live_status=post_live")],
        resolves=[stream("A"), stream("A")],
    )
    d, sinks = make(sc, once=True)
    await d.run()
    assert sc.attached == ["A", "A", "A"]
    assert sc.sleeps == [10.0, 30.0]
    assert d.handled == {"A": 40.0}
    assert [s["state"] for s in sinks.broadcast.statuses].count("attaching") == 3


async def test_crash_when_no_longer_live_marks_done_without_retry():
    sc = Script(probes=[stream("A")], attaches=[AttachResult("error", "boom")], resolves=[RuntimeError("yt-dlp failed")])
    d, sinks = make(sc, once=True)
    await d.run()
    assert sc.attached == ["A"] and sc.sleeps == []
    assert "A" in d.handled
    assert sinks.broadcast.statuses[-2]["state"] == "ended"
    assert "not live on re-probe" in sinks.broadcast.statuses[-2]["reason"]


async def test_retries_exhausted_gives_up_and_ignores_id():
    sc = Script(
        probes=[stream("A")],
        attaches=[AttachResult("error", "x")] * 4,
        resolves=[stream("A")] * 4,
    )
    d, sinks = make(sc, once=True)
    await d.run()
    assert sc.attached == ["A"] * 4
    assert sc.sleeps == [10.0, 30.0, 60.0]
    assert "gave up after 4 attempts" in sinks.broadcast.statuses[-2]["reason"]
    assert "A" in d.handled


async def test_replaced_video_on_reprobe_is_not_retried():
    sc = Script(probes=[stream("A")], attaches=[AttachResult("error", "x")], resolves=[stream("B")])
    d, sinks = make(sc, once=True)
    await d.run()
    assert sc.attached == ["A"] and "A" in d.handled


async def test_ignore_expires():
    sc = Script(probes=[stream("A"), None, stream("A")], attaches=[AttachResult("ended", "e"), AttachResult("ended", "e")])
    d, sinks = make(sc)
    d.ignore_seconds = 50  # one idle poll (60 s) is enough for the ignore to lapse
    d.handled["A"] = -1000.0  # marked long ago: already expired at t=0
    await run_until_script_ends(d)
    assert sc.probe_ignores[0] == set()
    assert sc.probe_ignores[1] == {"A"} and sc.probe_ignores[2] == set()
    assert sc.attached == ["A", "A"]


async def test_once_exits_after_first_stream():
    sc = Script(probes=[None, stream("A"), stream("B")], attaches=[AttachResult("ended", "e")])
    d, sinks = make(sc, once=True)
    await d.run()
    assert sc.attached == ["A"] and d.streams_handled == 1
    assert sinks.broadcast.statuses[-1]["state"] == "stopped" and sinks.closed


async def test_sigterm_mid_stream_records_daemon_stopped():
    import asyncio

    fb = FakeFirebase()
    sc = Script(probes=[stream("A")], attaches=[])

    async def hanging_attach(s):
        await asyncio.sleep(3600)

    sinks = FakeSinks(firebase=fb)
    d = WatchDaemon(channels=["c"], web=False, probe=sc.probe, attach=hanging_attach, resolve=sc.resolve,
                    sleep=sc.sleep, clock=sc.clock, sinks=sinks, poll_seconds=60)
    task = asyncio.create_task(d.run())
    await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert ("ended", "A", "daemon stopped", 0, 0) in fb.calls
    assert sinks.broadcast.statuses[-1]["state"] == "stopped" and sinks.closed
