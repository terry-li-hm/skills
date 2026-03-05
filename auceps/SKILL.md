---
name: auceps
description: Smart wrapper for the bird X/Twitter CLI. Use instead of bare bird — auto-routes URLs, handles, and search; adds --vault and --lustro output modes.
user_invocable: false
---

# auceps

Smart bird CLI wrapper. Auto-routes input, always injects auth, normalises errors. Use instead of calling bird directly.

## Commands

### Auto-routed (main interface)

```bash
auceps <url>           # x.com URL → bird read
auceps @handle         # handle → bird about + user-tweets combined
auceps handle          # bare handle (no @) → same as above
auceps "search query"  # multi-word → bird search
```

### Explicit subcommands

```bash
auceps thread <url> [--depth 2]   # follow quoted tweet chain
auceps bird <any bird args>        # direct passthrough to bird
```

### Output flags (global)

```bash
auceps @handle --vault      # Obsidian markdown: # @handle (Name), bio, tweets
auceps @handle --lustro     # JSON for lustro x_accounts ingestion
auceps @handle -n 5         # limit tweets (default: 20)
```

## Lustro JSON schema

```json
{
  "handle": "@handle",
  "name": "Display Name",
  "focus": "",
  "tier": 2
}
```

Note: `focus` is empty — bird doesn't expose profile bio text. Fill manually after generating.

## Gotchas

- **Auth:** Prefers `AUTH_TOKEN`/`CT0` env vars (injected via `~/.zshenv.tpl` from 1Password). Falls back to `--cookie-source chrome` if env vars absent. Never add auth args manually.
- **SSH/tmux:** If env vars not injected, bird fails with keychain exit 36. Fix: ensure `AUTH_TOKEN`/`CT0` are in `~/.zshenv.tpl` and shell was started after `op inject`. The old `security unlock-keychain` workaround is obsolete.
- **`-n` not `-l`:** short flag for limit is `-n`, long is `--limit`
- **`about` not `profile`:** auceps uses the correct bird subcommand internally — callers never need to know
- **focus field:** `--lustro` leaves focus blank; bio isn't available from bird. Fill it manually or from context.
- **Thread depth:** `auceps thread` follows quoted tweet URLs via regex. Stops early if no quoted tweet found.

## Binary

`~/.cargo/bin/auceps` — install/update: `cd ~/code/auceps && cargo install --path .`

## Source

`~/code/auceps/` — Rust, edition 2024, no async. Reference: keryx (subprocess pattern), stips (ExitCode entry point).
