# Rodney chart method (standing)

**Updated:** 2026-10-01  
**Primary chart:** TradingView **daily (1D)**  
**Lookback:** typically **several years** on the same daily chart  

## What he draws / checks

1. **Support & resistance** — multi-year swing highs/lows and prior reaction zones  
2. **Parallel channels** — rising/falling structure containing price  
3. **Fibonacci** — retracements (and extensions when relevant) across the major swing  
4. **Bollinger Bands** — volatility / stretch vs mean  
5. **MFI** (Money Flow Index) — entry timing / pressure  
6. **RSI** — entry timing / overbought-oversold / divergence  

## How John / Markets should use this

- Default analysis timeframe = **1D**, multi-year context first.  
- Mention confluence: level (S/R, channel, Fib) **plus** BB / MFI / RSI timing.  
- Paper exits stay Rodney’s stack (−2% hard / +2% arm / 1% trail / ⅓@+4%) unless he changes them.  
- Soloway/VI levels are **context**, not auto-entries.  
- TradingView AI Copilot + Pine helpers under `notes/pine/` support this workflow; John cannot log into TradingView directly.

## Pine helpers

| File | Role |
| --- | --- |
| `pine/rmllc-chart-toolkit-daily.pine` | BB + multi-year Fib + RSI/MFI panels (draw S/R & channels on chart / Copilot) |
| `pine/rmllc-exits-daily.pine` | Strategy Tester exit stack |
