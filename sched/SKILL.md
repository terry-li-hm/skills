---
name: sched
description: Schedule an event in Google Calendar and set a Due reminder in one step. "schedule", "add to calendar with reminder", "book X with reminder".
user_invocable: true
---

# /sched — Schedule + Remind

Create a Google Calendar event and set a Due reminder in one step.

## Trigger

- User says "schedule", "book", "add to calendar with reminder"
- User wants both a calendar event and a Due reminder at once

## Usage

Collect from the user (ask only what's missing):
- **Title** — event name
- **Date** — e.g. "tomorrow", "March 10"
- **Start time** — HH:MM (HKT)
- **End time** — HH:MM (HKT), or ask for duration
- **Reminder time** — explicit HH:MM, or `--remind-before Xm` to back-calculate

## Steps

### 1. Create Google Calendar event

```bash
gog calendar create terry.li.hm@gmail.com \
  --summary "Event title" \
  --from "2026-03-05T12:15:00+08:00" \
  --to "2026-03-05T13:45:00+08:00"
```

Default calendar: `terry.li.hm@gmail.com`
Use `family16675940229854502575@group.calendar.google.com` for family events.

Times must be RFC3339 with `+08:00` offset (HKT).

### 2. Set Due reminder via moneo

```bash
moneo add "Event title" --date 2026-03-05 --at 11:45 --sync
```

**Reminder time logic:**
- `--remind-at HH:MM` → use directly
- `--remind-before Xm` → subtract X minutes from event start
- Default if neither given: **30 minutes before**

If moneo outputs "Due editor open", click Save automatically:

```bash
peekaboo click "Save" --app Due --wait-for 3000
```

### 3. Confirm to user

Report both:
- Calendar event created (title, date, time)
- Due reminder set (time)

## Example

> "Schedule lunch with Simon on March 10 at 12:30, ends 2pm, remind me at noon"

```bash
gog calendar create terry.li.hm@gmail.com \
  --summary "Lunch with Simon" \
  --from "2026-03-10T12:30:00+08:00" \
  --to "2026-03-10T14:00:00+08:00"

moneo add "Lunch with Simon" --date 2026-03-10 --at 12:00 --sync
# If editor opens, click Save:
peekaboo click "Save" --app Due --wait-for 3000
```

## Gotchas

- `gog calendar create` requires RFC3339 with timezone offset — never bare `HH:MM`
- `moneo add --sync` usually handles CloudKit sync via AppleScript without needing a Save click; peekaboo is a fallback for when the editor opens
- `moneo rm` does not accept `--sync` — just `moneo rm <number>`
- Always confirm the reminder time with the user if it wasn't explicitly stated
