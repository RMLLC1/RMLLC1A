# Markets workspace

Research notes and **paper** (simulated) trading for John → **Markets Department** (`markets`).

| Path | Purpose |
| --- | --- |
| `trading-rules.md` | **Canonical paper rules** for John Cloud + John Mac (exits, SATA, text commands) |
| `paper-portfolio.md` | Virtual cash, positions, trade log (**local only / gitignored**) |
| `paper-state.json` / `last_marks.json` | Live paper book + marks (**local only / gitignored**) |
| `text-orders/` | iMessage → John Mac queue → John Cloud applies (see `text-orders/README.md`) |
| `queue_text_order.py` | Mac: parse/queue/push a text command |
| `apply_text_orders.py` | Cloud: pull pending and apply into `paper-state.json` |
| `notes/` | Thesis / research notes |
| `notes/gareth-soloway/` | Living knowledge base from Soloway’s YouTube (framework, levels, digests) |

Live trading is out of scope until Rodney explicitly upgrades and connects a broker with per-trade approval.

**Text trading:** Rodney may iMessage John Mac with BUY/SELL/CANCEL commands. Mac queues under `text-orders/pending/` (git). Cloud’s 5m marks run applies them into local paper state. Fills still email only.

## Near-live marks

```bash
python3 agents/markets/mark_to_market.py
```

Polls Yahoo Finance 1m charts for UXRP, GDXU, SATA, BTC-USD, XRP-USD. Updates `paper-state.json`, `last_marks.json`, and `paper-portfolio.md`. A Cloud Agent timer runs this about every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET). Outside that window the script exits without fetching (`--force` overrides).
