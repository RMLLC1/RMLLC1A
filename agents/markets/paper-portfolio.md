# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-27T16:10:48Z  
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
- BTC-USD: **$59952.2617** (yahoo_v8_chart_1m)
- GDXU: **$56.3800** (yahoo_v8_chart_1m)
- MRVL: **$137.8000** (yahoo_v8_chart_1m)
- NVDA: **$148.0450** (yahoo_v8_chart_1m)
- SATA: **$91.4469** (yahoo_v8_chart_1m)
- SOL-USD: **$72.1000** (yahoo_v8_chart_1m)
- UXRP: **$6.3701** (yahoo_v8_chart_1m)
- XRP-USD: **$0.9495** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| GDXU | LONG | 1993.9821 | 48.7700 | 97,246.51 | 56.3800 | 15,174.21 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| PB-SATA-3 | SATA | BUY_BEST | **UNWOUND** | Buy $8664.03 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:30:59Z per Rodney (paper rewind profit→SATA after HS). UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-4 | SATA | BUY_BEST | **UNWOUND** | Buy $8621.96 SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell. UNWOUND 2026-11-04T10:31:45Z paper rewind (do not re-fire). |
| PB-SATA-10 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.76 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| PB-SATA-11 | SATA | BUY_BEST | **UNWOUND** | Reinvest $24.77 SATA dividend cash (daily). HOLD for daily dividends — do not sell. UNWOUND 2026-11-10T00:06:10Z — reverse duplicate/early dividend reinvest (Nov9 already credited; UTC/NY date bug). |
| TS-GDXU-8 | GDXU | TRAILING_STOP_LIMIT_SELL | **ARMED** | Arm → $56.00 (Rodney 2026-11-27: arm at current price; was $70.00). Trail widened 0.5% → 5.0% per Rodney 2026-11-27 (market sell on reverse). (group BB-GDXU-4) |

## Trade log (buys/sells)

- 2026-11-11T21:25:07Z **COVER_MARKET** GDXU qty=583.4305925377931 @ $83.11 → cash $91511.08
- 2026-11-11T21:25:07Z **BUY** SATA qty=15.53809768637532 @ $97.25 → cash $90000.0
- 2026-11-14T14:15:19Z **BUY** SOL qty=667.3785534170665 @ $74.91999816894531 → cash $0.0
- 2026-11-16T20:57:55Z **SELL** SATA qty=252.2191680112639 @ $94.87999725341797 → cash $23930.55
- 2026-11-16T20:58:24Z **BUY** GDXU qty=373.5646411492827 @ $64.05999755859375 → cash $0.0
- 2026-11-17T15:00:26Z **SELL_MARKET** GDXU qty=373.5646411492827 @ $67.25 → cash $25122.22
- 2026-11-17T15:00:26Z **BUY** SATA qty=13.488643749548233 @ $95.0999984741211 → cash $23930.55
- 2026-11-17T15:00:59Z **BUY** SATA qty=251.6356507251896 @ $95.0999984741211 → cash $0.0
- 2026-11-23T14:10:20Z **SELL_MARKET** SOL qty=667.3785534170665 @ $75.47000122070312 → cash $50367.06
- 2026-11-23T14:10:20Z **BUY** SATA qty=5.294893284165829 @ $89.49 → cash $50000.0
- 2026-11-23T16:36:15Z **SELL** SATA qty=522.6383557701675 @ $90.4000015258789 → cash $97246.51
- 2026-11-23T16:36:23Z **BUY** GDXU qty=1993.9821424487884 @ $48.77000045776367 → cash $0.0

## Recent events

- 2026-11-27T15:35:29Z GDXU mark=56.2299 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T15:41:00Z GDXU mark=56.3011 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T15:45:41Z GDXU mark=56.3050 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T15:50:30Z GDXU mark=56.0873 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T15:55:37Z GDXU mark=55.8200 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T16:00:31Z GDXU mark=56.4855 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T16:00:58Z GDXU mark=56.3600 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T16:05:23Z GDXU mark=56.1900 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T16:05:51Z GDXU mark=56.0000 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-11-27T16:05:56Z GDXU mark=56.0000 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'ARMED', 'high_water': 56.0, 'stop': 55.72}
- 2026-11-27T16:10:41Z GDXU mark=56.3800 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'TRAILED', 'high_water': 56.380001068115234, 'stop': 56.0981}
- 2026-11-27T16:10:48Z GDXU mark=56.3800 {'id': 'TS-GDXU-8', 'symbol': 'GDXU', 'event': 'ARMED_HOLD', 'stop': 53.561}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
