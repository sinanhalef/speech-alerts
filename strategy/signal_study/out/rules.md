# Rule backtest: do the proposed decision rules separate movers from non-movers?

Unit: confirmed (signal, ticker) pairs with a measurable first reaction. `right` = moved ≥ 1σ in the expected direction (judge direction, stance as fallback); `wrong` = moved ≥ 1σ the other way. Events = unique (video, ticker).

| tier | pairs | events | videos | right ≥1σ (pairs) | wrong ≥1σ (pairs) | |z|≥2 (pairs) | mean adj z | right ≥1σ (events) | wrong ≥1σ (events) | right events |
|---|---|---|---|---|---|---|---|---|---|---|
| A  actionable: closed & new & directional & direct instrument & hard action & (announce|number) & !past & !hedge | 14 | 10 | 4 | 79% | 7% | 71% | +4.43 | 70% | 10% | CLF, NUE, NVDA, ORCL, SFTBY, SLX, STLD |
| A' same but judge up only (no down calls) | 13 | 9 | 3 | 85% | 0% | 77% | +4.87 | 78% | 0% | CLF, NUE, NVDA, ORCL, SFTBY, SLX, STLD |
| B  watch: closed & directional & not macro & (new | subject of event) & !past & !hedge | 488 | 360 | 32 | 13% | 6% | 8% | +0.35 | 8% | 6% | AAPL, BX, CARZ, CLF, CVX, DBA, MSFT, NUE, NVDA, ORCL, REMX, SFTBY, SLX, SMH, SOX |
| C  closed & directional, everything else | 1321 | 889 | 35 | 12% | 7% | 8% | +0.19 | 9% | 8% | AAPL, BX, CARZ, CI, CLF, CORN, CVX, DBA, DIA, DIS, ELV, EQT, EWU, EWY, EZU, FEZ, |
| D  in session, directional (any) | 2092 | 1344 | 52 | 0% | 1% | 0% | -0.01 | 0% | 0% | CARZ, CLF |
| E  non-directional (judge none), closed | 106 | 92 | 23 | n/a | n/a | 7% | n/a | n/a | n/a |  |
| baseline: judge up, closed | 477 | 328 | 33 | 19% | 3% | 9% | +0.54 | 13% | 4% | AAPL, BX, CARZ, CLF, CORN, CVX, DBA, EQT, GOOGL, JNJ, KSA, LLY, LNG, MSFT, MU, N |
| baseline: judge down, closed | 245 | 201 | 29 | 4% | 16% | 7% | -0.45 | 4% | 15% | CARZ, DIS, ICLN, SMH, SOXX, UNH, VNM, XLE |
| baseline: stance positive, closed | 972 | 658 | 35 | 14% | 6% | 8% | +0.27 | 9% | 8% | AAPL, BX, CARZ, CI, CLF, CORN, CVX, DBA, DIA, ELV, EQT, EWU, EWY, GOOGL, HUM, IB |
| baseline: all closed | 1427 | 947 | 35 | 12% | 7% | 8% | +0.19 | 9% | 8% | AAPL, BX, CARZ, CI, CLF, CORN, CVX, DBA, DIA, DIS, ELV, EQT, EWU, EWY, EZU, FEZ, |
| baseline: all | 3755 | 2353 | 78 | 5% | 3% | 3% | +0.07 | 4% | 4% | AAPL, BX, CARZ, CI, CLF, CORN, CVX, DBA, DIA, DIS, ELV, EQT, EWU, EWY, EZU, FEZ, |

## By video group (tier A and B)

| tier | pairs | events | videos | right ≥1σ (pairs) | wrong ≥1σ (pairs) | |z|≥2 (pairs) | mean adj z | right ≥1σ (events) | wrong ≥1σ (events) | right events |
|---|---|---|---|---|---|---|---|---|---|---|
| A  / headline | 13 | 9 | 3 | 85% | 0% | 77% | +4.87 | 78% | 0% | CLF, NUE, NVDA, ORCL, SFTBY, SLX, STLD |
| A  / expansion | 1 | 1 | 1 | 0% | 100% | 0% | -1.28 | 0% | 100% |  |
| A' / headline | 13 | 9 | 3 | 85% | 0% | 77% | +4.87 | 78% | 0% | CLF, NUE, NVDA, ORCL, SFTBY, SLX, STLD |
| B  / headline | 124 | 70 | 5 | 43% | 11% | 30% | +1.34 | 27% | 11% | AAPL, CARZ, CLF, DBA, MSFT, NUE, NVDA, ORCL, REMX, SFTBY, SLX, SMH, SOXX, STLD,  |
| B  / expansion | 364 | 290 | 27 | 3% | 4% | 1% | +0.02 | 3% | 4% | BX, CVX, NVDA, UNH, WBD, XLE, XOM |

