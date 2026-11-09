# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-09T20:00:40Z  
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
- BTC-USD: **$74813.3281** (yahoo_v8_chart_1m)
- GDXU: **$105.1000** (yahoo_v8_chart_1m)
- MRVL: **$153.6800** (yahoo_v8_chart_1m)
- NVDA: **$177.2200** (yahoo_v8_chart_1m)
- SATA: **$97.4450** (yahoo_v8_chart_1m)
- UXRP: **$8.6776** (yahoo_v8_chart_1m)
- XRP-USD: **$1.0931** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SATA | LONG | 461.0472 | 97.8667 | 45,121.19 | 97.4450 | -194.44 |
| NVDA | LONG | 283.9907 | 176.0621 | 50,000.00 | 177.2200 | 328.83 |
| MRVL | LONG | 326.3601 | 153.2050 | 50,000.00 | 153.6800 | 155.02 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| TS-NVDA-1 | NVDA | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm → $179.5833. Trail 0.5% → market sell on reverse. (group BB-NVDA-1; NO hard stop; NO scale-outs; arm +2% per Rodney 2026-11-09) |
| TS-MRVL-1 | MRVL | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm → $156.2691. Trail 0.5% → market sell on reverse. (group BB-MRVL-1; NO hard stop; NO scale-outs; arm +2% per Rodney 2026-11-09) |

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

- 2026-11-09T19:40:15Z MRVL mark=154.5700 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}
- 2026-11-09T19:45:23Z NVDA mark=176.6300 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'PENDING_ARM'}
- 2026-11-09T19:45:23Z MRVL mark=153.9100 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}
- 2026-11-09T19:50:24Z NVDA mark=176.7300 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'PENDING_ARM'}
- 2026-11-09T19:50:24Z MRVL mark=153.5750 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}
- 2026-11-09T19:55:09Z NVDA mark=176.6200 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'PENDING_ARM'}
- 2026-11-09T19:55:09Z MRVL mark=153.1990 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}
- 2026-11-09T20:00:10Z NVDA mark=177.0800 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'PENDING_ARM'}
- 2026-11-09T20:00:10Z MRVL mark=153.3201 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}
- 2026-11-09T20:00:25Z WATCHLIST set always=['GDXU', 'UXRP', 'SATA'] + open positions ['MRVL', 'NVDA', 'SATA']; monitor every 5m in NYSE extended hours
- 2026-11-09T20:00:40Z NVDA mark=177.2200 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'PENDING_ARM'}
- 2026-11-09T20:00:40Z MRVL mark=153.6800 {'id': 'TS-MRVL-1', 'symbol': 'MRVL', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
