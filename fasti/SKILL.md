---
name: fasti
description: Google Calendar CLI wrapper — list, move, delete events via fasti instead of raw gog commands
triggers: ["fasti", "calendar list", "reschedule event", "move calendar event", "delete calendar event"]
---
# fasti — Google Calendar CLI

Thin Rust wrapper over `gog` for token-efficient calendar ops. Hardcoded to primary calendar (`terry.li.hm@gmail.com`). Use instead of raw `gog calendar` commands.

## Commands

```bash
# List events (defaults to today)
fasti list
fasti list tomorrow
fasti list 2026-03-10

# Move an event (preserves duration)
fasti move <event-id> today 14:00
fasti move <event-id> tomorrow 09:30
fasti move <event-id> 2026-03-10 11:00

# Delete an event (no confirmation)
fasti delete <event-id>
```

## Event IDs

`fasti list` shows 8-char prefix IDs. `move` and `delete` accept either the prefix or the full ID.

## Gotchas

- Gemini tested against live calendar during build — it will actually execute moves/deletes. Don't use as a dry-run tool.
- `fasti list` shows today by default; no flag needed.
- Duration is always preserved on `move` — it queries the event first, computes delta, applies to new start.
- Raw `gog` flags: `--from`/`--to` (not `--start`/`--end`), calendar ID required as positional arg before event ID.

## When to use

Prefer `fasti` over raw `gog calendar` for all list/move/delete ops — saves token roundtrips from flag/ID discovery.

## Source

`~/code/fasti/src/main.rs`
