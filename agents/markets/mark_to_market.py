#!/usr/bin/env python3
"""Near-live Yahoo Finance marks + auto paper order execution (poll; not tick stream)."""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "paper-state.json"
MARKS_PATH = ROOT / "last_marks.json"
PORTFOLIO_MD = ROOT / "paper-portfolio.md"
UA = {"User-Agent": "Mozilla/5.0 (compatible; JohnMarkBot/1.0)"}

SYMBOLS = ["UXRP", "GDXU", "BTC-USD", "XRP-USD"]

# Email / chat notify ONLY on these fill events — never on marks or price updates.
FILL_EVENTS = {"FILLED_LIMIT", "FILLED_BUY", "FILLED_SELL"}


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
    last_1m = None
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


def ensure_position(pos_by_sym: dict, state: dict, symbol: str) -> dict:
    if symbol in pos_by_sym:
        return pos_by_sym[symbol]
    pos = {"symbol": symbol, "qty": 0.0, "avg_cost": 0.0, "cost_basis": 0.0}
    state["positions"].append(pos)
    pos_by_sym[symbol] = pos
    return pos


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
            # Limit sell at stop: paper-fill only if mark >= stop (limit or better for sells).
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
                        "side": "SELL",
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
            event.update(
                {
                    "event": "FILLED_LIMIT",
                    "side": "SELL",
                    "limit": limit,
                    "qty": qty,
                    "proceeds": proceeds,
                }
            )
            position["qty"] = 0.0
            position["cost_basis"] = 0.0
            return event
        event["event"] = "WORKING_LIMIT"
        event["limit"] = limit
        return event

    return {}


