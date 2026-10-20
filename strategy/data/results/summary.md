# Do the President's stock mentions move prices? Backtest of the speechalerts signals

_Generated 2026-09-15 12:30 EDT._

## Headline

We analysed **78 videos** (74.5 h of audio). The live algorithm (dictionary + Claude Haiku confirmation, replayed offline) raised **2178 heads-ups**, confirmed **1534 signals** and retracted 644.

Of the 1534 confirmed signals, the live app's stance labels 914 as positive (expected up), 370 negative (expected down) and 250 neutral. The Sonnet 5 judge (1534 judged) expects the primary ticker to go up in 492, down in 203 and sees no price relevance in 837.

918 signals had a measurable primary ticker (first mention of that ticker in the video; US-listed with Yahoo data). Returns below are **abnormal** = ticker return minus SPY return over the same window, measured from the last completed bar before the mention (market open) or the previous close (market closed).

## Judge (Sonnet 5) expectation

### Expected UP (first mentions, primary ticker)

| horizon | n | hit rate | mean abn | median abn | mean raw | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 108 | 55% | +0.61% | +0.09% | +0.60% | 0.39 |
| +10m | 55 | 67% | -0.05% | +0.03% | -0.15% | 0.01 |
| +30m | 49 | 43% | -0.08% | -0.03% | -0.14% | 0.39 |
| +1h | 203 | 49% | +0.21% | +0.00% | +0.16% | 0.89 |
| +2h | 169 | 51% | +0.22% | +0.03% | +0.16% | 0.76 |
| close_d0 | 245 | 53% | +0.17% | +0.05% | +0.12% | 0.44 |
| close_d1 | 245 | 50% | +0.35% | +0.00% | +0.22% | 1.00 |
| close_d2 | 238 | 52% | +0.38% | +0.15% | +0.40% | 0.65 |
| close_d5 | 235 | 45% | -0.01% | -0.41% | +0.27% | 0.12 |
| close_d21 | 210 | 50% | +0.58% | +0.00% | +2.23% | 0.95 |

### Expected DOWN (first mentions, primary ticker)

| horizon | n | hit rate | mean abn | median abn | mean raw | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 53 | 38% | +0.38% | +0.33% | -0.48% | 0.10 |
| +10m | 31 | 61% | +0.01% | -0.02% | +0.01% | 0.28 |
| +30m | 28 | 54% | -0.09% | -0.01% | -0.04% | 0.85 |
| +1h | 111 | 50% | +0.26% | +0.01% | -0.15% | 1.00 |
| +2h | 97 | 47% | +0.29% | +0.02% | -0.23% | 0.68 |
| close_d0 | 138 | 49% | +0.26% | +0.00% | -0.11% | 0.93 |
| close_d1 | 138 | 49% | +0.14% | +0.10% | -0.79% | 0.80 |
| close_d2 | 138 | 53% | -0.01% | -0.11% | -0.71% | 0.55 |
| close_d5 | 137 | 44% | -0.07% | +0.26% | -0.30% | 0.17 |
| close_d21 | 126 | 40% | +1.25% | +1.39% | +2.28% | 0.03 |

### Directional (long expected-up, short expected-down; sign-adjusted abnormal return)

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 161 | 49% | +0.28% | -0.00% | 1.79 | 0.87 |
| +10m | 86 | 65% | -0.03% | +0.03% | -0.35 | 0.01 |
| +30m | 77 | 47% | -0.02% | -0.00% | -0.20 | 0.65 |
| +1h | 314 | 49% | +0.04% | +0.00% | 0.40 | 0.87 |
| +2h | 266 | 50% | +0.03% | +0.00% | 0.27 | 1.00 |
| close_d0 | 383 | 51% | +0.02% | +0.02% | 0.18 | 0.61 |
| close_d1 | 383 | 49% | +0.17% | -0.00% | 1.20 | 0.84 |
| close_d2 | 376 | 52% | +0.25% | +0.13% | 1.33 | 0.44 |
| close_d5 | 372 | 44% | +0.02% | -0.30% | 0.06 | 0.03 |
| close_d21 | 336 | 46% | -0.11% | -0.46% | -0.20 | 0.14 |

### Expected NONE (control: judged not price-relevant)

| horizon | n | hit rate | mean abn | median abn | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|
| open | 209 | n/a | +0.21% | +0.00% | n/a |
| +10m | 95 | n/a | -0.13% | -0.02% | n/a |
| +30m | 88 | n/a | -0.10% | -0.04% | n/a |
| +1h | 434 | n/a | +0.12% | +0.00% | n/a |
| +2h | 370 | n/a | +0.19% | +0.03% | n/a |
| close_d0 | 535 | n/a | +0.10% | +0.00% | n/a |
| close_d1 | 535 | n/a | +0.04% | +0.00% | n/a |
| close_d2 | 531 | n/a | -0.01% | +0.00% | n/a |
| close_d5 | 531 | n/a | +0.15% | +0.00% | n/a |
| close_d21 | 485 | n/a | +0.39% | +0.00% | n/a |

## Stance baseline (what the live app shows today)

### Expected UP (first mentions, primary ticker)

| horizon | n | hit rate | mean abn | median abn | mean raw | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 228 | 52% | +0.49% | +0.06% | +0.36% | 0.55 |
| +10m | 105 | 50% | -0.07% | +0.00% | -0.15% | 1.00 |
| +30m | 96 | 35% | -0.11% | -0.02% | -0.18% | 0.01 |
| +1h | 432 | 49% | +0.22% | +0.00% | +0.12% | 0.67 |
| +2h | 372 | 51% | +0.26% | +0.01% | +0.11% | 0.64 |
| close_d0 | 517 | 49% | +0.18% | +0.00% | +0.04% | 0.60 |
| close_d1 | 517 | 45% | +0.23% | +0.00% | -0.06% | 0.02 |
| close_d2 | 506 | 48% | +0.19% | +0.00% | +0.08% | 0.35 |
| close_d5 | 503 | 44% | +0.01% | +0.00% | +0.28% | 0.01 |
| close_d21 | 460 | 47% | +0.59% | +0.00% | +2.15% | 0.24 |

### Expected DOWN (first mentions, primary ticker)

| horizon | n | hit rate | mean abn | median abn | mean raw | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 94 | 48% | +0.15% | +0.03% | -0.32% | 0.76 |
| +10m | 49 | 67% | -0.16% | -0.02% | -0.17% | 0.02 |
| +30m | 46 | 59% | -0.16% | -0.02% | -0.15% | 0.30 |
| +1h | 202 | 51% | +0.13% | -0.01% | -0.05% | 0.83 |
| +2h | 170 | 46% | +0.16% | +0.02% | -0.09% | 0.40 |
| close_d0 | 254 | 51% | +0.09% | -0.02% | -0.06% | 0.85 |
| close_d1 | 254 | 49% | +0.08% | +0.10% | -0.22% | 0.75 |
| close_d2 | 254 | 54% | -0.08% | -0.17% | -0.20% | 0.23 |
| close_d5 | 253 | 47% | +0.20% | +0.22% | +0.37% | 0.45 |
| close_d21 | 235 | 46% | +0.52% | +0.52% | +1.73% | 0.24 |

### Directional (long expected-up, short expected-down; sign-adjusted abnormal return)

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 322 | 51% | +0.30% | +0.04% | 3.05 | 0.78 |
| +10m | 154 | 55% | +0.01% | +0.02% | 0.08 | 0.23 |
| +30m | 142 | 43% | -0.02% | -0.00% | -0.39 | 0.11 |
| +1h | 634 | 50% | +0.11% | +0.00% | 1.86 | 0.84 |
| +2h | 542 | 50% | +0.13% | +0.00% | 1.80 | 0.97 |
| close_d0 | 771 | 49% | +0.09% | +0.00% | 1.55 | 0.77 |
| close_d1 | 771 | 46% | +0.13% | +0.00% | 1.29 | 0.04 |
| close_d2 | 760 | 50% | +0.15% | +0.00% | 1.22 | 0.97 |
| close_d5 | 756 | 45% | -0.06% | +0.00% | -0.33 | 0.01 |
| close_d21 | 695 | 47% | +0.21% | +0.00% | 0.53 | 0.10 |

### Expected NONE (control: judged not price-relevant)

| horizon | n | hit rate | mean abn | median abn | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|
| open | 48 | n/a | +0.09% | -0.12% | n/a |
| +10m | 27 | n/a | +0.03% | -0.01% | n/a |
| +30m | 23 | n/a | +0.11% | -0.04% | n/a |
| +1h | 114 | n/a | -0.01% | -0.02% | n/a |
| +2h | 94 | n/a | +0.11% | +0.08% | n/a |
| close_d0 | 147 | n/a | +0.10% | +0.07% | n/a |
| close_d1 | 147 | n/a | -0.09% | +0.04% | n/a |
| close_d2 | 147 | n/a | +0.02% | -0.06% | n/a |
| close_d5 | 147 | n/a | +0.06% | -0.07% | n/a |
| close_d21 | 126 | n/a | +0.60% | +0.13% | n/a |

## Splits (judge expectation, directional, sign-adjusted abnormal return)

### market open at mention

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 0 | n/a | n/a | n/a | n/a | n/a |
| +10m | 72 | 68% | +0.02% | +0.03% | 0.99 | 0.00 |
| +30m | 63 | 48% | +0.00% | -0.00% | 0.07 | 0.80 |
| +1h | 154 | 49% | -0.08% | +0.00% | -1.86 | 0.94 |
| +2h | 106 | 49% | -0.11% | -0.01% | -1.30 | 0.92 |
| close_d0 | 222 | 54% | -0.06% | +0.03% | -1.16 | 0.31 |
| close_d1 | 222 | 48% | +0.17% | -0.02% | 1.03 | 0.64 |
| close_d2 | 222 | 51% | +0.29% | +0.08% | 1.28 | 0.74 |
| close_d5 | 218 | 44% | -0.10% | -0.31% | -0.27 | 0.07 |
| close_d21 | 182 | 45% | -0.05% | -0.48% | -0.07 | 0.16 |

### market closed at mention

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 161 | 49% | +0.28% | -0.00% | 1.79 | 0.87 |
| +10m | 14 | 50% | -0.31% | -0.03% | -0.51 | 1.00 |
| +30m | 14 | 43% | -0.10% | -0.32% | -0.25 | 0.79 |
| +1h | 160 | 49% | +0.15% | -0.00% | 0.81 | 0.94 |
| +2h | 160 | 51% | +0.13% | +0.01% | 0.66 | 0.94 |
| close_d0 | 161 | 48% | +0.12% | -0.05% | 0.57 | 0.75 |
| close_d1 | 161 | 51% | +0.17% | +0.03% | 0.68 | 0.87 |
| close_d2 | 154 | 53% | +0.17% | +0.15% | 0.57 | 0.47 |
| close_d5 | 154 | 45% | +0.18% | -0.27% | 0.44 | 0.29 |
| close_d21 | 154 | 47% | -0.17% | -0.34% | -0.23 | 0.57 |

### recent videos (minute data)

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 0 | n/a | n/a | n/a | n/a | n/a |
| +10m | 51 | 69% | +0.02% | +0.03% | 0.76 | 0.01 |
| +30m | 43 | 47% | +0.00% | -0.00% | 0.05 | 0.76 |
| +1h | 26 | 62% | +0.02% | +0.02% | 0.34 | 0.33 |
| +2h | 2 | 50% | +0.08% | +0.08% | 0.42 | 1.00 |
| close_d0 | 53 | 62% | -0.02% | +0.05% | -0.23 | 0.10 |
| close_d1 | 53 | 64% | +1.10% | +0.84% | 3.27 | 0.05 |
| close_d2 | 53 | 62% | +1.55% | +0.74% | 2.60 | 0.10 |
| close_d5 | 49 | 59% | +1.27% | +0.54% | 1.62 | 0.25 |
| close_d21 | 16 | 50% | +1.32% | +0.00% | 0.58 | 1.00 |

### 2025 headline videos

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 43 | 49% | +0.59% | -0.02% | 1.13 | 1.00 |
| +10m | 0 | n/a | n/a | n/a | n/a | n/a |
| +30m | 0 | n/a | n/a | n/a | n/a | n/a |
| +1h | 72 | 46% | +0.13% | -0.04% | 0.40 | 0.56 |
| +2h | 68 | 49% | +0.02% | -0.01% | 0.05 | 0.90 |
| close_d0 | 77 | 53% | +0.14% | +0.08% | 0.42 | 0.65 |
| close_d1 | 77 | 49% | +0.12% | -0.01% | 0.30 | 1.00 |
| close_d2 | 77 | 51% | +0.46% | +0.14% | 1.14 | 1.00 |
| close_d5 | 77 | 43% | -0.35% | -0.55% | -0.73 | 0.25 |
| close_d21 | 77 | 45% | +0.16% | -0.89% | 0.17 | 0.49 |

### expansion videos (White House, Jun 2025 - Sep 2026)

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 118 | 49% | +0.17% | -0.00% | 1.68 | 0.93 |
| +10m | 32 | 56% | -0.12% | +0.02% | -0.48 | 0.60 |
| +30m | 31 | 45% | -0.04% | -0.05% | -0.25 | 0.72 |
| +1h | 213 | 50% | +0.01% | +0.00% | 0.15 | 1.00 |
| +2h | 193 | 51% | +0.04% | +0.03% | 0.37 | 0.77 |
| close_d0 | 250 | 49% | -0.01% | -0.01% | -0.15 | 0.75 |
| close_d1 | 250 | 46% | -0.00% | -0.13% | -0.02 | 0.23 |
| close_d2 | 243 | 50% | -0.10% | +0.01% | -0.49 | 1.00 |
| close_d5 | 243 | 42% | -0.12% | -0.40% | -0.36 | 0.01 |
| close_d21 | 243 | 46% | -0.29% | -0.37% | -0.45 | 0.20 |

### novelty = new

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 18 | 61% | +1.32% | +0.32% | 1.40 | 0.48 |
| +10m | 11 | 73% | +0.01% | +0.03% | 0.38 | 0.23 |
| +30m | 10 | 50% | +0.07% | -0.02% | 0.51 | 1.00 |
| +1h | 39 | 51% | +0.35% | +0.00% | 0.91 | 1.00 |
| +2h | 32 | 59% | +0.49% | +0.16% | 1.13 | 0.38 |
| close_d0 | 52 | 58% | +0.38% | +0.06% | 1.20 | 0.33 |
| close_d1 | 52 | 50% | +0.50% | -0.12% | 1.21 | 1.00 |
| close_d2 | 52 | 46% | +0.14% | -0.56% | 0.30 | 0.68 |
| close_d5 | 52 | 52% | -0.15% | +0.31% | -0.21 | 0.89 |
| close_d21 | 46 | 46% | +0.92% | -0.41% | 0.71 | 0.66 |

### novelty = repeat

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 115 | 49% | +0.19% | -0.00% | 1.22 | 0.85 |
| +10m | 53 | 62% | -0.07% | +0.03% | -0.44 | 0.10 |
| +30m | 49 | 45% | -0.07% | -0.03% | -0.65 | 0.57 |
| +1h | 220 | 48% | -0.06% | -0.01% | -0.48 | 0.54 |
| +2h | 192 | 46% | -0.08% | -0.06% | -0.59 | 0.28 |
| close_d0 | 261 | 49% | -0.12% | -0.00% | -1.08 | 0.80 |
| close_d1 | 261 | 47% | +0.04% | -0.08% | 0.24 | 0.32 |
| close_d2 | 254 | 52% | +0.23% | +0.11% | 1.01 | 0.57 |
| close_d5 | 252 | 42% | -0.00% | -0.51% | -0.00 | 0.01 |
| close_d21 | 233 | 47% | -0.09% | -0.22% | -0.14 | 0.43 |

### judge confidence >= 0.65

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 13 | 69% | +2.33% | +0.34% | 2.06 | 0.27 |
| +10m | 2 | 100% | +0.11% | +0.11% | 3.34 | 0.50 |
| +30m | 2 | 50% | -0.69% | -0.69% | -0.78 | 1.00 |
| +1h | 17 | 53% | +1.11% | +0.02% | 1.41 | 1.00 |
| +2h | 17 | 65% | +0.82% | +0.23% | 1.08 | 0.33 |
| close_d0 | 20 | 55% | +0.71% | +0.08% | 0.89 | 0.82 |
| close_d1 | 20 | 60% | +1.33% | +0.51% | 1.53 | 0.50 |
| close_d2 | 20 | 70% | +1.53% | +0.52% | 1.90 | 0.12 |
| close_d5 | 20 | 45% | +0.95% | -0.71% | 0.64 | 0.82 |
| close_d21 | 20 | 35% | -2.83% | -2.27% | -1.24 | 0.26 |

### main speaker only

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 159 | 48% | +0.26% | -0.02% | 1.61 | 0.75 |
| +10m | 75 | 64% | -0.05% | +0.03% | -0.45 | 0.02 |
| +30m | 68 | 49% | -0.03% | -0.00% | -0.31 | 0.90 |
| +1h | 296 | 49% | +0.01% | -0.01% | 0.12 | 0.77 |
| +2h | 253 | 49% | +0.01% | +0.00% | 0.06 | 0.90 |
| close_d0 | 355 | 51% | -0.01% | +0.01% | -0.10 | 0.83 |
| close_d1 | 355 | 50% | +0.14% | +0.00% | 0.96 | 0.92 |
| close_d2 | 348 | 53% | +0.24% | +0.14% | 1.25 | 0.36 |
| close_d5 | 344 | 44% | -0.05% | -0.32% | -0.16 | 0.02 |
| close_d21 | 312 | 45% | -0.24% | -0.48% | -0.45 | 0.10 |

### all tickers, all mentions (not just first/primary)

| horizon | n | hit rate | mean adj | median adj | t-stat | p (hit≠50%) |
|---|---:|---:|---:|---:|---:|---:|
| open | 723 | 52% | +0.35% | +0.06% | 2.90 | 0.23 |
| +10m | 337 | 50% | -0.05% | +0.00% | -1.33 | 0.91 |
| +30m | 299 | 43% | -0.09% | -0.04% | -2.19 | 0.03 |
| +1h | 1415 | 52% | +0.06% | +0.02% | 0.83 | 0.22 |
| +2h | 1209 | 53% | +0.03% | +0.06% | 0.32 | 0.07 |
| close_d0 | 1791 | 51% | +0.03% | +0.02% | 0.47 | 0.26 |
| close_d1 | 1791 | 51% | +0.24% | +0.05% | 2.84 | 0.45 |
| close_d2 | 1772 | 53% | +0.35% | +0.19% | 3.13 | 0.01 |
| close_d5 | 1768 | 47% | -0.01% | -0.26% | -0.06 | 0.01 |
| close_d21 | 1612 | 47% | -0.44% | -0.51% | -1.44 | 0.01 |

## Per-video signals

### Steel Across America event — `TBoLSAlhCDE`
_the President Participates in a Steel Across America Event (The White House); stream start 2026-09-08 10:21 ET; 28 min; 6 heads-ups / 3 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 10:23 | U.S. Steel | X, NUE, CLF, STLD | neutral | none (0.55) | repeat | United States Steel Building was creaking, really creaking | · | · | · | · |
| 11:03 | Steel | X, NUE, CLF, STLD | neutral | none (0.50) | repeat | U.S. Steel. The 16,000 pound beam lifted from the records of the South | · | · | · | · |
| 12:38 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | We have the highest stock market that we've ever had. | · | +0.00% | +0.00% | +0.00% |

### Signs executive orders, Sep 4 2026 — `xHSKMevaFIc`
_the President Signs Executive Orders, Sep. 4, 2026 (The White House); stream start 2026-09-04 14:03 ET; 50 min; 22 heads-ups / 14 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:18 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | very important meeting with a great group of farmers and ranchers | · | -0.18% | +1.13% | +1.20% |
| 11:22 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | unclear | farmers are processing their food, authorizing ranches to protect rura | · | -0.07% | +1.22% | +1.30% |
| 25:21 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | When we have great numbers, the stock market should go up. | · | +0.00% | +0.00% | +0.00% |
| 29:52 | Iran | XLE, USO, ITA | negative | up (0.55) | repeat | We stopped Iran from having | · | -0.04% | +1.60% | +1.88% |
| 29:59 | Russia | RSX, XLE | neutral | none (0.50) | repeat | Under your watch that Putin would never attack NATO territory. | · | · | · | · |
| 30:01 | Germany | EWG | neutral | none (0.55) | unclear | Germany is blaming Russia for an explosive drone found at a German air | · | +0.00% | -0.14% | -1.44% |
| 31:03 | Switzerland | EWL | negative | down (0.60) | unclear | We have the right to put tariffs on them, we have a right not to trade | · | -0.01% | -1.74% | -2.84% |
| 32:39 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | we should be paying the lowest interest rate in the world | · | -0.06% | +0.43% | -0.45% |
| 36:20 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | We lose with the European Union $200,000,000,000 | · | +0.07% | +0.06% | -1.42% |
| 42:51 | Argentina | ARGT | neutral | none (0.52) | repeat | It's coming from Argentina. It's coming from Brazil. | · | +0.11% | +0.27% | +0.40% |
| 43:18 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | ranchers are building up their herds | · | -0.01% | +1.36% | +1.43% |
| 43:29 | Brazil | EWZ | neutral | up (0.55) | unclear | primarily Argentina and Brazil, but there could be other countries | · | -0.13% | +2.45% | +0.76% |
| 46:58 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | you're gonna want a data center | · | -0.06% | -1.50% | -7.25% |
| 47:25 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | lot of places that want them, both in this country and in particular i | · | +0.22% | -1.65% | -1.44% |

### Meets with U.S. travel executives — `6QYMxVMrjrM`
_the President Meets with U.S. Travel Executives (The White House); stream start 2026-09-02 13:44 ET; 51 min; 35 heads-ups / 26 confirmed / 9 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:40 | American Airlines | AAL | positive | up (0.55) | repeat | executives from great companies like American Airlines | · | +0.77% | -1.79% | -0.70% |
| 10:43 | Airlines | JETS, DAL, UAL, AAL | positive | up (0.55) | repeat | got 12,500,000,000 for air traffic control | · | +0.06% | -0.98% | -1.02% |
| 14:33 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | investment cycle that is simply breathtaking, both AI | · | -0.10% | +0.64% | -1.84% |
| 17:53 | Honda | HMC | positive | up (0.55) | unclear | Honda just announced they're coming in with a big one. Monster. Big. | · | -0.04% | +0.95% | -1.43% |
| 17:57 | Automakers | GM, F, STLA, TSLA | positive | none (0.50) | repeat | many car companies that are coming in from Canada | · | -0.47% | +1.50% | +2.22% |
| 17:59 | Canada | EWC | negative | down (0.55) | repeat | they took them from us, and now we're getting them back | · | -0.08% | +1.22% | -0.35% |
| 18:10 | South Korea | EWY | neutral | none (0.50) | repeat | they're coming in from South Korea | · | -0.08% | +0.07% | +3.32% |
| 18:13 | Japan | EWJ | neutral | none (0.52) | repeat | coming in from Japan | · | -0.03% | +1.05% | +1.53% |
| 18:14 | Germany | EWG | neutral | none (0.55) | repeat | coming in from Germany | · | -0.04% | +0.03% | -0.96% |
| 18:18 | China | FXI, MCHI, KWEB | positive | up (0.55) | new | president of China coming on the 24th, very productive things to discu | · | +0.04% | -1.58% | -2.36% |
| 19:03 | Eli Lilly | LLY | positive | up (0.55) | repeat | Eli Lilly announced they're building 5 major | · | +0.03% | -1.34% | -2.48% |
| 19:16 | Merck | MRK | positive | up (0.55) | repeat | Merck, Pfizer, they're coming here | · | +0.36% | -0.08% | -3.13% |
| 19:16 | Pfizer | PFE | positive | none (0.55) | repeat | Merck, Pfizer, they're coming here | · | +0.38% | -1.44% | -3.44% |
| 25:00 | Agriculture | DBA, MOS, DE, ADM | negative | none (0.52) | repeat | They charge tremendous tariffs to our farmers. | · | -0.08% | -1.70% | +1.09% |
| 25:05 | Airlines | JETS, DAL, UAL, AAL | negative | none (0.50) | repeat | They take advantage of airlines. | · | +0.11% | -0.91% | -0.95% |
| 25:14 | Banks | XLF, KRE, JPM, BAC | negative | none (0.50) | repeat | Canada has all of its major banks here, biggest source of income | · | -0.02% | +0.47% | -0.45% |
| 28:24 | Canada | EWC | negative | down (0.60) | repeat | You build a car in Canada, you have to pay a 25% tariff | · | -0.02% | +1.26% | -0.31% |
| 28:46 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | we have more oil and gas than they do. We have tremendous | · | +0.16% | -1.82% | +0.66% |
| 28:51 | Lumber | WOOD, WY | negative | none (0.50) | repeat | We don't need their lumber. | · | -0.29% | -1.43% | -0.43% |
| 33:57 | Iran | XLE, USO, ITA | negative | up (0.55) | repeat | we can't let Iran have a nuclear weapon | · | +0.22% | -1.81% | +0.67% |
| 34:27 | Stock market | SPY, QQQ, DIA | positive | none (0.55) | repeat | stock market hits new records every day | · | +0.00% | +0.00% | +0.00% |
| 35:17 | Retailers | XRT | negative | none (0.52) | repeat | I want the retail prices. These were mostly retailers. | · | -0.28% | -1.14% | -2.70% |
| 37:18 | Russia | RSX, XLE | neutral | none (0.50) | repeat | tremendous numbers of soldiers, both Ukrainian and Russian, are being  | · | · | · | · |
| 38:05 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | we wanna have good relationship with Russia, Ukraine, with everybody | · | +0.13% | +0.13% | -1.30% |
| 39:10 | Film industry | DIS, NFLX, WBD, PSKY | neutral | up (0.52) | unclear | Canada gives tax incentives to take our film industry into their count | · | -0.12% | -2.37% | -1.60% |
| 39:33 | Netflix | NFLX | positive | none (0.55) | unclear | I've spoken to Netflix, who's fantastic | · | +0.08% | -0.60% | -6.68% |

### Healthcare affordability announcement, Aug 31 2026 — `uyeCoZ5Yego`
_the President Makes an Announcement on Healthcare Affordability, Aug. 31, 2026 (The White House); stream start 2026-08-31 15:02 ET; 58 min; 34 heads-ups / 22 confirmed / 12 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:48 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | new | most favored nation, drug pricing | · | · | +1.20% | -2.01% |
| 2:36 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | administrator of the Centers for Medicine and Medicaid Services | · | · | +2.47% | +3.10% |
| 6:31 | Novo Nordisk | NVO | positive | down (0.58) | repeat | slashed the cost of the weight loss drugs like Ozempic by more than $1 | · | · | -0.15% | -0.61% |
| 10:14 | Stellantis | STLA | positive | none (0.50) | unclear | I especially wanna thank UCB, Sun Pharma, Teva, and Stellantis for | · | · | -1.91% | -1.72% |
| 11:16 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | Drug prices went up every year. | · | · | +1.27% | -1.94% |
| 18:47 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.50) | repeat | $50 a month if you're eligible, get access to GLP 1 medications | · | · | +2.64% | +3.27% |
| 21:45 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | 638,000,000,000 of pharmaceutical investment in the country. | · | · | +1.21% | -2.00% |
| 34:09 | Eli Lilly | LLY | positive | up (0.58) | repeat | I wanna thank Eli Lilly | · | · | +0.53% | -3.12% |
| 34:10 | Pfizer | PFE | positive | up (0.55) | repeat | I wanna thank Eli Lilly and Pfizer | · | · | +0.21% | -2.98% |
| 34:10 | Merck | MRK | positive | up (0.55) | repeat | I wanna thank Eli Lilly and Pfizer, Merck | · | · | +1.54% | +0.06% |
| 35:11 | Health insurers | UNH, CI, ELV, HUM | negative | up (0.55) | repeat | Medicare for all paid by the government, by taxing higher earners. | · | · | +2.06% | +2.68% |
| 36:14 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | none (0.50) | repeat | broke down prices, and you get the level of care | · | · | +1.11% | -2.09% |
| 39:17 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | A lot of oil is coming out. That's why you haven't seen the price of o | · | · | +2.00% | +1.45% |
| 43:26 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | we should have the lowest interest rates anywhere | · | · | -0.04% | -0.19% |
| 47:33 | Pharmaceuticals | XLV, XPH, PFE, LLY | neutral | none (0.50) | repeat | drug companies had to agree | · | · | +1.12% | -2.08% |
| 50:40 | Oil | XLE, USO | positive | up (0.55) | unclear | taking out millions and millions of barrels of oil going to Houston | · | · | +2.11% | +1.56% |
| 50:55 | ExxonMobil | XOM | positive | up (0.60) | new | We have Exxon going in. | · | · | +3.19% | +0.22% |
| 50:57 | Chevron | CVX | positive | up (0.62) | unclear | We have Chevron going in. | · | · | +3.32% | +2.17% |
| 51:14 | Venezuela | XLE, CVX | positive | up (0.55) | unclear | it was also a very good deal for Venezuela | · | · | +2.11% | +1.56% |
| 51:34 | Refiners | VLO, MPC, PSX | positive | up (0.60) | new | our plants, our refineries are specifically | · | · | +1.24% | +6.49% |
| 51:40 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | We're gonna be taking all of that. We're gonna be taking that oil out. | · | · | +2.07% | +1.53% |
| 55:01 | Ukraine | ITA, XLE | negative | none (0.50) | repeat | You know where the money went was Ukraine. The money was really taken  | · | · | -0.57% | -1.96% |

### Remarks with technology leaders — `SDbFxr3HbHI`
_the President Delivers Remarks with Technology Leaders (The White House); stream start 2026-08-19 14:21 ET; 40 min; 50 heads-ups / 29 confirmed / 21 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:33 | Bitcoin | IBIT, COIN, MSTR | positive | up (0.55) | repeat | nation's brightest minds in finance, crypto, and technology | · | -0.02% | +7.37% | +15.34% |
| 1:24 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | We're leading in every aspect including AI | · | +0.34% | -0.05% | -3.79% |
| 2:16 | Blockchain / crypto industry | COIN, IBIT, MSTR, HOOD | positive | up (0.55) | repeat | All of the digital assets are all put into 1 | · | -1.49% | +8.53% | +13.97% |
| 2:22 | Coinbase | COIN | positive | up (0.55) | repeat | Many of the top industry leaders, including Coinbase | · | -1.49% | +8.53% | +13.97% |
| 2:37 | Intercontinental Exchange (NYSE) | ICE | positive | none (0.55) | repeat | He owns a thing called the New York Stock Exchange. Quite quite a nice | · | -0.90% | +1.17% | +2.81% |
| 2:49 | Nasdaq | NDAQ | neutral | none (0.55) | repeat | CEO of Nasdaq | · | -1.29% | +0.07% | +1.57% |
| 2:53 | Robinhood | HOOD | positive | none (0.52) | repeat | CEO of Robinhood, Vlad Tenev. | · | -0.28% | +0.32% | +13.92% |
| 2:59 | Kraken | COIN | positive | none (0.52) | repeat | CEO of Kraken | · | -1.49% | +8.53% | +13.97% |
| 3:24 | Ripple | COIN | neutral | up (0.55) | repeat | Brad Garlinghouse, co founder CEO of CTO and president of BitGo | · | -1.50% | +8.52% | +13.96% |
| 6:22 | Stablecoins | CRCL, COIN | positive | up (0.55) | repeat | I signed landmark legislation known as the Genius Act | · | -0.95% | +7.58% | +15.10% |
| 7:50 | Prediction markets | HOOD | positive | up (0.55) | repeat | creating a clear regulatory framework for pioneers and builders | · | +0.03% | +0.19% | +13.77% |
| 7:51 | Artificial intelligence / data centers | NVDA, MSFT, SMH, VRT | positive | up (0.55) | repeat | clear regulatory framework for pioneers and builders in AI | · | +0.33% | -0.09% | -3.82% |
| 8:46 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | We would really like to see interest rates come down. | · | +0.12% | +0.32% | +1.03% |
| 10:02 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market hit record highs 80 days in 1.5 years | · | +0.00% | +0.00% | +0.00% |
| 12:29 | Bitcoin | IBIT, COIN, MSTR | positive | none (0.50) | repeat | established a strategic Bitcoin reserve | · | -0.01% | +7.46% | +15.43% |
| 19:53 | Intercontinental Exchange (NYSE) | ICE | positive | none (0.55) | repeat | New York Stock Exchange was formed at the time of our country | · | -0.37% | +1.21% | +2.86% |
| 24:36 | Stablecoins | CRCL, COIN | positive | up (0.58) | repeat | stablecoin usage and adoption is increasing | · | -0.36% | +7.47% | +14.97% |
| 25:52 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | We're leading by a lot with AI. We wanna regulate, but regulation wher | · | -0.42% | -0.29% | -4.02% |
| 28:43 | Honda | HMC | positive | up (0.55) | repeat | Honda just announced. | · | +0.04% | +3.23% | -0.96% |
| 28:44 | Toyota | TM | positive | up (0.55) | unclear | Toyota just announced they're moving their operations. | · | -0.24% | +2.40% | +1.73% |
| 28:47 | Mexico | EWW | neutral | down (0.55) | repeat | moving their operations from Mexico, from Canada | · | -0.10% | +1.22% | +3.49% |
| 28:48 | Canada | EWC | positive | up (0.60) | new | We probably have a deal with Canada. | · | +0.19% | +0.94% | +1.23% |
| 31:03 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | we have very draconian sanctions | · | -0.21% | +1.06% | -1.47% |
| 31:55 | Oil | XLE, USO, XOM, CVX | neutral | none (0.52) | repeat | oil prices are gonna drop like a rock | · | -0.21% | +1.05% | -1.47% |
| 32:33 | Steel | X, NUE, CLF, STLD | neutral | down (0.55) | new | we're looking at that | · | · | · | · |
| 32:33 | Aluminum | AA, CENX | neutral | down (0.55) | new | we're looking at that | · | -0.23% | -0.12% | -2.20% |
| 32:38 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | unclear | farmers won't be paying any tariffs anymore | · | +0.10% | +1.18% | +1.47% |
| 34:57 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | Every time we do great, the interest rates go up. | · | +0.21% | +0.25% | +0.96% |
| 35:05 | Switzerland | EWL | positive | none (0.55) | repeat | countries like Switzerland where they're the number 1 lowest interest  | · | +0.36% | +0.07% | +0.31% |

### Roundtable on American mining — `V6VgPfBK8gQ`
_the President Hosts a Roundtable on American Mining (The White House); stream start 2026-08-07 15:01 ET; 36 min; 26 heads-ups / 19 confirmed / 7 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:42 | Rare earths | MP, REMX | positive | up (0.65) | repeat | Critical minerals are the raw materials of American strength | · | · | +4.01% | +11.35% |
| 5:01 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI plants, and so many other kinds of plants | · | · | -2.28% | +0.72% |
| 6:07 | Aluminum | AA, CENX | positive | up (0.55) | unclear | We've announced the construction of the 1st new aluminum smelter | · | · | +4.16% | +0.39% |
| 6:53 | Copper | COPX, FCX, SCCO | positive | up (0.60) | repeat | protecting American workers with historic tariffs on foreign copper | · | · | +1.60% | -3.16% |
| 6:54 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | protecting American workers with historic tariffs on foreign steel | · | · | · | · |
| 10:40 | Semiconductors | SMH, SOXX, NVDA, INTC | negative | none (0.50) | repeat | she wanted the miners of West Virginia to learn how to make chips | · | · | -2.22% | +0.51% |
| 11:12 | RTX (Raytheon) | RTX | positive | up (0.55) | new | making major grants to the Colorado School of Mines, the South Dakota  | · | · | +0.54% | -0.41% |
| 14:06 | MP Materials | MP | neutral | up (0.55) | repeat | CEO of MP Materials | · | · | +3.92% | +11.25% |
| 16:03 | Rare earths | MP, REMX | positive | up (0.62) | repeat | we have leaders from government, universities, private industry to sec | · | · | +3.92% | +11.25% |
| 18:45 | Anduril | PLTR | positive | none (0.50) | unclear | got Anduril Travnik here in the front row who's the assistant secretar | · | · | +2.67% | +1.55% |
| 21:18 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | Critical minerals national security issue. Advanced manufacturing, AI, | · | · | -2.10% | +0.64% |
| 21:49 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | section 2 32 tariffs, strengthened our steel, aluminum, copper industr | · | · | +0.03% | +0.43% |
| 21:52 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | repeat | section 2 32 tariffs, where we strengthened our steel | · | · | · | · |
| 21:52 | Aluminum | AA, CENX | positive | · | · | section 232 tariffs, where we strengthened our steel, our aluminum | · | · | +4.01% | +0.25% |
| 21:53 | Copper | COPX, FCX, SCCO | positive | up (0.55) | repeat | section 232 tariffs, where we strengthened our steel, our aluminum, an | · | · | +1.31% | -3.43% |
| 22:31 | South Korea | EWY | neutral | none (0.50) | unclear | chips program, we gave Korea zinc $7,400,000,000 | · | · | -1.68% | +7.92% |
| 33:40 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | clean, beautiful coal | · | · | +3.97% | +7.04% |
| 34:31 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | China is smart, and they're using coal. They're building 58 coal plant | · | · | +0.79% | -4.06% |
| 34:41 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.50) | repeat | They sell us wind turbines, but they don't use them. | · | · | -1.83% | -2.05% |

