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

SYMBOLS = ["UXRP", "GDXU", "SATA", "BTC-USD", "XRP-USD"]

# Email / chat notify ONLY on these fill events — never on marks or price updates.
FILL_EVENTS = {"FILLED_LIMIT", "FILLED_BUY", "FILLED_SELL"}

# Paper daily dividend for SATA (Strive preferred; board-declared; approx).
SATA_DAILY_DIV = 0.0516  # USD per share per U.S. business day (declared rate context)


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


def is_us_business_day(dt: datetime) -> bool:
    return dt.weekday() < 5  # Mon–Fri; ignores market holidays (paper approx)


def credit_sata_dividends(state: dict, now: str, events: list) -> None:
    """Credit paper daily dividends into dividend_cash; never sells SATA."""
    if not is_us_business_day(datetime.now(timezone.utc)):
        return
    day = now[:10]
    if state.get("last_sata_dividend_day") == day:
        return
    pos = next((p for p in state["positions"] if p["symbol"] == "SATA"), None)
    qty = float(pos["qty"]) if pos else 0.0
    if qty <= 0:
        state["last_sata_dividend_day"] = day
        return
    amount = round(qty * SATA_DAILY_DIV, 4)
    state["dividend_cash"] = round(float(state.get("dividend_cash") or 0) + amount, 4)
    state["last_sata_dividend_day"] = day
    state.setdefault("dividend_log", []).append(
        {"date": day, "symbol": "SATA", "qty": qty, "per_share": SATA_DAILY_DIV, "amount": amount}
    )
    state["dividend_log"] = state["dividend_log"][-90:]
    events.append(f"{now} SATA DIVIDEND paper ${amount} ({qty:.4f} × ${SATA_DAILY_DIV}) → dividend_cash")


def queue_sata_profit_buy(state: dict, profit: float, events: list, now: str) -> None:
    """Standing rule: realized trading profit buys SATA; hold for dividends (no sell)."""
    profit = round(float(profit), 2)
    if profit < 1.0:  # ignore dust
        return
    # Merge into existing open SATA profit buy if present
    for o in state["orders"]:
        if (
            o.get("symbol") == "SATA"
            and o.get("type") == "BUY_BEST"
            and o.get("status") in {"OPEN", "WORKING"}
            and o.get("purpose") == "PROFIT_TO_SATA"
        ):
            o["notional"] = round(float(o.get("notional") or 0) + profit, 2)
            o["params_text"] = f"Buy ${o['notional']:.2f} SATA with trading profit. HOLD for daily dividends — do not sell."
            events.append(f"{now} SATA profit-buy notional → ${o['notional']:.2f}")
            return
    n = sum(1 for o in state["orders"] if str(o.get("id", "")).startswith("PB-SATA-")) + 1
    state["orders"].append(
        {
            "id": f"PB-SATA-{n}",
            "symbol": "SATA",
            "type": "BUY_BEST",
            "status": "OPEN",
            "notional": profit,
            "attach_trailing_stop": False,
            "purpose": "PROFIT_TO_SATA",
            "params_text": f"Buy ${profit:.2f} SATA with trading profit. HOLD for daily dividends — do not sell.",
        }
    )
    events.append(f"{now} queued PB-SATA-{n} notional=${profit:.2f}")


def block_sata_sells(order: dict, pos: dict) -> bool:
    """True if this sell must be skipped (SATA hold-for-dividends). Buys still allowed."""
    if order.get("symbol") != "SATA":
        return False
    otype = order.get("type", "")
    if otype not in {
        "SELL_BEST",
        "MARKET_SELL",
        "LIMIT_SELL",
        "TRAILING_STOP_LIMIT_SELL",
    }:
        return False
    if pos.get("no_sell") or pos.get("hold_for_dividends"):
        return True
    return True  # default: never sell SATA under standing policy


