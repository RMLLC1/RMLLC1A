# RMLLC1A

Personal agent workspace for Rodney Bishop.

## Primary agent

The **primary agent** is the only agent you talk to. It plans work and directs specialist agents for research, implementation, verification, email, calendar, and Drive.

Start a Cloud Agent or IDE Agent session on this repo and speak to the primary agent in natural language.

## Layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating model for the primary agent |
| `.cursor/rules/primary-orchestrator.mdc` | Always-on orchestration rule |
| `.cursor/agents/` | Specialist subagents the primary directs |
| `agents/state/` | Durable status across turns |

## Specialists

- `planner` — break down complex work
- `researcher` — investigate before changing
- `implementer` — make repo changes
- `verifier` — validate results
- `email-assistant` — Gmail
- `calendar-assistant` — Google / Outlook calendar
- `drive-assistant` — Google Drive
