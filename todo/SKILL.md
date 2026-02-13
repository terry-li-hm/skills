---
name: todo
description: Manage TODO.md in the vault with Things 3-style scheduling. Use when user says "todo", "add todo", "check todo", "done with", "overdue", or "someday".
user_invocable: true
---

# Todo

Quick management of `~/notes/TODO.md` with time-based scheduling.

## Date Tag Format

Tasks can have inline date tags at the end of the line, wrapped in backticks:

```markdown
- [ ] Task with start date `when:2026-02-25`
- [ ] Task with deadline `due:2026-03-13`
- [ ] Task with both `when:2026-02-10` `due:2026-04-11`
- [ ] Deferred task `someday`
- [ ] Task with no dates (Anytime)
```

| Tag | Syntax | Meaning |
|-----|--------|---------|
| When | `` `when:YYYY-MM-DD` `` | Don't surface until this date (Things 3's "start date") |
| Deadline | `` `due:YYYY-MM-DD` `` | Hard due date. Overdue after this. |
| Someday | `` `someday` `` | Deferred indefinitely. Hidden from Today/Upcoming. |
| No tag | (nothing) | Anytime — visible in Today and All views. |

Dates are always ISO-8601 (`YYYY-MM-DD`). Regex patterns for parsing:

```
`when:(\d{4}-\d{2}-\d{2})`
`due:(\d{4}-\d{2}-\d{2})`
`someday`
```

## Commands

### `/todo` (Today view — default)

Show today's actionable tasks. This is the **default** when no subcommand is given.

**Logic:**
1. Run `date +%Y-%m-%d` to get today in HKT
2. Read `~/notes/TODO.md`
3. For each unchecked line (`- [ ]`):
   - SKIP if line contains `` `someday` ``
   - SKIP if line has `` `when:YYYY-MM-DD` `` where date > today
   - INCLUDE everything else (Anytime tasks, tasks where `when:` <= today, tasks with `due:`)
4. Group results by section heading (`## ...`)
5. Show overdue items first (`due:` date < today) with a warning prefix
6. Then show remaining today items
7. End with count: "X tasks today, Y overdue"

### `/todo today`

Same as bare `/todo` above.

### `/todo upcoming`

Show tasks scheduled for the next 14 days.

**Logic:**
1. Get today's date
2. For each unchecked line:
   - INCLUDE if `when:` date is between today and today+14
   - INCLUDE if `due:` date is between today and today+14
   - SKIP `someday` items
   - SKIP tasks with no date tags
3. Sort by earliest date (when or due)
4. Group by section heading

### `/todo overdue`

Show tasks past their deadline.

**Logic:**
1. Get today's date
2. For each unchecked line:
   - INCLUDE if `due:` date < today
3. Sort by how overdue (most overdue first)

### `/todo someday`

Show deferred tasks.

**Logic:** Show all unchecked lines containing `` `someday` ``, grouped by section.

### `/todo all`

Show all unchecked items regardless of date tags. This is the old default behaviour.

```bash
grep -n "^\- \[ \]" ~/notes/TODO.md
```

### `/todo add <task>`

Add a new task. Append to end of file. User can include inline tags.

```bash
echo "- [ ] <task>" >> ~/notes/TODO.md
```

Examples:
- `/todo add Review PR #123`
- `/todo add Review PR #123 \`due:2026-02-14\``
- `/todo add Explore new framework \`someday\``

### `/todo done <partial match>`

Mark a task as done by partial text match. Find the line, replace `- [ ]` with `- [x]`, then move the completed line to `~/notes/TODO Archive.md` (append under a dated section header like `## Archived YYYY-MM-DD`, creating one if today's doesn't exist).

### `/todo schedule <match> <date>`

Add or update a `when:` date on a matching task.

**Logic:**
1. Find the unchecked line matching `<match>`
2. If line already has `` `when:...` ``, replace the date
3. If not, append `` `when:YYYY-MM-DD` `` before any existing `` `due:...` `` or at end of line
4. Use the Edit tool to modify the line

### `/todo due <match> <date>`

Add or update a `due:` date on a matching task.

**Logic:**
1. Find the unchecked line matching `<match>`
2. If line already has `` `due:...` ``, replace the date
3. If not, append `` `due:YYYY-MM-DD` `` at end of line
4. Use the Edit tool to modify the line

### `/todo defer <match>`

Add `someday` tag to a task. Removes any `when:` or `due:` tags (deferred = no dates).

### `/todo undefer <match>`

Remove `someday` tag from a task. Task becomes Anytime (visible in Today view).

### `/todo clean`

Move all checked items (`- [x]`) to `~/notes/TODO Archive.md` under a dated section header, then remove them from TODO.md.

### `/todo spare`

Show the `🔋 Spare Capacity` section items — low-priority maintenance for when token budget has headroom.

## File Format

```markdown
## Section (optional emoji prefix)
- [ ] Unchecked task
- [ ] Task with dates `when:2026-02-25` `due:2026-03-13`
- [ ] Deferred task `someday`
- [x] Completed task
```

## Notes

- Single source: `~/notes/TODO.md`
- All agents (Claude Code, OpenCode) share this file
- Tasks grouped under `## Headings` — preserve section structure
- **Completed items are archived to `~/notes/TODO Archive.md`**, not left inline
- **Reflections/journaling items live in `~/notes/Reflections Queue.md`** — not TODO.md
- **`🔋 Spare Capacity` section** = low-priority maintenance for spare token budget
- **`Someday` subsection** at the bottom of Spare Capacity = deferred indefinitely
- Dates are always ISO-8601 (`YYYY-MM-DD`), always in HKT context
- Tasks with no date tags are "Anytime" — shown in Today and All views
- When comparing dates, use `date +%Y-%m-%d` (system is HKT)
- Related files: `[[TODO Archive]]` · `[[Reflections Queue]]`
