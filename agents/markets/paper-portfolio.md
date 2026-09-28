# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T17:20:40Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 100,000.00  
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
- UXRP: **$17.6100** (yahoo_v8_chart_1m)
- GDXU: **$109.7728** (yahoo_v8_chart_1m)
- SATA: **$100.0100** (yahoo_v8_chart_1m)
- BTC-USD: **$83980.2109** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5081** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| SATA | 44.4964 | 100.0046 | 4,449.85 | 100.0100 | 0.24 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0
- 2026-09-28T12:33:13Z **SELL_LIMIT** GDXU qty=275.558 @ $109.515 → cash $70177.73
- 2026-09-28T12:39:35Z **BUY** GDXU qty=639.0575544362919 @ $109.5363 → cash $177.73
- 2026-09-28T12:52:51Z **BUY** SATA qty=1.7778333500050014 @ $99.97 → cash $0.0
- 2026-09-28T14:30:19Z **SELL_LIMIT** GDXU qty=639.0575544362919 @ $111.2931 → cash $71122.7
- 2026-09-28T14:31:03Z **BUY** SATA qty=11.22756106967931 @ $99.99500274658203 → cash $70000.0
- 2026-09-28T14:54:15Z **BUY** UXRP qty=4124.197358277689 @ $16.972999572753906 → cash $0.0
- 2026-09-28T17:20:40Z **SELL_LIMIT** UXRP qty=5863.327758277689 @ $17.5923 → cash $103149.42
- 2026-09-28T17:20:40Z **BUY** SATA qty=31.491050222256366 @ $100.01000213623047 → cash $100000.0

## Recent events

- 2026-09-28T15:50:19Z UXRP mark=17.2121 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'PENDING_ARM'}
- 2026-09-28T16:00:14Z UXRP mark=17.2121 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'PENDING_ARM'}
- 2026-09-28T16:10:22Z UXRP mark=17.3899 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'ARMED', 'high_water': 17.38990020751953, 'stop': 17.216}
- 2026-09-28T16:20:31Z UXRP mark=17.3200 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'ARMED_HOLD', 'stop': 17.216}
- 2026-09-28T16:30:43Z UXRP mark=17.7700 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'TRAILED', 'high_water': 17.770000457763672, 'stop': 17.5923}
- 2026-09-28T16:40:25Z UXRP mark=17.5000 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.5923, 'mark': 17.5}
- 2026-09-28T16:50:22Z UXRP mark=17.5000 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.5923}
- 2026-09-28T17:00:20Z UXRP mark=17.4056 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.5923}
- 2026-09-28T17:10:21Z UXRP mark=17.1900 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'WORKING_LIMIT', 'limit': 17.5923}
- 2026-09-28T17:20:40Z UXRP mark=17.6100 {'id': 'TS-UXRP-2', 'symbol': 'UXRP', 'event': 'FILLED_LIMIT', 'side': 'SELL', 'limit': 17.5923, 'qty': 5863.327758277689, 'proceeds': 103149.42}
- 2026-09-28T17:20:40Z queued PB-SATA-3 notional=$3149.42
- 2026-09-28T17:20:40Z SATA mark=100.0100 {'id': 'PB-SATA-3', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 31.491050222256366, 'price': 100.01000213623047, 'cost': 3149.42}

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every **10 minutes** while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
