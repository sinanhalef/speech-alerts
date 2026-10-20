# Which mentions actually moved their stock? (hand analysis, 2026-09-16)

Data: 78 videos, 979 confirmed signals with a measurable primary ticker (first mention per video).
Influence is measured by the **first reaction**: the opening gap when the market was closed at the
mention, or the first hour when it was open, always relative to SPY and divided by the ticker's own
daily abnormal volatility over the prior 60 sessions (a z-score), so a 5% move in a coal miner is
not counted like a 5% move in Apple. Table: `influence_table.csv` (regenerate with
`uv run python -m backtest.influence`).

## 1. How rare a real reaction is

| | count | share |
|---|---:|---:|
| mentions with a measurable first reaction | 714 | |
| first reaction beyond 2σ ("mover") | 32 | 4.5% |
| … in the direction the stance implied | 14 | 2.0% |
| … while the market was open (+1h) | 3 | |
| … after hours (opening gap) | 29 | |

While the market is open, mentions do not move stocks within the hour: the average +10 min move
is −0.01%, the average +1 h move is 0.00%, and only 3% of in-hours mentions see a 1% move in the
first hour, against 33% of after-hours mentions gapping more than 1% at the open. The three
in-hours "movers" are noise (pharma on the drug-pricing morning, "the McDonald's shot").

Next-day moves are a poor guide to influence: the largest were UnitedHealth −19% (its own
guidance withdrawal on 2025-05-13), Microsoft −9.5% (earnings day) and gas, coal, rare-earth and
crypto ETFs that swing 5–10% on any day. Ranking by raw next-day move mostly ranks volatility.

## 2. Where the 32 movers came from

| event | signals | movers | what happened |
|---|---:|---:|---|
| Liberation Day, 2025-04-02 (16:00 ET) | 30 | 14 | macro shock: country and sector ETFs gapped 3–7% vs SPY (mostly *up* relative to SPY because the US fell more). The individual mention is irrelevant; the event is the signal |
| Stargate, 2025-01-21 (16:48 ET) | 11 | 2 | ORCL +10.5%, SFTBY +11.3% at the open: both companies were parties to a $500B deal announced on stage with their CEOs present |
| Apple $600B event, 2025-08-06 (17:04 ET) | 26 | 3 | TSM +5.1%, MU +4.4% (named with a new $200B figure), MP +4.6% (new Apple rare-earth line); AAPL itself +2.1%; suppliers named in passing (AVGO, Corning, IBM, JNJ, MRK) ~0 |
| Energy remarks, 2026-02-27 (16:37 ET) | 13 | 3 | XLE +4.4%, VLO +6.1%: an oil-market day; the remarks were retrospective criticism of Biden |
| Drug-pricing EO, 2025-05-12 (10:00 ET) | 16 | 2 | pharma bounced +1.7% in the first hour after the order turned out milder than feared |
| everything else (73 videos) | 618 | 8 | scattered, mostly against the stance |

## 3. Common ground of the mentions that moved a stock

The genuine cases (Stargate, Apple event partners, the 50% steel tariff → NUE/STLD +12%, Tesla
+6.7%, Intel "I made an investment" +4.4% gap / +15.8% day) share four traits:

1. **The company is a party to the announcement, not a name in a list.** Its executives are in
   the room or it is the co-announcer. Across all positive mentions, "executives present" is the
   single strongest feature: 12 cases, mean first reaction +2.2%, 25% beyond +1σ, none below −1σ,
   next day +2.3%. "Great company" praise, "X was there", "Merck, Pfizer, they're coming" do nothing.
2. **A new, specific commitment.** A dollar figure or stake the market did not already have (Stargate
   $500B, Micron $200B, the Intel stake, tariff 25% → 50%). Restated figures are inert: the APEC
   luncheon read the whole list (Apple $600B, Micron $200B, Oracle $500B, Google $25B, Pfizer $70B)
   and every gap was within ±0.4% except Micron +3.0%. Money in the quote alone is therefore not
   predictive (44 positive mentions with a dollar amount: +0.23%, 43% up next day).
