#!/usr/bin/env python3
"""Parse a Rodney text-trade command, write pending JSON, commit+push text-orders only."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PENDING = ROOT / "text-orders" / "pending"
PROCESSED = ROOT / "text-orders" / "processed"
REPO = ROOT.parent.parent  # workspace root


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_money(token: str) -> float | None:
    t = token.strip().upper().replace(",", "")
    t = t.replace("$", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(K)?", t)
    if not m:
        return None
    val = float(m.group(1))
    if m.group(2):
        val *= 1000.0
    return val


def parse_command(raw: str) -> dict:
    text = " ".join(raw.strip().split())
    upper = text.upper()
    if upper in {"STATUS", "PORTFOLIO", "BALANCES", "BALANCE"}:
        return {"action": "STATUS", "raw_text": text}

    # CANCEL <id>  or  CANCEL BUYS/SHORTS <SYM>
    m = re.match(r"^CANCEL\s+BUYS?\s+([A-Z][A-Z0-9.\-]*)\s*$", upper)
    if m:
        return {
            "action": "CANCEL_BUYS",
            "symbol": m.group(1),
            "raw_text": text,
        }
    m = re.match(r"^CANCEL\s+SHORTS?\s+([A-Z][A-Z0-9.\-]*)\s*$", upper)
    if m:
        return {
            "action": "CANCEL_SHORTS",
            "symbol": m.group(1),
            "raw_text": text,
        }
    m = re.match(r"^CANCEL\s+([A-Z0-9][A-Z0-9.\-]*)\s*$", upper)
    if m:
        return {
            "action": "CANCEL",
            "cancel_order_id": m.group(1),
            "raw_text": text,
        }

    # BUY SYM $notional LIMIT price | BEST
    m = re.match(
        r"^BUY\s+([A-Z][A-Z0-9.\-]*)\s+(\$?[\d,.]+K?)\s+(LIMIT\s+(\d+(?:\.\d+)?)|BEST|MKT|MARKET)\s*$",
        upper,
    )
    if m:
        sym = m.group(1)
        notional = parse_money(m.group(2))
        if notional is None or notional <= 0:
            raise ValueError(f"bad notional: {m.group(2)}")
        if m.group(3).startswith("LIMIT"):
            return {
                "action": "LIMIT_BUY",
                "symbol": sym,
                "notional": notional,
                "limit_price": float(m.group(4)),
                "attach_exits": True,
                "raw_text": text,
            }
        return {
            "action": "BUY_BEST",
            "symbol": sym,
            "notional": notional,
            "attach_exits": True,
            "raw_text": text,
        }

    # SELL SYM ALL BEST|LIMIT p
    m = re.match(
        r"^SELL\s+([A-Z][A-Z0-9.\-]*)\s+ALL\s+(LIMIT\s+(\d+(?:\.\d+)?)|BEST|MKT|MARKET)\s*$",
        upper,
    )
    if m:
        sym = m.group(1)
        if m.group(2).startswith("LIMIT"):
            return {
                "action": "LIMIT_SELL",
                "symbol": sym,
                "qty_all": True,
                "limit_price": float(m.group(3)),
                "raw_text": text,
            }
        return {
            "action": "SELL_BEST",
            "symbol": sym,
            "qty_all": True,
            "raw_text": text,
        }

    # SELL SYM QTY n LIMIT p
    m = re.match(
        r"^SELL\s+([A-Z][A-Z0-9.\-]*)\s+QTY\s+(\d+(?:\.\d+)?)\s+LIMIT\s+(\d+(?:\.\d+)?)\s*$",
        upper,
    )
    if m:
        return {
            "action": "LIMIT_SELL",
            "symbol": m.group(1),
            "qty": float(m.group(2)),
            "qty_all": False,
            "limit_price": float(m.group(3)),
            "raw_text": text,
        }

    # SHORT SYM $notional LIMIT price | BEST
    m = re.match(
        r"^SHORT\s+([A-Z][A-Z0-9.\-]*)\s+(\$?[\d,.]+K?)\s+(LIMIT\s+(\d+(?:\.\d+)?)|BEST|MKT|MARKET)\s*$",
        upper,
    )
    if m:
        sym = m.group(1)
        notional = parse_money(m.group(2))
        if notional is None or notional <= 0:
            raise ValueError(f"bad notional: {m.group(2)}")
        if m.group(3).startswith("LIMIT"):
            return {
                "action": "LIMIT_SHORT",
                "symbol": sym,
                "notional": notional,
                "limit_price": float(m.group(4)),
                "attach_exits": True,
                "raw_text": text,
            }
        return {
            "action": "SHORT_BEST",
            "symbol": sym,
            "notional": notional,
            "attach_exits": True,
            "raw_text": text,
        }

    # COVER SYM ALL BEST|LIMIT p
    m = re.match(
        r"^COVER\s+([A-Z][A-Z0-9.\-]*)\s+ALL\s+(LIMIT\s+(\d+(?:\.\d+)?)|BEST|MKT|MARKET)\s*$",
        upper,
    )
    if m:
        sym = m.group(1)
        if m.group(2).startswith("LIMIT"):
            return {
                "action": "LIMIT_COVER",
                "symbol": sym,
                "qty_all": True,
                "limit_price": float(m.group(3)),
                "raw_text": text,
            }
        return {
            "action": "COVER_BEST",
            "symbol": sym,
            "qty_all": True,
            "raw_text": text,
        }

    # COVER SYM QTY n LIMIT p
    m = re.match(
        r"^COVER\s+([A-Z][A-Z0-9.\-]*)\s+QTY\s+(\d+(?:\.\d+)?)\s+LIMIT\s+(\d+(?:\.\d+)?)\s*$",
        upper,
    )
    if m:
        return {
            "action": "LIMIT_COVER",
            "symbol": m.group(1),
            "qty": float(m.group(2)),
            "qty_all": False,
            "limit_price": float(m.group(3)),
            "raw_text": text,
        }

    raise ValueError(
        "Could not parse. Examples: BUY UXRP $50000 LIMIT 17 | SHORT UXRP $1000 LIMIT 16 | "
        "COVER UXRP ALL BEST | SELL GDXU ALL BEST | CANCEL LB-UXRP-4 | CANCEL BUYS UXRP | "
        "CANCEL SHORTS UXRP | STATUS"
    )


def git_push_pending(path: Path) -> None:
    rel = path.relative_to(REPO)
    subprocess.run(["git", "add", str(rel)], cwd=REPO, check=True)
    # Also keep README / processed dir scaffolding tracked if needed
    subprocess.run(
        ["git", "add", "agents/markets/text-orders/README.md"],
        cwd=REPO,
        check=False,
    )
    msg = f"Text order queue: {path.name}"
    subprocess.run(["git", "commit", "-m", msg], cwd=REPO, check=True)
    # Push current branch
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO, text=True
    ).strip()
    subprocess.run(["git", "push", "-u", "origin", branch], cwd=REPO, check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Queue a paper text order for John Cloud")
    ap.add_argument("--text", help="Full command text from Rodney")
    ap.add_argument("--from-e164", default="+18173715555")
    ap.add_argument("--no-git", action="store_true", help="Write file only (tests)")
    ap.add_argument("--json-out", action="store_true")
    args = ap.parse_args()
    if not args.text:
        print("ERROR: --text required", file=sys.stderr)
        return 2

    try:
        parsed = parse_command(args.text)
    except ValueError as exc:
        out = {"ok": False, "error": str(exc)}
        print(json.dumps(out, indent=2) if args.json_out else f"ERROR: {exc}")
        return 1

    if parsed["action"] == "STATUS":
        out = {
            "ok": True,
            "action": "STATUS",
            "reply": (
                "Paper book runs on John Cloud. Fills email regiaemanagementllc@gmail.com. "
                "For a live book snapshot, ask John Cloud in Cursor — or send BUY/SELL/CANCEL here."
            ),
        }
        print(json.dumps(out, indent=2) if args.json_out else out["reply"])
        return 0

    PENDING.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    oid = f"TO-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    doc = {
        "id": oid,
        "source": "imessage",
        "from": args.from_e164,
        "created": utc_now(),
        "status": "PENDING",
        **parsed,
    }
    path = PENDING / f"{oid}.json"
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    if not args.no_git:
        try:
            git_push_pending(path)
        except subprocess.CalledProcessError as exc:
            out = {
                "ok": False,
                "error": f"queued locally but git failed: {exc}",
                "path": str(path),
                "order": doc,
            }
            print(json.dumps(out, indent=2))
            return 1

    out = {
        "ok": True,
        "order_id": oid,
        "path": str(path),
        "order": doc,
        "reply": (
            f"Queued {doc['action']} {doc.get('symbol', '')} "
            f"(id {oid}) for John Cloud paper — usually within ~5 minutes in market hours."
        ).strip(),
    }
    print(json.dumps(out, indent=2) if args.json_out else out["reply"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
