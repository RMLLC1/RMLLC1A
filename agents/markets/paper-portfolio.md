# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-10T23:26:33Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 100,000.00  
**Dividend cash (SATA collected):** 0.0000  
**Dividends earned total (running):** 176.5480  
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
- BTC-USD: **$73613.3984** (yahoo_v8_chart_1m)
- GDXU: **$88.1588** (yahoo_v8_chart_1m)
- MRVL: **$156.4872** (yahoo_v8_chart_1m)
- NVDA: **$169.9000** (yahoo_v8_chart_1m)
- SATA: **$97.1400** (yahoo_v8_chart_1m)
- UXRP: **$8.1300** (yahoo_v8_chart_1m)
- XRP-USD: **$1.0556** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | LONG | 4920.0492 | 8.1300 | 40,000.00 | 8.1300 | 0.00 |
| GDXU | SHORT | 583.4306 | 85.7000 | 50,000.00 | 88.1588 | -1,434.54 |
| SATA | LONG | 480.0645 | 97.8466 | 46,972.67 | 97.1400 | -339.21 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-10 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.76 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| PB-SATA-11 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.77 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| TSC-GDXU-1 | GDXU | TRAILING_STOP_LIMIT_COVER | **PENDING_ARM** | Arm −3% → $83.129. Trail 0.5% → market cover on reverse up. (group SHB-GDXU-1) |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $8.2926. Trail 0.5% → market sell on reverse. (group BB-UXRP-1) |

## Trade log (buys/sells)

- 2026-11-04T22:10:07Z **SELL_MARKET** GDXU qty=701.0582339319045 @ $81.5 → cash $207136.25
- 2026-11-04T22:10:07Z **BUY** SATA qty=73.16979390956628 @ $97.53 → cash $200000.0
- 2026-11-09T19:00:34Z **BUY** SATA qty=0.7347149352461123 @ $96.98999786376953 → cash $100000.0
- 2026-11-09T19:16:57Z **BUY** NVDA qty=283.9907002752373 @ $176.06210327148438 → cash $50000.0
- 2026-11-09T19:16:57Z **BUY** MRVL qty=326.360101840128 @ $153.2050018310547 → cash $0.0
- 2026-11-09T22:15:21Z **SELL_MARKET** MRVL qty=326.360101840128 @ $156.44 → cash $51055.77
- 2026-11-09T22:15:21Z **BUY** SATA qty=10.873017507723997 @ $97.1 → cash $50000.0
- 2026-11-09T23:00:11Z **SELL_MARKET** NVDA qty=283.9907002752373 @ $178.7768 → cash $100770.95
- 2026-11-09T23:00:11Z **BUY** SATA qty=7.890992835209826 @ $97.7 → cash $100000.0
- 2026-11-10T09:00:14Z **BUY** SATA qty=0.25324741740820295 @ $97.77 → cash $100000.0
- 2026-11-10T17:11:03Z **SHORT** GDXU qty=583.4305925377931 @ $85.69999694824219 → cash $150000.0
- 2026-11-10T23:25:51Z **BUY** UXRP qty=4920.049200492004 @ $8.13 → cash $100000.0

## Recent events

- 2026-11-10T23:10:17Z GDXU mark=87.0000 {'id': 'TSC-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-10T23:15:14Z GDXU mark=87.0000 {'id': 'TSC-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-10T23:20:20Z GDXU mark=87.0000 {'id': 'TSC-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-10T23:25:23Z GDXU mark=87.3575 {'id': 'TSC-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-10T23:25:44Z TEXT queued BB-UXRP-1 BUY_BEST UXRP $40000.0
- 2026-11-10T23:25:51Z GDXU mark=87.3575 {'id': 'TSC-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-10T23:25:51Z UXRP mark=8.1300 {'id': 'BB-UXRP-1', 'symbol': 'UXRP', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 4920.049200492004, 'price': 8.13, 'cost': 40000.0}
- 2026-11-10T23:25:51Z UXRP attached TS-UXRP-1 PENDING_ARM arm=8.2926
- 2026-11-10T23:25:51Z UXRP no hard stop (Rodney DCA / no_hard_stop) group=BB-UXRP-1
- 2026-11-10T23:25:51Z UXRP STALE_QUOTE age=1296s mark=8.13 — order logic skipped
- 2026-11-10T23:26:33Z GDXU mark=88.1588 {'id': 'TSC-GDXU-1', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-10T23:26:33Z UXRP STALE_QUOTE age=1337s mark=8.13 — order logic skipped

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
