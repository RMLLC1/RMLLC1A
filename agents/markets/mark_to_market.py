#!/usr/bin/env python3
"""Near-live Yahoo Finance marks for paper portfolio (poll; not tick stream)."""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "paper-state.json"
MARKS_PATH = ROOT / "last_marks.json"
PORTFOLIO_MD = ROOT / "paper-portfolio.md"
UA = {"User-Agent": "Mozilla/5.0 (compatible; JohnMarkBot/1.0)"}

SYMBOLS = ["UXRP", "GDXU", "BTC-USD", "XRP-USD"]


def fetch_yahoo(symbol: str) -> dict:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        "?interval=1m&range=1d&includePrePost=true"
    )
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.load(resp)
    result = payload["chart"]["result"][0]
    meta = result["meta"]
    timestamps = result.get("timestamp") or []
    closes = (result.get("indicators", {}).get("quote") or [{}])[0].get("close") or []
    lasts = [c for c in closes if c is not None]
    last_1m = float(lasts[-1]) if lasts else None
    # Pair last non-null close with its timestamp when possible.
    last_ts = None
    if timestamps and closes:
        for ts, cl in zip(reversed(timestamps), reversed(closes)):
            if cl is not None:
                last_ts = int(ts)
                last_1m = float(cl)
                break
    regular = meta.get("regularMarketPrice")
    previous = meta.get("previousClose") or meta.get("chartPreviousClose")
    mark = last_1m if last_1m is not None else regular
    rtime = last_ts or meta.get("regularMarketTime")
    age_sec = None
    fresh = True
    if rtime is not None:
        age_sec = int(datetime.now(timezone.utc).timestamp() - int(rtime))
        # Allow up to ~15 min staleness for 1m polling; crypto usually fresher.
        fresh = age_sec <= 15 * 60
    return {
        "symbol": symbol,
        "mark": float(mark) if mark is not None else None,
        "regularMarketPrice": regular,
        "previousClose": previous,
        "last_1m": last_1m,
        "regularMarketTime": meta.get("regularMarketTime"),
        "bar_time": last_ts,
        "quote_age_sec": age_sec,
        "fresh": fresh,
        "instrumentType": meta.get("instrumentType"),
        "exchangeTimezoneName": meta.get("exchangeTimezoneName"),
        "source": "yahoo_v8_chart_1m",
    }


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    raise SystemExit(f"missing {STATE_PATH}")


def apply_trailing_stop(order: dict, mark: float, position: dict) -> dict:
    """Mutate order/position; return event dict or empty."""
    if order.get("status") in {"FILLED", "CANCELLED"}:
        return {}
    arm = float(order["arm_price"])
    trail = float(order.get("trail_pct", 0.02))
    event = {"id": order["id"], "symbol": order["symbol"]}

    if order["status"] == "PENDING_ARM":
        if mark >= arm:
            order["status"] = "ARMED"
            order["high_water"] = mark
            order["stop"] = round(mark * (1 - trail), 4)
            event["event"] = "ARMED"
            event["high_water"] = order["high_water"]
            event["stop"] = order["stop"]
            return event
        event["event"] = "PENDING_ARM"
        return event

    if order["status"] == "ARMED":
        hw = float(order.get("high_water") or mark)
        if mark > hw:
            order["high_water"] = mark
            order["stop"] = round(mark * (1 - trail), 4)
            event["event"] = "TRAILED"
            event["high_water"] = order["high_water"]
            event["stop"] = order["stop"]
            return event
        stop = float(order["stop"])
        if mark <= stop:
            # Limit sell at stop: paper-fill only if mark >= stop (limit or better for sells = higher).
            # At exact trigger mark == stop is fillable; if mark gapped below stop, leave WORKING_LIMIT.
            limit = stop
            if mark + 1e-9 >= limit:
                qty = float(position["qty"])
                proceeds = round(qty * limit, 2)
                order["status"] = "FILLED"
                order["fill_price"] = limit
                order["fill_qty"] = qty
                event.update(
                    {
                        "event": "FILLED_LIMIT",
                        "limit": limit,
                        "qty": qty,
                        "proceeds": proceeds,
                    }
                )
                position["qty"] = 0.0
                position["cost_basis"] = 0.0
                return event
            order["status"] = "WORKING_LIMIT"
            order["limit_price"] = limit
            event["event"] = "WORKING_LIMIT"
            event["limit"] = limit
            event["mark"] = mark
            return event
        event["event"] = "ARMED_HOLD"
        event["stop"] = stop
        return event

    if order["status"] == "WORKING_LIMIT":
        limit = float(order["limit_price"])
        if mark + 1e-9 >= limit:
            qty = float(position["qty"])
            proceeds = round(qty * limit, 2)
            order["status"] = "FILLED"
            order["fill_price"] = limit
            event.update({"event": "FILLED_LIMIT", "limit": limit, "qty": qty, "proceeds": proceeds})
            position["qty"] = 0.0
            position["cost_basis"] = 0.0
            return event
        event["event"] = "WORKING_LIMIT"
        event["limit"] = limit
        return event

    return {}


