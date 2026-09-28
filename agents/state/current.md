# Current state — John (primary agent)

**Updated:** 2026-09-28

## Active role

**John** is Rodney Bishop's primary agent for RMLLC1A — sole conversational interface; directs all specialists.

Establishment goal: **complete** (config + live specialist direction verified). John continues serving in this session.

## Decisions

- Primary agent name: **John**.
- John = this Cloud Agent session; specialists under `.cursor/agents/`.
- Confirm before irreversible external actions (send, delete, share, decline).
- Shared specialist return contract: Status / Actions / Blockers / Next for John.
- Free texting: **not available** for AT&T — carrier shut down email→SMS (2025-06-17). Do not use `@txt.att.net`. Use email instead unless Rodney adds a paid SMS MCP.
- Specialist `accountant` added for bookkeeping, taxes, accounting (2026-09-28).
- Specialist `markets` added for stock/crypto research + paper trading only (2026-09-28). No live trading.

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
| Sole conversational interface | Always-on rule + all specialists “Report only to John” | Pass |
| Plans work | `planner` + default pipelines | Pass |
| Directs research/implement/verify/email/calendar/drive | 7 specialists + live Task smokes | Pass |
| Clear status | `agents/state/current.md` + concise user updates | Pass |
| Never route user to specialists | Explicit bans in rules/`AGENTS.md` | Pass |

**Overall:** Pass — no required establishment work remains.

## Open loops

- Outlook Calendar auth when Rodney needs Outlook.
- Accountant specialist ready; Rodney will try a finance task later.
- Markets specialist ready; UXRP research delivered; paper UXRP 10% buy placed; GDXU research delivered.
- Awaiting Rodney's next task.

## Standing preferences

- Confirm before irreversible external actions.
- Keep replies concise; lead with the answer.
- Name: John.
- Prefer email for notifications (to `regiaemanagementllc@gmail.com`; updated 2026-09-28).
- Standing decision (2026-09-28): use email for messaging for now; no SMS/iMessage setup.
- Free AT&T texting: failed (carrier gateway shut down). Prefer email.
- Markets paper fills: **always best available price** (buy = lowest quote; sell = highest). Stop exits = **limit** (not market). UXRP ~30% @ $17.25; GDXU ~30% @ **$110** (Rodney-corrected); both trailing stop-limits pending +2% arm. Cash ~40%.
