# Gareth Soloway — Markets knowledge base

**Channels (both Soloway / Verified Investing):**  
- [Gareth Soloway](https://www.youtube.com/@GarethSolowayProTrader) (`UCwTu6kD2igaLMpxswtcdxlg`)  
- [Verified Investing](https://www.youtube.com/@verifiedinvesting) (`UCZ-J2m1AUSLnifUEKam5_dA`) — owned/operated with Gareth; includes *My Trading Game Plan*, Weekly Wrap-Up, etc.  

**Role:** Chief Market Strategist / Verified Investing ecosystem  
**Maintained by:** Markets Department (for John → Rodney)  
**Started:** 2026-09-30  
**Window:** newest public uploads via RSS (~15 per channel; deep digests from official descriptions + chapters)

## How we use this

When Rodney asks about possible trades, John/Markets should:
1. Check `framework.md` for Soloway’s method (how he thinks).
2. Check `levels-current.md` for his latest stated levels/bias by asset.
3. Check `last-30-days.md` for the video digests behind those levels.
4. Clearly label insights as **Soloway’s view (as of date)** — not our advice, not a guarantee.
5. Never override Rodney’s standing paper rules (auto-execute, +2%/1% trail, profits→SATA).

## Honest limits

- We **cannot literally watch** YouTube video. Digests use **official titles/descriptions/chapters** plus **auto-captions** (spoken points) when the caption fetch works.
- Caption text can be messy (duplicates, missed chart-only levels). Prefer dated spoken digests + description together.
- **Members-only** videos are listed but not digested (paywall).
- Levels go stale — re-pull before relying on a number for a live decision.

## Files

| File | Purpose |
| --- | --- |
| `framework.md` | Recurring method / playbook distilled from recent videos |
| `levels-current.md` | Latest key levels & bias by asset (from newest digests) |
| `last-30-days.md` | Gareth Soloway channel digests |
| `verified-investing-last-30-days.md` | Verified Investing channel digests |
| `spoken-digests/` | Per-video caption highlights (**local / gitignored**) |
| `transcripts/` | Cleaned full captions (**local / gitignored**) |
| `video-index.md` | Title index of recent uploads (incl. members-only flags) |

## Morning refresh (standing — Rodney 2026-09-30; captions 2026-10-01)

- **When:** each weekday morning **7:00 AM America/New_York** (timer: `soloway-youtube-refresh-am`).
- **Command:** `python3 agents/markets/notes/gareth-soloway/refresh_soloway.py`
- **Behavior:** rewrite digests from **both** channel RSS feeds; for **new** public videos fetch auto-captions → `spoken-digests/` + embed bullets in digest files; bump levels “as of”; track ids in `refresh-state.json`.
- **Backfill (manual):** `python3 .../refresh_soloway.py --backfill 5` for newest videos missing spoken digests.
- **Comms:** no email. Chat only if `new_count > 0` (include spoken highlights when present). No git for routine refreshes.
