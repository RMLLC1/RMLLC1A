# Markets workspace

Research notes and **paper** (simulated) trading for John → `markets` specialist.

| Path | Purpose |
| --- | --- |
| `paper-portfolio.md` | Virtual cash, positions, trade log |
| `notes/` | Optional thesis / research notes (create as needed) |

Live trading is out of scope until Rodney explicitly upgrades and connects a broker with per-trade approval.

## Near-live marks

```bash
python3 agents/markets/mark_to_market.py
```

Polls Yahoo Finance 1m charts for UXRP, GDXU, BTC-USD, XRP-USD. Updates `paper-state.json`, `last_marks.json`, and `paper-portfolio.md`. A Cloud Agent timer can run this about every 60 seconds.