3. **It happens after the close.** Announcement events are scheduled late afternoon; the reaction
   is an opening gap. Positive mentions when the market was closed: first reaction +0.54%, next day
   +0.63%, 58% up. Positive mentions during the session: −0.01%, next day −0.28%, **35% up**. That
   split holds in two of the three video groups (expansion: 32% vs 48% up; 2025 headline: 29% vs
   57%); only the small "recent" group breaks it.
4. **The stock is a mid-cap, an ADR or a supplier, not the mega-cap host.** By ticker volatility:
   names with 1.5–2.5% daily vol carry the effect (+0.52% first reaction, +0.45% next day); mega-caps
   under 1% vol barely move even when they are the subject (Apple +2.1% at its own event, Google,
   Microsoft ~0); names above 2.5% vol (coal, gas, rare earths, crypto) move a lot but never beyond
   their own noise (0% of them beyond 2σ).

Levels, when the conditions are met: party to a new deal +5% to +11% at the open (ORCL, SFTBY),
supplier named with a new number +3% to +5% (MU, TSM, MP), mega-cap host +2%, symbolic gesture
(Tesla purchase) +3% to +7% over a day. Everything outside those conditions sits inside ±1% noise.

## 4. Which positive mentions to act on, and which not

| rule (positive stance) | n | first reaction | next day | up next day | 1 week |
|---|---:|---:|---:|---:|---:|
| all positive mentions | 396 | +0.28% | +0.20% | 47% | −0.15% |
| market open at the mention | 186 | −0.01% | −0.28% | 35% | −1.04% |
| market closed at the mention | 210 | +0.54% | +0.63% | 58% | +0.66% |
| company + investment/deal + market closed | 54 | +0.77% | +0.71% | 56% | +1.07% |
| company + executives present | 3 | +7.4% | +5.4% | 100% | −5.5% |
| sector ETFs | 170 | +0.22% | +0.14% | 44% | −0.75% |
| country ETFs | 57 | +0.06% | −0.06% | 49% | +0.24% |

$10k simulation of the rules (buy, sell after 5 sessions):

| selection | trades | mean trade | win rate | equal-split profit on $10k |
|---|---:|---:|---:|---:|
| every positive mention | 609 | +0.2% | 52–55% | $22–34 |
| positive + company + investment/deal | 115 | +0.2% | 53–55% | $19–20 |
| positive + company + investment/deal + market closed | 65 | +0.6% | 58% | $56 |

Takeaways for the feed:

- **Do not act on in-hours positive mentions.** They have no first-hour effect and a negative next
  day. If a mention lands during the session, the market has either priced it or does not care.
- **Act (or at least rank first) on after-hours company mentions tied to an investment or deal**,
  ideally with the company's executives present. That is ~65 of 609 positive mentions (11%) and
  the only slice with a consistent positive drift, still small (+0.6%, t ≈ 0.6) and concentrated in
  a handful of announcement events.
- **Treat announcement events as the unit, not mentions.** Stargate, the Apple event and the steel
  rally each produced several correlated moves; the useful alert is "X is co-announcing a new $N
  commitment at a White House event", raised once, with the parties listed.
- **Drop sector and country ETF tickers from actionable alerts.** They only move on macro shocks
  (tariff days), where the individual mention adds nothing.
- **Ignore restated figures.** A number that has been read out before is already in the price;
  a memory of prior mentions per entity and amount is the cheapest novelty test.

## 5. Caveats

- 14 direction-consistent movers in 714 mentions is a small base; the "executives present" and
  "party to the deal" rules are drawn from about ten events and need forward validation.
- The regex for "executives present" is crude (it also fires on "farmers here today").
- Intel's +15.8% (2026-05-04) and Walmart's +8.2% (2025-11-19) could not be checked for
  unrelated same-day news without external sources.
- Yahoo intraday history limits the +10 min measurement to the last 30 days.
