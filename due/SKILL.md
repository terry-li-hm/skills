---
name: due
description: Add reminders and timers to the Due app via URL scheme. "due remind me", "add to Due", "due in X minutes".
user_invocable: true
---

# Due App

Create reminders in the Due iOS/macOS app via its `due://` URL scheme using `open` from the terminal.

## Trigger

Use when:
- User says "due remind me", "add to Due", "remind me in X"
- User wants to set a one-off or recurring reminder in Due
- User says "due search"

## URL Scheme

Base: `due://x-callback-url/add` or `due:///search`

### Timing parameters (pick one)

| Param | Type | Meaning |
|---|---|---|
| `duedate` | Unix timestamp | Absolute time |
| `secslater` | double | Seconds from now |
| `minslater` | double | Minutes from now |
| `hourslater` | double | Hours from now |

### Other add parameters

| Param | Type | Notes |
|---|---|---|
| `title` | string (URL-encoded) | Reminder text |
| `timezone` | string | e.g. `Asia/Hong_Kong` |
| `autosnooze` | int | 1, 5, 10, 15, 30, or 60 (minutes) |

### Recurrence parameters

| Param | Value | Meaning |
|---|---|---|
| `recurunit` | 16 | Daily |
| `recurunit` | 256 | Weekly |
| `recurunit` | 8 | Monthly |
| `recurunit` | 4 | Yearly |
| `recurfreq` | 1–30 | Multiplier (every N units) |
| `recurfromdate` | Unix timestamp | Start date |
| `recurbyday` | comma-separated int | Days of week (1–7) or month positions |

### Search parameters

| Param | Value |
|---|---|
| `query` | URL-encoded search string |
| `section` | `Reminders`, `Timers`, or `Logbook` |

## Workflow

1. **Parse the request** — extract title, timing (relative or absolute), recurrence if any.
2. **Compute Unix timestamp** if absolute time needed:
   ```bash
   python3 -c "from datetime import datetime, timezone; import calendar; dt = datetime(2026,3,5,9,0, tzinfo=timezone.utc); print(int(dt.timestamp()))"
   ```
   For HKT (UTC+8), subtract 8 hours from local time to get UTC, or use `Asia/Hong_Kong` timezone and set `timezone=Asia%2FHong_Kong`.
3. **URL-encode the title**: spaces → `%20`, `#` → `%23`, `&` → `%26`.
4. **Construct and open the URL**:
   ```bash
   open "due://x-callback-url/add?title=Call%20dentist&minslater=30&autosnooze=5"
   ```
5. **Confirm** to user: "Added to Due: [title] in [time]."

## Examples

**Relative — 30 minutes from now:**
```bash
open "due://x-callback-url/add?title=Call%20dentist&minslater=30"
```

**Absolute — tomorrow 9am HKT:**
```bash
# Compute: 2026-03-03 09:00 HKT = 2026-03-03 01:00 UTC = 1740963600
open "due://x-callback-url/add?title=Morning%20standup&duedate=1740963600&timezone=Asia%2FHong_Kong"
```

**Monthly recurring — pay rent, starting March 1:**
```bash
open "due://x-callback-url/add?title=Pay%20rent&recurunit=8&recurfreq=1&recurfromdate=1740787200"
```

**Search:**
```bash
open "due:///search?section=Reminders&query=dentist"
```

## Error Handling

- **Due not installed / URL doesn't open**: Inform user Due must be installed on macOS or the device must be reachable.
- **Time in the past**: Due will still accept it — warn the user.
- **Recurrence without `recurfromdate`**: Due defaults to today; usually fine.

## Limitations

- **URL scheme pre-fills but does not auto-submit.** Due always opens the add form for user confirmation — the user must click/tap **Create** to save the reminder. There is no way to bypass this.

## Notes

- On macOS, `open` fires the URL scheme immediately and Due opens.
- On iOS, there's no direct `open` from terminal — use Shortcuts automation or share the URL.
- HKT = UTC+8. Always set `timezone=Asia%2FHong_Kong` for absolute reminders to avoid DST-style shifts.
