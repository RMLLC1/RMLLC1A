# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-28T16:00:45Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 0.00  
**Dividend cash (SATA collected):** 0.0000  
**Dividends earned total (running):** 399.2004  
**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  
**Notify:** Gmail + Telegram on buy/sell fills (with balances) — never on mark/price updates  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Trading exits:** default hard **−2%** / arm **+1%** / trail **0.5%** market / scale **⅓@+2%** + **⅓@+5%**. **UXRP:** hard **−3%** / arm **+2%** / trail **0.5%**. **GDXU:** hard **−4.5%** / arm **+3%** / trail **0.5%** / scale **⅓@+3%** + **⅓@+7%**.
- **Income SATA (~dividends sleeve):** no stops / no scale-outs / no sells unless Rodney overrides.
- Open paper orders auto-fill when conditions hit (no manual confirm).
- **Profits → SATA:** realized **trading** profit buys **SATA** at best; **dividend_cash** reinvests daily into SATA (any balance ≥ $1; fractional OK).
- **Hold for daily dividends — do not sell** income SATA unless Rodney overrides.

**Marks:**
- BTC-USD: **$59439.9883** (yahoo_v8_chart_1m)
- GDXU: **$59.1900** (yahoo_v8_chart_1m)
- MRVL: **$139.9217** (yahoo_v8_chart_1m)
- NVDA: **$149.8000** (yahoo_v8_chart_1m)
- SATA: **$92.0000** (yahoo_v8_chart_1m)
- SOL-USD: **$70.6300** (yahoo_v8_chart_1m)
- UXRP: **$6.3500** (yahoo_v8_chart_1m)
- XRP-USD: **$0.9413** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SATA | LONG | 1251.0055 | 92.0161 | 115,112.59 | 92.0000 | -20.08 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-10 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.76 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| PB-SATA-11 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.77 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |

## Trade log (buys/sells)

- 2026-11-16T20:57:55Z **SELL** SATA qty=252.2191680112639 @ $94.87999725341797 → cash $23930.55
- 2026-11-16T20:58:24Z **BUY** GDXU qty=373.5646411492827 @ $64.05999755859375 → cash $0.0
- 2026-11-17T15:00:26Z **SELL_MARKET** GDXU qty=373.5646411492827 @ $67.25 → cash $25122.22
- 2026-11-17T15:00:26Z **BUY** SATA qty=13.488643749548233 @ $95.0999984741211 → cash $23930.55
- 2026-11-17T15:00:59Z **BUY** SATA qty=251.6356507251896 @ $95.0999984741211 → cash $0.0
- 2026-11-23T14:10:20Z **SELL_MARKET** SOL qty=667.3785534170665 @ $75.47000122070312 → cash $50367.06
- 2026-11-23T14:10:20Z **BUY** SATA qty=5.294893284165829 @ $89.49 → cash $50000.0
- 2026-11-23T16:36:15Z **SELL** SATA qty=522.6383557701675 @ $90.4000015258789 → cash $97246.51
- 2026-11-23T16:36:23Z **BUY** GDXU qty=1993.9821424487884 @ $48.77000045776367 → cash $0.0
- 2026-11-27T17:00:56Z **SELL_MARKET** GDXU qty=1993.9821424487884 @ $57.72999954223633 → cash $115112.59
- 2026-11-27T17:00:56Z **BUY** SATA qty=707.8224971417761 @ $91.98999786376953 → cash $50000.0
- 2026-11-27T19:45:24Z **BUY** SATA qty=543.1830526887561 @ $92.05 → cash $0.0

## Recent events

- 2026-11-27T16:51:03Z GDXU mark=57.6210 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 57.62099838256836, 'stop': 57.3329}
- 2026-11-27T16:55:35Z GDXU mark=58.0700 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 58.06999969482422, 'stop': 57.7796}
- 2026-11-27T17:00:56Z GDXU mark=57.7300 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'FILLED_MARKET', 'side': 'SELL', 'limit': 57.7796, 'price': 57.72999954223633, 'qty': 1993.9821424487884, 'proceeds': 115112.59}
- 2026-11-27T17:00:56Z queued PB-SATA-18 $65112.59 (EXIT_REMAINDER_TO_SATA)
- 2026-11-27T17:00:56Z GDXU exit_redeploy: keep $50,000.00 cash, $65,112.59 -> SATA
- 2026-11-27T17:00:56Z SATA mark=91.9900 {'id': 'PB-SATA-18', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 707.8224971417761, 'price': 91.98999786376953, 'cost': 65112.59}
- 2026-11-27T19:40:28Z TEXT queued LB-SATA-1 LIMIT_BUY SATA @92.0 $50000.0
- 2026-11-27T19:40:30Z SATA mark=92.0500 {'id': 'LB-SATA-1', 'symbol': 'SATA', 'event': 'WORKING_BUY', 'limit': 92.0}
- 2026-11-27T19:45:15Z SATA mark=92.0500 {'id': 'LB-SATA-1', 'symbol': 'SATA', 'event': 'WORKING_BUY', 'limit': 92.0}
- 2026-11-27T19:45:23Z TEXT cancel LB-SATA-1
- 2026-11-27T19:45:23Z TEXT queued BB-SATA-2 BUY_BEST SATA $50000.0
- 2026-11-27T19:45:24Z SATA mark=92.0500 {'id': 'BB-SATA-2', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 543.1830526887561, 'price': 92.05, 'cost': 50000.0}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