### Signs an executive order, Aug 10 2026 — `H_RititNE8U`
_the President Signs an Executive Order, Aug. 10, 2026 (The White House); stream start 2026-08-10 14:44 ET; 41 min; 20 heads-ups / 12 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:37 | Vaccine makers | PFE, MRNA, NVAX | negative | down (0.60) | new | America's recommended more childhood vaccines than any peer nation | · | +0.20% | -0.94% | -0.29% |
| 18:39 | Vaccine makers | PFE, MRNA, NVAX | negative | down (0.58) | unclear | change in the vaccines recommendations that the president has signed,  | · | · | -0.95% | -0.29% |
| 20:46 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | unclear | pressure from the pharmaceutical industry to pump your kids full of sh | · | · | +0.45% | -0.40% |
| 31:48 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | none (0.50) | repeat | pharmaceutical groups, I don't know | · | · | +0.40% | -0.44% |
| 33:19 | Toyota | TM | positive | up (0.55) | unclear | Toyota just announced that they're building the largest the largest ca | · | · | +1.15% | +0.54% |
| 33:31 | Mexico | EWW | negative | down (0.55) | repeat | They are leaving Mexico and they're coming to The United States. | · | · | -0.62% | -2.62% |
| 33:36 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI, other you know, they're they're opening. | · | · | -0.46% | +2.69% |
| 33:40 | Canada | EWC | negative | down (0.55) | repeat | They're leaving Canada. | · | · | +0.30% | +1.11% |
| 33:43 | Germany | EWG | negative | down (0.55) | repeat | They're leaving Germany. | · | · | +0.59% | +0.25% |
| 33:44 | Japan | EWJ | negative | down (0.55) | repeat | They're leaving Japan. | · | · | +0.51% | +2.20% |
| 33:45 | South Korea | EWY | negative | down (0.55) | repeat | They're leaving South Korea. | · | · | +2.37% | +12.99% |
| 38:39 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | unclear | It's a steel wall, infallible blockade. | · | · | · | · |

### Crypto executives event (Reuters), Aug 19 2026 — `K3_mcCs8Z8I`
_LIVE: The President speaks alongside crypto executives at the White House (Reuters); stream start 2026-08-19 14:49 ET; 56 min; 47 heads-ups / 31 confirmed / 16 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 14:08 | Bitcoin | IBIT, COIN, MSTR | positive | up (0.55) | repeat | We're delighted to welcome some of our nation's brightest minds in fin | · | · | +7.23% | +15.19% |
| 14:59 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | We're leading in every aspect including AI | · | · | -0.33% | -4.06% |
| 15:52 | Blockchain / crypto industry | COIN, IBIT, MSTR, HOOD | positive | up (0.55) | repeat | All of the digital assets are all put into 1. | · | · | +9.01% | +14.47% |
| 15:58 | Coinbase | COIN | positive | up (0.55) | repeat | including Coinbase | · | · | +9.01% | +14.47% |
| 16:12 | Intercontinental Exchange (NYSE) | ICE | positive | none (0.55) | repeat | He owns a thing called the New York Stock Exchange. Quite quite a nice | · | · | +1.17% | +2.81% |
| 16:24 | Nasdaq | NDAQ | positive | none (0.52) | repeat | CEO of Nasdaq, Adena Friedman. Thank you very much, Adena. Great job y | · | · | +0.31% | +1.81% |
| 16:29 | Robinhood | HOOD | positive | none (0.52) | repeat | CEO of Robinhood, Vlad Tenev. | · | · | +0.35% | +13.95% |
| 16:35 | Kraken | COIN | neutral | none (0.55) | repeat | CEO of Kraken | · | · | +8.85% | +14.30% |
| 17:01 | Ripple | COIN | neutral | none (0.52) | repeat | Brad Garlinghouse | · | · | +8.85% | +14.30% |
| 17:27 | Gemini | GEMI | neutral | none (0.50) | repeat | Peter Smith is here, and Tyler and Cameron Winklevoss | · | · | +8.72% | +18.69% |
| 20:01 | Stablecoins | CRCL, COIN | positive | up (0.55) | repeat | I signed landmark legislation known as the Genius Act. | · | · | +7.61% | +15.12% |
| 21:29 | Prediction markets | HOOD | positive | up (0.58) | repeat | creating a clear regulatory framework for pioneers and builders | · | · | -0.03% | +13.51% |
| 21:30 | Artificial intelligence / data centers | NVDA, MSFT, SMH, VRT | positive | up (0.55) | repeat | ensuring America remains undisputed leader in artificial intelligence | · | · | -0.28% | -4.01% |
| 22:26 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | We would really like to see interest rates come down. | · | · | +0.25% | +0.96% |
| 23:43 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market...creating jobs and great wealth | · | · | +0.00% | +0.00% |
| 26:12 | Bitcoin | IBIT, COIN, MSTR | positive | up (0.55) | repeat | established a strategic Bitcoin reserve | · | · | +7.76% | +15.76% |
| 31:00 | Blockchain / crypto industry | COIN, IBIT, MSTR, HOOD | positive | up (0.60) | repeat | make America the crypto capital of the world | · | · | +9.54% | +15.03% |
| 31:28 | Stablecoins | CRCL, COIN | positive | up (0.58) | repeat | Genius Act was another milestone just in the past year | · | · | +8.20% | +15.76% |
| 32:14 | Banks | XLF, KRE, JPM, BAC | negative | none (0.52) | repeat | Maybe some of the big banks don't want the competition from crypto com | · | · | -0.02% | +1.80% |
| 33:40 | Intercontinental Exchange (NYSE) | ICE | neutral | none (0.55) | repeat | New York Stock Exchange was formed at the time of our country | · | · | +2.28% | +3.94% |
| 39:43 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | We're leading by a lot with AI. We wanna keep it that way. We wanna re | · | · | -0.42% | -4.14% |
| 42:36 | Honda | HMC | positive | up (0.55) | unclear | Honda just announced they're moving their operations | · | · | +3.38% | -0.81% |
| 42:37 | Toyota | TM | positive | up (0.55) | unclear | Toyota just announced they're moving their operations | · | · | +2.67% | +2.01% |
| 42:40 | Mexico | EWW | neutral | down (0.55) | repeat | moving their operations from Mexico, from Canada | · | · | +1.36% | +3.64% |
| 42:41 | Canada | EWC | neutral | up (0.55) | unclear | probably have a deal with Canada | · | · | +0.84% | +1.13% |
| 45:53 | Oil | XLE, USO, XOM, CVX | neutral | none (0.50) | repeat | oil prices are gonna drop like a rock or | · | · | +1.35% | -1.18% |
| 46:30 | Steel | X, NUE, CLF, STLD | neutral | down (0.55) | new | we're looking at that. In order to get | · | · | · | · |
| 46:31 | Aluminum | AA, CENX | neutral | down (0.55) | new | we're looking at that. In order to get | · | · | +0.46% | -1.63% |
| 46:33 | Agriculture | DBA, MOS, DE, CORN | positive | up (0.55) | unclear | farmers have been hurt very badly by Canada | · | · | +1.23% | +1.52% |
| 48:56 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | interest rates go up because they wanna stop inflation | · | · | +0.21% | +0.91% |
| 49:04 | Switzerland | EWL | positive | none (0.55) | repeat | I see countries like Switzerland where they're the number 1 lowest int | · | · | -0.05% | +0.20% |

### Remarks, Sep 10 2026 — `ZoTDaKuZXkQ`
_the President Delivers Remarks, Sep. 10, 2026 (The White House); stream start 2026-09-10 14:13 ET; 34 min; 7 heads-ups / 4 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 17:58 | Toyota | TM | positive | up (0.55) | unclear | we're building many, many car plants | · | +0.02% | +2.24% | · |
| 18:00 | Mexico | EWW | negative | down (0.55) | repeat | Toyota just announced they're leaving Mexico. | · | -0.13% | -0.85% | · |
| 18:06 | General Motors | GM | positive | up (0.55) | repeat | General Motors just announced a massive plant. | · | +0.15% | -1.03% | · |
| 18:14 | Honda | HMC | positive | up (0.55) | unclear | Honda's coming in. They're all coming in. | · | +0.01% | +2.26% | · |

### Remarks, Aug 14 2026 — `BRGrk3Bw_P0`
_the President Delivers Remarks, Aug. 14, 2026 (The White House); stream start 2026-08-14 14:45 ET; 70 min; 13 heads-ups / 10 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 31:22 | Iran | XLE, USO, ITA | negative | up (0.55) | new | After we finish defeating Iran | · | · | +1.46% | +4.07% |
| 31:59 | Oil | XLE, USO | positive | none (0.50) | unclear | We've taken in millions and millions of barrels of oil. | · | · | +1.46% | +4.07% |
| 33:19 | Northrop Grumman | NOC | positive | none (0.52) | repeat | we didn't hit them with b 2 bombers, you would have had a nuclear weap | · | · | -2.17% | -4.55% |
| 34:37 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | unclear | The blockade is unstoppable. It's a wall of steel. | · | · | · | · |
| 37:00 | Intercontinental Exchange (NYSE) | ICE | neutral | none (0.60) | repeat | Right across from the New York Stock Exchange at a building. | · | · | +0.51% | +5.90% |
| 58:19 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market has set almost 80 all time high since the election | · | · | +0.00% | +0.00% |
| 59:28 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | Under my most favored nation policy on drug prices, we are delivering  | · | · | +0.27% | +5.69% |
| 61:16 | Oil | XLE, USO | positive | none (0.50) | repeat | taking millions and millions of barrels of oil out every single week | · | · | +1.59% | +4.20% |
| 61:23 | Iran | XLE, USO, ITA | positive | none (0.50) | unclear | winning big with the Islamic Republic Of Iran | · | · | +1.59% | +4.20% |
| 65:07 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.58) | repeat | We will pass the great health care plan to stop all payments to big in | · | · | -1.21% | -1.68% |

### the President Participates in Signing Time, Aug. 27, 2026 — `Kr7Ep94Mq1A`
_the President Participates in Signing Time, Aug. 27, 2026 (The White House); stream start 2026-08-27 13:05 ET; 12 min; 13 heads-ups / 13 confirmed / 0 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:19 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market just hit another all time high | · | +0.00% | +0.00% | +0.00% |
| 0:40 | Automakers | GM, F, STLA, TSLA | positive | none (0.52) | repeat | Car companies are moving back, building record number of plants, facto | · | -0.01% | -0.21% | +0.39% |
| 0:43 | Honda | HMC | positive | none (0.50) | repeat | Honda announced they're moving in from Mexico. They're coming here. | · | +0.01% | +1.80% | +5.06% |
| 0:44 | Toyota | TM | positive | none (0.50) | repeat | Toyota announced they're moving in from Mexico. They're coming here. | · | +0.02% | +1.09% | +3.39% |
| 0:46 | Mexico | EWW | neutral | down (0.55) | repeat | Honda and Toyota moving in from Mexico. | · | +0.04% | -0.98% | -0.84% |
| 0:50 | Canada | EWC | neutral | down (0.55) | unclear | Numerous plants are coming in to The United States from Canada. | · | +0.22% | -0.38% | +0.32% |
| 0:57 | Japan | EWJ | neutral | none (0.55) | repeat | numerous plants are coming in from Canada. Also, Japan | · | -0.12% | +0.33% | +1.95% |
| 0:58 | South Korea | EWY | positive | none (0.50) | repeat | plants are coming in from Canada. Also, Japan, South Korea | · | -0.55% | -0.30% | -0.60% |
| 1:00 | Germany | EWG | positive | none (0.52) | repeat | numerous plants are coming in from Germany | · | +0.00% | +0.35% | -1.65% |
| 5:53 | Agriculture | DBA, MOS, DE, CORN | negative | none (0.50) | repeat | Canadian officials charge our farmers 400% | · | +0.42% | +1.60% | +0.76% |
| 10:19 | China | FXI, MCHI, KWEB | negative | down (0.55) | unclear | sanction Chinese banks doing business | · | +0.21% | +1.18% | +0.20% |
| 10:20 | Banks | XLF, KRE, JPM, BAC | negative | none (0.52) | unclear | Who said I'm not? sanction banks doing business | · | +0.16% | +0.54% | +0.84% |
| 10:50 | Oil | XLE, USO | neutral | none (0.50) | unclear | Millions and millions of barrels of oil are coming out of the strait e | · | +1.09% | +1.22% | +3.84% |

### Liberation Day tariffs, Rose Garden, 2025-04-02 — `VFRsYs1VYMg`
_the President Marks America's Liberation Day in The Rose Garden of The White House (April 2, 2025) (MAGNO NEWS LIVE); stream start 2025-04-02 15:53 ET; 70 min; 55 heads-ups / 50 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 14:45 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | American steel workers, we have a lot of them here | · | · | · | · |
| 14:46 | Automakers | GM, F, STLA, TSLA | positive | down (0.60) | new | American auto workers, we have a lot of them here | +1.29% | +0.59% | +2.57% | -1.78% |
| 14:47 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | American farmers, we have a lot of them here today | +2.37% | +3.51% | +6.67% | +1.85% |
| 19:43 | India | INDA, EPI | negative | down (0.60) | repeat | India charges 70% | +2.37% | +3.14% | +5.90% | +5.06% |
| 19:45 | Vietnam | VNM | negative | down (0.60) | repeat | Vietnam charges 75% | -6.56% | -6.71% | +2.15% | -3.87% |
| 20:01 | European Union | VGK, EZU, FEZ | negative | down (0.55) | repeat | European Union charges us more than | +3.08% | +3.45% | +2.56% | +1.26% |
| 20:16 | South Korea | EWY | negative | down (0.60) | repeat | nonmonetary restrictions imposed by South Korea, Japan, and very many  | +1.86% | +2.19% | +4.31% | +1.93% |
| 20:32 | Toyota | TM | neutral | down (0.70) | new | Toyota sells 1,000,000 | -0.41% | -0.46% | -0.04% | +1.38% |
| 20:37 | General Motors | GM | negative | up (0.60) | new | Toyota sells 1,000,000 foreign made automobiles into The United States | +1.29% | +0.59% | +2.57% | -1.78% |
| 20:40 | Ford | F | negative | none (0.55) | repeat | Ford sells very little. | +1.86% | +0.40% | +4.88% | -2.88% |
| 24:06 | Canada | EWC | negative | down (0.55) | repeat | Canada imposes 250 to 300% tariff on many of our dairy products. | +1.61% | +2.96% | +2.85% | +0.22% |
| 24:29 | Mexico | EWW | negative | down (0.60) | repeat | with countries like Canada, you know, we subsidize a lot of countries  | +5.82% | +9.38% | +6.20% | +3.51% |
| 25:24 | Agriculture | DBA, MOS, DE, CORN | neutral | none (0.50) | repeat | Australia bans American beef; we're doing the same thing starting midn | +2.37% | +3.51% | +6.67% | +1.85% |
| 25:35 | China | FXI, MCHI, KWEB | negative | down (0.55) | repeat | China charges American rice farmers an over quota tariff rate of 65%. | +1.69% | +3.08% | +2.62% | -4.12% |
| 25:50 | Japan | EWJ | neutral | none (0.52) | repeat | And [[Japan]], | +0.33% | +0.53% | +0.66% | +1.21% |
| 34:26 | Taiwan | EWT, TSM | negative | down (0.65) | new | Taiwan, where they make they took all of our computer chips and semico | -0.07% | +0.25% | +0.88% | -3.57% |
| 34:30 | Semiconductors | SMH, SOXX, NVDA, INTC | negative | down (0.60) | new | Taiwan took all of our computer chips and semiconductors. | -1.89% | -1.73% | -5.06% | -1.28% |
| 35:59 | China | FXI, MCHI, KWEB | neutral | down (0.58) | repeat | President Xi understood. We took hundreds of billions in tariffs. | +1.69% | +3.08% | +2.62% | -4.12% |
| 36:55 | Switzerland | EWL | negative | down (0.60) | new | If you look at Switzerland, 61% to 31%. | +4.14% | +4.67% | +4.42% | +3.60% |
| 37:31 | Brazil | EWZ | neutral | none (0.55) | unclear | Brazil, 10%, 10%. | +4.17% | +5.27% | +4.22% | -0.38% |
| 38:09 | Automakers | GM, F, STLA, TSLA | positive | down (0.55) | repeat | I'm giving it to the auto workers. | +1.29% | +0.59% | +2.57% | -1.78% |
| 42:06 | Russia | RSX, XLE | negative | none (0.50) | repeat | trying to stop Russia and Ukraine and The Middle East | · | · | · | · |
| 42:06 | Ukraine | ITA, XLE | negative | none (0.50) | unclear | trying to stop Russia and Ukraine and The Middle East | -0.05% | +0.53% | -2.09% | +2.10% |
| 42:37 | Apple | AAPL | neutral | none (0.55) | repeat | company that built its factories and its plants in China | -4.76% | -4.35% | -5.37% | -7.87% |
| 42:47 | SoftBank | SFTBY | positive | up (0.55) | repeat | SoftBank, this is a company that built its factories and its plants in | +0.05% | -0.46% | -6.11% | -5.42% |
| 42:48 | OpenAI | MSFT | positive | none (0.50) | repeat | SoftBank, OpenAI | +1.51% | +1.55% | +4.66% | +6.87% |
| 42:49 | Oracle | ORCL | positive | none (0.55) | repeat | Oracle, and this is a company that built its factories | -1.09% | -1.12% | -1.57% | -1.50% |
| 42:57 | Nvidia | NVDA | positive | up (0.55) | repeat | Nvidia, great companies, are investing $500,000,000,000 | -2.82% | -0.97% | -4.10% | +4.49% |
| 43:03 | TSMC | TSM | positive | up (0.55) | repeat | TSMC, a hot company, is investing hundreds of billions | -2.62% | -1.98% | -3.35% | -4.23% |
| 43:26 | Semiconductors | SMH, SOXX | positive | none (0.50) | repeat | TSMC investing 200 billion, building plant here to avoid tariffs | -1.89% | -1.73% | -5.06% | -1.28% |
| 43:42 | Johnson & Johnson | JNJ | positive | up (0.55) | repeat | Johnson and Johnson, great company, $55,000,000,000 | +5.62% | +5.69% | +9.13% | +2.78% |
| 43:45 | Eli Lilly | LLY | positive | up (0.55) | repeat | Eli Lilly, great company, $55,000,000,000 | +2.50% | +2.09% | +0.72% | -4.82% |
| 43:48 | Meta | META | positive | none (0.52) | unclear | Meta is investing $500,000,000,000. | -3.02% | -3.43% | -3.07% | +0.63% |
| 44:02 | Merck | MRK | positive | none (0.52) | repeat | you have Merck and Palantis | +5.90% | +4.50% | +4.57% | -3.38% |
| 44:03 | Stellantis | STLA | neutral | up (0.55) | unclear | Merck and Palantis, Stellantis | +0.42% | -2.15% | -3.26% | -13.87% |
| 44:04 | General Motors | GM | positive | none (0.50) | repeat | General Motors putting in billions and billions of dollars | +1.29% | +0.59% | +2.57% | -1.78% |
| 44:05 | GE Aerospace | GE | positive | up (0.55) | repeat | GE Aerospace putting in billions and billions of dollars | -1.53% | -0.90% | -6.01% | -2.07% |
| 44:06 | Honda | HMC | positive | none (0.55) | repeat | Honda, Nissan, Hyundai are all putting in billions and billions of dol | +1.31% | +1.29% | +2.04% | +4.51% |
| 44:08 | Hyundai | HYMTF | positive | none (0.50) | repeat | Hyundai are all putting in billions and billions of dollars | · | · | · | · |
| 47:30 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | I have great respect for president Xi of China, great respect for Chin | +1.69% | +3.08% | +2.62% | -4.12% |
| 48:06 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | From the day of my election, the stock market went up in my 1st term 8 | +0.00% | +0.00% | +0.00% | +0.00% |
| 48:09 | Nasdaq | NDAQ | positive | none (0.50) | repeat | Nasdaq going up 155% | -0.85% | -0.67% | -2.34% | -3.14% |
| 48:50 | Mexico | EWW | neutral | none (0.52) | repeat | wanna see the biggest and the best. He said, well, we have to go to Me | +5.82% | +9.38% | +6.20% | +3.51% |
| 52:04 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | our great secretary of agriculture, you did a fantastic | +2.37% | +3.51% | +6.67% | +1.85% |
| 52:49 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | Gasoline is way under $3, and people are beginning to be able to buy t | -1.32% | -2.07% | -5.83% | -11.14% |
| 55:33 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.52) | repeat | We will not cut Social Security, Medicare, or Medicaid benefits | +4.74% | +5.83% | +10.85% | +20.68% |
| 56:05 | John Deere | DE | positive | none (0.55) | unclear | John Deere have been fantastic | +0.39% | +0.89% | +1.78% | +1.40% |
| 56:42 | Federal Reserve | TLT, XLF, KRE | neutral | none (0.50) | repeat | interest deduction on a loan for cars built in America | +4.63% | +4.86% | +12.05% | +1.60% |
| 59:42 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | pharmaceutical companies are gonna become roaring back. They got a big | +3.06% | +3.35% | +4.24% | +0.55% |
| 60:02 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | build our future with American steel | · | · | · | · |

### Stargate AI investment announcement (CNBC), 2025-01-21 — `zDo_RrzdRoQ`
_the President announces AI infrastructure investment — 1/21/2025 (CNBC Television); stream start 2025-01-21 16:47 ET; 47 min; 32 heads-ups / 21 confirmed / 11 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:18 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.70) | new | announce the largest AI infrastructure | +2.24% | +3.33% | +3.43% | -11.96% |
| 1:35 | Oracle | ORCL | positive | up (0.70) | new | largest AI infrastructure project by far in history, all taking place  | +10.50% | +6.29% | +6.94% | -5.91% |
| 1:38 | SoftBank | SFTBY | positive | up (0.65) | new | SoftBank CEO joined to announce largest AI infrastructure project in A | +11.27% | +9.71% | +7.58% | -2.23% |
| 1:47 | OpenAI | MSFT, ORCL, SFTBY | positive | none (0.50) | unclear | CEO of OpenAI | +1.64% | +2.02% | +3.14% | +3.43% |
| 2:08 | Stargate AI project | ORCL, SFTBY, NVDA | positive | up (0.65) | new | world leading technology giants are announcing the formation of Starga | +10.50% | +6.29% | +6.94% | -5.91% |
| 3:20 | Artificial intelligence | NVDA, SMH | positive | up (0.65) | new | we wanna keep it in this country, making it available, help through em | +2.24% | +3.33% | +3.43% | -11.96% |
| 8:02 | Nvidia | NVDA | positive | up (0.60) | unclear | technology partner with MGX. On top of that, we have the technology pa | +2.24% | +3.33% | +3.43% | -11.96% |
| 9:09 | SoftBank | SFTBY | positive | up (0.60) | repeat | Masa said, for AGI to get built here, to create hundreds of thousands  | +11.27% | +9.71% | +7.58% | -2.23% |
| 13:06 | Stargate AI project | ORCL, SFTBY, NVDA | positive | up (0.65) | unclear | $500,000,000 Stargate project comes in addition to a separate pledge | +10.50% | +6.29% | +6.94% | -5.91% |
| 14:04 | Artificial intelligence | NVDA, SMH | positive | up (0.60) | repeat | AI seems to be very hot. Tremendous amounts of money coming in. | +2.24% | +3.33% | +3.43% | -11.96% |
| 15:00 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | We declared a national energy emergency to drill baby drill, our term  | -0.79% | -1.43% | -2.48% | -3.84% |
| 23:24 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | water that they're throwing away to be used for California, and that i | -0.22% | +0.12% | +0.15% | +3.92% |
| 30:10 | Russia | RSX, XLE | negative | down (0.60) | unclear | additional sanctions on Russia. Sounds likely. | · | · | · | · |
| 31:48 | Canada | EWC | neutral | none (0.55) | repeat | are you going to impose tariffs on Canada | -0.14% | -0.79% | -0.58% | +0.84% |
| 31:49 | Mexico | EWW | neutral | none (0.50) | repeat | are you going to impose tariffs on Mexico | -0.12% | +0.55% | +1.43% | +3.08% |
| 32:51 | China | FXI, MCHI, KWEB | negative | down (0.55) | new | I had that talk with president Xi the other day too of China. I said,  | -1.19% | -1.30% | -1.73% | +3.72% |
| 38:17 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | you ought to get it settled | -0.46% | -1.22% | +0.17% | -1.42% |
| 41:29 | Cheniere | LNG | negative | none (0.55) | repeat | along with Cheniere and a couple of others convinced Bush, which was a | -2.73% | -4.48% | -7.26% | -8.44% |
| 44:09 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | If I didn't do that, you wouldn't have a steel mill open in The United | · | · | · | · |
| 44:30 | European Union | VGK, EZU, FEZ | negative | down (0.60) | repeat | Other countries are big abusers also. China's an abuser, but the Europ | -0.22% | -0.60% | -0.34% | +1.41% |
| 45:35 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | I'd like to see federal lands opened up for data centers. I think they | +2.24% | +3.33% | +3.43% | -11.96% |

### Tesla at the White House (Fox Business), 2025-03-11 — `WffynHPu6Ig`
_Tesla arrives at White House as the President vows to buy one to support Musk (Fox Business); stream start 2025-03-11 15:43 ET; 36 min; 30 heads-ups / 19 confirmed / 11 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:36 | Tesla | TSLA | positive | up (0.58) | new | I'm gonna buy 1. Now here's the bad news. | · | · | +6.75% | -3.43% |
| 0:59 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | repeat | stainless steel. very safe. very strong, heavy. | · | · | · | · |
| 3:08 | China | FXI, MCHI, KWEB | negative | down (0.55) | repeat | I did it, initially very strongly against, as you know, China and some | · | · | -0.18% | +5.31% |
| 3:27 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | We handed the stock market over. It was higher than it ever was. | · | · | +0.00% | +0.00% |
| 6:18 | Tesla | TSLA | positive | up (0.60) | new | Tesla's a great company. I don't like what's happening to you. | · | · | +6.75% | -3.43% |
| 8:55 | Mexico | EWW | negative | down (0.55) | repeat | Numerous plants in Mexico and other places that were under constructio | · | · | +1.46% | +3.91% |
| 9:42 | Canada | EWC | positive | none (0.55) | unclear | Canada, and I respect very much. There's a very strong man in Canada | · | · | +0.77% | +2.10% |
| 11:31 | Ukraine | ITA, XLE | neutral | up (0.55) | unclear | Ukraine cease fire | · | · | +0.38% | +2.28% |
| 11:36 | Russia | RSX, XLE | neutral | up (0.55) | unclear | go to Russia and hope president Putin will agree to that also | · | · | · | · |
| 13:59 | Federal Reserve | TLT, XLF, KRE | positive | none (0.50) | repeat | Interest rates have come down a lot. | · | · | -0.52% | +0.04% |
| 14:01 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | Gasoline prices have come down a lot. | · | · | +0.35% | +4.03% |
| 16:09 | Lumber | WOOD, WY | negative | none (0.50) | repeat | We don't have to have lumber from Canada. | · | · | -0.16% | +0.75% |
| 18:39 | Tesla | TSLA | positive | up (0.60) | new | You ever sat in one of these of a Tesla? It looks fast. | +6.09% | +6.52% | +5.19% | +0.27% |
| 27:07 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | tackling the waste of fraud in entitlements like Social Security, Medi | -1.72% | -1.07% | -0.12% | +1.51% |
| 28:29 | Dell | DELL | positive | up (0.55) | unclear | Dell was there. We had a lot of great companies. | +2.25% | +3.08% | +1.77% | +5.79% |
| 28:32 | HP | HPQ | positive | none (0.50) | repeat | We had a lot of great companies, Hewlett Packard. | -1.51% | -2.62% | -1.67% | -1.53% |
| 28:46 | Apple | AAPL | positive | up (0.55) | repeat | As you know, Apple | -1.44% | -1.41% | -4.24% | -4.55% |
| 28:54 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | He invested in China. He's got his plants plants in China. | -1.18% | -1.41% | +1.36% | +3.31% |
| 30:55 | Tesla | TSLA | positive | up (0.60) | new | I love Tesla. | +6.09% | +6.52% | +5.19% | +0.27% |

### Drug pricing executive order (USA TODAY), 2025-05-12 — `Bv66I-pK2NU`
_WATCH LIVE: the President set to sign executive order targeting drug prices (USA TODAY); stream start 2025-05-12 09:50 ET; 58 min; 37 heads-ups / 28 confirmed / 9 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:13 | Steel | X, NUE, CLF, STLD | neutral | none (0.50) | repeat | doesn't include tariffs on cars, steel | · | · | · | · |
| 3:13 | Aluminum | AA, CENX | neutral | up (0.55) | repeat | doesn't include tariffs on cars, steel, aluminum | · | +1.39% | +3.26% | +4.64% |
| 3:18 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | tariffs that may be imposed on pharmaceuticals | · | +1.70% | -1.68% | -1.18% |
| 3:34 | Apple | AAPL | positive | up (0.55) | unclear | I spoke to Tim Cook this morning, and he's gonna, I think, even up | · | -0.31% | +0.01% | -3.34% |
| 4:28 | China | FXI, MCHI, KWEB | positive | up (0.55) | repeat | we made a great deal with China, great trade deal | · | -0.08% | -1.84% | -2.88% |
| 4:55 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | they were gonna purchase from our farmers | · | +0.55% | +0.52% | -0.12% |
| 15:13 | Pharmaceuticals | XLV, XPH, PFE, LLY | neutral | down (0.55) | repeat | why doesn't somebody fight the drug price situation? equalization | · | +1.70% | -1.68% | -1.18% |
| 16:15 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | European Union has been brutal, brutal. | · | +0.21% | -0.15% | +0.79% |
| 16:17 | Apple | AAPL | negative | none (0.55) | repeat | suing all our companies, Apple | · | -0.31% | +0.01% | -3.34% |
| 16:18 | Google | GOOGL | negative | none (0.50) | repeat | European Union suing all our companies, Apple, Google | · | +0.19% | +0.35% | +3.42% |
| 16:20 | Meta | META | negative | none (0.55) | repeat | European Union suing all our companies, Apple, Google, Meta. | · | -0.01% | +3.05% | -0.80% |
| 18:04 | United Kingdom | EWU | negative | none (0.50) | repeat | in London I'm paying $88 | · | +0.39% | -0.24% | +0.76% |
| 20:48 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | your cost for Medicaid and Medicare | · | +0.15% | -19.20% | -19.39% |
| 23:26 | Agriculture | DBA, MOS, DE, CORN | negative | none (0.50) | repeat | They sell us their agricultural products. We sell them virtually none. | · | +0.55% | +0.52% | -0.12% |
| 26:04 | Novo Nordisk | NVO | negative | down (0.65) | repeat | weight loss drug Ozempic costs almost $500 here in America | · | +2.46% | +1.12% | +2.27% |
| 27:06 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | cut drug prices by 80 or 90% | · | +1.70% | -1.68% | -1.18% |
| 29:55 | European Union | VGK, EZU, FEZ | negative | down (0.55) | unclear | they don't have to sell cars into The United States anymore | · | +0.21% | -0.15% | +0.79% |
| 41:37 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | American people are subsidizing research and development efforts for d | · | +0.65% | -3.37% | -2.89% |
| 41:44 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | Europe will share the burden of that. | · | +0.34% | -0.37% | +0.58% |
| 43:44 | Ford | F | neutral | none (0.60) | unclear | buying a Ford for $175,000, people in London buying it for $10,000 | · | +0.23% | -0.53% | -0.49% |
| 44:18 | China | FXI, MCHI, KWEB | neutral | up (0.55) | repeat | what we did with China, the trade deal | · | +0.02% | -1.76% | -2.82% |
| 47:51 | Boeing | BA | negative | down (0.55) | repeat | very disappointed that it's taking Boeing so long to build a new Air F | · | +0.50% | +2.23% | +1.78% |
| 53:41 | Steel | X, NUE, CLF, STLD | neutral | none (0.50) | repeat | are you open to negotiating your tariffs on steel | · | · | · | · |
| 53:41 | Aluminum | AA, CENX | neutral | up (0.55) | repeat | are you open to negotiating your tariffs on aluminum | · | +0.08% | +1.83% | +3.19% |
| 53:56 | Mexico | EWW | negative | down (0.60) | repeat | They've left Mexico in a few cases. | · | -0.50% | +1.66% | +2.87% |
| 53:58 | Canada | EWC | negative | down (0.55) | repeat | They've left Canada. They're not gonna build in Canada. | · | -0.33% | -0.73% | -0.61% |
| 54:46 | Japan | EWJ | neutral | none (0.50) | repeat | if you look at Japan and these others, they do tremendously with cars | · | +0.32% | -1.70% | -2.65% |
| 56:52 | Agriculture | DBA, MOS, DE, ADM | negative | none (0.50) | repeat | farmers are being killed | · | -0.25% | -0.04% | -0.68% |

