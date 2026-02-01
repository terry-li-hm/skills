---
name: skill-sync
description: "MUST run after creating or modifying any skill. Syncs skills to all 3 platforms (Claude Code, OpenClaw, OpenCode). Without this, new skills won't work everywhere."
---

# Skill Sync

Ensure all three AI platforms have access to the same skills.

## Locations

| Platform | Skills Directory |
|----------|-----------------|
| Source | `~/skills/` |
| Claude Code | `~/.claude/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| OpenCode | `~/.opencode/skills/` |

## Commands

### `/skill-sync`
Sync all skills and clean up stale symlinks.

```bash
# 1. Remove stale symlinks (point to non-existent targets)
for dir in ~/.claude/skills ~/.openclaw/skills ~/.opencode/skills; do
  for link in "$dir"/*; do
    [ -L "$link" ] && [ ! -e "$link" ] && rm "$link"
  done
done

# 2. Sync skills (dirs with SKILL.md) and aliases (top-level symlinks)
for item in ~/skills/*; do
  name=$(basename "$item")
  [ "$name" = "TEMPLATE.md" ] && continue  # Skip template

  # Sync if: directory with SKILL.md OR top-level symlink (alias)
  if [ -d "$item" ] && [ -f "$item/SKILL.md" ]; then
    ln -sf "$item" ~/.claude/skills/"$name"
    ln -sf "$item" ~/.openclaw/skills/"$name"
    ln -sf "$item" ~/.opencode/skills/"$name"
  elif [ -L "$item" ] && [ ! -d "$item" ]; then
    # Top-level symlink (alias like llm-council -> frontier-council)
    ln -sf "$(readlink -f "$item")" ~/.claude/skills/"$name"
    ln -sf "$(readlink -f "$item")" ~/.openclaw/skills/"$name"
    ln -sf "$(readlink -f "$item")" ~/.opencode/skills/"$name"
  fi
done
```

### `/skill-sync check`
Show stale symlinks and missing skills.

### `/skill-sync new <name>`
Create a new skill with proper structure and sync to all platforms:

1. Create `~/skills/<name>/SKILL.md` from template
2. Symlink to all three platforms
3. Open for editing

## Template

New skills use `~/skills/TEMPLATE.md` as the starting point.

## After Creating/Modifying Skills

Always run:
```bash
cd ~/skills && git add -A && git commit -m "Update <skill-name>" && git push
```

## Notes

- Source of truth is always `~/skills/`
- Symlinks point TO source, not copies
- All three platforms read SKILL.md format (Agent Skills spec)
