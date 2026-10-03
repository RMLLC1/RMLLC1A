#!/bin/bash
# Starts the Cursor My Machines worker for John Mac (mac-mini-4).
set -euo pipefail

export HOME="${HOME:-/Users/regiaemanagementllc}"
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

REPO="${RMLLC1A_REPO:-$HOME/RMLLC1A}"
AGENT_BIN="$(command -v agent || true)"

if [[ -z "$AGENT_BIN" ]]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ERROR: agent CLI not found on PATH" >&2
  exit 1
fi

if [[ ! -d "$REPO" ]]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ERROR: repo missing: $REPO" >&2
  exit 1
fi

cd "$REPO"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) pulling handoff branch before worker start"
if GIT_TERMINAL_PROMPT=0 git pull --ff-only origin cursor/agent-department-names-cbe0; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) handoff pull ok"
  if [[ -f agents/state/john-sync.md ]]; then
    grep -m 1 "Last board update" agents/state/john-sync.md || true
  fi
else
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) WARNING: handoff pull failed; worker will still start" >&2
fi

echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) starting mac-mini-4 worker in $REPO"
exec "$AGENT_BIN" worker start --name "mac-mini-4" --worker-dir "$REPO"