### US Steel remarks, Pittsburgh (CNBC), 2025-05-30 — `DKddhD4z7UU`
_the President delivers remarks on the U.S. steel deal — 5/30/2025 (CNBC Television); stream start 2025-05-30 17:38 ET; 62 min; 39 heads-ups / 25 confirmed / 14 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:08 | Steel | X, NUE, CLF, STLD | positive | up (0.75) | repeat | heart and soul of U.S. Steel | · | · | · | · |
| 3:53 | Japan | EWJ | positive | none (0.50) | repeat | Japan has been a tremendous friend of mine | +0.69% | +0.71% | -1.12% | -2.00% |
| 6:24 | U.S. Steel | X, NUE, CLF, STLD | positive | up (0.75) | repeat | vice chairman of Nippon Steel. This will be a great company. | · | · | · | · |
| 14:37 | Steel | X, NUE, CLF, STLD | positive | up (0.70) | repeat | tough hardworking members of the United States Steel Workers | · | · | · | · |
| 18:48 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | They were dumping steel from China and from all over the world. | +0.68% | +0.49% | +0.86% | +4.14% |
| 22:52 | Mexico | EWW | negative | down (0.55) | repeat | imports of steel and rebar from Mexico exploded by more than 1000% | +1.16% | +1.27% | -0.77% | -0.22% |
| 23:00 | Canada | EWC | negative | none (0.55) | repeat | We were getting our steel from Canada. | +0.43% | +0.36% | -0.29% | -0.99% |
| 25:03 | Steel | X, NUE, CLF, STLD | positive | up (0.70) | new | imposing a 25% increase. We're going to bring it from 25% to 50%, the  | · | · | · | · |
| 27:17 | U.S. Steel | X, NUE, CLF, STLD | positive | up (0.70) | unclear | We want it built with the strength and the pride of Pittsburgh. It's P | · | · | · | · |
| 42:51 | U.S. Steel | X, NUE, CLF, STLD | positive | up (0.70) | repeat | I'm pretty passionate about it | · | · | · | · |
| 48:42 | Apple | AAPL | positive | none (0.50) | repeat | Apple is spending $500,000,000,000 | -0.01% | -0.02% | +0.07% | -1.45% |
| 48:46 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | Apple investing in America, not in China. | +0.68% | +0.49% | +0.86% | +4.14% |
| 48:47 | Nvidia | NVDA | positive | none (0.50) | repeat | Nvidia, 500,000,000,000 | +0.54% | +1.27% | +3.37% | +3.80% |
| 48:51 | TSMC | TSM | positive | none (0.55) | repeat | TSMC | +0.13% | +0.04% | +1.08% | +5.33% |
| 48:58 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | repeat | TSMC, the biggest in the world for chips | +0.04% | +0.87% | +2.63% | +5.43% |
| 49:01 | Amazon | AMZN | neutral | none (0.50) | repeat | Amazon, 4,000,000,000 | +0.26% | -0.20% | -0.80% | +4.09% |
| 49:07 | Merck | MRK | positive | none (0.52) | repeat | Merck | +0.51% | -0.97% | -0.75% | +1.49% |
| 49:07 | Stellantis | STLA | positive | up (0.55) | repeat | Stellantis | -2.78% | -3.07% | -3.50% | -3.52% |
| 49:09 | General Motors | GM | positive | up (0.55) | repeat | General Motors are putting in billions and billions of dollars | -0.75% | -4.10% | -2.25% | -5.13% |
| 49:34 | Homebuilders | XHB, ITB, LEN, DHI | positive | none (0.50) | repeat | Mortgage rates are down. | -0.28% | -2.31% | -0.68% | +0.32% |
| 49:38 | Oil | XLE, USO, XOM, CVX | positive | down (0.52) | repeat | Gasoline prices over Memorial Day weekend were the lowest since 2003. | +2.15% | +1.07% | +1.38% | +0.76% |
| 53:14 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | new | made with American steel | · | · | · | · |
| 53:15 | U.S. Steel | X, NUE, CLF, STLD | positive | up (0.60) | unclear | made with American steel and steel from US steel | · | · | · | · |
| 55:05 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | we pay the highest drug prices | +0.02% | -0.11% | -0.84% | -0.61% |
| 56:46 | Health insurers | UNH, CI, ELV, HUM | negative | none (0.50) | repeat | we're gonna be lowering your drug cost by 90%, by 85%, by 75% | +0.68% | +3.29% | -1.37% | -1.32% |

### Apple $600B investment announcement (White House), 2025-08-06 — `J6SK7lotKZQ`
_the President Makes an Announcement, Aug. 6, 2025 (The White House); stream start 2025-08-06 17:02 ET; 39 min; 55 heads-ups / 43 confirmed / 12 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:13 | Apple | AAPL | positive | up (0.65) | new | great and most esteemed business leaders and geniuses and innovators | +2.09% | +2.19% | +6.85% | +7.24% |
| 2:46 | Broadcom | AVGO | positive | up (0.55) | unclear | Apple suppliers like Corning, Broadcom | +0.94% | +1.92% | +0.40% | +1.25% |
| 2:49 | Samsung | SSNLF | positive | up (0.55) | unclear | Apple suppliers like Corning, Broadcom, Texas Instruments, and Samsung | -0.55% | · | -0.70% | -1.92% |
| 4:58 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | unclear | invest billions of dollars to construct data centers across the countr | +0.65% | +1.54% | +1.13% | -0.47% |
| 6:28 | Rare earths | MP, REMX | positive | up (0.75) | new | rare earth magnets from Texas and build | +4.62% | +5.16% | +9.39% | +11.51% |
| 6:38 | MP Materials | MP | positive | up (0.65) | new | build a brand new rare earth recycling line in Mountain Pass | +4.62% | +5.16% | +9.39% | +11.51% |
| 6:49 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | unclear | Apple will help develop and manufacture semiconductors | +1.62% | +1.76% | +1.72% | +3.41% |
| 9:30 | Nvidia | NVDA | positive | none (0.52) | repeat | Nvidia is investing 500,000,000,000 to | +0.65% | +1.54% | +1.13% | -0.47% |
| 9:37 | Micron | MU | positive | up (0.55) | repeat | Micron, great company, is investing 200,000,000,000. | +4.38% | +2.82% | +8.60% | +13.25% |
| 9:40 | IBM | IBM | positive | up (0.55) | unclear | IBM is investing more than 150,000,000,000. | -0.34% | +0.79% | -4.66% | -7.94% |
| 9:44 | SoftBank | SFTBY | positive | none (0.55) | repeat | SoftBank | +1.37% | +2.72% | +11.06% | +22.09% |
| 9:49 | TSMC | TSM | positive | up (0.55) | repeat | TSMC | +5.12% | +4.96% | +3.83% | +2.24% |
| 9:52 | Johnson & Johnson | JNJ | positive | up (0.55) | repeat | Johnson and Johnson, 55,000,000,000 | -0.21% | -0.31% | +0.91% | +0.50% |
| 9:55 | Merck | MRK | positive | none (0.50) | repeat | Merck, great company, is investing | -0.28% | -0.97% | +0.88% | +2.26% |
| 9:56 | Stellantis | STLA | positive | none (0.50) | unclear | Stellantis, and General Motors are putting many, many billions in. | +1.24% | +2.20% | +4.55% | +6.78% |
| 9:57 | General Motors | GM | positive | none (0.50) | repeat | General Motors are putting many, many billions in | +0.08% | +0.62% | +1.32% | +5.60% |
| 10:40 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | Costs are way down. Costs are down. | +0.04% | -0.07% | -0.45% | -0.93% |
| 11:21 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market has been hitting all time records, all time highs | +0.00% | +0.00% | +0.00% | +0.00% |
| 11:41 | Canada | EWC | neutral | none (0.52) | repeat | car plants coming in from Canada, from Mexico | -0.25% | -0.60% | -1.51% | -2.76% |
| 11:42 | Mexico | EWW | neutral | none (0.52) | repeat | car plants coming in from Canada, from Mexico | -0.51% | -0.05% | +0.75% | -1.54% |
| 12:03 | European Union | VGK, EZU, FEZ | neutral | none (0.50) | repeat | We just made a deal with the EU where they're paying hundreds of billi | +0.59% | +0.61% | +0.69% | +0.91% |
| 12:07 | Japan | EWJ | positive | none (0.50) | repeat | we just made a deal with the EU where they're paying hundreds of billi | +0.68% | +0.48% | +1.80% | +1.72% |
| 12:45 | Apple | AAPL | positive | up (0.60) | new | companies like Apple. They're coming home. They're all coming home. | +2.09% | +2.19% | +6.85% | +7.24% |
| 14:28 | Intel | INTC | positive | up (0.58) | new | we started with Intel | -2.56% | -3.23% | -2.95% | +14.98% |
| 17:29 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | new | producing tens of millions of chips for Apple using advanced process t | +1.62% | +1.76% | +1.72% | +3.41% |
| 18:00 | Rare earths | MP, REMX | positive | up (0.75) | new | committed to buying American made advanced rare earth magnets | +4.62% | +5.16% | +9.39% | +11.51% |
| 18:02 | MP Materials | MP | positive | up (0.80) | new | committed to buying American made advanced magnets developed by MP Mat | +4.62% | +5.16% | +9.39% | +11.51% |
| 19:00 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | unclear | significantly growing our investments in AI | +0.65% | +1.54% | +1.13% | -0.47% |
| 20:22 | Micron | MU | positive | up (0.55) | repeat | We had Micron in yesterday. | +4.38% | +2.82% | +8.60% | +13.25% |
| 22:11 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | China is right now building 58 coal fired plants. | -0.31% | -0.34% | -1.01% | -0.47% |
| 22:13 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | coal has opened up and opened up big. We brought it back. | +1.45% | -0.53% | +3.97% | +6.99% |
| 22:20 | Oil | XLE, USO, XOM, CVX | positive | none (0.52) | repeat | We have more oil and gas than anybody else in the world. | +0.04% | -0.07% | -0.45% | -0.93% |
| 24:18 | Northrop Grumman | NOC | positive | up (0.62) | new | We ordered brand new b 2 bombers | -1.58% | -1.45% | -2.08% | -2.87% |
| 24:56 | RTX (Raytheon) | RTX | positive | none (0.50) | repeat | we had Tomahawks | -1.25% | -1.51% | -1.27% | -2.35% |
| 25:47 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | estimate for Ukraine is about 9,000 | -0.41% | -1.09% | -1.18% | -2.64% |
| 27:03 | India | INDA, EPI | negative | down (0.65) | repeat | we put a 50% tariff on India | +0.35% | +0.59% | -0.96% | -1.64% |
| 27:09 | Russia | RSX, XLE | negative | none (0.50) | repeat | 50% tariff on India on oil. They're very close to China in terms of th | · | · | · | · |
| 29:27 | Apple | AAPL | positive | none (0.52) | repeat | The president wants a made in the USA iPhone. | +2.09% | +2.19% | +6.85% | +7.24% |
| 29:35 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | We're doing a lot of the semiconductors here. | +1.62% | +1.76% | +1.72% | +3.41% |
| 33:26 | Paramount (CBS) | PSKY | negative | none (0.55) | repeat | Colbert has no talent. | +4.89% | -1.07% | -5.50% | +28.33% |
| 33:38 | Disney (ABC) | DIS | negative | none (0.55) | repeat | Kimmel has no talent. They're next. They're gonna be going. | -0.04% | -0.80% | -3.07% | -0.93% |
| 35:44 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | building electric generating plants especially for AI because it needs | +0.65% | +1.54% | +1.13% | -0.47% |
| 37:56 | Russia | RSX, XLE | negative | down (0.55) | repeat | China is facing potential secondary sanctions for Russian oil | · | · | · | · |

### Press conference on DC crime, Nvidia chips Q&A (CNBC), 2025-08-11 — `zh6lh9GC0Ec`
_the-president announces plans to address violent crime and homelessness in Washington, D.C. — 8/11/25 (CNBC Television); stream start 2025-08-11 10:36 ET; 80 min; 27 heads-ups / 19 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 4:05 | Colombia | GXG | negative | none (0.55) | repeat | murder rate in Washington today is higher than that of Bogota, Colombi | · | · | +0.61% | +2.08% |
| 4:06 | Mexico | EWW | negative | none (0.55) | repeat | murder rate in Washington today is higher than that of Bogota, Colombi | · | +0.27% | +0.69% | -1.26% |
| 37:44 | Cheniere | LNG | positive | none (0.52) | repeat | Thank you, Cheniere. You're welcome. Great job. | · | +0.44% | -1.53% | -1.55% |
| 45:46 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | They agreed to put up 5% instead of 2% | · | +0.09% | +0.04% | -1.23% |
| 57:30 | Russia | RSX, XLE | negative | none (0.50) | repeat | I stopped the pipelines. It's called Nord Stream 2. | · | · | · | · |
| 59:10 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | I got it raised from 2 percent of GDP to 5% | · | -0.15% | -0.05% | -1.32% |
| 59:19 | European Union | VGK, EZU, FEZ | negative | none (0.50) | repeat | Europe has spent a 100,000,000,000. | · | -0.01% | +0.27% | +1.18% |
| 62:41 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | Putin wanted all of Ukraine. I happen to be 1 of them. | · | -0.15% | -0.05% | -1.32% |
| 63:34 | Oil | XLE, USO, XOM, CVX | negative | none (0.50) | repeat | 50% tariff on you if you buy | · | -0.22% | -0.61% | -0.24% |
| 64:18 | Lockheed Martin | LMT | positive | none (0.52) | repeat | I also gave the Javelins. Javelin is called a tank buster. | · | +0.30% | +0.53% | +2.57% |
| 67:32 | Nvidia | NVDA | negative | none (0.50) | repeat | advanced Nvidia and AMD chips. No. Obsolete. | · | +0.07% | -0.89% | -1.61% |
| 67:33 | Semiconductors | SMH, SOXX, NVDA, INTC | negative | down (0.50) | unclear | advanced chips. No. Obsolete. | · | -0.14% | +0.51% | -0.68% |
| 67:45 | Nvidia | NVDA | positive | none (0.55) | repeat | I deal with Jensen, who's a great guy | · | +0.07% | -0.89% | -1.61% |
| 67:50 | Semiconductors | SMH, SOXX | neutral | none (0.50) | repeat | the H20, that we're talking about, obsolete chip that China already ha | · | -0.14% | +0.51% | -0.68% |
| 68:28 | BlackRock | BLK | negative | none (0.55) | unclear | take 30% to 50% off of it | · | +0.40% | +2.12% | -0.06% |
| 69:55 | Defense | ITA, XAR, AVAV, KTOS | neutral | none (0.50) | repeat | We will sometimes sell fighter jets to a country | · | -0.15% | -0.05% | -1.32% |
| 72:21 | Russia | RSX, XLE | neutral | none (0.50) | repeat | I expect to have a meeting with Putin that I think it'll be good, but  | · | · | · | · |
| 76:54 | European Union | VGK, EZU, FEZ | positive | none (0.50) | repeat | I'll be calling the European leaders. They're great leaders. | · | -0.01% | +0.27% | +1.18% |
| 77:06 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | They've OD'd on trying to settle Ukraine. | · | -0.15% | -0.05% | -1.32% |

### Cabinet meeting (CNBC), 2025-08-26 — `cbEPqUdelFo`
_the President holds a cabinet meeting at the White House  — 8/26/2025 (CNBC Television); stream start 2025-08-26 12:11 ET; 198 min; 112 heads-ups / 85 confirmed / 27 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:43 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.60) | repeat | selling a tremendous amount of equipment to NATO... selling missiles a | · | -0.13% | -0.37% | -1.08% |
| 2:24 | RTX (Raytheon) | RTX | positive | up (0.62) | repeat | factories are doubling up and tripling up where they make the Patriots | · | -0.20% | +0.46% | -0.18% |
| 4:40 | Mexico | EWW | negative | down (0.55) | repeat | They're coming from Mexico. They don't wanna pay the tariffs. | · | +0.17% | +0.38% | +2.23% |
| 4:42 | Canada | EWC | negative | down (0.55) | repeat | They're coming from Mexico. They're coming from Canada. | · | -0.08% | +0.56% | +2.06% |
| 4:44 | European Union | VGK, EZU, FEZ | negative | down (0.55) | repeat | They're coming from Europe, all over Europe. | · | -0.05% | -0.71% | -1.44% |
| 4:57 | Meta | META | positive | none (0.55) | repeat | This is something given to me by Mark Zuckerberg. | · | -0.14% | -1.30% | -2.22% |
| 5:23 | Meta | META | neutral | none (0.52) | repeat | He's building in Louisiana. That's Meta. | · | -0.14% | -1.30% | -2.22% |
| 6:27 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | China goes out and builds these massive plants. | · | -0.04% | -3.28% | -1.07% |
| 6:33 | Coal | BTU, ARCH, AMR | positive | up (0.60) | repeat | China builds massive plants. Building 58 coal. | · | +0.46% | -0.83% | +1.58% |
| 6:43 | Coal | BTU, ARCH, AMR | positive | up (0.62) | repeat | coal is back with this country too. It works for them. We call it clea | · | +0.46% | -0.83% | +1.58% |
| 6:56 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.60) | repeat | We don't allow windmills. We're not allowing any windmills to go up. | · | -0.75% | -3.30% | -1.40% |
| 7:32 | Agriculture | DBA, MOS, DE, CORN | negative | none (0.50) | repeat | farmers are saying, they're building these massive | · | +0.10% | +0.52% | -0.35% |
| 8:04 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | They have oil. It's tremendous. | · | -0.16% | +1.28% | +0.89% |
| 9:10 | Ford | F | positive | none (0.50) | repeat | domestic auto production is up 18,000 cars a month. Ford, General Moto | · | -0.06% | +0.32% | -1.69% |
| 9:11 | General Motors | GM | positive | none (0.52) | repeat | domestic auto production is up 18,000 cars a month. Ford, General Moto | · | +0.04% | -0.26% | -1.52% |
| 9:14 | Stellantis | STLA | neutral | up (0.55) | repeat | Ford, General Motors, and couple of others, Stellantis | · | -0.24% | -3.86% | -7.27% |
| 10:01 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | repeat | Domestic steel production is up by 100,000 | · | · | · | · |
| 10:11 | Aluminum | AA, CENX | negative | up (0.55) | repeat | We have a 50% tariff on steel, aluminum | · | +0.25% | -1.31% | -3.01% |
| 10:13 | Copper | COPX, FCX, SCCO | negative | up (0.50) | repeat | Copper just got brought into the picture | · | +0.18% | -0.93% | +4.77% |
| 10:40 | Oil | XLE, USO | positive | none (0.50) | repeat | domestic oil production is up by more than 300,000 | · | -0.16% | +1.28% | +0.89% |
| 12:33 | Furniture / home goods | WSM, RH, LZB | positive | none (0.50) | repeat | businesses moving into our country, autos and AI, furniture as an exam | · | -0.41% | -4.48% | -4.05% |
| 14:34 | Hyundai | HYMTF | positive | up (0.55) | repeat | Hyundai, 14,000 | · | · | · | · |
| 14:41 | Mexico | EWW | negative | down (0.55) | repeat | General Motors is moving production from Mexico | · | +0.17% | +0.38% | +2.23% |
| 15:50 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | repeat | auto workers voted for me. They understood better than anybody else. | · | +0.04% | -0.26% | -1.52% |
| 16:27 | United Kingdom | EWU | positive | none (0.50) | repeat | negotiated historic trade deals with The United Kingdom | · | +0.10% | -0.47% | -1.18% |
| 16:28 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | negotiated historic trade deals with China | · | -0.04% | -3.28% | -1.07% |
| 16:29 | Vietnam | VNM | positive | up (0.55) | repeat | negotiated historic trade deals with Vietnam | · | -0.19% | -0.49% | +1.24% |
| 16:31 | Japan | EWJ | positive | none (0.52) | repeat | negotiated historic trade deals with Japan | · | +0.05% | -0.74% | -1.18% |
| 16:31 | South Korea | EWY | positive | up (0.55) | repeat | negotiated historic trade deals with South Korea | · | -0.06% | -0.63% | +0.43% |
| 16:34 | European Union | VGK, EZU, FEZ | positive | none (0.50) | repeat | negotiated historic trade deals with The United Kingdom, China, Indone | · | -0.05% | -0.71% | -1.44% |
| 21:16 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.50) | repeat | We strengthen Social Security. We strengthen Medicare, Medicaid. | · | +0.18% | -1.70% | +0.05% |
| 23:35 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | none (0.50) | repeat | awesome power of artificial intelligence is used to benefit all Americ | · | -0.06% | -0.56% | -6.15% |
| 40:16 | NuScale | SMR | negative | none (0.55) | unclear | Between him and NuScale, you got some real beauties | · | +0.70% | -0.84% | +14.52% |
| 42:57 | Germany | EWG | neutral | none (0.55) | repeat | you go to Germany, you go to England, you go to different places | · | -0.08% | -1.13% | -2.67% |
| 43:49 | European Union | VGK, EZU, FEZ | negative | none (0.50) | repeat | people go to Europe to buy drugs and they come back | · | -0.03% | -0.66% | -1.39% |
| 43:52 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | prescription drug...you can buy them for 10%, 15%, 20% | · | -0.03% | -0.53% | -0.13% |
| 44:40 | Eli Lilly | LLY | positive | down (0.60) | repeat | very great gentleman from Eli Lilly. I think he's an incredible execut | · | -0.12% | +0.50% | +1.45% |
| 45:05 | Johnson & Johnson | JNJ | negative | down (0.55) | repeat | a pill that's made by Johnson and Johnson | · | +0.02% | -0.48% | +0.65% |
| 45:14 | Canada | EWC | negative | none (0.50) | repeat | a pill made in Canada versus United States factory | · | +0.09% | +0.64% | +2.13% |
| 47:51 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | gonna have the biggest, price of that. Now that's gonna lower Social S | · | +0.18% | -1.70% | +0.05% |
| 51:32 | Oil | XLE, USO, XOM, CVX | negative | up (0.55) | unclear | If you build an oil derrick in The Gulf, you gotta put a bond down. | · | +0.30% | +1.44% | +1.05% |
| 51:56 | Natural gas / LNG | UNG, LNG, EQT | negative | up (0.55) | repeat | natural gas is 3¢. So it is the most expensive energy. | · | -1.00% | +2.01% | +9.78% |
| 67:40 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | Make America the AI capital of the world | · | -0.06% | -0.56% | -6.15% |
| 68:53 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | helping the farmers | · | -0.08% | +0.42% | -0.45% |
| 77:27 | Trucking / rail | IYT, UNP, CSX | positive | none (0.52) | repeat | I was with a trucking company in Ohio. | · | -0.00% | -0.81% | -1.54% |
| 83:03 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | Natural gas has become our main industrial fuel powering factories. | · | +0.72% | +3.04% | +10.88% |
| 84:37 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | none (0.50) | repeat | How do we lead the world in artificial intelligence if we're shrinking | · | +0.11% | -0.50% | -6.09% |
| 84:43 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | reshore steel and automobiles and jobs Americans want back | · | · | · | · |
| 84:44 | Aluminum | AA, CENX | positive | up (0.55) | repeat | reshore aluminum and automobiles and jobs Americans want back | · | -0.02% | -1.30% | -3.00% |
| 84:45 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | reshore semiconductors and jobs Americans want back in country | · | -0.07% | -0.23% | -3.56% |
| 84:55 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | hand leadership to China in artificial intelligence | · | +0.01% | -3.03% | -0.83% |
| 86:17 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | reshoring of steel, of aluminum, of plastics, of fertilizer | · | -0.05% | +0.50% | -0.36% |
| 90:06 | Defense | ITA, XAR, LMT, RTX | positive | up (0.52) | repeat | headed with secretary Duffy, with the South Korean president Lee today | · | +0.34% | -0.18% | -0.89% |
| 90:39 | McDonald's | MCD | positive | none (0.52) | unclear | McDonald's is investing 375,000 | · | +0.02% | -1.09% | +0.94% |
| 91:15 | Lumber | WOOD, WY | positive | none (0.52) | repeat | Buckeye Pacific, really a trading floor for the timber industry | · | -0.03% | -1.32% | -1.96% |
| 105:23 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | fight for the original American worker whom I think the farmer is | · | -0.05% | +0.50% | -0.36% |
| 122:32 | Defense | ITA, XAR, LMT, RTX | positive | none (0.50) | repeat | roads, bridges, pipelines, shipbuilding | · | +0.34% | -0.18% | -0.89% |
| 125:30 | Airlines | JETS, DAL, UAL, AAL | positive | up (0.55) | unclear | greatest contract ever crafted in the federal government for this buil | · | +0.00% | -0.37% | +1.27% |
| 125:45 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.50) | unclear | if you build windmills 1.2 miles from roadway, it can mess up | · | -0.29% | -2.40% | -0.49% |
| 126:53 | Space | RKLB, ARKX | positive | none (0.52) | repeat | Moon to Mars mission. It's truly remarkable. | · | +1.03% | -5.28% | -10.43% |
| 128:54 | Japan | EWJ | negative | none (0.50) | repeat | Japan and Korea, they're never gonna open their markets to us. | · | -0.03% | -0.70% | -1.14% |
| 128:54 | South Korea | EWY | negative | none (0.50) | repeat | Japan and Korea, they're never gonna open their markets to us. | · | -0.08% | -0.46% | +0.60% |
| 129:08 | European Union | VGK, EZU, FEZ | neutral | none (0.50) | repeat | European Union, the 2nd largest economy, $20,000,000,000,000 | · | -0.03% | -0.63% | -1.36% |
| 129:45 | Semiconductors | SMH, SOXX, NVDA, INTC | neutral | none (0.50) | repeat | the commerce department, which had the chips money | · | -0.07% | -0.23% | -3.56% |
| 131:20 | TSMC | TSM | positive | up (0.55) | repeat | We've got a 165,000,000,000 for TSMC | · | -0.08% | -0.01% | -2.87% |
| 131:45 | Furniture / home goods | WSM, RH, LZB | positive | down (0.55) | unclear | We're gonna do it for furniture. | · | -0.03% | -2.58% | -2.16% |
| 131:47 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | We got steel. Tariffs are gonna bring semiconductors home. | · | · | · | · |
| 131:47 | Aluminum | AA, CENX | positive | up (0.58) | repeat | We got aluminum. Tariffs are gonna bring semiconductors home. | · | -0.02% | -1.30% | -3.00% |
| 132:00 | Blockchain / crypto industry | COIN, IBIT, MSTR, HOOD | positive | up (0.55) | new | Department of Commerce is going to start issuing its statistics on the | · | +0.70% | +1.22% | -0.52% |
| 132:01 | Bitcoin | IBIT, COIN, MSTR | positive | none (0.50) | repeat | you are the crypto president | · | +0.60% | +1.50% | +2.14% |
| 137:19 | Northrop Grumman | NOC | positive | none (0.52) | repeat | from the tactical of standards to the strategic of b 2 bombers, we're  | · | +0.18% | -1.62% | -2.12% |
| 137:23 | Defense | ITA, XAR, LMT, RTX | positive | up (0.55) | repeat | Golden Dome for America, which is on track to deliver strategically | · | +0.34% | -0.18% | -0.89% |
| 141:53 | Federal Reserve | TLT, XLF, KRE | positive | up (0.55) | repeat | We're gonna be seeing lower interest rates. | · | -0.02% | -0.44% | -0.09% |
| 145:47 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | bringing back coal mining, bringing back mining | · | -1.22% | -2.30% | +0.08% |
| 145:49 | Lumber | WOOD, WY | positive | up (0.52) | repeat | bringing back timber. All the industries that have been killed | · | -0.18% | -1.29% | -1.94% |
| 150:09 | China | FXI, MCHI, KWEB | positive | none (0.52) | repeat | we're honored to have their students here | · | -0.16% | -3.05% | -0.84% |
| 153:47 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | People are paying too high an interest rate. | · | -0.02% | -0.44% | -0.09% |
| 155:14 | John Deere | DE | positive | none (0.52) | unclear | I will be speaking to John Deere | · | +0.15% | +1.08% | -3.33% |
| 157:41 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | Bobby was talking about with respect to drug prices is unbeatable. Nob | · | -0.06% | -0.48% | -0.08% |
| 170:31 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | we wouldn't have problems like Lisa Cook | · | · | -0.44% | -0.09% |
| 177:41 | Russia | RSX, XLE | negative | down (0.60) | repeat | very strong tariff system that's very costly to Russia | · | · | · | · |
| 177:42 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | tariff system that's very costly to Russia or Ukraine or whoever | · | · | -0.51% | -1.22% |
| 181:02 | Semiconductors | SMH, SOXX | negative | none (0.50) | repeat | Biden, with his stupid chip sack, handed money to all these people | · | · | -0.15% | -3.49% |
| 181:36 | Intel | INTC | positive | up (0.60) | repeat | I wanna see Intel do well. Intel was a great company. | · | · | +2.04% | -1.02% |
| 190:34 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | I love both groups, and we take care of our farmers. | · | · | +0.56% | -0.31% |

### Delivers Remarks to U.S. Embassy Personnel and Business Leaders — `-POgY_NsQ10`
_the President Delivers Remarks to U.S. Embassy Personnel and Business Leaders (The White House); stream start 2026-09-12 06:15 ET; 41 min; 17 heads-ups / 13 confirmed / 4 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 15:12 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | We have AI. We're dominating AI. We're leading everybody. | -2.54% | -2.88% | -2.06% | · |
| 19:07 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | 401ks up at record levels, never been so high | +0.00% | +0.00% | +0.00% | · |
| 22:48 | Toyota | TM | positive | none (0.50) | repeat | auto plants are going through the roof. They're all the auto companies | -0.02% | -0.42% | -0.44% | · |
| 22:49 | Honda | HMC | positive | up (0.55) | repeat | auto plants are going through the roof. They're all the auto companies | +0.63% | +0.47% | +0.26% | · |
| 22:54 | General Motors | GM | positive | up (0.55) | repeat | General Motors and Ford are going wild | +0.95% | +0.99% | +1.52% | · |
| 22:55 | Ford | F | positive | up (0.55) | repeat | General Motors and Ford are going wild | -0.10% | -0.83% | -1.47% | · |
| 25:40 | Natural gas / LNG | UNG, LNG, EQT | positive | up (0.52) | repeat | unleashed our vast energy resources to make America the number 1 suppl | +1.77% | +2.43% | +4.27% | · |
| 26:25 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | Venezuela, we took that over. We won the war. Millions and millions of | +1.95% | +1.36% | +1.40% | · |
| 26:37 | Oil | XLE, USO | positive | down (0.52) | unclear | 65,000,000,000 barrels of oil. It's good for 500 years. | +1.95% | +1.36% | +1.40% | · |
| 26:52 | Venezuela | XLE, CVX | positive | up (0.55) | unclear | Big oil companies are moving in. They're starting to drill. | +1.95% | +1.36% | +1.40% | · |
| 28:12 | RTX (Raytheon) | RTX | positive | up (0.60) | repeat | the demand our equipment is incredible, the Patriot missile | +0.04% | -0.37% | -0.89% | · |
| 29:03 | Lockheed Martin | LMT | positive | up (0.58) | repeat | We have the THAAD system and the Patriot system. | +1.15% | +2.00% | +1.94% | · |
| 31:00 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | other countries are buying it in record numbers, we're way advanced | -0.44% | -0.30% | -1.70% | · |

### Delivers Remarks, Aug. 5, 2026 — `khgwrHbUKnA`
_the President Delivers Remarks, Aug. 5, 2026 (The White House); stream start 2026-08-05 16:27 ET; 76 min; 26 heads-ups / 20 confirmed / 6 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 8:38 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | prescription drug prices down 4, 5, 600 percent | +1.15% | -0.51% | +0.48% | +1.52% |
| 12:10 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | we've been screwed by tariffs used against us for years by China | -0.53% | -0.60% | -0.20% | -4.43% |
| 12:10 | Japan | EWJ | negative | none (0.55) | repeat | we've been screwed by tariffs used against us for years by China, by J | -0.15% | +0.51% | +1.38% | +2.43% |
| 12:12 | South Korea | EWY | negative | none (0.52) | repeat | we've been screwed by tariffs used against us for years by China, by J | -4.31% | -1.76% | -2.25% | +4.55% |
| 12:13 | Germany | EWG | negative | none (0.52) | repeat | we've been screwed by tariffs used against us for years by China, by J | -0.47% | -0.27% | +0.42% | -0.32% |
| 12:14 | Canada | EWC | negative | down (0.55) | repeat | we've been screwed by tariffs used against us for years by China, by J | -0.19% | -0.05% | +0.40% | +1.12% |
| 13:27 | Mexico | EWW | neutral | down (0.55) | repeat | plants coming back from Mexico | +0.65% | +0.91% | +0.63% | -2.67% |
| 19:24 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | our country is really it's strong again. That is respectable. | +0.00% | +0.00% | +0.00% | +0.00% |
| 22:16 | General Motors | GM | positive | up (0.55) | repeat | General Motors and lithium, Americans are investing up to $1,600,000,0 | -0.05% | -0.75% | -2.22% | -4.16% |
| 36:32 | Oil | XLE, USO | positive | down (0.55) | unclear | Billions and billions of barrels of oil is coming out of Venezuela. | +1.83% | +0.61% | -0.12% | +5.49% |
| 36:34 | Venezuela | XLE, CVX | positive | up (0.55) | unclear | We're taking a lot of oil from Venezuela, and we're getting along grea | +1.83% | +0.61% | -0.12% | +5.49% |
| 40:40 | Oil | XLE, USO, XOM, CVX | negative | up (0.55) | repeat | radical left wants to ban a thing called gasoline | +1.83% | +0.61% | -0.12% | +5.49% |
| 41:42 | Electric vehicles | TSLA, RIVN, GM | negative | none (0.55) | repeat | These people are crazy. And I like electric cars. We sell 7%. | -1.45% | -0.33% | +1.74% | +4.67% |
| 49:34 | Dell | DELL | positive | up (0.55) | repeat | Go out and buy a Dell computer. | -2.68% | -2.66% | -2.38% | +5.82% |
| 49:39 | Micron | MU | positive | none (0.55) | repeat | Brad Mercer, Micron, Apple, so many companies. | -5.66% | +0.19% | -2.20% | +5.29% |
| 49:39 | Apple | AAPL | positive | none (0.55) | repeat | Brad Mercer, Micron, Apple, so many companies. | +1.02% | +0.51% | +0.30% | -2.90% |
| 68:51 | Iran | XLE, USO, ITA | negative | down (0.55) | repeat | as soon as this situation ends with Iran, oil is gonna go down | +1.83% | +0.61% | -0.12% | +5.49% |
| 68:51 | Oil | XLE, USO, XOM, CVX | positive | down (0.58) | repeat | oil is gonna go down to the floor, gasoline's gonna go down | +1.83% | +0.61% | -0.12% | +5.49% |
| 69:57 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | largest prescription drug price cuts in the history of our country | +1.15% | -0.51% | +0.48% | +1.52% |
| 72:01 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.60) | unclear | stop all payments to big insurance companies and give the money direct | +0.56% | -1.51% | -1.82% | -4.37% |

### Signs an Executive Order, Aug. 3, 2026 — `EtctNOj2gz4`
_the President Signs an Executive Order, Aug. 3, 2026 (The White House); stream start 2026-08-03 13:34 ET; 56 min; 11 heads-ups / 5 confirmed / 6 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 28:56 | United Kingdom | EWU | negative | none (0.55) | repeat | You keep it closed, you're gonna be a bankrupt country, which is what  | · | +0.10% | -1.35% | -1.26% |
| 30:58 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.55) | repeat | Windmills, you lose your shirt. | · | -0.45% | +2.15% | -1.01% |
| 32:12 | Oil | XLE, USO, XOM, CVX | negative | down (0.50) | unclear | They're making too much money. I don't like it. | · | -0.46% | -2.19% | +0.41% |
| 32:13 | Iran | XLE, USO, ITA | negative | down (0.62) | new | When we're finished with Iran, you're gonna see prices drop through th | · | -0.46% | -2.19% | +0.41% |
| 35:25 | Uber | UBER | positive | none (0.55) | repeat | They used to have to take Uber | · | +0.34% | -0.59% | +7.67% |

### Hosts a Cabinet Meeting, Jul. 31, 2026 — `V6vuYip9SWo`
_the President Hosts a Cabinet Meeting, Jul. 31, 2026 (The White House); stream start 2026-07-31 11:26 ET; 57 min; 30 heads-ups / 19 confirmed / 11 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:18 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | cyber attack, they blame it on Iran. I don't think so. | · | -0.70% | -2.66% | -6.95% |
| 3:44 | Walmart | WMT | positive | none (0.55) | repeat | Walmart, Sam's Club, Giant Eagle slashing prices by hundreds | · | -0.50% | -3.00% | -4.08% |
| 4:00 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market has set 73 all time record highs since the election | · | +0.00% | +0.00% | +0.00% |
| 7:15 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | achieving record discounts on prescription drugs | · | -0.38% | -2.33% | -2.31% |
| 8:38 | Germany | EWG | negative | none (0.55) | repeat | if you don't do it, we're gonna have to charge you tariffs | · | -0.30% | -0.66% | -1.26% |
| 9:21 | Health insurers | UNH, CI, ELV, HUM | negative | none (0.50) | repeat | What they've done Obamacare is a total disaster. It's a costly wreck. | · | -0.55% | -3.51% | -7.59% |
| 15:19 | Venezuela | XLE, CVX | positive | none (0.50) | unclear | we have a great relationship with Venezuela. We're working with partne | · | -0.24% | -2.31% | -6.60% |
| 15:30 | Oil | XLE, USO | positive | none (0.50) | unclear | taking out tens of millions of barrels of oil | · | -0.24% | -2.31% | -6.60% |
| 15:38 | Refiners | VLO, MPC, PSX | positive | up (0.58) | new | taking out tens of millions of barrels of oil and going to Houston, go | · | -0.39% | -2.19% | -7.29% |
| 32:21 | Banks | XLF, KRE, JPM, BAC | positive | up (0.52) | repeat | Small banks, community banks are lending again | · | -0.15% | -1.35% | -3.07% |
| 37:47 | Novo Nordisk | NVO | neutral | down (0.60) | repeat | list price for Ozempic was $1,350 | · | -0.77% | -1.99% | -3.73% |
| 38:39 | Amazon | AMZN | positive | up (0.55) | unclear | We have deals with Amazon and with GoodRx. | · | +0.60% | +3.66% | -1.98% |
| 39:07 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | 300,000 Americans saving $3,700 a year on pharmaceuticals | · | -0.26% | -2.16% | -2.14% |
| 40:46 | Israel | EIS, ITA | positive | none (0.50) | repeat | Israel would no longer be with us in big parts of the Middle East | · | +0.21% | -1.55% | -0.30% |
| 48:43 | RTX (Raytheon) | RTX | positive | up (0.55) | repeat | Tomahawk missile is the most incredible | · | -0.21% | -1.14% | -0.27% |
| 49:36 | Lockheed Martin | LMT | neutral | none (0.52) | repeat | I gave them the javelins | · | +0.02% | -0.60% | -2.41% |
| 50:08 | Nvidia | NVDA | positive | none (0.55) | repeat | It's a little like, Nvidia. | · | +0.84% | +3.20% | +9.91% |
| 52:11 | Iran | XLE, USO, ITA | neutral | up (0.55) | unclear | I'm losing faith in them | · | +0.14% | -2.09% | -6.38% |
| 55:03 | Russia | RSX, XLE | neutral | none (0.52) | repeat | I think Putin wants to make a deal. He seems very reluctant to make co | · | · | · | · |

