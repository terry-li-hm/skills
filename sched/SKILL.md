---
name: sched
description: Set a Due reminder for an event. "schedule", "remind me about", "book X with reminder". Use --invite only when user wants to send a calendar invite to others.
user_invocable: true
---

# /sched — Schedule + Remind (Due-only)

Set a Due reminder for an event. Google Calendar is opt-in only (see below).

## Trigger

- User says "schedule", "book", "remind me about X at Y"
- User wants a Due reminder for an upcoming event

## Usage

Collect from the user (ask only what's missing):
- **Title** — event name
- **Date** — e.g. "tomorrow", "March 10"
- **Reminder time** — explicit HH:MM, or `--remind-before Xm` to back-calculate from start time

## Steps

### 1. Set Due reminder via moneo

```bash
moneo add "Event title" --date 2026-03-10 --at 11:30 --sync
```

**Reminder time logic:**
- `--remind-at HH:MM` → use directly
- `--remind-before Xm` → subtract X minutes from event start
- Default if neither given: **30 minutes before event start**

**Duplicate guard:** `moneo add` rejects same title on same day — edit instead of re-adding.

### 2. Confirm to user

Report: reminder title + time set.

## Calendar (opt-in only)

Only when user explicitly asks to "send an invite" or "put it on the calendar":

```bash
gog calendar create terry.li.hm@gmail.com \
  --summary "Event title" \
  --from "2026-03-10T12:00:00+08:00" \
  --to "2026-03-10T14:00:00+08:00"
```

Default calendar: `terry.li.hm@gmail.com`
Use `family16675940229854502575@group.calendar.google.com` for family events.
Times must be RFC3339 with `+08:00` offset (HKT).

## Example

> "Remind me about lunch with Simon on March 10 at 12:30, ends 2pm"

```bash
moneo add "Lunch with Simon" --date 2026-03-10 --at 12:00 --sync
```

Confirm: "Reminder set for March 10 at 12:00."

## Gotchas

- `moneo add --sync` opens Due's editor via URL scheme + AppleScript-clicks Save — works screen-free (display-sleep safe)
- If moneo prints "Due editor open — please click Save manually", AppleScript failed; peekaboo fallback: `peekaboo click "Save" --app Due --wait-for 3000`
- `moneo rm` does not sync deletions to iPhone — if added with `--sync`, delete in Due on iPhone directly
- Always confirm the reminder time with the user if it wasn't explicitly stated
