# Agent state

Durable memory for John (primary agent) across turns.

| File | Purpose |
| --- | --- |
| `current.md` | Active goal, decisions, open loops, last outcomes, next action |
| `john-sync.md` | Handoff between **John Cloud** and **John Mac** (pull → update → commit/push) |

Update `current.md` when the active goal, decisions, or open loops change. Update `john-sync.md` when Cloud and Mac Johns need to share status. John owns this directory; specialists should not write here unless their brief says so.
