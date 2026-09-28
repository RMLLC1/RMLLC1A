# Paper portfolio (SIMULATED — not real money)

**Updated:** 2026-09-28T12:52:51Z  
**Base currency:** USD  
**Starting cash:** 100,000.00  
**Cash:** 0.00  
**Dividend cash (SATA collected):** 0.0917  
**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  
**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  
**Email:** only on buy/sell fills — never on mark/price updates  

### Standing fill rule (Rodney)

- **Buys:** best (lowest) available valid quote.
- **Sells:** best (highest) available valid quote.
- **Stop exits:** arm **+2%** from fill, then trail **1%** — **LIMIT** at stop (or better).
- Open paper orders auto-fill when conditions hit (no manual confirm).
- **Profits → SATA:** realized trading profit buys **SATA** at best price; **hold for daily dividends — do not sell**.

**Marks:**
- UXRP: **$17.8300** (yahoo_v8_chart_1m)
- GDXU: **$109.4900** (yahoo_v8_chart_1m)
- SATA: **$99.9700** (yahoo_v8_chart_1m)
- BTC-USD: **$83474.8125** (yahoo_v8_chart_1m)
- XRP-USD: **$1.5222** (yahoo_v8_chart_1m)

## Positions

| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |
| --- | ---: | ---: | ---: | ---: | ---: |
| UXRP | 1739.1304 | 17.2500 | 30,000.00 | 17.8300 | 1,008.70 |
| GDXU | 639.0576 | 109.5363 | 70,000.00 | 109.4900 | -29.59 |
| SATA | 1.7778 | 99.9700 | 177.73 | 99.9700 | 0.00 |

## Open orders (PAPER)

| ID | Symbol | Type | Status | Params |
| --- | --- | --- | --- | --- |
| TS-UXRP-1 | UXRP | TRAILING_STOP_LIMIT_SELL | **ARMED** | Arm +2% → $17.595. Trail 1% after armed. LIMIT sell at stop. |
| TS-GDXU-2 | GDXU | TRAILING_STOP_LIMIT_SELL | **PENDING_ARM** | Arm +2% → $111.727. Trail 1% after armed. LIMIT sell at stop. |

## Trade log (buys/sells)

- 2026-09-28T00:00:00Z **BUY** UXRP qty=1739.1304 @ $17.25 → cash $70000.0
- 2026-09-28T00:00:00Z **BUY** GDXU qty=275.558 @ $108.87 → cash $40000.0
- 2026-09-28T12:33:13Z **SELL_LIMIT** GDXU qty=275.558 @ $109.515 → cash $70177.73
- 2026-09-28T12:39:35Z **BUY** GDXU qty=639.0575544362919 @ $109.5363 → cash $177.73
- 2026-09-28T12:52:51Z **BUY** SATA qty=1.7778333500050014 @ $99.97 → cash $0.0

## Recent events

- 2026-09-28T12:47:16Z UXRP STALE_QUOTE age=1454s mark=17.83 — order logic skipped
- 2026-09-28T12:47:16Z GDXU mark=109.9480 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:48:19Z UXRP STALE_QUOTE age=1516s mark=17.83 — order logic skipped
- 2026-09-28T12:48:19Z GDXU mark=109.4040 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:49:22Z UXRP STALE_QUOTE age=1579s mark=17.83 — order logic skipped
- 2026-09-28T12:49:22Z GDXU mark=109.6440 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:50:25Z UXRP STALE_QUOTE age=1642s mark=17.83 — order logic skipped
- 2026-09-28T12:50:25Z GDXU mark=109.3158 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:52:51Z UXRP STALE_QUOTE age=1788s mark=17.83 — order logic skipped
- 2026-09-28T12:52:51Z GDXU mark=109.4900 {'id': 'TS-GDXU-2', 'symbol': 'GDXU', 'event': 'PENDING_ARM'}
- 2026-09-28T12:52:51Z SATA mark=99.9700 {'id': 'PB-SATA-1', 'symbol': 'SATA', 'event': 'FILLED_BUY', 'side': 'BUY', 'qty': 1.7778333500050014, 'price': 99.97, 'cost': 177.73}
- 2026-09-28T12:52:51Z SATA DIVIDEND paper $0.0917 (1.7778 × $0.0516) → dividend_cash

## Rules

- Simulated only. Not advice.
- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.
- **Do not email** on price/mark updates — email only when a buy or sell fills.
