# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T12:39:35Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 177.73  
**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  
**Email:** only on buy/sell fills — never on mark/price updates  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Stop exits:** **LIMIT** at stop (or better) — never market.
- Open paper orders auto-fill when conditions hit (no manual confirm).

**Marks:**
- UXRP: **$17.8300** (yahoo_v8_chart_1m)
- GDXU: **$109.5363** (yahoo_v8_chart_1m)
- BTC-USD: **$83322.3203** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5125** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.8300 | 1,008.70 |
| GDXU | 639.0576 | 109.5363 | 70,000.00 | 109.5363 | 0.00 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **ARMED** | Arm +2% → $17.595. Trail 2%. LIMIT sell at stop. |
| TS-GDXU-2 | GDXU | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $111.727. Trail 2%. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0
- 2026-09-28T12:33:13Z **SELL_LIMIT** GDXU qty=275.558 @ $109.515 → cash $70177.73
- 2026-09-28T12:39:35Z **BUY** GDXU qty=639.0575544362919 @ $109.5363 → cash $177.73

## Recent events

- 2026-09-28T12:32:21Z GDXU mark=109.3000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'WORKING_LIMIT', 'limit': 109.515, 'mark': 109.3}
- 2026-09-28T12:33:13Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:33:13Z GDXU mark=109.8000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'FILLED_LIMIT', 'side': 'SELL', 'limit': 109.515, 'qty': 275.558, 'proceeds': 30177.73}
- 2026-09-28T12:34:18Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:35:23Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:36:12Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:37:14Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:38:21Z UXRP STALE_QUOTE age=918s mark=17.83 — order logic skipped
- 2026-09-28T12:39:35Z UXRP STALE_QUOTE age=992s mark=17.83 — order logic skipped
- 2026-09-28T12:39:35Z GDXU mark=109.5363 {'id': 'LB-GDXU-2', 'symbol': 'GDXU', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 639.0575544362919, 'price': 109.5363, 'cost': 70000.0, 'limit': 110.0}
- 2026-09-28T12:39:35Z GDXU attached TS-GDXU-2 PENDING_ARM arm=111.727
- 2026-09-28T12:39:35Z GDXU mark=109.5363 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