def apply_trailing_stop(order: dict, mark: float, position: dict) -> dict:
    """Mutate order/position; return event dict or empty."""
    if order.get("status") in {"FILLED", "CANCELLED"}:
        return {}
    arm = float(order["arm_price"])
    trail = float(order.get("trail_pct", 0.01))
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
        f"**Dividend cash (SATA collected):** {float(state.get('dividend_cash') or 0):,.4f}  ",
        "**Mode:** PAPER only — **auto-execute** open buy/sell orders on each poll  ",
        "**Price feed:** Yahoo Finance v8 1m chart (near-live poll; premarket + regular; may lag)  ",
        "**Email:** only on buy/sell fills — never on mark/price updates  ",
        "",
        "### Standing fill rule (Rodney)",
        "",
        "- **Buys:** best (lowest) available valid quote.",
        "- **Sells:** best (highest) available valid quote.",
        "- **Stop exits:** arm **+2%** from fill, then trail **1%** — **LIMIT** at stop (or better).",
        "- Open paper orders auto-fill when conditions hit (no manual confirm).",
        "- **Profits → SATA:** realized trading profit buys **SATA** at best price; **hold for daily dividends — do not sell**.",
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
        "- Near-live poll ≈ every **10 minutes** while timer active; Yahoo free data can be delayed.",
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
            if block_sata_sells(order, pos):
                events.append(f"{now} {sym} SELL blocked — hold for dividends")
                order["status"] = "CANCELLED"
                continue
            basis_before = float(pos.get("cost_basis") or 0)
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
                realized = round(float(ev["proceeds"]) - basis_before, 2)
                if realized > 0:
                    queue_sata_profit_buy(state, realized, events, now)
            continue

        if otype in {"BUY_BEST", "MARKET_BUY", "LIMIT_BUY", "SELL_BEST", "MARKET_SELL", "LIMIT_SELL"}:
            pos = ensure_position(pos_by_sym, state, sym)
            if block_sata_sells(order, pos):
                events.append(f"{now} {sym} SELL blocked — hold for dividends")
                order["status"] = "CANCELLED"
                continue
            basis_before = float(pos.get("cost_basis") or 0)
            qty_before = float(pos.get("qty") or 0)
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
                if ev.get("event") == "FILLED_BUY" and sym == "SATA":
                    pos["hold_for_dividends"] = True
                    pos["no_sell"] = True
                if ev.get("event") == "FILLED_SELL":
                    # Approx realized on partial/full: use avg cost × qty sold
                    avg = float(pos.get("avg_cost") or 0) if qty_before <= float(ev["qty"]) else (
                        basis_before / qty_before if qty_before else 0
                    )
                    # After sell, avg on remaining is unchanged; cost of sold = avg_before * qty
                    avg_before = basis_before / qty_before if qty_before else 0
                    realized = round(float(ev["proceeds"]) - avg_before * float(ev["qty"]), 2)
                    if realized > 0:
                        queue_sata_profit_buy(state, realized, events, now)
                # Same standing exit rules: +2% arm, then 1% trail, LIMIT sell at stop.
                if (
                    ev.get("event") == "FILLED_BUY"
                    and order.get("attach_trailing_stop", False)
                    and sym != "SATA"
                ):
                    arm_pct = float(order.get("arm_pct", 0.02))
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

    # If profit buys were queued mid-loop, process SATA BUY_BEST once more this poll.
    for order in state["orders"]:
        if order.get("status") in {"FILLED", "CANCELLED"}:
            continue
        if not (order.get("symbol") == "SATA" and order.get("type") == "BUY_BEST"):
            continue
        quote = marks.get("SATA", {})
        mark = quote.get("mark")
        if mark is None or not quote.get("fresh", True):
            continue
        pos = ensure_position(pos_by_sym, state, "SATA")
        ev, cash = apply_buy_sell_order(order, float(mark), pos, cash)
        if not ev:
            continue
        events.append(f"{now} SATA mark={mark:.4f} {ev}")
        if ev.get("event") in FILL_EVENTS:
            fills.append(ev)
            pos["hold_for_dividends"] = True
            pos["no_sell"] = True
            fill_px = float(ev.get("price") or mark)
            state.setdefault("trade_log", []).append(
                {
                    "time": now,
                    "side": "BUY",
                    "symbol": "SATA",
                    "qty": ev["qty"],
                    "price": fill_px,
                    "cash_after": cash,
                    "rationale": f"Profit→SATA {order['id']} auto-filled; hold for dividends",
                }
            )

    state["cash"] = cash
    credit_sata_dividends(state, now, events)

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
        "dividend_cash": state.get("dividend_cash", 0),
        "big_items": fills,  # buy/sell fills only; empty ⇒ no email
        "events_tail": events[-5:],
        "note": "Never email on mark updates; email only if big_items non-empty",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
