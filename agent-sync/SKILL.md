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
| 1. Skills | Symlink `~/skills/` → CC, OpenCode, Codex | Python script (avoids zsh glob bugs) |
| 2. MCP servers | `~/agent-config/mcp-servers.json` → Codex, OpenCode | `mcp-sync --apply` |
| 3. Compound-engineering | Plugin → Codex format | `bunx @every-env/compound-plugin install compound-engineering --to codex` |

## Usage

### `/agent-sync`

Run all three steps:

```python
#!/usr/bin/env python3
"""Sync skills, MCP servers, and CE across all AI coding tools."""
import pathlib
import subprocess
import sys

HOME = pathlib.Path.home()
SKILLS_DIR = HOME / "skills"
TARGETS = [
    HOME / ".claude" / "skills",
    HOME / ".opencode" / "skills",
    HOME / ".codex" / "skills",
    HOME / ".agents" / "skills",
]
SKIP = {"TEMPLATE.md", ".git", ".archive", ".cache", ".gitignore", "config.json"}


def sync_skills():
    """Step 1: Symlink skills to all targets."""
    for t in TARGETS:
        t.mkdir(parents=True, exist_ok=True)

    # Clean stale symlinks
    for t in TARGETS:
        for link in t.iterdir():
            if link.is_symlink() and not link.exists():
                link.unlink()

    count = 0
    for item in sorted(SKILLS_DIR.iterdir()):
        if item.name in SKIP or item.is_symlink():
            continue
        if item.is_dir() and (item / "SKILL.md").exists():
            for t in TARGETS:
                dest = t / item.name
                if dest.is_symlink() or dest.exists():
                    dest.unlink()
                dest.symlink_to(item)
            count += 1

    print(f"✓ Skills: {count} synced to {len(TARGETS)} targets")


def sync_mcp():
    """Step 2: Sync MCP servers."""
    mcp_script = HOME / "scripts" / "mcp-sync.py"
    if not mcp_script.exists():
        print("⚠ MCP sync: ~/scripts/mcp-sync.py not found, skipping")
        return
    result = subprocess.run(
        [sys.executable, str(mcp_script), "--apply"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        # Count lines that mention actual changes
        lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
        print(f"✓ MCP: synced ({len(lines)} lines output)")
    else:
        print(f"⚠ MCP sync failed: {result.stderr.strip()}")


def sync_ce():
    """Step 3: Install compound-engineering to Codex."""
    ce_dir = HOME / ".claude" / "plugins" / "marketplaces" / "every-marketplace"
    if not ce_dir.exists():
        print("⚠ CE: every-marketplace not installed, skipping")
        return
    result = subprocess.run(
        ["bunx", "@every-env/compound-plugin", "install", "compound-engineering", "--to", "codex"],
        capture_output=True, text=True, cwd=str(ce_dir)
    )
    if "Installed" in result.stdout or result.returncode == 0:
        print("✓ CE: compound-engineering installed to Codex")
    else:
        print(f"⚠ CE install failed: {result.stderr.strip()}")


if __name__ == "__main__":
    print("Agent Sync — syncing across all platforms\n")
    sync_skills()
    sync_mcp()
    sync_ce()
    print("\nDone. Restart Codex/OpenCode to pick up changes.")
```

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

## Notes

- Source of truth is always `~/skills/` (skills), `~/agent-config/mcp-servers.json` (MCP), CE plugin (compound-engineering)
- Symlinks point TO source, not copies
- `~/.agents/skills/` must be a real directory (not a dir-level symlink) — Codex bug [#11314](https://github.com/openai/codex/issues/11314)
- CE install appends a tool mapping block to CLAUDE.md — idempotent, overwrites previous block
- Claude Code MCP commands are printed but not auto-executed (requires manual run)
