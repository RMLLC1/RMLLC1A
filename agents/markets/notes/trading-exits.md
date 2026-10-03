# Trading exit rules (active book)

**As of:** 2026-10-02  
**Chart review preference (Rodney 2026-10-01):** **daily (1D)** TradingView, multi-year lookback — S/R, parallel channels, Fib, Bollinger, MFI, RSI (`rodney-chart-method.md`).  
**Applies to:** UXRP, GDXU, and other non-SATA paper trades with `attach_trailing_stop`  
**Does not apply to:** income SATA (~$8k dividend sleeve)  
**TradingView:** `pine/rmllc-chart-toolkit-daily.pine`, `pine/rmllc-rsi-mfi-daily.pine`, `pine/rmllc-exits-daily.pine`

## Stack (per entry)

1. **Hard invalidation:** LIMIT sell at **entry − 2%** until the trailing stop arms, then cancel (**UXRP: −3%**; **GDXU: −4.5%**).
2. **Trail:** default arm at **entry + 1%**, then trail **0.5%** below high water — **market sell** remainder on reverse. **UXRP/GDXU:** trail waits until **2nd scale-out fills**, then arms at mark with **0.5%** HWM trail.
3. **Scale-out:** LIMIT sell **⅓** at **entry + 2%**, then **⅓** at **entry + 5%** (**GDXU: ⅓@+3% + ⅓@+7%**); remaining **⅓** stays on the trail.
4. **After 1st scale-out:** raise hard stop to **entry (breakeven)** on the remaining size.
5. **Profits → SATA:** realized trading P&amp;L buys SATA and holds for dividends (not stop-managed). Reinvest `dividend_cash` when ≥1 share; otherwise merge into the next profit→SATA buy.

## Short stack (mirrored)

Per short entry (`attach_trading_exits_short`):

1. **Hard invalidation:** LIMIT cover at **entry + 2%** until trail arms, then cancel (**UXRP: +3%**; **GDXU: +4.5%**).
2. **Trail:** default arm at **entry − 1%**, then trail **0.5%** above low water — **market cover** on reverse up. **UXRP/GDXU:** trail waits until **2nd scale-out fills**, then arms at mark with **0.5%** LWM trail.
3. **Scale-out:** LIMIT cover **⅓** at **entry − 2%**, then **⅓** at **entry − 5%** (**GDXU: ⅓@−3% + ⅓@−7%**); remaining **⅓** stays on trail.
4. **After 1st scale-out:** lower hard cover stop to **entry (breakeven)** on remaining size.

## Income sleeve

- Keep dividend / long-hold SATA on `hold_for_dividends` / `no_sell`.
- No hard stops, trails, or scale-outs on that sleeve unless Rodney overrides.
- **SHORT/COVER blocked** on SATA.
