# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T12:33:13Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 70,177.73  
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
- GDXU: **$109.8000** (yahoo_v8_chart_1m)
- BTC-USD: **$83298.1562** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5171** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.8300 | 1,008.70 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **ARMED** | Arm +2% → $17.595. Trail 2%. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0
- 2026-09-28T12:33:13Z **SELL_LIMIT** GDXU qty=275.558 @ $109.515 → cash $70177.73

## Recent events

- 2026-09-28T12:28:52Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:28:52Z GDXU mark=110.0000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'ARMED_HOLD', 'stop': 109.515}
- 2026-09-28T12:29:13Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:29:13Z GDXU mark=110.0000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'ARMED_HOLD', 'stop': 109.515}
- 2026-09-28T12:30:15Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:30:15Z GDXU mark=109.7700 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'ARMED_HOLD', 'stop': 109.515}
- 2026-09-28T12:31:17Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:31:17Z GDXU mark=109.9500 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'ARMED_HOLD', 'stop': 109.515}
- 2026-09-28T12:32:21Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:32:21Z GDXU mark=109.3000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'WORKING_LIMIT', 'limit': 109.515, 'mark': 109.3}
- 2026-09-28T12:33:13Z UXRP mark=17.8300 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.4734}
- 2026-09-28T12:33:13Z GDXU mark=109.8000 {'id': 'TS-GDXU-1', 'symbol': 'GDXU', 'event': 'FILLED_LIMIT', 'side': 'SELL', 'limit': 109.515, 'qty': 275.558, 'proceeds': 30177.73}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
