# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T12:08:18Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 40,000.00  
**Mode:** PAPER only  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; may lag / miss thin premarket prints)  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Stop exits:** **LIMIT** at stop (or better) — never market.

**Marks:**
- UXRP: **$17.4000** (yahoo_v8_chart_1m)
- GDXU: **$111.0000** (yahoo_v8_chart_1m)
- BTC-USD: **$83407.6484** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5068** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.4000 | 260.87 |
| GDXU | 275.5580 | 108.8700 | 30,000.00 | 111.0000 | 586.94 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $17.595. Trail 2%. LIMIT sell at stop. |
| TS-GDXU-1 | GDXU | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $111.0474. Trail 2%. LIMIT sell at stop. |

## Recent events

- 2026-09-28T12:03:31Z UXRP STALE_QUOTE age=1432s mark=17.4 — stop logic skipped
- 2026-09-28T12:03:31Z GDXU mark=108.7407 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:04:17Z UXRP STALE_QUOTE age=1478s mark=17.4 — stop logic skipped
- 2026-09-28T12:04:17Z GDXU mark=108.7400 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:05:08Z UXRP STALE_QUOTE age=1529s mark=17.4 — stop logic skipped
- 2026-09-28T12:05:08Z GDXU mark=108.7400 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:06:16Z UXRP STALE_QUOTE age=1597s mark=17.4 — stop logic skipped
- 2026-09-28T12:06:16Z GDXU mark=110.7500 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:07:13Z UXRP STALE_QUOTE age=1654s mark=17.4 — stop logic skipped
- 2026-09-28T12:07:13Z GDXU mark=111.0000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:08:18Z UXRP STALE_QUOTE age=1719s mark=17.4 — stop logic skipped
- 2026-09-28T12:08:18Z GDXU mark=111.0000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.
