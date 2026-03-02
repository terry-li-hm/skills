---
name: lucus
description: "Git worktree manager for parallel AI agent sessions. Use when starting a new feature/fix that needs isolation from other Claude Code / Codex / Gemini sessions running on the same repo."
user_invocable: false
---

# lucus — Git Worktree Manager

Repo: `~/code/lucus` | crates.io: `lucus` | Phase 1 shipped 2026-03-02

## When to use

Whenever running **parallel AI agent sessions** on the same repo. Each session gets its own worktree — no staging conflicts, no dirty index surprises from `git add -A` in another session.

## Core commands

```bash
lucus new feat/auth          # create worktree + branch at ../{repo}.{branch}
lucus list                   # all worktrees: branch, path, ahead/behind, uncommitted
lucus switch feat/auth       # cd into worktree (requires shell wrapper — see Setup)
lucus remove feat/auth       # tear down worktree + delete branch
lucus query feat/auth        # print path only (used internally by shell wrapper)
```

## Setup (one-time)

```bash
lucus init zsh               # writes shell function to ~/.zshrc
source ~/.zshrc              # activate in current shell
```

The shell wrapper is needed for `lucus switch` to actually `cd` — a binary can't change the parent shell's directory on its own.

## Config

`~/.config/lucus/config.toml` — created on first use with defaults:

```toml
[worktree]
path_template = "../{repo}.{branch}"   # worktrees land as siblings of the repo
default_branch = "main"

[hooks]
post_create = []       # blocking hooks run after worktree creation
post_create_bg = []    # background hooks (fire and forget)
pre_remove = []
post_remove = []
```

## Output

- TTY: coloured human table
- Non-TTY / `--json`: NDJSON (one object per line, `jq`-friendly)

## Symbolic shortcuts (Phase 2+)

```bash
lucus switch -   # previous worktree
lucus switch ^   # default branch
lucus switch @   # current worktree
```

## Gotchas

- `lucus switch` requires the shell wrapper (`lucus init zsh`) to actually `cd`
- Worktrees land at `../{repo}.{branch}` by default — sibling directories of the source repo
- `git2::Worktree` has no `.open()` — use `Repository::open(wt.path())` (fixed in Phase 1)
- Codex sandbox blocks crates.io DNS — always `cargo build` outside the sandbox

## Roadmap

- **Phase 2 (v0.3.0):** `lucus new "natural language prompt"` → Haiku generates branch name, persists task to `.lucus/tasks/`. Progressive list rendering (rayon + indicatif). Per-project `.lucus.toml`.
- **Phase 3 (v0.4.0):** `lucus merge`, `lucus status`, `lucus clean`, tmux integration, shell completions.
