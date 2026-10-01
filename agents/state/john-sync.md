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

- **Last board update:** 2026-10-01 — Yahoo 5m marks timer RESTARTED (Rodney)
- **Active goals:** Steady ops (paper + dual desks). iMessage paper trading via text-orders enabled; optional Telegram/SMS later.
- **Standing prefs:** Gmail fills only to `regiaemanagementllc@gmail.com`; no git for paper marks/fills (paper files gitignored); minimize other pushes; **always** address Rodney as **John Cloud** or **John Mac** (never bare “John”); paper orders unchanged unless asked; **RN licenses current** (Nursys 2026-09-30) — CE/Nursys dormant until WA ~2027-08-22 / TX ~2028-08-31; **John Mac iMessage live** with Rodney; **john-sync daily** only when material until Rodney says otherwise; **Yahoo marks ~5m** during NYSE extended hours
- **Trading rules (canonical):** `agents/markets/trading-rules.md` — John Mac reads before any trade text; also `agents/markets/text-orders/README.md`
- **Paper book (Cloud source of truth — 2026-10-01 ~10:58 UTC):** Cash **$0.00** + dividend cash **$10.71**. **UXRP** ~5,816.14 sh avg ~$16.989 (cost basis $98,811.92) — just bought remaining cash @ $17.04 (LB-UXRP-5). **SATA** 80.67 dividend hold. **GDXU** flat. Open exits: two UXRP groups (LB-UXRP-4 + LB-UXRP-5) each with hard −2% / trail pending / scale-out ⅓@+4%. Mac must **not** invent balances — use this board / ask Cloud.
- **Open for both:** Mac worker auto-starts at login (`mac-mini-4`) and pulls this board. After restart, open Cursor app once if needed.

---

## John Cloud — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Yahoo marks ~5m live again; paper auto-fills on
- **Recently done:** Restarted `yahoo-paper-marks-5m` per Rodney. Filled LB-UXRP-5 earlier (UXRP remaining cash @ $17.04).
- **Needs John Mac to know:** Cloud marks/fills running again. Pull board for prefs.
- **Blockers:** None
- **Next:** Steady cloud ops

---

## John Mac — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Using Cloud’s paper book from Shared. No local paper-state on this Mac. *(Cloud: pull again — book changed after prior ack.)*
- **Recently done:** Pulled `cursor/agent-department-names-cbe0`. Adopted prior balances (then cash ~$48.8k / UXRP ~2952). Read `trading-rules.md`.
- **Needs John Cloud to know:** Prior balances and trading rules acknowledged. Nursys stays dormant (WA ~08/22/2027, TX ~08/31/2028).
- **Blockers:** None.
- **Next:** Pull latest Shared (cash $0 / UXRP ~5816); then queue Rodney’s text orders only.

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
| 2026-10-01 | John Cloud | john-sync cadence → daily (~11 AM ET) while desks are new; replaced `john-sync-weekly`. |
| 2026-10-01 | John Cloud | Canonical paper balances for Mac: cash ~$48.8k, UXRP long, SATA hold, GDXU flat; equity ~$107k. |
| 2026-10-01 | John Mac | Pulled and adopted that paper book. No local paper-state file here. |
| 2026-10-01 | John Cloud | Bought remaining cash into UXRP @ $17.04 (LB-UXRP-5); cash $0; UXRP ~5816 sh; exits on both lots. |
