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

- **Last board update:** 2026-10-01 — John Mac first Mac session; `~/RMLLC1A/AGENTS.md` readable on this Mac
- **Active goals:** Mac Mini setup; My Machine worker `mac-mini-4`; dual John naming
- **Standing prefs:** Gmail fills only to `regiaemanagementllc@gmail.com`; no git for paper marks/fills; **always** address Rodney as **John Cloud** or **John Mac** (never bare “John”)
- **Open for both:** Texting later (paid SMS); keep worker Terminal open on Mac

---

## John Cloud — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** Cloud Primary agent as **John Cloud**; paper marks timer; sync board live
- **Recently done:** Gmail re-auth OK; GDXU paper buy filled; Mac Mini worker; Rodney wants full names John Cloud / John Mac in all user-facing chat
- **Needs John Mac to know:** Always sign replies as **John Mac**; worker `mac-mini-4`; repo `~/RMLLC1A`; handoff = this file
- **Blockers:** None for sync board
- **Next:** Cloud markets/timers; Mac work → John Mac session

---

## John Mac — doing / thinking

- **Updated:** 2026-10-01
- **Doing now:** First Mac session on `mac-mini-4`. Pulled this branch and filled this section. Confirmed `~/RMLLC1A/AGENTS.md` is readable on this Mac (John Cloud / John Mac operating model).
- **Recently done:** `git pull`. Local tree started on `main` (README only). Checked out `cursor/agent-department-names-cbe0` so the sync board and `AGENTS.md` are on disk.
- **Needs John Cloud to know:** John Mac is live on this Mac. Replies to Rodney use the full name **John Mac**. Pull this commit before the next handoff.
- **Blockers:** None.
- **Next:** Wait for Rodney’s Mac task.

---

## Handoff notes (optional short log)

| When (UTC) | From | Note |
| --- | --- | --- |
| 2026-10-01 | John Cloud | Sync board created. Mac Mini worker `mac-mini-4` was connected; this Cloud chat is still cloud-VM. |
| 2026-10-01 | John Mac | First Mac session. Read `~/RMLLC1A/AGENTS.md` on this Mac. Doing now: sync check-in. Next: wait for Rodney’s Mac task. |
