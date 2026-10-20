"""Deepgram live websocket transcription (SDK 7.x, listen v1)."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator

from deepgram import AsyncDeepgramClient
from deepgram.listen.v1.types.listen_v1results import ListenV1Results

from speechalerts.config import settings
from speechalerts.models import AudioChunk, TranscriptSegment, Word

log = logging.getLogger(__name__)

_DONE = object()


class DeepgramTranscriber:
    """Feeds PCM to Deepgram and yields TranscriptSegments (interim and final).

    One websocket session per call. If the socket drops mid-stream the session is reopened
    and audio continues; Deepgram's `start` timestamps restart at 0 on a new socket, so we
    add the audio offset at reconnect time to keep t_audio continuous.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        keyterms: list[str] | None = None,
        keepalive_seconds: float = 5.0,
        diarize: bool | None = None,
    ) -> None:
        self.api_key = api_key or settings.deepgram_api_key
        if not self.api_key:
            raise RuntimeError("DEEPGRAM_API_KEY is not set (put it in .env)")
        self.model = model or settings.deepgram_model
        self.keyterms = keyterms or []
        self.keepalive_seconds = keepalive_seconds
        self.diarize = settings.diarize if diarize is None else diarize
        self._client = AsyncDeepgramClient(api_key=self.api_key)

    async def transcribe(self, audio: AsyncIterator[AudioChunk]) -> AsyncIterator[TranscriptSegment]:
        queue: asyncio.Queue[TranscriptSegment | object] = asyncio.Queue()
        # Deepgram timestamps restart at 0 per socket; audio_offset maps them back to source time.
        # It is None until the first chunk tells us where the source starts (clips begin at --from).
        audio_offset: float | None = None
        last_chunk_t_audio = 0.0
        audio_exhausted = False
        session_no = 0

        # Pump the source into a queue from its own task. The sender waits on the queue with a
        # timeout for keepalives; waiting directly on the generator with wait_for would cancel
        # (and kill) the generator whenever a live read took longer than the keepalive interval.
        audio_q: asyncio.Queue[AudioChunk | None] = asyncio.Queue(maxsize=200)

        async def pump() -> None:
            last = time.monotonic()
            try:
                async for chunk in audio:
                    now_m = time.monotonic()
                    if now_m - last > 1.5:
                        log.debug("source stall: %.1fs between chunks (source at %.1fs)", now_m - last, chunk.t_audio)
                    last = now_m
                    if audio_q.full():
                        log.debug("audio queue full; sender is not keeping up")
                    await audio_q.put(chunk)
            except Exception as exc:  # noqa: BLE001
                log.error("audio source failed: %s", exc)
            finally:
                log.info("audio source ended")
                await audio_q.put(None)

        pump_task = asyncio.create_task(pump())

        async def session() -> None:
            nonlocal audio_offset, last_chunk_t_audio, audio_exhausted, session_no
            session_no += 1
            this_session = session_no
            connect_kwargs: dict = dict(
                model=self.model,
                encoding="linear16",
                sample_rate=settings.sample_rate,
                channels=1,
                interim_results=True,
                smart_format=True,
                punctuate=True,
                numerals=True,
                endpointing=300,
                vad_events=False,
            )
            if self.diarize:
                # Per-word speaker labels; labels restart at 0 on every new socket. The streaming
                # endpoint rejects `diarize_model` (HTTP 400), so only the flag is sent.
                connect_kwargs["diarize"] = "true"
            if self.keyterms and self.model.startswith("nova-3"):
                # nova-3 keyterm prompting: boosts recognition of company names.
                connect_kwargs["keyterm"] = self.keyterms[:100]

            async with self._client.listen.v1.connect(**connect_kwargs) as conn:
                log.info("deepgram connected (model=%s, offset=%s)", self.model, f"{audio_offset:.1f}s" if audio_offset is not None else "pending")
                session_offset = audio_offset
                first_chunk_in_session = True

                async def sender() -> None:
                    nonlocal last_chunk_t_audio, audio_exhausted, first_chunk_in_session, session_offset, audio_offset
                    last_send = time.monotonic()
                    sent_bytes = 0
                    last_report = time.monotonic()
                    try:
                        while True:
                            try:
                                chunk = await asyncio.wait_for(audio_q.get(), timeout=self.keepalive_seconds)
                            except asyncio.TimeoutError:
                                if time.monotonic() - last_send >= self.keepalive_seconds:
                                    await conn.send_keep_alive()
                                    last_send = time.monotonic()
                                continue
                            if chunk is None:
                                audio_exhausted = True
                                break
                            if first_chunk_in_session:
                                first_chunk_in_session = False
                                if session_offset is None:
                                    session_offset = chunk.t_audio
                                    audio_offset = chunk.t_audio
                            last_chunk_t_audio = chunk.t_audio + len(chunk.pcm) / (settings.sample_rate * 2)
                            t_send = time.monotonic()
                            await conn.send_media(chunk.pcm)
                            if time.monotonic() - t_send > 0.5:
                                log.debug("slow websocket send: %.1fs", time.monotonic() - t_send)
                            last_send = time.monotonic()
                            sent_bytes += len(chunk.pcm)
                            if time.monotonic() - last_report >= 30:
                                log.info("deepgram: sent %.0fs of audio so far (source at %.1fs)", sent_bytes / (settings.sample_rate * 2), last_chunk_t_audio)
                                last_report = time.monotonic()
                    except Exception as exc:  # noqa: BLE001
                        log.error("deepgram sender failed: %s", exc)
                        raise
                    finally:
                        try:
                            await conn.send_close_stream()
                        except Exception:  # socket may already be gone
                            pass

                send_task = asyncio.create_task(sender())
                last_msg = time.monotonic()
                try:
                    async for msg in conn:
                        if time.monotonic() - last_msg > 3:
                            log.debug("receiver gap: %.1fs without a deepgram message", time.monotonic() - last_msg)
                        last_msg = time.monotonic()
                        if isinstance(msg, ListenV1Results):
                            log.debug("deepgram results: start=%.2f dur=%.2f final=%s text=%r", msg.start, msg.duration, msg.is_final, (msg.channel.alternatives[0].transcript[:60] if msg.channel.alternatives else ""))
                            seg = self._to_segment(msg, session_offset or 0.0, this_session)
                            if seg is not None:
                                await queue.put(seg)
                        elif isinstance(msg, bytes):
                            continue
                        else:
                            log.info("deepgram message: %s", getattr(msg, "type", type(msg)))
                finally:
                    if not send_task.done():
                        send_task.cancel()
                    audio_offset = last_chunk_t_audio

        async def runner() -> None:
            backoff = 1.0
            try:
                while not audio_exhausted:
                    try:
                        await session()
                        if audio_exhausted:
                            break
                        log.warning("deepgram session ended early, reconnecting")
                    except Exception as exc:  # noqa: BLE001
                        log.error("deepgram session error: %s (retry in %.0fs)", exc, backoff)
                        await asyncio.sleep(backoff)
                        backoff = min(backoff * 2, 30)
                        continue
                    backoff = 1.0
            finally:
                await queue.put(_DONE)

        run_task = asyncio.create_task(runner())
        try:
            while True:
                item = await queue.get()
                if item is _DONE:
                    break
                yield item  # type: ignore[misc]
        finally:
            if not run_task.done():
                run_task.cancel()
            if not pump_task.done():
                pump_task.cancel()

    @staticmethod
    def _to_segment(msg: ListenV1Results, offset: float, session: int = 0) -> TranscriptSegment | None:
        alt = msg.channel.alternatives[0] if msg.channel.alternatives else None
        if alt is None or not alt.transcript.strip():
            return None
        words = [
            Word(
                text=w.punctuated_word or w.word,
                start=w.start + offset,
                end=w.end + offset,
                confidence=w.confidence,
                speaker=getattr(w, "speaker", None),
            )
            for w in alt.words
        ]
        return TranscriptSegment(
            text=alt.transcript,
            t_audio_start=msg.start + offset,
            t_audio_end=msg.start + msg.duration + offset,
            t_wall=time.time(),
            is_final=bool(msg.is_final),
            speech_final=bool(msg.speech_final),
            confidence=alt.confidence,
            words=words,
            session=session,
        )
