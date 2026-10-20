"""Low-latency puller for YouTube live streams.

Why not let ffmpeg read the HLS playlist? YouTube's live playlists carry a one-hour DVR window
(~720 segments, ~1 MB) and ffmpeg re-downloads the whole thing before every 5-second segment,
so a throttled connection falls behind within a minute. It also starts ~6 segments behind the
live edge.

Instead: resolve the audio-only HLS manifest once, read one segment URL as a template, then fetch
segments directly by sequence number. Each response carries `X-Head-Seqnum`, the newest segment
available, so we can start right at the edge and never touch the playlist again. Segments are
raw ADTS AAC (with an ID3 header), so concatenating them into ffmpeg's stdin decodes cleanly.

End of stream: the feeder records why it stopped on the source (`end_reason` / `error`) rather
than raising, because the STT pump swallows exceptions from the audio generator. Callers read
`outcome` after the pipeline finishes to tell "the broadcast ended" from "something broke".
"""

from __future__ import annotations

import asyncio
import gzip
import logging
import re
import time
from collections.abc import AsyncIterator
from typing import Literal

import httpx

from speechalerts.config import settings
from speechalerts.models import AudioChunk
from speechalerts.sources import youtube
from speechalerts.sources.base import StreamEnded
from speechalerts.sources.ffmpeg_source import BYTES_PER_SECOND
from speechalerts.sources.youtube import ENDED_STATUSES, ResolvedStream

log = logging.getLogger(__name__)

_SQ = re.compile(r"/sq/(\d+)/")
_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}


