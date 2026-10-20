"""Video metadata (yt-dlp) and audio download (ffmpeg) for one video."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

from speechalerts.sources import youtube

from backtest.marketclock import parse_event_start
from backtest.models import VideoMeta, VideoSpec

log = logging.getLogger(__name__)


async def fetch_meta(spec: VideoSpec) -> tuple[VideoMeta, dict]:
    """Return (meta, raw yt-dlp info)."""
    cmd = youtube._ytdlp_base() + ["-j", spec.page_url()]
    code, out, err = await youtube._run(cmd, timeout=120)
    if code != 0 or not out.strip():
        raise RuntimeError(f"yt-dlp failed for {spec.id}: {err.strip()[:300]}")
    info = json.loads(out.splitlines()[0])
    meta = VideoMeta(
        id=info.get("id") or spec.id,
        url=spec.page_url(),
        title=info.get("title") or "",
        channel=info.get("channel") or info.get("uploader") or "",
        duration=float(info["duration"]) if info.get("duration") else None,
        was_live=bool(info.get("was_live")) or info.get("live_status") == "was_live",
        release_timestamp=float(info["release_timestamp"]) if info.get("release_timestamp") else None,
        upload_timestamp=float(info["timestamp"]) if info.get("timestamp") else None,
        upload_date=info.get("upload_date"),
        label=spec.label,
        group=spec.group,
        notes=spec.notes,
    )
    if spec.event_start:
        meta.t0 = parse_event_start(spec.event_start).timestamp()
        meta.t0_source = "event_start"
    elif meta.was_live and meta.release_timestamp:
        meta.t0 = meta.release_timestamp
        meta.t0_source = "release_timestamp"
    else:
        meta.t0_source = "none"
        log.warning("%s: not a recorded livestream and no event_start given; wall-clock mapping unavailable", meta.id)
    return meta, info


def pick_format_id(info: dict) -> str | None:
    """Format id of the track `pick_format` would choose (so yt-dlp can download it itself)."""
    url = youtube.pick_format(info)
    for f in info.get("formats") or []:
        if f.get("url") == url and f.get("format_id"):
            return str(f["format_id"])
    return None


async def fetch_audio(info: dict, out_path: Path) -> Path:
    """Download the original-language audio track with yt-dlp (fast, throttling-aware), then
    transcode to 16 kHz mono Opus (~15 MB/h) for Deepgram."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = pick_format_id(info)
    page_url = info.get("webpage_url") or info.get("original_url") or f"https://www.youtube.com/watch?v={info.get('id')}"
    stem = out_path.with_suffix("")
    dl_tmpl = f"{stem}.src.%(ext)s"
    cmd = youtube._ytdlp_base() + ["-f", fmt or "bestaudio", "--no-part", "-o", dl_tmpl, page_url]
    code, out, err = await youtube._run(cmd, timeout=3600)
    src = next(iter(sorted(out_path.parent.glob(f"{stem.name}.src.*"))), None)
    if code != 0 or src is None:
        raise RuntimeError(f"yt-dlp download failed: {err.strip()[-400:]}")
    tmp = out_path.with_suffix(".part.ogg")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(src),
           "-vn", "-ac", "1", "-ar", "16000", "-c:a", "libopus", "-b:a", "32k", str(tmp)]
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
    _, err_b = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {err_b.decode(errors='replace')[-400:]}")
    tmp.rename(out_path)
    src.unlink(missing_ok=True)
    return out_path
