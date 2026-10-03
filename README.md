# RMLLC1A

Personal agent workspace for Rodney Bishop.

## John (primary agent)

**John** is the main chat session (Cloud Agent or IDE Agent on this repo) — there is no separate `primary.md` file. He is the only agent you talk to. He plans work and directs **departments** for research, engineering, quality, email, calendar, Drive, accounting, markets (research + paper trading), and nursing education (TX + WA).

Speak to John in natural language; he routes work to departments and brings you the answer. John keeps his personal name; every other agent is a department.

## Layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating model for John |
| `.cursor/rules/primary-orchestrator.mdc` | Always-on orchestration rule |
| `.cursor/agents/` | Department subagents John directs |
| `agents/state/` | Durable status across turns |
| `agents/nursing/` | RN CE requirements + course log (TX + WA) |

## Departments

| Department | Agent id | Role |
| --- | --- | --- |
| Planning Department | `planner` | Break down complex work |
| Research Department | `researcher` | Investigate before changing |
| Engineering Department | `implementer` | Make repo changes |
| Quality Department | `verifier` | Validate results |
| Communications Department | `email-assistant` | Gmail |
| Scheduling Department | `calendar-assistant` | Google / Outlook calendar |
| Records Department | `drive-assistant` | Google Drive |
| Accounting Department | `accountant` | Bookkeeping, taxes, accounting |
| Markets Department | `markets` | Stock/crypto research + paper trading (not live) |
| Nursing Education Department | `nurse-ce` | Texas + Washington RN CE (vet dual-state fit; you take the tests) |
