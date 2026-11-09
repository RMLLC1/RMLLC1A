# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-09T19:00:49Z  
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
- UXRP: **$8.5850** (yahoo_v8_chart_1m)
- GDXU: **$102.1200** (yahoo_v8_chart_1m)
- SATA: **$96.9900** (yahoo_v8_chart_1m)
- BTC-USD: **$74584.7266** (yahoo_v8_chart_1m)
- XRP-USD: **$1.0901** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SATA | LONG | 461.0472 | 97.8667 | 45,121.19 | 96.9900 | -404.22 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |

## Trade log (buys/sells)

- 2026-11-04T10:15:27Z **BUY** SATA qty=46.51403999585535 @ $96.51 → cash $100000.0
- 2026-11-04T10:21:08Z **SELL_LIMIT** GDXU qty=1402.1164678638092 @ $82.0 → cash $208664.03
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

## Recent events

- 2026-11-04T22:10:07Z GDXU mark=81.5000 {'id': 'TS-GDXU-14', 'symbol': 'GDXU', 'event': 'FILLED_MARKET', 'side': 'SELL', 'limit': 81.732, 'price': 81.5, 'qty': 701.0582339319045, 'proceeds': 57136.25}
- 2026-11-04T22:10:07Z queued PB-SATA-6 $7136.25 (PROFIT_TO_SATA)
- 2026-11-04T22:10:07Z SATA mark=97.5300 {'id': 'PB-SATA-6', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 73.16979390956628, 'price': 97.53, 'cost': 7136.25}
- 2026-11-05T00:00:11Z SATA DIVIDEND paper $23.7521 (460.3125 × $0.0516) → dividend_cash
- 2026-11-06T00:00:19Z SATA DIVIDEND paper $23.7521 (460.3125 × $0.0516) → dividend_cash
- 2026-11-09T09:00:17Z SATA DIVIDEND paper $23.7521 (460.3125 × $0.0516) → dividend_cash
- 2026-11-09T18:20:37Z CASH_SET trading cash 200000.00 → 100000.00 per Rodney (SATA + dividend_cash unchanged)
- 2026-11-09T18:31:04Z INIT dividends_earned_total=$151.7897 from dividend_log (Rodney: daily running total)
- 2026-11-09T19:00:34Z STANDING: daily_dividend_reinvest=true (any dividend_cash≥$1 → SATA)
- 2026-11-09T19:00:34Z queued PB-SATA-7 $71.26 (DIVIDEND_REINVEST)
- 2026-11-09T19:00:34Z dividend_cash $71.2563 → SATA daily reinvest (~0.7347 sh @ ~$96.99)
- 2026-11-09T19:00:34Z SATA mark=96.9900 {'id': 'PB-SATA-7', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 0.7347149352461123, 'price': 96.98999786376953, 'cost': 71.26}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
