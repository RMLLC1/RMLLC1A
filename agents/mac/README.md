# Mac Mini worker (John Mac)

Keeps My Machines worker **`mac-mini-4`** running so **John Mac** can attach after reboot.

## Install (once, on the Mac Mini)

```bash
cd ~/RMLLC1A
git fetch origin
git checkout cursor/agent-department-names-cbe0
git pull
bash agents/mac/install-mac-mini-4-worker-launchagent.sh
```

## What it does

- Starts at **login** (`RunAtLoad`)
- Restarts if the worker exits (`KeepAlive`)
- Logs to `~/Library/Logs/cursor-mac-mini-4-worker.log`

## After reboot

1. Log into the Mac (or enable automatic login for this user).
2. Wait ~30 seconds for the worker to connect.
3. Open [cursor.com/agents](https://cursor.com/agents) → environment **mac-mini-4** → open/create **John Mac**.

The worker auto-starts; the John Mac *chat* still needs to be opened once (Reconnect works once the worker is online).

## Stop / uninstall

```bash
launchctl bootout "gui/$(id -u)/com.rmllc1a.mac-mini-4-worker"
rm -f ~/Library/LaunchAgents/com.rmllc1a.mac-mini-4-worker.plist
```
