---
name: iter
description: HK bus stop navigator — know which stop to get off at when boarding an unfamiliar route. Use when boarding a bus and need to track stops or get an alert before your destination. NOT for MTR (use poros).
---

# iter — HK Bus Stop Navigator

## Commands

```bash
# Navigate a journey (main use case)
iter <route> <from_stop> <to_stop>
iter 1 "Prince Edward" "Star Ferry"
iter 74X "Sai Kung" "Diamond Hill"

# Adjust alert threshold (default: 2 stops out)
iter 1 "Mong Kok" "Jordan" --alert 3

# Browse all stops on a route first (then pick your stops)
iter 1 --list
iter 1 --list --inbound

# Force operator if auto-detect picks wrong one
iter 8 "Heng Fa Chuen" "Central" --operator ctb
```

## How it works

1. Fetches stop sequence from HK open data APIs (no auth required)
2. Fuzzy-matches your stop names (typos + partial names OK)
3. Shows the ordered stop list with boarding and exit highlighted
4. Press **Enter** each time you pass a stop
5. Sends a **Telegram push notification** at `--alert N` stops before destination
6. Prints "NEXT STOP IS YOURS" at 1 remaining; "GET OFF NOW" at 0

## Operators

| Flag | Operator | Routes |
|------|----------|--------|
| auto | KMB first, CTB fallback | most routes |
| `--operator kmb` | KMB/LWB | Kowloon + NT |
| `--operator ctb` | CTB/NWFB | HK Island + cross-harbour |

GMB (green minibus) not supported — different API.

## Gotchas

- **Route not found**: try `--inbound` (some routes only run one direction, or the stops are listed in reverse)
- **Wrong stops shown**: use `--list` first to see exact stop names, then copy-paste
- **Telegram alert missing**: check `TELEGRAM_BOT_TOKEN` env var is set (injected via 1Password at login)
- **Stop name matches wrong stop**: fuzzy threshold is 60; if it picks wrong one, use a more specific substring (e.g., "Star Ferry Harbour" instead of just "Star Ferry")
- **N+1 API calls**: ~25 HTTP calls to fetch stop names on first run — takes 5–10 seconds. Normal.
- **Shebang uses `uv run --script`**: direct execution (`iter`) works because `~/bin/iter → ~/code/iter/iter.py`

## Files

- Script: `~/code/iter/iter.py`
- Symlink: `~/bin/iter`
- Repo: `https://github.com/terry-li-hm/iter`
- APIs: `data.etabus.gov.hk` (KMB) · `rt.data.gov.hk` (CTB)

## Related

- `poros` — MTR journey time CLI (sister tool)
