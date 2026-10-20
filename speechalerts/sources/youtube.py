"""Resolve YouTube (and any other yt-dlp supported) page URLs to direct media URLs."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass

from speechalerts.config import settings

log = logging.getLogger(__name__)

_VIDEO_ID = r"[A-Za-z0-9_-]{11}"
_ID_PATTERNS = [
    re.compile(r"[?&]v=(" + _VIDEO_ID + r")(?:[&#]|$)"),
    re.compile(r"youtu\.be/(" + _VIDEO_ID + r")(?:[?&#/]|$)"),
    re.compile(r"/(?:live|shorts|embed|v)/(" + _VIDEO_ID + r")(?:[?&#/]|$)"),
]
# yt-dlp `live_status` values that mean the broadcast is over (or never was one).
ENDED_STATUSES = frozenset({"was_live", "post_live", "not_live"})


@dataclass(slots=True)
class ResolvedStream:
    page_url: str
    media_url: str
    title: str
    is_live: bool
    video_id: str = ""
    watch_url: str = ""  # canonical https://www.youtube.com/watch?v=<id>; pin resyncs to this
    live_status: str = ""  # yt-dlp: is_live | is_upcoming | was_live | post_live | not_live


def video_id_from_url(url: str) -> str | None:
    for pat in _ID_PATTERNS:
        m = pat.search(url)
        if m:
            return m.group(1)
    return None


def canonical_watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def _ytdlp_base(*, cookies: str | None = None) -> list[str]:
    cmd = ["yt-dlp", "--quiet", "--no-warnings", "--no-playlist"]
    cookies = cookies if cookies is not None else settings.ytdlp_cookies_from_browser
    if cookies:
        cmd += ["--cookies-from-browser", cookies]
    return cmd


async def _run(cmd: list[str], timeout: float = 60) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    try:
        out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        raise
    return proc.returncode or 0, out.decode(errors="replace"), err.decode(errors="replace")


def pick_format(info: dict) -> str | None:
    """Choose an audio format URL from yt-dlp's format list.

    Live: audio-only HLS (lowest latency ffmpeg can follow). VOD: plain HTTPS audio-only,
    highest bitrate, which avoids HLS extension quirks. Falls back to the top-level url.
    """
    # acodec is often None (unknown) on live HLS formats; only an explicit "none" means no audio.
    formats = [f for f in info.get("formats") or [] if f.get("url") and f.get("acodec") != "none"]
    audio_only = [f for f in formats if f.get("vcodec") in (None, "none")]
    is_live = bool(info.get("is_live"))

    def rank(f: dict) -> tuple:
        # YouTube auto-dubs recorded streams into many languages and lists every dub as a format.
        # The original track has language_preference >= 0 (dubs are -1) and "original" in its note.
        note = str(f.get("format_note") or "").lower()
        lang = str(f.get("language") or "").lower()
        original = 1 if ("original" in note or (f.get("language_preference") or -1) >= 0) else 0
        english = 1 if lang.startswith("en") or not lang else 0
        high = 1 if "high" in note else 0  # live audio tracks are labelled "Default, low/high"
        return (original, english, float(f.get("abr") or f.get("tbr") or 0), high)

    if is_live:
        hls = [f for f in audio_only if str(f.get("protocol", "")).startswith("m3u8")]
        pool = hls or [f for f in formats if str(f.get("protocol", "")).startswith("m3u8")] or formats
    else:
        https = [f for f in audio_only if f.get("protocol") in ("https", "http")]
        pool = https or audio_only or formats
    if not pool:
        return info.get("url")
    return max(pool, key=rank)["url"]


def stream_from_info(info: dict, page_url: str) -> ResolvedStream:
    """Build a ResolvedStream from one yt-dlp `-j` record. Raises if no media URL can be chosen."""
    media_url = pick_format(info)
    if not media_url:
        raise RuntimeError(f"yt-dlp returned no media URL for {page_url}")
    is_live = bool(info.get("is_live"))
    live_status = str(info.get("live_status") or ("is_live" if is_live else "not_live"))
    video_id = str(info.get("id") or "") or (video_id_from_url(page_url) or "")
    watch_url = ""
    if video_id and "youtube" in str(info.get("extractor_key") or info.get("extractor") or "youtube").lower():
        watch_url = canonical_watch_url(video_id)
    return ResolvedStream(
        page_url=page_url,
        media_url=media_url,
        title=info.get("title") or page_url,
        is_live=is_live,
        video_id=video_id,
        watch_url=watch_url,
        live_status=live_status,
    )


async def resolve(page_url: str) -> ResolvedStream:
    """Return the best audio media URL for a page (HLS for live, HTTPS audio for recordings)."""
    cmd = _ytdlp_base() + ["-j", page_url]
    code, out, err = await _run(cmd)
    if code != 0 or not out.strip():
        raise RuntimeError(f"yt-dlp failed for {page_url}: {err.strip()[:400]}")
    info = json.loads(out.splitlines()[0])
    return stream_from_info(info, page_url)


async def probe_live(page_url: str) -> ResolvedStream | None:
    """Return the live stream behind a channel /live page, or None if nothing is live right now.

    A stream that just ended (`post_live`) or is only scheduled (`is_upcoming`) counts as not live.
    """
    try:
        stream = await resolve(page_url)
    except RuntimeError as exc:
        # yt-dlp exits non-zero when a channel is not live; that is the normal idle case.
        log.debug("probe %s: %s", page_url, exc)
        return None
    if not stream.is_live or stream.live_status != "is_live":
        log.debug("probe %s: live_status=%s, not attaching", page_url, stream.live_status)
        return None
    return stream
