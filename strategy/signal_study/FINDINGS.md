# Which the President statements move stocks, and how to classify them live

_Written 2026-09-22 from the 78-video corpus (74.5 h of speech, Jan 2025 – Sep 2026; 1,534 confirmed mentions,
3,934 mention × ticker pairs with prices). Numbers come from `signal_study/out/*.md`; rerun the scripts in
`README.md` to refresh them. Companion: `SYSTEM_PROMPT.md`._

## 1. The short answer

1. **A speech almost never moves the whole market.** SPY moved more than 2σ on 1 of 78 videos, and that one
   (2026-07-29, 15:02) is an FOMC decision day. The only market-wide event in the corpus is Liberation Day
   (SPY −3.4% at the next open, −4.8% close to close, −6% the day after), and the reaction came after the
   close, once the tariff schedule was read out. Market-wide
   The President moves in this period came from written statements (Truth Social posts, executive orders, letters), not
   from speeches.
2. **A speech very rarely moves a stock, and only after hours.** Of 3,755 mention × ticker pairs, 116 (3%) moved
   more than 2σ at the first reaction. All but 3 of those were opening gaps after after-hours remarks. While the
   market is open, mentions are inert: at +10 min, 0.3% of pairs moved more than 2σ (a random 10-minute window
   would give 4.6%), and the direction of the 10-minute move matches the label 47–51% of the time. **No
   in-session remark in 52 in-session videos produced a measurable directional move within the hour.**
3. **Most "movers" are coincidences.** Of the 58 unique (video, ticker) after-hours movers, about 40 are
   earnings days (Microsoft, Tesla, Alphabet, Intel, Mosaic, Cigna, UnitedHealth, Walmart), oil-market days
   (2026-02-27, 2026-04-16), a rotation day (2026-06-03), or Liberation Day defensives that simply fell less than
   SPY. The attributable movers come from **seven events**: Stargate (2025-01-21), the Tesla purchase
   (2025-03-11), Liberation Day (2025-04-02), the drug-pricing order (2025-05-12), the steel tariff doubling
   (2025-05-30), the Apple event with the chip-tariff exemption (2025-08-06), the Pfizer pricing deal
   (2025-09-30), plus the Venezuela/Chevron weekend (2026-01-03).
4. **The attributable movers share one sentence shape:** a *new number or decision* ("bring it from 25% to 50%",
   "effective at midnight, 25% on all foreign made automobiles", "announcing the formation of Stargate… will
   invest $500,000,000,000", "a tariff of approximately 100% on chips… if you're building in the United States
   there will be no charge"), spoken about a *specific, listed beneficiary or target* (the domestic producers, the
   named partners, the exempted suppliers, the country with the new rate), *after the close*, in an event whose
   purpose is that announcement, often with the company's executives on stage. Restated numbers, lists of pledges,
   praise, criticism, past-tense comparisons and hedged intentions never moved anything.
5. **Direction: "up" calls work, "down" calls do not.** After hours (ex Liberation Day), when the judge expected
   the stock to rise on new information it rose ≥1σ 48% of the time and fell ≥1σ 1% of the time. When it expected
   a fall, the stock rose ≥1σ 10% of the time and fell ≥1σ 2%. Negative statements about pharma, insurers,
   chips, the Fed, media and countries were followed by ≥1σ *rises* 31 times and falls 20 times. Threats are
   priced or ignored; the concrete action that ends a threat (the Pfizer deal, the milder-than-feared drug order)
   produces a relief rally. The only statements that reliably move a stock *down* are new numeric actions
   against a specific foreign target (Vietnam 46% → VNM −6.6%).
6. **A strict rule reproduces this with high precision and low recall.** "Market closed, new decision or number,
   direct beneficiary, announcement language, no hedge, no past tense, expected up" flagged 9 unique cases in
   74 hours: 7 moved ≥1σ the right way (78%), 0 moved the wrong way, 6 moved ≥2σ. Every hit is from Stargate, the
   steel rally or the Apple event; the 2026 videos contain no statement of that shape. The looser "watch" tier
   (closed, new or subject of the event, not macro) is 13% right / 6% wrong — barely better than everything after
   hours (12% / 7%).

