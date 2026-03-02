---
name: due
description: Manage Due app reminders via moneo CLI. "due remind me", "add to Due", "remind me in X", "delete due reminder", "edit due reminder".
user_invocable: true
---

# Due App

Manage Due app reminders from the terminal using **moneo** (`~/bin/moneo`) — a CLI that edits the `.duedb` file directly, giving full read/add/edit/delete capability. Falls back to URL scheme for recurring reminders (not yet supported in moneo).

## Trigger

Use when:
- User says "due remind me", "add to Due", "remind me in X"
- User wants to list, edit, or delete Due reminders
- User says "due search"

## Primary: moneo CLI

### Commands

```bash
moneo ls                                    # list all reminders with index
moneo add "Call dentist" --in 30m           # relative time
moneo add "Standup" --at 09:30              # today at HH:MM
moneo add "Pay rent" --date 2026-04-01 --at 10:00  # specific date + time
moneo edit <index> --title "New title"      # rename
moneo edit <index> --at 16:00              # change time
moneo edit <index> --in 1h                 # push forward by 1h from now
moneo rm <index>                            # delete by index
```

### Time flags (mutually exclusive)

| Flag | Example | Meaning |
|---|---|---|
| `--in` | `--in 30m` | Relative: `s`, `m`, or `h` |
| `--at` | `--at 14:35` | Today at HH:MM (HKT) |
| `--date` + `--at` | `--date 2026-04-01 --at 09:00` | Specific date + time |
| `--date` only | `--date 2026-04-01` | That date at 09:00 |

### How it works

moneo reads `~/Library/Containers/com.phocusllp.duemac/Data/Library/Application Support/Due App/Due.duedb` (gzipped JSON), edits it, and writes back. If Due is running, it quits Due first via AppleScript, writes, then reopens. iCloud syncs changes to iPhone automatically.

### .duedb schema (reminders array `re`)

| Key | Meaning |
|---|---|
| `n` | title |
| `d` | due date (Unix timestamp, HKT) |
| `b` | created timestamp |
| `m` | modified timestamp |
| `si` | snooze interval (seconds; 300 = 5 min) |
| `u` | UUID (base64) |
| `rf` | recurrence unit (`w` = weekly, etc.) |
| `rd` | next recurrence timestamp |

Deleted items go into `dl` dict (UUID → deletion timestamp). Timers live in `tr` array with `c` = countdown seconds.

## Fallback: URL scheme (recurring reminders)

moneo doesn't yet support recurrence. Use URL scheme for those:

```bash
# Monthly recurring
open "due://x-callback-url/add?title=Pay%20rent&recurunit=8&recurfreq=1&recurfromdate=1740787200"
# Weekly
open "due://x-callback-url/add?title=Recycle&recurunit=256&recurbyday=3,6"
```

**Note:** URL scheme pre-fills but requires manual **Save** tap. Use AppleScript to auto-click:
```bash
sleep 1 && osascript -e 'tell application "System Events" to tell process "Due" to click button "Save" of window "Reminder Editor"'
```

### Recurrence parameters

| `recurunit` | Meaning |
|---|---|
| 16 | Daily |
| 256 | Weekly |
| 8 | Monthly |
| 4 | Yearly |

`recurfreq` = multiplier (1–30). `recurbyday` = comma-separated days (1–7 for weekly; 1–42 for monthly positions).

## Error Handling

- **Due not installed**: Install from Mac App Store, sign into iCloud in Due first.
- **moneo edits not appearing**: Due may have overwritten the file — try `moneo ls` to confirm, re-apply if needed.
- **AppleScript quit fails**: Use `pgrep -x Due` to check; fall back to `pkill Due`.
- **Reminder in the past**: moneo will add it — warn user it'll show as overdue immediately.

## Notes

- Always use HKT for times. moneo handles timezone internally.
- iCloud sync to iPhone usually takes a few seconds after Due reopens.
- `moneo ls` shows ⚠ for overdue reminders.
