---
name: sched
description: Schedule an event — adds to both Due (nag reminder) and Google Calendar by default. "schedule", "remind me about", "book X with reminder".
user_invocable: true
---

# /sched — Schedule + Remind

Schedule an event by adding to **both Due and Google Calendar** by default. Due = nag reminder so you don't forget. Google Calendar = source of truth for your schedule.

**Exception — Due only (no Google Calendar):** tasks, nudges, habits, follow-up reminders that aren't time-blocked appointments (e.g. "nudge Gavin if no reply", "dim lights tonight").

## Trigger

- User says "schedule", "book", "remind me about X at Y"
- User wants a Due reminder for an upcoming event

## Usage

Collect from the user (ask only what's missing):
- **Title** — event name
- **Date + time** — e.g. "tomorrow 10am"
- **End time** — default to 1h after start if not given
- **Location** — optional, include if known

## Steps

### 1. Set Due reminder via moneo

Default reminder time: **30 minutes before event start**.

```bash
moneo add "Event title" --date 2026-03-10 --at 09:30 --sync
```

**Duplicate guard:** `moneo add` rejects same title on same day — edit instead of re-adding.

### 2. Add to Google Calendar

```bash
gog calendar add primary \
  --summary "Event title" \
  --from "2026-03-10T10:00:00+08:00" \
  --to "2026-03-10T11:00:00+08:00" \
  --location "Optional location" \
  --description "Optional notes"
```

Default calendar: `primary` (terry.li.hm@gmail.com).
Use `family16675940229854502575@group.calendar.google.com` for family events.
Times must be RFC3339 with `+08:00` offset (HKT).
**Never add `--attendees`** — triggers email notifications to recipients.

### 3. Confirm to user

Report: reminder time (Due) + calendar event created.

## Example

> "Schedule AIA call tomorrow 10am, Tommy Lau +852 3727 6441"

```bash
moneo add "AIA call - Tommy Lau" --date 2026-03-06 --at 09:30 --sync
gog calendar add primary --summary "AIA call - Tommy Lau" --from "2026-03-06T10:00:00+08:00" --to "2026-03-06T11:00:00+08:00" --description "Tommy Lau +852 3727 6441"
```

## Gotchas

- `moneo add --sync` opens Due's editor via AppleScript, then uses **peekaboo** to auto-click Save — works screen-free (display-sleep safe)
- If moneo prints "Due editor open — please click Save manually", peekaboo lacks permissions — grant **Accessibility + Screen Recording** to `/opt/homebrew/bin/peekaboo` in System Settings → Privacy & Security. `peekaboo permissions` may show stale results; test with an actual `--sync` to confirm.
- `moneo rm` does not sync deletions to iPhone — if added with `--sync`, delete in Due on iPhone directly
- Always confirm the reminder time with the user if it wasn't explicitly stated
