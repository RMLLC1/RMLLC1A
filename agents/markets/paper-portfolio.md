# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-10T00:06:24Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 100,000.00  
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
- BTC-USD: **$75252.5781** (yahoo_v8_chart_1m)
- GDXU: **$103.5000** (yahoo_v8_chart_1m)
- MRVL: **$158.1277** (yahoo_v8_chart_1m)
- NVDA: **$181.3935** (yahoo_v8_chart_1m)
- SATA: **$97.7000** (yahoo_v8_chart_1m)
- UXRP: **$8.8044** (yahoo_v8_chart_1m)
- XRP-USD: **$1.0994** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SATA | LONG | 479.8112 | 97.8466 | 46,947.91 | 97.7000 | -70.35 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-10 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.76 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| PB-SATA-11 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.77 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |

## Trade log (buys/sells)

- 2026-11-04T10:31:45Z **UNWIND** GDXU qty=1402.1164678638092 @ $77.5 → cash $100000.0
- 2026-11-04T20:10:10Z **SELL** GDXU qty=701.0582339319047 @ $82.58000183105469 → cash $157893.39
- 2026-11-04T20:10:10Z **BUY** SATA qty=80.50782954168228 @ $98.04499816894531 → cash $150000.0
- 2026-11-04T22:10:07Z **SELL_MARKET** GDXU qty=701.0582339319045 @ $81.5 → cash $207136.25
- 2026-11-04T22:10:07Z **BUY** SATA qty=73.16979390956628 @ $97.53 → cash $200000.0
- 2026-11-09T19:00:34Z **BUY** SATA qty=0.7347149352461123 @ $96.98999786376953 → cash $100000.0
- 2026-11-09T19:16:57Z **BUY** NVDA qty=283.9907002752373 @ $176.06210327148438 → cash $50000.0
- 2026-11-09T19:16:57Z **BUY** MRVL qty=326.360101840128 @ $153.2050018310547 → cash $0.0
- 2026-11-09T22:15:21Z **SELL_MARKET** MRVL qty=326.360101840128 @ $156.44 → cash $51055.77
- 2026-11-09T22:15:21Z **BUY** SATA qty=10.873017507723997 @ $97.1 → cash $50000.0
- 2026-11-09T23:00:11Z **SELL_MARKET** NVDA qty=283.9907002752373 @ $178.7768 → cash $100770.95
- 2026-11-09T23:00:11Z **BUY** SATA qty=7.890992835209826 @ $97.7 → cash $100000.0

## Recent events

- 2026-11-09T23:00:11Z NVDA mark=178.7768 {'id': 'TS-NVDA-1', 'symbol': 'NVDA', 'event': 'FILLED_MARKET', 'side': 'SELL', 'limit': 178.7816, 'price': 178.7768, 'qty': 283.9907002752373, 'proceeds': 50770.95}
- 2026-11-09T23:00:11Z queued PB-SATA-9 $770.95 (PROFIT_TO_SATA)
- 2026-11-09T23:00:11Z SATA mark=97.7000 {'id': 'PB-SATA-9', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 7.890992835209826, 'price': 97.7, 'cost': 770.95}
- 2026-11-10T00:00:10Z SATA DIVIDEND paper $24.7583 (479.8112 × $0.0516) → dividend_cash (earned_total $176.5480)
- 2026-11-10T00:00:10Z queued PB-SATA-10 $24.76 (DIVIDEND_REINVEST)
- 2026-11-10T00:00:10Z dividend_cash $24.7583 → SATA daily reinvest (~0.2534 sh @ ~$97.70)
- 2026-11-10T00:00:10Z SATA mark=97.7000 {'id': 'PB-SATA-10', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 0.2534288638689867, 'price': 97.7, 'cost': 24.76}
- 2026-11-10T00:05:12Z SATA DIVIDEND paper $24.7713 (480.0647 × $0.0516) → dividend_cash (earned_total $201.3193)
- 2026-11-10T00:05:12Z queued PB-SATA-11 $24.77 (DIVIDEND_REINVEST)
- 2026-11-10T00:05:12Z dividend_cash $24.7713 → SATA daily reinvest (~0.2535 sh @ ~$97.70)
- 2026-11-10T00:05:12Z SATA mark=97.7000 {'id': 'PB-SATA-11', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 0.2535312180143296, 'price': 97.7, 'cost': 24.77}
- 2026-11-10T00:06:10Z REWIND duplicate/early SATA dividend reinvests PB-SATA-10/11 (−0.5070 sh, −$49.53 basis); earned_total→$151.7897; last_day=2026-11-09

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
