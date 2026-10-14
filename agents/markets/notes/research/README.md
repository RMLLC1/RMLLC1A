# Markets research — cycle workbook

Rodney (2026-10-02 Telegram): save & use when advising trades.

- **PDF:** `../../../research/workbook-5-before-the-run.pdf`
- **Digest (4-year cycle):** `../../../research/workbook-5-before-the-run-digest.md`

Trading rules remain in `../../trading-rules.md`. This workbook informs **timing psychology and staged exits**, not ticker picks.

## Level alerts (Rodney 2026-10-02 night)

Watch list: `level-watch.json` (UXRP/GDXU long + short recommended zones).  
Checker: `../../check_level_alerts.py` — Telegram once per zone hit.  
Fired state (local): `../../level-alerts-state.json` (gitignored).

## Auto long DCA (Rodney 2026-10-05 ARM)

Config: `auto-long-dca.json` — value 15% / trough +15% (no hard stop); deeper +30% (WITH hard stop).  
Runner: `../../auto_long_dca.py` — queues BUY BEST when zone hits; say **STOP AUTO** / `--disarm` to disable.  
State (local): `../../auto-long-state.json` (gitignored). GDXU deeper zone not defined yet.

Short-entry notes: `gdxu-short-entries-2026-10-02.md`, `uxrp-short-entries-2026-10-02.md`.
