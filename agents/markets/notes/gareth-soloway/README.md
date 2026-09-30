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

- We **cannot literally listen** to YouTube audio in this environment. Digests are built from **official titles, descriptions, and chapter lists** (Soloway’s own writeups are unusually complete).
- **Members-only** videos are listed but not digested (paywall).
- YouTube blocks full transcript pulls here; refresh via channel RSS when updating.
- Levels go stale — re-pull RSS before relying on a number for a live decision.

## Files

| File | Purpose |
| --- | --- |
| `framework.md` | Recurring method / playbook distilled from recent videos |
| `levels-current.md` | Latest key levels & bias by asset (from newest digests) |
| `last-30-days.md` | Gareth Soloway channel digests |
| `verified-investing-last-30-days.md` | Verified Investing channel digests |
| `video-index.md` | Title index of recent uploads (incl. members-only flags) |

## Morning refresh (standing — Rodney 2026-09-30)

- **When:** each weekday morning **7:00 AM America/New_York** (timer: `soloway-youtube-refresh-am`).
- **Command:** `python3 agents/markets/notes/gareth-soloway/refresh_soloway.py`
- **Behavior:** rewrite digests from **both** channel RSS feeds; bump levels “as of”; track new video ids in `refresh-state.json`.
- **Comms:** no email. Chat only if `new_count > 0`. No git commit/push for routine refreshes (keep on disk).
