# Findings: do the speechalerts signals move prices, and what should the product send?

_Written 2026-09-15 from the 78-video run (74.5 h of speech, Jun 2025 – Sep 2026). Numbers come from
`data/results/summary.md`, `analysis.md` and `portfolio.md`; re-run the stages to refresh them._

## 1. The short answer

- **On average the alerts do not predict price moves.** Across 979 measurable signals (first mention
  per video, primary ticker) the sign-adjusted abnormal return is +0.17% after one day and +0.25%
  after two (t ≈ 1.2–1.3, hit rate 49–52%). After a week it is zero. Intraday (+10 min to +2 h) the
  average move is a few basis points.
- **The first 19-video result (+1.2% next-day drift on positive mentions) did not survive the larger
  sample.** It came from one lucky group of recent videos (64% hit, +1.1%); the 59 added videos show
  46% and +0.01%. Treat that earlier number as noise.
- **A $10k account that bought every positively labelled mention and sold a week later** ended at
  $11,349 buying at the mention price and $12,663 buying at the next open, over a span in which SPY
  rose 25%. The mean trade is +0.2–0.3% raw, win rate 52–55%, t ≈ 1–1.5: that is market beta, not
  signal. Buying only what the judge expected to rise lost money (−13% to −19%), and the "new
  information" subset lost 42–46%, because those trades cluster on tariff days (Liberation Day:
  steel, autos and Apple were "positive" mentions and fell 8–12% with the market).
- **The one consistent pocket:** company mentions tied to a hard action (investment, deal, sanction,
  regulation, subsidy, tariff) show +0.5% next-day abnormal return with a 55% hit rate, and the sign
  holds in all three video groups (recent 75% / +1.4%, expansion 50% / +0.4%, 2025 headline 53% /
  +0.3%). It is 12% of today's alert volume. Weak (t ≈ 1.2), but it is the only filter that does not
  flip sign across groups.
- **Direction by action label:** sanction (80% hit, +1.4% d1, n = 18), investment (52% / +0.7%,
  n = 158) and regulation (57% / +0.6%, n = 80) go the expected way; tariff (42% / −0.5%, n = 105),
  deal (43% / −0.4%) and subsidy (25% / −1.3%) go the wrong way. "Tariffs help domestic producers"
  does not play out; tariff mentions hurt everything named near them.

## 2. Why the feed feels like too many tickers

| fact | value |
|---|---|
| confirmed alerts per hour of speech | 20.6 (≈ 54 ticker pushes per hour at 2.6 tickers per alert) |
| alerts that are country ETFs | 29% (China, Japan, Mexico, EU, Canada …) |
| alerts that are sector baskets of 3+ tickers | 46% |
| alerts the judge called repeated rhetoric / not price-relevant | 80% repeat; 58% "no direction" |
| alerts that are macro words ("stock market", "the Fed") | 70 (96% judged irrelevant) |
| mentions folded by the 10-minute cooldown | 1,008 (each alert is ~2 mentions) |

Country alerts are not just noise, they lean the wrong way: 44% hit, −0.31% next day, −1.4% on the
2025 headline days. "Stock market", "AI", "Germany", "South Korea", "Google", "Boeing" fired 8–45
times each with a 0% next-day hit rate.

## 3. What a better feed would send (to test in a separate feed, not the live one)

1. **Drop country and macro entities as alerts** (China, Japan, EU, Mexico, Canada, "stock market",
   "the Fed"). That removes ~35% of volume and the worst-performing group. Keep them as context
   words for the LLM, not as pushes.
2. **Send sector baskets only with a hard action.** Sector mentions ("oil", "steel", "pharma") are
   35% of volume and average +0.27% next day with no consistency; the ETF list on each alert is what
   makes the feed feel like a ticker firehose. One ticker per alert.
3. **Promote company + hard action to the top tier.** Company named, action in {investment, deal,
   sanction, regulation, subsidy, tariff}, LLM confidence ≥ 0.85: 100 alerts in 74 h (1.3 per hour
   instead of 20), 55% hit, +0.55% next day. Everything else becomes a low-priority "mentioned" line.
4. **Do not show tariff or deal mentions as bullish.** For those action labels the stance is a poor
   guide to price direction; label the alert factually and skip the stance arrow.
5. **Novelty needs a different mechanism.** The Sonnet judge's "new information" flag did not
   replicate (34% hit on the expansion group). 80% of alerts restate known policy, so the practical
   novelty filter is memory: suppress an entity that was already alerted in the last N days unless
   the action label changed. That is cheap and deterministic.
6. **Position the product as information, not as a trade signal.** The ten-minute reaction is
   directionally right 65–70% of the time but averages 0.0%, and the one-week P&L of buying everything
   positive equals the market. The honest pitch is "know within seconds what was said about the names
   you hold", with the small, action-bound company tier as the only thing that resembles a signal.

## 4. Which mentions actually move a stock (added 2026-09-16, details in `data/results/influence.md`)

Measured by the first reaction (opening gap or first hour) scaled by each ticker's own volatility:
only 32 of 714 mentions (4.5%) moved their stock beyond 2σ, 14 in the direction the stance implied,
and 29 of the 32 were opening gaps after after-hours events. In-hours mentions do not move stocks
within the hour (+10 min −0.01%, +1 h 0.00%). The genuine movers (Stargate: ORCL +10.5%, SFTBY
+11.3%; Apple event: TSM +5.1%, MU +4.4%, MP +4.6%; steel tariff: NUE/STLD +12%) share four traits:
the company is a party to the announcement (executives present), the commitment is new and
specific, the event is after the close, and the stock is a mid-cap/ADR/supplier rather than the
mega-cap host. Positive mentions during the session are followed by a *negative* next day (35% up)
while after-hours positive mentions are 58% up; the slice "positive + company + investment/deal +
market closed" (65 trades) averages +0.6% per trade with 58% wins. Restated figures, praise, name
lists, sector and country ETFs do nothing.

## 5. Caveats

- 78 videos and 979 measurable signals, but heavily clustered: single days (Liberation Day, the steel
  tariff rally, Stargate) dominate any portfolio calculation. Per-trade statistics are the fairer view.
- Abnormal returns subtract SPY only; sector moves are not removed.
- Judge look-ahead is possible for 2025 events, but the judge did not help even where it could not
  have known the outcome, so the conclusion does not depend on it.
- Prices are Yahoo: minute bars only for the last ~30 days, hourly for two years; five tickers had
  no data (US Steel delisted, ARCH, BRFS, HYMTF, RSX).
- No trading costs. At 0.2% average trade return, any spread or slippage removes the whole thing.

## 6. How to extend

- `videos.yaml`: add livestreams (White House `/streams` has ~190 candidates from the last year;
  `uv run backtest discover` lists them). `run-all` is idempotent.
- To test a candidate feed rule, add a row to `filters()` in `backtest/analyze.py` and re-run
  `uv run backtest analyze`; the ladder reports volume kept and returns per horizon.
- To test a trading rule, add a `select` case in `backtest/portfolio.py`.
