"""Deepgram pre-recorded transcription (nova-3, diarized, utterances) -> transcript files.

Writes two files per video into data/transcripts/:
  <id>.txt   one utterance per line as "<start seconds>\t<text>", replayable by the live
             pipeline (`speechalerts replay --transcript <file>`), '#' lines are comments
  <id>.json  Transcript model: utterances with speaker labels, confidence and words + video meta
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path

from deepgram import AsyncDeepgramClient
from speechalerts.config import settings

from backtest.models import Transcript, Utterance, VideoMeta, Word

log = logging.getLogger(__name__)


async def transcribe_file(audio_path: Path, *, keyterms: list[str], model: str = "nova-3") -> dict:
    if not settings.deepgram_api_key:
        raise RuntimeError("DEEPGRAM_API_KEY is not set in the root .env")
    client = AsyncDeepgramClient(api_key=settings.deepgram_api_key)
    data = audio_path.read_bytes()
    log.info("deepgram: uploading %s (%.1f MB)", audio_path.name, len(data) / 1e6)
    response = await client.listen.v1.media.transcribe_file(
        request=data,
        model=model,
        smart_format=True,
        punctuate=True,
        numerals=True,
        diarize=True,
        utterances=True,
        keyterm=keyterms[:100] if model.startswith("nova-3") else None,
        request_options={"timeout": 900},
    )
    raw = response.model_dump(mode="json") if hasattr(response, "model_dump") else json.loads(json.dumps(response, default=str))
    return raw


def to_transcript(raw: dict, meta: VideoMeta, *, model: str = "nova-3") -> Transcript:
    results = raw.get("results") or {}
    utts_raw = results.get("utterances") or []
    utterances: list[Utterance] = []
    speaker_seconds: dict[str, float] = defaultdict(float)
    if utts_raw:
        for u in utts_raw:
            text = (u.get("transcript") or "").strip()
            if not text:
                continue
            words = [
                Word(w=w.get("punctuated_word") or w.get("word", ""), s=float(w.get("start", 0)), e=float(w.get("end", 0)),
                     c=float(w.get("confidence", 0)), spk=w.get("speaker"))
                for w in (u.get("words") or [])
            ]
            utt = Utterance(start=float(u["start"]), end=float(u["end"]), text=text, speaker=u.get("speaker"),
                            confidence=float(u.get("confidence", 0)), words=words)
            utterances.append(utt)
            speaker_seconds[str(utt.speaker)] += utt.end - utt.start
    else:
        # No utterances (utterances=False or odd response): chunk the word list on pauses.
        alt = ((results.get("channels") or [{}])[0].get("alternatives") or [{}])[0]
        utterances = _chunk_words(alt.get("words") or [])
        for utt in utterances:
            speaker_seconds[str(utt.speaker)] += utt.end - utt.start
    main = max(speaker_seconds.items(), key=lambda kv: kv[1])[0] if speaker_seconds else None
    main_speaker = int(main) if main not in (None, "None") else None
    return Transcript(video=meta, model=model, main_speaker=main_speaker, speaker_seconds=dict(speaker_seconds), utterances=utterances)


def _chunk_words(words: list[dict], gap: float = 0.8, max_len: float = 12.0) -> list[Utterance]:
    out: list[Utterance] = []
    cur: list[dict] = []
    for w in words:
        if cur and (float(w["start"]) - float(cur[-1]["end"]) > gap or float(w["start"]) - float(cur[0]["start"]) > max_len
                    or w.get("speaker") != cur[-1].get("speaker")):
            out.append(_utt(cur))
            cur = []
        cur.append(w)
    if cur:
        out.append(_utt(cur))
    return out


def _utt(ws: list[dict]) -> Utterance:
    return Utterance(
        start=float(ws[0]["start"]), end=float(ws[-1]["end"]),
        text=" ".join(w.get("punctuated_word") or w.get("word", "") for w in ws),
        speaker=ws[0].get("speaker"),
        confidence=sum(float(w.get("confidence", 0)) for w in ws) / len(ws),
        words=[Word(w=w.get("punctuated_word") or w.get("word", ""), s=float(w["start"]), e=float(w["end"]),
                    c=float(w.get("confidence", 0)), spk=w.get("speaker")) for w in ws],
    )


def write_transcript(t: Transcript, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    txt = out_dir / f"{t.video.id}.txt"
    js = out_dir / f"{t.video.id}.json"
    lines = [
        f"# {t.video.title}",
        f"# {t.video.url}",
        f"# t0={t.video.t0} ({t.video.t0_source}); main_speaker={t.main_speaker}; model={t.model}",
    ]
    for u in t.utterances:
        lines.append(f"{u.start:.2f}\t{u.text.replace(chr(9), ' ')}")
    txt.write_text("\n".join(lines) + "\n")
    js.write_text(t.model_dump_json(indent=1))
    return txt, js


def read_transcript(path: Path) -> Transcript:
    return Transcript.model_validate_json(path.read_text())
