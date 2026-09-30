#!/usr/bin/env python3
"""Refresh Soloway + Verified Investing public YouTube digests from channel RSS.

Writes under agents/markets/notes/gareth-soloway/.
Stdout JSON summary for the morning timer. No email. No git.
"""

from __future__ import annotations

import json
import re
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

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


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


def render_digest(vids: list[dict], channel_label: str, handle: str) -> str:
    public = [v for v in vids if not v.get("members_only")]
    lines = [
        f"# {channel_label} — recent video digests",
        "",
        f"**Channel:** [{handle}](https://www.youtube.com/{handle})",
        "Deep digests from **official YouTube descriptions + chapters** (RSS). Newest first.",
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
        f"**As of:** {now} (RSS refresh)",
        f"**Newest public video dated:** {newest}",
        "**Sources:** Gareth Soloway + Verified Investing public channel RSS.",
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

    for ch in CHANNELS:
        vids = fetch_rss(ch["id"], ch["key"], ch["label"])
        public = [v for v in vids if not v.get("members_only")]
        per_channel[ch["key"]] = len(public)
        all_public.extend(public)
        (BASE / ch["digest"]).write_text(render_digest(vids, ch["label"], ch["handle"]))
        for v in public:
            if v["id"] not in prev_ids:
                new_ids.append(v["id"])
                new_titles.append(f"[{ch['label']}] {v['title']}")

    ids = [v["id"] for v in all_public]
    bump_levels_header(all_public)

    state = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "video_ids": ids,
        "new_ids": new_ids,
        "new_titles": new_titles,
        "channels": {c["key"]: c["id"] for c in CHANNELS},
    }
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")

    summary = {
        "updated": state["updated"],
        "channels": per_channel,
        "public_in_feed": len(all_public),
        "new_count": len(new_ids),
        "new_titles": new_titles,
        "note": "No email on Soloway/VI refresh; chat only if new_count > 0",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
