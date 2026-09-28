# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T12:21:43Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 40,000.00  
**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  
**Email:** only on buy/sell fills — never on mark/price updates  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Stop exits:** **LIMIT** at stop (or better) — never market.
- Open paper orders auto-fill when conditions hit (no manual confirm).

**Marks:**
- UXRP: **$17.6521** (yahoo_v8_chart_1m)
- GDXU: **$111.7500** (yahoo_v8_chart_1m)
- BTC-USD: **$83395.9922** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5177** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.6521 | 699.30 |
| GDXU | 275.5580 | 108.8700 | 30,000.00 | 111.7500 | 793.61 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **ARMED** | Arm +2% → $17.595. Trail 2%. LIMIT sell at stop. |
| TS-GDXU-1 | GDXU | TRAILING_STOP_LIMIT_SELL | **ARMED** | Arm +2% → $111.0474. Trail 2%. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0

## Recent events

- 2026-09-28T12:16:21Z UXRP STALE_QUOTE age=2241s mark=17.4 — order logic skipped
- 2026-09-28T12:16:21Z GDXU mark=110.1682 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:17:22Z UXRP STALE_QUOTE age=2302s mark=17.4 — order logic skipped
- 2026-09-28T12:17:22Z GDXU mark=110.7300 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:18:30Z UXRP STALE_QUOTE age=2371s mark=17.4 — order logic skipped
- 2026-09-28T12:18:30Z GDXU mark=110.7200 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:19:18Z UXRP STALE_QUOTE age=2418s mark=17.4 — order logic skipped
- 2026-09-28T12:19:18Z GDXU mark=110.7200 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:20:30Z UXRP mark=17.6521 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED', 'high_water': 17.6521, 'stop': 17.2991}
- 2026-09-28T12:20:30Z GDXU mark=111.4900 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'ARMED', 'high_water': 111.49, 'stop': 109.2602}
- 2026-09-28T12:21:43Z UXRP mark=17.6521 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.2991}
- 2026-09-28T12:21:43Z GDXU mark=111.7500 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 111.75, 'stop': 109.515}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
