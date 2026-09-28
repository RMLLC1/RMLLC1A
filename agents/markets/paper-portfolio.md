# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T11:31:23Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 70,000.00  
**Mode:** PAPER only  

### Standing fill rule (Rodney)

- **Buys:** always use the **best (lowest)** available valid quote at decision time (prefer live/session/pre-market over a stale prior close when a fresher bid/last is available).
- **Sells:** always use the **best (highest)** available valid quote.
- Label the quote source and session (close / pre-market / regular).

**Current UXRP mark:** ~**$17.25** pre-market (2026-09-28; Yahoo / StockAnalysis — lowest vs ~$17.34 VWAP).  
**Exposure:** ~**30%** of portfolio in UXRP ($30,000 cost / ~$100k).  
**Trailing stop TS-UXRP-1:** **PENDING_ARM** until mark ≥ **$17.595** (+2% vs avg $17.25).

## Positions

| Symbol | Qty | Avg cost | Cost basis | Market note |
| --- | ---: | ---: | ---: | --- |
| UXRP | 1739.1304 | 17.25 | 30,000.00 | 10% + additional 20% paper buys @ best pre-market ~$17.25 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params | Notes |
| --- | --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_SELL | **PENDING_ARM** | Arm when mark ≥ **+2%** vs avg cost → **$17.595**. After armed: trail **2%** below high-water mark. Qty: **all** (1739.1304). | Covers full UXRP position after 20% add-on. PAPER only. |

### Trailing-stop logic (TS-UXRP-1)

1. **While PENDING_ARM:** if mark ≥ $17.595, set status → **ARMED**, set `high_water = mark`, `stop = high_water × 0.98`.
2. **While ARMED:** if mark > high_water, raise high_water and stop (`stop = high_water × 0.98`).
3. **Trigger:** if mark ≤ stop, **SELL all** UXRP at best available sell quote (paper fill), log trade, clear order + position.
4. Refresh marks when Rodney asks; this environment does not stream live prices.

## Trade log

| UTC time | Side | Symbol | Qty | Price | Cash after | Rationale |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 2026-09-28T11:31:23Z | BUY | UXRP | 1159.4203 | 17.25 | 70,000.00 | Rodney: +20% of portfolio pre-market. Best buy quote ~$17.25 (vs higher VWAP ~$17.34). PAPER. Trailing stop TS-UXRP-1 retargeted to full position. |
| 2026-09-28T11:29:30Z | ADJUST | UXRP | 579.7101 | 17.25 | 90,000.00 | **Reprice** prior paper buy to best available pre-market ~$17.25 per Rodney standing rule (was 521.1058 @ 19.19). Same $10,000 notional. |
| 2026-09-28T11:20:55Z | BUY | UXRP | 521.1058 | 19.19 | 90,000.00 | SUPERSEDED — used stale close; corrected by ADJUST above. |
| — | — | — | — | — | 100000.00 | Initialized empty paper account |

## Watchlist

| Symbol | Notes |
| --- | --- |
| UXRP | ~30% paper weight. TS-UXRP-1 pending arm at $17.595 (+2%), then 2% trail. |

## Rules

- All fills are simulated. No broker or exchange connection.
- Do not treat P&amp;L as investable advice.
- Prefer best available price on buys (low) and sells (high) when multiple quotes exist.
