# Paper trading rules (Rodney / John Cloud / John Mac)

**Updated:** 2026-10-02  
**Mode:** PAPER only (simulated). Not live brokerage.

John Mac: read this before handling any trade text. John Cloud owns the paper book on the cloud disk; Mac **queues** text orders only.

---

## Who does what

| Desk | Role |
| --- | --- |
| **John Cloud** | Yahoo marks every ~5m (NYSE extended hours); applies text-orders; auto-executes fills; Gmail on fills only |
| **John Mac** | iMessage with Rodney; parse BUY/SELL/CANCEL → `queue_text_order.py` → git push `text-orders/pending/` only |
| **Telegram** | Optional: message John Cloud bot directly (`agents/markets/telegram/README.md`); queues on Cloud disk (`--no-git`) |
| **Rodney** | Approves strategy by text/Cursor; only his number `…8173715555` may text-trade |

---

## Session / marks

- Poll **Mon–Fri 4:00 AM–8:00 PM America/New_York** only (premarket through after-hours).
- Outside window: no Yahoo poll (text **queues** still apply anytime Cloud runs the apply step).
- **No git** for `paper-state.json`, `last_marks.json`, `paper-portfolio.md`, or fills (gitignored; avoids bot email spam).
- **Gmail** to `regiaemanagementllc@gmail.com` **only** on buy/sell fills — body must include **balances after** (cash, positions, approx equity). Never email marks, ARMED, WORKING, stale, UPL, status, or git activity.

---

## Entry fills

- **Buys:** best (lowest) valid quote at or better than limit (limit buys fill when mark ≤ limit).
- **Sells:** best (highest) valid quote at or better than limit (limit sells when mark ≥ limit).
- **BUY BEST / SELL BEST:** fill at current mark on a poll (best-available proxy).
- Open paper orders **auto-execute** when conditions hit (no second confirm).

---

## Default exits (new non-SATA buys)

Unless Rodney says otherwise on that order:

1. **Hard invalidation −2%** from fill → LIMIT sell at stop (if price **gaps through**, fill at **mark**, not hang above market).
2. **Arm +1%** from fill → then **trail 0.5%** below high water → **market sell** remainder when reverse >0.5%.
3. **Scale-out ⅓ at +2%** LIMIT, then **⅓ at +5%** LIMIT; remainder stays on trail/hard until done.
4. When trail **arms**, hard stop for that entry group is cancelled.

### UXRP override (noise-adjusted, 2026-10-02)

UXRP (2× daily) uses wider stops to avoid session chop:

1. **Hard −3%** until trail arms.
2. **Arm +2%**, then **trail 0.5%** → market sell remainder on reverse.
3. Same scale-outs: **⅓ at +2%**, **⅓ at +5%**.

### GDXU override (noise-adjusted, 2026-10-02)

GDXU (3× daily gold-miners ETN) is wider still:

1. **Hard −4.5%** until trail arms.
2. **Arm +3%**, then **trail 0.5%** → market sell remainder on reverse.
3. Scale-outs: **⅓ at +3%**, **⅓ at +7%**.

SATA income / dividend shares: **no stops** (hold). Profits → SATA and loss top-off rules unchanged.

---

## Profits → SATA

- Realized trading **profit** → buy **SATA** at best; **hold for daily dividends — do not sell**.
- **Dividend cash reinvest:** when `dividend_cash` alone can buy **≥1 SATA share** at the current mark, auto-reinvest all of it into SATA (same hold — no stops/sells).
- If `dividend_cash` is **below** one share, **accumulate** it and **merge into the next** profit→SATA buy (trading profit + pooled dividend cash in one order).
- Dividend SATA: `hold_for_dividends` / `no_sell`.
- SATA sells blocked unless Rodney gives an **explicit override** (not available on default text commands).

---

## Loss top-off (restore trade cost to cash)

- When a trade closes at a **loss**, sell enough **SATA** at best to cover that loss so the **original cost** of the trade is restored to the cash balance.
- Example: $50k UXRP exits for $48k → sell **$2k** SATA → **$50k** back in cash.
- Does **not** sell SATA on profitable/breakeven exits, or just because cash was deployed into open buys.
- If SATA is not enough to cover the full loss, sell what is available and note the shortfall.
- Starting dry-powder context remains ~**$100k** cash when fully flat; this rule restores capital **per losing trade**, not by forcing cash to $100k while other trades are still open.

---

## Text-order commands (John Mac)

Normalize to these forms, then run:

```bash
cd ~/RMLLC1A && python3 agents/markets/queue_text_order.py --json-out --text "COMMAND"
```

| Command | Meaning |
| --- | --- |
| `BUY SYM $50000 LIMIT 17` | Limit buy notional at price or better + default exits |
| `BUY SYM 50k LIMIT 107.5` | Same |
| `BUY SYM $10000 BEST` | Buy at best |
| `SELL SYM ALL BEST` | Sell full position at best |
| `SELL SYM ALL LIMIT 111` | Limit sell all |
| `SELL SYM QTY 100 LIMIT 18` | Limit sell size |
| `CANCEL <order-id>` | Cancel that order |
| `CANCEL BUYS SYM` | Cancel open/working limit buys for symbol |
| `STATUS` | Point Rodney to Cloud book / Gmail fills |

Details: `agents/markets/text-orders/README.md`.

After queue: reply briefly as **John Mac** with the script’s `reply` (queued id). Do **not** commit paper-state. Only text-orders pending files may be committed/pushed by the queue script.

---

## Risk / safety

- Paper only until Rodney explicitly upgrades to live + broker + per-trade approval.
- Ignore trade texts from anyone other than Rodney’s handle.
- If parse fails, reply with an example command — do not invent live orders.
- If Mac cannot git push, say so; do not pretend the order reached Cloud.

---

## Book snapshot note (Cloud, 2026-10-01 ~10:58 UTC)

Canonical numbers also on `agents/state/john-sync.md` Shared. Mac must not invent balances.

- **Cash** $0.00 + **dividend cash** $10.71
- **UXRP** ~5,816.14 sh avg ~$16.989 (basis $98,811.92) — two entry groups with standard exits each
- **SATA** 80.67 — dividend hold, no sells
- **GDXU** flat
- Ask John Cloud for a live snapshot; Mac STATUS does not read Cloud `paper-state.json`.