## Excluding Stargate, the steel rally and the Apple event

| tier | pairs | events | videos | right ≥1σ (pairs) | wrong ≥1σ (pairs) | |z|≥2 (pairs) | mean adj z | right ≥1σ (events) | wrong ≥1σ (events) | right events |
|---|---|---|---|---|---|---|---|---|---|---|
| A  actionable: closed & new & directional & direct instrument & hard action & (announce|number) & !past & !hedge | 1 | 1 | 1 | 0% | 100% | 0% | -1.28 | 0% | 100% |  |
| A' same but judge up only (no down calls) | 0 | 0 | 0 | n/a | n/a | nan% | n/a | n/a | n/a |  |
| B  watch: closed & directional & not macro & (new | subject of event) & !past & !hedge | 397 | 308 | 29 | 6% | 5% | 2% | +0.03 | 5% | 5% | BX, CARZ, CORN, CVX, DBA, NVDA, SMH, SOXX, TSLA, UNH, WBD, XLE, XOM |
| C  closed & directional, everything else | 1147 | 793 | 32 | 9% | 7% | 5% | +0.03 | 8% | 8% | BX, CARZ, CI, CORN, CVX, DBA, DIA, DIS, ELV, EQT, EWU, EWY, EZU, FEZ, FXI, GOOGL |

## Tier A cases (event level)

