# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T14:54:15Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 0.00  
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
- UXRP: **$16.9730** (yahoo_v8_chart_1m)
- GDXU: **$108.3509** (yahoo_v8_chart_1m)
- SATA: **$99.9950** (yahoo_v8_chart_1m)
- BTC-USD: **$82858.4297** (yahoo_v8_chart_1m)
- XRP-USD: **$1.4854** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 5863.3278 | 17.0552 | 100,000.00 | 16.9730 | -481.74 |
| SATA | 13.0054 | 99.9916 | 1,300.43 | 99.9950 | 0.04 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-2 | UXRP | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $17.3125. Trail 1%. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0
- 2026-09-28T12:33:13Z **SELL_LIMIT** GDXU qty=275.558 @ $109.515 → cash $70177.73
- 2026-09-28T12:39:35Z **BUY** GDXU qty=639.0575544362919 @ $109.5363 → cash $177.73
- 2026-09-28T12:52:51Z **BUY** SATA qty=1.7778333500050014 @ $99.97 → cash $0.0
- 2026-09-28T14:30:19Z **SELL_LIMIT** GDXU qty=639.0575544362919 @ $111.2931 → cash $71122.7
- 2026-09-28T14:31:03Z **BUY** SATA qty=11.22756106967931 @ $99.99500274658203 → cash $70000.0
- 2026-09-28T14:54:15Z **BUY** UXRP qty=4124.197358277689 @ $16.972999572753906 → cash $0.0

## Recent events

- 2026-09-28T14:30:19Z UXRP mark=17.2170 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:30:19Z GDXU mark=111.9195 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'FILLED_LIMIT', 'side': 'SELL', 'limit': 111.2931, 'qty': 639.0575544362919, 'proceeds': 71122.7}
- 2026-09-28T14:30:19Z queued PB-SATA-2 notional=$1122.70
- 2026-09-28T14:30:19Z SATA SELL blocked — hold for dividends
- 2026-09-28T14:30:39Z UXRP mark=17.2170 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:31:03Z UXRP mark=17.2170 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:31:03Z SATA mark=99.9950 {'id': 'PB-SATA-2', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 11.22756106967931, 'price': 99.99500274658203, 'cost': 1122.7}
- 2026-09-28T14:40:25Z UXRP mark=17.4450 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:50:31Z UXRP mark=17.0501 {'id': 'TS-UXRP-1', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.9388}
- 2026-09-28T14:54:15Z UXRP mark=16.9730 {'id': 'LB-UXRP-2', 'symbol': 'UXRP', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 4124.197358277689, 'price': 16.972999572753906, 'cost': 70000.0, 'limit': 17.05}
- 2026-09-28T14:54:15Z UXRP attached TS-UXRP-2 PENDING_ARM arm=17.3125
- 2026-09-28T14:54:15Z UXRP mark=16.9730 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every **10 minutes** while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
