---
name: mcp-sync
description: Sync MCP servers from Claude Code to Codex and OpenCode. Use when adding a new MCP server or checking sync status.
user_invocable: true
---

# MCP Sync

Syncs MCP server configurations from Claude Code (canonical) to Codex and OpenCode.

## Architecture

```
~/agent-config/claude/claude.json   ← Canonical source (with API keys)
        ↓
~/.codex/config.toml                ← TOML, API keys as ${VAR}
~/.opencode/mcp.json                ← JSON, API keys stripped
```

## Usage

```bash
# Dry run - show what would change
mcp-sync

# Apply changes
mcp-sync --apply
```

## Workflow

1. **Add server via Claude:** `claude mcp add <name> -- <command>`
2. **Run sync:** `mcp-sync --apply`

Or edit `~/agent-config/claude/claude.json` directly, then sync.

## Notes

- API keys stored only in Claude config (version controlled)
- Codex uses `${VAR}` env var references
- OpenCode gets API keys stripped (reads from env at runtime)
- Codex-only servers (`context7`, `serena`) are auto-added
