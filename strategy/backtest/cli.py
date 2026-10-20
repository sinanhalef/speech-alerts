"""backtest CLI: discover | fetch | transcribe | extract | judge | measure | report | run-all."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from backtest.models import SignalFile, VideoMeta, VideoSpec
from backtest.videos import DATA, load_videos

log = logging.getLogger("backtest")

AUDIO = DATA / "audio"
RAW = DATA / "raw"
TRANSCRIPTS = DATA / "transcripts"
SIGNALS = DATA / "signals"
PRICES = DATA / "prices"
RESULTS = DATA / "results"


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s", datefmt="%H:%M:%S", stream=sys.stderr)
    for name in ("httpx", "httpx2", "websockets", "anthropic", "yfinance", "peewee", "urllib3"):
        logging.getLogger(name).setLevel(logging.WARNING)


def _meta_path(vid: str) -> Path:
    return TRANSCRIPTS / f"{vid}.meta.json"


def _load_meta(vid: str) -> VideoMeta:
    return VideoMeta.model_validate_json(_meta_path(vid).read_text())


def _specs(args) -> list[VideoSpec]:
    return load_videos(only=args.video or None, include_skipped=bool(args.video))


# ---------- stages ----------

async def stage_discover(args) -> None:
    from backtest.discover import discover

    rows = await discover(days=args.days, searches=args.search or None, all_titles=args.all_titles, limit=args.limit)
    out = DATA / "candidates.json"
    out.write_text(json.dumps(rows, indent=1))
    for r in rows:
        print(f"{r['id']}  {r['start_et'] or '?':25}  {r['duration_min']:6.0f} min  live={r['was_live']!s:5}  {r['title'][:80]}")
    print(f"\n{len(rows)} candidates -> {out}")


async def stage_fetch(args, spec: VideoSpec) -> VideoMeta:
    from backtest.fetch import fetch_audio, fetch_meta

    meta_path, audio_path = _meta_path(spec.id), AUDIO / f"{spec.id}.ogg"
    if meta_path.exists() and audio_path.exists() and not args.force:
        meta = _load_meta(spec.id)
        # keep label/group/notes in sync with videos.yaml
        meta.label, meta.group, meta.notes = spec.label, spec.group, spec.notes
        meta_path.write_text(meta.model_dump_json(indent=1))
        return meta
    meta, info = await fetch_meta(spec)
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / f"{spec.id}.info.json").write_text(json.dumps(info, default=str))
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(meta.model_dump_json(indent=1))
    log.info("%s: %r (%s) start=%s dur=%.0f min", spec.id, meta.title[:60], meta.channel,
             meta.t0_et().strftime("%Y-%m-%d %H:%M ET") if meta.t0_et() else "unknown", (meta.duration or 0) / 60)
    if not audio_path.exists() or args.force:
        log.info("%s: downloading audio", spec.id)
        await fetch_audio(info, audio_path)
        log.info("%s: audio %.1f MB", spec.id, audio_path.stat().st_size / 1e6)
    return meta


async def stage_transcribe(args, spec: VideoSpec) -> Path:
    from speechalerts.extract.dictionary import Dictionary

    from backtest.transcribe import to_transcript, transcribe_file, write_transcript

    js = TRANSCRIPTS / f"{spec.id}.json"
    if js.exists() and not args.force:
        return js
    meta = _load_meta(spec.id)
    raw_path = RAW / f"{spec.id}.deepgram.json"
    if raw_path.exists() and not args.force:
        raw = json.loads(raw_path.read_text())
    else:
        raw = await transcribe_file(AUDIO / f"{spec.id}.ogg", keyterms=Dictionary.load().keyterms())
        raw_path.write_text(json.dumps(raw))
    t = to_transcript(raw, meta)
    txt, js = write_transcript(t, TRANSCRIPTS)
    log.info("%s: %d utterances, main speaker %s (%.0f%% of speech) -> %s", spec.id, len(t.utterances), t.main_speaker,
             100 * t.speaker_seconds.get(str(t.main_speaker), 0) / max(sum(t.speaker_seconds.values()), 1), txt.name)
    return js


async def stage_extract(args, spec: VideoSpec) -> Path:
    from speechalerts.extract.dictionary import Dictionary
    from speechalerts.extract.llm_confirm import Confirmer

    from backtest.extract import OfflineExtractor
    from backtest.transcribe import read_transcript

    out = SIGNALS / f"{spec.id}.json"
    if out.exists() and not args.force:
        return out
    t = read_transcript(TRANSCRIPTS / f"{spec.id}.json")
    confirmer = None if args.no_llm else Confirmer(_noop)
    ex = OfflineExtractor(Dictionary.load(), confirmer)
    sf = await ex.run(t)
    SIGNALS.mkdir(parents=True, exist_ok=True)
    out.write_text(sf.model_dump_json(indent=1))
    log.info("%s: %s", spec.id, sf.counts)
    return out


async def _noop(*_args, **_kwargs) -> None:
    return None


async def stage_judge(args, spec: VideoSpec) -> Path:
    from backtest.judge import Judge
    from backtest.transcribe import read_transcript

    path = SIGNALS / f"{spec.id}.json"
    sf = SignalFile.model_validate_json(path.read_text())
    todo = [s for s in sf.signals if s.state == "confirmed" and (s.judge is None or not s.judge.tickers or args.force)]
    if not todo:
        return path
    t = read_transcript(TRANSCRIPTS / f"{spec.id}.json")
    judge = Judge(model=args.judge_model)
    sem = asyncio.Semaphore(4)

    async def one(s):
        async with sem:
            try:
                s.judge = await judge.judge(s, t)
            except Exception as exc:  # noqa: BLE001
                log.error("judge failed for %s: %s", s.signal_id, exc)

    await asyncio.gather(*(one(s) for s in todo))
    path.write_text(sf.model_dump_json(indent=1))
    log.info("%s: judged %d signals", spec.id, len(todo))
    return path


def _signal_files(specs: list[VideoSpec]) -> list[SignalFile]:
    out = []
    for spec in specs:
        p = SIGNALS / f"{spec.id}.json"
        if p.exists():
            out.append(SignalFile.model_validate_json(p.read_text()))
        else:
            log.warning("%s: no signals file yet", spec.id)
    return out


def stage_measure(args, specs: list[VideoSpec]) -> Path:
    from backtest.measure import measure_files
    from backtest.prices import PriceStore

    files = _signal_files(specs)
    store = PriceStore(PRICES)
    df = measure_files(files, store, include_retracted=args.include_retracted)
    RESULTS.mkdir(parents=True, exist_ok=True)
    csv = RESULTS / "measurements.csv"
    df.to_csv(csv, index=False)
    df.to_json(RESULTS / "measurements.json", orient="records", indent=1)
    log.info("measured %d rows (%d with abnormal returns) -> %s", len(df), int(df["abn_ret"].notna().sum()), csv)
    return csv


def stage_report(args, specs: list[VideoSpec]) -> Path:
    import pandas as pd

    from backtest.report import build_summary

    files = _signal_files(specs)
    df = pd.read_csv(RESULTS / "measurements.csv")
    md, js = build_summary(df, files)
    (RESULTS / "summary.md").write_text(md)
    (RESULTS / "summary.json").write_text(json.dumps(js, indent=1))
    print(md.split("## Judge")[0])
    log.info("report -> %s", RESULTS / "summary.md")
    return RESULTS / "summary.md"


def stage_analyze(args, specs: list[VideoSpec]) -> Path:
    import pandas as pd

    from backtest.analyze import build_analysis

    files = _signal_files(specs)
    df = pd.read_csv(RESULTS / "measurements.csv")
    md, js = build_analysis(df, files)
    (RESULTS / "analysis.md").write_text(md)
    (RESULTS / "analysis.json").write_text(json.dumps(js, indent=1))
    log.info("analysis -> %s", RESULTS / "analysis.md")
    return RESULTS / "analysis.md"


def stage_portfolio(args, specs: list[VideoSpec]) -> Path:
    from backtest.portfolio import build_portfolio_report
    from backtest.prices import PriceStore

    files = _signal_files(specs)
    md, js = build_portfolio_report(files, PriceStore(PRICES))
    (RESULTS / "portfolio.md").write_text(md)
    (RESULTS / "portfolio.json").write_text(json.dumps(js, indent=1, default=str))
    print(md.split("\n## ")[0])
    log.info("portfolio -> %s", RESULTS / "portfolio.md")
    return RESULTS / "portfolio.md"


async def _per_video(args, specs: list[VideoSpec], stages: list[str]) -> None:
    sem = asyncio.Semaphore(args.concurrency)

    async def one(spec: VideoSpec) -> None:
        async with sem:
            try:
                if "fetch" in stages:
                    await stage_fetch(args, spec)
                if "transcribe" in stages:
                    await stage_transcribe(args, spec)
                if "extract" in stages:
                    await stage_extract(args, spec)
                if "judge" in stages:
                    await stage_judge(args, spec)
            except Exception as exc:  # noqa: BLE001
                log.error("%s failed: %s", spec.id, exc, exc_info=args.verbose)

    await asyncio.gather(*(one(s) for s in specs))


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="backtest", description="Offline backtest of speechalerts signals against prices")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--video", action="append", help="video id (repeatable); default: all in videos.yaml")
        sp.add_argument("--force", action="store_true", help="redo the stage even if outputs exist")
        sp.add_argument("--concurrency", type=int, default=2)
        sp.add_argument("--no-llm", action="store_true", help="extract: dictionary heads-ups only")
        sp.add_argument("--judge-model", default="claude-sonnet-5")
        sp.add_argument("--include-retracted", action="store_true", help="measure retracted heads-ups too")

    sp = sub.add_parser("discover", help="list recent White House livestreams as candidates")
    sp.add_argument("--days", type=int, default=75)
    sp.add_argument("--limit", type=int, default=60)
    sp.add_argument("--search", action="append", help="extra YouTube search query (repeatable)")
    sp.add_argument("--all-titles", action="store_true")
    for name in ("fetch", "transcribe", "extract", "judge", "measure", "report", "analyze", "portfolio", "run-all"):
        common(sub.add_parser(name))

    args = p.parse_args(argv)
    _setup_logging(args.verbose)
    if args.cmd == "discover":
        asyncio.run(stage_discover(args))
        return
    specs = _specs(args)
    if args.cmd in ("fetch", "transcribe", "extract", "judge"):
        asyncio.run(_per_video(args, specs, [args.cmd]))
    elif args.cmd == "measure":
        stage_measure(args, specs)
    elif args.cmd == "report":
        stage_report(args, specs)
    elif args.cmd == "analyze":
        stage_analyze(args, specs)
    elif args.cmd == "portfolio":
        stage_portfolio(args, specs)
    elif args.cmd == "run-all":
        asyncio.run(_per_video(args, specs, ["fetch", "transcribe", "extract", "judge"]))
        stage_measure(args, specs)
        stage_report(args, specs)
        stage_analyze(args, specs)
        stage_portfolio(args, specs)


if __name__ == "__main__":
    main()
