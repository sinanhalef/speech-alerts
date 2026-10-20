"""Command-line entry point: listen | replay | watch | serve | eval | make-golden | build-entities."""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from speechalerts.config import PROJECT_ROOT, settings

log = logging.getLogger("speechalerts")

if TYPE_CHECKING:
    from speechalerts.alerts.engine import AlertEngine
    from speechalerts.pipeline import Pipeline
    from speechalerts.sinks.broadcast import BroadcastSink
    from speechalerts.sinks.firebase import FirebaseSink
    from speechalerts.sinks.sqlite import SqliteSink


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)


@dataclass
class Sinks:
    """The long-lived sinks a run (or a whole daemon session) writes to."""

    all: list
    db: "SqliteSink"
    broadcast: "BroadcastSink"
    firebase: "FirebaseSink | None" = None

    def set_status(self, **fields: object) -> None:
        self.broadcast.set_status(**fields)
        if self.firebase is not None:
            self.firebase.set_status(**fields)

    async def close(self) -> None:
        for sink in self.all:
            try:
                await sink.close()
            except Exception as exc:  # noqa: BLE001
                log.error("closing sink %s failed: %s", type(sink).__name__, exc)


async def build_sinks(*, quiet: bool, show_interim: bool, firebase: bool | None = None) -> Sinks:
    from speechalerts.sinks.broadcast import BroadcastSink
    from speechalerts.sinks.sqlite import SqliteSink
    from speechalerts.sinks.terminal import TerminalSink

    broadcast = BroadcastSink()
    db = SqliteSink()
    sinks: list = [db, broadcast]
    if not quiet:
        sinks.insert(0, TerminalSink(show_interim=show_interim))
    fb = None
    if settings.firebase_enabled if firebase is None else firebase:
        from speechalerts.sinks.firebase import FirebaseSink

        fb = FirebaseSink()
        await fb.start()
        sinks.append(fb)
    return Sinks(all=sinks, db=db, broadcast=broadcast, firebase=fb)


async def run_pipeline(
    *,
    mode: str,
    target: str,
    title: str,
    source,
    transcriber,
    dictionary,
    sinks: Sinks,
    use_llm: bool,
    collect: list | None = None,
) -> tuple["Pipeline", "AlertEngine"]:
    """Run one stream/replay through the extractor into the given sinks. Does not close them."""
    from speechalerts.alerts.engine import AlertEngine
    from speechalerts.pipeline import Pipeline

    sinks.db.start_run(mode, target, title)
    sinks.set_status(state="listening", title=title, source=target, mode=mode)
    engine = AlertEngine(sinks.all, source=target)
    pipeline = Pipeline(
        source=source, transcriber=transcriber, dictionary=dictionary, engine=engine, sinks=sinks.all, use_llm=use_llm
    )
    log.info("%s: %s", mode, title)
    try:
        await pipeline.run()
    finally:
        sinks.db.end_run()
        log.info("run finished: %d segments, %d alerts", pipeline.segments, len(engine.alerts))
        if collect is not None:
            collect.extend(engine.alerts)
    return pipeline, engine


async def _build_and_run(
    *,
    mode: str,
    target: str,
    transcript: Path | None,
    speed: float | None,
    use_llm: bool,
    web: bool,
    quiet: bool,
    show_interim: bool,
    collect: list | None = None,
    start_seconds: float = 0.0,
    end_seconds: float | None = None,
) -> None:
    from speechalerts.extract.dictionary import Dictionary

    dictionary = Dictionary.load()
    sinks = await build_sinks(quiet=quiet, show_interim=show_interim)

    web_task = None
    if web:
        from speechalerts.web.app import create_app, serve

        web_task = asyncio.create_task(serve(create_app(sinks.broadcast, sinks.db)))

    try:
        if transcript is not None:
            from speechalerts.stt.text_replay import SilenceSource, TextReplayTranscriber

            source, title = SilenceSource(), transcript.name
            transcriber = TextReplayTranscriber(transcript, speed=speed)
        else:
            from speechalerts.sources.factory import open_source
            from speechalerts.stt.deepgram_stream import DeepgramTranscriber

            source, title = await open_source(target, speed=speed, start_seconds=start_seconds, end_seconds=end_seconds)
            if start_seconds or end_seconds is not None:
                title = f"{title} [{_fmt_clock(start_seconds)} - {_fmt_clock(end_seconds) if end_seconds else 'end'}]"
            transcriber = DeepgramTranscriber(keyterms=dictionary.keyterms())

        await run_pipeline(
            mode=mode, target=target, title=title, source=source, transcriber=transcriber,
            dictionary=dictionary, sinks=sinks, use_llm=use_llm, collect=collect,
        )
    finally:
        sinks.set_status(state="stopped")
        await sinks.close()
        if web_task and mode != "listen":
            await asyncio.sleep(0.2)
        if web_task:
            web_task.cancel()


