#!/usr/bin/env python3
"""Pull pending text-orders from git and apply them into local paper-state.json."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "paper-state.json"
PENDING = ROOT / "text-orders" / "pending"
PROCESSED = ROOT / "text-orders" / "processed"
REPO = ROOT.parent.parent


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sync_pending_from_remote() -> list[str]:
    """Best-effort: fetch and checkout only text-orders/pending from origin."""
    notes = []
    try:
        subprocess.run(
            ["git", "fetch", "origin"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO, text=True
        ).strip()
        # Prefer tracking branch tip for text-orders only
        ref = f"origin/{branch}"
        # Show if path exists on remote
        probe = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref, "agents/markets/text-orders"],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        if probe.returncode != 0 or not probe.stdout.strip():
            notes.append("no remote text-orders yet")
            return notes
        subprocess.run(
            ["git", "checkout", ref, "--", "agents/markets/text-orders"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        notes.append(f"synced text-orders from {ref}")
    except Exception as exc:  # noqa: BLE001 — best effort on timer
        notes.append(f"sync skipped: {exc}")
    return notes


def next_order_id(state: dict, prefix: str, symbol: str) -> str:
    n = (
        sum(
            1
            for o in state.get("orders", [])
            if o.get("symbol") == symbol and str(o.get("id", "")).startswith(prefix)
        )
        + 1
    )
    return f"{prefix}{symbol}-{n}"


def _already_applied_text_id(state: dict, text_id: str | None) -> str | None:
    """Return existing order id if this text_order_id was already applied."""
    if not text_id:
        return None
    for o in state.get("orders", []):
        if o.get("text_order_id") == text_id and o.get("status") not in {"CANCELLED"}:
            return str(o.get("id"))
    return None


def git_push_processed() -> list[str]:
    """Commit pending→processed moves so remote sync does not re-apply orders."""
    notes: list[str] = []
    try:
        subprocess.run(
            ["git", "add", "-A", "agents/markets/text-orders"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        )
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        )
        if not staged.stdout.strip():
            notes.append("no text-orders git changes to push")
            return notes
        subprocess.run(
            ["git", "commit", "-m", "Text orders: move applied files pending→processed"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
        )
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO, text=True
        ).strip()
        subprocess.run(
            ["git", "push", "-u", "origin", branch],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        notes.append(f"pushed text-orders processed to origin/{branch}")
    except Exception as exc:  # noqa: BLE001 — best effort on timer
        notes.append(f"processed git push skipped: {exc}")
    return notes


def apply_one(state: dict, doc: dict, events: list, now: str) -> dict:
    """Mutate state; return result dict."""
    action = doc.get("action")
    sym = doc.get("symbol")

    if action == "CANCEL":
        oid = doc.get("cancel_order_id")
        for o in state.get("orders", []):
            if o.get("id") == oid and o.get("status") not in {"FILLED", "CANCELLED"}:
                o["status"] = "CANCELLED"
                o["params_text"] = (o.get("params_text") or "") + " | Cancelled via text order"
                events.append(f"{now} TEXT cancel {oid}")
                return {"ok": True, "detail": f"cancelled {oid}"}
        return {"ok": False, "detail": f"order not found or already done: {oid}"}

    if action == "CANCEL_BUYS":
        cancelled = []
        for o in state.get("orders", []):
            if (
                o.get("symbol") == sym
                and o.get("type") == "LIMIT_BUY"
                and o.get("status") in {"OPEN", "WORKING"}
            ):
                o["status"] = "CANCELLED"
                o["params_text"] = (o.get("params_text") or "") + " | Cancelled via text CANCEL BUYS"
                cancelled.append(o["id"])
        events.append(f"{now} TEXT cancel buys {sym}: {cancelled or 'none'}")
        return {"ok": True, "detail": f"cancelled {cancelled}"}

    if action == "CANCEL_SHORTS":
        cancelled = []
        for o in state.get("orders", []):
            if (
                o.get("symbol") == sym
                and o.get("type") == "LIMIT_SHORT"
                and o.get("status") in {"OPEN", "WORKING"}
            ):
                o["status"] = "CANCELLED"
                o["params_text"] = (o.get("params_text") or "") + " | Cancelled via text CANCEL SHORTS"
                cancelled.append(o["id"])
        events.append(f"{now} TEXT cancel shorts {sym}: {cancelled or 'none'}")
        return {"ok": True, "detail": f"cancelled {cancelled}"}

    def _exit_stamps(symbol: str) -> tuple[dict, str]:
        """Per-symbol exit stamps for new text buys. SATA profits / loss top-off unchanged elsewhere."""
        if symbol == "UXRP":
            # Noise-adjusted (Rodney 2026-10-02): hard −3%, arm +2%; last ⅓ trail 0.5% market.
            return (
                {
                    "arm_pct": 0.02,
                    "trail_pct": 0.005,
                    "hard_stop_pct": 0.03,
                    "arm_after_scale_level": 2,
                },
                "Exits (UXRP): hard −3%; scale ⅓@+2% + ⅓@+5%; last ⅓ trail 0.5% market AFTER 2nd scale.",
            )
        if symbol == "GDXU":
            # Noise-adjusted (Rodney 2026-10-02): hard −4.5%, arm after 2nd scale; trail 0.5%; ⅓@+3% + ⅓@+7%.
            return (
                {
                    "arm_pct": 0.03,
                    "trail_pct": 0.005,
                    "hard_stop_pct": 0.045,
                    "arm_after_scale_level": 2,
                    "scale_out_levels": [
                        {"pct": 0.03, "fraction": 1.0 / 3.0},
                        {"pct": 0.07, "fraction": 1.0 / 3.0},
                    ],
                },
                "Exits (GDXU): hard −4.5%; scale ⅓@+3% + ⅓@+7%; last ⅓ trail 0.5% market AFTER 2nd scale.",
            )
        return (
            {"arm_pct": 0.01, "trail_pct": 0.005, "hard_stop_pct": 0.02},
            "Exits: hard −2%; +1% arm / 0.5% trail market; scale-out ⅓ at +2% and ⅓ at +5%.",
        )

    def _exit_stamps_short(symbol: str) -> tuple[dict, str]:
        """Per-symbol exit stamps for new text shorts (mirrored pct numbers, inverted wording)."""
        stamps, _ = _exit_stamps(symbol)
        if symbol == "UXRP":
            return (
                stamps,
                "Short exits (UXRP): hard +3%; scale ⅓@−2% + ⅓@−5%; last ⅓ trail 0.5% market AFTER 2nd scale.",
            )
        if symbol == "GDXU":
            return (
                stamps,
                "Short exits (GDXU): hard +4.5%; scale ⅓@−3% + ⅓@−7%; last ⅓ trail 0.5% market AFTER 2nd scale.",
            )
        return (
            stamps,
            "Short exits: hard +2%; −1% arm / 0.5% trail market; scale-out ⅓ at −2% and ⅓ at −5%.",
        )

    if action == "LIMIT_BUY":
        existing = _already_applied_text_id(state, doc.get("id"))
        if existing:
            return {"ok": True, "detail": f"skip duplicate; already {existing}", "skipped": True}
        oid = next_order_id(state, "LB-", sym)
        stamps, exit_blurb = _exit_stamps(sym)
        order = {
            "id": oid,
            "symbol": sym,
            "type": "LIMIT_BUY",
            "status": "OPEN",
            "limit_price": float(doc["limit_price"]),
            "notional": float(doc["notional"]),
            "attach_trailing_stop": bool(doc.get("attach_exits", True)),
            "attach_trading_exits": bool(doc.get("attach_exits", True)),
            **stamps,
            "source": "text_order",
            "text_order_id": doc.get("id"),
            "params_text": (
                f"Text: buy ${float(doc['notional']):,.0f} {sym} at ${float(doc['limit_price'])} or better. "
                f"{exit_blurb}"
            ),
        }
        state.setdefault("orders", []).append(order)
        events.append(f"{now} TEXT queued {oid} LIMIT_BUY {sym} @{doc['limit_price']} ${doc['notional']}")
        return {"ok": True, "detail": f"queued {oid}"}

    if action == "BUY_BEST":
        existing = _already_applied_text_id(state, doc.get("id"))
        if existing:
            return {"ok": True, "detail": f"skip duplicate; already {existing}", "skipped": True}
        oid = next_order_id(state, "BB-", sym)
        stamps, exit_blurb = _exit_stamps(sym)
        order = {
            "id": oid,
            "symbol": sym,
            "type": "BUY_BEST",
            "status": "OPEN",
            "notional": float(doc["notional"]),
            "attach_trailing_stop": bool(doc.get("attach_exits", True)),
            "attach_trading_exits": bool(doc.get("attach_exits", True)),
            **stamps,
            "source": "text_order",
            "text_order_id": doc.get("id"),
            "params_text": (
                f"Text: buy ${float(doc['notional']):,.0f} {sym} at best. "
                f"{exit_blurb}"
            ),
        }
        state.setdefault("orders", []).append(order)
        events.append(f"{now} TEXT queued {oid} BUY_BEST {sym} ${doc['notional']}")
        return {"ok": True, "detail": f"queued {oid}"}

    if action == "LIMIT_SHORT":
        if sym == "SATA":
            return {"ok": False, "detail": "SATA shorts blocked (dividend hold)"}
        existing = _already_applied_text_id(state, doc.get("id"))
        if existing:
            return {"ok": True, "detail": f"skip duplicate; already {existing}", "skipped": True}
        oid = next_order_id(state, "LSH-", sym)
        stamps, exit_blurb = _exit_stamps_short(sym)
        order = {
            "id": oid,
            "symbol": sym,
            "type": "LIMIT_SHORT",
            "status": "OPEN",
            "limit_price": float(doc["limit_price"]),
            "notional": float(doc["notional"]),
            "attach_trailing_stop": bool(doc.get("attach_exits", True)),
            "attach_trading_exits": bool(doc.get("attach_exits", True)),
            **stamps,
            "source": "text_order",
            "text_order_id": doc.get("id"),
            "params_text": (
                f"Text: short ${float(doc['notional']):,.0f} {sym} at ${float(doc['limit_price'])} or better. "
                f"{exit_blurb}"
            ),
        }
        state.setdefault("orders", []).append(order)
        events.append(
            f"{now} TEXT queued {oid} LIMIT_SHORT {sym} @{doc['limit_price']} ${doc['notional']}"
        )
        return {"ok": True, "detail": f"queued {oid}"}

    if action == "SHORT_BEST":
        if sym == "SATA":
            return {"ok": False, "detail": "SATA shorts blocked (dividend hold)"}
        existing = _already_applied_text_id(state, doc.get("id"))
        if existing:
            return {"ok": True, "detail": f"skip duplicate; already {existing}", "skipped": True}
        oid = next_order_id(state, "SHB-", sym)
        stamps, exit_blurb = _exit_stamps_short(sym)
        order = {
            "id": oid,
            "symbol": sym,
            "type": "SHORT_BEST",
            "status": "OPEN",
            "notional": float(doc["notional"]),
            "attach_trailing_stop": bool(doc.get("attach_exits", True)),
            "attach_trading_exits": bool(doc.get("attach_exits", True)),
            **stamps,
            "source": "text_order",
            "text_order_id": doc.get("id"),
            "params_text": (
                f"Text: short ${float(doc['notional']):,.0f} {sym} at best. "
                f"{exit_blurb}"
            ),
        }
        state.setdefault("orders", []).append(order)
        events.append(f"{now} TEXT queued {oid} SHORT_BEST {sym} ${doc['notional']}")
        return {"ok": True, "detail": f"queued {oid}"}

    if action in {"LIMIT_COVER", "COVER_BEST"}:
        if sym == "SATA":
            return {"ok": False, "detail": "SATA covers blocked (dividend hold)"}
        oid = next_order_id(state, "CB-" if action == "COVER_BEST" else "LC-", sym)
        order = {
            "id": oid,
            "symbol": sym,
            "type": action,
            "status": "OPEN",
            "source": "text_order",
            "text_order_id": doc.get("id"),
        }
        if doc.get("qty_all"):
            order["qty_all"] = True
            order["params_text"] = f"Text: cover ALL {sym} ({action})"
        else:
            order["qty"] = float(doc["qty"])
            order["params_text"] = f"Text: cover {sym} qty={doc['qty']} ({action})"
        if action == "LIMIT_COVER":
            order["limit_price"] = float(doc["limit_price"])
            order["params_text"] += f" limit={doc['limit_price']}"
        state.setdefault("orders", []).append(order)
        events.append(f"{now} TEXT queued {oid} {action} {sym}")
        return {"ok": True, "detail": f"queued {oid}"}

    if action in {"LIMIT_SELL", "SELL_BEST"}:
        if sym == "SATA" and not doc.get("allow_sata_sell"):
            return {"ok": False, "detail": "SATA sells blocked (dividend hold)"}
        oid = next_order_id(state, "SB-" if action == "SELL_BEST" else "LS-", sym)
        order = {
            "id": oid,
            "symbol": sym,
            "type": action,
            "status": "OPEN",
            "source": "text_order",
            "text_order_id": doc.get("id"),
        }
        if doc.get("allow_sata_sell"):
            order["allow_sata_sell"] = True
            order["rodney_override_sata_sell"] = True
        if doc.get("skip_profit_to_sata"):
            order["skip_profit_to_sata"] = True
        if doc.get("qty_all"):
            order["qty_all"] = True
            order["params_text"] = f"Text: sell ALL {sym} ({action})"
        elif doc.get("notional") is not None:
            order["notional"] = float(doc["notional"])
            order["params_text"] = f"Text: sell ${float(doc['notional']):,.2f} {sym} ({action})"
        else:
            order["qty"] = float(doc["qty"])
            order["params_text"] = f"Text: sell {sym} qty={doc['qty']} ({action})"
        if action == "LIMIT_SELL":
            order["limit_price"] = float(doc["limit_price"])
            order["params_text"] += f" limit={doc['limit_price']}"
        state.setdefault("orders", []).append(order)
        events.append(f"{now} TEXT queued {oid} {action} {sym}")
        return {"ok": True, "detail": f"queued {oid}"}

    return {"ok": False, "detail": f"unknown action {action}"}


def process_pending(state: dict | None = None) -> dict:
    """Apply all pending text orders. Returns summary; saves state if changes."""
    now = utc_now()
    sync_notes = sync_pending_from_remote()
    PENDING.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)

    own_state = state is None
    if own_state:
        if not STATE_PATH.exists():
            return {"applied": [], "errors": ["missing paper-state.json"], "sync": sync_notes}
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    events = state.setdefault("events", [])
    applied = []
    errors = []

    for path in sorted(PENDING.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if doc.get("status") not in {None, "PENDING"}:
            # already marked — move aside
            dest = PROCESSED / path.name
            shutil.move(str(path), str(dest))
            continue
        result = apply_one(state, doc, events, now)
        doc["status"] = "APPLIED" if result.get("ok") else "ERROR"
        doc["applied_at"] = now
        doc["apply_result"] = result
        dest = PROCESSED / path.name
        dest.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        path.unlink(missing_ok=True)
        if result.get("ok"):
            applied.append({"file": path.name, **result, "text_id": doc.get("id")})
        else:
            errors.append({"file": path.name, **result, "text_id": doc.get("id")})

    state["events"] = events[-400:]
    if applied or errors:
        state["updated"] = now
        if own_state:
            STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    # Always try to clear remote pending after local apply/move so timers don't re-queue.
    if applied or errors or any(PROCESSED.glob("TO-*.json")):
        sync_notes.extend(git_push_processed())

    return {
        "updated": now,
        "applied": applied,
        "errors": errors,
        "sync": sync_notes,
        "state_saved": bool(applied or errors) and own_state,
    }


def main() -> None:
    print(json.dumps(process_pending(), indent=2))


if __name__ == "__main__":
    main()