### Makes an Announcement on Freedom Haulers — `coFYdHAjdXs`
_the President Makes an Announcement on Freedom Haulers (The White House); stream start 2026-07-30 13:23 ET; 20 min; 6 heads-ups / 2 confirmed / 4 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:45 | Trucking / rail | IYT, UNP, CSX, WERN | positive | up (0.55) | unclear | representatives from the American Trucking Association | · | +0.16% | -0.16% | -1.45% |
| 2:17 | FedEx | FDX | positive | none (0.55) | repeat | thank UPS, FedEx, and Werner | · | +0.12% | -0.58% | -0.73% |

### Makes an Announcement with the Secretary of Transportation — `sCPQKhHlN9k`
_the President Makes an Announcement with the Secretary of Transportation (The White House); stream start 2026-07-29 15:02 ET; 37 min; 19 heads-ups / 14 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:50 | Airlines | JETS, DAL, UAL, AAL | positive | none (0.50) | repeat | safety of airlines and getting in with the control towers and all new  | · | · | +0.29% | +2.36% |
| 1:16 | United Airlines | UAL | positive | up (0.55) | unclear | Thanks as well to the CEO of United Airlines, Scott Kirby. | · | · | +0.65% | +4.35% |
| 8:23 | Nvidia | NVDA | positive | none (0.55) | repeat | a very great gentleman, if we can do with an airport like he does with | · | · | -0.17% | +8.45% |
| 8:37 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | his chips are a little bit more complicated | · | · | +2.80% | +4.90% |
| 11:30 | Airlines | JETS, DAL, UAL, AAL | neutral | none (0.50) | repeat | He's been very much involved with what we've done and other airlines t | · | · | +0.39% | +2.47% |
| 12:57 | United Airlines | UAL | positive | up (0.55) | unclear | United Airlines, the Air Force Authority, and the other airlines have  | · | · | +0.88% | +4.61% |
| 21:42 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.50) | repeat | He's got windmills all over the place. Every anytime you see windmills | · | · | +2.27% | +1.41% |
| 22:02 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | Norway gets it from the North Sea. They get their oil from the North S | · | · | +0.20% | -6.42% |
| 24:10 | China | FXI, MCHI, KWEB | positive | none (0.50) | repeat | We have the strongest investment ever made in a country of any country | · | · | -0.29% | -5.33% |
| 24:16 | Nvidia | NVDA | positive | none (0.52) | repeat | Jensen's spending hundreds of billions of dollars. | · | · | +0.12% | +8.82% |
| 24:58 | Toyota | TM | positive | up (0.55) | unclear | Toyota just announced they're building 1 of the largest | · | · | -2.46% | -9.14% |
| 27:27 | Airlines | JETS, DAL, UAL, AAL | neutral | none (0.50) | unclear | airlines who participate in the project are going to pay for it | · | · | +0.57% | +2.67% |
| 30:11 | Stargate AI project | ORCL, SFTBY, NVDA | negative | none (0.55) | unclear | Stargate did very little about it. | · | · | +5.59% | +15.82% |
| 34:24 | Iran | XLE, USO, ITA | negative | up (0.52) | new | I'd like them to add Iran as tariffs | · | · | -0.50% | -7.14% |

### Makes an Announcement on American Nuclear Innovation — `jAUidIyneEA`
_the President Makes an Announcement on American Nuclear Innovation (The White House); stream start 2026-07-24 15:01 ET; 39 min; 31 heads-ups / 13 confirmed / 18 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:36 | Nuclear energy | URA, CCJ, OKLO, SMR | positive | up (0.60) | repeat | historic milestone for civilian nuclear energy and incredible renaissa | · | · | +1.26% | -2.96% |
| 10:28 | New York Times | NYT | negative | none (0.55) | repeat | A failing New York Times. I just | · | · | +0.26% | +2.68% |
| 12:33 | ExxonMobil | XOM | neutral | none (0.52) | unclear | the big companies, you know, Exxon, all the big companies are | · | · | -1.66% | -2.31% |
| 13:02 | Venezuela | XLE, CVX | positive | none (0.50) | unclear | oil is being sent to Houston and Louisiana to be refined, we paid for  | · | · | -2.62% | -1.70% |
| 13:19 | Oil | XLE, USO | positive | none (0.50) | repeat | Venezuela is selling millions and millions of barrels of oil. | · | · | -2.62% | -1.70% |
| 15:57 | Mexico | EWW | negative | down (0.65) | new | put a major tariff on tax on Mexico | · | · | +1.18% | +0.46% |
| 16:01 | Canada | EWC | negative | down (0.60) | new | put a big tariff on Canada because of the smoke | · | · | +0.49% | -0.58% |
| 19:00 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | windmills for quite a long time. They're very ugly. | · | · | +0.70% | -4.74% |
| 20:00 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | They're made in China, but China doesn't use them. China uses coal. | · | · | +1.66% | +4.10% |
| 23:55 | Natural gas / LNG | UNG, LNG, EQT | positive | up (0.55) | repeat | ban on LNG exports from our country. Now we're the world's largest | · | · | -4.30% | -5.85% |
| 24:32 | Iran | XLE, USO, ITA | negative | up (0.55) | repeat | previous administration sanctioned more than Iran | · | · | -2.61% | -1.69% |
| 37:28 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | Barack Hussein Obama's nuclear deal that was so bad with Iran | · | · | -2.30% | -1.38% |
| 37:33 | Northrop Grumman | NOC | positive | up (0.55) | repeat | that beautiful plane, the wing, it carries the largest bombs | · | · | +0.90% | -1.12% |

### Makes an Announcement on the Ratepayer Protection Pledge — `ebICSW2yVww`
_the President Makes an Announcement on the Ratepayer Protection Pledge (The White House); stream start 2026-07-23 14:20 ET; 34 min; 19 heads-ups / 16 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2:59 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | new data centers go up all over, electricity bills for American famili | · | -0.29% | -0.96% | -7.00% |
| 5:56 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.50) | repeat | They make the windmills, but they don't use them. | · | -0.05% | -2.83% | -5.94% |
| 6:24 | Bitcoin | IBIT, COIN, MSTR | positive | none (0.52) | repeat | We're leading China in crypto. We wanna stay in front. | · | +0.12% | -0.96% | -0.38% |
| 9:32 | Toyota | TM | positive | up (0.55) | repeat | companies are pouring in [[Toyota]] | · | -0.01% | +0.33% | +7.90% |
| 10:02 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | repeat | same thing with chips | · | +0.33% | -2.97% | -7.20% |
| 10:09 | Semiconductors | SMH, SOXX | positive | up (0.55) | repeat | We'll have about 50% of the chip market by term end. | · | +0.33% | -2.97% | -7.20% |
| 10:17 | Intel | INTC | neutral | up (0.55) | repeat | We had Intel, we had virtually none other than Intel. | · | +1.12% | -7.43% | -9.00% |
| 14:24 | Google | GOOGL | positive | none (0.55) | repeat | Google's data center construction is allowing them to eliminate proper | · | -0.51% | -0.19% | +3.79% |
| 14:24 | Artificial intelligence / data centers | NVDA, MSFT, SMH, VRT | positive | none (0.50) | repeat | Google's data center construction revenue allowing property tax elimin | · | -0.36% | -1.03% | -7.07% |
| 17:11 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | lead the world in AI and high-tech | · | -0.56% | -1.11% | -7.14% |
| 18:05 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | surrender the AI race to China | · | -0.04% | +0.20% | +5.45% |
| 18:55 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | regulating oil, natural gas, and clean beautiful coal | · | -0.35% | -0.32% | -1.80% |
| 18:55 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.52) | repeat | regulating oil, natural gas, and clean beautiful coal | · | +0.06% | -0.93% | -6.39% |
| 18:57 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | clean beautiful coal | · | +0.06% | -4.30% | -10.56% |
| 20:06 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | just like we did with the Green New scam | · | +0.26% | -2.80% | -5.91% |
| 22:58 | Oil | XLE, USO | positive | none (0.50) | repeat | We're taking millions and millions of barrels of oil, it's going to Ho | · | -0.30% | -0.35% | -1.83% |

### Participates in a Press Conference, Jul. 8, 2026 — `9JYvcEVlu3s`
_the President Participates in a Press Conference, Jul. 8, 2026 (The White House); stream start 2026-07-08 11:05 ET; 40 min; 31 heads-ups / 27 confirmed / 4 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:04 | Defense | ITA, XAR, LMT, RTX | positive | up (0.55) | repeat | dramatically increase the defense spending | · | -0.69% | -2.10% | -3.84% |
| 6:01 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.60) | repeat | taking in over 1 trillion dollars a year toward defense | · | -0.69% | -2.10% | -3.84% |
| 7:25 | RTX (Raytheon) | RTX | positive | up (0.60) | repeat | Tomahawks and everything we have is considered to be the best. | · | -0.67% | -3.26% | -3.33% |
| 7:36 | Lockheed Martin | LMT | positive | up (0.60) | repeat | I had [[Lockheed]] and, we make the best equipment, the Patriots and t | · | +0.25% | -3.44% | -4.58% |
| 7:43 | Boeing | BA | positive | up (0.55) | repeat | We make the best equipment. I wish we made it faster because we could  | · | -0.81% | -2.40% | -5.02% |
| 10:22 | Eli Lilly | LLY | positive | none (0.55) | repeat | Eli Lilly is building plants, big drug | · | +0.29% | -2.10% | -7.43% |
| 10:24 | Merck | MRK | positive | none (0.52) | repeat | Merck, all of them, the drug companies are building. | · | +0.99% | -1.87% | -3.45% |
| 10:26 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | none (0.50) | repeat | all of them, the drug companies are building | · | +0.52% | -1.72% | -4.52% |
| 10:28 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | repeat | car companies are building like crazy | · | -0.61% | -0.02% | +0.87% |
| 10:34 | Toyota | TM | positive | up (0.55) | repeat | car companies are building like crazy. In fact, as you probably saw a  | · | -0.05% | -2.30% | -1.25% |
| 10:36 | Mexico | EWW | negative | down (0.58) | unclear | Toyota is leaving Mexico and they're gonna build in Texas. | · | -0.22% | -0.95% | +0.18% |
| 10:51 | Japan | EWJ | neutral | down (0.55) | repeat | if you build in Japan or if you build in | · | -0.16% | +0.73% | +0.29% |
| 10:54 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | China is a much higher tariff versus a 100% tariff | · | -0.07% | -1.57% | +0.60% |
| 11:11 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI plants, and all other plants, pharmaceutical plants | · | +0.21% | +1.77% | +6.29% |
| 11:15 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | pharmaceutical plants, chips | · | -0.90% | +2.56% | -0.75% |
| 11:31 | Semiconductors | SMH, SOXX | negative | down (0.55) | repeat | if they make a chip... they have to pay 100%, 200%, 250% | · | -0.90% | +2.56% | -0.75% |
| 12:50 | TikTok | ORCL | neutral | none (0.50) | repeat | I was watching somebody say, oh, the TikTok deal. | · | -1.27% | +1.79% | -7.00% |
| 15:34 | European Union | VGK, EZU, FEZ, LMT | positive | none (0.50) | unclear | $3,000,000,000 of new defense investments with US companies, Lockheed  | · | -0.19% | -0.59% | -0.20% |
| 15:43 | Northrop Grumman | NOC | positive | up (0.65) | new | Northrop Grumman is moving forward with the sale of advanced American  | · | +0.29% | -3.50% | -5.20% |
| 16:16 | Anduril | PLTR | positive | none (0.50) | unclear | Anduril is announcing a deal to build their | · | +0.31% | -0.80% | +2.45% |
| 17:13 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | we're doing great on steel because we charge tariffs | · | · | · | · |
| 17:43 | Aluminum | AA, CENX | positive | up (0.55) | new | We're gonna have the largest aluminum plant in the world | · | -2.42% | -1.78% | -2.48% |
| 21:05 | Iran | XLE, USO, ITA | positive | down (0.52) | repeat | The Iran war has been a tremendous military success. | · | +0.89% | -2.56% | +0.04% |
| 21:41 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | oil prices are lower than they were when I started | · | +0.89% | -2.56% | +0.04% |
| 27:19 | TikTok | ORCL | neutral | none (0.55) | repeat | I talk about it on TikTok, and I talk about it everywhere. | · | +0.04% | +3.13% | -5.81% |
| 31:46 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | everything went to Iran | · | -0.87% | -3.45% | -0.86% |
| 38:29 | Lockheed Martin | LMT | positive | up (0.55) | new | they're talking about the f 35 | · | -0.32% | -3.70% | -4.84% |

### Signs Executive Orders, Jun. 29, 2026 — `oDzq7mNCK0Q`
_the President Signs Executive Orders, Jun. 29, 2026 (The White House); stream start 2026-06-29 15:21 ET; 14 min; 4 heads-ups / 3 confirmed / 1 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:29 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | oil prices are way down | · | · | -2.45% | +0.26% |
| 0:36 | Iran | XLE, USO, ITA | neutral | down (0.55) | repeat | oil prices are way down. It was higher than that prior to the denuclea | · | · | -2.45% | +0.26% |
| 11:24 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | I'm reducing drug prices by 200 | · | · | -2.05% | +1.42% |

### Signs Executive Orders, Jun. 22, 2026 — `HNipoXNANAs`
_the President Signs Executive Orders, Jun. 22, 2026 (The White House); stream start 2026-06-22 15:44 ET; 39 min; 28 heads-ups / 20 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:22 | Google | GOOGL | neutral | none (0.55) | repeat | We're honored to be joined by Google president Ruth Porat. | · | · | +0.37% | +1.53% |
| 5:17 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | taking out tremendous amounts of oil | · | · | +2.16% | -0.46% |
| 6:14 | Agriculture | DBA, MOS, DE, ADM | positive | up (0.50) | unclear | money that's being unfrozen is gonna be used to buy food exclusively t | · | · | +1.15% | -0.18% |
| 10:31 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | Moore's law in semiconductor manufacturing | · | · | -4.77% | -4.27% |
| 11:15 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | unclear | natural gas at precrisis levels | · | · | -1.14% | -2.73% |
| 12:37 | Google | GOOGL | positive | up (0.55) | unclear | They have Ruth from Alphabet. They are doing amazing | · | · | +0.37% | +1.53% |
| 12:43 | IBM | IBM | positive | up (0.62) | unclear | We invested in his fab. He's got a leading fab. | · | · | +8.14% | +12.41% |
| 16:28 | Iran | XLE, USO, ITA | neutral | down (0.60) | new | president lifted sanctions on Iranian oil today | +1.57% | +0.70% | +0.59% | -2.08% |
| 16:29 | Oil | XLE, USO, XOM, CVX | neutral | down (0.55) | new | president lifted sanctions on Iranian oil today | +1.57% | +0.70% | +0.59% | -2.08% |
| 16:51 | Agriculture | DBA, MOS, DE, ADM | positive | up (0.50) | new | money gonna be put into this country...purchases of food...our farmers | +1.31% | +0.61% | +1.16% | -0.24% |
| 18:58 | New York Times | NYT | negative | none (0.55) | repeat | The fake New York Times said, oh, it's about the same as it was 4 mont | +2.30% | +1.26% | +0.30% | -3.23% |
| 21:12 | Israel | EIS, ITA | neutral | none (0.50) | repeat | We're gonna take a look at it. I'm a problem solver. | +0.52% | -0.02% | +0.93% | -0.63% |
| 22:45 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.55) | repeat | you have windmills all over the place | -2.05% | -1.77% | -3.33% | -3.53% |
| 22:58 | United Kingdom | EWU | negative | none (0.52) | repeat | You're really messing up energy. Windmills all over the place. Won't l | +1.01% | +0.70% | +0.97% | +0.67% |
| 24:22 | General Motors | GM | neutral | up (0.55) | new | They're dealing with General Motors. Now they're spending a lot of mon | -0.12% | -0.44% | -0.34% | -4.48% |
| 24:24 | Ford | F | neutral | none (0.52) | unclear | They're dealing with Ford. Now they're spending a lot of money. We're  | -0.49% | -0.25% | -0.42% | -1.81% |
| 24:35 | RTX (Raytheon) | RTX | positive | none (0.50) | unclear | We're gonna build weapons, including the Patriot, including the Tomaha | +2.06% | +2.08% | +3.27% | +4.02% |
| 24:45 | Automakers | GM, F, STLA, TSLA | positive | up (0.65) | new | car companies, if they have any excess capacity, we're gonna build wea | -0.12% | -0.44% | -0.34% | -4.48% |
| 24:53 | RTX (Raytheon) | RTX | positive | up (0.55) | unclear | some of the car companies, if they have any excess capacity, they're m | +2.06% | +2.08% | +3.27% | +4.02% |
| 37:56 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | overwhelming military victory that has been had over Iran | +1.57% | +0.70% | +0.59% | -2.08% |

### Holds a Press Conference, Jun. 17, 2026 — `90D179dxdCM`
_the President Holds a Press Conference, Jun. 17, 2026 (The White House); stream start 2026-06-17 11:49 ET; 69 min; 45 heads-ups / 30 confirmed / 15 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:17 | Stock market | SPY, QQQ, DIA | positive | up (0.55) | repeat | stock market has surged to record highs | · | +0.00% | +0.00% | +0.00% |
| 1:26 | Oil | XLE, USO, XOM, CVX | positive | down (0.60) | unclear | oil is dropping | · | -0.36% | -1.91% | +0.33% |
| 9:47 | Banks | XLF, KRE, JPM, BAC | negative | none (0.50) | repeat | loaded up a plane with $1,700,000,000 in green cash from banks all ove | · | -0.31% | -1.69% | -0.25% |
| 9:58 | Boeing | BA | neutral | none (0.55) | repeat | loaded up a plane with $1.7 billion in green cash into a Boeing 757 | · | +0.81% | -1.96% | -2.32% |
| 10:28 | Israel | EIS, ITA | positive | none (0.52) | repeat | Israel would have been blown away. | · | +0.05% | +0.67% | -0.24% |
| 15:24 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | unclear | it's like a steel wall | · | · | · | · |
| 15:34 | Northrop Grumman | NOC | positive | none (0.50) | repeat | if we didn't hit that with the b 2 bombers or if it wasn't successful | · | -0.16% | -5.91% | -8.23% |
| 16:37 | Iran | XLE, USO, ITA | neutral | down (0.55) | unclear | the deal we reached, with Iran on Sunday | · | -0.36% | -1.91% | +0.33% |
| 22:06 | Stock market | SPY, QQQ, DIA | positive | up (0.55) | repeat | the stock market will, I believe, continue to rise | · | +0.00% | +0.00% | +0.00% |
| 22:53 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | he raised interest rates too fast all at the same time | · | -0.08% | +0.85% | +3.20% |
| 27:56 | Northrop Grumman | NOC | positive | up (0.58) | unclear | Those b 2 bombers are unbelievable. | · | -0.16% | -5.91% | -8.23% |
| 29:34 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | The big deal is the Iran deal. That's where the money is, where the po | · | -0.36% | -1.91% | +0.33% |
| 34:04 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | It's gonna be the biggest thing ever. We have to be very careful with  | · | +0.37% | +2.49% | -3.09% |
| 34:17 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | We're leading China. We're leading the world on that. | · | -0.32% | -2.17% | -5.25% |
| 37:07 | Rare earths | MP, REMX | positive | · | · | accelerate our efforts to secure our critical minerals and rare earth  | · | +2.54% | +2.34% | -4.80% |
| 40:28 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | the worst inflation ever...because the oil is bringing it down | · | -0.36% | -1.91% | +0.33% |
| 43:30 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | I would really appreciate you're not giving or selling any of that stu | · | +0.20% | -1.55% | +0.69% |
| 46:30 | Comcast (NBC, MSNBC) | CMCSA | negative | none (0.55) | repeat | NBC is terrible. | · | -0.11% | -2.20% | +0.59% |
| 46:32 | Paramount (CBS) | PSKY | negative | none (0.55) | repeat | NBC is terrible, and CBS is terrible. | · | -0.00% | -1.24% | -4.63% |
| 46:33 | Warner Bros. Discovery (CNN) | WBD | negative | none (0.52) | repeat | CNN, obviously. | · | -0.17% | -0.65% | +3.95% |
| 49:22 | Israel | EIS, ITA | positive | none (0.50) | repeat | we'll work with Israel and get it done | · | +0.02% | +0.62% | -0.29% |
| 51:01 | Oil | XLE, USO, XOM, CVX | neutral | none (0.50) | repeat | if people want to invest, it does have oil | · | +0.20% | -1.55% | +0.69% |
| 52:04 | Oil | XLE, USO | neutral | none (0.50) | repeat | You have probably the 3rd largest oil reserves in the world. | · | +0.20% | -1.55% | +0.69% |
| 57:00 | Iran | XLE, USO, ITA | negative | down (0.60) | repeat | we're gonna have to put out the fire in Iran | · | +0.20% | -1.55% | +0.69% |
| 57:28 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | The people are great. I want it by so much. And I love the people, far | · | +0.17% | -0.25% | +2.49% |
| 58:21 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | I thought the stock market would go down 25 or 30%. | · | +0.00% | +0.00% | +0.00% |
| 59:46 | Disney (ABC) | DIS | negative | none (0.55) | repeat | You're from ABC. You're fake news. | · | +0.15% | +2.58% | -1.50% |
| 62:00 | United Kingdom | EWU | neutral | none (0.55) | unclear | I said, it'd be nice if you send some ships. | · | +0.04% | -1.66% | +0.90% |
| 62:35 | Israel | EIS, ITA | neutral | none (0.52) | repeat | We did it ourselves with Israel and with the Arab states | · | +0.02% | +0.62% | -0.29% |
| 65:08 | China | FXI, MCHI, KWEB | positive | up (0.55) | unclear | China's been terrific. I told you that before. | · | +0.19% | -1.85% | -4.95% |

### Makes an Announcement on Beautiful, Clean Coal — `eafk0lNExQE`
_the President Makes an Announcement on Beautiful, Clean Coal (The White House); stream start 2026-06-04 15:13 ET; 76 min; 48 heads-ups / 35 confirmed / 13 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:08 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | clean, beautiful coal | · | · | -7.56% | -13.15% |
| 7:02 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | If you look at China, if you look at so many of the successful countri | · | · | +0.51% | +0.93% |
| 7:46 | Microsoft | MSFT | neutral | none (0.55) | repeat | sold his company to, I think, Microsoft | · | · | +0.09% | -6.09% |
| 8:50 | Coal | BTU, ARCH, AMR | positive | up (0.68) | new | $700,000,000 investment, protect 14 coal plants and 42 coal mines | · | · | -7.56% | -13.15% |
| 9:25 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.58) | repeat | They talk about some but there's no no real alternative. | · | · | -6.58% | -9.09% |
| 9:36 | European Union | VGK, EZU, FEZ | negative | none (0.50) | repeat | stupid people from The United States, the suckers. And all over Europe | · | · | +0.69% | +3.29% |
| 10:22 | Automakers | GM, F, STLA, TSLA | negative | none (0.50) | unclear | They don't want people to fix their car. That's strange. | · | · | +1.27% | -0.27% |
| 11:12 | General Motors | GM | neutral | none (0.55) | unclear | great meeting yesterday with the head of General Motors | · | · | +1.27% | -0.27% |
| 11:15 | Ford | F | positive | none (0.52) | unclear | great meeting yesterday with Roger Penske, head of Ford | · | · | -0.01% | -1.28% |
| 18:07 | Coal | BTU, ARCH, AMR | positive | up (0.62) | new | approved 76 permits for clean, beautiful coal | · | · | -7.86% | -13.42% |
| 20:02 | Coal | BTU, ARCH, AMR | positive | up (0.62) | unclear | coal mining projects we've approved in less than 1 month | · | · | -7.86% | -13.42% |
| 20:50 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | unclear | without metallurgical coal, we don't have the steel industry | · | · | · | · |
| 28:00 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | Solar is irrelevant in the winter | · | · | -6.82% | -9.32% |
| 30:54 | Coal | BTU, ARCH, AMR | positive | up (0.60) | repeat | regulation after regulation trying to strangulate coal to destroy it | · | · | -7.86% | -13.42% |
| 33:54 | Rare earths | MP, REMX, BTU | positive | none (0.50) | unclear | companies like Peabody can get rare earth minerals and critical minera | · | · | -6.60% | -9.69% |
| 37:13 | Homebuilders | FNMA, XHB, ITB, LEN | positive | up (0.60) | repeat | done a phenomenal job at Fannie Mae | · | · | +2.59% | -3.10% |
| 41:30 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | windmills cost a fortune. They break. They kill the birds. They're bad | · | · | -6.82% | -9.32% |
| 44:56 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | European countries need it tremendous. They should have helped. | · | · | +0.68% | +3.27% |
| 48:00 | Ukraine | ITA, XLE | neutral | none (0.52) | repeat | Ukraine has been given a tremendous amount of our mil. | +0.13% | +0.53% | +0.50% | +2.98% |
| 51:36 | Venezuela | XLE, CVX | positive | none (0.50) | repeat | The relationship with Venezuela is incredible. We've taken out million | +0.50% | +0.22% | +1.65% | -0.02% |
| 51:40 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | We've taken out millions and millions of oil out of Venezuela. It's ve | +0.50% | +0.22% | +1.65% | -0.02% |
| 52:18 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | cannot let Iran have a nuclear weapon | +0.50% | +0.22% | +1.65% | -0.02% |
| 53:30 | Northrop Grumman | NOC | positive | up (0.55) | repeat | this beautiful plane right here, the b 2 bomber | +1.52% | +1.07% | +1.56% | +2.97% |
| 59:25 | RTX (Raytheon) | RTX | positive | none (0.52) | repeat | we hit it with tomahawks | +0.50% | +1.93% | +1.94% | +4.32% |
| 61:05 | Germany | EWG | negative | down (0.55) | repeat | bringing cars back from Germany. We lost the car industry. | +0.21% | -0.05% | +0.20% | +0.26% |
| 63:45 | Venezuela | XLE, CVX | neutral | none (0.50) | repeat | We lost not 1 soldier in Venezuela. We didn't lose 1 soldier. | +0.50% | +0.22% | +1.65% | -0.02% |
| 64:11 | Intercontinental Exchange (NYSE) | ICE | positive | none (0.52) | repeat | New York Stock Exchange just hit a new all time high | +1.01% | +0.48% | +0.24% | +0.95% |
| 64:15 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | every other exchange just hit a new all time high | +0.00% | +0.00% | +0.00% | +0.00% |
| 65:48 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI is a big deal. | -1.26% | -2.35% | -2.22% | -4.13% |
| 68:02 | Harley-Davidson | HOG | negative | none (0.50) | repeat | They wouldn't let Harley as an example | -0.07% | +0.63% | +4.66% | +7.32% |
| 68:06 | Harley-Davidson | HOG | negative | none (0.55) | repeat | they wouldn't let Harley as an example, in the past, they wouldn't let | -0.07% | +0.63% | +4.66% | +7.32% |
| 68:37 | India | INDA, EPI | positive | none (0.50) | repeat | we'll make a lot of money with India | +0.61% | +0.40% | +0.67% | +2.67% |
| 72:41 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | repeat | We had a great meeting with the auto, most of them were here. | -0.87% | +0.23% | +3.02% | -0.04% |
| 73:16 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | got rid of a lot of environmental restrictions | +0.50% | +0.22% | +1.65% | -0.02% |
| 73:29 | Electric vehicles | TSLA, RIVN, GM | negative | none (0.50) | repeat | getting rid of the electric vehicle mandate | +1.12% | -1.77% | +0.09% | -0.85% |

### Signs Executive Orders, Jun. 3, 2026 — `4EUzlV7-Dew`
_the President Signs Executive Orders, Jun. 3, 2026 (The White House); stream start 2026-06-03 15:50 ET; 43 min; 11 heads-ups / 8 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 23:24 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | we had the strongest stock market in history | +0.00% | +0.00% | +0.00% | +0.00% |
| 27:33 | Northrop Grumman | NOC | positive | up (0.55) | repeat | those beautiful b 2 right here, the b 2 bombers | +1.51% | +1.66% | +5.70% | +7.21% |
| 30:13 | Israel | EIS, ITA | positive | none (0.50) | repeat | He's been a great partner. For me, he's been very good. | -0.70% | -0.75% | -2.36% | +0.82% |
| 31:38 | Boeing | BA | neutral | none (0.55) | repeat | 1,700,000,000 put into a Boeing 7 5 7 | +1.43% | +2.87% | +4.53% | +7.43% |
| 31:48 | Banks | XLF, KRE, JPM, BAC | negative | none (0.52) | repeat | 1,700,000,000 in cash taken from the banks in DC | +1.60% | +2.24% | +5.02% | +5.63% |
| 34:47 | Warner Bros. Discovery (CNN) | WBD | negative | down (0.55) | repeat | The fake news like CNN | +0.62% | +0.34% | -0.60% | +1.67% |
| 34:48 | New York Times | NYT | negative | none (0.55) | repeat | The fake news like CNN, like the New York Times and like others, have  | +1.43% | +2.16% | +4.49% | +0.89% |
| 39:05 | Berkshire Hathaway | BRK.B | positive | none (0.50) | unclear | Was partners in a deal with them. I made a lot of money. | · | · | · | · |

### Participates in a Cabinet Meeting, May 27, 2026 — `ln-FnwDYE4Y`
_the President Participates in a Cabinet Meeting, May 27, 2026 (The White House); stream start 2026-05-27 11:26 ET; 80 min; 44 heads-ups / 22 confirmed / 22 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:59 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market has set 68 all time record highs since the election | · | +0.00% | +0.00% | +0.00% |
| 5:10 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | most favored nation agreements... having to do with medical... drug pr | · | -0.48% | +0.20% | -1.98% |
| 5:43 | Germany | EWG | neutral | none (0.55) | repeat | a pill that would sell in Germany or in London | · | -0.18% | -1.18% | -2.78% |
| 5:45 | United Kingdom | EWU | neutral | none (0.55) | repeat | a pill that would sell in Germany or in London | · | -0.09% | -1.32% | -2.50% |
| 13:28 | Health insurers | UNH, CI, HUM, ELV | positive | none (0.52) | repeat | took down 2 of the largest Medicaid fraud cases in Minnesota history | · | -0.04% | -0.86% | -2.25% |
| 15:04 | Russia | RSX, XLE | negative | none (0.55) | repeat | Russia Russia Russia hoax, a great hoax, a very dangerous hoax | · | · | · | · |
| 18:40 | Agriculture | DBA, MOS, DE, CORN | neutral | none (0.50) | repeat | Brooke at the Department of Agriculture, we send hundreds of billions  | · | -0.16% | -0.46% | -3.03% |
| 30:37 | Venezuela | XLE, CVX | positive | none (0.50) | unclear | 10,000,000 barrels of Venezuelan oil delivered to US since January 3 | · | +0.28% | -1.00% | +2.13% |
| 30:37 | Oil | XLE, USO, XOM, CVX | neutral | none (0.52) | unclear | selling oil in the market at market rates, money controlled by Treasur | · | +0.28% | -1.00% | +2.13% |
| 31:14 | GE Aerospace | GE | negative | none (0.55) | unclear | controls 70% of the economy. None of the money goes to help the Cuban  | · | +0.15% | +0.92% | -0.99% |
| 35:06 | Oil | XLE, USO | positive | up (0.55) | repeat | California has tremendous oil reserves. Used to be number 3 in the nat | · | +0.28% | -1.00% | +2.13% |
| 51:29 | Mexico | EWW | neutral | none (0.55) | unclear | from Pennsylvania to New Mexico, where I'll be tomorrow | · | -0.48% | -2.02% | -2.88% |
| 55:16 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | Oil will be lower than pre conflict levels when this ends. | · | +0.28% | -1.00% | +2.13% |
| 55:20 | Natural gas / LNG | UNG, LNG, EQT | positive | down (0.55) | repeat | Natural gas is already down. | · | +0.60% | +4.82% | +3.28% |
| 55:24 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | drug and pharmaceutical prices, they are plummeting | · | -0.48% | +0.20% | -1.98% |
| 64:24 | Oil | XLE, USO | positive | none (0.50) | repeat | 4,000,000 barrels of oil at 1 boat | · | +0.20% | -1.28% | +1.84% |
| 65:43 | Oil | XLE, USO, XOM, CVX | negative | down (0.55) | repeat | gas prices that are still high across the country | · | +0.20% | -1.28% | +1.84% |
| 66:02 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | We have tremendous amounts of energy. We're blessed with something ver | · | +0.59% | +10.50% | +14.40% |
| 66:26 | Northrop Grumman | NOC | neutral | none (0.52) | repeat | if we didn't hit them with the b 2 bombers | · | +0.18% | +0.47% | -5.49% |
| 66:40 | Iran | XLE, USO, ITA | negative | down (0.55) | repeat | I terminated the Obama deal, the Iran nuclear deal | · | +0.20% | -1.28% | +1.84% |
| 67:04 | Nuclear energy | URA, CCJ, OKLO, SMR | negative | none (0.52) | repeat | I wouldn't be comfortable. No sanctions. No money. | · | +0.05% | +0.20% | -0.47% |
| 77:35 | Iran | XLE, USO, ITA | negative | none (0.50) | unclear | If they don't sign to join the Abraham Accords, I don't know that we y | · | +0.20% | -1.28% | +1.84% |

### Participates in an Announcement with the Administrator of the EPA — `XU5-cs4Esio`
_the President Participates in an Announcement with the Administrator of the EPA (The White House); stream start 2026-05-21 11:29 ET; 49 min; 15 heads-ups / 9 confirmed / 6 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:42 | Semiconductors | SMH, SOXX, NVDA, INTC | negative | up (0.55) | new | rule...created national security risk by adding hurdles to manufacturi | · | +0.24% | +1.87% | +4.43% |
| 24:19 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | unclear | It's like a steel wall. It's our navy. | · | · | · | · |
| 25:43 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | No ship is going to or out of Iran without our approval. | · | -0.13% | -1.42% | -8.24% |
| 25:49 | Nuclear energy | URA, CCJ, OKLO, SMR | negative | none (0.50) | repeat | Can they keep their highly enriched uranium? | · | -0.08% | +0.88% | +3.16% |
| 27:20 | Oil | XLE, USO, XOM, CVX | neutral | down (0.55) | repeat | when it ends, your gasoline prices will go down lower than they were b | · | -0.13% | -1.42% | -8.24% |
| 32:09 | Artificial intelligence | NVDA, SMH | negative | none (0.52) | new | I didn't like certain aspects of it. I postponed it. | · | +0.31% | -2.54% | -5.92% |
| 41:13 | Uber | UBER | neutral | none (0.55) | repeat | they take [[Uber]] or something, and they were they felt unsafe even i | · | -0.19% | -2.77% | -6.18% |
| 43:18 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | I had to do a journey to Iran. I had to say, you know, we just hit the | · | -0.13% | -1.42% | -8.24% |
| 43:22 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | the stock market today | · | +0.00% | +0.00% | +0.00% |