| when | video | ticker | entity | dir | action | z_first | adj | quote |
|---|---|---|---|---|---|---|---|---|
| 2025-01-21T16:48 | Stargate AI investment announcemen | SFTBY | SoftBank | up | investment | +7.1 | +7.1 | SoftBank CEO joined to announce largest AI infrastructure project in A |
| 2025-01-21T16:49 | Stargate AI investment announcemen | ORCL | OpenAI | up | investment | +5.7 | +5.7 | CEO of OpenAI |
| 2025-01-21T16:49 | Stargate AI investment announcemen | NVDA | Stargate AI project | up | deal | +1.1 | +1.1 | world leading technology giants are announcing the formation of Starga |
| 2025-05-30T18:03 | US Steel remarks, Pittsburgh (CNBC | NUE | Steel | up | tariff | +7.8 | +7.8 | imposing a 25% increase. We're going to bring it from 25% to 50%, the  |
| 2025-05-30T18:03 | US Steel remarks, Pittsburgh (CNBC | CLF | Steel | up | tariff | +5.6 | +5.6 | imposing a 25% increase. We're going to bring it from 25% to 50%, the  |
| 2025-05-30T18:03 | US Steel remarks, Pittsburgh (CNBC | STLD | Steel | up | tariff | +7.1 | +7.1 | imposing a 25% increase. We're going to bring it from 25% to 50%, the  |
| 2025-05-30T18:03 | US Steel remarks, Pittsburgh (CNBC | SLX | Steel | up | tariff | +3.8 | +3.8 | imposing a 25% increase. We're going to bring it from 25% to 50%, the  |
| 2025-08-06T17:17 | Apple $600B investment announcemen | INTC | Intel | up | investment | -1.0 | -1.0 | we started with Intel |
| 2025-08-06T17:20 | Apple $600B investment announcemen | MP | MP Materials | up | investment | +0.5 | +0.5 | committed to buying American made advanced magnets developed by MP Mat |
| 2025-09-30T16:14 | Signs Executive Orders, Sep. 30, 2 | PFE | Pfizer | down | deal | +1.3 | -1.3 | Alfred Bulla, and his company, Pfizer, agreed. |

## Movers the rules missed (right ≥1σ events not in tier A or B, closed market)

| when | video | ticker | entity | kind | dir | novelty | action | z_first | past | hedge | quote |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025-01-21T17:00 | Stargate AI investment announcemen | ORCL | Stargate AI project | company | up | unclear | investment | +5.7 | False | False | $500,000,000 Stargate project comes in addition to a separat |
| 2025-01-21T17:00 | Stargate AI investment announcemen | SFTBY | Stargate AI project | company | up | unclear | investment | +7.1 | False | False | $500,000,000 Stargate project comes in addition to a separat |
| 2025-01-21T17:01 | Stargate AI investment announcemen | NVDA | Artificial intelligenc | sector | up | repeat | investment | +1.1 | False | False | AI seems to be very hot. Tremendous amounts of money coming  |
| 2025-01-21T17:28 | Stargate AI investment announcemen | LNG | Cheniere | company | none | repeat | criticism | -1.7 | False | False | along with Cheniere and a couple of others convinced Bush, w |
| 2025-01-21T17:32 | Stargate AI investment announcemen | VRT | Artificial intelligenc | sector | up | repeat | regulation | +1.3 | True | True | I'd like to see federal lands opened up for data centers. I  |
| 2025-01-21T17:32 | Stargate AI investment announcemen | MSFT | Artificial intelligenc | sector | up | repeat | regulation | +2.1 | True | True | I'd like to see federal lands opened up for data centers. I  |
| 2025-04-02T16:13 | Liberation Day tariffs, Rose Garde | VNM | Vietnam | country | down | repeat | tariff | -6.4 | False | False | Vietnam charges 75% |
| 2025-04-02T16:36 | Liberation Day tariffs, Rose Garde | XLE | Russia | country | none | repeat | other | -1.0 | False | False | trying to stop Russia and Ukraine and The Middle East |
| 2025-04-02T16:36 | Liberation Day tariffs, Rose Garde | MSFT | OpenAI | company | none | repeat | investment | +1.2 | False | False | SoftBank, OpenAI |
| 2025-04-02T16:37 | Liberation Day tariffs, Rose Garde | JNJ | Johnson & Johnson | company | up | repeat | praise | +2.8 | False | False | Johnson and Johnson, great company, $55,000,000,000 |
| 2025-04-02T16:37 | Liberation Day tariffs, Rose Garde | LLY | Eli Lilly | company | up | repeat | praise | +1.2 | False | False | Eli Lilly, great company, $55,000,000,000 |
| 2025-04-02T16:38 | Liberation Day tariffs, Rose Garde | MRK | Merck | company | none | repeat | praise | +2.5 | False | False | you have Merck and Palantis |
| 2025-04-02T16:42 | Liberation Day tariffs, Rose Garde | DIA | Stock market | asset | none | repeat | praise | +1.6 | False | False | From the day of my election, the stock market went up in my  |
| 2025-04-02T16:49 | Liberation Day tariffs, Rose Garde | ELV | Health insurers | sector | none | repeat | regulation | +2.3 | False | False | We will not cut Social Security, Medicare, or Medicaid benef |
| 2025-04-02T16:49 | Liberation Day tariffs, Rose Garde | CI | Health insurers | sector | none | repeat | regulation | +1.6 | False | False | We will not cut Social Security, Medicare, or Medicaid benef |
| 2025-04-02T16:49 | Liberation Day tariffs, Rose Garde | HUM | Health insurers | sector | none | repeat | regulation | +1.0 | False | False | We will not cut Social Security, Medicare, or Medicaid benef |
| 2025-04-02T16:49 | Liberation Day tariffs, Rose Garde | UNH | Health insurers | sector | none | repeat | regulation | +2.4 | False | False | We will not cut Social Security, Medicare, or Medicaid benef |
| 2025-05-30T17:53 | US Steel remarks, Pittsburgh (CNBC | STLD | Steel | sector | none | repeat | praise | +7.1 | False | True | tough hardworking members of the United States Steel Workers |
| 2025-05-30T17:53 | US Steel remarks, Pittsburgh (CNBC | NUE | Steel | sector | none | repeat | praise | +7.8 | False | True | tough hardworking members of the United States Steel Workers |
| 2025-05-30T17:53 | US Steel remarks, Pittsburgh (CNBC | SLX | Steel | sector | up | repeat | praise | +3.8 | False | True | tough hardworking members of the United States Steel Workers |
| 2025-07-23T17:48 | Delivers Remarks and Signs Executi | GOOGL | Google | company | none | repeat | investment | +2.0 | False | False | Meta, Amazon, Google, Microsoft are all investing |
| 2025-08-06T17:07 | Apple $600B investment announcemen | SMH | Artificial intelligenc | sector | up | unclear | investment | +1.5 | False | False | invest billions of dollars to construct data centers across  |
| 2025-08-06T17:12 | Apple $600B investment announcemen | MU | Micron | company | up | repeat | investment | +2.0 | False | False | Micron, great company, is investing 200,000,000,000. |
| 2025-08-06T17:32 | Apple $600B investment announcemen | SOXX | Semiconductors | sector | none | repeat | investment | +1.3 | False | False | We're doing a lot of the semiconductors here. |
| 2025-09-19T17:00 | Signs Executive Orders, Sep. 19, 2 | XLF | Federal Reserve | asset | none | repeat | criticism | -1.5 | False | False | Powell is terrible. He's terrible. |
| 2025-09-19T17:28 | Signs Executive Orders, Sep. 19, 2 | DIS | Disney (ABC) | company | down | repeat | criticism | -1.6 | False | False | ABC is a terrible network, a very unfair network |
| 2025-09-30T16:00 | Signs Executive Orders, Sep. 30, 2 | IBIT | Bitcoin | asset | none | repeat | other | +1.2 | False | False | AI and crypto czar, David Sachs. |
| 2025-09-30T16:00 | Signs Executive Orders, Sep. 30, 2 | MSTR | Bitcoin | asset | none | repeat | other | +1.2 | False | False | AI and crypto czar, David Sachs. |
| 2025-10-29T00:03 | Delivers Keynote Remarks at APEC C | XLF | Federal Reserve | asset | none | repeat | criticism | -2.0 | False | False | incompetent head of the Fed. He's incompetent. |
| 2025-10-29T00:07 | Delivers Keynote Remarks at APEC C | SOXX | Semiconductors | sector | up | repeat | investment | +1.1 | False | False | building tremendous plants in United States, Arizona, Texas |
| 2025-10-29T00:07 | Delivers Keynote Remarks at APEC C | NVDA | Artificial intelligenc | sector | up | repeat | investment | +2.0 | False | False | AI plants being built all over, tremendous strides creating  |
| 2025-10-29T00:07 | Delivers Keynote Remarks at APEC C | SMH | Artificial intelligenc | sector | up | repeat | investment | +1.2 | False | False | AI plants being built all over, tremendous strides creating  |
| 2025-10-29T00:21 | Delivers Keynote Remarks at APEC C | MU | Micron | company | up | repeat | investment | +1.0 | False | False | Micron, 200,000,000,000 |
| 2025-10-29T00:37 | Delivers Keynote Remarks at APEC C | EWY | South Korea | country | none | repeat | other | +2.2 | False | False | gleaming streets of Seoul |
| 2025-11-17T18:27 | Delivers Remarks at McDonald's Imp | EZU | European Union | country | none | repeat | deal | -1.1 | False | False | We made a deal with the European Union, $950,000,000,000. |
| 2025-12-09T19:59 | Delivers Remarks on the Economy | EWU | United Kingdom | country | none | repeat | other | +1.2 | False | False | UK has to if they don't go back to oil |
| 2025-12-19T21:02 | Delivers Remarks on the Economy, D | FEZ | European Union | country | none | repeat | other | -1.9 | False | False | France as an example, UK, European Union |
| 2025-12-19T21:41 | Delivers Remarks on the Economy, D | KWEB | China | country | none | repeat | tariff | -4.9 | True | False | 50% tariffs to save North Carolina's furniture industry, dec |
| 2025-12-19T22:09 | Delivers Remarks on the Economy, D | USO | Iran | country | none | repeat | sanction | +1.1 | False | False | destroyed the Iran nuclear threat |
| 2026-01-03T12:26 | Holds a Press Conference, Jan. 3,  | CVX | Venezuela | country | up | new | investment | +4.6 | False | False | greatest oil companies invest billions and billions, take ou |
| 2026-01-03T12:26 | Holds a Press Conference, Jan. 3,  | XLE | Venezuela | country | up | new | investment | +2.4 | False | False | greatest oil companies invest billions and billions, take ou |
| 2026-02-11T16:34 | Participates in the Champion of Co | KWEB | China | country | none | repeat | criticism | -1.2 | False | False | They're made in China, but not used by China. They sell us t |
| 2026-02-11T16:34 | Participates in the Champion of Co | MCHI | China | country | none | repeat | criticism | -1.1 | False | False | They're made in China, but not used by China. They sell us t |
| 2026-02-11T16:45 | Participates in the Champion of Co | EWY | South Korea | country | none | repeat | deal | +1.0 | False | False | historic trade deals with Japan, Korea, India, and others to |
| 2026-02-19T16:22 | Delivers Remarks on the Economy, F | FXI | China | country | none | repeat | criticism | -1.4 | False | False | Don't forget China and these other countries, they paid for  |
| 2026-02-19T16:22 | Delivers Remarks on the Economy, F | MCHI | China | country | none | repeat | criticism | -1.4 | False | False | Don't forget China and these other countries, they paid for  |
| 2026-02-19T16:22 | Delivers Remarks on the Economy, F | KWEB | China | country | none | repeat | criticism | -1.5 | False | False | Don't forget China and these other countries, they paid for  |
| 2026-02-27T16:37 | Delivers Remarks on Energy, Feb. 2 | LNG | Natural gas / LNG | sector | up | repeat | criticism | +3.9 | True | False | Biden administration waged radical left war on American oil  |
| 2026-02-27T16:37 | Delivers Remarks on Energy, Feb. 2 | EQT | Natural gas / LNG | sector | up | repeat | criticism | +1.1 | True | False | Biden administration waged radical left war on American oil  |
| 2026-02-27T16:38 | Delivers Remarks on Energy, Feb. 2 | XOM | Oil | sector | up | repeat | criticism | +3.1 | True | False | gasoline reached a peak of over $6 a gallon in some states |
| 2026-02-27T16:38 | Delivers Remarks on Energy, Feb. 2 | CVX | Oil | sector | up | repeat | criticism | +1.9 | True | False | gasoline reached a peak of over $6 a gallon in some states |
| 2026-02-27T16:40 | Delivers Remarks on Energy, Feb. 2 | USO | Oil | sector | none | repeat | regulation | +4.0 | True | False | US oil production is now up by 600,000 barrels |
| 2026-02-27T16:52 | Delivers Remarks on Energy, Feb. 2 | XLE | Oil | sector | up | repeat | regulation | +2.9 | False | False | mandate is over and now you can buy gasoline powered car |
| 2026-02-27T17:15 | Delivers Remarks on Energy, Feb. 2 | EWU | United Kingdom | country | none | repeat | criticism | -1.0 | False | False | in London, I'm paying $87 |
| 2026-02-27T17:33 | Delivers Remarks on Energy, Feb. 2 | NOC | Northrop Grumman | company | none | repeat | praise | +2.0 | False | False | beautiful b 2 bombers |
| 2026-03-27T18:02 | Delivers Remarks at the Future Inv | KSA | Saudi Arabia | country | up | repeat | investment | +1.3 | False | False | crown prince announced that Saudi Arabia would be investing |
| 2026-03-31T17:13 | Signs an Executive Order, Mar. 31, | TLT | Federal Reserve | asset | none | repeat | criticism | -1.0 | False | False | I'm not building the Federal Reserve where the guy is spendi |
| 2026-03-31T17:14 | Signs an Executive Order, Mar. 31, | XLE | Iran | country | down | unclear | sanction | -1.9 | False | False | All I have to do is leave Iran, and we'll be doing that very |
| 2026-04-16T19:48 | Delivers Remarks on Tax Week in La | CARZ | Automakers | sector | up | repeat | tariff | +1.0 | False | False | car companies are expanding like never before. We're selling |
| 2026-04-16T20:03 | Delivers Remarks on Tax Week in La | USO | Iran | country | none | repeat | military | -2.1 | False | False | We killed him, and that had a big impact on Iran. |
| 2026-04-16T20:03 | Delivers Remarks on Tax Week in La | XLE | Iran | country | none | repeat | military | -2.4 | False | False | We killed him, and that had a big impact on Iran. |
| 2026-06-03T16:14 | Signs Executive Orders, Jun. 3, 20 | DIA | Stock market | asset | none | repeat | praise | +3.3 | False | False | we had the strongest stock market in history |
| 2026-06-04T16:17 | Makes an Announcement on Beautiful | DIA | Stock market | asset | none | repeat | praise | +1.8 | False | False | every other exchange just hit a new all time high |
| 2026-06-22T16:01 | Signs Executive Orders, Jun. 22, 2 | CORN | Agriculture | sector | up | new | subsidy | +1.2 | False | True | money gonna be put into this country...purchases of food...o |
| 2026-06-22T16:01 | Signs Executive Orders, Jun. 22, 2 | SOYB | Agriculture | sector | up | new | subsidy | +1.3 | False | True | money gonna be put into this country...purchases of food...o |
| 2026-06-22T16:01 | Signs Executive Orders, Jun. 22, 2 | DBA | Agriculture | sector | up | new | subsidy | +1.1 | False | True | money gonna be put into this country...purchases of food...o |
| 2026-06-22T16:07 | Signs Executive Orders, Jun. 22, 2 | ICLN | Solar / wind | sector | down | repeat | criticism | -1.9 | False | False | you have windmills all over the place |
| 2026-06-22T16:09 | Signs Executive Orders, Jun. 22, 2 | RTX | RTX (Raytheon) | company | up | unclear | deal | +1.2 | False | False | some of the car companies, if they have any excess capacity, |
| 2026-09-12T06:42 | Delivers Remarks to U.S. Embassy P | XLE | Venezuela | country | up | unclear | investment | +1.1 | False | False | Big oil companies are moving in. They're starting to drill. |
| 2026-09-12T06:42 | Delivers Remarks to U.S. Embassy P | CVX | Venezuela | country | up | unclear | investment | +1.1 | False | False | Big oil companies are moving in. They're starting to drill. |
