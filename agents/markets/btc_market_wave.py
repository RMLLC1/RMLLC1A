#!/usr/bin/env python3
"""Paper BTC Market Wave–style sleeve for Rodney (side-by-side with GDXU short).

Rules (proxy of Arch Public Market Wave):
- 20-day SMA band ±4%
- BUY clip when daily mark closes below lower band
- SELL clip when daily mark closes above upper band
- Mid-band = no action (chop ignored)
- Clip size $500; sell only above cost basis when sell_above_cost_basis=True
- Sleeve capital earmarked from trading cash; does not touch SATA
"""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "paper-state.json"
SLEEVE_PATH = ROOT / "btc-market-wave.json"

ALLOCATION = 10_000.0
CLIP = 500.0
SMA_DAYS = 20
BAND_PCT = 0.04
SYMBOL = "BTC-USD"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_daily_closes(symbol: str = SYMBOL, range_: str = "3mo") -> list[float]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_}&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    quote = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return [float(c) for c in quote if c is not None]


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2) + "\n")


def ensure_sleeve(paper: dict) -> dict:
    sleeve = load_json(SLEEVE_PATH, None)
    if sleeve and sleeve.get("status") == "ACTIVE":
        return sleeve

    cash = float(paper.get("cash") or 0)
    if cash < ALLOCATION:
        raise SystemExit(json.dumps({"ok": False, "error": "insufficient_cash", "cash": cash}))

    paper["cash"] = round(cash - ALLOCATION, 2)
    sleeve = {
        "status": "ACTIVE",
        "name": "BTC Market Wave paper sleeve",
        "created": utc_now(),
        "symbol": SYMBOL,
        "allocation": ALLOCATION,
        "cash": ALLOCATION,
        "qty": 0.0,
        "avg_cost": 0.0,
        "cost_basis": 0.0,
        "clip": CLIP,
        "sma_days": SMA_DAYS,
        "band_pct": BAND_PCT,
        "sell_above_cost_basis": True,
        "last_action_day": None,
        "trades": [],
        "events": [],
        "note": (
            "Arch Public Market Wave proxy: buy below 20d SMA−4%, sell above 20d SMA+4%, "
            "ignore mid-band. $500 clips. Sell only above avg cost."
        ),
    }
    paper.setdefault("events", []).append(
        {
            "time": utc_now(),
            "kind": "BTC_MARKET_WAVE_FUNDED",
            "amount": ALLOCATION,
            "detail": "Earmarked $10,000 trading cash into BTC Market Wave paper sleeve",
        }
    )
    save_json(STATE_PATH, paper)
    save_json(SLEEVE_PATH, sleeve)
    return sleeve


def bands(closes: list[float]) -> tuple[float, float, float, float]:
    mark = closes[-1]
    window = closes[-SMA_DAYS:]
    sma = sum(window) / len(window)
    lower = sma * (1 - BAND_PCT)
    upper = sma * (1 + BAND_PCT)
    return mark, sma, lower, upper


def avg_cost(sleeve: dict) -> float:
    qty = float(sleeve.get("qty") or 0)
    if qty <= 0:
        return 0.0
    return float(sleeve.get("cost_basis") or 0) / qty


def evaluate(sleeve: dict, closes: list[float]) -> dict:
    mark, sma, lower, upper = bands(closes)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    action = "HOLD"
    fill = None
    zone = "BELOW" if mark < lower else ("ABOVE" if mark > upper else "MID")

    # One action per UTC day max (daily close proxy).
    if sleeve.get("last_action_day") != day:
        cash = float(sleeve.get("cash") or 0)
        qty = float(sleeve.get("qty") or 0)
        if zone == "BELOW" and cash >= CLIP:
            buy_qty = CLIP / mark
            sleeve["cash"] = round(cash - CLIP, 4)
            sleeve["qty"] = qty + buy_qty
            sleeve["cost_basis"] = round(float(sleeve.get("cost_basis") or 0) + CLIP, 4)
            sleeve["avg_cost"] = round(avg_cost(sleeve), 4)
            sleeve["last_action_day"] = day
            action = "BUY"
            fill = {"side": "BUY", "qty": buy_qty, "price": mark, "notional": CLIP}
        elif zone == "ABOVE" and qty > 0:
            ac = avg_cost(sleeve)
            if (not sleeve.get("sell_above_cost_basis")) or mark > ac:
                sell_notional = min(CLIP, qty * mark)
                sell_qty = sell_notional / mark
                proceeds = sell_notional
                # Reduce cost basis proportionally
                cb = float(sleeve.get("cost_basis") or 0)
                cb_reduce = cb * (sell_qty / qty) if qty else 0
                sleeve["qty"] = qty - sell_qty
                sleeve["cash"] = round(cash + proceeds, 4)
                sleeve["cost_basis"] = round(max(0.0, cb - cb_reduce), 4)
                sleeve["avg_cost"] = round(avg_cost(sleeve), 4) if sleeve["qty"] > 1e-12 else 0.0
                if sleeve["qty"] < 1e-12:
                    sleeve["qty"] = 0.0
                    sleeve["cost_basis"] = 0.0
                    sleeve["avg_cost"] = 0.0
                sleeve["last_action_day"] = day
                action = "SELL"
                fill = {"side": "SELL", "qty": sell_qty, "price": mark, "notional": proceeds}

    if fill:
        trade = {
            "time": utc_now(),
            "day": day,
            "action": action,
            **fill,
            "zone": zone,
            "sma": round(sma, 2),
            "lower": round(lower, 2),
            "upper": round(upper, 2),
        }
        sleeve.setdefault("trades", []).append(trade)
        sleeve["trades"] = sleeve["trades"][-200:]
        sleeve.setdefault("events", []).append(f"{utc_now()} {action} {fill}")
        sleeve["events"] = sleeve["events"][-100:]

    equity = round(float(sleeve["cash"]) + float(sleeve["qty"]) * mark, 2)
    out = {
        "ok": True,
        "action": action,
        "zone": zone,
        "mark": round(mark, 2),
        "sma20": round(sma, 2),
        "lower": round(lower, 2),
        "upper": round(upper, 2),
        "cash": round(float(sleeve["cash"]), 2),
        "qty": float(sleeve["qty"]),
        "avg_cost": float(sleeve.get("avg_cost") or 0),
        "equity": equity,
        "pnl": round(equity - ALLOCATION, 2),
        "fill": fill,
        "updated": utc_now(),
    }
    sleeve["last_mark"] = out
    save_json(SLEEVE_PATH, sleeve)
    return out


def main() -> None:
    paper = load_json(STATE_PATH, {})
    sleeve = ensure_sleeve(paper)
    closes = fetch_daily_closes()
    if len(closes) < SMA_DAYS:
        raise SystemExit(json.dumps({"ok": False, "error": "insufficient_history"}))
    result = evaluate(sleeve, closes)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
