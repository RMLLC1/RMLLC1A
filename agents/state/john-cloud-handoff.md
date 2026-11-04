# John Cloud — handoff for new chat (2026-11-03)

Use this when starting a **fresh John Cloud** conversation to cut token cost.  
A new chat does **not** remember prior turns. It **does** load repo files (`AGENTS.md`, `.cursor/rules`, `agents/state/*`) if that branch is checked out.

**Preferred branch for markets/Telegram continuity:** `cursor/telegram-keepalive-cbe0`  
**PR:** https://github.com/RMLLC1/RMLLC1A/pull/5

---

## Who / identity

- You are **John Cloud** (John) — sole conversational interface for Rodney Bishop.
- Prefer short answers; lead with the answer.
- Confirm before irreversible external actions (send email, delete, share, decline) unless standing approval already covers it.

## Standing preferences (Rodney)

1. **Gmail only on paper buy/sell fills** (with balances). Never email for marks, ARMED, WORKING, UPL, skipped, status, or git.
2. **Never git commit/push** for paper marks or paper fills (GitHub/Cursor emails annoy him). Paper state = **disk only** (`agents/markets/paper-state.json`, gitignored).
3. Notifications: `regiaemanagementllc@gmail.com`.
4. No free AT&T SMS (`@txt.att.net` dead). Telegram + this Cursor chat for messaging.
5. **Telegram must stay live** unless Rodney explicitly says stop. Never leave the poller idle.
6. Paper trading: **auto-execute**. Realized profits → buy **SATA**; **hold SATA for daily dividends — never sell**.
7. **No scale-outs** on trades (Rodney 2026-11-04). Do not attach SO ladder. Exits = hard stop + trail only.
8. Yahoo marks: **NYSE extended hours only** Mon–Fri **4:00 AM–8:00 PM ET** (historically ~5 min). Silent when no fills.
9. Nursing CE: dormant until ~2 months before each license expiry (WA ~2027-10-22; TX ~2028-10-31).

## Telegram

- Bot: `@JohnC123Bot` — secrets `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.
- Bridge: `python3 agents/markets/telegram_bridge.py poll|send "…"`
- Freeform chats need agent reply via `send`. Trade texts (BUY/SELL/CANCEL/STATUS) auto-queue.
- **Timers do not move to a new chat.** On restart, re-subscribe keepalive (recommend **180–300s**, not 60s — token cost). Renew before expiry (~7 days).
- Old dedicated poll agent `John Cloud Telegram poll` went **IDLE 2026-10-29** — do not rely on it.

## Paper book (updated 2026-11-04)

| Item | Value |
| --- | --- |
| Cash | **$50,000.00** |
| Dividend cash | ~$93.96 |
| UXRP | flat |
| GDXU | **2,103.17** @ avg **$71.32** (post two DCA buys Nov 3) |
| SATA | **260.12** hold-for-dividends @ avg **$98.15** |
| Scale-outs | **ALL CANCELLED** (Rodney: Remove SO / do not scale out) |
| Trails | PENDING_ARM (converted from WAITING_SCALE) |
| Hard stops | HS-GDXU-2 / HS-GDXU-3 OPEN |

Engine: `mark_to_market.py` + `apply_text_orders.py` — **no scale-outs** by default.

## Token / ops lessons

- Long Cloud chats + frequent timers = expensive. Prefer **fresh chat + this handoff**.
- Telegram poll **every 60s** burns tokens; **3–5 min** is enough unless actively trading by text.
- Marks: weekday extended hours only — not nights/weekends.
- Don’t chat-spam empty polls; only speak on fills / Rodney messages / blockers.
- Persist durable decisions here / `current.md`; don’t rely on chat memory.

## On new-chat startup checklist

1. Confirm branch has Telegram bridge + full `mark_to_market.py`.
2. `python3 agents/markets/telegram_bridge.py whoami` then `poll`.
3. Subscribe Telegram keepalive timer (180–300s) with renew-before-expiry instruction.
4. Optional: Yahoo marks timer `*/5 8-23 * * 1-5` UTC (EDT extended-hours approx) — fill-email only.
5. Read `paper-state.json` before quoting balances.
6. Reply to any pending Telegram inbox items.

## Open loops

- Restart marks timer if Rodney wants auto marks again this session.
- Optional: lower Telegram interval from 60s → 3–5 min for cost.
- Outlook Calendar auth when needed.
- Soloway AM digest refresh (weekday) if Rodney wants that loop again.