The practical consequence: the classifier's job is to say **"no"** to ~97% of mentions with confidence, and to
recognise the rare announcement sentence when it comes. Its output should be graded (signal / weak / none), it
should never label a negative remark as a short unless a new number or ban is attached, and it should treat
in-session remarks as information, not as trades.

## 2. Data and method

- Transcripts, labels and prices from the `strategy/` backtest (`data/transcripts`, `data/signals`,
  `data/results/measurements.csv`, `data/prices`). 78 videos: 8 headline events of 2025 (CNBC/White House),
  11 recent White House livestreams (Aug–Sep 2026, 1-minute bars), 59 White House livestreams Jun 2025 – Sep 2026.
- Unit: a confirmed dictionary mention × each ticker attached to it (Haiku tickers, dictionary tickers, judge
  additions). 3,934 pairs, 3,755 with a measurable first reaction.
- **First reaction** = opening gap of the next session (market closed at the remark) or last completed bar → +1 h
  (market open). **z** = abnormal return (ticker − SPY) / the ticker's own 60-session daily abnormal-return
  standard deviation, so moves are comparable across a coal miner and Apple. For in-session 10/30/60-minute
  windows the vol is scaled by √(minutes/390).
- **Expected direction** = Sonnet judge direction per ticker, stance (positive → up, negative → down) as fallback.
  right = z·sign ≥ +1; wrong = z·sign ≤ −1.
- Event level = unique (video, ticker), keeping the mention with the highest judge confidence.
- Pre-move = the ticker's abnormal return on the session before an after-hours remark (was the news already out?).
- Scripts: `01_events.py` … `06_rules.py`; outputs in `out/`.

## 3. Base rates

| level | measure | value |
|---|---|---|
| video (78) | SPY first reaction beyond 1σ / 2σ | 4 / 1 (the 2σ one is FOMC day 2026-07-29) |
| video | SPY move to the close beyond 2σ | 2 (incl. Liberation Day, whose announcement was after the close) |
| video | at least one sector ETF beyond 2σ at the first reaction | 15 (mostly earnings/macro days; steel, Venezuela, Pfizer, oil days) |
| pair (3,755) | first reaction beyond 2σ | 3.1% (116 pairs, 73 signals, 20 videos) |
| pair, market closed (1,427) | beyond 1σ / 2σ | 20% / 8% |
| pair, market open (2,328) | beyond 1σ / 2σ within the hour | 1% / 0% |
| pair, market open, +10 min (590, 1-minute bars) | beyond 2σ of a 10-minute window | 0.3% (random: 4.6%) |
| pair, judge up, closed, ex Liberation Day (460) | right ≥1σ / wrong ≥1σ | 19% / 2% |
| pair, judge down, closed, ex Liberation Day (204) | right ≥1σ / wrong ≥1σ | 2% / 10% |
| pair, judge up + novelty new, closed (71) | right ≥1σ / ≥2σ / wrong | 48% / 24% / 1% |
| event, judge up + new, closed (46 unique) | right ≥1σ / ≥2σ / wrong | 46% / 17% / 7% |
| event, strict rule (tier A′, 9 unique) | right ≥1σ / ≥2σ / wrong | 78% / 67% / 0% |

By entity kind (first reaction, all pairs): company 8% beyond 2σ and +0.41 mean adjusted z; sector 2% / +0.05;
country 3% / −0.05; asset ("stock market", "the Fed", bitcoin) 1% / 0.00.

By action label (judge direction, after hours, ex Liberation Day): investment 30% right / 1% wrong (n=143);
regulation 54% / 0% (n=28, almost all the steel event); tariff (up) 16% / 0% (n=31); praise 12% / 2% (n=66);
deal 5% / 7% (n=86: country deals restated); military 0% / 0%; every "down" action label ≤ 8% right.

## 4. The movers, case by case

Unique (video, ticker) after-hours movers with |z| ≥ 2 at the open, plus the in-session cases above 1σ.
"pre-move" = the ticker's abnormal return during the session before the remark.

