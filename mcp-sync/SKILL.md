---
name: mcp-sync
description: Sync MCP servers across Claude Code, Codex, and OpenCode. Use when adding a new MCP server or checking sync status.
user_invocable: true
---

# MCP Sync

Syncs MCP server configurations across all three AI coding tools.

## Architecture

```
~/.opencode/mcp.json     ← Canonical source (JSON)
        ↓
~/.codex/config.toml     ← Auto-generated (TOML)
        ↓
claude mcp add           ← Manual commands (CLI)
```

## Usage

```bash
# Dry run - show what would change
uv run ~/scripts/mcp-sync.py

# Apply changes to Codex, print Claude commands
uv run ~/scripts/mcp-sync.py --apply
```

## Workflow

1. **Add new server to OpenCode:** Edit `~/.opencode/mcp.json`
2. **Run sync:** `mcp-sync --apply`
3. **Run printed Claude commands** to update Claude Code

## Notes

- Codex-only servers (`context7`, `serena`) are preserved and not overwritten
- API key env vars are referenced as `${VAR}` in Codex config
- Claude Code servers managed by plugins are skipped
