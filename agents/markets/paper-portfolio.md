# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-16T20:58:24Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 0.00  
**Dividend cash (SATA collected):** 78.0870  
**Dividends earned total (running):** 279.4063  
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
- BTC-USD: **$64891.1016** (yahoo_v8_chart_1m)
- GDXU: **$64.0600** (yahoo_v8_chart_1m)
- MRVL: **$145.4500** (yahoo_v8_chart_1m)
- NVDA: **$155.9150** (yahoo_v8_chart_1m)
- SATA: **$94.7500** (yahoo_v8_chart_1m)
- SOL: **$71.3400** (yahoo_v8_chart_1m)
- SOL-USD: **$71.3400** (yahoo_v8_chart_1m)
- UXRP: **$6.6100** (yahoo_v8_chart_1m)
- XRP-USD: **$0.9530** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| GDXU | LONG | 373.5646 | 64.0600 | 23,930.55 | 64.0600 | 0.00 |
| SATA | LONG | 252.2192 | 97.8215 | 24,672.46 | 94.7500 | -774.69 |
| SOL | LONG | 667.3786 | 74.9200 | 50,000.00 | 71.3400 | -2,389.22 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-10 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.76 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| PB-SATA-11 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.77 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| TS-SOL-1 | SOL | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +1% → $75.6692. Trail 0.5% → market sell on reverse. (group LB-SOL-1) |
| TS-GDXU-7 | GDXU | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +3% → $65.9818. Trail 0.5% → market sell on reverse. (group BB-GDXU-3) |

## Trade log (buys/sells)

- 2026-11-09T23:00:11Z **BUY** SATA qty=7.890992835209826 @ $97.7 → cash $100000.0
- 2026-11-10T09:00:14Z **BUY** SATA qty=0.25324741740820295 @ $97.77 → cash $100000.0
- 2026-11-10T17:11:03Z **SHORT** GDXU qty=583.4305925377931 @ $85.69999694824219 → cash $150000.0
- 2026-11-10T23:25:51Z **BUY** UXRP qty=4920.049200492004 @ $8.13 → cash $100000.0
- 2026-11-11T09:00:21Z **BUY** SATA qty=0.2571903229155851 @ $96.31 → cash $100000.0
- 2026-11-11T15:50:15Z **SELL_MARKET** UXRP qty=4920.049200492004 @ $8.300000190734863 → cash $140836.41
- 2026-11-11T15:50:15Z **BUY** SATA qty=8.578564102564103 @ $97.5 → cash $140000.0
- 2026-11-11T21:25:07Z **COVER_MARKET** GDXU qty=583.4305925377931 @ $83.11 → cash $91511.08
- 2026-11-11T21:25:07Z **BUY** SATA qty=15.53809768637532 @ $97.25 → cash $90000.0
- 2026-11-14T14:15:19Z **BUY** SOL qty=667.3785534170665 @ $74.91999816894531 → cash $0.0
- 2026-11-16T20:57:55Z **SELL** SATA qty=252.2191680112639 @ $94.87999725341797 → cash $23930.55
- 2026-11-16T20:58:24Z **BUY** GDXU qty=373.5646411492827 @ $64.05999755859375 → cash $0.0

## Recent events

- 2026-11-16T20:45:23Z SOL mark=71.3400 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-16T20:50:15Z SOL mark=71.4900 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-16T20:55:23Z SOL mark=71.4100 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-16T20:57:47Z TEXT queued SB-SATA-1 SELL_BEST SATA
- 2026-11-16T20:57:55Z SOL mark=71.3200 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-16T20:57:55Z SATA mark=94.8800 {'id': 'SB-SATA-1', 'symbol': 'SATA', 'event': 'FILLED_SELL', 'side': 'SELL', 'qty': 252.2191680112639, 'price': 94.87999725341797, 'proceeds': 23930.55, 'basis_released': 24672.47}
- 2026-11-16T20:58:08Z TEXT queued BB-GDXU-3 BUY_BEST GDXU $23930.55
- 2026-11-16T20:58:24Z SOL mark=71.3400 {'id': 'TS-SOL-1', 'symbol': 'SOL', 'event': 'PENDING_ARM'}
- 2026-11-16T20:58:24Z GDXU mark=64.0600 {'id': 'BB-GDXU-3', 'symbol': 'GDXU', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 373.5646411492827, 'price': 64.05999755859375, 'cost': 23930.55}
- 2026-11-16T20:58:24Z GDXU attached TS-GDXU-7 PENDING_ARM arm=65.9818
- 2026-11-16T20:58:24Z GDXU no hard stop (Rodney DCA / no_hard_stop) group=BB-GDXU-3
- 2026-11-16T20:58:24Z GDXU mark=64.0600 {'id': 'TS-GDXU-7', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
