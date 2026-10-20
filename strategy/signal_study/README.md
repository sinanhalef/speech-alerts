# signal_study — which the President statements move stocks, and how to classify them live

Read-only study on top of the `strategy/` backtest data (78 videos, 74.5 h of speech, Jan 2025 – Sep 2026;
1,534 confirmed mentions with Haiku labels and a Sonnet judge; Yahoo prices). Nothing here writes to
`strategy/data/` or touches the live `speechalerts` package.

Deliverables:

- `FINDINGS.md` — the study: base rates, the movers case by case, what they have in common, what never moves,
  direction rules, the rule backtest, caveats.
- `SYSTEM_PROMPT.md` — the system prompt for a live classifier, with the output schema and worked examples
  drawn from the corpus.

Scripts (run from `strategy/` with its venv; each writes to `signal_study/out/`):

```bash
cd strategy
.venv/bin/python signal_study/01_events.py     # per-video: did SPY / QQQ / TLT / sector ETFs move? -> out/events.md, events.csv
.venv/bin/python signal_study/02_movers.py     # every (signal, ticker) z-scored on its own abnormal vol -> out/mentions_z.csv, movers.md
.venv/bin/python signal_study/03_direction.py  # unique movers + pre-move, direction calibration, relief rallies, sectors, in-session 10-min -> out/direction.md
.venv/bin/python signal_study/04_contexts.py   # ±75 s speaker-tagged transcript around movers and duds -> out/contexts_movers.md, contexts_duds.md
.venv/bin/python signal_study/05_sagas.py      # repeated themes over time (pharma, chips, steel, China, oil, ...) -> out/sagas.md
.venv/bin/python signal_study/06_rules.py      # backtest of the decision rules used in SYSTEM_PROMPT.md -> out/rules.md
```

`02` must run before `03`–`06` (they read `out/mentions_z.csv`). `common.py` holds the loaders.

Definitions used throughout:

- **first reaction**: the opening gap of the next session when the market was closed at the remark, else the move
  from the last completed bar before the remark to +1 h (fallback +2 h, close).
- **z**: abnormal return (ticker − SPY) divided by the ticker's own standard deviation of daily abnormal returns
  over the 60 sessions before the event. A 5 % move in a coal miner and a 1 % move in Apple can both be ~1σ.
- **mover**: |z| ≥ 2 at the first reaction. **right / wrong**: moved ≥ 1σ with / against the expected direction
  (Sonnet judge direction, live stance as fallback).
