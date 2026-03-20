---
name: todo
description: Manage TODO.md in the vault with time-based scheduling. Use when user says "todo", "add todo", "check todo", "done with", "overdue", or "someday".
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
| When | `` `when:YYYY-MM-DD` `` | Don't surface until this date |
| Deadline | `` `due:YYYY-MM-DD` `` | Hard due date. Overdue after this. |
| Someday | `` `someday` `` | Deferred indefinitely. Hidden from Today/Upcoming. |
| Agent | `` `agent:` `` | Claude executes this autonomously — not a Terry action. |
| Low-energy | `` `low-energy` `` | Quick/simple task for downtime. Surfaced by `/mora`. |
| No tag | (nothing) | Anytime — visible in Today and All views. |

Dates are always ISO-8601 (`YYYY-MM-DD`). Regex patterns for parsing:

```
`when:(\d{4}-\d{2}-\d{2})`
`due:(\d{4}-\d{2}-\d{2})`
`someday`
```

## Commands

If `~/notes/TODO.md` is missing, create it with a minimal heading before running any command. If creation fails, report "TODO store unavailable" and stop.

### `/todo` (Today view — default)

```bash
todo-cli today
```

The CLI handles all date filtering, recurring item matching, grouping by section, and overdue detection. Present the output directly.

### `/todo today`

Same as bare `/todo` above.

### `/todo upcoming`

```bash
todo-cli upcoming
```

### `/todo overdue`

```bash
todo-cli overdue
```

### `/todo someday`

```bash
todo-cli someday
```

### `/todo all`

```bash
todo-cli all
```

### `/todo spare`

```bash
todo-cli spare
```

### `/todo stats`

```bash
todo-cli stats
```

### `/todo add <task>`

Add a new task — but apply the **intake gate** first.

**Intake gate (check before adding):**

| Test | Question | If NO → |
|------|----------|---------|
| **Irreversible** | If I miss this, is the consequence irreversible? | Lean skip |
| **Committed** | Has someone external been told this will happen? | Lean skip |
| **Natural recall** | Will I naturally remember this without a prompt? | If YES → skip |
| **Attention cost** | Does tracking this displace focus from higher-stakes items? | If YES → skip |

**Pass 1 or 2 → add.** Fail both but pass 3+4 → skip. If borderline, ask Terry rather than defaulting to add.

If the task clears the gate, append to end of file. User can include inline tags.

```bash
echo "- [ ] <task>" >> ~/notes/TODO.md
```
If append fails, report "Failed to add task" and do not claim success.

Examples:
- `/todo add Review PR #123`
- `/todo add Review PR #123 \`due:2026-02-14\``
- `/todo add Explore new framework \`someday\``

### `/todo done <partial match>`

Mark a task as done by partial text match. Find the line, replace `- [ ]` with `- [x]`, then move the completed line to `~/notes/TODO Archive.md` (append under the current month's section like `## March 2026`, creating it if it doesn't exist).
If no unique match is found, ask for a narrower match and do not modify files.

### `/todo schedule <match> <date>`

Add or update a `when:` date on a matching task.

**Logic:**
1. Find the unchecked line matching `<match>`
2. If line already has `` `when:...` ``, replace the date
3. If not, append `` `when:YYYY-MM-DD` `` before any existing `` `due:...` `` or at end of line
4. Use the Edit tool to modify the line
If `<date>` is not valid `YYYY-MM-DD`, reject and ask for a valid date.

### `/todo due <match> <date>`

Add or update a `due:` date on a matching task.

**Logic:**
1. Find the unchecked line matching `<match>`
2. If line already has `` `due:...` ``, replace the date
3. If not, append `` `due:YYYY-MM-DD` `` at end of line
4. Use the Edit tool to modify the line
If `<date>` is not valid `YYYY-MM-DD`, reject and ask for a valid date.

### `/todo defer <match>`

Add `someday` tag to a task. Removes any `when:` or `due:` tags (deferred = no dates).
If no unique match is found, ask for a narrower match and do not modify files.

### `/todo undefer <match>`

Remove `someday` tag from a task. Task becomes Anytime (visible in Today view).
If no unique match is found, ask for a narrower match and do not modify files.

### `/todo clean`

```bash
todo-cli clean
```

Moves all `[x]` items to `~/notes/TODO Archive.md` under the current month's section.

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
- **NEVER leave `- [x]` lines in TODO.md.** When marking done — whether via `/todo done` or manually — always move the completed line to `~/notes/TODO Archive.md` in the same edit. No exceptions, no "clean up later".
- **Reflections/journaling items live in `~/notes/Reflections Queue.md`** — not TODO.md
- **`🔋 Spare Capacity` section** = low-priority maintenance for spare token budget
- **`Someday` subsection** at the bottom of Spare Capacity = deferred indefinitely
- Dates are always ISO-8601 (`YYYY-MM-DD`), always in HKT context
- Tasks with no date tags are "Anytime" — shown in Today and All views
- When comparing dates, use `date +%Y-%m-%d` (system is HKT)
- Related files: `[[TODO Archive]]` · `[[Reflections Queue]]`

## Due Alarm Convention

When adding a task with `due:` within 7 days, also set a phone alarm:

```bash
moneo add --date YYYY-MM-DD "<task title>"
```

**Bar for Due at all:** Would forgetting cause real damage? If missing the moment has no cost (low-stakes admin, "sometime in April"), it belongs in TODO.md only — not Due. Due is for time-critical only.

**When to apply a moneo alarm:** Hard deadlines requiring action on a specific day — not `someday`, not `when:` gates, not recurring habits. Pick a time that fits the day (not just 9am default). This is a manual step — don't automate it, so the time is chosen deliberately.

## Boundaries

- Do NOT reinterpret task intent; only perform requested task list operations.
- Do NOT create project plans or prioritization frameworks here; this skill manages TODO state only.

## Example

> `/todo` → 6 tasks today, 2 overdue.
> Overdue: "Submit CPD record" (`due:2026-03-01`), "SmarTone bill" (`due:2026-03-02`).
> Added: "Review Capco deck `due:2026-03-05`".
