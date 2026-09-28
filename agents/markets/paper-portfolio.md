# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T11:34:04Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 40,000.00  
**Mode:** PAPER only  

### Standing fill rule (Rodney)

- **Buys:** always use the **best (lowest)** available valid quote at decision time (prefer live/session/pre-market over a stale prior close when a fresher bid/last is available).
- **Sells:** always use the **best (highest)** available valid quote.
- **Stop exits:** use **limit** orders (limit = stop price, fill at limit or better) — **never market** sells from the trailing stop.
- Label the quote source and session (close / pre-market / regular).

**Marks / exposure (approx):**
- UXRP ~$17.25 pre-market → ~30% ($30k)
- GDXU ~$108.87 pre-market (Yahoo; best vs last close ~$127.75) → ~30% ($30k)
- Cash 40%
- **TS-UXRP-1** PENDING_ARM @ $17.595 | **TS-GDXU-1** PENDING_ARM @ $111.0474

## Positions

| Symbol | Qty | Avg cost | Cost basis | Market note |
| --- | ---: | ---: | ---: | --- |
| UXRP | 1739.1304 | 17.25 | 30,000.00 | ~30% — best pre-market fills |
| GDXU | 275.5580 | 108.87 | 30,000.00 | U.S. MicroSectors 3× gold miners ETN. ~30% @ best pre-market ~$108.87 (vs close ~$127.75) |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params | Notes |
| --- | --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → **$17.595**. Trail 2%. Trigger → **LIMIT sell** at stop (not market). Qty: all. | PAPER |
| TS-GDXU-1 | GDXU | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → **$111.0474**. Trail 2%. Trigger → **LIMIT sell** at stop (not market). Qty: all (275.5580). | Same rules as UXRP. PAPER |

### Trailing-stop logic (shared)

1. **PENDING_ARM** until mark ≥ avg_cost × 1.02 → **ARMED**; `high_water = mark`; `stop = high_water × 0.98`.
2. **ARMED:** raise high_water/stop on new highs (`stop = high_water × 0.98`).
3. **Trigger** (mark ≤ stop): working **LIMIT SELL** all shares at **limit = stop** — never market.
4. **Limit fill:** only at limit or better; if quote below limit, leave working / unfilled — do not chase market.
5. On fill: log, clear order + position.

## Trade log

| UTC time | Side | Symbol | Qty | Price | Cash after | Rationale |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 2026-09-28T11:34:04Z | BUY | GDXU | 275.5580 | 108.87 | 40,000.00 | Rodney: 30% portfolio. Best buy = pre-market ~$108.87 (Yahoo) vs last close ~$127.75. U.S. GDXU. PAPER. TS-GDXU-1 set (+2% arm, 2% trail, limit exit). |
| 2026-09-28T11:31:23Z | BUY | UXRP | 1159.4203 | 17.25 | 70,000.00 | Rodney: +20% of portfolio pre-market. Best buy quote ~$17.25. PAPER. |
| 2026-09-28T11:29:30Z | ADJUST | UXRP | 579.7101 | 17.25 | 90,000.00 | Reprice prior buy to best pre-market ~$17.25. |
| 2026-09-28T11:20:55Z | BUY | UXRP | 521.1058 | 19.19 | 90,000.00 | SUPERSEDED — stale close. |
| — | — | — | — | — | 100000.00 | Initialized empty paper account |

## Watchlist

| Symbol | Notes |
| --- | --- |
| UXRP | ~30%. TS-UXRP-1 pending arm $17.595; limit exit. |
| GDXU | ~30% U.S. 3× miners ETN. TS-GDXU-1 pending arm $111.0474; limit exit. |

## Rules

- All fills are simulated. No broker or exchange connection.
- Do not treat P&amp;L as investable advice.
- Prefer best available price on buys (low) and sells (high); stop exits are limits only.
