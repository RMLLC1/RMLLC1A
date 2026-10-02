# Trading exit rules (active book)

**As of:** 2026-10-02  
**Chart review preference (Rodney 2026-10-01):** **daily (1D)** TradingView, multi-year lookback — S/R, parallel channels, Fib, Bollinger, MFI, RSI (`rodney-chart-method.md`).  
**Applies to:** UXRP, GDXU, and other non-SATA paper trades with `attach_trailing_stop`  
**Does not apply to:** income SATA (~$8k dividend sleeve)  
**TradingView:** `pine/rmllc-chart-toolkit-daily.pine`, `pine/rmllc-rsi-mfi-daily.pine`, `pine/rmllc-exits-daily.pine`

## Stack (per entry)

1. **Hard invalidation:** LIMIT sell at **entry − 2%** until the trailing stop arms, then cancel (**UXRP: −3%**; **GDXU: −4.5%**).
2. **Trail:** arm at **entry + 1%**, then trail **0.5%** below high water — **market sell** remainder on reverse (**UXRP: arm +2% / trail 2%**; **GDXU: arm +3% / trail 3%**).
3. **Scale-out:** LIMIT sell **⅓** at **entry + 2%**, then **⅓** at **entry + 5%** (**GDXU: ⅓@+3% + ⅓@+7%**); remaining **⅓** stays on the trail.
4. **Profits → SATA:** realized trading P&amp;L buys SATA and holds for dividends (not stop-managed). Reinvest `dividend_cash` when ≥1 share; otherwise merge into the next profit→SATA buy.

## Income sleeve

- Keep dividend / long-hold SATA on `hold_for_dividends` / `no_sell`.
- No hard stops, trails, or scale-outs on that sleeve unless Rodney overrides.
