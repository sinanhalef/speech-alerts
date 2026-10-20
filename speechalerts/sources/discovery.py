"""Poll channel /live pages and report when a matching live stream appears."""

from __future__ import annotations

import asyncio
import logging
import re

from speechalerts.config import settings
from speechalerts.sources import youtube
from speechalerts.sources.youtube import ResolvedStream

log = logging.getLogger(__name__)


def title_matches(title: str, patterns: list[str] | None = None) -> bool:
    patterns = patterns if patterns is not None else settings.watch_title_patterns
    lowered = title.lower()
    return any(re.search(p.lower(), lowered) for p in patterns)


async def probe_channels(
    channels: list[str] | None = None,
    *,
    require_match: bool = True,
    ignore_ids: frozenset[str] | set[str] = frozenset(),
) -> ResolvedStream | None:
    """One pass over the channels: the first live stream that matches and is not in `ignore_ids`."""
    channels = channels or settings.watch_channels
    results = await asyncio.gather(*(youtube.probe_live(c) for c in channels), return_exceptions=True)
    for channel, res in zip(channels, results):
        if isinstance(res, BaseException):
            log.warning("probe %s failed: %s", channel, res)
            continue
        if res is None:
            continue
        if res.video_id and res.video_id in ignore_ids:
            log.debug("live but already handled: %s (%s)", res.title, res.video_id)
            continue
        if require_match and not title_matches(res.title):
            log.info("live but not matching: %s (%s)", res.title, channel)
            continue
        log.info("live stream found: %s (%s)", res.title, res.watch_url or res.page_url)
        return res
    return None


async def wait_for_live_stream(
    channels: list[str] | None = None,
    *,
    poll_seconds: float | None = None,
    require_match: bool = True,
) -> ResolvedStream:
    """Block until one of the channels is live with a matching title, then return it."""
    poll = poll_seconds or settings.watch_poll_seconds
    while True:
        stream = await probe_channels(channels, require_match=require_match)
        if stream is not None:
            return stream
        await asyncio.sleep(poll)
