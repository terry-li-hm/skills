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

# 2. Sync valid skills (must have SKILL.md)
for skill in ~/skills/*/; do
  name=$(basename "$skill")
  [ -f "$skill/SKILL.md" ] || continue  # Only sync if SKILL.md exists
  ln -sf "$skill" ~/.claude/skills/"$name"
  ln -sf "$skill" ~/.openclaw/skills/"$name"
  ln -sf "$skill" ~/.opencode/skills/"$name"
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
