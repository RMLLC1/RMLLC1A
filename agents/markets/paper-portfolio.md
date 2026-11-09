# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-09T19:16:57Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 0.00  
**Dividend cash (SATA collected):** 0.0000  
**Dividends earned total (running):** 151.7897  
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
- BTC-USD: **$74589.9062** (yahoo_v8_chart_1m)
- GDXU: **$101.9600** (yahoo_v8_chart_1m)
- MRVL: **$153.2050** (yahoo_v8_chart_1m)
- NVDA: **$176.0621** (yahoo_v8_chart_1m)
- SATA: **$96.8050** (yahoo_v8_chart_1m)
- UXRP: **$8.6300** (yahoo_v8_chart_1m)
- XRP-USD: **$1.0922** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SATA | LONG | 461.0472 | 97.8667 | 45,121.19 | 96.8050 | -489.51 |
| NVDA | LONG | 283.9907 | 176.0621 | 50,000.00 | 176.0621 | 0.00 |
| MRVL | LONG | 326.3601 | 153.2050 | 50,000.00 | 153.2050 | 0.00 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| TS-NVDA-1 | NVDA | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +1% → $177.8227. Trail 0.5% → market sell on reverse. (group BB-NVDA-1) |
| TS-MRVL-1 | MRVL | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +1% → $154.7371. Trail 0.5% → market sell on reverse. (group BB-MRVL-1) |

## Trade log (buys/sells)

- 2026-11-04T10:21:08Z **BUY** SATA qty=89.77339135840846 @ $96.51 → cash $200000.0
- 2026-11-04T10:30:59Z **UNWIND** GDXU qty=1402.1164678638092 @ $77.5 → cash $100000.0
- 2026-11-04T10:31:09Z **SELL_LIMIT** GDXU qty=1402.1164678638092 @ $82.0 → cash $208621.96
- 2026-11-04T10:31:09Z **BUY** SATA qty=89.3374779815563 @ $96.51 → cash $200000.0
- 2026-11-04T10:31:45Z **UNWIND** GDXU qty=1402.1164678638092 @ $77.5 → cash $100000.0
- 2026-11-04T20:10:10Z **SELL** GDXU qty=701.0582339319047 @ $82.58000183105469 → cash $157893.39
- 2026-11-04T20:10:10Z **BUY** SATA qty=80.50782954168228 @ $98.04499816894531 → cash $150000.0
- 2026-11-04T22:10:07Z **SELL_MARKET** GDXU qty=701.0582339319045 @ $81.5 → cash $207136.25
- 2026-11-04T22:10:07Z **BUY** SATA qty=73.16979390956628 @ $97.53 → cash $200000.0
- 2026-11-09T19:00:34Z **BUY** SATA qty=0.7347149352461123 @ $96.98999786376953 → cash $100000.0
- 2026-11-09T19:16:57Z **BUY** NVDA qty=283.9907002752373 @ $176.06210327148438 → cash $50000.0
- 2026-11-09T19:16:57Z **BUY** MRVL qty=326.360101840128 @ $153.2050018310547 → cash $0.0

## Recent events

- 2026-11-09T19:00:34Z dividend_cash $71.2563 → SATA daily reinvest (~0.7347 sh @ ~$96.99)
- 2026-11-09T19:00:34Z SATA mark=96.9900 {'id': 'PB-SATA-7', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 0.7347149352461123, 'price': 96.98999786376953, 'cost': 71.26}
- 2026-11-09T19:16:20Z TEXT queued BB-NVDA-1 BUY_BEST NVDA $50000.0
- 2026-11-09T19:16:20Z TEXT queued BB-MRVL-1 BUY_BEST MRVL $50000.0
- 2026-11-09T19:16:57Z NVDA mark=176.0621 {'id': 'BB-NVDA-1', 'symbol': 'NVDA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 283.9907002752373, 'price': 176.06210327148438, 'cost': 50000.0}
- 2026-11-09T19:16:57Z NVDA attached TS-NVDA-1 PENDING_ARM arm=177.8227
- 2026-11-09T19:16:57Z NVDA no hard stop (Rodney DCA / no_hard_stop) group=BB-NVDA-1
- 2026-11-09T19:16:57Z MRVL mark=153.2050 {'id': 'BB-MRVL-1', 'symbol': 'MRVL', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 326.360101840128, 'price': 153.2050018310547, 'cost': 50000.0}
- 2026-11-09T19:16:57Z MRVL attached TS-MRVL-1 PENDING_ARM arm=154.7371
- 2026-11-09T19:16:57Z MRVL no hard stop (Rodney DCA / no_hard_stop) group=BB-MRVL-1
- 2026-11-09T19:16:57Z NVDA mark=176.0621 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'PENDING_ARM'}
- 2026-11-09T19:16:57Z MRVL mark=153.2050 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
