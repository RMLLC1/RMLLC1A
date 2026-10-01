# Text orders (iMessage → John Mac → John Cloud paper)

Rodney texts **John Mac**; Mac queues a paper order here; **John Cloud** applies it on the next marks cycle (~5 minutes during NYSE extended hours; cancels/queues apply anytime).

## Allowed sender

Only Rodney’s iMessage number ending in **8173715555**.

## Commands (examples)

| Text | Effect |
| --- | --- |
| `BUY UXRP $50000 LIMIT 17` | Limit buy $50k notional at $17 or better + standard exits |
| `BUY GDXU 50k LIMIT 107.5` | Same |
| `BUY UXRP $10000 BEST` | Buy at best available |
| `SELL UXRP ALL BEST` | Sell full position at best |
| `SELL GDXU ALL LIMIT 111` | Limit sell all at $111 |
| `SELL UXRP QTY 100 LIMIT 18` | Limit sell 100 shares |
| `CANCEL LB-UXRP-4` | Cancel that order id |
| `CANCEL BUYS UXRP` | Cancel open/working limit buys for UXRP |
| `STATUS` | Mac replies that book is on Cloud; check Gmail fills / Cursor |

SATA sells stay blocked unless the order includes an explicit override (not available by default text).

Default exits on new buys (non-SATA): hard −2%, arm +2% / trail 1%, scale-out ⅓ at +4%.

## Files

| Path | Role |
| --- | --- |
| `pending/*.json` | Queued by Mac (`queue_text_order.py`); committed to git |
| `processed/*.json` | Moved here by Cloud after apply |
| `outbox/*.json` | Optional short status notes for Mac |

Paper `paper-state.json` stays **local on Cloud** (not committed).
