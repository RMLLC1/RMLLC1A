# UXRP research brief (PAPER / education only)

**For:** Rodney Bishop (via John)  
**Date:** 2026-09-28  
**Analyst:** markets specialist  
**Disclaimer:** Not licensed advice. Simulated/paper context only. No live trade.

## What it is

**UXRP** is the **ProShares Ultra XRP ETF** — a U.S.-listed **leveraged ETF**, not spot XRP and not an ETN.

| Item | Detail |
| --- | --- |
| Issuer | ProShares |
| Ticker | UXRP |
| Objective | **2× the daily** performance of the **Bloomberg XRP Index** (before fees/expenses) |
| Inception | 2025-07-14 |
| Expense ratio | **1.67%** (issuer-stated) |
| How exposure is built | **XRP futures** (and related derivatives); **does not hold spot XRP** |
| Typical use (issuer framing) | Short-term / tactical; daily reset product |

**Clarification vs “Uxrp” / XRP spot:** Holding UXRP is **not** the same as owning XRP on an exchange or wallet. Returns track a **daily 2×** target via futures, so multi-day results can diverge sharply from 2× of XRP’s multi-day move (compounding / volatility decay).

## Underlying exposure

- **Benchmark:** Bloomberg XRP Index (USD performance of XRP).
- **Mechanism:** Leveraged long via CME/other cash-settled XRP futures (holdings change over time).
- **Not:** Direct XRP custody, staking, or 1:1 spot ETF exposure.

## Key risks

1. **Leverage (2× daily)** — Gains and losses on a single day are amplified; large adverse moves can be severe.
2. **Crypto volatility** — XRP itself is highly volatile; leverage magnifies that.
3. **Daily reset / path dependency** — Holding beyond one day often does **not** equal 2× XRP’s return over the same period; choppy markets can erode value even if XRP ends flat-to-up.
4. **Futures basis / tracking** — Futures can diverge from spot; fund may miss its daily target.
5. **Fees & liquidity** — ~1.67% expense ratio; bid-ask and volume matter for small accounts.
6. **Product age / drawdowns** — Relatively new; issuer total-return figures show very large declines since inception (see price context). Loss of principal is plausible.

## Recent price context (public sources — label uncertainty)

| Source / as-of | Figure | Uncertainty |
| --- | --- | --- |
| ProShares site, **as of 2026-09-25** | Market price **~$19.19**; NAV **~$19.23**; volume ~263k | Issuer page; not a live quote for 2026-09-28 |
| Recent sessions (third-party history, ~Sep 18–24) | Closes roughly **~$13–$19** range in a volatile week | Aggregators disagree slightly; treat as approximate |
| 52-week-style range (third parties) | Roughly **~$8.67 – ~$160–$180** | Ranges vary by vendor |
| ProShares month-end (as of **2026-08-31**) | NAV ~**−89%** 1Y / since inception (approx.) | Confirms path-dependency + crypto drawdown risk |

**No live quote pulled for 2026-09-28 market open.** Do not treat any figure above as a fill price.

## Paper-trade experiment (educational only)

A **small** paper position (e.g. a few hundred simulated USD) could be educational to observe:

- how UXRP moves vs spot XRP day-to-day, and  
- multi-day drift vs a naive “2× XRP” expectation.

**Cautious note:** Educational value is highest with a **tiny** size, a **short** holding window, and explicit journaling of daily P&amp;L vs XRP. It is **not** a recommendation to buy live or to size meaningfully. Leverage + crypto = high chance of a large simulated loss quickly.

**This turn:** No paper trade placed; portfolio unchanged (`agents/markets/paper-portfolio.md` still 100% cash).

## Sources (public)

- ProShares UXRP product page / fact sheet  
- SEC / NASDAQ information circulars describing 2× daily Bloomberg XRP Index objective  
- Third-party quote aggregators for recent closes (approximate)

---

*Uncertainty labeled throughout. Not advice. PAPER context only.*
