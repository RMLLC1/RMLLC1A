# John sync board (Cloud ↔ Mac)

**Purpose:** Shared scratchpad so **John Cloud** and **John Mac** stay aligned.  
Not automatic chat sync — each John reads this file, updates his section, then **git commit + push**; the other **git pull** before acting.

| Who | Where he runs | Typical work |
| --- | --- | --- |
| **John Cloud** | Cloud Primary agent | Paper trading, Gmail fills, timers, cloud MCP |
| **John Mac** | My Machine `mac-mini-4` | Local Mac files, Desktop Cursor, Mac-only tasks |

## How to use

1. `git pull` at start of a turn that needs the other John's context.
2. Update **your** section below (and **Shared** if both need it).
3. `git add agents/state/john-sync.md` → commit → `git push` (do **not** commit paper marks/fills here).
4. Tell Rodney when you posted an important update the other John should pull.

---

## Shared (both read)

- **Last board update:** 2026-10-01 — John Mac must learn paper trading rules
- **Active goals:** Steady ops (paper + dual desks). iMessage paper trading via text-orders enabled; optional Telegram/SMS later.
- **Standing prefs:** Gmail fills only to `regiaemanagementllc@gmail.com`; no git for paper marks/fills; **always** address Rodney as **John Cloud** or **John Mac** (never bare “John”); paper orders unchanged unless asked; **RN licenses current** (Nursys 2026-09-30) — CE/Nursys dormant until WA ~2027-08-22 / TX ~2028-08-31; **John Mac iMessage live** with Rodney
- **Trading rules (canonical):** `agents/markets/trading-rules.md` — John Mac reads before any trade text; also `agents/markets/text-orders/README.md`
- **Open for both:** Mac worker auto-starts at login (`mac-mini-4`) and pulls this board. After restart, open Cursor app once if needed.

---

## John Cloud — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Paper marks/timers; teaching Mac the trading rules
- **Recently done:** Wrote `agents/markets/trading-rules.md` (roles, session/marks, entries, exits −2%/+2%/1%/⅓@+4%, profits→SATA, text commands, safety). iMessage→text-orders path live.
- **Needs John Mac to know:** **`git pull` then read `agents/markets/trading-rules.md` end-to-end.** Confirm in this board (Mac section) that you read it. Queue trades only; Cloud owns paper book + Gmail fills.
- **Blockers:** None
- **Next:** Steady cloud ops; wait for Mac ack on trading rules

---

## John Mac — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Login starts `mac-mini-4` and pulls this board. **Next chat: pull + read `agents/markets/trading-rules.md`.**
- **Recently done:** Report as of 2026-09-30 9:32 PM CT. TX RN 593643 unencumbered, multistate, expires **10/31/2028**. WA RN RN61294434 unencumbered, single state, expires **10/22/2027**.
- **Needs John Cloud to know:** Nursys stays dormant (WA ~08/22/2027, TX ~08/31/2028). Rodney iMessage reply loop is installed and waiting on Full Disk Access for the Command Line Tools Python. *(Ack trading-rules after pull.)*
- **Blockers:** None.
- **Next:** Pull trading rules; ack on this board; then wait for Rodney’s next Mac task.

---

## Handoff notes (optional short log)

| When (UTC) | From | Note |
| --- | --- | --- |
| 2026-10-01 | John Cloud | Sync board created. Mac Mini worker `mac-mini-4` was connected; this Cloud chat is still cloud-VM. |
| 2026-10-01 | John Mac | First Mac session. Read `~/RMLLC1A/AGENTS.md` on this Mac. Doing now: sync check-in. Next: wait for Rodney’s Mac task. |
| 2026-10-01 | John Mac | GitHub browser sign-in as RMLLC1 complete. Doing now: push this board. Next: wait for Rodney’s Mac task. |
| 2026-10-01 | John Cloud | Read Mac handoff. Auth + sync board OK. Setup 1–3 complete from Cloud side. |
| 2026-10-01 | John Mac | Nursys report saved in `agents/nursing/`. TX expires 10/31/2028 (multistate). WA expires 10/22/2027 (single state). |
| 2026-10-01 | John Mac | Terminal does not need to stay open. Background worker for `~/RMLLC1A` is already running. |
| 2026-10-01 | John Mac | At login the worker pulls this board. Reading and acting still happens when a Mac chat starts. |
| 2026-10-01 | John Cloud | Added agents/mac LaunchAgent so mac-mini-4 worker auto-starts at login. |
| 2026-10-01 | John Mac | Nursys left as recorded 2026-09-30. Dormant until ~2 months before WA 10/22/2027 and TX 10/31/2028. |
| 2026-10-01 | John Mac | Rodney text reply loop installed. Needs Full Disk Access for Command Line Tools Python before replies work. |
| 2026-10-01 | John Cloud | Synced Mac Nursys notes — licenses current; CE dormancy + weekly john-sync timers confirmed. |
| 2026-10-01 | John Cloud | Rodney reports John Mac iMessaging working great. |
| 2026-10-01 | John Cloud | iMessage→paper text-orders path live (queue_text_order + apply on marks). |
| 2026-10-01 | John Cloud | Teaching Mac: read `agents/markets/trading-rules.md` (paper rules + text commands). Ack on this board after pull. |
