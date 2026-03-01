---
name: agent-sync
description: "Sync skills, MCP servers, and compound-engineering across Claude Code, OpenCode, and Codex. Run after any config change."
user_invocable: true
---

# Agent Sync

Single command to keep all AI coding tools in sync. Replaces `/skill-sync` and `/mcp-sync`.

## What it syncs

| Step | What | How |
|------|------|-----|
| 1. Skills | Symlink `~/skills/` → CC, OpenCode, Codex | `~/bin/agent-sync` (Rust binary, `~/code/agent-sync/`) |
| 2. MCP servers | `~/agent-config/mcp-servers.json` → Codex, OpenCode | `mcp-sync --apply` |
| 3. Compound-engineering | Plugin → Codex format | `bunx @every-env/compound-plugin install compound-engineering --to codex` |

## Usage

### `/agent-sync`

Run all three steps:

```bash
~/bin/agent-sync --full
```

Skills only (fast, what the git hook runs):

```bash
~/bin/agent-sync
```

Dry run:

```bash
~/bin/agent-sync --check
```

Binary source: `~/code/agent-sync/` (Rust). Rebuild after changes: `cargo build --release` in that dir.

### `/agent-sync check`
Show current state without changing anything. Check each target for stale or missing symlinks.

### `/agent-sync new <name>`
Create a new skill and sync to all platforms:

1. Create `~/skills/<name>/SKILL.md` from `~/skills/TEMPLATE.md`
2. Symlink to all targets
3. Open for editing

## Locations

| Platform | Skills | MCP | Instructions |
|----------|--------|-----|-------------|
| Source | `~/skills/` | `~/agent-config/mcp-servers.json` | `~/CLAUDE.md` |
| Claude Code | `~/.claude/skills/` | `claude mcp add` (manual) | `~/.claude/CLAUDE.md` (auto) |
| OpenCode | `~/.opencode/skills/` | `~/.opencode/mcp.json` | — |
| Codex | `~/.codex/skills/` | `~/.codex/config.toml` | `~/.codex/AGENTS.md → ~/CLAUDE.md` |
| Codex (agents) | `~/.agents/skills/` | — | — |

## After creating/modifying skills

```bash
cd ~/skills && git add -A && git commit -m "Update <skill-name>" && git push
```

## Codex CLI Gotchas

- **Dir-level symlinks break skill discovery** ([#11314](https://github.com/openai/codex/issues/11314)): `~/.agents/skills → ~/skills/` doesn't work. Must be a real directory with per-skill symlinks inside.
- **Two skill paths:** `~/.codex/skills/` and `~/.agents/skills/` — skill-sync populates both.
- **AGENTS.md already symlinked:** `~/.codex/AGENTS.md → ~/CLAUDE.md` (set up Feb 4).
- **Skills invocation:** `$skill-name` (not `/skill-name`).
- **No hooks interception** in Codex — `notify` only (post-turn). Hooks PR rejected by OpenAI.
- **Memory CLIs work unchanged** from Codex shell: `oghma`, `qmd`, `km-ask` are just bash commands.

## Notes

- Source of truth is always `~/skills/` (skills), `~/agent-config/mcp-servers.json` (MCP), CE plugin (compound-engineering)
- Symlinks point TO source, not copies
- `~/.agents/skills/` must be a real directory (not a dir-level symlink) — Codex bug [#11314](https://github.com/openai/codex/issues/11314)
- CE install appends a tool mapping block to CLAUDE.md — idempotent, overwrites previous block
- Claude Code MCP commands are printed but not auto-executed (requires manual run)
