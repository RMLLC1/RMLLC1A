#!/usr/bin/env python3
"""Refresh Soloway + Verified Investing public YouTube digests from channel RSS.

Also fetches auto-captions for **new** public videos (spoken digests) via a
caption HTTP endpoint, cleans them, and writes highlight bullets.

Writes under agents/markets/notes/gareth-soloway/.
Stdout JSON summary for the morning timer. No email. No git.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

CHANNELS = [
    {
        "key": "soloway",
        "label": "Gareth Soloway",
        "id": "UCwTu6kD2igaLMpxswtcdxlg",
        "handle": "@GarethSolowayProTrader",
        "digest": "last-30-days.md",
    },
    {
        "key": "verified",
        "label": "Verified Investing",
        "id": "UCZ-J2m1AUSLnifUEKam5_dA",
        "handle": "@verifiedinvesting",
        "digest": "verified-investing-last-30-days.md",
    },
]

BASE = Path(__file__).resolve().parent
LEVELS_PATH = BASE / "levels-current.md"
STATE_PATH = BASE / "refresh-state.json"
TRANSCRIPT_DIR = BASE / "transcripts"
SPOKEN_DIR = BASE / "spoken-digests"

# Free caption fetch (no API key). Fair-use / personal only.
TRANSCRIPT_URL = "https://youtube-transcript.ai/transcript/{vid}.txt"

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

HIGHLIGHT_RE = re.compile(
    r"("
    r"\$[\d,]+(?:\.\d+)?[kKmMbB]?|"
    r"\d+(?:\.\d+)?%|"
    r"\b(?:support|resistance|target|pullback|breakout|breakdown|"
    r"trend\s*line|invalidat|scene of the crime|neutral zone|"
    r"bull flag|bear flag|head and shoulders|scale[- ]?out|"
    r"daily close|line in the sand|buy zone|sell)\b"
    r")",
    re.I,
)


def fetch_rss(channel_id: str, channel_key: str, channel_label: str) -> list[dict]:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    with urllib.request.urlopen(url, timeout=45) as resp:
        root = ET.fromstring(resp.read())
    vids = []
    for e in root.findall("a:entry", NS):
        vid = e.find("yt:videoId", NS).text
        title = e.find("a:title", NS).text or ""
        pub = e.find("a:published", NS).text or ""
        desc_el = e.find("media:group/media:description", NS)
        desc = desc_el.text if desc_el is not None and desc_el.text else ""
        vids.append(
            {
                "id": vid,
                "title": title,
                "published": pub,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "description": desc,
                "members_only": "MEMBERS ONLY" in title.upper(),
                "channel_key": channel_key,
                "channel_label": channel_label,
            }
        )
    return vids


def trim_body(desc: str) -> tuple[str, list[str]]:
    desc = desc.replace("\r\n", "\n").strip()
    chapters: list[str] = []
    body = desc
    parts = re.split(r"\n\s*Chapters?:\s*\n|\n\s*CHAPTERS\s*\n", desc, maxsplit=1, flags=re.I)
    if len(parts) > 1:
        body = parts[0].strip()
        chapters = [ln.strip() for ln in parts[1].splitlines() if re.match(r"^\d", ln.strip())]
    for marker in (
        "Join Gareth",
        "Get more of Gareth",
        "More from Gareth",
        "Subscribe to Verified",
        "www.VerifiedInvesting.com",
        "#Stock",
        "#Gold",
        "#Silver",
        "#Bitcoin",
    ):
        idx = body.find(marker)
        if idx > 200:
            body = body[:idx].strip()
            break
    return body, chapters[:20]


def fetch_transcript_raw(vid: str) -> str:
    url = TRANSCRIPT_URL.format(vid=vid)
    req = urllib.request.Request(url, headers={"User-Agent": "RMLLC1A-soloway-refresh/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def clean_transcript(raw: str) -> str:
    """Drop metadata header; collapse tripled auto-caption lines; strip [music]."""
    text = raw.replace("\r\n", "\n")
    if "## Transcript" in text:
        text = text.split("## Transcript", 1)[1]
    out: list[str] = []
    for block in re.split(r"\n(?=\[\d+:\d+\])", text):
        block = block.strip()
        if not block:
            continue
        m = re.match(r"^\[(\d+:\d+(?::\d+)?)\]\s*(.*)$", block, re.S)
        if not m:
            continue
        ts, body = m.group(1), m.group(2)
        body = re.sub(r"\[music\]", " ", body, flags=re.I)
        body = re.sub(r"\s+", " ", body).strip()
        if not body:
            continue
        # Auto-captions sometimes repeat each phrase 3× in one block.
        words = body.split()
        n = len(words)
        cleaned = body
        if n >= 9 and n % 3 == 0:
            third = n // 3
            a, b, c = words[:third], words[third : 2 * third], words[2 * third :]
            if a == b == c:
                cleaned = " ".join(a)
            elif a == b:
                cleaned = " ".join(a + c)
        # Collapse repeated phrases (auto-caption stutter / triples).
        for _ in range(3):
            nxt = re.sub(r"\b(.{8,80}?)\s+\1(?:\s+\1)?\b", r"\1", cleaned)
            if nxt == cleaned:
                break
            cleaned = nxt
        out.append(f"[{ts}] {cleaned}")
    return "\n".join(out)


def extract_highlights(cleaned: str, limit: int = 18) -> list[str]:
    """Heuristic spoken bullets: sentences that look level/trade relevant."""
    plain = re.sub(r"\[\d+:\d+(?::\d+)?\]\s*", "", cleaned)
    # Split on sentence boundaries.
    parts = re.split(r"(?<=[.!?])\s+", plain)
    hits: list[str] = []
    seen: set[str] = set()
    skip_bits = (
        "subscribe",
        "members",
        "top squad",
        "verifiedinvesting.com",
        "rumble wallet",
        "not financial advice",
        "comment below",
        "like this video",
    )
    for p in parts:
        s = p.strip()
        if len(s) < 40 or len(s) > 320:
            continue
        low = s.lower()
        if any(b in low for b in skip_bits):
            continue
        if not HIGHLIGHT_RE.search(s):
            continue
        key = re.sub(r"\W+", "", low)[:80]
        if key in seen:
            continue
        seen.add(key)
        hits.append(s)
        if len(hits) >= limit:
            break
    return hits


def write_spoken_digest(vid: dict, cleaned: str, highlights: list[str]) -> Path:
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    SPOKEN_DIR.mkdir(parents=True, exist_ok=True)
    pub = (vid.get("published") or "")[:10]
    title = vid.get("title") or vid["id"]
    spoken_path = SPOKEN_DIR / f"{vid['id']}.md"
    tr_path = TRANSCRIPT_DIR / f"{vid['id']}.txt"
    tr_path.write_text(cleaned + "\n")
    lines = [
        f"# Spoken digest — {title}",
        "",
        f"- **Date:** {pub}",
        f"- **Channel:** {vid.get('channel_label')}",
        f"- **URL:** {vid.get('url')}",
        f"- **ID:** `{vid['id']}`",
        f"- **Source:** auto-captions (cleaned). Not a human watch.",
        "",
        "## Important points (heuristic from captions)",
        "",
    ]
    if highlights:
        for h in highlights:
            lines.append(f"- {h}")
    else:
        lines.append("- _(few level-like sentences found — read cleaned transcript)_")
    lines += [
        "",
        f"Full cleaned captions on disk: `transcripts/{vid['id']}.txt` (gitignored).",
        "",
    ]
    spoken_path.write_text("\n".join(lines))
    return spoken_path


def fetch_and_store_spoken(vid: dict) -> dict:
    """Fetch captions for one video. Returns status dict."""
    out = {"id": vid["id"], "title": vid.get("title"), "ok": False, "highlights": 0, "error": None}
    try:
        raw = fetch_transcript_raw(vid["id"])
        if "Transcript" not in raw and len(raw) < 200:
            out["error"] = "empty_or_blocked"
            return out
        cleaned = clean_transcript(raw)
        if len(cleaned) < 80:
            out["error"] = "clean_too_short"
            return out
        highlights = extract_highlights(cleaned)
        write_spoken_digest(vid, cleaned, highlights)
        out["ok"] = True
        out["highlights"] = len(highlights)
    except urllib.error.HTTPError as e:
        out["error"] = f"http_{e.code}"
    except Exception as e:  # noqa: BLE001 — surface in JSON for timer
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def load_spoken_highlights(vid_id: str) -> list[str]:
    path = SPOKEN_DIR / f"{vid_id}.md"
    if not path.exists():
        return []
    bullets = []
    in_section = False
    for ln in path.read_text().splitlines():
        if ln.startswith("## Important points"):
            in_section = True
            continue
        if in_section:
            if ln.startswith("## ") or ln.startswith("Full cleaned"):
                break
            if ln.startswith("- ") and "few level-like" not in ln:
                bullets.append(ln[2:].strip())
    return bullets


def render_digest(vids: list[dict], channel_label: str, handle: str) -> str:
    public = [v for v in vids if not v.get("members_only")]
    lines = [
        f"# {channel_label} — recent video digests",
        "",
        f"**Channel:** [{handle}](https://www.youtube.com/{handle})",
        "Deep digests from **official YouTube descriptions + chapters** (RSS),",
        "plus **spoken points from auto-captions** when available. Newest first.",
        "",
        f"**Refreshed:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"Public videos in feed: **{len(public)}** (YouTube RSS cap ~15).",
        "",
    ]
    for v in public:
        pub = (v.get("published") or "")[:10]
        body, chapters = trim_body(v.get("description") or "")
        lines += [
            f"## {pub} — {v['title']}",
            "",
            f"- **URL:** {v['url']}",
            f"- **ID:** `{v['id']}`",
            f"- **Channel:** {channel_label}",
            "",
            "### Summary (from description)",
            "",
            body or "_(no description)_",
            "",
        ]
        if chapters:
            lines.append("### Chapters")
            lines.append("")
            for c in chapters:
                lines.append(f"- {c}")
            lines.append("")
        spoken = load_spoken_highlights(v["id"])
        if spoken:
            lines.append("### Spoken points (from captions)")
            lines.append("")
            for s in spoken[:12]:
                lines.append(f"- {s}")
            lines.append("")
            lines.append(f"_Full spoken digest: `spoken-digests/{v['id']}.md`_")
            lines.append("")
        lines += ["---", ""]
    return "\n".join(lines)


def bump_levels_header(all_public: list[dict]) -> None:
    """Update as-of stamp + headline snapshot; keep curated body if present."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sorted_vids = sorted(all_public, key=lambda v: v.get("published") or "", reverse=True)
    newest = (sorted_vids[0].get("published") or "")[:10] if sorted_vids else now
    headlines = []
    for v in sorted_vids[:8]:
        ch = v.get("channel_label") or ""
        headlines.append(
            f"- **{(v.get('published') or '')[:10]}** [{ch}] — {v['title']}"
        )
    header = [
        "# Current levels & bias (Soloway / Verified Investing)",
        "",
        f"**As of:** {now} (RSS + caption refresh)",
        f"**Newest public video dated:** {newest}",
        "**Sources:** Gareth Soloway + Verified Investing public channel RSS + auto-captions.",
        '**Label in chat:** "Soloway/VI view as of <date>" — not advice; levels stale quickly.',
        "",
        "## Headline bias snapshot (newest across both channels)",
        "",
    ] + (headlines or ["- _(no public videos in feed)_"]) + ["", "---", ""]

    if LEVELS_PATH.exists():
        old = LEVELS_PATH.read_text()
        if "\n---\n" in old:
            curated = old.split("\n---\n", 1)[1].lstrip()
            if (
                curated.startswith("## Macro")
                or curated.startswith("## S&P")
                or "How to answer Rodney" in curated
            ):
                LEVELS_PATH.write_text("\n".join(header) + curated)
                return
        LEVELS_PATH.write_text("\n".join(header) + old)
    else:
        LEVELS_PATH.write_text(
            "\n".join(header) + "_Curated levels not yet written — see digest files._\n"
        )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--backfill",
        type=int,
        default=0,
        help="Also fetch spoken digests for N newest public videos missing captions files",
    )
    ap.add_argument(
        "--no-transcripts",
        action="store_true",
        help="Skip caption fetch (RSS digests only)",
    )
    args = ap.parse_args()

    prev = {}
    if STATE_PATH.exists():
        try:
            prev = json.loads(STATE_PATH.read_text())
        except json.JSONDecodeError:
            prev = {}
    prev_ids = set(prev.get("video_ids") or [])

    all_public: list[dict] = []
    per_channel: dict[str, int] = {}
    new_titles: list[str] = []
    new_ids: list[str] = []
    by_id: dict[str, dict] = {}
    channel_vids: dict[str, list[dict]] = {}

    for ch in CHANNELS:
        vids = fetch_rss(ch["id"], ch["key"], ch["label"])
        public = [v for v in vids if not v.get("members_only")]
        per_channel[ch["key"]] = len(public)
        all_public.extend(public)
        channel_vids[ch["key"]] = vids
        for v in public:
            by_id[v["id"]] = v
            if v["id"] not in prev_ids:
                new_ids.append(v["id"])
                new_titles.append(f"[{ch['label']}] {v['title']}")

    transcript_jobs: list[str] = []
    if not args.no_transcripts:
        seen_jobs: set[str] = set()
        for vid_id in new_ids:
            if vid_id not in seen_jobs:
                transcript_jobs.append(vid_id)
                seen_jobs.add(vid_id)
        if args.backfill > 0:
            newest = sorted(all_public, key=lambda v: v.get("published") or "", reverse=True)
            backfilled = 0
            for v in newest:
                if v["id"] in seen_jobs:
                    continue
                if (SPOKEN_DIR / f"{v['id']}.md").exists():
                    continue
                transcript_jobs.append(v["id"])
                seen_jobs.add(v["id"])
                backfilled += 1
                if backfilled >= args.backfill:
                    break

    spoken_results: list[dict] = []
    for i, vid_id in enumerate(transcript_jobs):
        v = by_id.get(vid_id)
        if not v:
            continue
        spoken_results.append(fetch_and_store_spoken(v))
        if i + 1 < len(transcript_jobs):
            time.sleep(0.6)  # be polite to free caption endpoint

    # Write digests after spoken files exist so bullets embed.
    for ch in CHANNELS:
        (BASE / ch["digest"]).write_text(
            render_digest(channel_vids[ch["key"]], ch["label"], ch["handle"])
        )

    ids = [v["id"] for v in all_public]
    bump_levels_header(all_public)

    state = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "video_ids": ids,
        "new_ids": new_ids,
        "new_titles": new_titles,
        "spoken_fetched": [r["id"] for r in spoken_results if r.get("ok")],
        "channels": {c["key"]: c["id"] for c in CHANNELS},
    }
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")

    summary = {
        "updated": state["updated"],
        "channels": per_channel,
        "public_in_feed": len(all_public),
        "new_count": len(new_ids),
        "new_titles": new_titles,
        "spoken_attempted": len(spoken_results),
        "spoken_ok": sum(1 for r in spoken_results if r.get("ok")),
        "spoken_results": spoken_results,
        "note": (
            "No email on Soloway/VI refresh; chat only if new_count > 0. "
            "Read spoken-digests/ for caption points; no git."
        ),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
