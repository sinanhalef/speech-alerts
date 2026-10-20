# strategy/ — do the President's stock mentions move prices?

Offline backtest of the `speechalerts` signal pipeline against market prices. Separate uv project;
it imports the live package read-only and never writes to `data/alerts.sqlite3`.

## Pipeline

```
videos.yaml ─ fetch ─▶ data/audio/<id>.ogg + data/transcripts/<id>.meta.json   (yt-dlp + ffmpeg, original-language track)
             transcribe ─▶ data/transcripts/<id>.txt / .json                     (Deepgram pre-recorded nova-3, diarized)
             extract ─▶ data/signals/<id>.json                                   (live Dictionary + Confirmer, replayed on audio time)
             judge ─▶ adds `judge` to each confirmed signal                     (Claude Sonnet 5: expected direction per ticker)
             measure ─▶ data/results/measurements.csv                           (Yahoo prices, SPY-adjusted, 10 horizons)
             report ─▶ data/results/summary.md + summary.json
             analyze ─▶ data/results/analysis.md + analysis.json           (alert volume, filter ladder, per-entity / per-action tables)
             portfolio ─▶ data/results/portfolio.md + portfolio.json       ($10k account: buy positive mentions, sell 5 sessions later)
```

## Run

```bash
cd strategy
uv sync                                   # own .venv; keys come from ../.env via the speechalerts package
uv run pytest                             # unit tests, no network
uv run backtest discover --days 75        # list recent White House livestreams -> data/candidates.json
uv run backtest run-all                   # everything for every video in videos.yaml (idempotent)
uv run backtest run-all --video <id>      # one video
uv run backtest extract --force --video <id>   # redo one stage
uv run backtest measure && uv run backtest report && uv run backtest analyze && uv run backtest portfolio
```

Stages skip work whose outputs exist; `--force` redoes them. `--concurrency N` runs videos in
parallel for fetch/transcribe/extract/judge. `--no-llm` (extract) keeps dictionary heads-ups only.

## What is measured

Per confirmed signal and ticker: `open` (next session's opening print vs previous close; closed-market
mentions only), `+10m`, `+30m`, `+1h`, `+2h` (from the mention, or from the next 09:30 when the
market was closed), and closes on day 0, +1, +2, +5 (one week), +21 (one month). Baseline is the last
*completed* bar before the mention (no look-ahead) or the previous close. `abn_ret = ret − SPY ret`
over the identical window. Hit = sign of the abnormal return matches the expected direction.

Expected direction comes from two sources: the live app's stance (positive→up, negative→down) and a
Sonnet 5 judge that reads ±60 s of transcript and states direction, confidence, novelty
(new announcement vs repeated rhetoric) and may add up to two related tickers.

Yahoo limits: 1-minute bars ≈ last 30 days, 5-minute ≈ 60 days, hourly ≈ 2 years. Intraday horizons
use the finest interval no coarser than the horizon, so `+10m`/`+30m` are blank for 2025 events.

## Product analysis

`analyze` answers "which alerts are worth sending?": alerts per hour, tickers per alert, share of repeated
rhetoric, and a *filter ladder* that applies candidate rules (entity kind, action label, confidence, single
ticker vs basket, judge novelty, ...) and reports how many alerts each keeps and the sign-adjusted abnormal
return at +10m, +1h, day +1, +2 and +5. Section 3 repeats the key filters per video group (recent, headline,
expansion) as a consistency check; section 4 lists the entities that fire most and how they moved.
Conclusions drawn from it live in `FINDINGS.md`.

`portfolio` simulates a $10,000 account that buys the primary ticker of every positively labelled signal
(first mention per video) and sells at the close five sessions later, with two entry rules (at the mention
price, or at the next market open) and three selections (stance positive, judge up, judge up + new). Open
positions share the equity with daily equal-weight rebalancing; the naive "equal split" column puts
$10k / N into each trade independently.

## Files worth keeping

- `data/transcripts/<id>.txt` — `t<TAB>text` per utterance; replayable through the live pipeline from
  the repo root: `uv run python -m speechalerts replay --transcript strategy/data/transcripts/<id>.txt --speed 8`
  (that writes to the shared alerts DB, so it is not part of this batch).
- `data/transcripts/<id>.json` — utterances with speaker labels, confidence and word timings.
- `data/signals/<id>.json` — every heads-up with its confirmation/retraction, the context the model
  saw, and the judge's verdict.
- `data/results/measurements.csv` — one row per signal × ticker × horizon.

Wall-clock mapping: recorded livestreams give `release_timestamp`; `t_wall = release_timestamp + t_audio`.
Plain uploads need `event_start` in `videos.yaml`.

Costs (approx.): Deepgram pre-recorded $0.0043/min of audio; Haiku ≈ $0.003 per confirmation;
Sonnet 5 ≈ $0.01–0.02 per judged signal.