def apply_buy_sell_order(order: dict, mark: float, position: dict, cash: float) -> tuple[dict, float]:
    """Auto-execute standing paper BUY/SELL orders at best available mark. Returns (event, new_cash)."""
    if order.get("status") in {"FILLED", "CANCELLED"}:
        return {}, cash

    otype = order.get("type", "")
    status = order.get("status", "OPEN")
    event = {"id": order["id"], "symbol": order["symbol"]}

    # Immediate best-price buy (uses current fresh mark as best available print).
    if otype in {"BUY_BEST", "MARKET_BUY"} and status in {"OPEN", "WORKING"}:
        notional = order.get("notional")
        qty = order.get("qty")
        if notional is not None:
            qty = float(notional) / mark
        else:
            qty = float(qty or 0)
        cost = round(qty * mark, 2)
        if qty <= 0 or cost > cash + 1e-9:
            event["event"] = "BUY_BLOCKED_CASH"
            return event, cash
        # Best buy = lowest valid quote → fill at mark (proxy for best available on this poll).
        prev_qty = float(position["qty"])
        prev_basis = float(position["cost_basis"])
        new_qty = prev_qty + qty
        new_basis = prev_basis + cost
        position["qty"] = new_qty
        position["cost_basis"] = round(new_basis, 2)
        position["avg_cost"] = round(new_basis / new_qty, 6) if new_qty else 0.0
        cash = round(cash - cost, 2)
        order["status"] = "FILLED"
        order["fill_price"] = mark
        order["fill_qty"] = qty
        event.update({"event": "FILLED_BUY", "side": "BUY", "qty": qty, "price": mark, "cost": cost})
        return event, cash

    # Limit buy: fill when mark <= limit (best price at or below limit).
    if otype == "LIMIT_BUY" and status in {"OPEN", "WORKING"}:
        limit = float(order["limit_price"])
        if mark <= limit + 1e-9:
            fill_px = mark  # best (lowest) available at or under limit
            notional = order.get("notional")
            qty = order.get("qty")
            if notional is not None:
                qty = float(notional) / fill_px
            else:
                qty = float(qty or 0)
            cost = round(qty * fill_px, 2)
            if qty <= 0 or cost > cash + 1e-9:
                event["event"] = "BUY_BLOCKED_CASH"
                return event, cash
            prev_qty = float(position["qty"])
            prev_basis = float(position["cost_basis"])
            new_qty = prev_qty + qty
            new_basis = prev_basis + cost
            position["qty"] = new_qty
            position["cost_basis"] = round(new_basis, 2)
            position["avg_cost"] = round(new_basis / new_qty, 6) if new_qty else 0.0
            cash = round(cash - cost, 2)
            order["status"] = "FILLED"
            order["fill_price"] = fill_px
            order["fill_qty"] = qty
            event.update(
                {"event": "FILLED_BUY", "side": "BUY", "qty": qty, "price": fill_px, "cost": cost, "limit": limit}
            )
            return event, cash
        event["event"] = "WORKING_BUY"
        event["limit"] = limit
        return event, cash

    # Immediate best-price sell.
    if otype in {"SELL_BEST", "MARKET_SELL"} and status in {"OPEN", "WORKING"}:
        qty = float(order.get("qty") or position["qty"])
        avail = float(position["qty"])
        if qty <= 0 or qty > avail + 1e-9:
            event["event"] = "SELL_BLOCKED_QTY"
            return event, cash
        # Best sell = highest valid quote → fill at mark.
        proceeds = round(qty * mark, 2)
        basis = float(position["cost_basis"])
        avg = float(position["avg_cost"])
        rem = avail - qty
        position["qty"] = rem
        position["cost_basis"] = round(avg * rem, 2) if rem > 0 else 0.0
        if rem <= 0:
            position["avg_cost"] = 0.0
        cash = round(cash + proceeds, 2)
        order["status"] = "FILLED"
        order["fill_price"] = mark
        order["fill_qty"] = qty
        event.update(
            {
                "event": "FILLED_SELL",
                "side": "SELL",
                "qty": qty,
                "price": mark,
                "proceeds": proceeds,
                "basis_released": round(basis - float(position["cost_basis"]), 2),
            }
        )
        return event, cash

    # Limit sell: fill when mark >= limit (best price at or above limit).
    if otype == "LIMIT_SELL" and status in {"OPEN", "WORKING"}:
        limit = float(order["limit_price"])
        if mark + 1e-9 >= limit:
            fill_px = mark  # best (highest) available at or over limit
            qty = float(order.get("qty") or position["qty"])
            avail = float(position["qty"])
            if qty <= 0 or qty > avail + 1e-9:
                event["event"] = "SELL_BLOCKED_QTY"
                return event, cash
            proceeds = round(qty * fill_px, 2)
            avg = float(position["avg_cost"])
            rem = avail - qty
            position["qty"] = rem
            position["cost_basis"] = round(avg * rem, 2) if rem > 0 else 0.0
            if rem <= 0:
                position["avg_cost"] = 0.0
            cash = round(cash + proceeds, 2)
            order["status"] = "FILLED"
            order["fill_price"] = fill_px
            order["fill_qty"] = qty
            event.update(
                {
                    "event": "FILLED_SELL",
                    "side": "SELL",
                    "qty": qty,
                    "price": fill_px,
                    "proceeds": proceeds,
                    "limit": limit,
                }
            )
            return event, cash
        event["event"] = "WORKING_SELL"
        event["limit"] = limit
        return event, cash

    return {}, cash


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
        "**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  ",
        "**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  ",
        "**Email:** only on buy/sell fills — never on mark/price updates  ",
        "",
        "### Standing fill rule (Rodney)",
        "",
        "- **Buys:** best (lowest) available valid quote.",
        "- **Sells:** best (highest) available valid quote.",
        "- **Stop exits:** **LIMIT** at stop (or better) — never market.",
        "- Open paper orders auto-fill when conditions hit (no manual confirm).",
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
        if o.get("status") in {"FILLED", "CANCELLED"}:
            continue
        params = o.get("params_text") or json.dumps(
            {
                k: o.get(k)
                for k in ("arm_price", "trail_pct", "stop", "high_water", "limit_price", "qty", "notional")
                if o.get(k) is not None
            }
        )
        lines.append(f"| {o['id']} | {o['symbol']} | {o['type']} | **{o['status']}** | {params} |")

    lines += ["", "## Trade log (buys/sells)", ""]
    for t in state.get("trade_log", [])[-12:]:
        lines.append(
            f"- {t.get('time')} **{t.get('side')}** {t.get('symbol')} qty={t.get('qty')} @ ${t.get('price')} → cash ${t.get('cash_after')}"
        )
    if not state.get("trade_log"):
        lines.append("- (none yet)")

    lines += ["", "## Recent events", ""]
    for e in state.get("events", [])[-12:]:
        lines.append(f"- {e}")
    lines += [
        "",
        "## Rules",
        "",
        "- Simulated only. Not advice.",
        "- Near-live poll ≈ every 60s while timer active; Yahoo free data can be delayed.",
        "- **Do not email** on price/mark updates — email only when a buy or sell fills.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    marks = {s: fetch_yahoo(s) for s in SYMBOLS}
    MARKS_PATH.write_text(json.dumps({"updated": now, "marks": marks}, indent=2) + "\n")

    state = load_state()
    state["updated"] = now
    state["auto_execute"] = True
    events = []
    fills = []  # only buy/sell fills — email-worthy

    pos_by_sym = {p["symbol"]: p for p in state["positions"]}
    cash = float(state["cash"])

    for order in state["orders"]:
        if order.get("status") in {"FILLED", "CANCELLED"}:
            continue
        sym = order["symbol"]
        quote = marks.get(sym, {})
        mark = quote.get("mark")
        if mark is None:
            continue

        otype = order.get("type", "")

        # Do not execute equity/crypto orders on stale last-close prints.
        if not quote.get("fresh", True):
            events.append(
                f"{now} {sym} STALE_QUOTE age={quote.get('quote_age_sec')}s mark={mark} — order logic skipped"
            )
            continue

        if otype == "TRAILING_STOP_LIMIT_SELL":
            pos = ensure_position(pos_by_sym, state, sym)
            if float(pos["qty"]) <= 0:
                continue
            ev = apply_trailing_stop(order, float(mark), pos)
            if not ev:
                continue
            msg = f"{now} {sym} mark={mark:.4f} {ev}"
            events.append(msg)
            if ev.get("event") in FILL_EVENTS:
                fills.append(ev)
                cash = round(cash + float(ev["proceeds"]), 2)
                state.setdefault("trade_log", []).append(
                    {
                        "time": now,
                        "side": "SELL_LIMIT",
                        "symbol": sym,
                        "qty": ev["qty"],
                        "price": ev["limit"],
                        "cash_after": cash,
                        "rationale": f"Trailing stop-limit {order['id']} auto-filled",
                    }
                )
            continue

        if otype in {"BUY_BEST", "MARKET_BUY", "LIMIT_BUY", "SELL_BEST", "MARKET_SELL", "LIMIT_SELL"}:
            pos = ensure_position(pos_by_sym, state, sym)
            ev, cash = apply_buy_sell_order(order, float(mark), pos, cash)
            if not ev:
                continue
            msg = f"{now} {sym} mark={mark:.4f} {ev}"
            events.append(msg)
            if ev.get("event") in FILL_EVENTS:
                fills.append(ev)
                side = "BUY" if ev["event"] == "FILLED_BUY" else "SELL"
                fill_px = float(ev.get("price") or ev.get("limit"))
                state.setdefault("trade_log", []).append(
                    {
                        "time": now,
                        "side": side,
                        "symbol": sym,
                        "qty": ev["qty"],
                        "price": fill_px,
                        "cash_after": cash,
                        "rationale": f"{otype} {order['id']} auto-filled at best available",
                    }
                )
                # Same standing exit rules: +2% arm, 2% trail, LIMIT sell at stop.
                if (
                    ev.get("event") == "FILLED_BUY"
                    and order.get("attach_trailing_stop", False)
                ):
                    arm_pct = float(order.get("arm_pct", 0.02))
                    # Standing rule: trail 1% after +2% arm (Rodney 2026-09-28).
                    trail_pct = float(order.get("trail_pct", 0.01))
                    arm = round(fill_px * (1 + arm_pct), 4)
                    n = sum(1 for o in state["orders"] if o.get("symbol") == sym and o.get("type") == "TRAILING_STOP_LIMIT_SELL") + 1
                    ts = {
                        "id": f"TS-{sym}-{n}",
                        "symbol": sym,
                        "type": "TRAILING_STOP_LIMIT_SELL",
                        "status": "PENDING_ARM",
                        "arm_price": arm,
                        "trail_pct": trail_pct,
                        "params_text": f"Arm +{arm_pct*100:.0f}% → ${arm}. Trail {trail_pct*100:.0f}%. LIMIT sell at stop.",
                    }
                    state["orders"].append(ts)
                    events.append(f"{now} {sym} attached {ts['id']} PENDING_ARM arm={arm}")

    state["cash"] = cash

    for p in state["positions"]:
        qty = float(p["qty"])
        if qty <= 0:
            continue
        mark = marks.get(p["symbol"], {}).get("mark")
        if mark is None:
            continue
        basis = float(p["cost_basis"])
        upl_pct = (qty * mark - basis) / basis * 100 if basis else 0
        p["last_upl_pct"] = round(upl_pct, 2)
        # Marks / UPL are never email-worthy.

    state.setdefault("events", [])
    state["events"].extend(events[-20:])
    state["events"] = state["events"][-50:]
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
    PORTFOLIO_MD.write_text(render_md(state, marks))

    summary = {
        "updated": now,
        "marks": {k: v.get("mark") for k, v in marks.items()},
        "cash": state["cash"],
        "big_items": fills,  # buy/sell fills only; empty ⇒ no email
        "events_tail": events[-5:],
        "note": "Never email on mark updates; email only if big_items non-empty",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
