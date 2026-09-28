# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T12:18:30Z  
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
- UXRP: **$17.4000** (yahoo_v8_chart_1m)
- GDXU: **$110.7200** (yahoo_v8_chart_1m)
- BTC-USD: **$83358.4375** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5138** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.4000 | 260.87 |
| GDXU | 275.5580 | 108.8700 | 30,000.00 | 110.7200 | 509.78 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $17.595. Trail 2%. LIMIT sell at stop. |
| TS-GDXU-1 | GDXU | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $111.0474. Trail 2%. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0

## Recent events

- 2026-09-28T12:12:12Z UXRP STALE_QUOTE age=1993s mark=17.4 — stop logic skipped
- 2026-09-28T12:12:12Z GDXU mark=109.5161 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:15:26Z UXRP STALE_QUOTE age=2186s mark=17.4 — order logic skipped
- 2026-09-28T12:15:26Z GDXU mark=110.1500 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:16:03Z UXRP STALE_QUOTE age=2223s mark=17.4 — order logic skipped
- 2026-09-28T12:16:03Z GDXU mark=110.2000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:16:21Z UXRP STALE_QUOTE age=2241s mark=17.4 — order logic skipped
- 2026-09-28T12:16:21Z GDXU mark=110.1682 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:17:22Z UXRP STALE_QUOTE age=2302s mark=17.4 — order logic skipped
- 2026-09-28T12:17:22Z GDXU mark=110.7300 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:18:30Z UXRP STALE_QUOTE age=2371s mark=17.4 — order logic skipped
- 2026-09-28T12:18:30Z GDXU mark=110.7200 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
