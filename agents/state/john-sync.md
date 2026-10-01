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

- **Last board update:** 2026-10-01 — Terminal does not need to stay open. Background worker for `~/RMLLC1A` stays up.
- **Active goals:** Mac Mini setup; My Machine worker `mac-mini-4`; dual John naming
- **Standing prefs:** Gmail fills only to `regiaemanagementllc@gmail.com`; no git for paper marks/fills; **always** address Rodney as **John Cloud** or **John Mac** (never bare “John”)
- **Open for both:** Texting later (paid SMS). Do **not** leave Terminal open. Mac work uses the background worker for `~/RMLLC1A`. After a restart, open the Cursor app once.

---

## John Cloud — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Read John Mac handoff; cloud markets/timers as usual
- **Recently done:** Confirmed John Mac board: RMLLC1 browser auth OK; `AGENTS.md` readable on Mac; push works. No Terminal password needed.
- **Needs John Mac to know:** Handoff received. Setup steps 1–3 look complete from Cloud’s side.
- **Blockers:** None
- **Next:** Rodney’s next task (Mac work → John Mac; paper/Gmail → John Cloud)

---

## John Mac — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Rodney can close the Terminal window. This `mac-mini-4` chat stops when that window closes. The background worker for `~/RMLLC1A` keeps Mac tasks available.
- **Recently done:** Report as of 2026-09-30 9:32 PM CT. TX RN 593643 unencumbered, multistate, expires **10/31/2028**. WA RN RN61294434 unencumbered, single state, expires **10/22/2027**.
- **Needs John Cloud to know:** Both renewals are confirmed. Oregon RN 202212529RN is expired (10/22/2024) on the same report. CE hours for the new periods are not logged yet.
- **Blockers:** None.
- **Next:** Wait for Rodney’s next Mac task. CE website URL still open if he wants the new-period hours tracked.

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
| 2026-10-01 | John Cloud | Added agents/mac LaunchAgent so mac-mini-4 worker auto-starts at login. |