def render_md(state: dict, marks: dict) -> str:
    now = state["updated"]
    cash = state["cash"]
    lines = [
        "# Paper portfolio (SIMULATED — not real money)",
        "",
        f"**Updated:** {now}  ",
        "**Base currency:** USD  ",
        f"**Starting cash:** {state['starting_cash']:,.2f}  ",
        f"**Cash:** {cash:,.2f}  ",
        "**Mode:** PAPER only  ",
        "**Price feed:** Yahoo Finance v8 1m chart (near-live poll; may lag / miss thin premarket prints)  ",
        "",
        "### Standing fill rule (Rodney)",
        "",
        "- **Buys:** best (lowest) available valid quote.",
        "- **Sells:** best (highest) available valid quote.",
        "- **Stop exits:** **LIMIT** at stop (or better) — never market.",
        "",
        "**Marks:**",
    ]
    for sym, m in marks.items():
        if m.get("mark") is not None:
            lines.append(f"- {sym}: **${m['mark']:.4f}** ({m.get('source')})")
    lines += ["", "## Positions", "", "| Symbol | Qty | Avg cost | Cost basis | Mark | UPL |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for p in state["positions"]:
        sym = p["symbol"]
        qty = float(p["qty"])
        if qty <= 0:
            continue
        avg = float(p["avg_cost"])
        basis = float(p["cost_basis"])
        mark = float(marks.get(sym, {}).get("mark") or avg)
        upl = round(qty * mark - basis, 2)
        lines.append(f"| {sym} | {qty:.4f} | {avg:.4f} | {basis:,.2f} | {mark:.4f} | {upl:,.2f} |")

    lines += ["", "## Open orders (PAPER)", "", "| ID | Symbol | Type | Status | Params |", "| --- | --- | --- | --- | --- |"]
    for o in state["orders"]:
        params = o.get("params_text") or json.dumps({k: o.get(k) for k in ("arm_price", "trail_pct", "stop", "high_water", "limit_price") if o.get(k) is not None})
        lines.append(f"| {o['id']} | {o['symbol']} | {o['type']} | **{o['status']}** | {params} |")

    lines += ["", "## Recent events", ""]
    for e in state.get("events", [])[-12:]:
        lines.append(f"- {e}")
    lines += [
        "",
        "## Rules",
        "",
        "- Simulated only. Not advice.",
        "- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    marks = {s: fetch_yahoo(s) for s in SYMBOLS}
    MARKS_PATH.write_text(json.dumps({"updated": now, "marks": marks}, indent=2) + "\n")

    state = load_state()
    state["updated"] = now
    events = []
    big = []

    pos_by_sym = {p["symbol"]: p for p in state["positions"]}
    for order in state["orders"]:
        sym = order["symbol"]
        quote = marks.get(sym, {})
        mark = quote.get("mark")
        if mark is None or sym not in pos_by_sym:
            continue
        if float(pos_by_sym[sym]["qty"]) <= 0 and order["status"] not in {"FILLED", "CANCELLED"}:
            continue
        # Do not arm/trigger equity stops on stale last-close prints (common in free Yahoo premarket).
        if not quote.get("fresh", True):
            events.append(
                f"{now} {sym} STALE_QUOTE age={quote.get('quote_age_sec')}s mark={mark} — stop logic skipped"
            )
            continue
        ev = apply_trailing_stop(order, float(mark), pos_by_sym[sym])
        if not ev:
            continue
        msg = f"{now} {sym} mark={mark:.4f} {ev}"
        events.append(msg)
        if ev.get("event") in {"ARMED", "FILLED_LIMIT", "WORKING_LIMIT"}:
            big.append(ev)
        if ev.get("event") == "FILLED_LIMIT":
            state["cash"] = round(float(state["cash"]) + float(ev["proceeds"]), 2)
            state.setdefault("trade_log", []).append(
                {
                    "time": now,
                    "side": "SELL_LIMIT",
                    "symbol": sym,
                    "qty": ev["qty"],
                    "price": ev["limit"],
                    "cash_after": state["cash"],
                    "rationale": f"Trailing stop-limit {order['id']} filled",
                }
            )

    # Material UPL move > 5% on a position vs cost
    for p in state["positions"]:
        qty = float(p["qty"])
        if qty <= 0:
            continue
        mark = marks.get(p["symbol"], {}).get("mark")
        if mark is None:
            continue
        basis = float(p["cost_basis"])
        upl_pct = (qty * mark - basis) / basis * 100 if basis else 0
        prev = p.get("last_upl_pct")
        p["last_upl_pct"] = round(upl_pct, 2)
        if prev is not None and abs(upl_pct - prev) >= 5:
            big.append({"event": "UPL_MOVE", "symbol": p["symbol"], "upl_pct": round(upl_pct, 2)})

    state.setdefault("events", [])
    state["events"].extend(events[-20:])
    state["events"] = state["events"][-50:]
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
    PORTFOLIO_MD.write_text(render_md(state, marks))

    summary = {
        "updated": now,
        "marks": {k: v.get("mark") for k, v in marks.items()},
        "cash": state["cash"],
        "big_items": big,
        "events_tail": events[-5:],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
