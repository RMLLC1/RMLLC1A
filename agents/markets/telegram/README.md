# Telegram ↔ John Cloud

Message **John Cloud** on Telegram for paper trading commands and short questions.

Fills still email Gmail only (with balances). Telegram is for inbound chat + trade commands.

## One-time setup (Rodney)

1. In Telegram, open **@BotFather** → `/newbot` (or use your existing bot).
2. Copy the **bot token**.
3. Add Cloud Agent secret **`TELEGRAM_BOT_TOKEN`** = that token  
   (Cursor Dashboard → Cloud Agents → this environment → Secrets).
4. Optional but recommended: also set **`TELEGRAM_CHAT_ID`** to your numeric chat id  
   (after you message the bot once, Cloud can lock the first chat automatically).
5. Open your bot in Telegram → tap **Start** → send `STATUS`.
6. Tell John Cloud “Telegram secret is set” so he can start the poll timer.

## Commands (same as iMessage / John Mac)

| Text | Effect |
| --- | --- |
| `BUY UXRP $50000 LIMIT 17` | Limit buy + standard exits (hard −2%; +1% arm / 0.5% trail market; ⅓@+2% + ⅓@+5%) |
| `BUY UXRP $10000 BEST` | Buy at best |
| `SELL UXRP ALL BEST` | Sell all at best |
| `CANCEL LB-UXRP-4` | Cancel order |
| `STATUS` | Short how-to / book pointer |

Freeform texts (not BUY/SELL/CANCEL/STATUS) go to John Cloud’s inbox; he replies on the next Telegram poll cycle.

## Files (local / gitignored)

| Path | Role |
| --- | --- |
| `state.json` | Update offset + locked chat id |
| `inbox.jsonl` | Inbound messages log |

## Scripts

```bash
python3 agents/markets/telegram_bridge.py whoami
python3 agents/markets/telegram_bridge.py poll
python3 agents/markets/telegram_bridge.py send "Hello from John Cloud"
```

Trade queues use `queue_text_order.py --no-git` (Cloud disk only — no GitHub push emails).