### 4a. Attributable to what was said

| when (ET) | ticker | first reaction | pre-move | what was said | why it moved |
|---|---|---|---|---|---|
| 2025-01-21 16:49 | ORCL +10.5% (5.7σ), SFTBY +11.3% (7.1σ), NVDA +2.2% (1.1σ), VRT +4.4% (1.3σ), MSFT +1.6% | ORCL +6.3%, SFTBY +3.2% | "Together, these world leading technology giants are announcing the formation of Stargate… A new American company that will invest $500,000,000,000 at least… creating over 100,000 American jobs almost immediately." CEOs of Oracle, SoftBank, OpenAI on stage. | New venture, new number, named parties present. Oracle gets the compute contracts, SoftBank finances it. Reported that afternoon, yet the on-stage confirmation added +10%. |
| 2025-03-11 16:02 | TSLA +6.1% (1.6σ) | +4.6% | The President buys a Tesla on the South Lawn: "You ever sat in one of these?… I'll do that [label dealership attackers domestic terrorists]… they're harming a great American company." | Symbolic demand + protection for a brand under boycott (announced on Truth Social the night before; a soft CPI print the next morning helped). |
| 2025-04-02 16:13–16:31 | VNM −6.6% (−6.4σ); EWW +5.8%, EWC +1.6%, EWL +4.1%, EWZ +4.2%, VGK +3.1%, INDA +2.4% (all *relative* to SPY's −3.4% opening gap; SPY closed −4.8%) | ~0 | "effective at midnight, we will impose a 25% tariff on all foreign made automobiles"; the per-country chart: "Cambodia, 97%. We're gonna bring it down to 49… Brazil, 10%, 10%… Switzerland, 61% to 31%." | Market-wide: the average rate was far above expectations → SPY −4.8%, −6% next day. Per country: direction set by the *number* versus expectation and by exemptions (Canada/Mexico under USMCA rose relative), not by the rhetoric ("Canada imposes 250 to 300% on dairy" was labelled negative; EWC outperformed). |
| 2025-05-12 09:53–10:17 (in session) | MRK +5.0% (2.2σ), PFE +3.4% (1.8σ), XLV +1.7% in the first hour | MRK day +2.6% | Drug-pricing order signed live: "cut drug prices by 80 or 90%… tariffs that may be imposed on pharmaceuticals" | The order was milder than the "most favored nation" fear posted the night before, with no enforcement mechanism → relief rally; faded to 0 by day 1, −4% by day 2. |
| 2025-05-30 18:03 | NUE +12.7% (7.8σ), STLD +10.5% (7.1σ), CLF +23.6% (5.6σ), SLX +3.7% (3.8σ) | NUE +0.5%, CLF −1.1% | "And today, I have a major announcement… We are going to be imposing a 25% increase. We're going to bring it from 25% to 50%, the tariffs on steel into The United States of America… I was thinking about 40… They said, we'll take 50." | New number, explicit old→new, specific product, effective policy. Beneficiaries = the protected domestic producers, who are mid-caps. No pre-move: genuinely new. |
| 2025-08-06 17:12–17:20 | TSM +5.1% (3.5σ), MU +4.4% (2.0σ), MP +4.6% (0.5σ, volatile), SMH +1.6% (1.5σ), AAPL +2.1% (1.9σ) | AAPL +4.3% (the $100B top-up was reported that morning); MU −1.0%, TSM −1.2% | "we'll be putting a tariff on of approximately 100 percent on chips and semiconductors. But if you're building in The United States… there will be no charge… I didn't even tell you that inside." Plus the supplier program: "Apple will help develop and manufacture semiconductors… TSMC… Micron, great company, is investing 200,000,000,000… committed to buying American made advanced magnets developed by MP Materials." | New policy with a number *and an exemption mechanism* that names its beneficiaries: chipmakers with US fabs and the suppliers in Apple's program. The host (Apple, already reported) moved +2%; the suppliers +4–5%. IBM, J&J, Corning, Broadcom, named in the same list without a new fact: ~0. |
| 2025-09-30 16:14 | PFE +2.4% (1.3σ), then +5.8% day 1; XLV +2.3% into the close | PFE +6.5% during the session | "Alfred Bourla, and his company, Pfizer, agreed… most favored nation drug pricing" | The threatened action arrived as a negotiated deal → certainty; the judge called it "down" and was wrong. |
| 2026-01-03 12:26 (Saturday) | CVX +5.8% (4.6σ), XLE +2.8% (2.4σ), XOM +1.6% | CVX +2.1% on Friday | After the Maduro operation: "We'll have the greatest oil companies in the world going and invest billions and billions of dollars and take out money, use that money in Venezuela… the embargo on all Venezuelan oil remains in full effect." | Geopolitical action with one obvious listed beneficiary: the only US major with Venezuelan assets. The event was the operation; the speech added "who runs the oil". |
| 2026-08-19 14:54 (in session) | CLF −4.4% (−1.0σ) within the hour | – | On Canada: "Are you willing to lower tariffs on steel and aluminum? Well, we're looking at that… we may bring some of the tariffs down" | The one in-session directional case: a hint of *removing* protection is negative for the protected producer. Hedged, small, and CLF is volatile; treat as weak. |

### 4b. Not attributable (same-day company news or macro)

MSFT +7.4% 2025-07-31 (earnings), TSLA −6.8% and GOOGL +3.5% 2025-07-24 (earnings), STLA −5.7% 2025-07-24
(results), INTC −12.3% 2025-07-25 (earnings), MOS −10.6% 2025-08-06 (earnings), CI −2.4% / UNH −2.5% 2025-07-31
(earnings), UNH −19% 2025-05-13 (own guidance withdrawal), WMT +8.2% 2025-11-20 (earnings), INTC +15.8%
2026-05-05 (the remark was "I made an investment. Intel… then it got taken away", i.e. retrospective), the whole
oil complex on 2026-02-27 (USO +8%, XLE +4.4%, VLO/PSX/XOM/LNG +4–6%: the remarks were Biden-era criticism; an
oil-market weekend), USO −9.5% / XLE −4.5% on 2026-04-17 (Iran war news; the speech contained one forward hint,
"everybody said [oil] was going to $250… I think you're gonna be pleasantly surprised"), DIA/QQQ/XLF/JPM/KRE on
2026-06-04 (value/tech rotation; the remark was "we had the strongest stock market in history"), KWEB −5.7%
2025-12-22 (restated furniture tariff), EWJ −1.6% 2025-11-18 (restated Japan deal; Japanese market fell on
SoftBank), EWY +2.6% 2025-10-29 (the Korea trade deal concluded that day; "gleaming streets of Seoul"), PSKY,
ADM, CARZ, DBA/CORN/SOYB on Liberation Day (ag ETFs fell less than SPY).

Rule of thumb from this table: **if the mover is a mega-cap or a name reporting earnings that week, or the whole
sector moved together on a macro headline, the speech did not cause it.** The influence table in
`data/results/influence.md` reached the same conclusion from the primary-ticker view.

## 5. Anatomy of a moving statement

Common to the attributable cases (and absent from every dud):

1. **A decision, not a description.** "We are going to be imposing", "effective at midnight", "announcing the
   formation of", "agreed", "there will be no charge", "we'll be putting a tariff on of approximately 100 percent".
   Contrast the duds: "we're looking at that", "I'd like to see", "may be imposed", "they're coming back",
   "we're doing great on steel".
2. **A number or mechanism that is new.** 25→50%; $500B and a new company name; 100% with a build-in-the-US
   exemption; 46% for Vietnam; "the embargo remains in full effect". Restated numbers are inert even when large:
   the APEC luncheon read Apple $600B, Micron $200B, Oracle $500B, Google $25B, Pfizer $70B and every gap was
   inside ±0.4% except Micron +3%. Among positive company mentions after hours, a dollar figure in the quote
   *lowered* the hit rate (23% vs 32%) because dollar figures are mostly restated pledges.
3. **A specific listed beneficiary or target, who is the subject of the event.** The company's executives are on
   stage or it is named as a party ("We're joined by Oracle executive chairman Larry Ellison", "Tim, I'll tell
   you", "Alfred Bourla and his company, Pfizer"). Mentions repeated within the same 10 minutes (the entity is
   the subject, not a name in a list) moved ≥1σ 52% of the time vs 20% for single mentions; the "executives
   present" cue 71% vs 28%.
4. **Who gets the money matters more than who is praised.** Investment pledges are mildly positive for the
   pledger (Apple +2%) and strongly positive for the parties that *receive* contracts, protection or an exemption
   (Oracle, the steelmakers, TSMC/Micron). A company announcing its own capex abroad (Oracle $14B in Saudi
   Arabia, Toyota $10B, Blackstone $25B in Pennsylvania) does not move on it.
5. **After the close.** Announcement events are scheduled at 16:00–18:00 ET; the reaction is the next open.
   In-session remarks are either already known (Intel stake, Nvidia H20 share, Pfizer deal all reported hours
   earlier) or not decisions.
6. **Mid-cap, ADR or supplier, not the mega-cap host.** Names with 1.5–2.5% daily abnormal vol carry the effect;
   mega-caps move ~2% at most on their own event; ultra-volatile names (coal, uranium, crypto) move 3–5% on any
   day, so a 2.5% gap on the coal order (2026-02-11) was noise and reversed.
7. **The market often knows first.** Oracle (+6.3% that day), Pfizer (+6.5%), Tesla (+4.6%), Apple (+4.3%), Intel
   (+7.4% on the Bloomberg report a week earlier) had all moved before the remark. The on-stage confirmation with
   details still added 2–10% for Oracle/SoftBank/Pfizer/Tesla, nothing for Intel (whose confirmation came in
   session). The steel doubling and the chip exemption were unleaked and moved the most per σ.

## 6. What never moves (the duds)

From `out/contexts_duds.md` (58 cases the judge labelled *new* with an expected direction, where the first
reaction was < 0.5σ; read case by case in a separate pass), the sagas, and the judge-expected table. In the 58
"new" duds, 15 excerpts carried an explicit restatement cue in the same breath as the flagged sentence, 9 had
the actionable content spoken by a CEO, a secretary or a reporter rather than by the President, 41 fell during market
hours, 26 targeted mega-caps, and the judge's direction matched the sign of the (small) first move in 24 cases
against 28 wrong. Three talking points produced a third of them: Venezuela oil (9), data centres and
electricity (4), Iran and oil (5). Categories, most frequent first:

1. **Restated pledges and deals.** "Apple, $600,000,000,000 investment", "TSMC has pledged $100B", "We made a deal
   with Japan, $650B", "we approved the TikTok deal", "Nvidia has committed $500B over the next 4 years". The President
   repeats each figure in most speeches; the market moved on the first report, weeks earlier. The sagas show
   pharma "drug prices down 500 / 1000 / 1500%" 20+ times with no reaction; "50% tariffs on steel" 20+ times, one
   reaction (the day it changed).
2. **Company pledging its own spending.** Oracle $14B cloud in Saudi Arabia (−0.2σ), Toyota "I was with Mr Toyota"
   $10B (−1.8σ), Blackstone $25B Pennsylvania (0), "Eli Lilly is building 6 new plants" (−0.4σ). Capex is not
   revenue.
3. **Praise, name lists and thank-yous.** "great company", "Go out and buy a Dell computer" (5 times, never moved),
   "Merck, Pfizer, they're coming here", "beautiful B-2 bombers", "I wanna thank Eli Lilly and Pfizer, Merck",
   "representatives from Apple, Google, Samsung, Amazon, OpenAI". Zero effect unless the name is the subject of a
   new decision.
4. **Threats and criticism without a new number or date.** "we'll break them up. He has 100% market share"
   (Nvidia, +0.6σ), "a 100% tariff or a 200 or a 300 or a 500%" on chips (4 times, ~0), "Powell is terrible",
   "ABC is a terrible network" (DIS −1.6σ, the one small exception, during the FCC/Kimmel affair), "fat cats"
   insurers (UNH −1.2σ). Negative rhetoric about pharma/insurers/chips/countries was followed by ≥1σ rises more
   often than falls.
5. **Past tense and Biden comparisons.** "waged a radical left war on American oil", "piled crippling regulations
   on refiners", "decimated by China", "we saved a little company called U.S. Steel". Even when the sector moved
   that day (2026-02-27), the remark was not the cause.
6. **Hedged intentions and answers to reporters.** "we're looking at that", "I'd like to see federal lands opened",
   "we may bring some of the tariffs down", "could have. Depends on how we do", "I'll let you know about it".
   No commitment, no date, no number.
7. **Country deals and country ETFs.** Japan/EU/Korea "$550B / $950B / $350B" restatements: 5% of Canada/Mexico
   mentions and 15% of EU mentions reached 1σ, with hit rates of 39–45% (i.e. the wrong way as often as not).
   Country ETFs move on the *rate* (Liberation Day) or on a *deal signed that day* (Korea, 2025-10-29), never on
   the rhetoric.
8. **Macro words.** "Stock market" (60 mentions, 45 videos, 10% ≥1σ, all noise), "the Fed" (42 mentions, 14% ≥1σ,
   noise), "AI" as a sector (36 mentions, no ≥2σ), bitcoin/crypto (35 mentions, 3% ≥1σ).
9. **Second-order tickers.** A sector ETF for a single-company story (XPH for the Pfizer deal, SMH for a Micron
   line), or a mega-cap (Microsoft for OpenAI, Nvidia for "AI"). The effect, if any, is inside noise.
10. **In-session confirmations of morning news.** Intel stake (2025-08-22, +0.1σ), Nvidia H20 15% share
    (2025-08-11, +0.1σ), the Stellantis $13B plan (2025-12-03, 0.0σ): reported before the remark.
11. **Someone else is speaking.** "we're very excited to announce… a further $25,000,000,000 investment"
    (Blackstone's president, 2025-07-15), "as an update, Medicare 2 months ago offered at $50 a month" (a guest,
    2026-08-31), "the president lifted sanctions on Iranian oil today, sir" (a reporter; The President: "I'm gonna have to
    find out exactly the status"). Diarization sometimes puts a reporter's words inside the President's block; "Mister
    president" / "sir" inside a [T] span marks a question.
12. **Reporter-prompted banter and instantly hedged threats.** "we're gonna put a major tariff on Mexico because
    of the lettuce, and… on Canada because of the smoke. Alright?… I haven't thought about it. It's the 1st time
    I've been asked that question" (2026-07-24); "every bridge in Iran will be decimated by 12:00 tomorrow night…
    We don't want that to happen. We may even get involved with helping them rebuild" (2026-04-06).

**Linguistic markers counted across the 58 dud excerpts:** restatement cues "announced" 20, "as you know" 12,
"yesterday" 12, "last night" 6, "just announced" 6, "just signed" 3, "you probably saw" 2, "as an update" 2;
hedges "I think" 71, "maybe" 27, "probably" 15, "I guess" 11, "we'll see" 8, "I don't know" 6, "let's see what
happens" 3; asides "by the way" 15 (both B-2 "orders" were asides); rally filler "greatest" 14, "historic" 10,
"nobody's ever seen" 7. Vague future "gonna be" 66 / "we're gonna" 61 without a number, date or counterparty.
Note that the hedge idiom "we're looking at" did not appear in the duds at all; the tell is the *missing* number,
date and counterparty, not a particular phrase.

**Specific and new, yet flat (the hard cases):** the 32% Taiwan rate on Liberation Day (EWT −0.1%: the index
carried the whole move, country ETFs added no alpha); the $700M coal package "protecting 14 coal plants and 42
mines" (2026-06-04, BTU/AMR flat then −5–8%: ~$12M per asset, defensive, ultra-volatile names); the formal
termination of CAFE standards (2025-12-03, F/GM flat: scheduled, CEOs in the room, relief years out), while at
the same event Stellantis' own "$13B, 5,000 jobs" figure moved STLA +3.3% next day; "we ordered 25 more" B-2s
(NOC flat: a second-airing aside with no contract). Quantified is not the same as material.

## 7. Direction rules the data supports

| statement type | instrument | observed direction | evidence |
|---|---|---|---|
| new tariff level on a product (steel 25→50%) | protected domestic producers | up, large (+10–25% small/mid caps, +4% ETF) | 2025-05-30; every restatement afterwards: 0 |
| hint of lowering a protective tariff | protected domestic producers | down, small | CLF −4.4% in the hour, 2026-08-19 (hedged) |
| new tariff with a build-in-the-US exemption | exempted producers / suppliers | up (+4–5%); host +2% | 2025-08-06 |
| sweeping tariff schedule above expectations | whole market | down (SPY −4.8%, −6% next day); rate vs expectation sets each country's relative move; exemptions rise | 2025-04-02 |
| new tariff rate on one country, above expectation | that country's ETF | down (VNM −6.6%) | 2025-04-02; the only reliable "down" |
| new venture / contract with named listed parties on stage | the parties that receive the business | up, large (+10%) | Stargate |
| company's own capex pledge (new or restated) | the pledger | ~0 | Oracle/Saudi, Toyota, Blackstone, Lilly, IBM, J&J |
| government purchase / stake / endorsement of a company | the company | up (+3–7%), mostly already leaked | Tesla; Intel (moved on the report, not the remark) |
| concrete deal that ends a threat (Pfizer MFN) or milder-than-feared order | threatened sector | up (relief, +2–5%), fades in days | 2025-05-12, 2025-09-30; judge said "down" both times |
| repeated threat to a sector (drug prices, chip tariffs, break-ups) | sector | none | 20+ pharma, 10+ chip cases |
| criticism of a media company with a regulatory lever | that company | down, small (−1.5%) | DIS 2025-09-19 |
| criticism of the Fed, banks, countries, "stock market" talk | anything | none | 40+ cases |
| geopolitical action with one obvious corporate beneficiary | that company | up, large (+6%) | CVX 2026-01-03 |
| war/peace hints | oil, defense | oil down on peace hints (weak, confounded) | 2026-04-16, 2026-06-17 |

## 8. Repeated themes ("sagas")

`out/sagas.md` lists every mention per theme in time order. What the n-th repetition does:

- **Pharma / MFN (83 mentions, 30 videos):** 13% of first reactions ≥1σ; every one is Liberation Day defensives,
  the 2025-05-12 relief rally or the Pfizer deal. Directional hit 46%. The judge said "down" on ~60 of them.
- **Semiconductors (156 mentions, 47 videos):** 19% ≥1σ but 2% ≥2σ; the only ≥2σ cases are the Apple-event
  exemption (TSM/MU) and APEC night (NVDA, confounded by GTC). Chip-tariff threats (100–300%) four times: nothing.
- **Steel (71 mentions, 35 videos):** one event moved (the doubling). "50% tariffs on steel" restated 20+ times: 0.
- **China (61 mentions, 42 videos):** 7% ≥1σ, none attributable; "deal with China" / "China is ripping us off"
  both inert.
- **Oil/gas (259 mentions, 63 videos):** 10% ≥1σ, all on oil-market days or the Venezuela event; "drill baby
  drill" and gasoline-price boasts: 0.
- **Coal (31), defense (165), crypto (35), automakers (107):** 0–3% ≥1σ. Defense praise ("B-2 bombers", "Patriot")
  never moved LMT/NOC/RTX; "some of the car companies… are making a deal to build missiles" moved RTX +1.2σ once.

## 9. Rule backtest (`out/rules.md`)

| tier (all after hours unless noted) | pairs | events | right ≥1σ | wrong ≥1σ | ≥2σ | mean adj z |
|---|---:|---:|---:|---:|---:|---:|
| A′ new + judge up + direct beneficiary + hard action + announce/number − past − hedge | 13 | 9 | 85% | 0% | 77% | +4.9 |
| A same incl. "down" calls | 14 | 10 | 79% | 7% | 71% | +4.4 |
| B watch: directional, not macro, new or subject of event, − past − hedge | 488 | 360 | 13% | 6% | 8% | +0.35 |
| C every other directional after-hours pair | 1,321 | 889 | 12% | 7% | 8% | +0.19 |
| D in session, directional | 2,092 | 1,344 | 0% | 1% | 0% | −0.01 |
| baseline judge up | 477 | 328 | 19% | 3% | 9% | +0.54 |
| baseline judge down | 245 | 201 | 4% | 16% | 7% | −0.45 |

Tier A′ hits: SFTBY, ORCL, NVDA (Stargate); NUE, CLF, STLD, SLX (steel); it also flagged MP (+0.5σ, volatile) and
Intel "we started with Intel" (−1.0σ, a name-drop the judge over-read). Tier A adds the Pfizer "down" call
(wrong, relief). By video group tier B is 43% / 11% on the 2025 headline events and 3% / 4% on the 2026
livestreams: outside scheduled announcement events, novelty labels do not find anything. Movers the rules
missed are duplicates of the same events under other mentions, Liberation Day (VNM: the judge labelled the
criticism "repeat" although the *rate* was new), CVX/Venezuela (kind = country excluded it; the rule should ask
"is there one listed beneficiary", not "is the entity a company"), and confounds.

## 10. What the live classifier should do

1. **Gate on the speaker, then on novelty, then on the beneficiary, then on commitment, then on timing.** A
   mention has to pass all five to be a signal; the base rate after the first gate is ~3%.
2. **Ask "what is the new fact?" and make the model write it down.** If the only content is a name, a repeated
   number, praise, a past-tense comparison or a hedge, it is not a signal. Give the model a memory of numbers
   and entities already announced (the last 30 days of alerts) so restatements are recognised deterministically.
3. **Ask "who receives the money, the protection or the exemption?"** and attach the signal to that instrument,
   not to the sector ETF or the mega-cap host. Allow a country/geopolitical event to map to a single company.
4. **Never emit a bearish signal on rhetoric.** Bearish only for a new numeric action on a specific target, a
   hint of removing protection from a protected producer, or a media company facing a concrete regulatory
   lever. Expect relief rallies when a threatened sector gets a concrete, milder deal.
5. **Grade, don't binarise.** signal (expect ≥2σ at the next open), weak (a lean, ≤1σ, information only), none.
   In-session statements are at most "weak" unless they are a scheduled announcement with a number.
6. **Calibrate.** After hours, "new + up + direct beneficiary + announcement sentence" was right ~80% of the
   time and wrong 0%; "new + up" alone 46% right, 7% wrong; anything else ≤13% right. Confidence above 0.6 should
   be rare (a few times per year).
7. **Treat the event as the unit.** One announcement produces several correlated movers (Stargate → ORCL, SFTBY,
   NVDA, VRT); emit one signal listing the parties rather than one per name.

## 11. Caveats

- Seven attributable events drive every positive statistic. The strict rule's 78% is 7 of 9 unique cases; it
  needs forward validation, and the 2026 videos suggest such events come a few times per year, not per month.
- Abnormal returns subtract SPY only; sector co-movement is not removed, which is why oil-market days and the
  2026-06-04 rotation appear as movers. Earnings confounds were identified by hand from the dates.
- Judge labels (novelty, direction) were produced with possible look-ahead for 2025 events; the rule backtest
  therefore overstates what a live model would see. The steel and Stargate sentences are, however, unambiguous
  on their face.
- Yahoo intraday history limits 1-minute measurements to the last 30 days; 5-minute to 60 days; hourly otherwise.
  The in-session "nothing moves" result rests on 590 pairs with 1-minute bars and 2,092 with hourly bars.
- No transaction costs; a +0.6% average drift on the "positive company after hours" slice would not survive them.
- Whole-market moves triggered by Truth Social posts, letters and executive-order text are not in this corpus.
  The classifier should be pointed at those sources too if market-wide signals matter.
