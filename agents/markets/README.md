# Markets workspace

Research notes and **paper** (simulated) trading for John → **Markets Department** (`markets`).

| Path | Purpose |
| --- | --- |
| `paper-portfolio.md` | Virtual cash, positions, trade log |
| `notes/` | Optional thesis / research notes (create as needed) |

Live trading is out of scope until Rodney explicitly upgrades and connects a broker with per-trade approval.

## Near-live marks

```bash
python3 agents/markets/mark_to_market.py
```

Polls Yahoo Finance 1m charts for UXRP, GDXU, SATA, BTC-USD, XRP-USD. Updates `paper-state.json`, `last_marks.json`, and `paper-portfolio.md`. A Cloud Agent timer runs this about every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET). Outside that window the script exits without fetching (`--force` overrides).
