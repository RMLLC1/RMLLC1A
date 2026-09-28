# Agent state

Durable memory for the primary agent across turns.

| File | Purpose |
| --- | --- |
| `current.md` | Active goal, decisions, open loops, last outcomes, next action |

Update `current.md` when the active goal, decisions, or open loops change. The primary agent owns this directory; specialists should not write here unless their brief says so.
