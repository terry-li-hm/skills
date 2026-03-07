---
name: safe-rm
description: Safe rm CLI — validates paths and performs deletion with confirmation. Replaces safe_rm.py.
---

# safe-rm

Rust CLI that wraps deletion: validates protected paths, shows what will be deleted, prompts for confirmation, then performs the actual `rm`.

Replaces the old two-step: `python3 ~/scripts/safe_rm.py <path>` + manual `rm`.

## Installation

```bash
cd ~/code/safe-rm && cargo build --release
ln -sf ~/code/safe-rm/target/release/safe-rm ~/bin/safe-rm
```

## Commands

```bash
# Interactive delete (shows size, prompts y/N)
safe-rm ~/some/path

# Multiple paths — validates all before prompting
safe-rm ~/path/a ~/path/b

# Skip confirmation (for hooks/scripts)
safe-rm --force ~/path

# Dry run — validate and report, no delete
safe-rm --dry-run ~/path
safe-rm -n ~/path
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Deleted, dry-run OK, or user aborted |
| 1 | Protected path blocked |
| 2 | IO error during deletion |

## Protected Paths

Refuses to delete (exit 1):
- `/`, `/Users`, `/Users/terry`, `~`
- `~/.ssh`, `~/.gnupg`
- `/etc`, `/usr`, `/System`, `/bin`, `/sbin`, `/var`, `/tmp`

Also blocks deletion of any parent of a protected path.

## Hook Integration

CLAUDE.md hook: `rm -rf` → `safe-rm <path>` (replaces `python3 ~/scripts/safe_rm.py <path>`)

The `--force` flag is for scripted use where the hook has already validated. For interactive use, let it prompt.

## Source

`~/code/safe-rm/` — Rust, clap 4, release profile with strip=true.
