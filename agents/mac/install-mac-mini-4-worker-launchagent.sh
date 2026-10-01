#!/bin/bash
# Install LaunchAgent so mac-mini-4 worker starts at login and restarts if it exits.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PLIST_SRC="$REPO/agents/mac/com.rmllc1a.mac-mini-4-worker.plist"
RUN_SRC="$REPO/agents/mac/run-mac-mini-4-worker.sh"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PLIST_DST="$LAUNCH_AGENTS/com.rmllc1a.mac-mini-4-worker.plist"
LABEL="com.rmllc1a.mac-mini-4-worker"

mkdir -p "$LAUNCH_AGENTS" "$HOME/Library/Logs"
chmod +x "$RUN_SRC"

# Rewrite plist paths for this Mac user/repo (in case home differs).
sed \
  -e "s|/Users/regiaemanagementllc/RMLLC1A|$REPO|g" \
  -e "s|/Users/regiaemanagementllc|$HOME|g" \
  "$PLIST_SRC" > "$PLIST_DST"

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl kickstart -k "gui/$(id -u)/$LABEL" 2>/dev/null || launchctl start "$LABEL" || true

echo "Installed: $PLIST_DST"
echo "Label: $LABEL"
echo "Logs: $HOME/Library/Logs/cursor-mac-mini-4-worker.log"
echo "Check: launchctl print gui/$(id -u)/$LABEL | head"
echo "Worker should appear as mac-mini-4 at https://cursor.com/agents"
