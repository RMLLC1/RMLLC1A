# Gareth Soloway — Markets knowledge base

**Channel:** [Gareth Soloway](https://www.youtube.com/@GarethSolowayProTrader) (`UCwTu6kD2igaLMpxswtcdxlg`)  
**Role:** Chief Market Strategist, Verified Investing  
**Maintained by:** Markets Department (for John → Rodney)  
**Started:** 2026-09-30  
**Window:** last ~30 days of public uploads (deep digests from official video descriptions + chapters)

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
| `last-30-days.md` | Per-video digests (newest first) |
| `video-index.md` | Title index of recent uploads (incl. members-only flags) |

## Refresh command (for John/Markets)

```bash
curl -sL "https://www.youtube.com/feeds/videos.xml?channel_id=UCwTu6kD2igaLMpxswtcdxlg" -o /tmp/soloway_rss.xml
# Then update digests / levels from new entries
```
