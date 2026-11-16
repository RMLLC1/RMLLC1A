# Current state — John (primary agent)

**Updated:** 2026-11-03

**Handoff for new chats:** `agents/state/john-cloud-handoff.md` (rules, lessons, paper book, Telegram).

## Active role

**John / John Cloud** is Rodney Bishop's primary agent for RMLLC1A — sole conversational interface; directs all specialists.

Establishment goal: **complete**. Prefer starting a **fresh chat** when context is huge; load the handoff + this file.

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

- **Telegram:** Keepalive on this session; never idle without Rodney asking. See handoff.
- **Paper book:** Cash $50k; GDXU 2,103.17 @ $71.32; SATA 260.12 hold; all SO cancelled 2026-11-04.
- Re-subscribe timers after any **new chat** (timers do not transfer).
- Outlook Calendar auth when needed.
- Nursing CE: dormant until ~2 months before WA/TX renewals (see handoff).

## Standing preferences

Full list: **`agents/state/john-cloud-handoff.md`**. Short form:

- Gmail **fills only**; no git on marks/fills; paper on disk.
- Telegram always on unless Rodney says stop.
- SATA hold for dividends; profits → SATA.
- **No scale-outs / no hard stops** — trail only (2026-11-04).
- Marks: NYSE extended hours only; silent if no fills.