### Participates in a Healthcare Affordability Event, May 18, 2026 — `qCf6OPSGvac`
_the President Participates in a Healthcare Affordability Event, May 18, 2026 (The White House); stream start 2026-05-18 16:19 ET; 31 min; 12 heads-ups / 8 confirmed / 4 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:33 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | largest discounts on prescription drugs in the history of our country | +0.46% | +2.01% | +0.62% | +0.51% |
| 4:22 | Amazon | AMZN | positive | up (0.55) | unclear | Vice president of Amazon Pharmacy, Tanvi Patel. Thank you very much. | -0.54% | -2.09% | -0.30% | +1.04% |
| 6:00 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | administrator for the Centers for Medicare and Medicaid Services | +0.24% | +1.19% | -2.35% | -3.42% |
| 17:11 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | pharmaceutical companies to come sit with us to make their product por | +0.46% | +2.01% | +0.62% | +0.51% |
| 20:46 | Iran | XLE, USO, ITA | neutral | down (0.55) | new | no nuclear weapon going into the hands of Iran | +0.90% | +1.36% | -1.64% | -7.52% |
| 22:55 | Amazon | AMZN | positive | up (0.55) | unclear | get drugs out through Amazon, through the whole group | -0.54% | -2.09% | -0.30% | +1.04% |
| 26:28 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market hit a brand new high a little while ago | +0.00% | +0.00% | +0.00% | +0.00% |
| 27:15 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | unclear | we built really a tremendous steel wall | · | · | · | · |

### Participates in a Small Business Summit — `nEDoEBVlHJE`
_the President Participates in a Small Business Summit (The White House); stream start 2026-05-04 15:17 ET; 68 min; 30 heads-ups / 24 confirmed / 6 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2:32 | Stock market | SPY, QQQ, DIA | positive | none (0.52) | repeat | We have a stock market that hit even with this | · | · | +0.00% | +0.00% |
| 2:39 | Iran | XLE, USO, ITA | negative | down (0.55) | repeat | We can't let Iran have a nuclear weapon. | · | · | -0.66% | -6.67% |
| 7:12 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | AI plants being built all over the country | · | · | -1.71% | +7.70% |
| 7:14 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | We're leading China in AI. | · | · | -1.08% | -0.57% |
| 8:40 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | virtually eliminated the unfair estate tax or debt tax for farmers | · | · | -0.54% | -2.84% |
| 19:56 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | I did a poll on the war with Iran, and they said only 32% | · | · | -0.48% | -6.49% |
| 32:11 | Oil | XLE, USO | positive | none (0.50) | unclear | hundreds of millions of barrels of oil coming out of Venezuela going t | · | · | -0.48% | -6.49% |
| 32:12 | Venezuela | XLE, CVX | positive | up (0.55) | unclear | great relationship, hundreds of millions of barrels of oil coming out  | · | · | -0.48% | -6.49% |
| 33:12 | Microsoft | MSFT | neutral | none (0.55) | repeat | sold it for 1000000000 dollars to Microsoft | · | · | -1.27% | -3.13% |
| 34:03 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | we're drilling more oil by far | · | · | -0.48% | -6.49% |
| 35:31 | Canada | EWC | negative | none (0.50) | repeat | We lost 54% of our car industry to Canada | · | · | -1.24% | -2.64% |
| 35:31 | Mexico | EWW | negative | none (0.50) | repeat | We lost 54% of our car industry to Mexico | · | · | +1.73% | +3.08% |
| 35:32 | Germany | EWG | negative | none (0.52) | repeat | We lost 54% of our car industry to Germany | · | · | +1.35% | -0.47% |
| 35:33 | Japan | EWJ | negative | none (0.52) | repeat | We lost 54% of our car industry to Canada, Mexico, Germany, Japan | · | · | +0.46% | +1.70% |
| 35:34 | South Korea | EWY | negative | none (0.52) | repeat | lost 54% of our car industry to Canada, Mexico, Germany, Japan, South  | · | · | +5.04% | +14.70% |
| 37:26 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | Coastal was hit very hard. Their core business dropped from 2 shifts t | · | · | · | · |
| 38:09 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | thanks to the tax cuts and the steel tariffs that I put on, coast is t | · | · | -0.48% | +2.30% |
| 39:40 | China | FXI, MCHI, KWEB | negative | none (0.55) | repeat | jobs that were going to China | · | · | -1.03% | -0.51% |
| 43:53 | Furniture / home goods | WSM, RH, LZB | positive | down (0.55) | unclear | we're putting tariffs on furniture | +0.30% | +0.37% | +3.93% | -2.98% |
| 48:52 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.52) | repeat | agriculture critical part of securing our supply chains | -0.56% | -0.51% | -3.02% | -1.82% |
| 50:18 | Trucking / rail | IYT, UNP, CSX | positive | none (0.52) | repeat | trucking companies | -0.01% | +0.84% | +2.95% | -0.37% |
| 63:59 | Intel | INTC | positive | up (0.60) | repeat | I made a investment. Intel | +4.41% | +13.45% | +15.79% | +23.11% |
| 64:53 | Automakers | GM, F, STLA, TSLA | negative | none (0.50) | repeat | car companies were leaving Detroit and leaving our country | +0.23% | +0.83% | +1.76% | -1.83% |
| 67:03 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | the stock market's higher now than it was when I assumed | +0.00% | +0.00% | +0.00% | +0.00% |

### Participates in an Executive Order Signing, April 30th, 2026 — `jDw21pUBBMU`
_the President Participates in an Executive Order Signing, April 30th, 2026 (The White House); stream start 2026-04-30 14:41 ET; 60 min; 38 heads-ups / 31 confirmed / 7 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:37 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | since my election, the stock market has set 59 | · | +0.00% | +0.00% | +0.00% |
| 2:25 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI is doing great. We're leading | · | -0.15% | -1.54% | +3.43% |
| 2:27 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | We're leading China by quite a bit. | · | +0.14% | +0.09% | -0.39% |
| 2:33 | Canada | EWC | neutral | down (0.55) | repeat | They're coming back from Canada. | · | +0.14% | -0.29% | -2.81% |
| 2:35 | Mexico | EWW | neutral | down (0.52) | repeat | They're coming back from Mexico. | · | +0.18% | +0.19% | +2.45% |
| 2:35 | Germany | EWG | neutral | none (0.52) | repeat | They're coming back from Canada. They're coming back from Mexico, Germ | · | -0.10% | -0.39% | -1.51% |
| 2:37 | Japan | EWJ | neutral | none (0.52) | repeat | auto plants being built all over the country. They're coming back from | · | -0.02% | -1.23% | +0.27% |
| 2:38 | South Korea | EWY | positive | down (0.55) | repeat | auto plants coming back from South Korea | · | +0.18% | +1.29% | +9.02% |
| 2:46 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | repeat | auto plants being built all over the country. They're coming back | · | +0.07% | -2.05% | -0.15% |
| 4:03 | Federal Reserve | TLT, XLF, KRE | neutral | none (0.50) | repeat | I was talking to Kevin Hassett a little while ago | · | -0.27% | -0.62% | -2.09% |
| 5:20 | Uber | UBER | neutral | none (0.55) | unclear | Uber drivers or something, they don't have access to that | · | -0.09% | +0.10% | +0.73% |
| 5:46 | Dell | DELL | positive | none (0.55) | repeat | the new savings accounts, you remember with Michael Dell, Susan, and the group t | · | +1.11% | +1.76% | +10.01% |
| 8:30 | Trucking / rail | IYT, UNP, CSX | negative | none (0.50) | repeat | As opposed to trucking it or training it | · | +0.31% | -0.31% | -1.87% |
| 12:41 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | a lot of that's AI, and a lot of that's maybe | · | -0.15% | -1.54% | +3.43% |
| 12:52 | Germany | EWG | negative | none (0.50) | repeat | They're coming back from different countries where they left us for Ge | · | -0.10% | -0.39% | -1.51% |
| 13:15 | Japan | EWJ | neutral | none (0.55) | repeat | They left us for Germany, Japan, South Korea, Canada, Mexico. | · | -0.02% | -1.23% | +0.27% |
| 13:22 | Toyota | TM | positive | up (0.55) | unclear | Japan just announced $10,000,000,000 more plants gonna be built betwee | · | +0.12% | -2.41% | -3.78% |
| 13:23 | Honda | HMC | positive | up (0.55) | unclear | Japan just announced $10,000,000,000 more plants gonna be built betwee | · | +0.07% | -1.35% | -3.00% |
| 13:28 | South Korea | EWY | positive | none (0.50) | repeat | companies they're pouring into our country in South Korea | · | +0.18% | +1.29% | +9.02% |
| 13:30 | Canada | EWC | neutral | none (0.50) | repeat | If they build here, they don't have to pay tariffs. | · | +0.14% | -0.29% | -2.81% |
| 16:20 | Iran | XLE, USO, ITA | neutral | down (0.55) | unclear | Iran is dying to make a deal. They cannot be nuclear. | · | -0.04% | -1.34% | -7.74% |
| 17:02 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | we just hit a new high today on the stock market | · | +0.00% | +0.00% | +0.00% |
| 17:58 | Northrop Grumman | NOC | positive | up (0.60) | new | that beautiful B-2 bomber | · | +0.03% | -1.76% | -6.04% |
| 19:40 | Venezuela | XLE, CVX | neutral | up (0.55) | unclear | they have good military in Venezuela, but this they did not expect | · | · | -1.34% | -7.74% |
| 20:18 | Oil | XLE, USO, XOM, CVX | neutral | up (0.52) | repeat | They're not getting any money from oil. | · | · | -1.34% | -7.74% |
| 29:21 | India | INDA, EPI | positive | none (0.50) | repeat | In the case of India | · | · | -0.52% | -0.62% |
| 33:12 | Ukraine | ITA, XLE | negative | none (0.50) | repeat | He's got a big problem with Ukraine | · | · | -1.06% | +0.28% |
| 36:47 | General Motors | GM | neutral | none (0.55) | repeat | PGA tour is playing at Dural, the Cadillac Championship | · | · | -2.05% | -0.15% |
| 39:17 | Federal Reserve | TLT, XLF, KRE | neutral | none (0.50) | repeat | I don't care if he stays on, he stays on. | · | · | -0.62% | -2.09% |
| 48:45 | Iran | XLE, USO, ITA | neutral | none (0.50) | repeat | I'm negotiating a deal with Iran. | · | · | -1.34% | -7.74% |
| 51:52 | Northrop Grumman | NOC | positive | none (0.52) | repeat | B 2 bombers, it's amazing how great our military is. | · | · | -1.79% | -6.06% |

### Signs an Executive Order, Apr. 18, 2026 — `8xrI-_qo64E`
_the President Signs an Executive Order, Apr. 18, 2026 (The White House); stream start 2026-04-18 08:54 ET; 50 min; 8 heads-ups / 3 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 5:29 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | drug prices went down 0.25 or 0.125 of a percent | -0.04% | +0.01% | -1.08% | -4.30% |
| 6:41 | Novo Nordisk | NVO | negative | down (0.65) | repeat | a friend of mine called me up and he said, you know, he's a very rich  | +0.17% | -0.02% | -1.86% | +0.97% |
| 11:02 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | not gonna hold the drug companies or the insurance companies liable | +0.06% | -0.50% | +7.44% | +8.55% |

### Delivers Remarks on Tax Week in Las Vegas, Nevada — `mpKpfdZitCM`
_the President Delivers Remarks on Tax Week in Las Vegas, Nevada (The White House); stream start 2026-04-16 19:36 ET; 48 min; 13 heads-ups / 10 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 9:14 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | farmers have no inheritance tax, no death tax | -1.38% | -1.82% | -1.45% | -0.72% |
| 10:24 | McDonald's | MCD | negative | none (0.55) | repeat | It was a little tacky. | -0.52% | +0.32% | -1.01% | -4.23% |
| 12:23 | Automakers | GM, F, STLA, TSLA | positive | up (0.58) | repeat | car companies are expanding like never before. We're selling more cars | +1.09% | +3.50% | +2.18% | -1.75% |
| 13:04 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | none (0.50) | repeat | pharmaceutical companies are coming in at levels that nobody's ever se | -0.12% | +0.37% | -0.45% | -3.41% |
| 16:22 | Stock market | DIA, SPY, QQQ | positive | none (0.50) | repeat | we just hit 50,000 on the Dow. 50,000 on the Dow is unthinkable. | +0.40% | +0.84% | +0.79% | -0.40% |
| 19:39 | Dell | DELL | positive | up (0.55) | unclear | buy their computer | -0.77% | -0.01% | +4.77% | +10.16% |
| 20:31 | Nucor | NUE | positive | none (0.50) | repeat | made interest on Nucor loans deductible, which I told you is a big dea | -0.35% | +0.54% | +4.42% | +9.95% |
| 26:50 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | We killed him, and that had a big impact on Iran. | -4.47% | -5.87% | -3.67% | -1.24% |
| 27:49 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | we just hit an all time new | +0.00% | +0.00% | +0.00% | +0.00% |
| 36:22 | Oil | XLE, USO | positive | none (0.50) | repeat | we have more oil production than Russia and Saudi Arabia by far | -4.47% | -5.87% | -3.67% | -1.24% |

### Holds a Press Conference, Apr. 6, 2026 — `xFO-SY9ykdA`
_the President Holds a Press Conference, Apr. 6, 2026 (The White House); stream start 2026-04-06 12:58 ET; 94 min; 18 heads-ups / 15 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 12:56 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | over Iran for 7 hours at times facing very, very heavy enemy fire | · | +0.40% | +1.19% | -8.04% |
| 36:28 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | Just ask any Iranian soldier who dared attempt | · | -0.10% | +0.79% | -8.42% |
| 54:35 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | Kurdistan region had resumed exporting oil to international market wit | · | -0.10% | +0.79% | -8.42% |
| 56:42 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | you just saw great and John Ratcliffe, unbelievable | · | +0.22% | -0.69% | -0.53% |
| 66:53 | Iran | XLE, USO, ITA | negative | up (0.55) | repeat | I didn't terminate the Barack Hussein Obama Iran nuclear deal | · | -0.10% | +0.79% | -8.42% |
| 67:02 | Israel | EIS, ITA | positive | none (0.50) | repeat | He chose Iran over Israel | · | +0.14% | -0.16% | +1.41% |
| 68:49 | Northrop Grumman | NOC | positive | none (0.50) | repeat | those beautiful b 2 bombers not gone in 8 months ago | · | -0.10% | -1.57% | -6.98% |
| 72:37 | New York Times | NYT | negative | none (0.55) | repeat | Circulation way down at The New York Times. | · | -0.28% | -0.18% | -11.87% |
| 75:37 | Warner Bros. Discovery (CNN) | WBD | negative | none (0.55) | repeat | CNN fake. | · | -0.11% | -0.48% | -4.49% |
| 79:56 | Venezuela | XLE, CVX | positive | · | · | we are a partner with Venezuela | · | -0.10% | +0.79% | -8.42% |
| 82:23 | Ford | F | neutral | none (0.55) | unclear | They saw that big beautiful aircraft carrier, the Ford in that case | · | -0.13% | -0.54% | +0.91% |
| 85:51 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | unclear | we want free traffic of oil and everything else | · | -0.10% | +0.79% | -8.42% |
| 88:11 | Iran | XLE, USO, ITA | negative | up (0.60) | new | every bridge in Iran will be decimated by 12:00 tomorrow night, every  | · | -0.10% | +0.79% | -8.42% |
| 91:26 | South Korea | EWY | positive | none (0.55) | repeat | Do you notice how nice things are with North Korea? It's very nice. | · | -0.17% | +0.88% | +7.94% |
| 92:31 | RTX (Raytheon) | RTX | negative | none (0.55) | unclear | they didn't know how to use our great patriots | · | -0.10% | -0.19% | -2.51% |

### Signs an Executive Order, Mar. 31, 2026 — `ELT3855m3qA`
_the President Signs an Executive Order, Mar. 31, 2026 (The White House); stream start 2026-03-31 16:55 ET; 42 min; 20 heads-ups / 10 confirmed / 10 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 12:07 | Tesla | TSLA | positive | none (0.52) | repeat | we were helped by Elon Musk with the communication with his great comm | +1.30% | +1.10% | -3.85% | -11.58% |
| 18:15 | Federal Reserve | TLT, XLF, KRE | negative | none (0.55) | repeat | I'm not building the Federal Reserve where the guy is spending $4,000, | -1.02% | -0.98% | -0.73% | -4.54% |
| 19:16 | Iran | XLE, USO, ITA | negative | down (0.55) | unclear | All I have to do is leave Iran, and we'll be doing that very soon. | -3.06% | -4.39% | -4.13% | -10.96% |
| 19:46 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | stock prices were up today almost to a record | +0.82% | +1.98% | +0.60% | +1.40% |
| 20:21 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market broke all records | +0.00% | +0.00% | +0.00% | +0.00% |
| 20:37 | Northrop Grumman | NOC | positive | up (0.55) | repeat | we did not come out with the b 2 bomber, we would have a nuclear weapo | +0.49% | +0.80% | +2.13% | -3.33% |
| 24:17 | Steel | X, NUE, CLF, STLD | positive | none (0.52) | repeat | very powerful steel, very steel | · | · | · | · |
| 28:48 | Microsoft | MSFT | neutral | none (0.55) | unclear | Iran's IRGC warning to target Microsoft if US continues assassinations | +0.35% | -0.36% | +0.04% | -3.76% |
| 37:25 | Federal Reserve | TLT, XLF, KRE | positive | none (0.50) | repeat | low interest rates, low taxes | -1.02% | -0.98% | -0.73% | -4.54% |
| 38:01 | New York Times | NYT | negative | none (0.55) | repeat | fake New York Times | -0.76% | +0.54% | +1.50% | -6.04% |

### Delivers Remarks at the Future Investment Initiative — `19b7cuFkXPE`
_the President Delivers Remarks at the Future Investment Initiative (The White House); stream start 2026-03-27 17:12 ET; 78 min; 39 heads-ups / 34 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 6:04 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | Iranian lunatics refused to cease their pursuit of nuclear weapons | -0.04% | +0.06% | -4.64% | -7.80% |
| 6:10 | Boeing | BA | neutral | none (0.55) | repeat | he sent 2 7 57 Boeing 7 57 jetliners | -0.45% | -0.67% | +1.90% | +6.26% |
| 7:10 | Saudi Arabia | KSA, XLE | positive | none (0.50) | repeat | Saudis. Oh, yes, sir. You are so powerful. | +1.45% | +2.12% | +2.29% | -1.67% |
| 8:41 | Northrop Grumman | NOC | positive | none (0.52) | repeat | we hit him with the b 2 bombers, so we did it twice | +0.53% | -0.65% | -2.09% | -2.27% |
| 10:14 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | We're crushing Iran's currently as we speak. They're being hit so hard | -0.35% | -1.67% | -1.31% | -0.60% |
| 12:20 | Google | GOOGL | positive | none (0.55) | repeat | Google Maps changed the name. We won the court case. | -0.19% | -0.38% | +2.26% | +7.38% |
| 17:04 | Russia | RSX, XLE | neutral | none (0.50) | repeat | hatred between president Putin and president Zelensky | · | · | · | · |
| 17:05 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | hatred between president Putin and president Zelensky | -0.35% | -1.67% | -1.31% | -0.60% |
| 17:39 | RTX (Raytheon) | RTX | positive | up (0.58) | repeat | there's nothing like these Patriots | +0.52% | -0.80% | -0.88% | +0.36% |
| 29:23 | Federal Reserve | TLT, XLF, KRE | positive | none (0.52) | repeat | low interest rates, and no inflation | +0.21% | +0.85% | -1.34% | -2.80% |
| 30:47 | Warner Bros. Discovery (CNN) | WBD | negative | none (0.55) | repeat | CNN, which is terrible. They treat me terribly. | -0.69% | -0.36% | -1.12% | -2.85% |
| 45:06 | Oil | XLE, USO, XOM, CVX | neutral | none (0.50) | repeat | oil prices were gonna go up higher than they are now | -0.04% | +0.06% | -4.64% | -7.80% |
| 45:24 | Stock market | DIA, SPY, QQQ | positive | none (0.50) | repeat | I hit 50,000 on the Dow. | -0.02% | +0.30% | +0.05% | -0.75% |
| 50:02 | Saudi Arabia | KSA, XLE | positive | up (0.55) | repeat | crown prince announced that Saudi Arabia would be investing | +1.45% | +2.12% | +2.29% | -1.67% |
| 50:15 | Oracle | ORCL | positive | up (0.55) | repeat | Oracle will be building | -0.68% | -0.94% | +2.77% | -1.45% |
| 50:22 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | unclear | Oracle will be building a $14,000,000,000 worth of cloud computing and | -0.20% | -0.64% | +1.54% | +2.35% |
| 51:02 | Boeing | BA | positive | up (0.60) | repeat | Boeing is selling dozens of 737 airplanes in a deal valued at $4,800,0 | -0.45% | -0.67% | +1.90% | +6.26% |
| 52:27 | Lockheed Martin | LMT | positive | up (0.65) | repeat | sell Saudi Arabia perhaps the most capable fighter jet ever built, the | -0.11% | -1.47% | -4.42% | -2.04% |
| 60:32 | Canada | EWC | neutral | down (0.55) | repeat | tariffs are driving people in from Canada | -0.28% | +0.01% | -0.40% | -0.07% |
| 60:32 | Mexico | EWW | neutral | down (0.55) | repeat | tariffs are driving people in from Mexico | -0.33% | +0.25% | +1.76% | +1.35% |
| 60:32 | Germany | EWG | neutral | none (0.52) | repeat | tariffs are driving people in from Germany | -0.21% | +0.22% | +1.61% | +1.37% |
| 60:33 | Japan | EWJ | neutral | none (0.52) | repeat | tariffs are driving people in from Japan | +0.55% | +0.49% | +1.13% | +1.05% |
| 60:33 | South Korea | EWY | neutral | none (0.52) | repeat | tariffs are driving people in from South Korea | -0.72% | -3.07% | -0.88% | +1.17% |
| 60:42 | Toyota | TM | neutral | up (0.55) | unclear | I met mister Toyota | -1.54% | -1.57% | -2.87% | -5.45% |
| 61:27 | Bitcoin | IBIT, COIN, MSTR | positive | up (0.55) | repeat | America remains at the bleeding edge of crypto revolution | +1.86% | +1.65% | +0.16% | +0.58% |
| 61:57 | Stablecoins | CRCL, COIN | positive | up (0.58) | repeat | I signed the Landmark Genius Act into law, creating framework for doll | +1.83% | -2.74% | -0.69% | -3.47% |
| 64:58 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | the 1 that they're going crazy about is AI | -0.20% | -0.64% | +1.54% | +2.35% |
| 69:06 | China | FXI, MCHI, KWEB | positive | up (0.55) | repeat | I called up president Xi. I get along really well with him. | -0.09% | +0.31% | +0.45% | -2.16% |
| 69:10 | TikTok | ORCL | positive | up (0.55) | repeat | He even approved the TikTok deal. He said, I will not approve that dea | -0.68% | -0.94% | +2.77% | -1.45% |
| 69:27 | Warner Bros. Discovery (CNN) | WBD | negative | none (0.55) | repeat | fake news CNN | -0.69% | -0.36% | -1.12% | -2.85% |
| 72:48 | Oil | XLE, USO, XOM, CVX | positive | none (0.52) | repeat | we have the biggest the most oil, gas, coal, and everything of any nat | -0.04% | +0.06% | -4.64% | -7.80% |
| 72:48 | Coal | BTU, ARCH, AMR | positive | none (0.52) | repeat | we have the biggest the most oil, gas, coal, and everything of any nat | -1.53% | -3.66% | -19.15% | -23.05% |
| 76:01 | New York Times | NYT | negative | none (0.55) | repeat | New York Times, which is fake | -0.21% | +0.37% | -1.43% | -0.25% |
| 76:07 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | if you read the New York Times, you would think we're doing badly agai | -0.04% | +0.06% | -4.64% | -7.80% |

### Delivers Remarks to Farmers — `IyKAzbxybog`
_the President Delivers Remarks to Farmers (The White House); stream start 2026-03-27 12:32 ET; 38 min; 12 heads-ups / 10 confirmed / 2 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:22 | Agriculture | DBA, MOS, DE, CORN | positive | up (0.55) | unclear | single largest gathering of American farmers | · | -0.24% | +0.48% | -3.16% |
| 10:23 | China | FXI, MCHI, KWEB | positive | none (0.50) | repeat | sending over $40,000,000,000 in American soybeans to China | · | +0.06% | +1.25% | -1.39% |
| 11:07 | European Union | VGK, EZU, FEZ | positive | none (0.50) | repeat | expanded markets for American beef, dairy products, biofuels across As | · | -0.01% | +1.01% | +1.68% |
| 11:26 | Agriculture | DBA, MOS, DE, CORN | positive | up (0.55) | repeat | farmers want a level playing field | · | -0.24% | +0.48% | -3.16% |
| 14:25 | John Deere | DE | positive | none (0.52) | repeat | We have a lot of John Deere's. That's a big dig. | · | -0.18% | -1.88% | -2.68% |
| 20:08 | Caterpillar | CAT | neutral | down (0.55) | new | John Deere and Case and all of... They're great companies. Caterpillar | · | -0.03% | -3.78% | -0.33% |
| 21:37 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | We have the greatest farmers also. | · | -0.24% | +0.48% | -3.16% |
| 24:04 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | To help lower gasoline prices for farmers and consumers, this week, I  | · | +0.14% | -0.10% | -7.96% |
| 24:41 | Refiners | VLO, MPC, PSX | positive | down (0.55) | new | find a deal that works for farmers, consumers, and refiners | · | +0.53% | -0.14% | -6.22% |
| 33:23 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | largest investment in rural America for our farmers and ranchers in Am | · | -0.24% | +0.48% | -3.16% |

### Holds a Press Conference, Mar. 9, 2026 — `ViW6wZw8Dn8`
_the President Holds a Press Conference, Mar. 9, 2026 (The White House); stream start 2026-03-09 17:43 ET; 34 min; 15 heads-ups / 14 confirmed / 1 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:54 | Venezuela | XLE, CVX | positive | none (0.50) | unclear | great success we've had in Venezuela and all other places | -0.38% | -0.26% | +1.46% | +4.99% |
| 3:34 | Northrop Grumman | NOC | positive | up (0.55) | repeat | our b 2 bombers recently dropped dozens of 2,000 pound | -1.17% | -1.77% | -1.61% | -2.02% |
| 10:38 | Defense | ITA, XAR, LMT, RTX | positive | up (0.55) | repeat | We have a lot of navy ships there. We have the best equipment in the w | -0.39% | -0.46% | -1.08% | -2.65% |
| 11:12 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | unclear | result will be lower oil prices, oil and gas prices | -0.38% | -0.26% | +1.46% | +4.99% |
| 12:09 | Venezuela | XLE, CVX | positive | down (0.55) | unclear | Venezuela now as our new partner, great partner. | -0.38% | -0.26% | +1.46% | +4.99% |
| 14:50 | Russia | RSX, XLE | positive | up (0.55) | unclear | I had a very good call with Russian president Vladimir Putin today | · | · | · | · |
| 15:12 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | tremendous hatred between president Putin and president Zelensky | -0.39% | -0.46% | -1.08% | -2.65% |
| 18:09 | RTX (Raytheon) | RTX | neutral | none (0.55) | repeat | Tomahawk, which is 1 of the most powerful weapons around, is used by y | -0.82% | -0.43% | -0.18% | -1.25% |
| 21:34 | Northrop Grumman | NOC | positive | none (0.52) | repeat | B 2 bombers took out their nuclear capability | -1.17% | -1.77% | -1.61% | -2.02% |
| 27:21 | Oil | XLE, USO | positive | none (0.50) | unclear | We've taken out a 100,000,000 barrels of oil. | -0.38% | -0.26% | +1.46% | +4.99% |
| 27:34 | Refiners | VLO, MPC, PSX | positive | up (0.55) | unclear | It's brought to the refineries. It's being refined in | +0.11% | +1.51% | +7.28% | +10.37% |
| 27:44 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | We've taken out 100,000,000 barrels of oil. It's being refined in Hous | -0.38% | -0.26% | +1.46% | +4.99% |
| 27:53 | Venezuela | XLE, CVX | positive | up (0.52) | new | 100,000,000 barrels of oil, partnership, great for Venezuela, great fo | -0.38% | -0.26% | +1.46% | +4.99% |
| 28:22 | RTX (Raytheon) | RTX | neutral | none (0.55) | repeat | Tomahawks are used by others, as you know. | -0.82% | -0.43% | -0.18% | -1.25% |

### Participates in a Roundtable on Ratepayer Protection Pledge — `W50sSr87n4Q`
_the President Participates in a Roundtable on Ratepayer Protection Pledge (The White House); stream start 2026-03-04 15:10 ET; 56 min; 50 heads-ups / 29 confirmed / 21 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:51 | Iran | XLE, USO, ITA | negative | up (0.55) | repeat | terminate the worst deal, the Obama nuclear deal where he gave everyth | · | · | +1.64% | +3.25% |
| 3:25 | Northrop Grumman | NOC | positive | none (0.52) | repeat | b twos hit and I use the word obliterate because it really was | · | · | -0.60% | -0.79% |
| 4:07 | Oil | XLE, USO | positive | none (0.50) | unclear | taking out hundreds of millions of barrels of oil | · | · | +1.64% | +3.25% |
| 4:11 | Venezuela | XLE, CVX | positive | up (0.55) | unclear | We're taking out hundreds of millions of barrels of oil, and that goes | · | · | +1.64% | +3.25% |
| 6:45 | Stock market | DIA, SPY, QQQ | positive | none (0.50) | repeat | We've never broke 50,000 on the Dow. We did it in the 1st year. | · | · | -0.91% | -1.22% |
| 7:10 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | new | big tech companies committing to fully cover cost of increased electri | · | · | +0.25% | +2.43% |
| 9:13 | Bitcoin | IBIT, COIN, MSTR | positive | none (0.50) | repeat | AI and crypto czar David Sachs | · | · | -2.50% | -2.54% |
| 10:00 | Google | GOOGL | neutral | none (0.52) | repeat | president of Google | · | · | +0.09% | +3.40% |
| 10:07 | U.S. Steel | X, NUE, CLF, STLD | neutral | none (0.50) | repeat | used to be US Steel and things like that. Now it's Google | · | · | · | · |
| 10:50 | Microsoft | MSFT | positive | none (0.55) | repeat | Microsoft is unbelievable. | · | · | +1.18% | +0.48% |
| 10:57 | OpenAI | MSFT | neutral | none (0.55) | repeat | COO of OpenAI, Brad Lightcap. | · | · | +1.18% | +0.48% |
| 13:39 | Artificial intelligence | NVDA, SMH | neutral | none (0.50) | repeat | massive energy demand from AI data centers could drive up electricity  | · | · | +0.25% | +2.43% |
| 13:46 | Canada | EWC | neutral | none (0.50) | repeat | big plants that are being built all over the country there coming in f | · | · | -0.16% | -0.18% |
| 13:46 | Mexico | EWW | neutral | none (0.50) | repeat | big plants that are being built all over the country there coming in f | · | · | -2.07% | -2.07% |
| 13:48 | Germany | EWG | neutral | none (0.50) | repeat | big plants that are being built all over the country there coming in f | · | · | -1.31% | -1.49% |
| 13:49 | Japan | EWJ | neutral | none (0.55) | repeat | big plants that are being built all over the country there coming in f | · | · | -2.16% | -1.62% |
| 13:50 | South Korea | EWY | neutral | none (0.55) | repeat | big plants being built coming in from South Korea | · | · | -8.22% | -2.35% |
| 14:06 | Semiconductors | SMH, SOXX, NVDA, INTC | negative | none (0.50) | repeat | We lost the chip industry | · | · | -0.56% | +1.58% |
| 14:19 | Taiwan | EWT, TSM | negative | down (0.58) | repeat | if you're gonna make your product and sell it back in here, you're gon | · | · | -1.02% | +1.81% |
| 18:05 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | 2 big LNG plants in Louisiana. When I came in originally | · | · | +3.24% | +11.02% |
| 21:59 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | China is building tremendous energy. I gotta respect it. | · | · | -1.19% | +1.80% |
| 24:26 | Bitcoin | IBIT, COIN, MSTR | positive | none (0.50) | repeat | In crypto, we wanna be dominant. | · | · | -2.39% | -2.43% |
| 24:36 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | America can maintain the most advanced AI infrastructure on the planet | · | · | +0.86% | +3.06% |
| 26:05 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.50) | repeat | It's worthless. Don't get approvals for wind. We don't do wind. | · | · | -0.81% | +2.90% |
| 26:19 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | Europe is buying them by the thousands. | · | · | -1.33% | -0.97% |
| 32:26 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | America leading in AI and stopping the price rises. | · | · | +0.86% | +3.06% |
| 43:26 | Google | GOOGL | positive | none (0.55) | repeat | Google's investment | · | · | +0.07% | +3.38% |
| 45:46 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | x AI builds huge supercomputers and data centers, and we build them fa | · | · | +0.86% | +3.06% |
| 47:01 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | unclear | deploying our AI technology to make people's lives better | · | · | +0.86% | +3.06% |

### Delivers Remarks on Energy, Feb. 27, 2026 — `rr2RA4JAntQ`
_the President Delivers Remarks on Energy, Feb. 27, 2026 (The White House); stream start 2026-02-27 16:32 ET; 63 min; 28 heads-ups / 17 confirmed / 11 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 5:03 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | Biden administration waged radical left war on American oil and natura | +4.62% | +3.76% | +7.42% | +7.98% |
| 5:52 | Refiners | VLO, MPC, PSX | negative | none (0.50) | repeat | piled crippling regulations on producers and refiners, imposed natural | +6.12% | +2.99% | +7.21% | +6.65% |
| 6:06 | Oil | XLE, USO, XOM, CVX | negative | up (0.55) | repeat | gasoline reached a peak of over $6 a gallon in some states | +4.37% | +1.78% | +1.90% | +1.84% |
| 7:16 | Oil | XLE, USO | positive | up (0.55) | repeat | US oil production is now up by 600,000 barrels | +4.37% | +1.78% | +1.90% | +1.84% |
| 9:21 | Venezuela | XLE, CVX | neutral | up (0.55) | unclear | Crude oil exports are up by hundreds of thousands of barrels a day. Ve | +4.37% | +1.78% | +1.90% | +1.84% |
| 19:18 | Electric vehicles | TSLA, RIVN, GM | negative | down (0.55) | repeat | terminated the insane electric vehicle mandate | -1.90% | -0.58% | -1.68% | +0.17% |
| 19:49 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | mandate is over and now you can buy gasoline powered car | +4.37% | +1.78% | +1.90% | +1.84% |
| 21:03 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The stock market has hit 53 | +0.00% | +0.00% | +0.00% | +0.00% |
| 24:02 | Dell | DELL | positive | up (0.55) | unclear | Go out and buy a Dell computer. They're great. | +0.17% | +0.22% | -1.13% | +0.07% |
| 41:03 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | most favored nation agreements for drug prices, slashing drug prices a | +0.43% | -0.77% | -1.33% | -2.58% |
| 42:46 | United Kingdom | EWU | negative | none (0.55) | repeat | in London, I'm paying $87 | -0.70% | -1.31% | -3.12% | -3.78% |
| 45:08 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.60) | repeat | unaffordable care act, which is Obamacare | -0.68% | -0.18% | -0.56% | -1.64% |
| 46:45 | Artificial intelligence | NVDA, SMH | negative | none (0.55) | repeat | big tech companies energy usage AI data centers cannot drive up price | -0.17% | +2.24% | +2.44% | +4.21% |
| 48:03 | Homebuilders | XHB, ITB, LEN, DHI | positive | up (0.65) | unclear | after I directed the purchase of 200,000,000,000 in mortgage bonds, mo | -0.91% | -1.90% | -2.55% | -7.67% |
| 48:19 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | I have a lousy guy in the Fed. Terrible. | +0.14% | -0.83% | -0.71% | -0.63% |
| 57:25 | Space | RKLB, ARKX | positive | none (0.52) | repeat | beautiful space force | -2.44% | +1.62% | +2.32% | +4.57% |
| 60:15 | Northrop Grumman | NOC | positive | none (0.52) | repeat | beautiful b 2 bombers | +3.91% | +4.32% | +5.62% | +4.29% |

