---
name: todo
description: Manage TODO.md in the vault. Use when user says "todo", "add todo", "todos", "check todo", or "done with".
user_invocable: true
---

# Todo

Quick management of `~/notes/TODO.md`.

## Commands

### `/todo` or `/todos`
List all unchecked items.

### `/todo add <task>`
Add a new task. Example: `/todo add Review PR #123`

### `/todo done <partial match>`
Mark a task as done by partial text match. Example: `/todo done PR #123`

## Implementation

**List todos:**
```bash
grep -n "^\- \[ \]" ~/notes/TODO.md
```

**Add todo:**
```bash
echo "- [ ] <task>" >> ~/notes/TODO.md
```

**Mark done** (match and replace `- [ ]` with `- [x]`):
- Find the line matching the partial text
- Replace `- [ ]` with `- [x]` on that line

## File Format

```markdown
## Section (optional)
- [ ] Unchecked task
- [x] Completed task
```

## Notes

- Single source: `~/notes/TODO.md` (symlinked from `~/clawd/TODO.md`)
- All 3 agents (Claude Code, OpenClaw, OpenCode) share this file
- Tasks can be grouped under `## Headings`
- Completed items stay in file (for history) unless user asks to clean up
- `/todo clean` can remove all checked items if requested
