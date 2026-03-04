---
name: due
description: Manage Due app reminders via moneo CLI. "due remind me", "add to Due", "remind me in X", "delete due reminder", "edit due reminder".
user_invocable: true
---

# Due App

Manage Due app reminders from the terminal using **moneo** (`~/bin/moneo`) — a CLI that edits the `.duedb` file directly, giving full read/add/edit/delete/recurrence capability.

## Trigger

Use when:
- User says "due remind me", "add to Due", "remind me in X"
- User wants to list, edit, or delete Due reminders
- User says "due search"

## Primary: moneo CLI

### Commands

```bash
moneo ls                                              # list all reminders with index
moneo add "Call dentist" --in 30m                    # relative time
moneo add "Standup" --at 09:30                       # today at HH:MM
moneo add "Pay rent" --date 2026-04-01 --at 10:00   # specific date + time
moneo add "Team sync" --at 11:00 --recur weekly      # recurring weekly
moneo add "Pay rent" --date 2026-04-01 --recur monthly  # recurring monthly
moneo edit <index> --title "New title"               # rename
moneo edit <index> --at 16:00                        # change time
moneo edit <index> --in 1h                           # push forward by 1h from now
moneo rm <index>                                     # delete by index
```

### Time flags (mutually exclusive)

| Flag | Example | Meaning |
|---|---|---|
| `--in` | `--in 30m` | Relative: `s`, `m`, or `h` |
| `--at` | `--at 14:35` | Today at HH:MM (HKT) |
| `--date` + `--at` | `--date 2026-04-01 --at 09:00` | Specific date + time |
| `--date` only | `--date 2026-04-01` | That date at 09:00 |

### Recurrence flag

`--recur daily|weekly|monthly|yearly` — sets `rf` + `rd` in `.duedb`. First occurrence = the date/time you specify.

### How it works

All operations edit `.duedb` directly (gzipped JSON). Due is killed with SIGTERM, file is written, Due is reopened. Changes are **Mac-only** — CloudKit is bypassed, so iPhone won't reflect them until Due's UI re-saves (edit a reminder and hit Save).

Due uses CloudKit (not iCloud Drive) for sync. Direct file edits bypass CloudKit entirely.

### .duedb schema (reminders array `re`)

| Key | Meaning |
|---|---|
| `n` | title |
| `d` | due date (Unix timestamp, HKT) |
| `b` | created timestamp |
| `m` | modified timestamp |
| `si` | snooze interval (seconds; 300 = 5 min) |
| `u` | UUID (base64, **no padding** — `rstrip("=")`) |
| `rf` | recurrence unit (`d`=daily, `w`=weekly, `m`=monthly, `y`=yearly) |
| `rd` | next recurrence timestamp (same as `d` on creation) |

Deleted items go into `dl` dict (UUID → deletion timestamp). Timers live in `tr` array with `c` = countdown seconds.

**UUID gotcha:** Due requires base64 UUIDs without `=` padding. Padding causes Due to crash on launch. Always use `base64.b64encode(...).rstrip("=")`.

## Error Handling

- **Due not installed**: Install from Mac App Store, sign into iCloud in Due first.
- **moneo edits not appearing**: Due may have overwritten the file — try `moneo ls` to confirm, re-apply if needed.
- **Due crashes after moneo write**: likely UUID padding issue — check `u` field has no `=`.
- **Reminder in the past**: moneo will add it — warn user it'll show as overdue immediately.

## Notes

- Always use HKT for times. moneo handles timezone internally.
- `moneo ls` shows ⚠ for overdue reminders.
- **moneo writes are Mac-only** — CloudKit is bypassed. For important recurring reminders, open in Due on Mac and hit Save once → CloudKit syncs to iPhone.
- No separate backup needed — recovery is just re-adding via moneo (2 min).
