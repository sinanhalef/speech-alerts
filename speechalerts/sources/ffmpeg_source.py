"""Decode any ffmpeg-readable input (file, HLS URL, http stream) into paced PCM chunks."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from collections.abc import AsyncIterator

from speechalerts.models import AudioChunk

log = logging.getLogger(__name__)

BYTES_PER_SECOND = 16000 * 2  # 16 kHz, 16-bit mono


class FfmpegSource:
    """Runs ffmpeg and yields PCM chunks.

    speed=None  -> emit as fast as ffmpeg decodes (correct for live inputs, which are already paced)
    speed=1.0   -> pace to real time (for replaying recordings)
    speed=4.0   -> replay four times faster than real time
    """

    def __init__(
        self,
        input_url: str,
        *,
        name: str = "ffmpeg",
        speed: float | None = None,
        chunk_ms: int = 100,
        live: bool = False,
        extra_args: list[str] | None = None,
        start_seconds: float = 0.0,
        end_seconds: float | None = None,
    ) -> None:
        self.name = name
        self.input_url = input_url
        self.speed = speed
        self.chunk_bytes = int(BYTES_PER_SECOND * chunk_ms / 1000)
        self.live = live
        self.extra_args = extra_args or []
        self.start_seconds = max(start_seconds, 0.0)
        self.end_seconds = end_seconds
        self._proc: asyncio.subprocess.Process | None = None

    def _cmd(self) -> list[str]:
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", os.getenv("FFMPEG_LOGLEVEL", "error"), "-nostdin"]
        if self.live:
            # Reconnect on transient HTTP failures; start at the live edge for lowest latency.
            cmd += [
                "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
                "-live_start_index", "-1",
                "-fflags", "nobuffer", "-flags", "low_delay",
            ]
        if "m3u8" in self.input_url or "/manifest/" in self.input_url:
            # HLS demuxer options: YouTube segments carry odd paths; relax the extension check.
            cmd += ["-allowed_extensions", "ALL", "-extension_picky", "0"]
        cmd += self.extra_args
        if self.start_seconds and not self.live:
            cmd += ["-ss", f"{self.start_seconds:.3f}"]  # input-side seek: fast, keyframe-accurate
        cmd += ["-i", self.input_url]
        if self.end_seconds is not None and not self.live:
            cmd += ["-t", f"{max(self.end_seconds - self.start_seconds, 0.0):.3f}"]
        cmd += [
            "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-acodec", "pcm_s16le",
            "pipe:1",
        ]
        return cmd

    async def chunks(self) -> AsyncIterator[AudioChunk]:
        self._proc = await asyncio.create_subprocess_exec(
            *self._cmd(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=1 << 22,
        )
        assert self._proc.stdout is not None
        stderr_task = asyncio.create_task(self._drain_stderr())
        t_audio = self.start_seconds if not self.live else 0.0
        t_start_wall = time.time() - (t_audio / self.speed if self.speed else 0.0)
        try:
            while True:
                data = await self._proc.stdout.readexactly(self.chunk_bytes)
                if self.speed:
                    # Pace: this chunk should not leave before its scheduled wall time.
                    due = t_start_wall + t_audio / self.speed
                    delay = due - time.time()
                    if delay > 0:
                        await asyncio.sleep(delay)
                yield AudioChunk(pcm=data, t_audio=t_audio, t_wall=time.time())
                t_audio += len(data) / BYTES_PER_SECOND
        except asyncio.IncompleteReadError as exc:
            if exc.partial:
                yield AudioChunk(pcm=exc.partial, t_audio=t_audio, t_wall=time.time())
            log.info("%s: ffmpeg input ended after %.1fs of audio (source position %.1fs)", self.name, t_audio - (self.start_seconds if not self.live else 0.0), t_audio)
        finally:
            stderr_task.cancel()
            await self.close()

    async def _drain_stderr(self) -> None:
        assert self._proc and self._proc.stderr
        async for line in self._proc.stderr:
            text = line.decode(errors="replace").rstrip()
            if text:
                log.warning("ffmpeg: %s", text)

    async def close(self) -> None:
        proc = self._proc
        if proc and proc.returncode is None:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=3)
            except asyncio.TimeoutError:
                proc.kill()
        self._proc = None