### the President’s 2026 State of the Union Address — `eWrZQBgpY7I`
_the President’s 2026 State of the Union Address (The White House); stream start 2026-02-24 20:58 ET; 124 min; 15 heads-ups / 13 confirmed / 2 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 20:41 | Homebuilders | XHB, ITB, LEN, DHI | positive | up (0.55) | repeat | Mortgage rates are the lowest in 4 years and falling fast | -0.49% | -4.12% | -1.91% | -4.75% |
| 20:58 | Federal Reserve | TLT, XLF, KRE | positive | up (0.52) | repeat | low interest rates will solve the Biden created housing problem | -0.62% | -0.69% | +0.13% | -0.51% |
| 21:22 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The stock market is at 53 | +0.00% | +0.00% | +0.00% | +0.00% |
| 22:58 | Oil | XLE, USO | positive | up (0.55) | repeat | American oil production is up by more than 600,000 | -0.05% | -1.64% | -0.37% | +2.30% |
| 23:06 | Venezuela | XLE, CVX | positive | down (0.55) | new | new friend and partner, Venezuela, more than 80,000,000 | -0.05% | -1.64% | -0.37% | +2.30% |
| 23:22 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | American natural gas production is at an all time high | +1.16% | +1.57% | -0.98% | +3.12% |
| 41:57 | Dell | DELL | neutral | none (0.55) | unclear | I asked Michael Dell, how do you make all that money? | -1.80% | +0.81% | +1.11% | +23.13% |
| 43:24 | Stock market | DIA, SPY, QQQ | positive | none (0.50) | repeat | the Dow Jones broke 5000 | -0.04% | -0.41% | +0.34% | -0.50% |
| 49:37 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.60) | unclear | Obamacare, a big insurance company that's gotten rich. It was meant fo | +0.81% | +2.25% | +4.36% | +6.90% |
| 52:07 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | will now pay the lowest price anywhere in the world for drugs | -0.41% | -0.31% | -0.57% | -0.20% |
| 56:57 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market has done so well setting all those records | +0.00% | +0.00% | +0.00% | +0.00% |
| 118:52 | Aluminum | AA, CENX | positive | none (0.50) | repeat | Americans lifted humanity into the skies on the wings of aluminum | +1.52% | +3.52% | +3.07% | +0.55% |
| 118:52 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | repeat | Americans lifted humanity into the skies on the wings of steel | · | · | · | · |

### Delivers Remarks on the Economy, Feb. 19, 2026 — `dSvsEvBq84o`
_the President Delivers Remarks on the Economy, Feb. 19, 2026 (The White House); stream start 2026-02-19 16:17 ET; 72 min; 25 heads-ups / 19 confirmed / 6 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2:58 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | brand new steel and equipment that just went up because of our tariffs | · | · | · | · |
| 4:50 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | Don't forget China and these other countries, they paid for it. It's a | -1.42% | -0.69% | +0.49% | -3.67% |
| 8:25 | Canada | EWC | negative | down (0.55) | repeat | other countries like Canada | +0.33% | -0.16% | +0.66% | +1.95% |
| 15:19 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | I see the yellow steel. | · | · | · | · |
| 16:38 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market | +0.00% | +0.00% | +0.00% | +0.00% |
| 20:23 | Oil | XLE, USO | positive | none (0.50) | repeat | oil production is up by more than 600,000 | -0.01% | -0.81% | +0.25% | +1.12% |
| 20:27 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | natural gas production is at an all time high | +0.99% | +0.72% | -0.20% | -2.59% |
| 20:37 | Venezuela | XLE, CVX | positive | up (0.55) | unclear | we have a great relationship with a country named Venezuela | -0.01% | -0.81% | +0.25% | +1.12% |
| 29:25 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | what you've done for us economically with the tariffs in particular | · | · | · | · |
| 32:02 | Canada | EWC | negative | down (0.58) | repeat | plants from Canada, they took a lot of our car business | +0.33% | -0.16% | +0.66% | +1.95% |
| 38:08 | Dell | DELL | positive | up (0.55) | unclear | go out and buy a Dell computer | -0.78% | +1.66% | +0.37% | +24.15% |
| 52:01 | Steel | X, NUE, CLF, STLD | positive | none (0.05) | unclear | these 2 guys, they're like steel | · | · | · | · |
| 59:22 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | Our policies have brought gas prices way down | -0.01% | -0.81% | +0.25% | +1.12% |
| 62:29 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.60) | unclear | insurance companies are getting from our country for healthcare | -0.04% | -1.34% | -2.31% | +0.93% |
| 63:34 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | slashing drug prices by 400 | +0.15% | -1.00% | +1.12% | +1.65% |
| 64:19 | United Kingdom | EWU | neutral | none (0.55) | repeat | pill selling for $10 in New York, $130 in London, 13 times more | +0.53% | +0.27% | +0.75% | +1.88% |
| 67:11 | Homebuilders | XHB, ITB, LEN, DHI | positive | up (0.55) | repeat | slashed the yearly cost of new mortgages by $4,000 | +0.65% | +1.31% | -0.87% | -2.35% |
| 68:34 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | we take care of our amazing farmers. Nobody's taken care of farmers li | +0.62% | -0.22% | +0.58% | +0.24% |
| 71:25 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | This steel mill, I'm gonna come back here in 2 years. You'll be 3 time | · | · | · | · |

### Participates in the Champion of Coal Event — `jBfm-1j30eE`
_the President Participates in the Champion of Coal Event (The White House); stream start 2026-02-11 16:26 ET; 28 min; 22 heads-ups / 17 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:37 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | We love clean, beautiful coal. Thank you very much, fellas. | +2.47% | -1.72% | -4.83% | -8.45% |
| 2:10 | Stock market | SPY, QQQ, DIA | positive | none (0.55) | repeat | We just hit the highest price in the history of the stock market, 50,0 | +0.00% | +0.00% | +0.00% | +0.00% |
| 5:46 | Coal | BTU, ARCH, AMR | positive | up (0.58) | repeat | America's beautiful clean coal plants would keep running when we need  | +2.47% | -1.72% | -4.83% | -8.45% |
| 7:02 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.58) | repeat | coal generation surged 31%, while solar and wind | +0.63% | -0.40% | +0.69% | +2.75% |
| 7:16 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | They're made in China, but not used by China. They sell us those thing | -1.01% | -1.30% | -1.41% | -1.31% |
| 10:36 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | unclear | These plants were slated for termination | +0.64% | +2.21% | +3.17% | +5.86% |
| 12:15 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | energy prices way down. You see what's happening even with gasoline. | -0.40% | -0.33% | +0.33% | +0.18% |
| 16:35 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | Coal is critical to our national security, vital to steel production | · | · | · | · |
| 16:36 | Defense | ITA, XAR, LMT, RTX | positive | none (0.50) | unclear | Coal is critical to our national security, vital to shipbuilding | +0.64% | +2.21% | +3.17% | +5.86% |
| 16:37 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | none (0.50) | repeat | Coal is critical to our national security, vital to artificial intelli | +1.24% | +0.70% | -2.33% | +0.24% |
| 17:01 | Coal | BTU, ARCH, AMR | positive | up (0.70) | new | Department of War to work directly with coal plants on new power purch | +2.47% | -1.72% | -4.83% | -8.45% |
| 17:12 | Coal | BTU, ARCH, AMR | positive | up (0.65) | new | we're gonna be buying a lot of coal through the military now | +2.47% | -1.72% | -4.83% | -8.45% |
| 18:43 | Japan | EWJ | positive | none (0.52) | repeat | historic trade deals with Japan | -0.30% | -0.26% | +1.35% | -2.29% |
| 18:43 | South Korea | EWY | positive | none (0.52) | repeat | historic trade deals with Japan, Korea, India, and others to increase  | +1.76% | +2.24% | +4.06% | +9.00% |
| 18:44 | India | INDA, EPI | positive | none (0.50) | repeat | historic trade deals with Japan, Korea, India, and others to increase  | -0.61% | -0.30% | +0.28% | +0.16% |
| 20:54 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | breaking 7,000 on the S and P | +0.00% | +0.00% | +0.00% | +0.00% |
| 21:39 | Saudi Arabia | KSA, XLE | positive | none (0.50) | repeat | in Saudi Arabia, the king said, you know, sir | -0.23% | +0.33% | +1.40% | -1.06% |

### Signs Executive Orders, Jan. 30, 2026 — `E9y3yfTAUaE`
_the President Signs Executive Orders, Jan. 30, 2026 (The White House); stream start 2026-01-30 11:31 ET; 32 min; 13 heads-ups / 5 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2:22 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | unclear | America made more steel than Japan. Can you believe it? | · | · | · | · |
| 3:22 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | S and P 500 just set a new record, 7,000 | · | +0.00% | +0.00% | +0.00% |
| 15:26 | Federal Reserve | TLT, XLF, KRE | positive | up (0.55) | new | We just named a new Fed chairman today. He's central casting. | · | +0.00% | -1.48% | +0.35% |
| 21:24 | Disney (ABC) | DIS | negative | none (0.55) | repeat | You're a loud person. Very loud. | · | +0.31% | -7.16% | -2.67% |
| 31:04 | Uber | UBER | neutral | none (0.55) | repeat | You used to take an Uber or a taxi or something | · | -0.13% | +0.28% | -6.61% |

### Participates in a Cabinet Meeting, Jan. 29, 2026 — `lT62rXuOAh4`
_the President Participates in a Cabinet Meeting, Jan. 29, 2026 (The White House); stream start 2026-01-29 11:33 ET; 87 min; 54 heads-ups / 40 confirmed / 14 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 9:49 | Venezuela | XLE, CVX | positive | up (0.55) | new | major oil companies going to Venezuela now, scouting it out and pickin | · | -0.45% | -0.32% | +4.05% |
| 9:52 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | new | major oil companies going to Venezuela now, scouting it out and pickin | · | -0.45% | -0.32% | +4.05% |
| 11:49 | Agriculture | DBA, MOS, DE, CORN | positive | up (0.50) | repeat | we gave $12,000,000,000 to the farmers of our country | · | -0.36% | -1.25% | +1.26% |
| 12:23 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | just yesterday, the S and P 500 hit 7,000 for the 1st time | · | +0.00% | +0.00% | +0.00% |
| 17:17 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | I'm not a fan of his. | · | -0.50% | -0.97% | +1.52% |
| 19:28 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | repeat | gonna be great for everybody, including the car companies | · | +0.21% | -2.62% | -1.35% |
| 19:32 | Ford | F | positive | up (0.55) | repeat | I went to the Ford factory, I was in Detroit 3 weeks ago. | · | +0.55% | -0.49% | +0.44% |
| 19:34 | General Motors | GM | positive | up (0.55) | repeat | They're doing better than they've ever done. | · | +0.21% | -2.62% | -1.35% |
| 20:33 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | You have AI building, but the | · | +0.46% | +1.16% | -7.00% |
| 20:46 | Germany | EWG | neutral | none (0.52) | repeat | coming back from Germany. All over Europe. | · | +0.35% | -0.42% | +1.04% |
| 20:47 | European Union | VGK, EZU, FEZ | neutral | down (0.55) | repeat | coming back from Germany. All over Europe. | · | +0.16% | -0.63% | +0.62% |
| 21:09 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | repeat | they're all coming back. 1 statistic yesterday that Scott told me is t | · | · | · | · |
| 22:54 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | bringing drug prices down by 90% | · | -0.57% | -0.22% | +1.93% |
| 23:55 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.60) | repeat | unaffordable care act, which is Obamacare, it's unaffordable | · | +0.61% | -1.56% | -5.81% |
| 26:08 | United Kingdom | EWU | neutral | none (0.55) | repeat | selling a pill for $10 in London and a $130 in New York | · | -0.12% | -0.71% | +0.90% |
| 29:50 | Novo Nordisk | NVO | negative | down (0.60) | repeat | cost $87 there, cost $1,300 in New York. What's going on? | · | -0.17% | +0.10% | -25.08% |
| 34:56 | Russia | RSX, XLE | neutral | up (0.55) | repeat | Russia, Ukraine, we're making a lot of progress. | · | · | · | · |
| 34:58 | Ukraine | ITA, XLE | positive | down (0.55) | unclear | we're making a lot of progress | · | -0.14% | -0.51% | -1.10% |
| 38:49 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | Biden administration had destroyed the American people with interest r | · | -0.50% | -0.97% | +1.52% |
| 39:27 | John Deere | DE | positive | up (0.55) | unclear | CEO said thanks to your tariffs, new plants in Indiana and North Carol | · | -0.67% | -0.05% | +9.22% |
| 42:48 | Stock market | SPY, QQQ, DIA | positive | none (0.52) | repeat | record high profits, and stock prices | · | +0.00% | +0.00% | +0.00% |
| 43:13 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | none (0.50) | repeat | pharmaceutical discounts and rents | · | -0.57% | -0.22% | +1.93% |
| 49:09 | Eli Lilly | LLY | positive | up (0.55) | repeat | Eli Lilly is building 6 new plants, including an API plant. | · | -0.80% | +0.31% | +0.81% |
| 49:19 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | not gonna be stuck buying API from China who cuts us off | · | +0.12% | -2.63% | -4.03% |
| 49:23 | Novo Nordisk | NVO | positive | up (0.55) | unclear | Novo Nordisk is building 4 new plants | · | -0.17% | +0.10% | -25.08% |
| 51:52 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.55) | repeat | fighting hundreds of billions of dollars in Medicaid, Medicare fraud | · | +0.61% | -1.56% | -5.81% |
| 53:33 | Merck | MRK | positive | none (0.50) | repeat | Eli Lilly, Merck, Pfizer, every drug company, they're spending trillio | · | -0.71% | +0.49% | +11.27% |
| 53:34 | Pfizer | PFE | neutral | none (0.55) | repeat | Eli Lilly, Merck, Pfizer | · | -0.36% | +0.85% | +3.13% |
| 54:18 | Eli Lilly | LLY | positive | none (0.55) | repeat | head of Eli Lilly, who's a fantastic guy, a star | · | -0.80% | +0.31% | +0.81% |
| 55:35 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | we gotta get interest rates down even lower | · | -0.50% | -0.97% | +1.52% |
| 61:35 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | natural gas production today is greater than Russia | · | +1.44% | +15.22% | -5.77% |
| 62:11 | Coal | BTU, ARCH, AMR | positive | up (0.60) | repeat | beautiful clean coal was the MVP | · | +0.11% | -1.96% | -2.72% |
| 62:36 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | Coal delivered 20 times more electricity than solar and batteries. | · | +0.37% | -2.55% | +3.12% |
| 63:40 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | Europe is destroying itself with stupid windmills | · | +0.07% | -0.78% | +0.46% |
| 65:17 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | China does most of everything they're doing with coal. | · | +0.02% | -2.73% | -4.12% |
| 65:34 | Coal | BTU, ARCH, AMR | positive | up (0.62) | repeat | coal...great backup...in case of tragedy, bad weather | · | +0.11% | -1.96% | -2.72% |
| 68:37 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | They can use oil and gas. Many are choosing oil and gas because it's p | · | +0.27% | +0.14% | +4.49% |
| 70:51 | NuScale | SMR | negative | none (0.55) | unclear | NuScale, and the city, the mayor who's grossly incompetent | · | -1.79% | -8.79% | -20.51% |
| 79:22 | Ford | F | neutral | none (0.55) | repeat | Ford has 5,000 small manufacturing suppliers. | · | -0.17% | -1.03% | -0.09% |
| 80:58 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | new | We have the steel now, and we're gonna be doing that. | · | · | · | · |

### Delivers Remarks on the new savings accounts — `ebH-gklOcl8`
_the President Delivers Remarks on the new savings accounts (The White House); stream start 2026-01-28 10:55 ET; 49 min; 23 heads-ups / 20 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 4:11 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | hundreds of massive plants so big, car plants, AI plants | · | +0.25% | +0.93% | -7.51% |
| 6:02 | Canada | EWC | neutral | none (0.55) | repeat | factories coming in from Canada | · | +0.14% | +1.14% | -0.44% |
| 6:03 | Mexico | EWW | neutral | none (0.52) | repeat | factories coming in from Mexico | · | +0.04% | +0.85% | +0.41% |
| 6:03 | Japan | EWJ | neutral | none (0.52) | repeat | factories coming in from Canada, Mexico, Japan, Germany, all over Euro | · | +0.13% | +1.70% | +4.47% |
| 6:04 | Germany | EWG | neutral | none (0.50) | repeat | factories coming in from Canada, Mexico, Japan, Germany, all over Euro | · | +0.04% | -0.79% | -0.10% |
| 6:05 | European Union | VGK, EZU, FEZ | neutral | down (0.55) | repeat | factories coming in from Canada, Mexico, Japan, Germany, all over Euro | · | -0.02% | +0.90% | +1.65% |
| 19:47 | Federal Reserve | TLT, XLF, KRE | positive | none (0.50) | repeat | He's so good. Kevin Hassett. | · | +0.03% | +0.42% | +0.32% |
| 24:32 | TikTok | ORCL | positive | up (0.55) | repeat | we got the TikTok deal done | · | -2.21% | -4.83% | -16.23% |
| 26:04 | Dell | DELL | neutral | none (0.55) | repeat | Not as much as Michael Dell. Not quite. | · | +0.76% | +1.35% | +5.50% |
| 32:17 | Uber | UBER | positive | none (0.55) | unclear | dozens of major employers have signed up including Uber | · | -0.73% | +0.98% | -7.48% |
| 32:25 | Intel | INTC | positive | none (0.55) | unclear | Intel, Nvidia, Broadcom, IBM signed up today | · | +1.73% | +2.09% | +3.09% |
| 32:25 | Nvidia | NVDA | positive | none (0.55) | unclear | Intel, Nvidia, Broadcom, IBM signed up today | · | +0.25% | +0.93% | -7.51% |
| 32:26 | Broadcom | AVGO | positive | none (0.55) | unclear | Intel, Nvidia, Broadcom, IBM signed up today | · | -0.54% | +0.25% | -5.47% |
| 32:28 | Coinbase | COIN | positive | up (0.52) | new | Coinbase, and just today, it was announced | · | -0.45% | -4.83% | -18.25% |
| 32:31 | Comcast (NBC, MSNBC) | CMCSA | positive | none (0.52) | new | Comcast have all signed up for really big contributions. | · | +0.32% | +2.02% | +7.53% |
| 34:06 | Microsoft | MSFT | positive | none (0.55) | repeat | they privately own Nvidia and Microsoft, all the greatest companies | · | -0.27% | -9.52% | -12.41% |
| 36:33 | Robinhood | HOOD | positive | up (0.55) | repeat | Vlad of Robinhood, what a job he's done. | · | +0.20% | -2.83% | -21.43% |
| 36:44 | Kraken | COIN | positive | none (0.52) | repeat | Arjun Sethi of Kraken. What a job you've done. | · | -0.13% | -4.40% | -17.89% |
| 37:57 | Visa | V | positive | up (0.55) | new | Visa is creating a brand new platform for cash back rewards into the President | · | +0.16% | +2.05% | +2.61% |
| 38:45 | Stock market | SPY, QQQ, DIA, V | positive | none (0.50) | repeat | S and P 500 hit 7,000 for the 1st time ever | · | +0.00% | +0.00% | +0.00% |

### Delivers Remarks to the Detroit Economic Club — `lGTJgtL_QYw`
_the President Delivers Remarks to the Detroit Economic Club (The White House); stream start 2026-01-13 13:46 ET; 67 min; 36 heads-ups / 33 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:14 | Ford | F | positive | up (0.55) | repeat | I just left Bill Ford. He's running his plant, 150 plant | · | +0.20% | -0.74% | -0.52% |
| 3:34 | Automakers | GM, F, STLA, TSLA | positive | none (0.50) | repeat | crown jewel of Detroit, still going after 100 years | · | +0.31% | -2.00% | -1.65% |
| 9:33 | Oil | XLE, USO | positive | none (0.50) | unclear | They have 50,000,000 barrels of oil. They said take it. | · | -0.06% | +2.40% | +4.58% |
| 9:39 | Venezuela | XLE, CVX | positive | none (0.50) | unclear | They have 50,000,000 barrels of oil. They said take it. It's $5,000,00 | · | -0.06% | +2.40% | +4.58% |
| 11:24 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | growth at an all time high | · | +0.00% | +0.00% | +0.00% |
| 14:18 | Oil | XLE, USO, XOM, CVX | negative | down (0.55) | repeat | We're gonna get it down further. Have it down at about a 6 year low. | · | -0.06% | +2.40% | +4.58% |
| 16:11 | Ford | F | positive | up (0.55) | repeat | I saw it today at Ford | · | +0.20% | -0.74% | -0.52% |
| 16:15 | Federal Reserve | TLT, XLF, KRE | negative | none (0.52) | repeat | don't raise interest rates every time good news is mentioned | · | +0.03% | +0.92% | +0.48% |
| 21:56 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market is now the highest in history since the election | · | +0.00% | +0.00% | +0.00% |
| 22:36 | Berkshire Hathaway | BRK.B | positive | none (0.50) | repeat | She thinks I'm Warren Buffett. She thinks I'm brilliant. | · | · | · | · |
| 24:04 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | anti tariff person is a pro Chinese person | · | -0.10% | -0.20% | -1.22% |
| 24:05 | Coca-Cola | KO | negative | none (0.55) | repeat | This guy's fought me in every election I've ever been in, and I've kic | · | +0.40% | +1.56% | +3.08% |
| 27:07 | Rare earths | MP, REMX | positive | up (0.60) | repeat | The President tariffs have delivered us trillions of dollars of new investment | · | -0.98% | +7.51% | +1.04% |
| 27:09 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | none (0.52) | repeat | The President tariffs have delivered us trillions of dollars of new investment | · | -0.16% | -0.67% | +0.14% |
| 31:28 | Automakers | GM, F, STLA, TSLA | positive | up (0.60) | unclear | 25% tariff on all foreign automobiles, standing up for American autowo | · | +0.31% | -2.00% | -1.65% |
| 31:36 | Japan | EWJ | neutral | none (0.52) | repeat | Let Japan come in. They are. | · | -0.02% | +1.10% | +1.51% |
| 32:08 | Ford | F | positive | up (0.55) | repeat | Ford has announced it will invest $5,000,000,000 | · | +0.20% | -0.74% | -0.52% |
| 32:15 | General Motors | GM | positive | up (0.60) | repeat | GM is moving production of the Chevy Blazer and Equinox from Mexico | · | +0.31% | -2.00% | -1.65% |
| 32:18 | General Motors | GM | positive | up (0.58) | repeat | GM is moving production of the Chevy Blazer and Equinox from Mexico | · | +0.31% | -2.00% | -1.65% |
| 32:20 | Mexico | EWW | negative | down (0.55) | repeat | GM is moving production of the Chevy Blazer and Equinox from Mexico | · | +0.15% | +2.37% | +5.84% |
| 33:01 | Stellantis | STLA | positive | up (0.55) | repeat | Stellantis is investing $13,000,000,000 | · | +0.09% | +0.71% | -1.04% |
| 33:29 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | I just spoke to an AI guy, and that's booming too. | · | -0.16% | -0.67% | +0.14% |
| 43:29 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | canceled all meetings with Iranian officials until senseless killing s | · | -0.00% | +2.45% | +4.63% |
| 45:49 | Homebuilders | XHB, ITB, LEN, DHI | positive | up (0.60) | repeat | US government purchasing $200,000,000,000 of mortgage bonds to bring d | · | +0.05% | -0.38% | +1.17% |
| 46:01 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | not with the help of the Fed | · | +0.04% | +0.89% | +0.44% |
| 46:36 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.58) | unclear | confronting the monstrosity known as the unaffordable care act | · | -0.09% | +0.57% | +5.11% |
| 47:28 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | reduce premiums for millions of lower drug prices, delivering price tr | · | +0.01% | +1.15% | +2.12% |
| 51:48 | Electric vehicles | TSLA, RIVN, GM | negative | down (0.55) | repeat | I terminated the insane electric vehicle mandate | · | +0.41% | -0.94% | -1.96% |
| 57:14 | Mercedes-Benz | MBGYY | negative | none (0.55) | unclear | Mercedes Benz dealers do well in that area of Minnesota | · | +0.26% | +1.77% | +0.18% |
| 59:51 | Visa | V | negative | none (0.55) | unclear | We're investigating large scale visa fraud | · | -0.32% | +0.15% | -0.31% |
| 63:55 | Ford | F | positive | none (0.55) | repeat | Our country was built by legends like Henry Ford | · | -0.32% | -0.94% | -0.72% |
| 64:03 | General Motors | GM | positive | none (0.55) | repeat | Alfred P. Sloan, the founder of General Motors | · | -0.08% | -2.30% | -1.95% |
| 66:06 | Automakers | GM, F, STLA, TSLA | positive | none (0.52) | repeat | our auto industry is returning to | · | -0.08% | -2.30% | -1.95% |

### Participates in a Meeting with Oil and Gas Executives — `iaE8lw8_x30`
_the President Participates in a Meeting with Oil and Gas Executives (The White House); stream start 2026-01-09 14:52 ET; 88 min; 59 heads-ups / 33 confirmed / 26 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 4:09 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | new | American companies can help rapidly rebuild Venezuela's oil industry | · | +0.19% | -0.79% | +2.60% |
| 4:16 | Venezuela | XLE, CVX | positive | up (0.55) | new | discuss how these great American companies can help rapidly rebuild Ve | · | +0.19% | -0.79% | +2.60% |
| 10:33 | Oil | XLE, USO | positive | up (0.55) | new | American companies will have the opportunity to rebuild Venezuela's ro | · | · | -0.79% | +2.60% |
| 14:07 | Chevron | CVX | neutral | up (0.55) | repeat | We have Chevron, which has been where's Chevron? | · | · | +0.12% | +3.04% |
| 14:29 | ExxonMobil | XOM | positive | up (0.55) | repeat | Mark Nelson, thank you very much. | · | · | -0.34% | +4.87% |
| 14:41 | ConocoPhillips | COP | positive | up (0.55) | unclear | And ConocoPhillips | · | · | -3.47% | -0.24% |
| 17:08 | Venezuela | XLE, CVX | negative | up (0.55) | new | stole the wealth of that country to fund a repressive regime and also  | · | · | -0.79% | +2.60% |
| 17:20 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | every penny everything they buy with the money from oil will be bought | · | · | -0.79% | +2.60% |
| 21:58 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | record production of natural gas in The United States | · | · | +6.56% | -1.04% |
| 24:16 | Chevron | CVX | positive | up (0.60) | unclear | Venezuelan employees have been working tirelessly to operate safely, p | · | · | +0.12% | +3.04% |
| 26:06 | Russia | RSX, XLE | neutral | none (0.50) | unclear | Russia can get all the oil they need from us | · | · | · | · |
| 27:08 | China | FXI, MCHI, KWEB | negative | none (0.50) | unclear | China and Russia would have been there if we didn't do this. | · | · | +3.28% | +0.38% |
| 28:09 | ExxonMobil | XOM | positive | up (0.58) | unclear | And ExxonMobil, I wanna thank you. | · | · | -0.34% | +4.87% |
| 28:12 | ConocoPhillips | COP | positive | up (0.55) | repeat | followed by Conoco | · | · | -3.47% | -0.24% |
| 35:20 | Chevron | CVX | neutral | up (0.62) | new | Go back to Chevron. They wanna discuss something. | · | · | +0.12% | +3.04% |
| 43:46 | Russia | RSX, XLE | negative | none (0.50) | repeat | Russian soldiers lost 31,000 people, Russian economy doing poorly | · | · | · | · |
| 43:58 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | I settled 8 wars. I thought this would be in the middle of the pack | · | · | +1.65% | +5.26% |
| 44:31 | Rare earths | MP, REMX | neutral | none (0.50) | repeat | I did make a rare earth deal to get it back | · | · | +6.49% | +12.93% |
| 44:53 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | selling our military equipment. They're probably giving it to Ukraine. | · | · | +1.65% | +5.26% |
| 52:53 | India | INDA, EPI | neutral | none (0.55) | repeat | India and Pakistan, where already 8 jets were shot out of the air | · | · | +0.46% | -0.07% |
| 54:54 | Mercedes-Benz | MBGYY | neutral | none (0.55) | repeat | They sell more Mercedes Benzes in that area than almost can you imagin | · | · | -0.88% | -2.48% |
| 59:41 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | putting windmills all over the place and losing a fortune | · | · | +4.04% | +4.03% |
| 60:36 | European Union | VGK, EZU, FEZ | negative | none (0.50) | repeat | They make them and sell them to suckers like Europe | · | · | +0.54% | +0.96% |
| 60:51 | Steel | X, NUE, CLF, STLD | negative | none (0.50) | repeat | junkyard of steel. So we don't approve | · | · | · | · |
| 63:43 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | Obama with that horrible deal they made with Iran. It was a short term | · | · | -0.98% | +2.41% |
| 68:04 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | They're gonna be taking the oil, and they're gonna be bringing oil pri | +0.66% | -0.56% | +0.75% | +4.37% |
| 68:12 | Venezuela | XLE, CVX | positive | up (0.60) | new | people of Venezuela are gonna be big beneficiaries | +0.66% | -0.56% | +0.75% | +4.37% |
| 68:40 | Chevron | CVX | positive | up (0.60) | unclear | where's mister Chevron? | +0.85% | +0.27% | +1.13% | +4.34% |
| 69:28 | China | FXI, MCHI, KWEB | neutral | none (0.50) | unclear | China would like to be doing a lot of business there by buying oil | +1.66% | +2.11% | +2.33% | +1.16% |
| 69:34 | Russia | RSX, XLE | neutral | none (0.55) | repeat | I wanna just tell President Xi and President Putin | · | · | · | · |
| 83:01 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | one of the largest LNG off takers of American LNG | +3.18% | +4.45% | +8.89% | +21.32% |
| 84:14 | Chevron | CVX | positive | up (0.60) | unclear | support of Chevron. We have ability to scale. | +0.85% | +0.27% | +1.13% | +4.34% |
| 86:41 | Venezuela | XLE, CVX | neutral | up (0.58) | new | divvy it all up between Venezuela, The United States, and them | +0.66% | -0.56% | +0.75% | +4.37% |

### Holds a Press Conference, Jan. 3, 2026 — `SsdkClL2_bg`
_the President Holds a Press Conference, Jan. 3, 2026 (The White House); stream start 2026-01-03 10:51 ET; 106 min; 8 heads-ups / 4 confirmed / 4 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 52:21 | Venezuela | XLE, CVX | negative | none (0.50) | unclear | drugs mostly come from a place called Venezuela | +2.81% | +0.88% | -1.29% | -0.24% |
| 92:55 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | unclear | We're in the oil business. We're gonna sell it to them. | +2.81% | +0.88% | -1.29% | -0.24% |
| 95:26 | Venezuela | XLE, CVX | positive | up (0.55) | new | greatest oil companies invest billions and billions, take out money, u | +2.81% | +0.88% | -1.29% | -0.24% |
| 104:16 | Ukraine | ITA, XLE | negative | none (0.52) | repeat | people are being killed in Kiev, people are being killed in other citi | +0.11% | +0.95% | +2.43% | +4.79% |

### Delivers Remarks on the Economy, Dec. 19, 2025 — `FKU63HY1KJQ`
_the President Delivers Remarks on the Economy, Dec. 19, 2025 (The White House); stream start 2025-12-19 20:47 ET; 94 min; 30 heads-ups / 26 confirmed / 4 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 8:21 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | cut the cost of prescription drugs by 300, 400, 500 | -1.00% | -0.54% | -1.05% | -0.47% |
| 8:50 | United Kingdom | EWU | negative | none (0.55) | repeat | prices in London and in Paris all over | -0.42% | -0.15% | -0.07% | +0.62% |
| 10:39 | Film industry | DIS, NFLX, WBD, PSKY | positive | none (0.50) | repeat | some of them went to Hollywood and actually did very well | -0.34% | +0.20% | +0.70% | +2.25% |
| 13:03 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | prices down, they're going down silver. They look at gasoline. A lot o | -0.47% | -0.16% | -0.24% | +0.94% |
| 14:49 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | France as an example, UK, European Union | -0.24% | -0.18% | -0.09% | +0.46% |
| 19:18 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.60) | repeat | taking in the gigantic health insurance companies that have gotten ric | -1.87% | -0.16% | -1.88% | +0.50% |
| 23:46 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | unclear | big drug companies get up and talk about things | -1.00% | -0.54% | -1.05% | -0.47% |
| 33:17 | Comcast (NBC, MSNBC) | CMCSA | negative | none (0.55) | repeat | NBC and CBS and ABC fake news. They're fake news. | -0.80% | +0.26% | -1.73% | +0.41% |
| 33:18 | Paramount (CBS) | PARA, PSKY | negative | none (0.55) | repeat | NBC and CBS and ABC fake news. They're fake news. | +0.43% | · | -2.93% | -7.42% |
| 33:19 | Disney (ABC) | DIS | negative | none (0.55) | repeat | ABC fake news. They're fake news. | -0.34% | +0.20% | +0.70% | +2.25% |
| 38:19 | Oil | XLE, USO, XOM, CVX | negative | none (0.50) | repeat | gasoline prices went up 30 to 75% | -0.47% | -0.16% | -0.24% | +0.94% |
| 43:18 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | the only things that are going up are your salaries, the stock market | +0.00% | +0.00% | +0.00% | +0.00% |
| 49:38 | Comcast (NBC, MSNBC) | CMCSA | negative | none (0.55) | repeat | the wage chart that you see up there is incredible there that, you kno | -0.80% | +0.26% | -1.73% | +0.41% |
| 52:20 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI plants, factories, auto plants | +1.13% | +0.86% | +3.46% | +2.68% |
| 52:33 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | I ended the radical left's war on American energy, terminated the gree | -0.47% | -0.16% | -0.24% | +0.94% |
| 53:20 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | 50% tariffs on foreign steel | · | · | · | · |
| 53:28 | Furniture / home goods | WSM, RH, LZB | positive | none (0.50) | repeat | 25, 30, and 50% tariffs to save North Carolina's cherished furniture i | -0.54% | -1.56% | -2.53% | -5.91% |
| 53:32 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | 50% tariffs to save North Carolina's furniture industry, decimated by  | -0.62% | -0.49% | -1.26% | -0.76% |
| 55:14 | Semiconductors | SMH, SOXX, NVDA, INTC | negative | down (0.40) | repeat | they didn't put them on chips | +1.24% | +0.32% | +0.86% | +1.04% |
| 56:50 | Fox Corporation | FOXA | negative | none (0.55) | repeat | I don't like about Fox is their pollster. Total fake. | +0.57% | +2.24% | +1.62% | +1.75% |
| 60:51 | Dell | DELL | positive | none (0.55) | unclear | Michael Dell Dell computer. He put up 6,250,000,000. | +1.37% | -0.57% | -0.13% | +0.24% |
| 62:56 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | Green New scam | +1.16% | +1.56% | +1.80% | +0.16% |
| 63:30 | Tesla | TSLA | positive | none (0.55) | repeat | Elon Musk with his incredible, you would call it | +1.31% | +0.94% | -0.18% | -6.51% |
| 63:59 | Electric vehicles | TSLA, RIVN, GM | negative | none (0.55) | repeat | I don't believe in the mandate where everybody has to have an electric | +1.31% | +0.94% | -0.18% | -6.51% |
| 81:00 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | unclear | record investment in our military, warrior dividend of $1,776.17 | +0.25% | +1.10% | +1.62% | +0.19% |
| 81:35 | Iran | XLE, USO, ITA | positive | none (0.50) | repeat | destroyed the Iran nuclear threat | -0.47% | -0.16% | -0.24% | +0.94% |

