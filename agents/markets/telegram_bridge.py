#!/usr/bin/env python3
"""Telegram ↔ John Cloud bridge (Bot API poll + send).

Secrets (env, never commit):
  TELEGRAM_BOT_TOKEN   — from @BotFather
  TELEGRAM_CHAT_ID     — Rodney's numeric chat id (optional until first message;
                         first inbound from any chat is locked if unset)

Usage:
  python3 telegram_bridge.py poll          # fetch new msgs; queue trades; print inbox
  python3 telegram_bridge.py send "text"   # reply to allowed chat
  python3 telegram_bridge.py whoami        # bot identity + pending updates peek
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
TG_DIR = ROOT / "telegram"
STATE_PATH = TG_DIR / "state.json"
INBOX_PATH = TG_DIR / "inbox.jsonl"
API = "https://api.telegram.org"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def token() -> str:
    t = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    if not t:
        raise SystemExit(
            "Missing TELEGRAM_BOT_TOKEN. Add it as a Cloud Agent secret, then restart."
        )
    return t


def load_state() -> dict:
    TG_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"offset": 0, "allowed_chat_id": None}


def save_state(state: dict) -> None:
    TG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def api_call(method: str, payload: dict | None = None) -> dict:
    url = f"{API}/bot{token()}/{method}"
    data = None
    headers = {"User-Agent": "JohnCloudTelegram/1.0"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Telegram API HTTP {exc.code}: {err}") from exc
    if not body.get("ok"):
        raise SystemExit(f"Telegram API error: {body}")
    return body["result"]


def allowed_chat_id(state: dict) -> int | None:
    env = (os.environ.get("TELEGRAM_CHAT_ID") or "").strip()
    if env:
        return int(env)
    cid = state.get("allowed_chat_id")
    return int(cid) if cid is not None else None


def append_inbox(item: dict) -> None:
    TG_DIR.mkdir(parents=True, exist_ok=True)
    with INBOX_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(item) + "\n")


def looks_like_trade(text: str) -> bool:
    u = text.strip().upper()
    return u.startswith(("BUY ", "SELL ", "CANCEL ", "STATUS")) or u in {
        "STATUS",
        "PORTFOLIO",
        "BALANCES",
        "BALANCE",
    }


def queue_trade(text: str) -> dict:
    """Queue on Cloud disk (no git — avoids GitHub email spam)."""
    cmd = [
        sys.executable,
        str(ROOT / "queue_text_order.py"),
        "--json-out",
        "--no-git",
        "--from-e164",
        "telegram",
        "--text",
        text,
    ]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    try:
        out = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        out = {"ok": False, "error": proc.stdout or proc.stderr or "queue failed"}
    out["exit_code"] = proc.returncode
    return out


def send_message(chat_id: int, text: str) -> dict:
    # Telegram limit ~4096 chars
    text = text[:4000]
    return api_call("sendMessage", {"chat_id": chat_id, "text": text})


def cmd_whoami() -> int:
    me = api_call("getMe")
    state = load_state()
    print(
        json.dumps(
            {
                "bot": me,
                "allowed_chat_id": allowed_chat_id(state),
                "offset": state.get("offset", 0),
                "inbox": str(INBOX_PATH),
            },
            indent=2,
        )
    )
    return 0


def cmd_send(text: str) -> int:
    state = load_state()
    chat_id = allowed_chat_id(state)
    if chat_id is None:
        raise SystemExit("No TELEGRAM_CHAT_ID / locked chat yet — message the bot once first.")
    result = send_message(chat_id, text)
    print(json.dumps({"ok": True, "message_id": result.get("message_id")}, indent=2))
    return 0


def cmd_poll(*, auto_reply_trades: bool = True) -> int:
    state = load_state()
    offset = int(state.get("offset") or 0)
    updates = api_call(
        "getUpdates",
        {"offset": offset, "timeout": 0, "allowed_updates": ["message"]},
    )
    allowed = allowed_chat_id(state)
    trade_events = []
    chat_events = []

    for upd in updates:
        upd_id = int(upd["update_id"])
        state["offset"] = max(int(state.get("offset") or 0), upd_id + 1)
        msg = upd.get("message") or {}
        chat = msg.get("chat") or {}
        chat_id = chat.get("id")
        text = (msg.get("text") or "").strip()
        if chat_id is None or not text:
            continue

        # Lock to first chat if none configured.
        if allowed is None:
            state["allowed_chat_id"] = int(chat_id)
            allowed = int(chat_id)
            save_state(state)

        if int(chat_id) != int(allowed):
            # Ignore other users silently.
            continue

        from_user = msg.get("from") or {}
        item = {
            "time": utc_now(),
            "update_id": upd_id,
            "chat_id": int(chat_id),
            "from": from_user.get("username") or from_user.get("id"),
            "text": text,
        }

        if looks_like_trade(text):
            queued = queue_trade(text)
            item["kind"] = "trade"
            item["queue"] = queued
            trade_events.append(item)
            append_inbox(item)
            if auto_reply_trades:
                reply = queued.get("reply") or queued.get("error") or json.dumps(queued)
                if queued.get("ok"):
                    send_message(int(chat_id), f"John Cloud: {reply}")
                else:
                    send_message(int(chat_id), f"John Cloud: could not queue — {reply}")
        else:
            item["kind"] = "chat"
            chat_events.append(item)
            append_inbox(item)

    save_state(state)
    print(
        json.dumps(
            {
                "ok": True,
                "polled": len(updates),
                "allowed_chat_id": allowed,
                "trades": trade_events,
                "chats": chat_events,
                "chat_count": len(chat_events),
                "trade_count": len(trade_events),
                "note": "Freeform chats need agent reply via: telegram_bridge.py send ...",
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Telegram bridge for John Cloud")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami")
    p_poll = sub.add_parser("poll")
    p_poll.add_argument("--no-auto-reply", action="store_true")
    p_send = sub.add_parser("send")
    p_send.add_argument("text")

    args = ap.parse_args()
    if args.cmd == "whoami":
        return cmd_whoami()
    if args.cmd == "poll":
        return cmd_poll(auto_reply_trades=not args.no_auto_reply)
    if args.cmd == "send":
        return cmd_send(args.text)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
