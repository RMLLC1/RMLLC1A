# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T11:25:00Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 90,000.00  
**Mode:** PAPER only  
**Equity (mark ≈ last close):** refresh on next mark-to-market

## Positions

| Symbol | Qty | Avg cost | Cost basis | Market note |
| --- | ---: | ---: | ---: | --- |
| UXRP | 521.1058 | 19.19 | 10,000.00 | ~10% of portfolio; assumed fill = last official close 2026-09-25 (Yahoo). Not a live broker fill. |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params | Notes |
| --- | --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_SELL | **PENDING_ARM** | Arm when mark ≥ **+2%** vs avg cost → **$19.5738**. After armed: trail **2%** below high-water mark. Qty: **all** (521.1058). | Rodney 2026-09-28. Not a live broker order. Trail = 2% (matched to profit trigger). |

### Trailing-stop logic (TS-UXRP-1)

1. **While PENDING_ARM:** if mark ≥ $19.5738, set status → **ARMED**, set `high_water = mark`, `stop = high_water × 0.99`.
2. **While ARMED:** if mark > high_water, raise high_water and stop (`stop = high_water × 0.99`).
3. **Trigger:** if mark ≤ stop, **SELL all** UXRP at assumed mark (paper fill), log trade, clear order + position.
4. John / markets must refresh a mark when Rodney asks for a check; this environment does not stream live prices.

## Trade log

| UTC time | Side | Symbol | Qty | Price | Cash after | Rationale |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 2026-09-28T11:20:55Z | BUY | UXRP | 521.1058 | 19.19 | 90,000.00 | Rodney: 10% paper portfolio buy. Assumed price = UXRP last close 2026-09-25 ~$19.19 (Yahoo). PAPER only. |
| — | — | — | — | — | 100000.00 | Initialized empty paper account |

## Watchlist

| Symbol | Notes |
| --- | --- |
| UXRP | ProShares Ultra XRP (2× daily). Trailing stop TS-UXRP-1 pending +2% arm. |

## Rules

- All fills are simulated. No broker or exchange connection.
- Do not treat P&amp;L as investable advice.
- Assumed prices are labeled; refresh marks when Rodney asks for a portfolio update.
