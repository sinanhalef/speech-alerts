# Speech Alerts — handoff (written 2026-09-12, end of day 1)

Read this first in a new session. It captures the product, every decision, what is built and
verified, what broke and why, and what is next. `README.md` has the runbook; this file has the
context behind it.

---

## 1. The product

An app that alerts retail investors within seconds when the President (later: other political figures)
mentions a stock, company, industry, commodity or country in a market-relevant way during a live
speech. Thesis: HFT firms react in milliseconds, but the retail wave starts minutes later; a user
sitting in a café who gets a push within seconds can act before that wave. Target price $1-2/month
on iOS.

Three stages:

1. **Stage 1 (current, private, not distributed):** Python backend on the user's Mac. Listens to
   live speeches, transcribes, extracts mentions, shows alerts in the terminal and on a local web
   page, logs everything to SQLite. Grey-area methods (yt-dlp on YouTube) are acceptable here.
2. **Stage 2:** iOS app (SwiftUI, StoreKit 2 subscription), hosted backend (small VM for the
   listener + Firebase for push/feed/auth), neutral brand name, official stream sources, terms.
3. **Stage 3:** more political figures (the `figure` field exists on every model already).

## 2. Decisions the user made (do not re-litigate)

| Question | Decision |
|---|---|
| Sources | Live audio streams first. Truth Social later (its ToS forbids scraping). |
| Speech-to-text | Deepgram streaming, Nova-3. Local Whisper rejected (latency). |
| Extraction | Hybrid: dictionary (instant heads-up) + Claude confirmation. Model `claude-haiku-4-5` for latency/cost. |
| Language | Python 3.12 via uv (system Python is 3.14, kept away for wheel compatibility). |
| Hosting | Stage 1 on the Mac on purpose (YouTube bot-checks datacenter IPs; listener is a 24/7 process, wrong shape for Cloud Run). Stage 2: small VM + Firebase (FCM push, Firestore feed, Sign in with Apple). |
| Alert style | Factual only ("X said Y about Z at T"), labelled stance, never "buy". |

## 3. Legal constraints that shape the code

