---
name: interphase
description: Use when heading home from work — single evening routine covering full inbox triage, messages, work summary, brain dump, and tomorrow prep. "leaving office", "on the bus", "going home", "end of day", "check emails", "review inbox", "interphase"
user_invocable: true
---

# Interphase — Evening Routine

The quiet phase between divisions. Everything between "leaving the office" and "walking through the door." Process inputs, consolidate, prep for the next cycle.

## Design

Phone-friendly (Blink/tmux). Target: one bus ride. No deep reflection — capture facts, clear queues, prep tomorrow.

## Context Load (parallel, before starting)

- `[[Email Threads Tracker]]` (`~/notes/Email Threads Tracker.md`)
- `~/reticulum/claude/memory/prospective.md` — check for `WHEN: email triage` or `WHEN: interphase` entries
- Today's daily note

## Steps

### 0. Gather

```bash
interphase-gather
```

All deterministic gathering runs here (inbox, WhatsApp, calendar, TODO, NOW, budget, reminders, email threads, prospective memory). Review output, then proceed.

### 1. Inbox Triage

Invoke the **sorting** skill. It handles the full triage: categorise, drill, filter, archive, update Email Threads Tracker.

### 2. Messages

- WhatsApp via `keryx read_messages` — draft responses, never send
- LinkedIn notifications — replies, messages from network
- If a person has history, `amicus lookup <name>` for context

### 3. Brain Dump

Ask Terry: **"Anything still rattling around?"**

Capture to today's daily note. One or two exchanges max. Get it out of his head, not processed.

### 4. What Shipped Today

- Read today's daily note for `/cytokinesis` session logs
- If empty/missing, delegate to subagent (haiku): `python3 ~/scripts/chat_history.py --full`
- Write a 2-3 line summary to the daily note

### 5. Tomorrow Prep

Run in parallel: `fasti` (calendar), `moneo ls` (due items), Praxis.md (items with tomorrow's date or overdue), Schedule.md (recurring commitments).

If meetings tomorrow: one-line prep note for each.

**Thursday only:** Weekly token reset ~11am HKT tomorrow. Run `usus --json` — flag significant headroom.

### 6. Daily Note Close

Header: `# YYYY-MM-DD — Day — themes, comma, separated`

Append:
```markdown
## Interphase

**Shipped:** [2-3 line summary]
**Tomorrow:** [key items — meetings, deadlines, prep needed]
**Open threads:** [anything waiting on others]
**Mood:** [one word or phrase]
```

### 7. NOW.md Sync

Update resolved items, add new open items, mark blocked/waiting.

Then: **"You're done. Evening is yours."**

## Fail States

- `cora brief show` crashes → `porta run --domain cora.computer` fallback
- `gog gmail` fails → note "inbox skipped", continue
- Daily note empty + history scan fails → continue with current session context, label "partial"
- Any step fails → skip it, never block the whole routine

## Boundaries

- Draft only — never send (WhatsApp, email, LinkedIn)
- No deep reflection or extended conversation
- Only update: daily note, Email Threads Tracker, NOW.md
- Nothing cognitive after walking through the door
