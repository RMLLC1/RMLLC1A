# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T11:29:30Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 90,000.00  
**Mode:** PAPER only  

### Standing fill rule (Rodney)

- **Buys:** always use the **best (lowest)** available valid quote at decision time (prefer live/session/pre-market over a stale prior close when a fresher bid/last is available).
- **Sells:** always use the **best (highest)** available valid quote.
- Label the quote source and session (close / pre-market / regular).

**Current UXRP mark:** ~**$17.25** pre-market (2026-09-28). Entry now matches that better buy price after reprice. Arm needs **$17.595** (+2%) → stop **PENDING_ARM**. Position mark ~**$10,000**; unrealized ~**$0** at current mark.

## Positions

| Symbol | Qty | Avg cost | Cost basis | Market note |
| --- | ---: | ---: | ---: | --- |
| UXRP | 579.7101 | 17.25 | 10,000.00 | ~10% portfolio. **Repriced** to best available pre-market ~$17.25 (was incorrectly filled at stale close $19.19). |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params | Notes |
| --- | --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_SELL | **PENDING_ARM** | Arm when mark ≥ **+2%** vs avg cost → **$17.595**. After armed: trail **2%** below high-water mark. Qty: **all** (579.7101). | Updated after buy reprice. PAPER only. |

### Trailing-stop logic (TS-UXRP-1)

1. **While PENDING_ARM:** if mark ≥ $17.595, set status → **ARMED**, set `high_water = mark`, `stop = high_water × 0.98`.
2. **While ARMED:** if mark > high_water, raise high_water and stop (`stop = high_water × 0.98`).
3. **Trigger:** if mark ≤ stop, **SELL all** UXRP at best available sell quote (paper fill), log trade, clear order + position.
4. Refresh marks when Rodney asks; this environment does not stream live prices.

## Trade log

| UTC time | Side | Symbol | Qty | Price | Cash after | Rationale |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 2026-09-28T11:29:30Z | ADJUST | UXRP | 579.7101 | 17.25 | 90,000.00 | **Reprice** prior paper buy to best available pre-market ~$17.25 per Rodney standing rule (was 521.1058 @ 19.19). Same $10,000 notional. |
| 2026-09-28T11:20:55Z | BUY | UXRP | 521.1058 | 19.19 | 90,000.00 | SUPERSEDED — used stale close; corrected by ADJUST above. |
| — | — | — | — | — | 100000.00 | Initialized empty paper account |

## Watchlist

| Symbol | Notes |
| --- | --- |
| UXRP | ProShares Ultra XRP (2× daily). Trailing stop TS-UXRP-1 pending +2% arm at $17.595. |

## Rules

- All fills are simulated. No broker or exchange connection.
- Do not treat P&amp;L as investable advice.
- Prefer best available price on buys (low) and sells (high) when multiple quotes exist.
