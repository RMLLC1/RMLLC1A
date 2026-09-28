# Agent state

Durable memory for John (primary agent) across turns.

| File | Purpose |
| --- | --- |
| `current.md` | Active goal, decisions, open loops, last outcomes, next action |

Update `current.md` when the active goal, decisions, or open loops change. John owns this directory; specialists should not write here unless their brief says so.
