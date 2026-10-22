# TradingView Pine scripts (daily)

Rodney prefers **daily (1D)** charts, often **multi-year** lookback.

## Chart checklist (Rodney)

Support/resistance · parallel channels · Fibonacci · Bollinger Bands · MFI · RSI  

Details: `../rodney-chart-method.md`

## Scripts

| File | Pane | Purpose |
| --- | --- | --- |
| `rmllc-chart-toolkit-daily.pine` | Overlay | Multi-year Fib + Bollinger; reminder to draw S/R & channels |
| `rmllc-rsi-mfi-daily.pine` | Below | RSI + MFI for entry timing |
| `rmllc-exits-daily.pine` | Overlay strategy | Exit stack: hard −2% / +1% arm / 0.5% trail / ⅓@+2% + ⅓@+5% |

## How to set up (TradingView Business)

1. Symbol on **1D**, zoom out several years.  
2. Add **toolkit** + **RSI/MFI** scripts from Pine Editor.  
3. Draw **S/R** and **parallel channels** (manual or AI Copilot).  
4. Optionally add **exits** strategy for Strategy Tester.  
5. Entries: wait for level confluence (S/R / channel / Fib) **and** RSI/MFI timing — don’t chase mid-band with hot oscillators.

Paper book on John Cloud still uses Yahoo marks + standing exits; these scripts are for **chart review / backtests**, not live broker orders.
