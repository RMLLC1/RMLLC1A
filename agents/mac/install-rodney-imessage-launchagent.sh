#!/bin/bash
# Install the Rodney iMessage watcher. It starts at login.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PLIST_SRC="$REPO/agents/mac/com.rmllc1a.rodney-imessage.plist"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PLIST_DST="$LAUNCH_AGENTS/com.rmllc1a.rodney-imessage.plist"
LABEL="com.rmllc1a.rodney-imessage"

mkdir -p "$LAUNCH_AGENTS" "$HOME/Library/Logs" "$HOME/Library/Application Support/john-mac"
chmod +x "$REPO/agents/mac/rodney_imessage_watch.py"

sed \
  -e "s|/Users/regiaemanagementllc/RMLLC1A|$REPO|g" \
  -e "s|/Users/regiaemanagementllc|$HOME|g" \
  "$PLIST_SRC" > "$PLIST_DST"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl kickstart -k "gui/$(id -u)/$LABEL" 2>/dev/null || true

echo "Installed: $PLIST_DST"
echo "Logs: $HOME/Library/Logs/john-mac-imessage.log"
echo "Full Disk Access is required for /Library/Developer/CommandLineTools/usr/bin/python3 so the watcher can read Messages."