- **Not investment advice.** Impersonal publication (publisher's exclusion, Lowe v. SEC). Alerts
  carry stance/action labels, never recommendations or rankings. Verbatim quote stored per alert.
- **Content rights.** Presidential remarks are public domain; broadcast recordings are not. We
  keep short quotes and transcript segments for audit, never redistribute audio/full transcripts.
- **YouTube ToS.** yt-dlp capture breaks YouTube's terms (contract, not copyright). OK privately;
  Stage 2 must move to official White House streams or a licensed feed.
- **Trademark.** "Speech Alerts" is a working name only; The President marks are enforced. Ship under a
  neutral brand with "The President" as an in-app filter.
- **App Store gates (Stage 2).** Not-financial-advice disclaimer, no trading facilitation (so no
  broker licensing), privacy label (only a push token), careful wording ("alerts", not "signals").
- **Liability (Stage 2).** Terms must disclaim latency and transcription accuracy. Every alert logs
  four timestamps (audio position, wall-clock when audio arrived, transcript arrival, alert time).

## 4. Architecture (as built)

```
YouTube page URL
  ├─ live      → sources/youtube_live.py  (fetch AAC segments by sequence number, pipe → ffmpeg)
  └─ recording → sources/ffmpeg_source.py (yt-dlp resolves an HTTPS audio URL, ffmpeg decodes,
                                            optional --from/--to clip, optional pacing --speed)
        ↓ 16 kHz mono s16le PCM, 100 ms chunks, AudioChunk{pcm, t_audio, t_wall}
stt/deepgram_stream.py   Deepgram listen v1 websocket, nova-3, interim results, keyterm boosting,
                         keepalive, reconnect; audio pumped via a queue from its own task
        ↓ TranscriptSegment{text, t_audio_start/end, t_wall, is_final, words}
transcript.py            RollingWindow (last 90 s of finals + current interim), AudioClock
        ↓
extract/dictionary.py    Aho-Corasick over entities.yaml aliases + trigger words; needs_context
                         entities only fire near a trigger (triggers may sit in the prior 10 s)
        ↓ Candidate                                  → alerts/engine.py → HEADS-UP alert (yellow)
extract/llm_confirm.py   debounced 1 s, concurrent, prompt-guided JSON (NOT schema-constrained),
                         candidates bracket-marked in a 30 s transcript excerpt, live context via
                         context_provider, deferred recheck after 3 s for mentions at the window end
        ↓ Mention{entity, tickers, stance, action, confidence, quote, summary}
alerts/engine.py         CONFIRMED (green) or RETRACTED (dim red); cooldown 600 s per dictionary
                         entity; retracted entities muted 60 s; stance flip pos↔neg re-alerts
        ↓
sinks/terminal.py (rich) · sinks/sqlite.py (runs/alerts/segments) · sinks/broadcast.py → web/app.py
(FastAPI, SSE at /events, page at http://127.0.0.1:8000)
```

`pipeline.py` wires it; `cli.py` exposes `listen | replay | watch | serve | eval | build-entities`.

### Key files

| Path | What |
|---|---|
| `speechalerts/config.py` | All settings from `.env`: keys, `LLM_MODEL`, `LLM_DEBOUNCE_SECONDS=1.0`, `LLM_MIN_CONFIDENCE=0.7`, `LLM_CONTEXT_SECONDS=30`, `COOLDOWN_SECONDS=600`, `WATCH_CHANNELS`, `WATCH_TITLE_PATTERNS`, `YTDLP_COOKIES_FROM_BROWSER` |
| `speechalerts/models.py` | AudioChunk, TranscriptSegment, Entity, Candidate, Mention (pydantic), Alert (+`latency_ms`, `to_dict`) |
| `speechalerts/extract/entities.yaml` | ~190 curated entities (companies, sectors→ETFs, countries→ETFs, persons→their company, crypto names) + 92 trigger words. `needs_context: true` on ambiguous aliases (target, apple-as-fruit is handled by the LLM, countries, "chip", "ai", "meta", "gm", "ge", "ups"). |
| `speechalerts/sources/youtube.py` | `resolve()` via `yt-dlp -j`; `pick_format()` prefers original-language track, English, bitrate, "high" |
| `speechalerts/sources/youtube_live.py` | Live puller (see §6.3) |
| `speechalerts/sources/discovery.py` | `wait_for_live_stream()` polls channel `/live` pages every 60 s, matches titles |
| `speechalerts/stt/text_replay.py` | Fake transcriber replaying a `t<TAB>text` file: zero-cost extractor testing |
| `speechalerts/evaluate.py` | Golden-set scoring: precision/recall, heads-up and confirmed latency p50/p95 |
| `eval/golden/synthetic_intel_speech.{txt,json}` + `eval/audio/*.wav` | Synthetic speech (macOS `say`) with 11 expected mentions and 2 traps |
| `deploy/com.speechalerts.watch.plist` | launchd job for unattended `watch --quiet` |
| `scripts/build_ticker_list.py` | SEC company list → `data/entities/sec_tickers.json` (context-gated, not yet run) |
| `tests/` | 35 unit tests, `uv run pytest` |

## 5. Verified results

### Synthetic golden set (real Deepgram + Claude, audio at 1x)

| Metric | Value |
|---|---|
| Confirmed mentions | 11 of 11, 0 false positives; traps ("apple pie", "hit our target") correctly retracted |
| Heads-up latency (audio received → alert) | p50 0.7 s, p95 1.7 s |
| Confirmed latency | p50 4.2 s, p95 10.5 s |
| Claude call | 1.2-3 s, ~600 in / ~120 out tokens |

Reproduce: `uv run python -m speechalerts eval` (~1.5 min STT). Text-only: `eval --text --no-llm`.

### Real recordings and live

- Crypto executives event (`K3_mcCs8Z8I`, 15:30-17:30): Coinbase, ICE, Nasdaq, Robinhood, Kraken,
  Ripple, Gemini all confirmed; "Vlad Tether" (STT error) raised a Tether heads-up that the LLM
  retracted.
- Live (Sky News 24/7, and the President's Ireland remarks / a press Q&A): continuous transcript, 60 s
  audio in 60 s wall, alerts fire on live speech (Iran, oil). Live latency floor ≈ 5-7 s after
  the broadcast because YouTube serves 5 s segments; broadcaster delay is on top.

## 6. Bugs found and fixed (the expensive lessons)

### 6.1 Claude confirmation
- Schema-constrained output (`output_config.format` / `messages.parse`) took ~6.5 s on Haiku vs
  ~2.5 s for prompt-guided JSON with the same content. Switched; `parse_mentions()` strips code
  fences, validates with pydantic, salvages valid entries and repairs truncated JSON.
- Calls were serialized and queued (confirmed latency hit 20 s). Now concurrent.
- Haiku described every entity in the window. Fix: candidates bracket-marked in the transcript,
  "at most one entry per listed candidate", engine ignores non-candidate entries.
- Every interim transcript re-submitted the same entity (5-8 calls per mention). Fix: an entity is
  blocked while a call (or its recheck) is in flight; `still_needed` filter at fire time.
- Mentions at the very end of the window were retracted before the sentence finished. Fix: defer
  (keep heads-up) and recheck after 3 s **with live context** (`context_provider`). The first
  version reused the submission-time snapshot and rechecked the same truncated text.
- Retracted false positives re-fired on the next interim. Fix: 60 s retraction cooldown.
- A sector alert sharing a ticker masked a company alert (COIN). Fix: dedupe key = dictionary
  entity id, not ticker.

### 6.2 YouTube recordings
- Recorded live streams expose ~10 **auto-dubbed audio tracks** as equal formats; picking by
  bitrate chose Arabic → Deepgram English produced one garbled line in 10 minutes. `pick_format`
  now prefers `language_preference >= 0` / "original".
- ffmpeg rejects YouTube HLS segments unless `-allowed_extensions ALL -extension_picky 0` (only
  valid for HLS inputs; passing them for HTTPS inputs errors).
- Deepgram timestamps restart at 0 per socket; clipped replays (`--from`) needed the offset added
  back, else timestamps and latency were wrong.
- Replay faster than 1x makes Deepgram lag behind the feed → latency numbers meaningless (alerts
  still correct). Eval defaults audio to 1x.

### 6.3 YouTube live (the big one)
- yt-dlp reports live audio formats with `acodec: None`; treating None as "no audio" discarded
  them → "no media URL" crash.
- **Sender cancellation bug:** `asyncio.wait_for(audio_gen.__anext__(), 5)` for keepalives cancels
  the generator itself when it times out; live HLS first reads take >5 s → audio source silently
  killed, run "finished" after 2 segments with no error. Fix: pump task + queue.
- **Playlist size:** YouTube live HLS playlists carry a 1 h DVR window (~720 segments, 1 MB);
  ffmpeg refetches it before every 5 s segment; on throttled connections each segment took 8-19 s
  and the transcript arrived in bursts with 20-50 s gaps. ffmpeg also starts ~6 segments (30 s)
  behind live. The DVR window is inside the signed URL (rewriting → 403). yt-dlp cannot pipe live
  HLS to stdout (uses ffmpeg internally).
  **Solution:** `sources/youtube_live.py` fetches the playlist once (gzip: 18 KB), takes a
  segment URL as template (URLs differ only in `/sq/N/`), then fetches segments by sequence
  number; every response has `X-Head-Seqnum` (live edge) so it jumps to the edge and polls ahead.
  Segments are ADTS AAC with an ID3 prefix → ffmpeg `-f aac -i pipe:0` (not mpegts).
- YouTube inserts **server-side ad breaks** (loud music, `#EXT-X-DATERANGE:CLASS="CUEPOINT-AD"`)
  into live streams; transcript goes quiet. Not a bug.

## 7. Observations from the live Q&A run (open question from the user)

The President on the podium mic transcribes at confidence 0.99-1.0. Reporters asking questions off-mic
transcribe at 0.79-0.83 with dropped/garbled words ("President from the general Dasha, go said
that very little is off limits"). This is an audio-quality limit (distance, room echo, no mic),
not a Deepgram bug; Nova-3 is already the strongest streaming model. Options, none implemented yet:
1. Diarization (`diarize_model="v1"` on the connect call) to label speakers, then gate alerts to
   the dominant speaker (The President) — also a product requirement: a reporter saying "Coinbase" must
   not alert. Deepgram per-word `confidence` is already in `TranscriptSegment.words`.
2. Pass low-confidence flags to the LLM prompt so it discounts garbled spans; mark low-confidence
   text dimmer in the UI.
3. Mild audio preprocessing for quiet speech (`speechnorm`/`dynaudnorm` in the ffmpeg chain);
   small gain, worth an A/B on a recorded Q&A.
4. Whisper-large as a slow second pass for context would improve hard audio but at 5-10 s; never
   for the alert path.

## 8. Costs (estimated, 1 h transcription/day, 1000 users)

Deepgram ~$14/mo (list $0.0077/min; promo $0.0048), Claude ~$2-3, Firebase push free, Firestore
$0-2, Apple Developer $8, misc $1-3. Total ~$25-45/mo; scales with speech hours, not users
(~3 cents/user). Not included: market data feed ($50-200+/mo if live quotes), legal setup, Apple's
15-30 % cut of revenue.

## 9. How to run (see README for the full list)

```bash
cp .env.example .env    # DEEPGRAM_API_KEY, ANTHROPIC_API_KEY are set already in the user's .env
uv sync && uv run pytest
uv run python -m speechalerts listen "https://www.youtube.com/watch?v=..."          # live or VOD
uv run python -m speechalerts watch                                                  # auto-attach
uv run python -m speechalerts replay "URL" --from 12 --to 15 --speed 4               # clip a VOD
uv run python -m speechalerts replay --transcript eval/golden/synthetic_intel_speech.txt --speed 10 --no-llm
uv run python -m speechalerts eval                                                   # golden set
uv run python -m speechalerts -v listen ... > logs/x.log 2>&1                        # debug: stall/loop/segment logs
FFMPEG_LOGLEVEL=info ...                                                            # ffmpeg chatter
```

Flags: `--no-llm`, `--no-web`, `--quiet`, `--interim`. Web page: http://127.0.0.1:8000.
Data: `data/alerts.sqlite3` (tables runs, alerts, segments). Logs from tests: `logs/`.

## 10. Open items / next steps (suggested order)

1. **Speaker gating** (§7): diarization → only alert on the main speaker; show confidence in UI.
2. **Real golden files from real speeches.** yt-dlp `--write-auto-sub` pulls YouTube's captions
   for free with timestamps → build `eval/golden/*.json` for past events (crypto event, Intel
   stake, tariff announcements). A `make-golden` command was offered, not built.
3. **Run `build-entities`** (SEC list, context-gated) and review false positives it introduces.
4. ~~Watch mode in anger~~ → done on day 3 (daemon, §13). Still to do: install the plist and
   confirm title patterns catch a real event (`WATCH_TITLE_PATTERNS`).
5. **Speech-hours cost control:** pause STT when the stream is music/ads or when the President is not
   speaking (silence/ad-cue detection; diarization helps here too).
6. **Latency floor:** 5 s YouTube segments dominate live latency. Options: check whether the
   broadcaster offers 1-2 s "ultra-low-latency" segments (segment `dur/` in the URL), or a
   non-YouTube source (official whitehouse.gov live, C-SPAN) for Stage 2.
7. **Stage 2 prep:** ~~Firebase project, `sinks/firestore.py`~~ (day 3, §13), APNs fan-out /
   a client subscribed to the FCM topic, neutral brand, terms/disclaimers, official stream
   sources, LLC.
8. Housekeeping: git repo is initialized but nothing is committed yet (user never asked for
   commits). `.env` is gitignored.

## 11. Things a new session should know about the user

- Wants to move fast and test on real events; asks "how does X work" and expects a direct
  answer plus the command.
- Approved plans via plan mode; decisions in §2 are final unless the user reopens them.
- Keys are in `.env` (Deepgram, Anthropic). Deepgram signup credit is being used.

---

## 12. Day 2 (2026-09-15): speaker attribution + dictionary pass

Trigger: watching the live briefing
`SE_aiQ4tBbc` and re-reading runs 35/37/39 showed reporter questions confirming as alerts
(Kurdistan oil, "Mark Meredith, Fox News"), STT-shaped false positives ("SS Coal", "the RTX
artificial intelligence", "Dell'sy" = Delcy Rodríguez) and misses ("B-2 bombers ... we ordered
25 more", "100,000,000 barrels of oil ... refineries ... partnership ... Venezuela").

### What changed
- **Speaker layer.** `DIARIZE=1` sends `diarize=true` to Deepgram streaming (`diarize_model` is
  rejected with HTTP 400 on the websocket, contrary to the docs). `Word.speaker`,
  `TranscriptSegment.session/speaker_label`, `transcript.SpeakerTracker` (dominant speaker =
  most words in 300 s, min 60 words, reset per socket), `Candidate.speaker/speaker_role/
  word_confidence` (from `dictionary._words_at`). Engine: `speaker_role == "other"` → silent
  heads-up (`_Recent.emitted=False`, logged `question: ...`), still sent to Claude; a later
  mention by the figure upgrades it to a real heads-up regardless of cooldowns; nothing is
  retracted that was never shown. `Mention.speaker` (figure/questioner/other) and `Action.MILITARY`
  added; the prompt renders `[main speaker]`/`[speaker N]` turns and per-candidate
  `spoken by` + `word confidence`. Terminal/web show `T`/`Q` per transcript line.
- **Prompt: exactly one entry per candidate.** Letting Haiku omit rejects made recall flicker
  (India/CNN dropped on one run, kept on the next). Forcing an entry per candidate gave 18/18
  across the four golden sets at ~+0.5 s per extra candidate in a batch.
- **Dictionary** (224 entities, 110 triggers): ticker-like and first-name aliases gated as
  `*_word` twins (rtx, amd, ibm, dell, coal, jensen, elon/musk, bezos, ellison, masa, harley, coke,
  visa, deere, jeep/dodge, 747, lilly, interceptors, patriot); media outlets gated
  (`*_outlet`); defense hardware (B-2, F-47, HIMARS, THAAD, Tomahawk, submarines), refiners
  (VLO/MPC/PSX), stock market (SPY/QQQ/DIA), Fed nominees and "cut rates", Skydance/Kimmel/
  Nexstar/Sinclair, Cracker Barrel, American Eagle, Kenvue/Tylenol, vaccines, EVs, heavy trucks,
  furniture, prediction markets, World Liberty, Argentina, Colombia. Triggers: fcc, defamation,
  settlement, ratings, ordered, purchase(d), partnership, barrels, refineries.
  `Entity.key` strips `_word/_short/_strong/_outlet/_abc/_patriot` so twins share dedupe.
- **Word boundary**: an apostrophe after an alias only ends the word when it is a possessive.
- **Cooldowns on audio time** (`_Recent.t` = candidate `t_audio`), so `eval --text` at 20x
  behaves like live.
- **Eval**: `make-golden RUN_ID --out ...` exports stored segments as replay text
  (`t<TAB>speaker<TAB>text`, speaker 0 = figure, hand-annotated for runs 35 and 39);
  `not_expected` in golden JSON (listed as `wrong:`). Golden sets: `press_qa_iran_2026_09_12`,
  `iran_remarks_2026_09_14`, `briefing_2026_09_15`, `synthetic_intel_speech` (now expects the
  stock-market and semiconductor mentions too).

### Results (text replay, Claude only)
18/18 expected confirmed, 0 wrong, 0 extra; Claude p50 2.9 s. Reporter cases behaved: the
tomahawk question was held silently, the President's answer fired a heads-up that Claude retracted as
`questioner`-driven; the Kurdistan oil question produced no alert; "Fox News" never fired.

### Diarization latency (150 s live clip replayed at 1x, `--no-llm`)
Same 36 final segments both ways; source-to-transcript delay p50 1.11 s off vs 1.13 s on, p90
2.16 s both, mean 1.08 s both. Diarization is free on the STT path, so `DIARIZE` defaults to on.
Labels: first 5 finals (~20 s, under `SPEAKER_MIN_WORDS`) unlabelled, then all `T`.
Method: `scratchpad/ab_analyze.py` over the replay DBs: (t_wall - run.started_at) - t_audio_end.

### Open
- The dominant-speaker rule assumes the figure talks most; on a panel or a long reporter
  monologue it can flip. `SPEAKER_MIN_WORDS`/`SPEAKER_WINDOW_SECONDS` are the knobs.
- Cooldown semantics unchanged: a second, different statement about the same company inside
  600 s (B-2 "dropped bombs" then "we ordered 25 more") is a count bump, not a new alert.
- Golden sets are text replays with hand-annotated speakers; a diarized audio golden set is
  still to be recorded from a real Q&A.

---

## 13. Day 3 (2026-10-01): always-on daemon + Firebase notifications (simulated)

Goal: the system runs on its own
cycle (poll → attach when the President goes live → alert → back to polling) and alerts reach a Firebase
project as if an app were subscribed.

### Decisions
- New Firebase project `your-firebase-project` (Firestore native, nam5; FCM enabled). Backend service
  account `speechalerts-backend@…` with `datastore.user` + `firebasecloudmessaging.admin`; key in
  `secrets/` (gitignored), path in `.env` as `FIREBASE_CREDENTIALS`. Rules: clients read-only.
- Push on HEADSUP and CONFIRMED; RETRACTED only merges `state`/`resolved_by` into the heads-up doc.
- Simulation = Firestore console + `FCM_DRY_RUN=1` (FCM validates, nothing delivered, log says
  `would push …`). No client yet.

### What changed
- **Video pinning.** `ResolvedStream` carries `video_id`, `watch_url`, `live_status`
  (`stream_from_info`, `video_id_from_url`). `YoutubeLiveSource` takes `resolved=` (no second
  yt-dlp at attach) and pins `page_url` to `watch?v=…`; a resync that returns another id raises
  `StreamEnded("replaced by …")`. `probe_live` only returns `live_status == "is_live"`.
- **Bounded end of stream.** `sources/base.StreamEnded`; `_resync` re-raises it immediately and
  retries other errors `LIVE_RESYNC_ATTEMPTS` (5) times; stall threshold `LIVE_STALL_SECONDS`
  (45, was 90). The feeder records `end_reason` / `error` on the source (`outcome` property)
  instead of raising, because `DeepgramTranscriber.pump()` swallows source exceptions; `chunks()`
  and `close()` await the feeder so nothing is left unretrieved.
- **Daemon.** `speechalerts/daemon.py: WatchDaemon` (`cmd_watch` delegates). Long-lived sinks and
  web server; per-stream engine/pipeline. Handled-ids map with TTL `WATCH_IGNORE_ENDED_HOURS`;
  crash-while-live retries (`WATCH_ATTACH_RETRIES`, 10/30/60 s); status transitions mirrored to
  the web page and Firestore. `cli.py` now exposes `build_sinks()` / `run_pipeline()` / `Sinks`;
  `SqliteSink.end_run()`; `discovery.probe_channels()` with `ignore_ids`.
- **`sinks/firebase.py: FirebaseSink`.** One worker task + `asyncio.to_thread` per write;
  `alerts/{id}`, `streams/{video_id}`, `status/current`; FCM topic pushes with factual wording.
  Alerts are snapshotted (`to_dict()`) at emit time because the engine mutates a heads-up's
  `state` in place on confirmation (first replay wrote heads-ups as "confirmed").
- launchd plist: `uv run --frozen`, `GRPC_ENABLE_FORK_SUPPORT=0`.
- Tests: 72 (`test_daemon.py`, `test_firebase_sink.py`, pinning/end-of-stream cases).

### Verified
- Replay of `synthetic_intel_speech` with Firebase on: 23 dry-run pushes, docs in the console.
- Admin-SDK smoke test against the real project: write, dry-run send, read back, delete.

### Open
- Install the plist and let it run through a real scheduled event; check `WATCH_TITLE_PATTERNS`.
- Firestore has no TTL/cleanup; add one before a real client reads the feed.
- Pushes per heads-up can be noisy on long Q&As; `FCM` states are one setting away from
  "confirmed only" if needed.

## 14. Day 4 (2026-10-02): watcher installed, hosted feed page

- The day-3 daemon had never been installed; nothing ran between the 2026-10-01 smoke test and
  today. `.env` now sets `WATCH_CHANNELS` (WhiteHouse, cspan, FoxNews, RSBN, LiveNOWfromFOX,
  ForbesBreakingNews) and rally-friendly `WATCH_TITLE_PATTERNS`. The launchd job
  `com.speechalerts.watch` is loaded and wrapped in `caffeinate -i` (idle sleep only; a closed
  lid still stops it). Log: `logs/watch.log`.
- Firebase Hosting page at https://<your-site>.web.app (see `firebase/README.md`): status,
  schedule (viewer-local and venue times), alerts tail, per-stream verbatim quotes.
  `data/schedule.yaml` + `scripts/push_schedule.py` feed the `events` collection by hand.
- Known rallies: Mobile AL 2026-10-02 18:00 CT, Vandalia OH 2026-10-03 17:30 ET; more Ohio,
  Iowa, Nebraska dates expected in October (not yet on file).
- Open: confirm a rally title actually matches the patterns tonight; the hosted page was
  checked on desktop only; no Firestore TTL yet; `FCM_DRY_RUN=1` still on.
- 2026-10-05 evening (Grand Island, NE rally, the first real rally the daemon caught): the Mac
  had been in clamshell sleep since 15 min after the Friday install, so Mobile and Vandalia were
  missed; `caffeinate -i` does not stop lid-close sleep (`sudo pmset -a disablesleep 1` does).
  User asked for the full transcript on the page: `FirebaseSink.segment` now writes finals to
  `streams/{id}/segments` (`FIREBASE_TRANSCRIPTS`, default on), page is two panes (scrollback
  left, transcript right, stacked under 1000px). `scripts/backfill_transcript.py` copies a
  SQLite run into Firestore. A daemon restart mid-rally re-attached to Fox's stream of the same
  speech (per-process handled ids), so one speech can span two `streams` docs.
- 2026-10-05 later: live watch of the Grand Island speech (`strategy/live_watch.py`: transcript +
  alerts from SQLite, 14 futures contracts from Yahoo 1m bars with ~10 min delay, events for a
  monitor; `strategy/live_check.py` for after-hours/next-open stock comparison). No futures
  contract moved >0.3% during the speech; stocks had 15 min of empty after-hours tape. The Mac
  slept again 20:41–21:31 and ~21:33–22:36 (lid open, battery <10%, "Sleep Service" cycles).
  **Bug found:** after waking, `YoutubeLiveSource` on the ended Fox stream kept pulling from the
  DVR start and re-alerted 19:47 content at 22:37 (6 duplicate alerts + 28 segments deleted from
  Firestore by hand). Resync must raise `StreamEnded` when `live_status` is `was_live`/`post_live`
  after a resume, and the puller should not restart at the playlist head. Missed minutes were
  recovered with `replay <RSBN url> --from 7:48:00 --to 8:03:56 --speed 0 --no-web` and
  `scripts/backfill_transcript.py --wall-from-release`. RSBN's VOD stays up as "LIVE REPLAY".
