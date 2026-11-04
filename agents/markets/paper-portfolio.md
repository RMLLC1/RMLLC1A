# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-11-04T00:55:21Z  
**Base currency:** USD  
**Starting cash:** 200,000.00  
**Cash:** 50,000.00  
**Dividend cash (SATA collected):** 93.9556  
**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  
**Notify:** Gmail + Telegram on buy/sell fills (with balances) — never on mark/price updates  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Trading exits:** default hard **−2%** / arm **+1%** / trail **0.5%** market / scale **⅓@+2%** + **⅓@+5%**. **UXRP:** hard **−3%** / arm **+2%** / trail **0.5%**. **GDXU:** hard **−4.5%** / arm **+3%** / trail **0.5%** / scale **⅓@+3%** + **⅓@+7%**.
- **Income SATA (~dividends sleeve):** no stops / no scale-outs / no sells unless Rodney overrides.
- Open paper orders auto-fill when conditions hit (no manual confirm).
- **Profits → SATA:** realized **trading** profit buys **SATA** at best; **dividend_cash** reinvests when ≥1 share, else merges into the next profit→SATA buy.
- **Hold for daily dividends — do not sell** income SATA unless Rodney overrides.

**Marks:**
- UXRP: **$11.5900** (yahoo_v8_chart_1m)
- GDXU: **$65.0000** (yahoo_v8_chart_1m)
- SATA: **$95.6000** (yahoo_v8_chart_1m)
- BTC-USD: **$77040.8516** (yahoo_v8_chart_1m)
- XRP-USD: **$1.2581** (yahoo_v8_chart_1m)

## Positions

| Symbol | Side | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| GDXU | LONG | 2103.1747 | 71.3208 | 150,000.00 | 65.0000 | -13,293.64 |
| SATA | LONG | 260.1208 | 98.1514 | 25,531.22 | 95.6000 | -663.67 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| SO-GDXU-30 | GDXU | LIMIT_SELL | **OPEN** | Scale-out 33% at +7% → $86.8091 LIMIT. (group LB-GDXU-6; ⅓ at +3%, ⅓ at +7%) |
| TS-GDXU-11 | GDXU | TRAILING_STOP_LIMIT_SELL | **WAITING_SCALE** | Trail 0.5% market arms only after scale-out #2 fills. (group LB-GDXU-6) |
| TS-GDXU-2 | GDXU | TRAILING_STOP_LIMIT_SELL | **WAITING_SCALE** | Trail 0.5% market arms only after scale-out #2 fills. (group BB-GDXU-1) |
| HS-GDXU-2 | GDXU | HARD_STOP_LIMIT_SELL | **OPEN** | Hard invalidation −4% → $61.9127 LIMIT until trail arms. (group BB-GDXU-1) |
| SO-GDXU-3 | GDXU | LIMIT_SELL | **OPEN** | Scale-out 33% at +3% → $66.7749 LIMIT. (group BB-GDXU-1; ⅓ at +3%, ⅓ at +7%) |
| SO-GDXU-4 | GDXU | LIMIT_SELL | **OPEN** | Scale-out 33% at +7% → $69.3681 LIMIT. (group BB-GDXU-1; ⅓ at +3%, ⅓ at +7%) |
| TS-GDXU-3 | GDXU | TRAILING_STOP_LIMIT_SELL | **WAITING_SCALE** | Trail 0.5% market arms only after scale-out #2 fills. (group BB-GDXU-2) |
| HS-GDXU-3 | GDXU | HARD_STOP_LIMIT_SELL | **OPEN** | Hard invalidation −4% → $62.2326 LIMIT until trail arms. (group BB-GDXU-2) |
| SO-GDXU-5 | GDXU | LIMIT_SELL | **OPEN** | Scale-out 33% at +3% → $67.12 LIMIT. (group BB-GDXU-2; ⅓ at +3%, ⅓ at +7%) |
| SO-GDXU-6 | GDXU | LIMIT_SELL | **OPEN** | Scale-out 33% at +7% → $69.7266 LIMIT. (group BB-GDXU-2; ⅓ at +3%, ⅓ at +7%) |

## Trade log (buys/sells)

- 2026-10-22T14:43:25Z **BUY** GDXU qty=1232.5897126267564 @ $81.12999725341797 → cash $100000.0
- 2026-10-28T19:58:08Z **SELL_LIMIT** GDXU qty=410.86323754225214 @ $84.26000213623047 → cash $134708.22
- 2026-10-28T19:58:08Z **BUY** SATA qty=14.042385339344797 @ $97.91000366210938 → cash $133333.33
- 2026-11-03T19:25:52Z **BUY** GDXU qty=514.1651867736454 @ $64.83000183105469 → cash $100000.0
- 2026-11-03T19:30:23Z **BUY** GDXU qty=767.2830399375646 @ $65.16500091552734 → cash $50000.0

## Recent events

- 2026-11-04T00:50:17Z GDXU mark=64.9896 {'id': 'SO-GDXU-3', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 66.7749}
- 2026-11-04T00:50:17Z GDXU mark=64.9896 {'id': 'SO-GDXU-4', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 69.3681}
- 2026-11-04T00:50:17Z GDXU mark=64.9896 {'id': 'HS-GDXU-3', 'symbol': 'GDXU', 'event': 'HARD_STOP_HOLD', 'stop': 62.2326}
- 2026-11-04T00:50:17Z GDXU mark=64.9896 {'id': 'SO-GDXU-5', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 67.12}
- 2026-11-04T00:50:17Z GDXU mark=64.9896 {'id': 'SO-GDXU-6', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 69.7266}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'SO-GDXU-30', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 86.8091}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'HS-GDXU-2', 'symbol': 'GDXU', 'event': 'HARD_STOP_HOLD', 'stop': 61.9127}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'SO-GDXU-3', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 66.7749}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'SO-GDXU-4', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 69.3681}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'HS-GDXU-3', 'symbol': 'GDXU', 'event': 'HARD_STOP_HOLD', 'stop': 62.2326}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'SO-GDXU-5', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 67.12}
- 2026-11-04T00:55:21Z GDXU mark=65.0000 {'id': 'SO-GDXU-6', 'symbol': 'GDXU', 'event': 'WORKING_SELL', 'limit': 69.7266}

## Rules

- Simulated only. Not advice.
- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).
- **Do not email** on price/mark updates — email only when a buy or sell fills.
