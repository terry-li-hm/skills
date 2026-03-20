---
name: commute
description: Use when heading home from work — single evening routine covering full inbox triage, messages, work summary, brain dump, and tomorrow prep. "leaving office", "on the bus", "going home", "end of day", "check emails", "review inbox"
user_invocable: true
---

# Commute — Evening Routine

The one daily routine. Everything between "leaving the office" and "walking through the door." After this, nothing work-related until tomorrow.

## Triggers

- commute
- heading home
- leaving office
- on the bus
- going home
- end of day
- eod
- done for the day
- end of work
- eow
- check emails
- review inbox

## Design

Phone-friendly (Blink/tmux). Target: one bus ride. No deep reflection — capture facts, clear queues, prep tomorrow. The commute is the trigger, not a reminder.

## Steps

### 0. Context Gather

```bash
commute-gather
```

This runs all deterministic gathering in parallel (inbox, WhatsApp, calendar, TODO, NOW, budget, reminders, email threads, prospective memory). Review the output, then proceed through steps using the gathered context.

### 1. Inbox triage (full)

Use the email/WhatsApp sections from `commute-gather` output. If details are insufficient, drill in:
```bash
cora brief                                              # list all briefs — check for unread
gog gmail search "in:inbox" --limit 30                  # full inbox
gog gmail search "label:Cora/Action" --limit 20         # Cora-flagged actions
gog gmail search "NOT in:inbox newer_than:7d" --limit 50  # silent miss sweep
```

Read all unread briefs via `cora brief show <id>` before triaging.

Categorise every email:

| Bucket | Action |
|--------|--------|
| **Action required** | Present with context, draft replies |
| **Borderline** | One-line mention before archiving |
| **Monitor** | Note and archive |
| **Archive now** | Archive without presenting |

Work through action items with Terry. Draft replies where needed. Archive noise:
- Inbox emails → `cora email archive <id>`, verify with `gog gmail search "in:inbox"`
- Silent miss / Cora/Action → `gog gmail thread modify <id> --remove INBOX`
- Mark processed briefs as read: `cora brief read <id>`

If `cora brief show` crashes, fallback: `porta run --domain cora.computer --selector body "https://cora.computer/14910/briefs?date=YYYY-MM-DD&time=morning"`

After triage, update `[[Email Threads Tracker]]` — add new threads, update status, move resolved.

### 2. Messages

- `keryx read_messages` — WhatsApp, anything needing response
- LinkedIn notifications — replies, messages from network
- Draft responses where needed (never send WhatsApp directly)
- If a person has history, `amicus lookup <name>` for context

### 3. Brain dump

Ask Terry: **"Anything still rattling around?"**

Capture to today's daily note. One or two exchanges max. The goal is to get it out of his head, not to process it.

### 4. What shipped today

Quick scan:
- Read today's daily note (`~/notes/Daily/YYYY-MM-DD.md`) for session logs from `/legatum`
- If empty/missing, delegate history scan to a subagent (haiku): `python ~/scripts/chat_history.py --full`
- Write a 2-3 line summary to the daily note

### 5. Tomorrow prep

Run in parallel:
- Calendar: check tomorrow's events via `fasti`
- Due: `moneo ls` — surface tomorrow's items
- TODO.md: items with `due:` or `when:` = tomorrow, plus overdue items
- Schedule.md: recurring commitments for tomorrow's day-of-week

If meetings tomorrow: one-line prep note for each.

**Thursday only:** Weekly token reset tomorrow ~11am HKT. Run `cu` — if significant headroom remains, flag it.

### 6. Daily note close

Update the daily note header with thematic tagline:
```markdown
# YYYY-MM-DD — Day — themes, comma, separated
```

Append:
```markdown
## Commute Close

**Shipped:** [2-3 line summary of the work day]
**Tomorrow:** [key items — meetings, deadlines, prep needed]
**Open threads:** [anything waiting on others]
**Mood:** [one word or phrase — how the day felt]
```

### 7. NOW.md sync

- Update any items resolved today
- Add any new open items that surfaced
- Mark anything that's now blocked or waiting

Then: **"You're done. Evening is yours."**

## Fail states

- `cora brief show` crashes → porta fallback (see Step 1)
- `gog gmail` fails (keychain locked) → note "inbox skipped" and continue
- Daily note empty + history scan fails → continue with current session context, label "partial"
- Any step fails → skip it, continue with the rest. Never block the whole routine on one failure.

## Boundaries

- Do NOT send anything — draft only (WhatsApp, email, LinkedIn)
- Do NOT do deep reflection or extended conversation — capture facts, move on
- Do NOT create new vault notes — only update daily note, Email Threads Tracker, NOW.md
- Nothing cognitive after walking through the door

## Context loading

At start, read in parallel:
- `[[Email Threads Tracker]]` (`~/notes/Email Threads Tracker.md`)
- `memory/prospective.md` — check for `WHEN: email triage` or `WHEN: commute` entries
- Today's daily note

## See also

- `/auspex` — optional morning brief (weather, calendar)
- `/statio` — start-of-work at the desk (priorities, gates)
- `/kairos` — ad-hoc "what now?"
