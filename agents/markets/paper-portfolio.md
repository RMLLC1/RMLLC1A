# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-17T15:00:59Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 0.00  
**Dividend cash (SATA collected):** 0.0000  
**Dividends earned total (running):** 292.4208  
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
- BTC-USD: **$64879.9609** (yahoo_v8_chart_1m)
- GDXU: **$68.0400** (yahoo_v8_chart_1m)
- MRVL: **$147.4000** (yahoo_v8_chart_1m)
- NVDA: **$155.3100** (yahoo_v8_chart_1m)
- SATA: **$95.1000** (yahoo_v8_chart_1m)
- SOL: **$73.6100** (yahoo_v8_chart_1m)
- SOL-USD: **$73.6100** (yahoo_v8_chart_1m)
- UXRP: **$6.7901** (yahoo_v8_chart_1m)
- XRP-USD: **$0.9710** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SATA | LONG | 517.3435 | 96.4268 | 49,885.78 | 95.1000 | -686.42 |
| SOL | LONG | 667.3786 | 74.9200 | 50,000.00 | 73.6100 | -874.26 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-10 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.76 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| PB-SATA-11 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.77 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| TS-SOL-1 | SOL | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +1% → $75.6692. Trail 0.5% → market sell on reverse. (group LB-SOL-1) |

## Trade log (buys/sells)

- 2026-11-10T23:25:51Z **BUY** UXRP qty=4920.049200492004 @ $8.13 → cash $100000.0
- 2026-11-11T09:00:21Z **BUY** SATA qty=0.2571903229155851 @ $96.31 → cash $100000.0
- 2026-11-11T15:50:15Z **SELL_MARKET** UXRP qty=4920.049200492004 @ $8.300000190734863 → cash $140836.41
- 2026-11-11T15:50:15Z **BUY** SATA qty=8.578564102564103 @ $97.5 → cash $140000.0
- 2026-11-11T21:25:07Z **COVER_MARKET** GDXU qty=583.4305925377931 @ $83.11 → cash $91511.08
- 2026-11-11T21:25:07Z **BUY** SATA qty=15.53809768637532 @ $97.25 → cash $90000.0
- 2026-11-14T14:15:19Z **BUY** SOL qty=667.3785534170665 @ $74.91999816894531 → cash $0.0
- 2026-11-16T20:57:55Z **SELL** SATA qty=252.2191680112639 @ $94.87999725341797 → cash $23930.55
- 2026-11-16T20:58:24Z **BUY** GDXU qty=373.5646411492827 @ $64.05999755859375 → cash $0.0
- 2026-11-17T15:00:26Z **SELL_MARKET** GDXU qty=373.5646411492827 @ $67.25 → cash $25122.22
- 2026-11-17T15:00:26Z **BUY** SATA qty=13.488643749548233 @ $95.0999984741211 → cash $23930.55
- 2026-11-17T15:00:59Z **BUY** SATA qty=251.6356507251896 @ $95.0999984741211 → cash $0.0

## Recent events

- 2026-11-17T14:50:11Z SOL mark=73.6900 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-17T14:50:11Z GDXU mark=68.1650 {'id': 'TS-GDXU-7', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 68.16500091552734, 'stop': 67.8242}
- 2026-11-17T14:55:07Z SOL mark=73.7000 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-17T14:55:07Z GDXU mark=68.1970 {'id': 'TS-GDXU-7', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 68.1969985961914, 'stop': 67.856}
- 2026-11-17T15:00:26Z SOL mark=73.7600 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-17T15:00:26Z GDXU mark=67.2500 {'id': 'TS-GDXU-7', 'symbol': 'GDXU', 'event': 'FILLED_MARKET', 'side': 'SELL', 'limit': 67.856, 'price': 67.25, 'qty': 373.5646411492827, 'proceeds': 25122.22}
- 2026-11-17T15:00:26Z merged $91.1015 dividend_cash into profit→SATA buy (below 1-share reinvest threshold alone)
- 2026-11-17T15:00:26Z queued PB-SATA-16 $1282.77 (PROFIT_TO_SATA)
- 2026-11-17T15:00:26Z SATA mark=95.1000 {'id': 'PB-SATA-16', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 13.488643749548233, 'price': 95.0999984741211, 'cost': 1282.77}
- 2026-11-17T15:00:57Z TEXT queued BB-SATA-1 BUY_BEST SATA $23930.55
- 2026-11-17T15:00:59Z SOL mark=73.6100 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-17T15:00:59Z SATA mark=95.1000 {'id': 'BB-SATA-1', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 251.6356507251896, 'price': 95.0999984741211, 'cost': 23930.55}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