### Signs an Executive Order, Dec. 18, 2025 — `DTVbPs1RoKo`
_the President Signs an Executive Order, Dec. 18, 2025 (The White House); stream start 2025-12-18 13:42 ET; 36 min; 8 heads-ups / 3 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2:11 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.55) | unclear | reclassification, which polls at 82, will help many patients | · | -0.01% | -0.45% | -0.54% |
| 24:26 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.55) | repeat | We have a problem. The insurance companies | · | -0.01% | -0.45% | -0.54% |
| 31:03 | Venezuela | XLE, CVX | negative | up (0.55) | repeat | land attacks on drug cartels in Venezuela | · | -0.06% | -0.46% | -1.74% |

### Delivers Remarks on the Economy — `I8WJz5A1Q7Y`
_the President Delivers Remarks on the Economy (The White House); stream start 2025-12-09 18:59 ET; 100 min; 40 heads-ups / 32 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 9:12 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | repeat | we saved a little company called U.S. Steel, and it's hot as a pistol  | · | · | · | · |
| 10:48 | Agriculture | DBA, MOS, DE, CORN | positive | up (0.52) | repeat | I just helped our farmers out because they're starting to do really we | +0.22% | +0.25% | +0.01% | +0.95% |
| 11:47 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | AI plants, plants of every type, which we would have never had | +0.07% | -0.59% | -3.08% | -5.88% |
| 11:55 | European Union | VGK, EZU, FEZ | neutral | none (0.52) | unclear | Europe now is saying, we gotta start doing what the President is doing. We got | +0.29% | +0.27% | +1.09% | +2.92% |
| 12:56 | Boeing | BA | positive | up (0.55) | repeat | 250 Boeing jets. I brought back | +0.07% | +0.35% | -0.73% | +4.68% |
| 16:52 | Oil | XLE, USO, XOM, CVX | positive | none (0.52) | repeat | we're right now drilling more oil | +0.38% | +0.12% | -0.33% | -0.31% |
| 20:49 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The only thing that's really going up big. It's called the stock marke | +0.00% | +0.00% | +0.00% | +0.00% |
| 23:33 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.50) | repeat | Wind is the worst. It's a scam. They ruin your valleys. | -0.25% | -0.08% | +2.83% | +1.24% |
| 27:22 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | We have a bad head of the Fed. We're gonna be making a change. | +0.10% | +0.34% | -0.65% | +1.51% |
| 39:11 | China | FXI, MCHI, KWEB | positive | up (0.55) | repeat | We're getting along with China. They're buying a lot of our soybeans. | +0.46% | +0.61% | +0.06% | -0.79% |
| 39:16 | Agriculture | DBA, SOYB, ADM, MOS | positive | up (0.52) | repeat | They're buying a lot of our soybeans. Keep buying those soybeans. | +0.22% | +0.25% | +0.01% | +0.95% |
| 39:20 | Rare earths | MP, REMX | positive | none (0.50) | repeat | You heard all about magnets and rare earth. They were great. | -0.03% | -2.92% | -0.58% | -11.32% |
| 41:21 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | down lower than we've been in 7 years at gasoline prices and oil price | +0.38% | +0.12% | -0.33% | -0.31% |
| 42:10 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market is at the highest point | +0.00% | +0.00% | +0.00% | +0.00% |
| 42:34 | Walmart | WMT | positive | none (0.52) | repeat | Walmart, I thanked them. You know, they came out with a big | +0.32% | +0.31% | -0.50% | +2.23% |
| 47:52 | Homebuilders | XHB, ITB, LEN, DHI | negative | none (0.50) | repeat | prices are coming down tremendously from the highest prices | +0.53% | +0.91% | +3.23% | +2.57% |
| 47:54 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | Even with a lousy Fed chair | +0.10% | +0.34% | -0.65% | +1.51% |
| 52:08 | Health insurers | UNH, CI, ELV, HUM | negative | down (0.58) | repeat | working to bring down the cost of healthcare. We're also working to br | -0.19% | -0.58% | +3.16% | +4.19% |
| 54:22 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The stock market has set | +0.00% | +0.00% | +0.00% | +0.00% |
| 58:50 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.55) | repeat | Let's go buy those windmills for millions of dollars each | -0.25% | -0.08% | +2.83% | +1.24% |
| 58:53 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | buy those windmills for millions of dollars each from China | +0.46% | +0.61% | +0.06% | -0.79% |
| 59:54 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | Open up the North Sea oil. | +0.38% | +0.12% | -0.33% | -0.31% |
| 60:17 | United Kingdom | EWU | positive | none (0.52) | repeat | UK has to if they don't go back to oil | +0.86% | +0.61% | +0.90% | +1.84% |
| 60:22 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | If they don't go back to oil, a lot of bad things are happening to Eur | +0.29% | +0.27% | +1.09% | +2.92% |
| 60:56 | Electric vehicles | TSLA, RIVN, GM | positive | none (0.52) | repeat | I think electric cars are great | +0.27% | +0.19% | -0.51% | +6.67% |
| 63:21 | Natural gas / LNG | UNG, LNG, EQT, X | positive | none (0.50) | repeat | natural gas production is booming | +1.49% | +1.21% | -8.13% | -8.65% |
| 63:24 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | Coal mining is up by 2,400,000 | -0.42% | -3.15% | +1.91% | +1.77% |
| 63:32 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | repeat | With our historic tariffs, steel production is roaring back. | · | · | · | · |
| 72:23 | Dell | DELL | positive | up (0.55) | unclear | Go out and buy a Dell computer. | -0.05% | -0.46% | -0.62% | -5.77% |
| 72:38 | Dell | DELL | positive | up (0.55) | unclear | Michael Dell and his beautiful Dell computer. Go out and buy a Dell co | -0.05% | -0.46% | -0.62% | -5.77% |
| 79:36 | Venezuela | XLE, CVX | negative | none (0.50) | repeat | Venezuela, their entire prison population was set into our country. | +0.38% | +0.12% | -0.33% | -0.31% |
| 95:49 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | repeat | the steel mills of | · | · | · | · |

### Makes an Announcement, Dec. 3, 2025 — `2Ey5TwGj7Cc`
_the President Makes an Announcement, Dec. 3, 2025 (The White House); stream start 2025-12-03 15:19 ET; 59 min; 50 heads-ups / 27 confirmed / 23 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:38 | Automakers | GM, F, STLA, TSLA | positive | up (0.65) | new | Terminating Joe Biden's ridiculously burdensome CAFE standards that im | · | · | +0.92% | +7.84% |
| 0:55 | Electric vehicles | TSLA, RIVN, GM | negative | down (0.55) | repeat | insane electric vehicle mandate combined with expensive restrictions | · | · | +1.68% | +0.53% |
| 1:19 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | greatest scam in American history, the Green New scam | · | · | +1.79% | +2.89% |
| 1:54 | Ford | F | positive | up (0.58) | repeat | CEO of Ford, Jim Farley. Jim, where is Jim? | · | · | +0.37% | +1.97% |
| 2:02 | Stellantis | STLA | neutral | up (0.58) | unclear | CEO of Stellantis, Antonio | · | · | +3.26% | +5.24% |
| 2:17 | General Motors | GM | neutral | up (0.58) | repeat | manager of General Motors | · | · | +0.92% | +7.84% |
| 5:47 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | we're leading everybody in AI | · | · | +1.45% | +1.21% |
| 5:48 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | we're leading China in AI because of tariffs | · | · | +0.49% | -0.54% |
| 6:38 | Mexico | EWW | negative | down (0.55) | unclear | General Motors plans to invest $4,000,000,000 as it brings its manufac | · | · | +0.54% | +0.40% |
| 7:42 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | repeat | we're gonna have a big percentage of the chip market very soon | · | · | -0.31% | +2.67% |
| 12:06 | Volkswagen | VWAGY | neutral | none (0.55) | repeat | they have a very small car, sort of like the Beetle used to be with th | · | · | +2.57% | +3.46% |
| 12:27 | Honda | HMC | positive | up (0.55) | new | If you take a look, Honda, they really are beautiful. | · | · | +1.25% | +3.86% |
| 12:30 | Japan | EWJ | positive | none (0.50) | unclear | I've authorized the secretary to immediately approve production of tho | · | · | +1.24% | +1.12% |
| 12:55 | Toyota | TM | positive | up (0.58) | new | if Toyota or any other company wants to make smaller, more affordable  | · | · | +1.71% | +2.53% |
| 13:16 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | new | cleared the deck so they can make them in America and sell them in Ame | · | · | +1.07% | +8.00% |
| 13:37 | Stellantis | STLA | positive | up (0.65) | new | Stellantis decided to invest to Jeep, Ram, Dodge, and Chrysler, $13,00 | · | · | +3.29% | +5.27% |
| 24:00 | Electric vehicles | TSLA, RIVN, GM | negative | none (0.52) | repeat | they got into the e vehicles, and basically, they couldn't sell 1 | · | · | +1.86% | +0.71% |
| 29:14 | Automakers | GM, F, STLA, TSLA | positive | up (0.55) | repeat | companies investing tens of billions of dollars in our country | · | · | +1.07% | +8.00% |
| 31:19 | Boeing | BA | positive | up (0.55) | repeat | We'll be building the f 47 and then f 1 fifties. | · | · | -0.13% | -2.15% |
| 37:24 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | regulations forced cars to be plastic instead of steel | · | · | · | · |
| 43:51 | Russia | RSX, XLE | neutral | up (0.55) | unclear | they had a very good meeting yesterday with president Putin | · | · | · | · |
| 50:58 | China | FXI, MCHI, KWEB | neutral | none (0.52) | repeat | export controls and the types of ships that Nvidia can give to China | +0.20% | +0.41% | +1.47% | -0.82% |
| 51:02 | Nvidia | NVDA | positive | up (0.55) | repeat | He's done an amazing job. Nvidia, very good. | +0.92% | +0.87% | +1.31% | -0.03% |
| 56:01 | Mexico | EWW | neutral | none (0.50) | repeat | work out another deal with Mexico and Canada | -0.28% | +0.23% | +0.10% | +3.07% |
| 56:01 | Canada | EWC | neutral | none (0.50) | repeat | work out another deal with Mexico and Canada | +0.00% | +0.94% | +1.30% | +2.30% |
| 58:01 | Ford | F | positive | up (0.55) | repeat | the people that are up here from Salantis and Ford | +0.56% | +0.00% | -0.72% | +3.35% |
| 58:02 | General Motors | GM | positive | none (0.52) | repeat | the people that are up here from Salantis and General Motors | +0.21% | +1.10% | +1.56% | +7.48% |

### Delivers Remarks at the U.S. - Saudi Investment Forum — `D0_1MbanXRM`
_the President Delivers Remarks at the U.S. - Saudi Investment Forum (The White House); stream start 2025-11-19 11:56 ET; 64 min; 48 heads-ups / 40 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 5:39 | Saudi Arabia | KSA, XLE, LMT, GD | positive | up (0.60) | unclear | selling Saudi Arabia some of the greatest military equipment ever buil | · | +0.15% | +1.12% | -5.10% |
| 5:41 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.62) | unclear | We build the best military equipment in the world by far | · | -0.16% | -0.44% | -2.11% |
| 8:04 | Nuclear energy | URA, CCJ, OKLO, SMR | positive | up (0.55) | new | groundbreaking agreements on civil nuclear energy | · | -0.48% | -4.30% | -2.40% |
| 8:05 | Rare earths | MP, REMX | positive | up (0.60) | unclear | groundbreaking agreements on critical minerals | · | -1.53% | -11.13% | -9.88% |
| 8:06 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.60) | new | groundbreaking agreements on artificial intelligence | · | -0.41% | -1.13% | -5.44% |
| 11:52 | Federal Reserve | TLT, XLF, KRE | neutral | none (0.50) | repeat | We're thinking about him for the Fed | · | +0.22% | +1.56% | -0.96% |
| 13:54 | Oil | XLE, USO, XOM, CVX | positive | none (0.52) | repeat | I called it drill baby drill. | · | +0.39% | +0.65% | -2.98% |
| 14:13 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | allowing all of those AI plants that are being built to build their ow | · | -0.41% | -1.13% | -5.44% |
| 16:40 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | We're leading China by a lot in AI. | · | +0.27% | +0.27% | -1.81% |
| 16:45 | Canada | EWC | neutral | down (0.55) | repeat | bringing auto plants in from Canada | · | +0.05% | +0.40% | +0.94% |
| 16:46 | Mexico | EWW | neutral | down (0.55) | repeat | bringing auto plants in from Mexico | · | +0.08% | +0.07% | -1.25% |
| 17:02 | Toyota | TM | positive | none (0.55) | repeat | Toyota just announced $10,000,000,000 | · | +0.03% | -1.20% | +0.40% |
| 17:11 | Japan | EWJ | positive | none (0.50) | repeat | Toyota is coming in with a $10,000,000,000 | · | +0.11% | +0.04% | +0.62% |
| 17:28 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | We led the chip industry 30, 40 years ago. We had a 100%. | · | -0.49% | -2.37% | +0.22% |
| 17:46 | Taiwan | EWT, TSM | negative | down (0.40) | unclear | when you sell your product back into this country, there will be a 250 | · | +0.10% | +0.25% | -0.67% |
| 17:57 | Intel | INTC | positive | none (0.50) | repeat | Intel would have been a giant. | · | -0.55% | -2.17% | +2.88% |
| 18:01 | Nvidia | NVDA | neutral | up (0.55) | repeat | He now owns a big chunk of Intel. He's got it figured all different wa | · | -0.41% | -1.13% | -5.44% |
| 18:19 | Nvidia | NVDA | positive | up (0.55) | repeat | Blackwell doing? Okay? | · | -0.41% | -1.13% | -5.44% |
| 20:35 | Boeing | BA | positive | up (0.55) | repeat | We just have a new plane, the f 47. | · | +0.14% | -1.07% | -1.08% |
| 25:29 | GE Aerospace | GE | positive | up (0.65) | new | Under the deals being signed this week, workers at GE Aerospace | · | -0.64% | -1.74% | -3.84% |
| 28:23 | Vaccine makers | PFE, MRNA, NVAX | positive | none (0.52) | repeat | we did a great job with all of the things that we did with the vaccine | · | -0.11% | -1.28% | -0.16% |
| 30:03 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.52) | repeat | we want those people to teach our people how to make computer chips | · | -0.49% | -2.37% | +0.22% |
| 31:25 | Taiwan | EWT, TSM | negative | none (0.50) | repeat | Jensen, I don't think you can open up a big plant with your friend fro | · | +0.10% | +0.25% | -0.67% |
| 31:28 | Semiconductors | SMH, SOXX | negative | none (0.55) | repeat | 40 or 50% of the computer chip business at a very... I don't think you | · | -0.49% | -2.37% | +0.22% |
| 32:31 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | Since the election, the stock market has set | · | +0.00% | +0.00% | +0.00% |
| 38:00 | Walmart | WMT | positive | none (0.52) | repeat | Walmart just announced that the cost of their standard Thanksgiving me | · | +0.10% | +8.17% | +6.05% |
| 41:52 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | Brooke Rollins did a fantastic job. Department of Agriculture | · | -0.12% | +0.63% | -2.75% |
| 41:56 | Homebuilders | XHB, ITB, LEN, DHI | positive | up (0.55) | repeat | Mortgage rates are down despite the Fed. | · | -0.18% | +0.42% | +5.98% |
| 41:58 | Federal Reserve | TLT, XLF, KRE | neutral | none (0.50) | repeat | Mortgage rates are down despite the Fed. | · | -0.01% | +1.35% | -1.18% |
| 44:16 | Tesla | TSLA | positive | none (0.55) | repeat | deduction on the interest if they buy a nice Tesla car and they borrow | · | -0.66% | -0.62% | +3.05% |
| 44:28 | Electric vehicles | TSLA, RIVN, GM | positive | up (0.58) | repeat | let him buy other than electric cars, these are minor details | · | -0.66% | -0.62% | +3.05% |
| 44:32 | Tesla | TSLA | positive | up (0.55) | repeat | giving them a deduction on the interest if they buy 1 of a nice Tesla  | · | -0.66% | -0.62% | +3.05% |
| 45:44 | Apple | AAPL | positive | none (0.55) | repeat | Apple alone, Tim Cook brought in hundreds of billions of dollars. | · | -0.11% | -0.23% | -0.16% |
| 48:00 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | stopped Joe Biden's radical crusade to kill oil | · | +0.24% | +0.27% | -3.37% |
| 48:00 | Natural gas / LNG | UNG, LNG, EQT | positive | up (0.55) | repeat | stopped Joe Biden's radical crusade to kill natural gas | · | -0.42% | -0.67% | -5.93% |
| 48:11 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | Windmills don't work. | · | -0.27% | -3.53% | -2.97% |
| 51:24 | Saudi Arabia | KSA, XLE | positive | up (0.58) | repeat | America and Saudi Arabia are partnering on energy like never before. | · | +0.18% | +0.97% | -5.25% |
| 53:10 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | proudly ended the ridiculous Biden era restrictions on artificial inte | · | -0.05% | -0.73% | -5.04% |
| 53:19 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | ended the ridiculous Biden era restrictions on artificial intelligence | · | -0.05% | -0.73% | -5.04% |
| 58:23 | Russia | RSX, XLE | neutral | none (0.50) | repeat | Putin called me and said, I can't believe you got that settled. | · | · | · | · |

### Delivers Remarks at McDonald's Impact Summit — `QPid-oVSSi4`
_the President Delivers Remarks at McDonald's Impact Summit (The White House); stream start 2025-11-17 18:10 ET; 49 min; 20 heads-ups / 18 confirmed / 2 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:06 | McDonald's | MCD | positive | none (0.52) | repeat | incredible company, heart and soul of greatest companies in history | +0.79% | +1.54% | -0.25% | +0.42% |
| 1:53 | Google | GOOGL | neutral | none (0.55) | repeat | the famous Sundar and Sergei, Sergei Brin. These are 2 guys that own a | +1.55% | -0.21% | +3.19% | +12.08% |
| 7:22 | Walmart | WMT | positive | up (0.55) | repeat | one of your groups that you admire, I admire, Walmart came up last wee | +0.57% | +0.70% | -1.82% | +2.53% |
| 8:41 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | That's car factories. That's AI. It's everything. | -1.19% | -1.56% | +0.41% | -6.11% |
| 10:40 | Coca-Cola | KO | positive | none (0.55) | repeat | best Coca Cola in America. Best Coca Cola. | +0.97% | +1.45% | +1.07% | +1.33% |
| 11:11 | McDonald's | MCD | positive | none (0.55) | repeat | It has nothing to do with McDonald's, but maybe it does because it's v | +0.79% | +1.54% | -0.25% | +0.42% |
| 16:35 | Automakers | GM, F, STLA, TSLA | negative | up (0.55) | repeat | We lost our auto industry. | +0.42% | +0.34% | +1.33% | +5.77% |
| 16:52 | Japan | EWJ | positive | none (0.52) | repeat | We made a deal with Japan, $650,000,000,000. | -1.61% | -1.27% | -1.71% | -2.07% |
| 16:57 | European Union | VGK, EZU, FEZ | negative | none (0.52) | repeat | We made a deal with the European Union, $950,000,000,000. | -0.50% | -0.21% | -0.90% | -1.19% |
| 17:00 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | European Union deal, they have to buy our oil and gas | +0.10% | +0.70% | -0.05% | -3.32% |
| 17:06 | China | FXI, MCHI, KWEB | positive | up (0.55) | repeat | We made a deal recently with China where they buy our soybeans | -0.60% | +0.33% | -0.95% | -1.58% |
| 17:08 | Agriculture | DBA, ADM, MOS, DE | positive | up (0.55) | repeat | They buy our soybeans, but it's hundreds of billions of dollars | +0.61% | +0.97% | -0.83% | -3.60% |
| 21:19 | Northrop Grumman | NOC | positive | up (0.55) | repeat | greatest military equipment anywhere in the world | +0.89% | +2.14% | +0.81% | -0.27% |
| 27:02 | McDonald's | MCD | positive | none (0.55) | repeat | board like no other other than perhaps the McDonald's board. You have  | +0.79% | +1.54% | -0.25% | +0.42% |
| 28:18 | Oil | XLE, USO, XOM, CVX | positive | none (0.50) | repeat | energy prices are way down. If you start bringing the price of gas, th | +0.10% | +0.70% | -0.05% | -3.32% |
| 34:13 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | farmers especially, have a great wonderful thing and a way of life | +0.61% | +0.97% | -0.83% | -3.60% |
| 41:47 | McDonald's | MCD | positive | none (0.55) | repeat | Carlos took over his 1st McDonald's. Where's Carlos? | +0.79% | +1.54% | -0.25% | +0.42% |
| 46:20 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The stock market hit its all time high | +0.00% | +0.00% | +0.00% | +0.00% |

### Delivers Remarks at the America Business Forum Miami — `6xVpv3kfvv8`
_the President Delivers Remarks at the America Business Forum Miami (The White House); stream start 2025-11-05 13:16 ET; 66 min; 28 heads-ups / 23 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 4:17 | McDonald's | MCD | neutral | none (0.55) | repeat | We did the McDonald's shot. Remember the McDonald's shot? | · | -0.95% | -1.13% | -0.27% |
| 4:26 | Google | GOOGL | positive | none (0.50) | repeat | McDonald's was the biggest hit in the history of Google. | · | +0.07% | +2.02% | +0.79% |
| 6:45 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | factories, AI, auto plants all over the country being built | · | -0.21% | -5.12% | -4.20% |
| 7:55 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The stock market has set 40 time all time record highs | · | +0.00% | +0.00% | +0.00% |
| 11:42 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | great Department of Agriculture headed by Brooke Rollins, we did a gre | · | -0.07% | -0.36% | -1.19% |
| 12:33 | Oil | XLE, USO, XOM, CVX | negative | down (0.55) | repeat | Gas prices are surging to $5 a gallon | · | +0.05% | +1.42% | +1.74% |
| 12:37 | Homebuilders | XHB, ITB, LEN, DHI | negative | none (0.50) | repeat | mortgage rates skyrocketed | · | -0.20% | +0.97% | +0.44% |
| 13:56 | Walmart | WMT | positive | none (0.55) | repeat | Grocery prices are way down, and Walmart | · | -0.04% | +0.75% | +0.54% |
| 14:48 | Federal Reserve | TLT, XLF, KRE | positive | none (0.50) | repeat | Interest rates are down despite the fact that we have a total nincompo | · | -0.07% | +2.30% | +0.78% |
| 26:25 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | I'm getting plants approved in 2 weeks. | · | -0.08% | +0.01% | -0.93% |
| 27:02 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | We're leading China. We're leading everybody by a lot. | · | +0.10% | +2.33% | +2.34% |
| 27:04 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | We're leading everybody by a lot in AI. | · | +0.07% | -4.92% | -3.99% |
| 28:04 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | Some by nuclear, some by oil and gas | · | -0.50% | +1.37% | +1.69% |
| 28:06 | Coal | BTU, ARCH, AMR | positive | up (0.58) | repeat | some by coal as a substitute | · | +0.13% | +3.65% | +4.03% |
| 35:18 | Bitcoin | IBIT, COIN, MSTR | positive | up (0.55) | repeat | signed historic executive orders to end the federal government's war o | · | +0.08% | -1.66% | -3.02% |
| 36:17 | Blockchain / crypto industry | COIN, IBIT, MSTR, HOOD | positive | up (0.55) | repeat | making The United States the crypto capital of the world | · | +0.53% | -5.68% | -4.84% |
| 51:47 | Nuclear energy | URA, CCJ, OKLO, SMR | positive | none (0.50) | repeat | We're the number 1 nuclear power. We redid our nuclear. | · | +0.47% | -4.37% | -5.29% |
| 52:54 | China | FXI, MCHI, KWEB | neutral | none (0.55) | repeat | We made a deal with China last week | · | +0.10% | +2.33% | +2.34% |
| 52:57 | Japan | EWJ | positive | none (0.52) | repeat | We made a deal with Japan last week. | · | -0.01% | +1.51% | +1.26% |
| 54:10 | Israel | EIS, ITA | positive | none (0.50) | repeat | Tariffs did that. Without tariffs, that would have never happened. | · | -0.03% | -0.27% | +2.36% |
| 54:11 | Iran | XLE, USO, ITA | positive | none (0.50) | repeat | Tariffs did that. Without tariffs, that would have never happened. | · | -0.50% | +1.37% | +1.69% |
| 62:40 | Steel | X, NUE, CLF, STLD | positive | none (0.50) | repeat | From the steel mills of Pittsburgh to the oil wells of Houston | · | · | · | · |
| 62:50 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | those coal mines are opening up 1 after another. Clean, beautiful coal | · | +0.13% | +3.65% | +4.03% |

### Delivers Keynote Remarks at APEC CEOs Luncheon — `eDOKTKbcJC4`
_the President Delivers Keynote Remarks at APEC CEOs Luncheon (The White House); stream start 2025-10-28 23:55 ET; 44 min; 49 heads-ups / 42 confirmed / 7 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 6:24 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | The stock market, as you know, has set | +0.00% | +0.00% | +0.00% | +0.00% |
| 7:35 | Toyota | TM | positive | up (0.60) | new | Yesterday, I was with mister Toyota | -2.23% | -2.21% | -0.86% | -4.34% |
| 7:36 | Japan | EWJ | neutral | none (0.50) | unclear | Yesterday, I was with mister Toyota in Japan | -0.73% | -0.86% | +0.19% | +0.03% |
| 8:11 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | Gasoline prices are down. | -0.13% | +0.18% | +1.20% | +1.45% |
| 8:15 | Homebuilders | XHB, ITB, LEN, DHI | positive | up (0.55) | repeat | Mortgage rates are down | -0.97% | -0.91% | -2.41% | -2.42% |
| 8:18 | Federal Reserve | TLT, XLF, KRE | negative | up (0.52) | repeat | incompetent head of the Fed. He's incompetent. | -0.39% | -0.56% | -0.53% | -1.95% |
| 10:33 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | Steel production is way up by 155,000 | · | · | · | · |
| 10:36 | Oil | XLE, USO | positive | none (0.50) | repeat | Oil production is through the roof by 500000 barrels a day | -0.13% | +0.18% | +1.20% | +1.45% |
| 10:42 | Coal | BTU, ARCH, AMR | positive | up (0.58) | unclear | mining of clean beautiful coal is up by 2,600,000 | +0.63% | -0.83% | -4.77% | +7.17% |
| 11:12 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | repeat | semiconductor manufacturing is rapidly returning to The United States | +1.40% | +1.96% | +1.22% | +0.39% |
| 11:16 | Nvidia | NVDA | positive | up (0.55) | repeat | semiconductor manufacturing is rapidly returning to The United States. | +3.22% | +4.49% | +1.98% | -1.52% |
| 11:18 | TSMC | TSM | positive | up (0.55) | repeat | semiconductor manufacturing is rapidly returning to The United States. | +1.17% | +0.85% | +1.61% | -1.24% |
| 11:52 | Semiconductors | SMH, SOXX | positive | up (0.55) | repeat | building tremendous plants in United States, Arizona, Texas | +1.40% | +1.96% | +1.22% | +0.39% |
| 12:21 | Artificial intelligence | NVDA, SMH | positive | up (0.62) | repeat | AI plants being built all over, tremendous strides creating great jobs | +3.22% | +4.49% | +1.98% | -1.52% |
| 15:17 | Defense | ITA, XAR, LMT, RTX | positive | up (0.55) | repeat | we're working with you on shipbuilding | -0.25% | -0.22% | +0.03% | -2.33% |
| 18:42 | Oil | XLE, USO, XOM, CVX | positive | none (0.52) | repeat | We have the most oil and gas and coal | -0.13% | +0.18% | +1.20% | +1.45% |
| 19:53 | South Korea | EWY | positive | none (0.50) | repeat | South Korea is buying a lot of our weapons. | +2.55% | +2.49% | +1.91% | +3.68% |
| 20:16 | Aluminum | AA, CENX | positive | up (0.55) | repeat | you need steel. You need aluminum. | +1.39% | +0.01% | -5.43% | -7.70% |
| 23:27 | Japan | EWJ | positive | none (0.50) | repeat | Japanese investors financed $16,000,000,000 plant in Louisiana | -0.73% | -0.86% | +0.19% | +0.03% |
| 23:30 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | guaranteeing a rapid and expedited regulatory review for all new proje | -1.38% | -0.56% | +4.94% | +11.83% |
| 26:18 | TSMC | TSM | positive | up (0.55) | repeat | TSMC has pledged to invest $100,000,000,000 in The United States. | +1.17% | +0.85% | +1.61% | -1.24% |
| 26:25 | Taiwan | EWT, TSM | positive | none (0.50) | repeat | TSMC has pledged to invest $100,000,000,000 in The United States. So t | +0.32% | +0.15% | +0.23% | -0.20% |
| 26:31 | Apple | AAPL | positive | up (0.55) | repeat | Apple, $600,000,000,000 investment. | -0.14% | +0.25% | +1.94% | +1.80% |
| 26:34 | Hyundai | HYMTF | positive | up (0.55) | repeat | Hyundai | · | · | · | · |
| 26:36 | Micron | MU | positive | up (0.55) | repeat | Micron, 200,000,000,000 | +2.98% | +3.29% | +2.00% | +8.41% |
| 26:37 | SoftBank | SFTBY | positive | none (0.55) | repeat | SoftBank | +2.76% | +2.53% | -1.01% | -10.85% |
| 26:39 | OpenAI | MSFT | positive | none (0.50) | repeat | OpenAI | +0.29% | -0.99% | -1.96% | -5.06% |
| 26:40 | Oracle | ORCL | positive | up (0.55) | repeat | Oracle, over 500,000,000,000 | -0.02% | -2.79% | -7.47% | -9.49% |
| 26:42 | Amazon | AMZN | positive | none (0.52) | repeat | Amazon, 35,000,000,000. | +0.81% | -0.33% | -1.74% | +10.52% |
| 26:44 | Pfizer | PFE | positive | up (0.55) | repeat | Pfizer, 70,000,000,000. | -0.12% | -0.16% | +0.20% | +1.83% |
| 26:48 | Google | GOOGL | positive | none (0.50) | repeat | Google, 25,000,000,000. | -0.14% | +0.39% | +6.29% | +7.68% |
| 26:50 | Nvidia | NVDA | positive | up (0.55) | repeat | Nvidia, [investment amount cut off] | +3.22% | +4.49% | +1.98% | -1.52% |
| 26:55 | Johnson & Johnson | JNJ | positive | up (0.55) | repeat | Johnson and Johnson, 57. We're bringing back all of our pharmaceutical | -0.36% | -1.03% | +2.19% | +0.88% |
| 26:58 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | none (0.50) | repeat | We're bringing back all of our pharmaceutical business. | -0.40% | -0.63% | +0.26% | +1.52% |
| 27:02 | AstraZeneca | AZN | positive | up (0.55) | repeat | AstraZeneca, 50,000,000,000 among many others | +0.70% | -0.21% | +0.73% | -0.39% |
| 32:31 | Defense | ITA, XAR, LMT, RTX | positive | up (0.55) | repeat | forging new partnerships on strategically important industries like sh | -0.25% | -0.22% | +0.03% | -2.33% |
| 32:33 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.55) | repeat | forging new partnerships on strategically important industries like sh | +1.40% | +1.96% | +1.22% | +0.39% |
| 33:00 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.52) | repeat | America is number 1 by a lot in artificial intelligence | +3.22% | +4.49% | +1.98% | -1.52% |
| 33:20 | Shipbuilders (Navy) | HII, GD, BWXT | positive | up (0.55) | repeat | We have a long lead on nuclear submarines. We are so far advanced. | +0.05% | -0.54% | +7.71% | +3.90% |
| 36:38 | India | INDA, EPI | positive | up (0.58) | repeat | I'm doing a trade deal with India, and I have great respect | +0.38% | +0.22% | +0.56% | +0.94% |
| 42:21 | South Korea | EWY | positive | none (0.52) | repeat | gleaming streets of Seoul | +2.55% | +2.49% | +1.91% | +3.68% |
| 42:28 | Japan | EWJ | positive | none (0.50) | repeat | from the bright lights of Tokyo | -0.73% | -0.86% | +0.19% | +0.03% |

### Makes an Announcement, Oct. 16, 2025 — `xagrobF4q1k`
_the President Makes an Announcement, Oct. 16, 2025 (The White House); stream start 2025-10-16 15:34 ET; 59 min; 22 heads-ups / 11 confirmed / 11 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:06 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | Drugs are gonna come down. Drug prices are coming down. | · | · | -0.03% | +0.80% |
| 3:15 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.52) | repeat | Drug prices are coming down. Great for Medicare, Medicaid. | · | · | -0.41% | -0.44% |
| 3:45 | United Kingdom | EWU | neutral | none (0.55) | repeat | In London, you'd buy a certain drug for $130 and even less. | · | · | -0.53% | -0.39% |
| 8:21 | Pfizer | PFE | neutral | down (0.55) | repeat | we were with Pfizer, and Pfizer's doing something very similar | · | · | +0.26% | -0.20% |
| 19:49 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | new | negotiated a spectacular MFN deal to reduce the cost of IVF drug price | · | · | -0.03% | +0.80% |
| 20:54 | CVS | CVS | positive | none (0.50) | unclear | CVS Specialty Pharmacy willing to stand up and do the right thing | · | · | +0.66% | -2.25% |
| 27:50 | Amazon | AMZN | positive | none (0.55) | repeat | large companies like Amazon and others offer benefits | +0.21% | -0.49% | -0.68% | +2.03% |
| 40:22 | Warner Bros. Discovery (CNN) | WBD | negative | none (0.55) | repeat | CNN fake news | -0.26% | +0.90% | -1.45% | +13.12% |
| 43:40 | RTX (Raytheon) | RTX | positive | none (0.50) | repeat | we need Tomahawks for | -0.29% | -0.16% | +0.72% | +11.24% |
| 51:26 | Russia | RSX, XLE | neutral | down (0.55) | unclear | sanctions on Russia | · | · | · | · |
| 57:32 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | Prices are down. Oil is down. | +0.59% | +0.28% | +0.27% | +0.76% |

### Hosts a Cabinet Meeting, Oct. 9, 2025 — `uUdwiR2s8JQ`
_the President Hosts a Cabinet Meeting, Oct. 9, 2025 (The White House); stream start 2025-10-09 11:51 ET; 70 min; 24 heads-ups / 14 confirmed / 10 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 5:57 | Iran | XLE, USO, ITA | negative | none (0.52) | repeat | attack was very important on Iran because they'd probably have nuclear | · | -0.03% | -0.87% | -1.93% |
| 8:19 | Russia | RSX, XLE | neutral | none (0.55) | repeat | Russia, Ukraine, and I think that's gonna happen too. | · | · | · | · |
| 10:01 | Pfizer | PFE | negative | down (0.60) | repeat | Pfizer and other country companies have already signed | · | +0.17% | +0.61% | -2.70% |
| 11:10 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.55) | repeat | We reduced drugs from 1 from the beginning of the year to the end of t | · | -0.06% | +0.95% | -0.04% |
| 11:34 | European Union | VGK, EZU, FEZ | negative | none (0.50) | repeat | pill or treatment selling in Europe for 10% of what we pay | · | -0.03% | +1.38% | +2.24% |
| 13:11 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.50) | repeat | This is gonna have a huge positive impact on Medicare, Medicaid | · | -0.42% | -2.37% | -2.93% |
| 21:24 | Oil | XLE, USO, XOM, CVX | positive | down (0.55) | repeat | gasoline is gonna be below $2 | · | -0.03% | -0.87% | -1.93% |
| 37:13 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | military power to reorder the globe | · | -0.05% | -0.62% | -1.66% |
| 40:42 | Space | RKLB, ARKX | positive | none (0.50) | repeat | I love our space force. It's turned out to be very important. | · | -0.08% | -1.30% | +1.66% |
| 46:22 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.50) | repeat | MFN agreement will lower the price of drugs. Immediately begins to aff | · | -0.34% | -1.97% | -2.52% |
| 51:35 | Vaccine makers | PFE, MRNA, NVAX | negative | down (0.60) | repeat | something artificially, I think, induced, something whether it's the v | · | +0.42% | +0.45% | -2.86% |
| 52:15 | Kenvue (Tylenol) | KVUE | negative | down (0.65) | repeat | don't take Tylenol | · | +1.28% | +3.71% | -12.84% |
| 65:37 | China | FXI, MCHI, KWEB | positive | down (0.55) | unclear | great deal with China where they would buy $50,000,000,000 | · | -0.15% | -2.99% | -0.04% |
| 66:51 | Agriculture | DBA, MOS, DE, CORN | positive | none (0.50) | repeat | I said to the farmers, buy larger tractors and more land. | · | +0.24% | +2.07% | +2.48% |

