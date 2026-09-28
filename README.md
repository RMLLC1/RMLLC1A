# RMLLC1A

Personal agent workspace for Rodney Bishop.

## John (primary agent)

**John** is the main chat session (Cloud Agent or IDE Agent on this repo) — there is no separate `primary.md` file. He is the only agent you talk to. He plans work and directs specialist agents for research, implementation, verification, email, calendar, Drive, accounting, and markets (research + paper trading).

Speak to John in natural language; he routes work to specialists and brings you the answer.

## Layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating model for John |
| `.cursor/rules/primary-orchestrator.mdc` | Always-on orchestration rule |
| `.cursor/agents/` | Specialist subagents John directs |
| `agents/state/` | Durable status across turns |

## Specialists

- `planner` — break down complex work
- `researcher` — investigate before changing
- `implementer` — make repo changes
- `verifier` — validate results
- `email-assistant` — Gmail
- `calendar-assistant` — Google / Outlook calendar
- `drive-assistant` — Google Drive
- `accountant` — bookkeeping, taxes, accounting
- `markets` — stock/crypto research + paper trading (not live)
