# Current state — John (primary agent)

**Updated:** 2026-09-30

## Active role

**John** is Rodney Bishop's primary agent for RMLLC1A — sole conversational interface; directs all **departments**.

Establishment goal: **complete** (config + live specialist direction verified). John continues serving in this session.

## Decisions

- Primary agent name: **John** (only personal name; Rodney talks only to John).
- All other agents are **departments** (Planning, Research, Engineering, Quality, Communications, Scheduling, Records, Accounting, Markets, Nursing Education). Internal Task ids unchanged (`planner`, `researcher`, etc.).
- Durable work folders: `agents/markets/`, `agents/nursing/`, `agents/accounting/` (expand as needed).
- John = this Cloud Agent session; departments under `.cursor/agents/`.
- Confirm before irreversible external actions (send, delete, share, decline).
- Shared department return contract: Status / Actions / Blockers / Next for John.
- Free texting: **not available** for AT&T — carrier shut down email→SMS (2025-06-17). Do not use `@txt.att.net`. Use email instead unless Rodney adds a paid SMS MCP.
- Accounting Department (`accountant`) for bookkeeping, taxes, accounting (2026-09-28).
- Markets Department (`markets`) for stock/crypto research + paper trading only (2026-09-28). No live trading.

## MCP readiness (live smoke)

| Service | Status |
| --- | --- |
| Gmail | ready |
| Google Calendar | ready |
| Google Drive | ready (empty Drive) |
| Outlook Calendar | needsAuth — deferred until needed |

## Final requirement audit

| Requirement | Evidence | Result |
| --- | --- | --- |
| Identifies as John | `AGENTS.md`, `primary-orchestrator.mdc` | Pass |
| Sole conversational interface | Always-on rule + all departments “Report only to John” | Pass |
| Plans work | Planning Department (`planner`) + default pipelines | Pass |
| Directs research/implement/verify/email/calendar/drive | Departments + live Task smokes | Pass |
| Clear status | `agents/state/current.md` + concise user updates | Pass |
| Never route user to departments | Explicit bans in rules/`AGENTS.md` | Pass |
| Department naming | John keeps name; others are departments (2026-09-30) | Pass |

**Overall:** Pass — no required establishment work remains.

## Open loops

- **Dual John desks (2026-10-01):** **John Cloud** (this Primary agent) + **John Mac** (`mac-mini-4` worker). Shared handoff: `agents/state/john-sync.md` (git pull/push; not auto chat sync).
- **Markets / Soloway learning (2026-09-30):** Knowledge base under `agents/markets/notes/gareth-soloway/` for **both** `@GarethSolowayProTrader` and `@verifiedinvesting`. **Standing refresh:** weekdays **7:00 AM ET** via timer `soloway-youtube-refresh-am`. No email; chat only if new public videos; no git for routine refreshes.
- Outlook Calendar auth when Rodney needs Outlook.
- Accountant specialist ready; Rodney will try a finance task later.
- Markets specialist ready; UXRP research delivered; paper UXRP 10% buy placed; GDXU research delivered.
- **Nursing CE (dormant until 2 months before expiry — Rodney 2026-10-01):** WA RN expires **2027-10-22** → wake **~2027-08-22** (`nursing-ce-wake-wa`). TX RN expires **2028-10-31** → wake **~2028-08-31** (`nursing-ce-wake-tx`). Renewals confirmed Nursys 2026-09-30; no active CE shopping until wake.
- **John sync hygiene (2026-10-01):** daily timer `john-sync-daily` (~11:00 AM ET) while desks are new — John Cloud updates `agents/state/john-sync.md` and pushes; chat only if something needs Rodney. Can thin to weekly later.
- Awaiting Rodney's next task.

## Standing preferences

- Confirm before irreversible external actions.
- Keep replies concise; lead with the answer.
- Name with Rodney: always **John Cloud** or **John Mac** (full desk name; never bare “John”). This session = **John Cloud**.
- Prefer email for notifications (to `regiaemanagementllc@gmail.com`; updated 2026-09-28).
- Standing decision (2026-09-28): email for Cloud fill alerts. **Updated 2026-10-01:** John Mac iMessage with Rodney is working (Mac desk).
- **Email volume (Rodney 2026-09-28):** **Gmail** only when stock/crypto is bought or sold. Never for marks/prices. **No git commit/push** for paper marks or paper fills (stops GitHub/Cursor-bot notification emails). Paper state stays on disk only.
- Free AT&T texting: failed (carrier gateway shut down). Prefer email.
- Markets paper: **auto-execute**; trail **+2% arm / 1% trail** limit stops. **Realized profits → buy SATA**; **hold for daily dividends — never sell**.
- **Price feed:** Yahoo poll every **5 minutes** during **NYSE extended hours only** (Mon–Fri **4:00 AM–8:00 PM ET**). Gmail **only on buy/sell fills**.
- **Soloway / Verified Investing YouTube:** weekday morning refresh **7:00 AM ET** (`soloway-youtube-refresh-am`) for both `@GarethSolowayProTrader` and `@verifiedinvesting`. Chat only on new public videos; no email; no git for routine refreshes.
- **Premarket plan (queued 2026-09-30):** Sell overnight SATA (~1000 sh) at **≥$100.0002** (no loss); keep dividend SATA. Then buy **$50k UXRP @$17** and **$50k GDXU @$107.50**.
- **Trading exits (2026-09-30):** hard **−2%** until arm; arm **+2%** / trail **1%** LIMIT; scale-out **⅓ at +4%**; profits→SATA hold. **Income SATA (~$8k): no stops.**
- **Paper (Rodney 2026-10-01):** Leave working orders alone unless Rodney asks to change (UXRP $50k @$17 still working; GDXU held with exits).
- **Mac reboot auto-start:** Verified OK (Rodney 2026-10-01).
- **iMessage paper trading (2026-10-01):** Rodney may text John Mac BUY/SELL/CANCEL; Mac queues `agents/markets/text-orders/pending/`; Cloud applies on marks poll. Fills still Gmail only.
- **Trading rules doc (2026-10-01):** `agents/markets/trading-rules.md` — John Mac must pull + read; Cloud teaches via john-sync.
