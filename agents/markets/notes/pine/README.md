# TradingView Pine scripts (daily)

Rodney prefers **daily** timeframes for chart review.

| File | Purpose |
| --- | --- |
| `rmllc-exits-daily.pine` | Strategy Tester stack: hard **−2%** until arm; arm **+2%** / trail **1%**; scale-out **⅓ at +4%** |

## How to run (TradingView Business)

1. Open the symbol (e.g. `UXRP`) on a **1D** chart.
2. Pine Editor → New blank indicator/strategy → paste the `.pine` file → Add to chart.
3. Open **Strategy Tester** below the chart; tweak inputs / entry rule as needed.
4. Optional: use TradingView **AI Copilot** to refine the entry theory; keep the exit stack unless you ask John to change paper rules.

Paper book on John Cloud still uses Yahoo marks + your standing exits — this Pine file is for **chart backtests**, not live broker orders.
