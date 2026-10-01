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
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) starting mac-mini-4 worker in $REPO"
exec "$AGENT_BIN" worker start --name "mac-mini-4" --worker-dir "$REPO"