async def cmd_listen(args: argparse.Namespace) -> None:
    await _build_and_run(
        mode="listen", target=args.url, transcript=None, speed=None, use_llm=not args.no_llm,
        web=not args.no_web, quiet=args.quiet, show_interim=args.interim,
    )


async def cmd_replay(args: argparse.Namespace) -> None:
    speed = None if args.speed == 0 else args.speed
    start = parse_clock(args.start) if args.start else 0.0
    end = parse_clock(args.end) if args.end else None
    if end is not None and end <= start:
        raise SystemExit("--to must be later than --from")
    await _build_and_run(
        mode="replay", target=args.target or str(args.transcript), transcript=args.transcript, speed=speed,
        use_llm=not args.no_llm, web=not args.no_web, quiet=args.quiet, show_interim=args.interim,
        start_seconds=start, end_seconds=end,
    )


async def cmd_watch(args: argparse.Namespace) -> None:
    from speechalerts.daemon import WatchDaemon

    daemon = WatchDaemon(
        channels=args.channel or settings.watch_channels,
        require_match=not args.any_title,
        use_llm=not args.no_llm,
        web=not args.no_web,
        quiet=args.quiet,
        show_interim=args.interim,
        once=args.once,
        ignore_hours=args.ignore_hours,
    )
    await daemon.run()


async def cmd_serve(args: argparse.Namespace) -> None:
    from speechalerts.sinks.broadcast import BroadcastSink
    from speechalerts.sinks.sqlite import SqliteSink
    from speechalerts.web.app import create_app, serve

    broadcast = BroadcastSink()
    db = SqliteSink()
    for rec in reversed(db.recent_alerts(100)):
        broadcast.recent_alerts.appendleft(rec)
    broadcast.set_status(state="history only", title="(no listener running)")
    await serve(create_app(broadcast, db), port=args.port)


async def cmd_eval(args: argparse.Namespace) -> None:
    from speechalerts.evaluate import load_golden, score, summarize
    from speechalerts.models import AlertState

    files = sorted(Path(args.golden_dir).glob("*.json"))
    if not files:
        log.error("no golden files in %s", args.golden_dir)
        return
    results = []
    for path in files:
        golden = load_golden(path)
        transcript = golden.get("transcript")
        source = golden.get("source")
        use_text = bool(transcript) and (args.text or not source)
        alerts: list = []
        await _build_and_run(
            mode="eval",
            target=source if (source and not use_text) else (transcript or path.stem),
            transcript=(PROJECT_ROOT / transcript) if use_text else None,
            # Audio must replay at 1x for latency numbers to mean anything (STT lags at higher speeds);
            # text replays can run as fast as the golden file or --speed asks.
            speed=None if args.speed == 0 else (args.speed or (golden.get("speed") or 8.0 if use_text else 1.0)),
            use_llm=not args.no_llm,
            web=False,
            quiet=args.quiet,
            show_interim=False,
            collect=alerts,
        )
        final_state = AlertState.HEADSUP if args.no_llm else AlertState.CONFIRMED
        results.append(
            score(
                golden["name"], golden.get("expected", []), alerts, final_state=final_state,
                not_expected=golden.get("not_expected", []),
            )
        )
    print(summarize(results))


def cmd_make_golden(args: argparse.Namespace) -> None:
    """Write a stored run's transcript as a replay file plus a JSON stub to fill in by hand."""
    import json

    from speechalerts.evaluate import golden_text_from_segments
    from speechalerts.sinks.sqlite import SqliteSink

    conn = SqliteSink().conn  # opens with schema migrations applied
    run = conn.execute("SELECT id, source, title FROM runs WHERE id=?", (args.run_id,)).fetchone()
    if run is None:
        raise SystemExit(f"no run {args.run_id} in {settings.db_path}")
    rows = conn.execute(
        "SELECT t_audio_start, text, speaker_label FROM segments WHERE run_id=? ORDER BY t_audio_start", (args.run_id,)
    ).fetchall()
    if not rows:
        raise SystemExit(f"run {args.run_id} has no stored segments")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(golden_text_from_segments(rows))
    stub = out.with_suffix(".json")
    if not stub.exists():
        stub.write_text(json.dumps({
            "name": out.stem,
            "transcript": str(out.relative_to(PROJECT_ROOT)) if out.is_relative_to(PROJECT_ROOT) else str(out),
            "source_url": run[1],
            "title": run[2],
            "speed": 20,
            "expected": [],
            "not_expected": [],
        }, indent=2) + "\n")
    log.info("wrote %s (%d segments) and %s", out, len(rows), stub)


