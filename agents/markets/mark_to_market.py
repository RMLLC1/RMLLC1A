#!/usr/bin/env python3
"""Near-live Yahoo Finance marks + auto paper order execution (poll; not tick stream)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "paper-state.json"
MARKS_PATH = ROOT / "last_marks.json"
PORTFOLIO_MD = ROOT / "paper-portfolio.md"
UA = {"User-Agent": "Mozilla/5.0 (compatible; JohnMarkBot/1.0)"}
NY_TZ = ZoneInfo("America/New_York")

# NYSE extended session (Yahoo/broker typical): premarket 4:00 AM – after-hours 8:00 PM ET, weekdays.
SESSION_OPEN = time(4, 0)
SESSION_CLOSE = time(20, 0)  # inclusive through 8:00 PM ET

SYMBOLS = ["UXRP", "GDXU", "SATA", "BTC-USD", "XRP-USD"]

# Email / chat notify ONLY on these fill events — never on marks or price updates.
FILL_EVENTS = {"FILLED_LIMIT", "FILLED_BUY", "FILLED_SELL", "FILLED_MARKET"}

# Paper daily dividend for SATA (Strive preferred; board-declared; approx).
SATA_DAILY_DIV = 0.0516  # USD per share per U.S. business day (declared rate context)

# Standing cash floor (Rodney): when cash is below this, sell SATA to top up.
CASH_FLOOR_USD = 100_000.0


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


def _queue_sata_buy(
    state: dict,
    notional: float,
    purpose: str,
    params_text: str,
    events: list,
    now: str,
) -> None:
    """Queue SATA BUY_BEST (no stops). Merges into an open order with the same purpose."""
    notional = round(float(notional), 2)
    if notional < 1.0:
        return
    for o in state["orders"]:
        if (
            o.get("symbol") == "SATA"
            and o.get("type") == "BUY_BEST"
            and o.get("status") in {"OPEN", "WORKING"}
            and o.get("purpose") == purpose
        ):
            o["notional"] = round(float(o.get("notional") or 0) + notional, 2)
            o["params_text"] = params_text.replace("${NOTIONAL}", f"${o['notional']:.2f}")
            events.append(f"{now} SATA {purpose} notional → ${o['notional']:.2f}")
            return
    n = sum(1 for o in state["orders"] if str(o.get("id", "")).startswith("PB-SATA-")) + 1
    oid = f"PB-SATA-{n}"
    state["orders"].append(
        {
            "id": oid,
            "symbol": "SATA",
            "type": "BUY_BEST",
            "status": "OPEN",
            "notional": notional,
            "attach_trailing_stop": False,
            "purpose": purpose,
            "params_text": params_text.replace("${NOTIONAL}", f"${notional:.2f}"),
        }
    )
    events.append(f"{now} queued {oid} ${notional:.2f} ({purpose})")


def queue_sata_profit_buy(state: dict, profit: float, events: list, now: str) -> float:
    """Trading profit → SATA; sweep any sub-share dividend_cash into the same buy."""
    profit = round(float(profit), 2)
    div = round(float(state.get("dividend_cash") or 0), 4)
    div_sweep = 0.0
    if div > 0:
        state["dividend_cash"] = 0
        div_sweep = div
        events.append(
            f"{now} merged ${div:.4f} dividend_cash into profit→SATA buy (below 1-share reinvest threshold alone)"
        )
    notional = round(profit + div_sweep, 2)
    if notional < 1.0:
        if div_sweep > 0:
            state["dividend_cash"] = div_sweep
        return 0.0
    _queue_sata_buy(
        state,
        notional,
        "PROFIT_TO_SATA",
        "Buy ${NOTIONAL} SATA (trading profit + any dividend cash). HOLD for daily dividends — do not sell.",
        events,
        now,
    )
    return div_sweep


def try_reinvest_dividend_cash(
    state: dict, sata_mark: float | None, events: list, now: str
) -> float:
    """When dividend_cash alone can buy ≥1 SATA share, reinvest at best. Returns cash to add."""
    if sata_mark is None or sata_mark <= 0:
        return 0.0
    div = round(float(state.get("dividend_cash") or 0), 4)
    if div < float(sata_mark):
        return 0.0
    state["dividend_cash"] = 0
    _queue_sata_buy(
        state,
        div,
        "DIVIDEND_REINVEST",
        "Reinvest ${NOTIONAL} SATA dividend cash. HOLD for daily dividends — do not sell.",
        events,
        now,
    )
    events.append(f"{now} dividend_cash ${div:.4f} → SATA reinvest (≥1 share @ ~${sata_mark:.2f})")
    return div


def _trading_loss_total(fills: list) -> float:
    """Sum of realized losses on non-SATA sells this poll (positive dollars lost)."""
    lost = 0.0
    for ev in fills or []:
        if ev.get("symbol") == "SATA":
            continue
        if ev.get("event") not in {"FILLED_SELL", "FILLED_LIMIT"}:
            continue
        if ev.get("side") not in {None, "SELL"}:
            continue
        realized = ev.get("realized")
        if realized is None:
            continue
        realized = float(realized)
        if realized < 0:
            lost += -realized
    return round(lost, 2)


def maybe_queue_loss_topoff_sata_sell(
    state: dict,
    sata_mark: float | None,
    events: list,
    now: str,
    *,
    fills: list | None = None,
) -> None:
    """If trades close at a loss, sell SATA to restore that original cost to cash.

    Example: $50k UXRP exits for $48k → sell $2k SATA so the $50k cost is back in cash.
    Does **not** run on wins/breakeven or while cash is merely deployed into open buys.
    """
    rules = state.get("standing_rules") or {}
    if rules.get("cash_floor_from_sata") is False:
        return
    loss_total = _trading_loss_total(fills or [])
    if loss_total < 1.0:
        return

    if sata_mark is None or sata_mark <= 0:
        events.append(f"{now} loss top-off: need ${loss_total:.2f} but no SATA mark")
        return
    pos = next((p for p in state["positions"] if p["symbol"] == "SATA"), None)
    qty = float(pos["qty"]) if pos else 0.0
    if qty <= 0:
        events.append(f"{now} loss top-off: need ${loss_total:.2f} but no SATA shares to sell")
        return
    max_proceeds = round(qty * float(sata_mark), 2)
    notional = min(loss_total, max_proceeds)
    if notional < 1.0:
        return
    params = (
        "Trade loss top-off: sell ${NOTIONAL} SATA at best to restore original cost to cash "
        "(Rodney override; skip profit→SATA)."
    )
    for o in state["orders"]:
        if (
            o.get("symbol") == "SATA"
            and o.get("type") == "SELL_BEST"
            and o.get("status") in {"OPEN", "WORKING"}
            and o.get("purpose") == "CASH_FLOOR"
        ):
            o["notional"] = notional
            o["allow_sata_sell"] = True
            o["rodney_override_sata_sell"] = True
            o["skip_profit_to_sata"] = True
            o["params_text"] = params.replace("${NOTIONAL}", f"${notional:.2f}")
            events.append(
                f"{now} loss top-off SATA sell notional → ${notional:.2f} (restore trade cost)"
            )
            return
    n = sum(1 for o in state["orders"] if str(o.get("id", "")).startswith("SB-SATA-")) + 1
    oid = f"SB-SATA-{n}"
    state["orders"].append(
        {
            "id": oid,
            "symbol": "SATA",
            "type": "SELL_BEST",
            "status": "OPEN",
            "notional": notional,
            "purpose": "CASH_FLOOR",
            "allow_sata_sell": True,
            "rodney_override_sata_sell": True,
            "skip_profit_to_sata": True,
            "source": "loss_topoff",
            "params_text": params.replace("${NOTIONAL}", f"${notional:.2f}"),
        }
    )
    note = (
        f"{now} queued {oid} SELL_BEST SATA ${notional:.2f} "
        f"(restore ${loss_total:.2f} trade cost after loss"
    )
    if notional + 1e-9 < loss_total:
        note += f"; short ${loss_total - notional:.2f} — insufficient SATA"
    note += ")"
    events.append(note)


def cancel_entry_group(
    state: dict, entry_group: str, events: list, now: str, *, except_ids: set[str] | None = None
) -> None:
    """Cancel open protective orders sharing an entry_group (hard stop / trail / scale-out)."""
    if not entry_group:
        return
    except_ids = except_ids or set()
    for o in state["orders"]:
        if o.get("id") in except_ids:
            continue
        if o.get("entry_group") != entry_group:
            continue
        if o.get("status") in {"FILLED", "CANCELLED"}:
            continue
        o["status"] = "CANCELLED"
        events.append(f"{now} cancelled {o['id']} (entry_group={entry_group})")


def cancel_symbol_exits(
    state: dict, symbol: str, events: list, now: str, *, except_ids: set[str] | None = None
) -> None:
    """Cancel open protective exits for a symbol (all entry groups). Used when position goes flat."""
    except_ids = except_ids or set()
    protective = {
        "TRAILING_STOP_LIMIT_SELL",
        "HARD_STOP_LIMIT_SELL",
    }
    for o in state["orders"]:
        if o.get("id") in except_ids:
            continue
        if o.get("symbol") != symbol:
            continue
        if o.get("status") in {"FILLED", "CANCELLED"}:
            continue
        otype = o.get("type")
        is_scale = o.get("purpose") == "SCALE_OUT"
        has_group = bool(o.get("entry_group"))
        if otype not in protective and not (otype == "LIMIT_SELL" and (is_scale or has_group)):
            continue
        o["status"] = "CANCELLED"
        o["params_text"] = (o.get("params_text") or "") + " | Cancelled — position flat"
        events.append(f"{now} cancelled {o['id']} (symbol flat {symbol})")


def apply_hard_stop_limit(order: dict, mark: float, position: dict) -> dict:
    """Fixed stop-limit sell (hard invalidation). Triggers when mark <= stop; LIMIT at stop."""
    if order.get("status") in {"FILLED", "CANCELLED"}:
        return {}
    stop = float(order["stop_price"])
    limit = float(order.get("limit_price") or stop)
    event = {"id": order["id"], "symbol": order["symbol"]}
    status = order.get("status", "OPEN")

    def _fill_hard_stop(fill_px: float) -> dict:
        qty = float(position["qty"])
        if qty <= 0:
            order["status"] = "CANCELLED"
            event["event"] = "CANCELLED_NO_QTY"
            return event
        proceeds = round(qty * fill_px, 2)
        order["status"] = "FILLED"
        order["fill_price"] = fill_px
        order["fill_qty"] = qty
        avg = float(position.get("avg_cost") or 0)
        position["qty"] = 0.0
        position["cost_basis"] = 0.0
        position["avg_cost"] = 0.0
        event.update(
            {
                "event": "FILLED_LIMIT",
                "side": "SELL",
                "limit": limit,
                "qty": qty,
                "price": fill_px,
                "proceeds": proceeds,
                "basis_released": round(avg * qty, 2),
            }
        )
        return event

    if status == "WORKING_LIMIT":
        limit = float(order["limit_price"])
        # Fill at limit if printable; if price gapped through the stop-limit, fill at mark.
        if mark + 1e-9 >= limit:
            return _fill_hard_stop(limit)
        if mark <= stop + 1e-9:
            return _fill_hard_stop(mark)
        event["event"] = "WORKING_LIMIT"
        event["limit"] = limit
        return event

    if mark <= stop + 1e-9:
        if mark + 1e-9 >= limit:
            return _fill_hard_stop(limit)
        # Gap through: do not leave a sell limit stranded above the market.
        return _fill_hard_stop(mark)

    event["event"] = "HARD_STOP_HOLD"
    event["stop"] = stop
    return event


# Per-symbol exit defaults (Rodney 2026-10-02 — UXRP noise-adjusted).
# Global default remains hard −2% / arm +1% / trail 0.5% market / ⅓@+2% + ⅓@+5%.
SYMBOL_EXIT_DEFAULTS: dict[str, dict] = {
    "UXRP": {
        "arm_pct": 0.02,
        "trail_pct": 0.005,
        "hard_stop_pct": 0.03,
        # Last ⅓ trail arms only after 2nd scale-out fills (Rodney 2026-10-02).
        "arm_after_scale_level": 2,
    },
    "GDXU": {
        "arm_pct": 0.03,
        "trail_pct": 0.005,
        "hard_stop_pct": 0.045,
        "arm_after_scale_level": 2,
        "scale_out_levels": [
            {"pct": 0.03, "fraction": 1.0 / 3.0},
            {"pct": 0.07, "fraction": 1.0 / 3.0},
        ],
    },
}


def _default_scale_out_levels(order: dict, rules: dict, sym_rules: dict | None = None) -> list[dict]:
    """Scale-out ladder: ⅓ at +2%, ⅓ at +5% (remainder on trail)."""
    sym_rules = sym_rules or {}
    levels = (
        order.get("scale_out_levels")
        or sym_rules.get("scale_out_levels")
        or rules.get("scale_out_levels")
    )
    if levels:
        return [
            {"pct": float(x["pct"]), "fraction": float(x["fraction"])}
            for x in levels
        ]
    # Legacy single-level override still supported.
    if any(k in order or k in sym_rules or k in rules for k in ("scale_out_pct",)):
        return [
            {
                "pct": float(
                    order.get(
                        "scale_out_pct",
                        sym_rules.get("scale_out_pct", rules.get("scale_out_pct", 0.02)),
                    )
                ),
                "fraction": float(
                    order.get(
                        "scale_out_fraction",
                        sym_rules.get(
                            "scale_out_fraction", rules.get("scale_out_fraction", 1.0 / 3.0)
                        ),
                    )
                ),
            }
        ]
    return [
        {"pct": 0.02, "fraction": 1.0 / 3.0},
        {"pct": 0.05, "fraction": 1.0 / 3.0},
    ]


def _exit_rule_for(state: dict, order: dict, sym: str) -> tuple[float, float, float, list[dict], int | None]:
    """Resolve arm/trail/hard/scale/arm_after for a symbol."""
    rules = state.get("standing_rules") or {}
    sym_rules = dict(SYMBOL_EXIT_DEFAULTS.get(sym) or {})
    standing_sym = (rules.get("symbol_exits") or {}).get(sym) or {}
    sym_rules.update(standing_sym)

    arm_pct = float(
        order.get("arm_pct", sym_rules.get("arm_pct", rules.get("arm_pct", 0.01)))
    )
    trail_pct = float(
        order.get(
            "trail_pct",
            sym_rules.get("trail_pct", rules.get("trail_pct_after_arm", 0.005)),
        )
    )
    hard_pct = float(
        order.get(
            "hard_stop_pct",
            sym_rules.get("hard_stop_pct", rules.get("hard_stop_pct", 0.02)),
        )
    )
    scale_levels = _default_scale_out_levels(order, rules, sym_rules)
    arm_after = order.get("arm_after_scale_level", sym_rules.get("arm_after_scale_level"))
    arm_after_i = int(arm_after) if arm_after is not None else None
    return arm_pct, trail_pct, hard_pct, scale_levels, arm_after_i


def attach_trading_exits(
    state: dict, order: dict, sym: str, fill_px: float, fill_qty: float, events: list, now: str
) -> None:
    """Attach hard stop, trail (market on reverse), and dual scale-outs. Not for SATA.

    Global default: hard −2%, arm +1%, trail 0.5% market, ⅓@+2% + ⅓@+5%.
    UXRP override: hard −3%, arm +2%, trail 0.5% market after 2nd scale-out (same scale-outs).
    GDXU override: hard −4.5%, arm +3%, trail 0.5% market after 2nd scale-out, ⅓@+3% + ⅓@+7%.
    """
    arm_pct, trail_pct, hard_pct, scale_levels, arm_after = _exit_rule_for(state, order, sym)
    entry_group = order["id"]

    arm = round(fill_px * (1 + arm_pct), 4)
    hard = round(fill_px * (1 - hard_pct), 4)

    n_ts = sum(1 for o in state["orders"] if o.get("symbol") == sym and o.get("type") == "TRAILING_STOP_LIMIT_SELL") + 1
    n_hs = sum(1 for o in state["orders"] if o.get("symbol") == sym and o.get("type") == "HARD_STOP_LIMIT_SELL") + 1
    n_so = sum(1 for o in state["orders"] if o.get("symbol") == sym and o.get("purpose") == "SCALE_OUT") + 1

    scale_blurb = "; ".join(
        f"⅓ at +{lvl['pct']*100:.1f}%".replace(".0%", "%")
        if abs(lvl["fraction"] - 1.0 / 3.0) < 1e-9
        else f"{lvl['fraction']*100:.0f}% at +{lvl['pct']*100:.1f}%"
        for lvl in scale_levels
    )
    # Prefer clean fractions in params text for the standard ladder.
    if len(scale_levels) == 2 and all(
        abs(lvl["fraction"] - 1.0 / 3.0) < 1e-9 for lvl in scale_levels
    ):
        scale_blurb = (
            f"⅓ at +{scale_levels[0]['pct']*100:.0f}%, "
            f"⅓ at +{scale_levels[1]['pct']*100:.0f}%"
        )

    trail_note = (
        f"Trail 0.5% market arms only after scale-out #{arm_after} fills."
        if arm_after
        else f"Arm +{arm_pct*100:.0f}% → ${arm}. Trail {trail_pct*100:.1f}% → market sell on reverse."
    )
    ts = {
        "id": f"TS-{sym}-{n_ts}",
        "symbol": sym,
        "type": "TRAILING_STOP_LIMIT_SELL",
        "status": "PENDING_ARM",
        "arm_price": arm,
        "trail_pct": trail_pct,
        "fill_at_market": True,
        "entry_group": entry_group,
        "entry_price": fill_px,
        "params_text": f"{trail_note} (group {entry_group})",
    }
    if arm_after is not None:
        ts["arm_after_scale_level"] = arm_after
        ts["status"] = "WAITING_SCALE"  # not armed until 2nd ⅓ sells
    hs = {
        "id": f"HS-{sym}-{n_hs}",
        "symbol": sym,
        "type": "HARD_STOP_LIMIT_SELL",
        "status": "OPEN",
        "stop_price": hard,
        "limit_price": hard,
        "entry_group": entry_group,
        "entry_price": fill_px,
        "cancel_when_trail_armed": True,
        "params_text": (
            f"Hard invalidation −{hard_pct*100:.0f}% → ${hard} LIMIT until trail arms. "
            f"(group {entry_group})"
        ),
    }
    attached = [ts, hs]
    events.append(
        f"{now} {sym} attached {ts['id']} "
        f"{'WAITING_SCALE#'+str(arm_after) if arm_after else 'PENDING_ARM arm='+str(arm)}"
    )
    events.append(f"{now} {sym} attached {hs['id']} HARD_STOP stop={hard}")

    for i, lvl in enumerate(scale_levels):
        scale_px = round(fill_px * (1 + float(lvl["pct"])), 4)
        scale_qty = fill_qty * float(lvl["fraction"])
        so = {
            "id": f"SO-{sym}-{n_so + i}",
            "symbol": sym,
            "type": "LIMIT_SELL",
            "status": "OPEN",
            "limit_price": scale_px,
            "qty": scale_qty,
            "purpose": "SCALE_OUT",
            "scale_level": i + 1,
            "entry_group": entry_group,
            "entry_price": fill_px,
            "params_text": (
                f"Scale-out {float(lvl['fraction'])*100:.0f}% at +{float(lvl['pct'])*100:.0f}% "
                f"→ ${scale_px} LIMIT. (group {entry_group}; {scale_blurb})"
            ),
        }
        attached.append(so)
        events.append(
            f"{now} {sym} attached {so['id']} SCALE_OUT qty={scale_qty:.4f} @ {scale_px}"
        )

    state["orders"].extend(attached)


def scale_out_filled(state: dict, entry_group: str, level: int) -> bool:
    """True if SCALE_OUT at the given level for this entry group is FILLED."""
    for o in state.get("orders") or []:
        if (
            o.get("entry_group") == entry_group
            and o.get("purpose") == "SCALE_OUT"
            and int(o.get("scale_level") or 0) == int(level)
            and o.get("status") == "FILLED"
        ):
            return True
    return False


def raise_hard_stop_after_scale(
    state: dict, entry_group: str, scale_level: int, events: list, now: str
) -> None:
    """After 1st scale-out fills, raise hard stop to entry (breakeven) on remaining size.

    Rodney 2026-10-02: don't give back the win after banking the first ⅓.
    """
    if int(scale_level) != 1:
        return
    entry_px = None
    for o in state.get("orders") or []:
        if o.get("entry_group") == entry_group and o.get("entry_price") is not None:
            entry_px = float(o["entry_price"])
            break
    if entry_px is None or entry_px <= 0:
        return
    for o in state.get("orders") or []:
        if (
            o.get("entry_group") == entry_group
            and o.get("type") == "HARD_STOP_LIMIT_SELL"
            and o.get("status") not in {"FILLED", "CANCELLED"}
        ):
            old = o.get("stop_price")
            # Only raise (never loosen) the stop.
            if old is not None and float(old) >= entry_px - 1e-9:
                continue
            o["stop_price"] = round(entry_px, 4)
            o["limit_price"] = round(entry_px, 4)
            o["breakeven_after_scale1"] = True
            o["params_text"] = (
                f"Hard stop raised to breakeven ${entry_px:.4f} after 1st scale-out. "
                f"(was {old}; group {entry_group})"
            )
            events.append(
                f"{now} {o.get('symbol')} {o['id']} hard stop → breakeven ${entry_px:.4f} "
                f"(after scale #1; was {old})"
            )


def arm_trail_after_scale(
    state: dict, entry_group: str, mark: float, events: list, now: str
) -> None:
    """Arm waiting trails once required scale-out has filled; cancel hard stops."""
    for order in state.get("orders") or []:
        if order.get("entry_group") != entry_group:
            continue
        if order.get("type") != "TRAILING_STOP_LIMIT_SELL":
            continue
        if order.get("status") not in {"WAITING_SCALE", "PENDING_ARM"}:
            continue
        need = order.get("arm_after_scale_level")
        if need is not None and not scale_out_filled(state, entry_group, int(need)):
            continue
        trail = float(order.get("trail_pct", 0.005))
        order["status"] = "ARMED"
        order["high_water"] = mark
        order["stop"] = round(mark * (1 - trail), 4)
        order["armed_at_mark"] = mark
        events.append(
            f"{now} {order['symbol']} {order['id']} ARMED after scale-out "
            f"hw={mark:.4f} stop={order['stop']:.4f}"
        )
        for o in state["orders"]:
            if (
                o.get("entry_group") == entry_group
                and o.get("type") == "HARD_STOP_LIMIT_SELL"
                and o.get("cancel_when_trail_armed")
                and o.get("status") not in {"FILLED", "CANCELLED"}
            ):
                o["status"] = "CANCELLED"
                events.append(f"{now} cancelled {o['id']} — trail {order['id']} ARMED")


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
    # Explicit Rodney override (e.g. exit overnight SATA redeploy).
    if order.get("allow_sata_sell") or order.get("rodney_override_sata_sell"):
        return False
    if pos.get("no_sell") or pos.get("hold_for_dividends"):
        return True
    return True  # default: never sell SATA under standing policy


def apply_trailing_stop(order: dict, mark: float, position: dict) -> dict:
    """Mutate order/position; return event dict or empty.

    Default fill_at_market=True: when price reverses through the trail stop, sell
    remaining qty at the current mark (Rodney: market on >0.5% reverse).
    """
    if order.get("status") in {"FILLED", "CANCELLED"}:
        return {}
    if order.get("status") == "WAITING_SCALE":
        return {
            "id": order["id"],
            "symbol": order["symbol"],
            "event": "WAITING_SCALE",
            "need_scale_level": order.get("arm_after_scale_level"),
        }
    arm = float(order["arm_price"])
    trail = float(order.get("trail_pct", 0.005))
    fill_at_market = bool(order.get("fill_at_market", True))
    event = {"id": order["id"], "symbol": order["symbol"]}

    def _fill_trail(fill_px: float, *, limit: float | None = None) -> dict:
        qty = float(position["qty"])
        if qty <= 0:
            order["status"] = "CANCELLED"
            event["event"] = "CANCELLED_NO_QTY"
            return event
        proceeds = round(qty * fill_px, 2)
        order["status"] = "FILLED"
        order["fill_price"] = fill_px
        order["fill_qty"] = qty
        event.update(
            {
                "event": "FILLED_LIMIT" if not fill_at_market else "FILLED_MARKET",
                "side": "SELL",
                "limit": limit if limit is not None else fill_px,
                "price": fill_px,
                "qty": qty,
                "proceeds": proceeds,
            }
        )
        position["qty"] = 0.0
        position["cost_basis"] = 0.0
        return event

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
            if fill_at_market:
                return _fill_trail(mark, limit=stop)
            # Legacy limit-at-stop path.
            if mark + 1e-9 >= stop:
                return _fill_trail(stop, limit=stop)
            order["status"] = "WORKING_LIMIT"
            order["limit_price"] = stop
            event["event"] = "WORKING_LIMIT"
            event["limit"] = stop
            event["mark"] = mark
            return event
        event["event"] = "ARMED_HOLD"
        event["stop"] = stop
        return event

    if order["status"] == "WORKING_LIMIT":
        limit = float(order["limit_price"])
        if fill_at_market and mark <= float(order.get("stop") or limit) + 1e-9:
            return _fill_trail(mark, limit=limit)
        if mark + 1e-9 >= limit:
            return _fill_trail(limit, limit=limit)
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
        avail = float(position["qty"])
        if order.get("notional") is not None and order.get("qty") is None:
            qty = float(order["notional"]) / mark
        else:
            qty = float(order.get("qty") or avail)
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


def format_fill_email(state: dict, marks: dict, fills: list, now: str) -> str:
    """Plain-text Gmail body: each fill + book balances after. Only call when fills non-empty."""
    lines = [f"John Cloud — PAPER fill(s) {now}", ""]
    for ev in fills:
        side = ev.get("side") or ("BUY" if ev.get("event") == "FILLED_BUY" else "SELL")
        sym = ev.get("symbol", "?")
        qty = float(ev.get("qty") or 0)
        px = float(ev.get("price") or ev.get("limit") or 0)
        oid = ev.get("id", "")
        lines.append(f"{side} {sym} ({oid})")
        lines.append(f"  qty {qty:.4f} @ ${px:.4f}")
        if ev.get("cost") is not None:
            lines.append(f"  cost ${float(ev['cost']):,.2f}")
        if ev.get("proceeds") is not None:
            lines.append(f"  proceeds ${float(ev['proceeds']):,.2f}")
        if ev.get("realized") is not None:
            lines.append(f"  realized ${float(ev['realized']):,.2f}")
        lines.append("")
    cash = float(state.get("cash") or 0)
    div = float(state.get("dividend_cash") or 0)
    lines.append("Balances after:")
    lines.append(f"  Cash ${cash:,.2f}")
    lines.append(f"  Dividend cash ${div:,.4f}")
    equity = cash + div
    for p in state.get("positions") or []:
        qty = float(p.get("qty") or 0)
        if qty <= 0:
            continue
        sym = p["symbol"]
        avg = float(p.get("avg_cost") or 0)
        basis = float(p.get("cost_basis") or 0)
        mk = marks.get(sym, {}).get("mark")
        if mk is not None:
            mv = qty * float(mk)
            equity += mv
            lines.append(
                f"  {sym}: {qty:.4f} sh @ avg ${avg:.4f} | mkt ${mv:,.2f} (mark ${float(mk):.4f})"
            )
        else:
            lines.append(f"  {sym}: {qty:.4f} sh @ avg ${avg:.4f} | basis ${basis:,.2f}")
    lines.append(f"  Approx equity ${equity:,.2f}")
    return "\n".join(lines)


def notify_telegram_fill(body: str) -> dict:
    """Send fill + balances to Rodney on Telegram (in addition to Gmail). Never raises."""
    if not (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip():
        return {"ok": False, "skipped": "no TELEGRAM_BOT_TOKEN"}
    bridge = ROOT / "telegram_bridge.py"
    if not bridge.exists():
        return {"ok": False, "skipped": "no telegram_bridge.py"}
    text = "John Cloud PAPER fill\n\n" + body
    try:
        proc = subprocess.run(
            [sys.executable, str(bridge), "send", text[:3900]],
            cwd=str(ROOT.parent.parent),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": (proc.stdout or "")[:500],
            "stderr": (proc.stderr or "")[:300],
        }
    except Exception as exc:  # noqa: BLE001 — fill path must not abort marks
        return {"ok": False, "error": str(exc)}


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
        "**Notify:** Gmail + Telegram on buy/sell fills (with balances) — never on mark/price updates  ",
        "",
        "### Standing fill rule (Rodney)",
        "",
        "- **Buys:** best (lowest) available valid quote.",
        "- **Sells:** best (highest) available valid quote.",
        "- **Trading exits:** default hard **−2%** / arm **+1%** / trail **0.5%** market / scale **⅓@+2%** + **⅓@+5%**. **UXRP:** hard **−3%** / arm **+2%** / trail **0.5%**. **GDXU:** hard **−4.5%** / arm **+3%** / trail **0.5%** / scale **⅓@+3%** + **⅓@+7%**.",
        "- **Income SATA (~dividends sleeve):** no stops / no scale-outs / no sells unless Rodney overrides.",
        "- Open paper orders auto-fill when conditions hit (no manual confirm).",
        "- **Profits → SATA:** realized **trading** profit buys **SATA** at best; **dividend_cash** reinvests when ≥1 share, else merges into the next profit→SATA buy.",
        "- **Hold for daily dividends — do not sell** income SATA unless Rodney overrides.",
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
        "- Poll ≈ every **5 minutes** during **NYSE extended hours only** (Mon–Fri 4:00 AM–8:00 PM ET).",
        "- **Do not email** on price/mark updates — email only when a buy or sell fills.",
        "",
    ]
    return "\n".join(lines)


def in_nyse_extended_hours(now_et: datetime | None = None) -> bool:
    """True Mon–Fri from 4:00 AM through 8:00 PM America/New_York."""
    now_et = now_et or datetime.now(NY_TZ)
    if now_et.weekday() >= 5:  # Sat/Sun
        return False
    t = now_et.time()
    return SESSION_OPEN <= t <= SESSION_CLOSE


def main() -> None:
    force = "--force" in sys.argv
    now_et = datetime.now(NY_TZ)

    # iMessage text-orders: pull pending from git and apply into local paper-state even off-hours.
    from apply_text_orders import process_pending  # local module beside this file

    text_summary = process_pending()

    if not force and not in_nyse_extended_hours(now_et):
        summary = {
            "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "skipped": True,
            "reason": "outside_nyse_extended_hours",
            "local_et": now_et.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "window": "Mon–Fri 04:00–20:00 America/New_York (premarket through after-hours)",
            "big_items": [],
            "text_orders": text_summary,
            "note": "No Yahoo poll outside NYSE extended hours; use --force to override",
        }
        print(json.dumps(summary, indent=2))
        return

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    marks = {s: fetch_yahoo(s) for s in SYMBOLS}
    MARKS_PATH.write_text(json.dumps({"updated": now, "marks": marks}, indent=2) + "\n")

    # Re-load after text apply so newly queued OPEN orders are visible this poll.
    state = load_state()
    state["updated"] = now
    state["auto_execute"] = True
    events = []
    fills = []  # only buy/sell fills — email-worthy

    pos_by_sym = {p["symbol"]: p for p in state["positions"]}
    cash = float(state["cash"])

    credit_sata_dividends(state, now, events)
    sata_mark_early = marks.get("SATA", {}).get("mark")
    rules_early = state.get("standing_rules") or {}
    floor_early = float(rules_early.get("cash_floor_usd", CASH_FLOOR_USD))
    # Prefer cash floor over dividend→SATA reinvest when cash is already short.
    if cash + 1e-9 >= floor_early or rules_early.get("cash_floor_from_sata") is False:
        cash = round(cash + try_reinvest_dividend_cash(state, sata_mark_early, events, now), 2)

    for order in state["orders"]:
        if order.get("status") in {"FILLED", "CANCELLED"}:
            continue
        sym = order["symbol"]
        quote = marks.get(sym, {})
        mark = quote.get("mark")
        if mark is None:
            continue

        otype = order.get("type", "")

        # Stops stay blocked on stale quotes. Directed best-price buys/sells may use latest mark.
        allow_on_stale = {"BUY_BEST", "MARKET_BUY", "LIMIT_BUY", "SELL_BEST", "MARKET_SELL", "LIMIT_SELL"}
        if not quote.get("fresh", True) and otype not in allow_on_stale:
            events.append(
                f"{now} {sym} STALE_QUOTE age={quote.get('quote_age_sec')}s mark={mark} — order logic skipped"
            )
            continue

        if otype == "HARD_STOP_LIMIT_SELL":
            pos = ensure_position(pos_by_sym, state, sym)
            if float(pos["qty"]) <= 0:
                order["status"] = "CANCELLED"
                continue
            if block_sata_sells(order, pos):
                events.append(f"{now} {sym} SELL blocked — hold for dividends")
                order["status"] = "CANCELLED"
                continue
            qty_before = float(pos.get("qty") or 0)
            basis_before = float(pos.get("cost_basis") or 0)
            ev = apply_hard_stop_limit(order, float(mark), pos)
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
                        "rationale": f"Hard stop-limit {order['id']} auto-filled",
                    }
                )
                avg_before = basis_before / qty_before if qty_before else 0
                realized = round(float(ev["proceeds"]) - avg_before * float(ev["qty"]), 2)
                ev["realized"] = realized
                if realized > 0:
                    cash = round(cash + queue_sata_profit_buy(state, realized, events, now), 2)
                cancel_entry_group(
                    state, order.get("entry_group", ""), events, now, except_ids={order["id"]}
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
            # UXRP/GDXU: trail waits until 2nd scale-out fills, then arms at mark.
            if order.get("status") == "WAITING_SCALE":
                need = order.get("arm_after_scale_level")
                if need is not None and scale_out_filled(
                    state, order.get("entry_group", ""), int(need)
                ):
                    arm_trail_after_scale(
                        state, order.get("entry_group", ""), float(mark), events, now
                    )
                else:
                    continue
            qty_before = float(pos.get("qty") or 0)
            basis_before = float(pos.get("cost_basis") or 0)
            ev = apply_trailing_stop(order, float(mark), pos)
            if not ev:
                continue
            if ev.get("event") == "WAITING_SCALE":
                continue
            msg = f"{now} {sym} mark={mark:.4f} {ev}"
            events.append(msg)
            if ev.get("event") == "ARMED":
                # Drop hard invalidation once trail is live.
                for o in state["orders"]:
                    if (
                        o.get("entry_group") == order.get("entry_group")
                        and o.get("type") == "HARD_STOP_LIMIT_SELL"
                        and o.get("cancel_when_trail_armed")
                        and o.get("status") not in {"FILLED", "CANCELLED"}
                    ):
                        o["status"] = "CANCELLED"
                        events.append(
                            f"{now} cancelled {o['id']} — trail {order['id']} ARMED"
                        )
            if ev.get("event") in FILL_EVENTS:
                fills.append(ev)
                cash = round(cash + float(ev["proceeds"]), 2)
                state.setdefault("trade_log", []).append(
                    {
                        "time": now,
                        "side": "SELL_LIMIT" if ev.get("event") == "FILLED_LIMIT" else "SELL_MARKET",
                        "symbol": sym,
                        "qty": ev["qty"],
                        "price": float(ev.get("price") or ev.get("limit")),
                        "cash_after": cash,
                        "rationale": f"Trailing stop {order['id']} auto-filled",
                    }
                )
                avg_before = basis_before / qty_before if qty_before else 0
                realized = round(float(ev["proceeds"]) - avg_before * float(ev["qty"]), 2)
                ev["realized"] = realized
                if realized > 0:
                    cash = round(cash + queue_sata_profit_buy(state, realized, events, now), 2)
                cancel_entry_group(
                    state, order.get("entry_group", ""), events, now, except_ids={order["id"]}
                )
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
                    purpose = order.get("purpose", "")
                    if purpose == "DIVIDEND_REINVEST":
                        rationale = f"Dividend reinvest→SATA {order['id']} auto-filled; hold for dividends"
                    elif purpose == "PROFIT_TO_SATA":
                        rationale = f"Profit→SATA {order['id']} auto-filled; hold for dividends"
                    else:
                        rationale = f"{otype} {order['id']} auto-filled at best available; hold for dividends"
                    state["trade_log"][-1]["rationale"] = rationale
                if ev.get("event") == "FILLED_SELL":
                    # Approx realized on partial/full: use avg cost × qty sold
                    avg_before = basis_before / qty_before if qty_before else 0
                    realized = round(float(ev["proceeds"]) - avg_before * float(ev["qty"]), 2)
                    ev["realized"] = realized
                    # Skip profit→SATA on explicit redeploy exits (cash needed for other buys).
                    if (
                        realized > 0
                        and not order.get("skip_profit_to_sata")
                        and order.get("purpose") != "OVERNIGHT_REDEPLOY"
                    ):
                        cash = round(cash + queue_sata_profit_buy(state, realized, events, now), 2)
                # Trading exits: hard −2% until arm; +1% arm / 0.5% trail market; ⅓@+2% + ⅓@+5%.
                if (
                    ev.get("event") == "FILLED_BUY"
                    and order.get("attach_trailing_stop", False)
                    and sym != "SATA"
                ):
                    attach_trading_exits(
                        state, order, sym, fill_px, float(ev["qty"]), events, now
                    )
                # Scale-out partial: leave trail/hard on remaining qty (hard cancels when trail arms).
                if ev.get("event") == "FILLED_SELL" and order.get("purpose") == "SCALE_OUT":
                    lvl = int(order.get("scale_level") or 0)
                    # After 1st scale: raise hard stop to entry (breakeven).
                    raise_hard_stop_after_scale(
                        state, order.get("entry_group", ""), lvl, events, now
                    )
                    # After 2nd scale-out, arm remainder trail at current mark (0.5% HWM).
                    arm_trail_after_scale(
                        state, order.get("entry_group", ""), float(mark), events, now
                    )
                    if float(pos.get("qty") or 0) <= 0:
                        cancel_entry_group(
                            state,
                            order.get("entry_group", ""),
                            events,
                            now,
                            except_ids={order["id"]},
                        )
                # Discretionary full/partial sell that flats the symbol: drop orphan exits.
                elif ev.get("event") == "FILLED_SELL" and float(pos.get("qty") or 0) <= 0:
                    cancel_symbol_exits(
                        state, sym, events, now, except_ids={order["id"]}
                    )

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
            purpose = order.get("purpose", "")
            if purpose == "DIVIDEND_REINVEST":
                rationale = f"Dividend reinvest→SATA {order['id']} auto-filled; hold for dividends"
            elif purpose == "PROFIT_TO_SATA":
                rationale = f"Profit→SATA {order['id']} auto-filled; hold for dividends"
            else:
                rationale = f"SATA {order['id']} auto-filled at best available; hold for dividends"
            state.setdefault("trade_log", []).append(
                {
                    "time": now,
                    "side": "BUY",
                    "symbol": "SATA",
                    "qty": ev["qty"],
                    "price": fill_px,
                    "cash_after": cash,
                    "rationale": rationale,
                }
            )

    # After a trading loss, sell SATA so the original trade cost returns to cash.
    sata_mark_floor = marks.get("SATA", {}).get("mark")
    maybe_queue_loss_topoff_sata_sell(state, sata_mark_floor, events, now, fills=fills)
    for order in state["orders"]:
        if order.get("status") in {"FILLED", "CANCELLED"}:
            continue
        if not (
            order.get("symbol") == "SATA"
            and order.get("type") == "SELL_BEST"
            and order.get("purpose") == "CASH_FLOOR"
        ):
            continue
        quote = marks.get("SATA", {})
        mark = quote.get("mark")
        if mark is None:
            continue
        pos = ensure_position(pos_by_sym, state, "SATA")
        if block_sata_sells(order, pos):
            events.append(f"{now} SATA cash-floor SELL blocked — hold for dividends")
            order["status"] = "CANCELLED"
            continue
        basis_before = float(pos.get("cost_basis") or 0)
        qty_before = float(pos.get("qty") or 0)
        ev, cash = apply_buy_sell_order(order, float(mark), pos, cash)
        if not ev:
            continue
        events.append(f"{now} SATA mark={mark:.4f} {ev}")
        if ev.get("event") in FILL_EVENTS:
            fills.append(ev)
            fill_px = float(ev.get("price") or mark)
            state.setdefault("trade_log", []).append(
                {
                    "time": now,
                    "side": "SELL",
                    "symbol": "SATA",
                    "qty": ev["qty"],
                    "price": fill_px,
                    "cash_after": cash,
                    "rationale": f"Cash floor→SATA sell {order['id']} auto-filled",
                }
            )
            # skip_profit_to_sata is set on CASH_FLOOR orders; keep explicit.
            _ = basis_before, qty_before

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
        "dividend_cash": state.get("dividend_cash", 0),
        "big_items": fills,  # buy/sell fills only; empty ⇒ no email
        "text_orders": text_summary,
        "events_tail": events[-5:],
        "note": "Never email on mark updates; email only if big_items non-empty",
    }
    if fills:
        summary["fill_email_to"] = "regiaemanagementllc@gmail.com"
        summary["fill_email_subject"] = "PAPER fill — balances after trade"
        body = format_fill_email(state, marks, fills, now)
        summary["fill_email_body"] = body
        # Rodney 2026-10-02: also Telegram on fills (keep Gmail).
        summary["telegram_fill"] = notify_telegram_fill(body)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
