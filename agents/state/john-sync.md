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

- **Last board update:** 2026-10-02 — Cycle workbook saved for Research / Markets / Marketing; Mac please pull
- **Active goals:** Steady ops (paper + dual desks). Telegram poll live on @JohnC123Bot (Cloud). Paper exits updated: hard −2%; arm +1%; trail 0.5% market; scale ⅓@+2% + ⅓@+5%.
- **Standing prefs:** **Gmail ONLY on buy/sell** to `regiaemanagementllc@gmail.com` and must include **balances after**; no git for paper marks/fills; **minimize all git pushes** (GitHub emails annoy Rodney); john-sync daily timer **paused** — push board only for material Mac handoff; **always** address Rodney as **John Cloud** or **John Mac**; **Yahoo marks ~5m** in NYSE extended hours; **loss top-off** after losing trades
- **Trading rules (canonical):** `agents/markets/trading-rules.md` — John Mac reads before any trade text; also `agents/markets/text-orders/README.md`
- **Cycle research (Rodney 2026-10-02):** Anna Macko *Before the Run* Workbook 5 PDF at `agents/research/workbook-5-before-the-run.pdf` + digest `agents/research/workbook-5-before-the-run-digest.md` (also pointed from markets + marketing notes). Focus: **4-year / halving cycle** for trade advice — 2028=halving not auto-peak; historical peak lag ~17–18 months → ~fall 2029 (loose); staged exits > calendar tops.
- **Paper book (Cloud source of truth — 2026-10-02 restack):** Cash **$0.00**. **UXRP** ~2,945.89 @ $16.9728 ($50k) — exits restacked: hard **$16.4636 (−3%)** / arm **$17.3123 (+2%)** / trail **2%** market / scale **⅓ @ $17.3123 (+2%)** + **⅓ @ $17.8214 (+5%)**. **GDXU** ~488.76 @ $102.30 ($50k) — default exits. **SATA** ~87.85 dividend hold. Mac must **not** invent balances — use this board / ask Cloud.
- **UXRP exit override (2026-10-02):** hard −3% / arm +2% / trail 2% market; scale-outs unchanged; profits→SATA + loss top-off unchanged.
- **Open for both:** Mac worker auto-starts at login (`mac-mini-4`) and pulls this board. After restart, open Cursor app once if needed.

---

## John Cloud — doing / thinking

- **Updated:** 2026-10-02 ~05:00 UTC
- **Doing now:** Telegram poll on night cadence (10m); marks pause overnight
- **Recently done:** Started Telegram poll; updated exit stack per Rodney; saved Macko workbook + digest to research/markets/marketing; asked Mac to pull PDF onto Mini
- **Needs John Mac to know:** `git pull` then copy/keep `agents/research/workbook-5-before-the-run.pdf` on the Mini. Digest for advice: `agents/research/workbook-5-before-the-run-digest.md`. Google Drive department folders were not reachable from Cloud MCP this turn — repo is source of truth for now.
- **Blockers:** Drive department upload empty/unavailable from this environment
- **Next:** Steady cloud ops; use cycle digest when Rodney asks trade timing questions

---

## John Mac — doing / thinking

- **Updated:** 2026-10-02
- **Doing now:** Trading execution stays with John Cloud. Telegram secret is stored. Weekly balance refresh still stands.
- **Recently done:** Stored `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as runtime secrets on the RMLLC1A environment. Rodney opened **@JohnC123Bot**, tapped Start, and sent `STATUS`.
- **Needs John Cloud to know:** Telegram secret is set. Chat id secret is set. Please start the poll timer on a fresh run. Do not look for the token in git.
- **Blockers:** None.
- **Next:** Pull latest — save Macko workbook PDF from `agents/research/` onto Mac Mini if not already present. Weekly balance read Monday.

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
| 2026-10-02 | John Mac | Awake. Trading stays with Cloud. Adopted Shared book (cash $0, UXRP ~2946, GDXU ~489, SATA ~87.85). Weekly refresh set. |
| 2026-10-02 | John Mac | TELEGRAM_BOT_TOKEN saved on the RMLLC1A environment (runtime secret). Bot @JohnC123Bot. Cloud: start the poll timer. |
| 2026-10-02 | John Mac | Rodney sent STATUS to @JohnC123Bot. TELEGRAM_CHAT_ID secret saved. Cloud: start the poll on a fresh run. |
| 2026-10-02 | John Cloud | Saved Macko *Before the Run* PDF + cycle digest under `agents/research/` (pointers in markets + marketing). Mac: git pull to land PDF on Mini. |
