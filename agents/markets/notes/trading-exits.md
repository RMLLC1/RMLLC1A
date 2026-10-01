# Trading exit rules (active book)

**As of:** 2026-09-30  
**Chart review preference (Rodney 2026-10-01):** **daily (1D)** TradingView, multi-year lookback — S/R, parallel channels, Fib, Bollinger, MFI, RSI (`rodney-chart-method.md`).  
**Applies to:** UXRP, GDXU, and other non-SATA paper trades with `attach_trailing_stop`  
**Does not apply to:** income SATA (~$8k dividend sleeve)  
**TradingView:** `pine/rmllc-chart-toolkit-daily.pine`, `pine/rmllc-rsi-mfi-daily.pine`, `pine/rmllc-exits-daily.pine`

## Stack (per entry)

1. **Hard invalidation:** LIMIT sell at **entry − 2%** until the trailing stop arms, then cancel.
2. **Trail:** arm at **entry + 2%**, then trail **1%** below high water — LIMIT at stop.
3. **Scale-out:** LIMIT sell **⅓** of the entry qty at **entry + 4%**; remaining **⅔** stay on the trail.
4. **Profits → SATA:** realized trading P&amp;L buys SATA and holds for dividends (not stop-managed).

## Income sleeve

- Keep dividend / long-hold SATA on `hold_for_dividends` / `no_sell`.
- No hard stops, trails, or scale-outs on that sleeve unless Rodney overrides.
