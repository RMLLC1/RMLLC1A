# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T14:31:03Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 70,000.00  
**Dividend cash (SATA collected):** 0.0917  
**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  
**Email:** only on buy/sell fills — never on mark/price updates  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Stop exits:** arm **+2%** from fill, then trail **1%** — **LIMIT** at stop (or better).
- Open paper orders auto-fill when conditions hit (no manual confirm).
- **Profits → SATA:** realized trading profit buys **SATA** at best price; **hold for daily dividends — do not sell**.

**Marks:**
- UXRP: **$17.2170** (yahoo_v8_chart_1m)
- GDXU: **$111.3500** (yahoo_v8_chart_1m)
- SATA: **$99.9950** (yahoo_v8_chart_1m)
- BTC-USD: **$83300.0000** (yahoo_v8_chart_1m)
- XRP-USD: **$1.4972** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.2170 | -57.39 |
| SATA | 13.0054 | 99.9916 | 1,300.43 | 99.9950 | 0.04 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **WORKING_LIMIT** | Arm +2% → $17.595. Trail 1% after armed. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0
- 2026-09-28T12:33:13Z **SELL_LIMIT** GDXU qty=275.558 @ $109.515 → cash $70177.73
- 2026-09-28T12:39:35Z **BUY** GDXU qty=639.0575544362919 @ $109.5363 → cash $177.73
- 2026-09-28T12:52:51Z **BUY** SATA qty=1.7778333500050014 @ $99.97 → cash $0.0
- 2026-09-28T14:30:19Z **SELL_LIMIT** GDXU qty=639.0575544362919 @ $111.2931 → cash $71122.7
- 2026-09-28T14:31:03Z **BUY** SATA qty=11.22756106967931 @ $99.99500274658203 → cash $70000.0

## Recent events

- 2026-09-28T14:00:13Z GDXU mark=112.4173 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 112.41729736328125, 'stop': 111.2931}
- 2026-09-28T14:10:20Z UXRP mark=17.7400 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388, 'mark': 17.739999771118164}
- 2026-09-28T14:10:20Z GDXU mark=111.4400 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'ARMED_HOLD', 'stop': 111.2931}
- 2026-09-28T14:20:31Z UXRP mark=17.4800 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:20:31Z GDXU mark=110.7000 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'WORKING_LIMIT', 'limit': 111.2931, 'mark': 110.69999694824219}
- 2026-09-28T14:30:19Z UXRP mark=17.2170 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:30:19Z GDXU mark=111.9195 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'FILLED_LIMIT', 'side': 'SELL', 'limit': 111.2931, 'qty': 639.0575544362919, 'proceeds': 71122.7}
- 2026-09-28T14:30:19Z queued PB-SATA-2 notional=$1122.70
- 2026-09-28T14:30:19Z SATA SELL blocked — hold for dividends
- 2026-09-28T14:30:39Z UXRP mark=17.2170 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:31:03Z UXRP mark=17.2170 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:31:03Z SATA mark=99.9950 {'id': 'PB-SATA-2', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 11.22756106967931, 'price': 99.99500274658203, 'cost': 1122.7}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every **10 minutes** while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