### Participates in a Bilateral Meeting with the Prime Minister of Canada — `qnRQP628zfM`
_the President Participates in a Bilateral Meeting with the Prime Minister of Canada (The White House); stream start 2025-10-07 11:57 ET; 33 min; 25 heads-ups / 14 confirmed / 11 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 4:04 | Steel | X, NUE, CLF, STLD | neutral | none (0.50) | repeat | they want steel and we want steel | · | · | · | · |
| 4:38 | Automakers | GM, F, STLA, TSLA | negative | none (0.52) | repeat | let car companies leave here and go to Canada | · | -0.04% | -1.73% | +1.21% |
| 5:30 | Canada | EWC | neutral | none (0.55) | repeat | continue to bring it in from Canada, but there is a tariff to pay | · | -0.35% | -0.60% | -0.16% |
| 7:39 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | It's coming in with AI. It's coming in with auto plants. | · | +0.26% | +1.52% | -1.76% |
| 16:44 | Canada | EWC | neutral | up (0.55) | unclear | They're gonna be very happy. We have a lot of things we're working on. | · | -0.35% | -0.60% | -0.16% |
| 17:31 | Agriculture | DBA, MOS, DE, CORN | negative | none (0.50) | repeat | our farmers went up to as much as 400% | · | +0.09% | -0.35% | +1.08% |
| 18:53 | European Union | VGK, EZU, FEZ | negative | none (0.50) | repeat | prior to the deal with Europe where they pay | · | +0.08% | -0.26% | +0.22% |
| 19:19 | Germany | EWG | negative | none (0.50) | repeat | They charge us tremendous. I said to Angela Merkel once, how many cars | · | +0.13% | -0.14% | -0.11% |
| 19:52 | Japan | EWJ | positive | none (0.55) | repeat | We made a deal with Japan. It's a much different deal. | · | +0.11% | -1.08% | -1.54% |
| 20:48 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | none (0.55) | repeat | windmills all over the place | · | -0.28% | -0.05% | +3.21% |
| 22:54 | Russia | RSX, XLE | neutral | none (0.52) | repeat | things happen with respect to Russia | · | · | · | · |
| 22:55 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | things happen with respect to Ukraine | · | +0.04% | +0.62% | +0.18% |
| 25:47 | Israel | EIS, ITA | neutral | none (0.50) | repeat | once this deal happens, if it does happen, look, they're in negotiatio | · | +0.33% | +0.63% | +2.49% |
| 29:34 | Canada | EWC | neutral | none (0.52) | unclear | trade deal with Canada that doesn't include supply managed goods | · | -0.35% | -0.60% | -0.16% |

### Signs Executive Orders, Sep. 30, 2025 — `SckFiRw0suk`
_the President Signs Executive Orders, Sep. 30, 2025 (The White House); stream start 2025-09-30 15:59 ET; 36 min; 15 heads-ups / 10 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 0:17 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | none (0.50) | repeat | harness the extraordinary potential of artificial intelligence | · | · | +0.26% | -1.02% |
| 1:34 | Bitcoin | IBIT, COIN, MSTR | positive | none (0.52) | repeat | AI and crypto czar, David Sachs. | +2.45% | +2.57% | +5.34% | +6.74% |
| 3:35 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | We're leading in AI. We're leading everybody by a lot. | -0.27% | +0.14% | +0.78% | +0.32% |
| 3:36 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | We're leading China by a lot. They're creating their own energy. | +0.60% | +0.45% | +1.03% | -1.26% |
| 15:28 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | new | lowering drug prices by 50, 102 | +0.90% | +1.53% | +2.43% | +2.80% |
| 15:52 | Pfizer | PFE | positive | down (0.60) | new | Alfred Bulla, and his company, Pfizer, agreed. | +2.37% | +4.16% | +5.82% | -0.26% |
| 20:00 | Artificial intelligence | NVDA, SMH | positive | up (0.52) | repeat | plants that are opening up in the country, $17,000,000,000,000 | -0.27% | +0.14% | +0.78% | +0.32% |
| 21:57 | Canada | EWC | neutral | down (0.55) | repeat | They're moving in from Canada. They're moving in from Mexico. | +0.33% | +0.52% | -0.38% | +0.13% |
| 25:02 | Health insurers | UNH, CI, ELV, HUM | negative | none (0.50) | repeat | we're gonna be paying whatever the lowest price is | +0.05% | +0.65% | +1.98% | +6.09% |
| 26:19 | Pharmaceuticals | XLV, XPH, PFE, LLY | positive | down (0.50) | repeat | money we're saving on pharmaceuticals | +0.90% | +1.53% | +2.43% | +2.80% |

### Signs Executive Orders, Sep. 19, 2025 — `gK9L029BcaM`
_the President Signs Executive Orders, Sep. 19, 2025 (The White House); stream start 2025-09-19 16:06 ET; 101 min; 33 heads-ups / 25 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 41:58 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | If you look at the stock market and other indicators, we have tremendo | +0.00% | +0.00% | +0.00% | +0.00% |
| 45:38 | China | FXI, MCHI, KWEB | positive | up (0.55) | unclear | I had a great call with president Xi | -0.34% | -0.70% | -1.95% | +0.13% |
| 45:46 | TikTok | ORCL | positive | up (0.62) | unclear | we approved the TikTok deal | +0.54% | +1.88% | +1.75% | -8.39% |
| 52:07 | Paramount (CBS) | PSKY | negative | none (0.55) | repeat | 60 minutes took Kamala's answer | +0.23% | -0.27% | +4.36% | +3.07% |
| 53:45 | Russia | RSX, XLE | neutral | none (0.50) | repeat | We're working with Russia and Ukraine. | · | · | · | · |
| 53:46 | Ukraine | ITA, XLE | neutral | none (0.50) | repeat | We're working with Russia and Ukraine. | +0.05% | -0.58% | +1.43% | +1.01% |
| 54:00 | Federal Reserve | TLT, XLF, KRE | negative | none (0.50) | repeat | Powell is terrible. He's terrible. | +0.00% | -0.44% | +0.41% | +0.69% |
| 54:18 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | We have another record stock market today. | +0.00% | +0.00% | +0.00% | +0.00% |
| 58:40 | Iran | XLE, USO, ITA | negative | none (0.50) | repeat | destruction of a vast potential nuclear disaster in Iran, which we wip | -0.97% | -1.48% | +0.82% | +2.01% |
| 58:50 | Northrop Grumman | NOC | positive | up (0.65) | new | Just ordered some more of them, by the way. The B2 bomber. | +0.34% | -0.54% | +0.78% | +3.66% |
| 59:36 | Shipbuilders (Navy) | HII, GD, BWXT | positive | none (0.52) | repeat | fired 30 of them from a submarine | -0.23% | -0.44% | +0.39% | +1.60% |
| 60:00 | China | FXI, MCHI, KWEB | neutral | none (0.50) | repeat | President Xi and I spoke to him about it | -0.34% | -0.70% | -1.95% | +0.13% |
| 72:37 | Vaccine makers | PFE, MRNA, NVAX | negative | down (0.55) | unclear | Autism out of control. Bobby Kennedy unwinding the vaccine. | +1.27% | +2.44% | +0.49% | -0.75% |
| 73:07 | Pfizer | PFE | negative | none (0.55) | repeat | Pfizer where they spent a lot of money | +1.27% | +2.44% | +0.49% | -0.75% |
| 73:09 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | none (0.50) | repeat | drug companies they spent a lot of money on | -0.58% | -0.44% | -0.18% | -1.01% |
| 76:45 | TikTok | ORCL | positive | up (0.55) | repeat | save TikTok. So many people. It's a big thing. | +0.54% | +1.88% | +1.75% | -8.39% |
| 77:47 | Trucking / rail | UNP, CSX, IYT | positive | up (0.55) | repeat | beautiful railroad. He's a great guy. | +0.24% | +2.37% | +3.41% | +7.06% |
| 79:41 | Uber | UBER | negative | none (0.55) | repeat | they took Uber and they took other forms of transportation, they felt  | +0.72% | +2.87% | -0.65% | +1.08% |
| 82:15 | Disney (ABC) | DIS | negative | down (0.55) | repeat | ABC is a terrible network, a very unfair network | -1.53% | -0.49% | -1.25% | +0.90% |
| 82:20 | Comcast (NBC, MSNBC) | CMCSA | negative | none (0.55) | repeat | NBC is equally bad. I think they're equally bad. | -0.60% | -0.67% | +0.17% | -0.31% |
| 92:52 | Visa | V | positive | none (0.55) | unclear | h 1 b visas and all of the big companies are on board | -0.54% | +0.34% | -0.78% | -0.42% |
| 96:30 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | China, for years, charged us tariffs, and they continue to do it | -0.34% | -0.70% | -1.95% | +0.13% |
| 96:40 | European Union | VGK, EZU, FEZ | positive | none (0.50) | repeat | European Union, as you know, I get along very well with them | +0.29% | -0.21% | +0.43% | +0.10% |
| 97:12 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.50) | repeat | We'll be able to take care of our Medicare, Medicaid, Social Security. | -0.44% | +0.38% | +3.34% | +2.52% |
| 100:22 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | We have the highest stock market in history. | +0.00% | +0.00% | +0.00% | +0.00% |

### Makes an Announcement, Sep. 2, 2025 — `qn2K3UyIsEo`
_the President Makes an Announcement, Sep. 2, 2025 (The White House); stream start 2025-09-02 14:40 ET; 49 min; 19 heads-ups / 14 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 4:01 | Defense | ITA, XAR, LMT, RTX | positive | up (0.55) | repeat | SpaceCom will play a key role in building the Golden Dome | · | +0.12% | -1.41% | -2.81% |
| 7:45 | SpaceX | RTX, LMT | neutral | · | · | We have NASA, Blue Origin, and SpaceX. | · | · | · | · |
| 12:54 | Nuclear energy | URA, CCJ, OKLO, SMR | positive | none (0.50) | repeat | knocking out potential nuclear power for a long time to come | · | +0.85% | +2.20% | +2.74% |
| 35:34 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market needs the tariffs, they want the tariffs | · | · | +0.00% | +0.00% |
| 35:42 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | repeat | If you look at AI | · | · | -0.10% | -1.05% |
| 36:56 | Japan | EWJ | positive | none (0.52) | repeat | We signed a deal with Japan. They're paying us hundreds of billions of | · | · | -0.97% | +0.73% |
| 37:00 | South Korea | EWY | positive | none (0.50) | repeat | We signed a deal with South Korea. | · | · | +0.70% | +2.46% |
| 37:02 | European Union | VGK, EZU, FEZ | positive | none (0.52) | repeat | We signed a deal with the European Union. | · | · | -0.25% | +0.35% |
| 38:25 | India | INDA, EPI | neutral | none (0.52) | repeat | We'll get along with India very well. But India has | · | · | -0.34% | -1.20% |
| 39:15 | Harley-Davidson | HOG | negative | none (0.55) | repeat | I'll give you an example, Harley Davidson. | · | · | -0.02% | +4.41% |
| 39:36 | Automakers | GM, F, STLA, TSLA | neutral | up (0.52) | repeat | car companies are coming into The US | · | · | -2.13% | -2.72% |
| 39:47 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | they're coming from China | · | · | -1.31% | +0.37% |
| 39:48 | Mexico | EWW | negative | none (0.50) | repeat | they're coming from Mexico | · | · | -1.02% | +0.27% |
| 43:24 | Federal Reserve | TLT, XLF, KRE | neutral | up (0.55) | repeat | We need a little help from the Fed. | · | · | +0.21% | +2.29% |

### Signs Executive Orders, Aug. 25, 2025 — `rlPfxyCnxHg`
_the President Signs Executive Orders, Aug. 25, 2025 (The White House); stream start 2025-08-25 10:36 ET; 78 min; 19 heads-ups / 12 confirmed / 7 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 8:55 | Rivian | RIVN | negative | down (0.55) | repeat | when I have some slob like Rivian criticizing us | · | -1.46% | -0.48% | +5.26% |
| 43:15 | India | INDA, EPI | positive | none (0.50) | repeat | war with India and Pakistan, that was the next level that was gonna be | · | -0.13% | -1.78% | -1.39% |
| 59:10 | Intel | INTC | positive | up (0.60) | repeat | I wanna try and get as much as I can. If people come in and they need  | · | -0.50% | -3.32% | -3.11% |
| 61:22 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market went up almost 1000 points on Friday | · | +0.00% | +0.00% | +0.00% |
| 64:33 | Rare earths | MP, REMX | positive | none (0.50) | repeat | 1000000000000 dollars worth of air that we have from the country | · | -0.22% | -3.79% | -6.50% |
| 64:56 | Ukraine | ITA, XLE | neutral | up (0.55) | repeat | We don't deal really with Ukraine. | · | -0.09% | +1.68% | +1.69% |
| 64:59 | RTX (Raytheon) | RTX | neutral | up (0.55) | repeat | They want Patriots. They want missiles. We give the missiles to NATO. | · | -0.00% | +1.81% | +1.57% |
| 65:21 | Lockheed Martin | LMT | positive | up (0.55) | repeat | I gave the Javelins. They were very effective. | · | -0.07% | +1.87% | +1.97% |
| 66:19 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | NATO agreed to go to 5%. They had 2% and didn't pay. | · | -0.09% | +1.68% | +1.69% |
| 72:33 | Health insurers | UNH, CI, ELV, HUM | positive | none (0.55) | repeat | we're not gonna hurt anybody on Medicaid, Medicare, or Social Security | · | -0.62% | -1.74% | +1.76% |
| 73:16 | Pharmaceuticals | XLV, XPH, PFE, LLY | negative | down (0.55) | repeat | reducing drug prices by 1500% | · | -0.30% | +0.10% | +1.23% |
| 73:21 | Germany | EWG | neutral | none (0.55) | repeat | pill that sells in Germany for $10 costs $150 | · | +0.02% | -0.58% | -2.40% |

### Makes an Announcement, Aug. 22, 2025 — `rB9gbCxb_K0`
_the President Makes an Announcement, Aug. 22, 2025 (The White House); stream start 2025-08-22 12:50 ET; 67 min; 17 heads-ups / 12 confirmed / 5 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 19:47 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | the stock market went up 1000 points | · | +0.00% | +0.00% | +0.00% |
| 36:21 | Steel | X, NUE, CLF, STLD | positive | none (0.52) | repeat | high grade steel, very hard to cut | · | · | · | · |
| 40:25 | Russia | RSX, XLE | negative | down (0.55) | unclear | I'm not happy about it, and I'm not happy about anything having to do  | · | · | · | · |
| 40:26 | Ukraine | ITA, XLE | negative | none (0.50) | repeat | I'm not happy about anything having to do with that war. | · | -0.32% | -0.26% | +0.90% |
| 53:24 | Stock market | SPY, QQQ, DIA | positive | none (0.50) | repeat | stock market today, it's way up to start off with | · | +0.00% | +0.00% | +0.00% |
| 54:11 | European Union | VGK, EZU, FEZ | positive | up (0.55) | repeat | We just signed a deal with the European Union. They're paying us essen | · | +0.02% | -0.97% | -1.99% |
| 54:48 | Intel | INTC | positive | up (0.65) | new | I met a man. He was a very nice man, and I called for his removal | · | +0.31% | -0.92% | -2.12% |
| 55:47 | Nvidia | NVDA | neutral | none (0.55) | repeat | Jensen and some of our friends, Nvidia | · | +0.02% | +1.42% | -2.14% |
| 56:09 | Taiwan | EWT, TSM | negative | down (0.55) | repeat | put a 100% tariff or a 200 or a 300 or a 500% | · | +0.15% | -0.14% | -1.28% |
| 57:21 | Nvidia | NVDA | neutral | none (0.55) | unclear | We have restrictive covenants with Jensen. We have it's Nvidia. | · | +0.02% | +1.42% | -2.14% |
| 59:13 | Bank of America | BAC | neutral | none (0.55) | repeat | I own a big chunk of the Bank of America building in San Francisco. | · | +0.21% | +0.57% | +2.72% |
| 61:56 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | He's too late. You should've cut them a year ago. | · | +0.15% | +0.32% | -0.31% |

### Signs an Executive Order, Aug. 5, 2025 — `QFBG9DBdsHg`
_the President Signs an Executive Order, Aug. 5, 2025 (The White House); stream start 2025-08-05 15:52 ET; 32 min; 9 heads-ups / 1 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 22:05 | Agriculture | DBA, MOS, DE, ADM | positive | none (0.50) | repeat | we wanna help our farmers because our farmers are producing like never | -0.21% | -0.32% | +0.59% | +1.09% |

### Delivers Remarks on Making Health Technology Great Again — `xqlARu9srSY`
_the President Delivers Remarks on Making Health Technology Great Again (The White House); stream start 2025-07-30 16:34 ET; 38 min; 20 heads-ups / 12 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:09 | European Union | VGK, EZU, FEZ | positive | up (0.55) | repeat | We've done very well with the EU deal. It's a very big deal. | -1.42% | -1.33% | +0.39% | +1.50% |
| 1:17 | Japan | EWJ | positive | up (0.55) | repeat | Just completed Japan | -0.42% | -0.79% | +2.13% | +3.92% |
| 1:38 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | factories for AI and for | +1.24% | +0.60% | -1.09% | +1.19% |
| 5:31 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | administrator of the Centers for Medicine and Medicaid Services | -2.53% | -4.33% | -8.62% | -7.68% |
| 5:56 | Apple | AAPL | neutral | none (0.55) | repeat | representatives from Apple | -1.06% | -0.79% | -1.18% | +5.60% |
| 5:57 | Google | GOOGL | neutral | none (0.55) | repeat | representatives from Apple, Google, Samsung, Amazon, OpenAI | -1.21% | -2.02% | -1.76% | +0.34% |
| 5:58 | Samsung | SSNLF | neutral | none (0.55) | repeat | representatives from Apple, Google, Samsung | -0.79% | · | +2.01% | +0.35% |
| 5:59 | Amazon | AMZN | neutral | none (0.55) | repeat | representatives from Apple, Google, Samsung, Amazon | +1.64% | +0.33% | -4.70% | -2.72% |
| 6:00 | OpenAI | MSFT | neutral | none (0.50) | repeat | representatives from Apple, Google, Samsung, Amazon, OpenAI | +7.39% | +4.08% | +4.13% | +1.83% |
| 6:04 | Oracle | ORCL | positive | up (0.52) | unclear | representatives from Apple, Google, Samsung, Amazon, OpenAI, Anthropic | +1.27% | +2.22% | -0.46% | -0.13% |
| 16:03 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.55) | repeat | 60 years ago today, we passed Medicaid and Medicare | -2.53% | -4.33% | -8.62% | -7.68% |
| 27:19 | Health insurers | UNH, CI, ELV, HUM | neutral | none (0.50) | repeat | 91 percent of Medicaid patients have smartphones | -2.53% | -4.33% | -8.62% | -7.68% |

### Delivers Remarks and Signs Executive Orders at AI Summit — `tBNX9x5GgPE`
_the President Delivers Remarks and Signs Executive Orders at AI Summit (The White House); stream start 2025-07-23 17:10 ET; 57 min; 39 heads-ups / 36 confirmed / 3 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1:19 | Japan | EWJ | positive | up (0.60) | new | we've just concluded our big trade deal with Japan | +0.29% | +0.43% | -1.51% | -3.42% |
| 2:53 | Stock market | SPY, QQQ, DIA | positive | up (0.55) | repeat | their stock market went up, and our stock market went up | +0.00% | +0.00% | +0.00% | +0.00% |
| 3:52 | European Union | VGK, EZU, FEZ | neutral | up (0.55) | unclear | We've offered such a deal to the European Union | -0.97% | -0.88% | -1.34% | -4.59% |
| 5:15 | China | FXI, MCHI, KWEB | neutral | up (0.55) | repeat | in the process of completing our deal with China | -0.09% | -0.17% | -1.56% | -3.86% |
| 5:17 | United Kingdom | EWU | positive | none (0.52) | repeat | The UK, we made a deal. It was a very good deal for everybody. | -0.01% | +0.00% | -1.09% | -2.33% |
| 11:09 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | making incredible deals on energy, including deals in Alaska | -0.33% | +0.01% | -0.12% | +0.80% |
| 14:26 | Nvidia | NVDA | negative | none (0.55) | repeat | I said, we'll break them up. He has 100% market. | +0.91% | +0.67% | +1.14% | +4.49% |
| 14:27 | Nvidia | NVDA | negative | none (0.60) | repeat | I said we'll break them up. He has 100% market share. | +0.91% | +0.67% | +1.14% | +4.49% |
| 15:28 | Palantir | PLTR | positive | up (0.55) | repeat | Sham Sanacar of Palantir | -0.48% | -0.02% | +2.24% | +2.74% |
| 15:38 | European Union | VGK, EZU, FEZ | positive | none (0.50) | repeat | made a deal with the European Union | -0.97% | -0.88% | -1.34% | -4.59% |
| 15:45 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.65) | repeat | made a deal with the European Union, they're gonna pay 100% of the cos | +0.23% | +0.63% | +0.25% | +0.19% |
| 17:19 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | one of the most important technological revolutions in the history of  | +0.91% | +0.67% | +1.14% | +4.49% |
| 20:43 | China | FXI, MCHI, KWEB | negative | none (0.52) | repeat | China's not doing it, and if you're gonna be beating China | -0.09% | -0.17% | -1.56% | -3.86% |
| 21:36 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | AI to use that pool of knowledge without going complexity of contract  | +0.91% | +0.67% | +1.14% | +4.49% |
| 26:33 | Automakers | GM, F, STLA, TSLA | positive | none (0.50) | repeat | car companies moving in all the time | -0.36% | -0.04% | +0.05% | +0.73% |
| 27:57 | India | INDA, EPI | negative | none (0.52) | repeat | hiring workers in India | -0.61% | -0.86% | -2.15% | -3.48% |
| 28:54 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.62) | repeat | ensure that The United States can build and maintain the largest, most | +0.91% | +0.67% | +1.14% | +4.49% |
| 29:00 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.60) | repeat | America needs new data centers, new semiconductor | +0.14% | -0.24% | -0.15% | +1.09% |
| 33:51 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | on day 1, I terminated the Green New scam | +0.88% | +0.23% | -0.86% | -5.95% |
| 35:38 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | unleashing all forms of energy, including natural gas, oil, and clean  | +2.05% | +1.58% | +0.42% | -0.54% |
| 36:15 | Coal | BTU, ARCH, AMR | positive | up (0.55) | repeat | China's using it. They're building now 57 big power plants all fueled  | -0.00% | -0.10% | -4.37% | -6.74% |
| 37:27 | Oil | XLE, USO, XOM, CVX | positive | up (0.55) | repeat | drill baby drill and build baby build | -0.33% | +0.01% | -0.12% | +0.80% |
| 37:34 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | China added 11 times as much power generation capacity as did The Unit | -0.09% | -0.17% | -1.56% | -3.86% |
| 38:24 | Amazon | AMZN | positive | none (0.55) | repeat | In a few months, Meta, Amazon | +0.32% | +1.03% | +0.92% | +2.89% |
| 38:25 | Google | GOOGL | positive | none (0.55) | repeat | Meta, Amazon, Google, Microsoft are all investing | +3.51% | +1.46% | +1.10% | +1.21% |
| 38:25 | Microsoft | MSFT | positive | none (0.52) | repeat | Meta, Amazon, Google, Microsoft are all investing | +0.51% | +0.49% | +1.09% | +5.80% |
| 38:55 | Nvidia | NVDA | positive | up (0.55) | repeat | Google, Microsoft investing $320 billion in data centers, AI infrastru | +0.91% | +0.67% | +1.14% | +4.49% |
| 39:00 | Nvidia | NVDA | positive | none (0.50) | repeat | Nvidia has committed $500,000,000,000 over the next 4 years. Thank you | +0.91% | +0.67% | +1.14% | +4.49% |
| 39:19 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | $92 billion in energy and data center projects, largest natural gas po | +0.91% | +0.67% | +1.14% | +4.49% |
| 41:08 | Artificial intelligence | NVDA, SMH | positive | up (0.62) | unclear | get the entire world running on the backbone of American | +0.91% | +0.67% | +1.14% | +4.49% |
| 43:27 | Saudi Arabia | KSA, XLE | positive | up (0.55) | repeat | king of Saudi Arabia met 3 great leaders. We're gonna come home with t | -0.19% | -0.75% | -1.11% | -0.74% |
| 44:01 | Defense | ITA, XAR, AVAV, KTOS | positive | up (0.55) | repeat | NATO weeks ago, where we made the deal where they pay 5% instead of 2% | +0.23% | +0.63% | +0.25% | +0.19% |
| 44:46 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | up (0.58) | unclear | expand American AI exports of all kinds from chips to software | +0.14% | -0.24% | -0.15% | +1.09% |
| 50:52 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | Joe Biden had a plan to lose the AI race | +0.91% | +0.67% | +1.14% | +4.49% |
| 51:20 | OpenAI | MSFT | positive | up (0.52) | repeat | The people of OpenAI, pushing the bounds of human knowledge. | +0.51% | +0.49% | +1.09% | +5.80% |
| 51:21 | Google | GOOGL | positive | up (0.55) | repeat | The people of OpenAI, Google, pushing the bounds of human knowledge | +3.51% | +1.46% | +1.10% | +1.21% |

### Participates in the Inaugural Pennsylvania Energy and Innovation Event — `5N8iGKpU_-A`
_the President Participates in the Inaugural Pennsylvania Energy and Innovation Event (The White House); stream start 2025-07-15 15:30 ET; 61 min; 45 heads-ups / 24 confirmed / 21 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 8:23 | Boeing | BA | positive | up (0.55) | repeat | many, many planes that they are gonna build through Boeing | · | · | -0.69% | -2.04% |
| 12:22 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | they're building plants already, amazing job | · | · | +0.54% | -2.76% |
| 15:27 | Coal | BTU, ARCH, AMR | positive | up (0.58) | repeat | We brought coal back in. Maybe powered by coal. | · | · | -2.15% | +14.55% |
| 20:37 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | repeat | America's destiny is to dominate every industry in artificial intellig | · | · | +0.54% | -2.76% |
| 20:40 | China | FXI, MCHI, KWEB | negative | none (0.50) | repeat | We are way ahead of China | · | · | -0.49% | +2.14% |
| 20:47 | Defense | ITA, XAR, AVAV, KTOS | positive | none (0.50) | repeat | plants are starting up. The construction is starting up. | · | · | +0.36% | -1.55% |
| 21:11 | Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | tariffs are coming in by the hundreds of billions of dollars, mostly o | · | · | · | · |
| 21:25 | Copper | COPX, FCX, SCCO | positive | none (0.50) | unclear | Indonesia really has great copper, very powerful copper, full access | · | · | -0.15% | +3.17% |
| 21:54 | India | INDA, EPI | positive | up (0.55) | unclear | India is gonna open up and a lot of countries are gonna open up. | · | · | +0.49% | -1.46% |
| 22:16 | Semiconductors | SMH, SOXX, NVDA, INTC | positive | none (0.50) | repeat | We have the great chips. We have the great everything. | · | · | -0.64% | -2.73% |
| 23:42 | Artificial intelligence | NVDA, SMH | positive | up (0.55) | repeat | remaining the world's leader in AI will require enormous energy produc | · | · | +0.54% | -2.76% |
| 24:27 | Solar / wind | TAN, ICLN, FSLR, ENPH | negative | down (0.55) | repeat | green new scam, greatest scam in history | · | · | -1.16% | +3.98% |
| 25:19 | Google | GOOGL | positive | up (0.55) | new | Google will be investing billions and billions of dollars to revitaliz | · | · | -0.28% | +3.54% |
| 26:41 | Coal | BTU, ARCH, AMR | negative | up (0.55) | repeat | they're building right now about 52 power plants, all of coal | · | · | -2.15% | +14.55% |
| 26:49 | Nuclear energy | URA, CCJ, OKLO, SMR | positive | up (0.55) | repeat | I signed historic executive orders to expedite construction of brand n | · | · | +1.92% | +1.76% |
| 28:20 | U.S. Steel | X, NUE, CLF, STLD | positive | up (0.55) | repeat | historic investment deal with Nippon Steel | · | · | · | · |
| 28:22 | Japan | EWJ | positive | none (0.52) | repeat | Nippon Steel of Japan | · | · | +0.33% | +0.92% |
| 31:16 | Steel | X, NUE, CLF, STLD | positive | up (0.60) | repeat | American workers will forge the steel, produce the energy, build the f | · | · | · | · |
| 32:32 | Private equity | BX, KKR, APO | positive | up (0.60) | unclear | You'll hear from Blackstone | +1.75% | +3.31% | +6.99% | +5.67% |
| 34:21 | Natural gas / LNG | UNG, LNG, EQT | positive | none (0.50) | repeat | Unbelievable natural gas reserves, abundant freshwater | +1.61% | +1.58% | +0.08% | -13.72% |
| 35:42 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.55) | new | $25,000,000,000 in data center and energy infrastructure in Northeast  | -0.05% | -0.49% | +0.40% | -1.89% |
| 46:12 | Artificial intelligence | NVDA, SMH | positive | none (0.52) | unclear | AI works for America. partnerships with leading employers | -0.05% | -0.49% | +0.40% | -1.89% |
| 47:37 | Artificial intelligence / data centers | NVDA, SMH, MSFT, VRT | positive | up (0.52) | repeat | investing $6,000,000,000 into a Lancaster, Pennsylvania, data center | -0.05% | -0.49% | +0.40% | -1.89% |
| 56:42 | Natural gas / LNG | UNG, LNG, EQT | positive | up (0.55) | repeat | Pennsylvania natural gas production could ramp up tremendously | +1.61% | +1.58% | +0.08% | -13.72% |

### Participates in Invest America Roundtable — `dLhUDEOIdks`
_the President Participates in Invest America Roundtable (The White House); stream start 2025-06-09 14:40 ET; 54 min; 15 heads-ups / 7 confirmed / 8 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 3:19 | Stock market | SPY, QQQ, DIA | positive | none (0.55) | repeat | will track the overall stock market | · | +0.00% | +0.00% | +0.00% |
| 3:33 | Dell | DELL | positive | none (0.55) | repeat | Maybe you should be the index. I'd like to have that. | · | +0.13% | -1.78% | -1.28% |
| 6:59 | Goldman Sachs | GS | positive | none (0.55) | repeat | very powerful man in the world of business, CEO David Solomon of Goldm | · | -0.45% | -0.82% | +1.35% |
| 14:47 | Dell | DELL | positive | none (0.55) | repeat | leadership of Brad Gerstner and Michael Dell in really having the visi | · | +0.13% | -1.78% | -1.28% |
| 35:10 | China | FXI, MCHI, KWEB | neutral | up (0.55) | repeat | We wanna open up China. It'll be a great thing for China, great thing  | · | · | -0.00% | -1.42% |
| 37:08 | SpaceX | TSLA | positive | · | · | It's a good service. | · | · | · | · |
| 49:42 | Goldman Sachs | GS | negative | none (0.55) | repeat | If Goldman Sachs was like that, you wouldn't have Goldman Sachs anymor | · | · | -0.37% | +1.81% |

### Holds a Press Briefing, June 27, 2025 — `XkgLela6l6o`
_the President Holds a Press Briefing, June 27, 2025 (The White House); stream start 2025-06-27 11:28 ET; 76 min; 20 heads-ups / 13 confirmed / 7 retracted_

| t | entity | tickers | stance | judge (primary) | novelty | quote | open | +1h | d+1 | d+5 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 35:20 | China | FXI, MCHI, KWEB | positive | up (0.55) | repeat | We've made a deal with China. | · | -0.21% | -0.69% | -2.37% |
| 35:25 | United Kingdom | EWU | positive | none (0.52) | repeat | With The UK, it was a great deal for both. | · | -0.03% | -0.60% | -1.81% |
| 35:59 | India | INDA, EPI | positive | up (0.55) | new | we're gonna reach a deal where we have the right to go in and trade | · | -0.08% | -0.88% | -1.91% |
| 38:27 | Russia | RSX, XLE | negative | none (0.55) | repeat | fake news...from Russia...Russia Russia Russia hoax | · | · | · | · |
| 47:40 | Artificial intelligence | NVDA, SMH | positive | none (0.50) | repeat | AI is being built here instead of being built all over Europe and Asia | · | -0.30% | -0.36% | -0.66% |
| 47:43 | European Union | VGK, EZU, FEZ | negative | none (0.55) | repeat | AI is being built here instead of being built all over Europe and Asia | · | +0.18% | -0.15% | -1.00% |
| 54:47 | Russia | RSX, XLE | neutral | none (0.50) | repeat | we talk about Russia, and we're gonna work | · | · | · | · |
| 55:05 | India | INDA, EPI | positive | none (0.52) | repeat | We did some great work. India and Pakistan, | · | -0.08% | -0.88% | -1.91% |
| 58:13 | Health insurers | UNH, CI, ELV, HUM | negative | none (0.50) | repeat | destroy Social Security, destroy Medicare, and destroy | · | +1.01% | +1.62% | -1.54% |
| 58:38 | Bitcoin | IBIT, COIN, MSTR | positive | up (0.55) | repeat | I became a fan of crypto, I view it as an industry. | · | +0.29% | +0.34% | +0.19% |
| 64:41 | Nuclear energy | URA, CCJ, OKLO, SMR | negative | none (0.50) | repeat | If Iran can enrich uranium to a level that concerns you, would you con | · | -0.01% | +0.87% | -1.75% |
| 73:02 | Federal Reserve | TLT, XLF, KRE | negative | up (0.55) | repeat | He doesn't wanna lower the rates. He could lower the interest cost by  | · | +0.06% | -0.02% | -2.87% |
| 73:56 | Iran | XLE, USO, ITA | negative | down (0.55) | repeat | talking about this for 30 years about Iran being nuclear | · | +0.36% | -0.68% | +0.48% |

## Coverage

- 3 of 1534 confirmed signals have no judge verdict (API credit ran out / unparseable reply); they count as 'none' in the judge tables and are still in the stance tables. Re-run `uv run backtest judge` to fill them.
- Tickers without usable Yahoo data: ARCH, BRFS, BRK.B, HYMTF, RSX, X (delisted or OTC).
- Where Yahoo's intraday bars and split-adjusted daily closes disagreed (a later split), the bars were rescaled to the daily basis.

## Caveats

- Small sample: a handful of videos and a few dozen signals. Hit rates near 50% with p > 0.1 are noise.
- Judge look-ahead: for 2025 events the judge model may remember what happened; the stance baseline cannot. Compare the 'recent videos' split, which is after the model's knowledge.
- Timing: t_audio is mapped to wall clock via the livestream's start timestamp; if the recording was trimmed the mapping is off by that amount. Baseline is the mention minute, not the alert time (live latency is ~5-10 s).
- Intraday horizons need bars no coarser than the horizon: Yahoo serves 1-minute bars for ~30 days, 5-minute for ~60 days and hourly for ~2 years, so +10m/+30m are blank for 2025 events.
- +1h/+2h are blank when the session ended in between (see close_d0 instead). Closed-market mentions measure intraday horizons from the next session's open.
- Abnormal return subtracts SPY over the identical window; sector moves are not removed.
- Multi-ticker signals (sector ETFs, judge additions) are in the 'all tickers' split only; the headline tables use one primary ticker per signal.
