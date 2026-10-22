#!/usr/bin/env python3
"""Auto-enter UXRP/GDXU long DCA stages when zones hit (Rodney ARM).

Config: notes/research/auto-long-dca.json (tracked)
State:  auto-long-state.json (local / gitignored) — fired stage ids

Usage:
  python3 auto_long_dca.py           # check + queue buys if armed
  python3 auto_long_dca.py --dry-run # print only
  python3 auto_long_dca.py --disarm  # set enabled=false in config
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "notes" / "research" / "auto-long-dca.json"
STATE_PATH = ROOT / "auto-long-state.json"
PAPER_STATE = ROOT / "paper-state.json"
PENDING = ROOT / "text-orders" / "pending"
UA_FETCH = ROOT / "check_level_alerts.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path, default: dict) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def in_zone(mark: float, low: float, high: float, tol: float) -> bool:
    mid = (low + high) / 2.0
    pad = max(mid * tol, 0.01)
    return (low - pad) - 1e-9 <= mark <= (high + pad) + 1e-9


def fetch_mark(symbol: str) -> float | None:
    # Reuse Yahoo fetch from check_level_alerts
    sys.path.insert(0, str(ROOT))
    from check_level_alerts import fetch_mark as _fetch  # noqa: WPS433

    return _fetch(symbol)


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
        return {"ok": False, "stdout": proc.stdout, "stderr": proc.stderr}


def queue_buy_best(symbol: str, notional: float, no_hard_stop: bool, stage_id: str) -> dict:
    PENDING.mkdir(parents=True, exist_ok=True)
    oid = f"TO-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    doc = {
        "id": oid,
        "source": "auto_long_dca",
        "from": "+18173715555",
        "created": utc_now(),
        "status": "PENDING",
        "action": "BUY_BEST",
        "symbol": symbol,
        "notional": round(notional, 2),
        "attach_exits": True,
        "no_hard_stop": bool(no_hard_stop),
        "auto_stage_id": stage_id,
        "raw_text": f"AUTO BUY {symbol} ${notional:.0f} BEST ({stage_id})",
    }
    path = PENDING / f"{oid}.json"
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return {"order_id": oid, "path": str(path), "doc": doc}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--disarm", action="store_true")
    ap.add_argument("--json-out", action="store_true")
    args = ap.parse_args()

    cfg = load_json(CONFIG_PATH, {"enabled": False, "stages": []})
    if args.disarm:
        cfg["enabled"] = False
        cfg["disarmed_at"] = utc_now()
        save_json(CONFIG_PATH, cfg)
        print(json.dumps({"ok": True, "enabled": False}))
        return 0

    if not cfg.get("enabled"):
        print(json.dumps({"ok": True, "skipped": "disarmed", "updated": utc_now()}))
        return 0

    tol = float(cfg.get("tolerance_pct") or 0.004)
    state = load_json(STATE_PATH, {"fired": {}, "updated": None})
    fired = state.setdefault("fired", {})
    paper = load_json(PAPER_STATE, {"cash": 0})
    cash = float(paper.get("cash") or 0)

    marks: dict[str, float | None] = {}
    for sym in sorted({s["symbol"] for s in cfg.get("stages") or []}):
        try:
            marks[sym] = fetch_mark(sym)
        except Exception as exc:  # noqa: BLE001
            marks[sym] = None
            print(f"WARN {sym} quote failed: {exc}", file=sys.stderr)

    queued = []
    for stage in cfg.get("stages") or []:
        sid = stage["id"]
        if stage.get("skipped"):
            if sid not in fired:
                fired[sid] = {
                    "at": utc_now(),
                    "skipped": True,
                    "reason": stage.get("skip_reason"),
                }
            continue
        if sid in fired:
            continue
        mark = marks.get(stage["symbol"])
        if mark is None:
            continue
        if not in_zone(mark, float(stage["low"]), float(stage["high"]), tol):
            continue

        # Re-read cash for sequential stages in one pass
        paper = load_json(PAPER_STATE, {"cash": 0})
        cash = float(paper.get("cash") or 0)
        pct = float(stage["cash_pct"])
        notional = round(cash * pct, 2)
        if notional < 1:
            fired[sid] = {"at": utc_now(), "skipped": True, "reason": "cash too low"}
            continue

        hard = bool(stage.get("hard_stop", True))
        no_hard = not hard
        info = {
            "id": sid,
            "symbol": stage["symbol"],
            "mark": mark,
            "notional": notional,
            "cash_pct": pct,
            "no_hard_stop": no_hard,
            "label": stage.get("label"),
        }
        if args.dry_run:
            queued.append({**info, "dry_run": True})
            continue

        q = queue_buy_best(stage["symbol"], notional, no_hard, sid)
        fired[sid] = {
            "at": utc_now(),
            "mark": mark,
            "notional": notional,
            "order_id": q["order_id"],
            "no_hard_stop": no_hard,
        }
        msg = (
            f"AUTO LONG — {stage['symbol']} {sid}\n"
            f"{stage.get('label')}\n"
            f"Mark ${mark:.4f} → BUY BEST ${notional:,.2f} "
            f"({'no hard stop' if no_hard else 'WITH hard stop'})\n"
            f"Queued {q['order_id']} — fills on next marks poll."
        )
        tg = telegram_send(msg)
        queued.append({**info, "order_id": q["order_id"], "telegram": tg})

        # Apply + fill immediately so next stage sees updated cash
        subprocess.run(
            [sys.executable, str(ROOT / "mark_to_market.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    if not args.dry_run:
        state["updated"] = utc_now()
        save_json(STATE_PATH, state)

    out = {
        "ok": True,
        "updated": utc_now(),
        "enabled": True,
        "marks": marks,
        "cash": cash,
        "queued": queued,
        "fired_count": len(fired),
    }
    print(json.dumps(out, indent=2) if args.json_out else json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
