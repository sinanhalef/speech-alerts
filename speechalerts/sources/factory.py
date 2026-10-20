"""Build an AudioSource from a CLI-style input (local file, page URL, or direct media URL)."""

from __future__ import annotations

import logging
from pathlib import Path

from speechalerts.sources import youtube
from speechalerts.sources.ffmpeg_source import FfmpegSource
from speechalerts.sources.youtube_live import YoutubeLiveSource

log = logging.getLogger(__name__)


async def open_source(
    target: str,
    *,
    speed: float | None,
    live: bool | None = None,
    start_seconds: float = 0.0,
    end_seconds: float | None = None,
) -> tuple[FfmpegSource | YoutubeLiveSource, str]:
    """Return (source, human title). `speed=None` means no pacing (correct for live inputs).
    start/end trim a recording; they are ignored for live streams."""
    clip = dict(start_seconds=start_seconds, end_seconds=end_seconds)
    if Path(target).exists():
        return FfmpegSource(target, name=Path(target).name, speed=speed, live=False, **clip), Path(target).name

    if target.startswith("http") and ("youtube.com" in target or "youtu.be" in target or live is not None):
        stream = await youtube.resolve(target)
        is_live = stream.is_live if live is None else live
        log.info("resolved %s -> live=%s title=%r", target, is_live, stream.title)
        if is_live:
            # Segment-by-sequence puller: immune to the 1 MB playlist problem, starts at the edge.
            # Pinned to the resolved video (watch?v=...) so a resync never follows a channel /live
            # page onto a different broadcast.
            return YoutubeLiveSource(stream.watch_url or target, name=stream.title[:60], resolved=stream), stream.title
        return FfmpegSource(stream.media_url, name=stream.title[:60], speed=speed, live=False, **clip), stream.title

    # Any other URL: hand it straight to ffmpeg.
    return FfmpegSource(target, name=target[:60], speed=speed, live=live or False, **clip), target
