"""FirebaseSink against fake Firestore/messaging objects: document shape, parent updates, pushes."""

import asyncio
import logging

from speechalerts.models import Alert, AlertState, TranscriptSegment
from speechalerts.sinks.firebase import FirebaseSink


class FakeDoc:
    def __init__(self, store, path):
        self.store, self.path = store, path

    def set(self, data, merge=False):
        if merge and self.path in self.store:
            self.store[self.path] = {**self.store[self.path], **data}
        else:
            self.store[self.path] = dict(data)

    def collection(self, name):
        return FakeCollection(self.store, f"{self.path}/{name}")


class FakeCollection:
    def __init__(self, store, name):
        self.store, self.name = store, name

    def document(self, doc_id):
        return FakeDoc(self.store, f"{self.name}/{doc_id}")


class FakeDb:
    def __init__(self):
        self.store: dict[str, dict] = {}

    def collection(self, name):
        return FakeCollection(self.store, name)


class FakeMessaging:
    def __init__(self):
        self.sent: list[tuple[dict, bool]] = []

    class Message:
        def __init__(self, topic, notification, data):
            self.topic, self.notification, self.data = topic, notification, data

    class Notification:
        def __init__(self, title, body):
            self.title, self.body = title, body

    def send(self, message, dry_run=False):
        self.sent.append(({"topic": message.topic, "title": message.notification.title,
                           "body": message.notification.body, "data": message.data}, dry_run))
        return "projects/x/messages/1"


def make_sink(**kw):
    db, msg = FakeDb(), FakeMessaging()
    opts = {"topic": "alerts", "dry_run": True, "figure": "the president", "server_timestamp": lambda: "TS", **kw}
    sink = FirebaseSink(db=db, messaging=msg, **opts)
    return sink, db, msg


def alert(state, **kw):
    base = dict(figure="the president", state=state, entity="Intel", tickers=["INTC"], quote="a stake in Intel",
                t_audio=10.0, t_spoken=1000.0, t_stt=1000.5, t_alert=1001.0, source="test")
    return Alert(**{**base, **kw})


async def test_headsup_doc_and_dry_run_push():
    sink, db, msg = make_sink()
    sink.set_stream("vid123", "LIVE: The President")
    await sink.start()
    a = alert(AlertState.HEADSUP)
    await sink.alert(a)
    await sink.close()
    doc = db.store[f"alerts/{a.id}"]
    assert set(a.to_dict()) <= set(doc)
    assert doc["stream_id"] == "vid123" and doc["stream_title"].startswith("LIVE") and doc["created_at"] == "TS"
    assert len(msg.sent) == 1
    sent, dry = msg.sent[0]
    assert dry is True and sent["topic"] == "alerts"
    assert sent["title"] == "The President mentioned Intel (INTC)" and sent["body"] == "a stake in Intel"
    assert sent["data"]["state"] == "headsup" and sent["data"]["tickers"] == "INTC"
    assert all(isinstance(v, str) for v in sent["data"].values())


async def test_confirmed_updates_parent_and_pushes():
    sink, db, msg = make_sink()
    await sink.start()
    h = alert(AlertState.HEADSUP)
    c = alert(AlertState.CONFIRMED, parent_id=h.id, stance="positive", action="investment",
              summary="The President says the US takes a stake in Intel.", confidence=0.95)
    await sink.alert(h)
    await sink.alert(c)
    await sink.close()
    parent = db.store[f"alerts/{h.id}"]
    assert parent["state"] == "confirmed" and parent["resolved_by"] == c.id and parent["resolved_at"] == "TS"
    assert parent["quote"] == "a stake in Intel"  # merge kept the original fields
    assert db.store[f"alerts/{c.id}"]["state"] == "confirmed"
    assert [s["data"]["state"] for s, _ in msg.sent] == ["headsup", "confirmed"]
    assert msg.sent[1][0]["title"] == "The President on Intel: positive · investment"
    assert msg.sent[1][0]["body"].startswith("The President says")