class YoutubeLiveSource:
    """Yields 16 kHz mono PCM for a live YouTube page URL, staying near the live edge."""

    def __init__(
        self,
        page_url: str,
        *,
        name: str = "",
        chunk_ms: int = 100,
        edge_lag: int = 0,
        resolved: ResolvedStream | None = None,
        stall_seconds: float | None = None,
        resync_attempts: int | None = None,
    ) -> None:
        self.page_url = page_url
        self.name = name or page_url
        self.chunk_bytes = int(BYTES_PER_SECOND * chunk_ms / 1000)
        self.edge_lag = edge_lag  # segments behind the head to start at; 0 = newest available
        self.stall_seconds = stall_seconds if stall_seconds is not None else settings.live_stall_seconds
        self.resync_attempts = resync_attempts if resync_attempts is not None else settings.live_resync_attempts
        self._resolved = resolved  # first resolve result, reused so attach does not run yt-dlp twice
        self._proc: asyncio.subprocess.Process | None = None
        self._feeder: asyncio.Task | None = None
        self._client = httpx.AsyncClient(headers=_HEADERS, timeout=httpx.Timeout(20.0, connect=10.0), follow_redirects=True)
        self.segments_fetched = 0
        self.head_seq: int | None = None
        self.video_id: str | None = None
        self.end_reason: str | None = None  # set when the broadcast ended normally
        self.error: BaseException | None = None  # set when the feeder died for another reason
        if resolved is not None:
            self._pin(resolved)

    @property
    def outcome(self) -> Literal["ended", "error", "unknown"]:
        if self.end_reason is not None:
            return "ended"
        if self.error is not None:
            return "error"
        return "unknown"

    # ---------- manifest / template ----------

    def _pin(self, stream: ResolvedStream) -> None:
        """Lock this source to one video so a resync can never follow the channel to a new stream."""
        if not stream.video_id:
            return
        if self.video_id is None:
            self.video_id = stream.video_id
            if stream.watch_url:
                self.page_url = stream.watch_url
        elif stream.video_id != self.video_id:
            raise StreamEnded(f"replaced by video {stream.video_id}")

    async def _resolve(self) -> ResolvedStream:
        if self._resolved is not None:
            stream, self._resolved = self._resolved, None
        else:
            stream = await youtube.resolve(self.page_url)
        self._pin(stream)
        if not stream.is_live or stream.live_status in ENDED_STATUSES:
            raise StreamEnded(f"live_status={stream.live_status or 'not_live'}")
        return stream

    async def _template(self) -> tuple[str, int]:
        """Return (segment URL template with {sq}, last sequence listed in the playlist)."""
        stream = await self._resolve()
        r = await self._client.get(stream.media_url)
        r.raise_for_status()
        body = r.content
        if body[:2] == b"\x1f\x8b":  # httpx normally decodes gzip; guard anyway
            body = gzip.decompress(body)
        lines = [ln.strip() for ln in body.decode(errors="replace").splitlines()]
        seg_urls = [ln for ln in lines if ln and not ln.startswith("#")]
        if not seg_urls:
            raise RuntimeError("live playlist had no segments")
        last = seg_urls[-1]
        m = _SQ.search(last)
        if not m:
            raise RuntimeError(f"unexpected segment URL shape: {last[:120]}")
        template = _SQ.sub("/sq/{sq}/", last, count=1)
        return template, int(m.group(1))

    # ---------- segment feed ----------

    async def _feed(self, stdin: asyncio.StreamWriter) -> None:
        try:
            await self._feed_loop(stdin)
        except StreamEnded as exc:
            self.end_reason = exc.reason
            log.info("%s: stream ended (%s)", self.name, exc.reason)
        except asyncio.CancelledError:
            self.end_reason = self.end_reason or "cancelled"
            raise
        except Exception as exc:  # noqa: BLE001
            self.error = exc
            log.error("%s: live feeder failed: %s", self.name, exc, exc_info=True)
        finally:
            try:
                stdin.close()
            except Exception:  # noqa: BLE001
                pass

    async def _feed_loop(self, stdin: asyncio.StreamWriter) -> None:
        template, last_listed = await self._template()
        log.info("live template ready; playlist tail sq=%d", last_listed)
        seq = last_listed
        misses = 0
        last_ok = time.monotonic()
        while True:
            url = template.format(sq=seq)
            try:
                r = await self._client.get(url)
            except httpx.HTTPError as exc:
                log.warning("segment %d fetch error: %s", seq, exc)
                await asyncio.sleep(1.0)
                misses += 1
                if misses > 60:
                    template, seq = await self._resync()
                    misses = 0
                continue
            head = r.headers.get("x-head-seqnum")
            if head is not None:
                self.head_seq = int(head)
            log.debug("segment sq=%d -> HTTP %d, %d bytes, head=%s", seq, r.status_code, len(r.content), head)
            if r.status_code == 200 and r.content:
                if self.segments_fetched == 0 and self.head_seq is not None:
                    # First fetch: jump to the live edge instead of the playlist's tail.
                    target = max(self.head_seq - self.edge_lag, seq)
                    if target != seq:
                        log.info("jumping from sq %d to live edge sq %d", seq, target)
                        seq = target
                        continue
                stdin.write(r.content)
                await stdin.drain()
                self.segments_fetched += 1
                misses = 0
                last_ok = time.monotonic()
                seq += 1
                # If we are still behind the head, keep pulling without waiting.
                if self.head_seq is not None and seq <= self.head_seq:
                    continue
                await asyncio.sleep(0.5)
            elif r.status_code in (403, 410) or time.monotonic() - last_ok > self.stall_seconds:
                # Expired URL, or no new segment for a while: ask YouTube whether it is still live.
                log.warning("segment %d -> HTTP %d after %.0fs without audio; re-resolving stream",
                            seq, r.status_code, time.monotonic() - last_ok)
                template, seq = await self._resync(seq)
                last_ok = time.monotonic()
            else:
                # 404 (not published yet) or empty: the next segment is not ready.
                misses += 1
                await asyncio.sleep(0.5 if misses < 20 else 2.0)

    async def _resync(self, keep_seq: int | None = None) -> tuple[str, int]:
        """Re-resolve the stream (URLs expire after a few hours) and continue the sequence.

        Raises StreamEnded as soon as YouTube says the broadcast is over; retries other failures.
        """
        attempts = max(1, self.resync_attempts)
        for attempt in range(attempts):
            try:
                template, last_listed = await self._template()
                seq = keep_seq if keep_seq is not None else last_listed
                # Never fall behind the playlist tail after a resync.
                return template, max(seq, last_listed)
            except StreamEnded:
                raise
            except Exception as exc:  # noqa: BLE001
                log.error("resync failed (%d/%d): %s", attempt + 1, attempts, exc)
                if attempt + 1 < attempts:
                    await asyncio.sleep(min(5 * (attempt + 1), 20))
        raise RuntimeError("could not re-resolve live stream")

    # ---------- AudioSource protocol ----------

    async def chunks(self) -> AsyncIterator[AudioChunk]:
        self._proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
            "-fflags", "nobuffer", "-flags", "low_delay",
            "-probesize", "65536", "-analyzeduration", "500000",
            "-f", "aac", "-i", "pipe:0",  # YouTube live audio segments are ADTS AAC with an ID3 prefix
            "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-acodec", "pcm_s16le", "pipe:1",
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            limit=1 << 22,
        )
        assert self._proc.stdin and self._proc.stdout
        self._feeder = asyncio.create_task(self._feed(self._proc.stdin))
        stderr_task = asyncio.create_task(self._drain_stderr())
        t_audio = 0.0
        try:
            while True:
                data = await self._proc.stdout.readexactly(self.chunk_bytes)
                yield AudioChunk(pcm=data, t_audio=t_audio, t_wall=time.time())
                t_audio += len(data) / BYTES_PER_SECOND
        except asyncio.IncompleteReadError as exc:
            if exc.partial:
                yield AudioChunk(pcm=exc.partial, t_audio=t_audio, t_wall=time.time())
            await self._await_feeder()
            log.info("%s: live decode ended after %.1fs of audio (%s)", self.name, t_audio, self._outcome_text())
        finally:
            stderr_task.cancel()
            await self.close()

    def _outcome_text(self) -> str:
        if self.end_reason:
            return f"ended: {self.end_reason}"
        if self.error:
            return f"error: {self.error}"
        return "reason unknown"

    async def _await_feeder(self, timeout: float = 5.0) -> None:
        """Collect the feeder's result so its exception (if any) is never left unretrieved."""
        if self._feeder is None:
            return
        try:
            await asyncio.wait_for(asyncio.shield(self._feeder), timeout)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            pass
        except Exception as exc:  # noqa: BLE001
            self.error = self.error or exc

    async def _drain_stderr(self) -> None:
        assert self._proc and self._proc.stderr
        async for line in self._proc.stderr:
            text = line.decode(errors="replace").rstrip()
            if text:
                log.warning("ffmpeg: %s", text)

    async def close(self) -> None:
        if self._feeder and not self._feeder.done():
            self._feeder.cancel()
            await self._await_feeder(timeout=2.0)
        proc = self._proc
        if proc and proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=3)
            except asyncio.TimeoutError:
                proc.kill()
        self._proc = None
        await self._client.aclose()
