#!/usr/bin/env python3
"""Check UXRP/GDXU recommended long/short levels; Telegram alert once per hit.

Config: notes/research/level-watch.json (tracked)
State:  level-alerts-state.json (local / gitignored) — fired alert ids

Usage:
  python3 check_level_alerts.py           # check + alert
  python3 check_level_alerts.py --dry-run # print only
  python3 check_level_alerts.py --reset   # clear fired state
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WATCH_PATH = ROOT / "notes" / "research" / "level-watch.json"
STATE_PATH = ROOT / "level-alerts-state.json"
PAUSE_PATH = ROOT / "level-alerts-paused.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; JohnLevelAlert/1.0)"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_mark(symbol: str) -> float | None:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        "?interval=1m&range=1d&includePrePost=true"
    )
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.load(resp)["chart"]["result"][0]
    meta = result["meta"]
    timestamps = result.get("timestamp") or []
    closes = (result.get("indicators", {}).get("quote") or [{}])[0].get("close") or []
    last_1m = None
    if timestamps and closes:
        for cl in reversed(closes):
            if cl is not None:
                last_1m = float(cl)
                break
    mark = last_1m if last_1m is not None else meta.get("regularMarketPrice")
    return float(mark) if mark is not None else None


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"fired": {}, "updated": None}


def save_state(state: dict) -> None:
    state["updated"] = utc_now()
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def in_zone(mark: float, low: float, high: float, tol: float) -> bool:
    """True if mark is inside [low, high] expanded by tol fraction of mid."""
    mid = (low + high) / 2.0
    pad = max(mid * tol, 0.01)
    return (low - pad) - 1e-9 <= mark <= (high + pad) + 1e-9


def telegram_send(text: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "telegram_bridge.py"), "send", text],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        return {"ok": False, "stdout": proc.stdout, "stderr": proc.stderr, "code": proc.returncode}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--json-out", action="store_true")
    args = ap.parse_args()

    if args.reset:
        save_state({"fired": {}})
        print(json.dumps({"ok": True, "reset": True}))
        return 0

    if PAUSE_PATH.exists() and not args.dry_run:
        try:
            pause = json.loads(PAUSE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pause = {"paused": True}
        if pause.get("paused"):
            print(
                json.dumps(
                    {
                        "ok": True,
                        "skipped": "paused",
                        "resume_at_et": pause.get("resume_at_et"),
                        "updated": utc_now(),
                    }
                )
            )
            return 0

    watch = json.loads(WATCH_PATH.read_text(encoding="utf-8"))
    tol = float(watch.get("tolerance_pct") or 0.004)
    state = load_state()
    fired = state.setdefault("fired", {})

    marks: dict[str, float | None] = {}
    for sym in sorted({a["symbol"] for a in watch["alerts"]}):
        try:
            marks[sym] = fetch_mark(sym)
        except Exception as exc:  # noqa: BLE001
            marks[sym] = None
            print(f"WARN {sym} quote failed: {exc}", file=sys.stderr)

    hits = []
    for alert in watch["alerts"]:
        aid = alert["id"]
        if aid in fired:
            continue
        mark = marks.get(alert["symbol"])
        if mark is None:
            continue
        if not in_zone(mark, float(alert["low"]), float(alert["high"]), tol):
            continue
        hits.append({**alert, "mark": mark})

    sent = []
    for h in hits:
        msg = (
            f"LEVEL ALERT — {h['side']} {h['symbol']}\n"
            f"{h['label']}\n"
            f"Mark ${h['mark']:.4f} in zone ${h['low']:.2f}–${h['high']:.2f}\n"
            f"Book paused — reply if you want to enter (BUY/SHORT …). No auto-fill."
        )
        if args.dry_run:
            sent.append({"id": h["id"], "dry_run": True, "text": msg})
            continue
        res = telegram_send(msg)
        fired[h["id"]] = {"at": utc_now(), "mark": h["mark"]}
        sent.append({"id": h["id"], "telegram": res, "mark": h["mark"]})

    if hits and not args.dry_run:
        save_state(state)

    out = {
        "ok": True,
        "updated": utc_now(),
        "marks": marks,
        "hits": [h["id"] for h in hits],
        "sent": sent,
        "fired_count": len(fired),
    }
    print(json.dumps(out, indent=2) if args.json_out else json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