async def test_retraction_updates_parent_without_push():
    sink, db, msg = make_sink()
    await sink.start()
    h = alert(AlertState.HEADSUP)
    r = alert(AlertState.RETRACTED, parent_id=h.id, summary="Not a market-relevant mention of Intel")
    await sink.alert(h)
    await sink.alert(r)
    await sink.close()
    assert db.store[f"alerts/{h.id}"]["state"] == "retracted"
    assert f"alerts/{r.id}" in db.store
    assert [s["data"]["state"] for s, _ in msg.sent] == ["headsup"]


async def test_live_push_flag_passthrough():
    sink, db, msg = make_sink(dry_run=False)
    await sink.start()
    await sink.alert(alert(AlertState.CONFIRMED))
    await sink.close()
    assert msg.sent[0][1] is False


async def test_write_failure_is_logged_not_raised(caplog):
    sink, db, msg = make_sink()

    def boom(*a, **k):
        raise RuntimeError("firestore down")

    db.collection = boom
    await sink.start()
    with caplog.at_level(logging.ERROR):
        await sink.alert(alert(AlertState.HEADSUP))
        await sink.close()
    assert sink.failed == 1 and "firestore down" in caplog.text


async def test_status_and_stream_docs():
    sink, db, msg = make_sink()
    await sink.start()
    sink.set_status(state="polling", channels=["a"])
    sink.stream_started("vid1", "The President speaks", "https://www.youtube.com/watch?v=vid1")
    sink.set_status(state="listening", video_id="vid1")
    sink.stream_ended("vid1", "live_status=post_live", segments=12, alerts=3)
    await sink.close()
    assert db.store["status/current"] == {"state": "listening", "channels": ["a"], "video_id": "vid1", "updated_at": "TS"}
    s = db.store["streams/vid1"]
    assert s["state"] == "ended" and s["started_at"] == "TS" and s["end_reason"] == "live_status=post_live"
    assert s["segments"] == 12 and s["alerts"] == 3 and s["title"] == "The President speaks"
    assert sink.stream_id == "vid1"
    assert msg.sent[0][0]["title"] == "The President is live" and msg.sent[0][0]["data"]["kind"] == "stream"


async def test_alert_before_start_still_writes():
    sink, db, msg = make_sink()
    a = alert(AlertState.HEADSUP)
    await sink.alert(a)  # no explicit start(): worker is created lazily on the running loop
    await asyncio.sleep(0)
    await sink.close()
    assert f"alerts/{a.id}" in db.store


async def test_headsup_snapshot_survives_later_mutation():
    """The engine flips a heads-up's state in place on confirmation; the doc must keep 'headsup'."""
    sink, db, msg = make_sink()
    await sink.start()
    h = alert(AlertState.HEADSUP)
    await sink.alert(h)
    h.state = AlertState.CONFIRMED  # what AlertEngine.on_confirmation does to the parent object
    await sink.close()
    assert db.store[f"alerts/{h.id}"]["state"] == "headsup"
    assert msg.sent[0][0]["title"].startswith("The President mentioned")


def segment(text="hello", final=True, t_wall=1700000000.5):
    return TranscriptSegment(text=text, t_audio_start=1.0, t_audio_end=2.5, t_wall=t_wall,
                             is_final=final, confidence=0.9, speaker_label="T")


async def test_final_segments_written_under_stream():
    sink, db, _ = make_sink(transcripts=True)
    sink.set_stream("vid1", "The President speaks")
    await sink.segment(segment())
    await sink.segment(segment("interim", final=False))
    await sink.segment(segment("   ", t_wall=1700000001.0))
    await sink.close()
    assert list(db.store) == ["streams/vid1/segments/0001700000000500"]
    d = db.store["streams/vid1/segments/0001700000000500"]
    assert d["text"] == "hello" and d["speaker_label"] == "T" and d["t_audio_start"] == 1.0


async def test_segments_skipped_without_stream_or_when_disabled():
    sink, db, _ = make_sink(transcripts=True)
    await sink.segment(segment())  # no stream id (bare listen / replay)
    await sink.close()
    assert db.store == {}
    sink, db, _ = make_sink(transcripts=False)
    sink.set_stream("vid1")
    await sink.segment(segment())
    await sink.close()
    assert db.store == {}
