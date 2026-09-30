#!/usr/bin/env python3
"""Refresh Gareth Soloway public YouTube digests from channel RSS.

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

CHANNEL_ID = "UCwTu6kD2igaLMpxswtcdxlg"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
BASE = Path(__file__).resolve().parent
DIGEST_PATH = BASE / "last-30-days.md"
LEVELS_PATH = BASE / "levels-current.md"
STATE_PATH = BASE / "refresh-state.json"

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch_rss() -> list[dict]:
    with urllib.request.urlopen(RSS_URL, timeout=45) as resp:
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


def render_digest(vids: list[dict]) -> str:
    lines = [
        "# Last ~30 days — video digests",
        "",
        "Deep digests from **official YouTube descriptions + chapters** (RSS). Newest first.",
        "",
        f"**Refreshed:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        f"Public videos in feed: **{len(vids)}** (YouTube RSS cap ~15).",
        "",
    ]
    for v in vids:
        if v.get("members_only"):
            continue
        pub = (v.get("published") or "")[:10]
        body, chapters = trim_body(v.get("description") or "")
        lines += [
            f"## {pub} — {v['title']}",
            "",
            f"- **URL:** {v['url']}",
            f"- **ID:** `{v['id']}`",
            "",
            "### Summary (from his description)",
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


def bump_levels_header(vids: list[dict]) -> None:
    """Update as-of stamp + headline snapshot; keep curated body if present."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    newest = (vids[0].get("published") or "")[:10] if vids else now
    headlines = []
    for v in vids[:5]:
        if v.get("members_only"):
            continue
        headlines.append(f"- **{(v.get('published') or '')[:10]}** — {v['title']}")
    header = [
        "# Current levels & bias (Soloway)",
        "",
        f"**As of:** {now} (RSS refresh)",
        f"**Newest public video dated:** {newest}",
        "**Sources:** public channel RSS descriptions.",
        '**Label in chat:** "Soloway\'s view as of <date>" — not advice; levels stale quickly.',
        "",
        "## Headline bias snapshot (newest in feed)",
        "",
    ] + (headlines or ["- _(no public videos in feed)_"]) + ["", "---", ""]

    if LEVELS_PATH.exists():
        old = LEVELS_PATH.read_text()
        # Keep curated sections after first horizontal rule if present
        if "\n---\n" in old:
            curated = old.split("\n---\n", 1)[1].lstrip()
            # Drop old auto header if file was fully auto
            if curated.startswith("## Macro") or curated.startswith("## S&P") or "How to answer Rodney" in curated:
                LEVELS_PATH.write_text("\n".join(header) + curated)
                return
        # Fallback: prepend snapshot note
        LEVELS_PATH.write_text("\n".join(header) + old)
    else:
        LEVELS_PATH.write_text("\n".join(header) + "_Curated levels not yet written — see last-30-days.md._\n")


def main() -> None:
    prev = {}
    if STATE_PATH.exists():
        try:
            prev = json.loads(STATE_PATH.read_text())
        except json.JSONDecodeError:
            prev = {}
    prev_ids = set(prev.get("video_ids") or [])

    vids = fetch_rss()
    public = [v for v in vids if not v.get("members_only")]
    ids = [v["id"] for v in public]
    new_ids = [i for i in ids if i not in prev_ids]
    new_titles = [v["title"] for v in public if v["id"] in set(new_ids)]

    DIGEST_PATH.write_text(render_digest(public))
    bump_levels_header(public)

    state = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "video_ids": ids,
        "new_ids": new_ids,
        "new_titles": new_titles,
    }
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")

    summary = {
        "updated": state["updated"],
        "public_in_feed": len(public),
        "new_count": len(new_ids),
        "new_titles": new_titles,
        "digest": str(DIGEST_PATH),
        "note": "No email on Soloway refresh; chat only if new_count > 0",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