def cmd_build_entities(args: argparse.Namespace) -> None:
    from scripts.build_ticker_list import build

    build(top_n=args.top, out=settings.sec_tickers_path)


def parse_clock(text: str) -> float:
    """'12' or '12.5' are minutes; '12:30' is mm:ss; '1:02:30' is h:mm:ss. Returns seconds."""
    text = text.strip()
    if ":" not in text:
        return float(text) * 60.0
    parts = [float(p) for p in text.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise argparse.ArgumentTypeError(f"cannot parse time {text!r}")


def _fmt_clock(seconds: float | None) -> str:
    if seconds is None:
        return "end"
    s = int(seconds)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="speechalerts", description="Real-time stock/industry mention alerts from live speeches")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--no-llm", action="store_true", help="dictionary heads-ups only, no Claude confirmation")
        sp.add_argument("--no-web", action="store_true", help="do not start the local web page")
        sp.add_argument("--quiet", action="store_true", help="no terminal output (web + sqlite only)")
        sp.add_argument("--interim", action="store_true", help="print interim transcript results too")

    sp = sub.add_parser("listen", help="transcribe a live stream or page URL and alert")
    sp.add_argument("url")
    common(sp)

    sp = sub.add_parser("replay", help="replay a recording, VOD URL, or saved transcript")
    sp.add_argument("target", nargs="?", help="local media file or URL")
    sp.add_argument("--transcript", type=Path, help="replay a text transcript instead of audio (no STT cost)")
    sp.add_argument("--speed", type=float, default=1.0, help="playback speed; 0 = as fast as possible")
    sp.add_argument("--from", dest="start", help="start position: minutes (12, 12.5) or clock (12:30, 1:02:30)")
    sp.add_argument("--to", dest="end", help="end position, same formats")
    common(sp)

    sp = sub.add_parser("watch", help="poll channels for a matching live stream, then listen")
    sp.add_argument("--channel", action="append", help="channel /live URL (repeatable); default from config")
    sp.add_argument("--any-title", action="store_true", help="attach to any live stream, ignore title patterns")
    sp.add_argument("--once", action="store_true", help="exit after the first stream ends")
    sp.add_argument("--ignore-hours", type=float, default=None,
                    help="hours to ignore a video id after it ended (default from config)")
    common(sp)

    sp = sub.add_parser("serve", help="serve the web page over the stored alert history only")
    sp.add_argument("--port", type=int, default=settings.web_port)

    sp = sub.add_parser("eval", help="run the golden set and report precision, recall and latency")
    sp.add_argument("--golden-dir", default=str(PROJECT_ROOT / "eval" / "golden"))
    sp.add_argument("--speed", type=float, default=None, help="override replay speed (0 = max)")
    sp.add_argument("--no-llm", action="store_true")
    sp.add_argument("--text", action="store_true", help="replay the golden transcript text instead of its audio (no STT cost)")
    sp.add_argument("--quiet", action="store_true", default=True)
    sp.add_argument("--show", dest="quiet", action="store_false", help="print alerts during eval")

    sp = sub.add_parser("make-golden", help="export a stored run's transcript as a golden replay file")
    sp.add_argument("run_id", type=int, help="row id in the runs table (see data/alerts.sqlite3)")
    sp.add_argument("--out", required=True, help="output .txt path, e.g. eval/golden/press_qa_2026_09_12.txt")

    sp = sub.add_parser("build-entities", help="download the SEC ticker list into data/entities/")
    sp.add_argument("--top", type=int, default=800)
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    _setup_logging(args.verbose)
    if args.cmd == "build-entities":
        cmd_build_entities(args)
        return
    if args.cmd == "make-golden":
        cmd_make_golden(args)
        return
    handler = {
        "listen": cmd_listen, "replay": cmd_replay, "watch": cmd_watch, "serve": cmd_serve, "eval": cmd_eval,
    }[args.cmd]

    async def runner() -> None:
        loop = asyncio.get_running_loop()
        task = asyncio.ensure_future(handler(args))
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, task.cancel)
        try:
            await task
        except asyncio.CancelledError:
            log.info("stopped")

    asyncio.run(runner())


if __name__ == "__main__":
    main()
