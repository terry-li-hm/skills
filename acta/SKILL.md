---
name: acta
description: "Guided inbox triage session — review Gmail inbox together with Terry, prioritise actionable items, action each one, and archive noise. Use when Terry says 'review inbox', 'check emails', 'email review', or 'acta'."
user_invocable: true
---

# Relego — Email Review Session

A collaborative inbox triage. Claude pulls the inbox, reads each email, and works through them with Terry one by one.

## Step 1 — Load the inbox

Run in parallel:
```bash
cora brief show          # digest since last review
gog gmail search "in:inbox" --limit 30   # full inbox list
```

If the brief errored or is stale (>6h), note it but continue with the glimpse.

## Step 2 — Triage and present

Categorise every email into one of three buckets:

| Bucket | Criteria | Action |
|---|---|---|
| **Action required** | Needs a reply, decision, or follow-up | Present with context |
| **Monitor / waiting** | Ball is in someone else's court | Note and archive if clean |
| **Archive now** | Transactional, automated, or already handled | Archive without presenting |

**Archive now without asking:** Cora Briefs emails, OTPs, login notifications, password resets, booking confirmations already actioned, automated "pending request" emails that have been superseded.

Present the action-required list first. For each item, include:
- Who it's from and subject
- What's needed (reply / decision / read)
- Any relevant context from vault (e.g. open items in NOW.md that match)

## Step 3 — Work through each item together

For each action-required email:
1. `cora email show <id>` or `gog gmail thread show <id>` for full thread
2. Summarise the situation in 2–3 sentences
3. Recommend an action (reply, archive, research, calendar, vault update)
4. Wait for Terry's call before acting
5. Execute: draft reply / archive / update vault / update calendar as agreed
6. Archive the email once resolved unless Terry says keep it

## Step 4 — Archive the noise

After working through all action items, batch-archive the identified noise:
```bash
cora email archive <id1> && cora email archive <id2> ...
```

Confirm count: "Archived X emails."

## Step 5 — Sync NOW.md

After the session:
- Update any `[open]` items in NOW.md that were resolved
- Add any new open items that surfaced
- Note any emails still pending a reply (waiting on others)

## Workflow conventions

- **Inbox = action queue.** Archive = done. Don't leave resolved emails in inbox.
- **Thread view first.** Before actioning, always check if there are newer messages in the thread (`gog gmail thread show`).
- **Silent miss check.** For any expected email that isn't in the inbox: `gog gmail search "from:<domain>"` — catches emails Cora missed entirely.
- **Domain filters.** If a critical domain keeps missing the inbox, add a filter: `gog gmail filters create --from "<domain>" --never-spam --important`. Currently set: `aia.com`, `mtr.com.hk`, `capco.com`.

## Fail states

- `cora brief show` errors → continue with gog inbox; note brief is unavailable
- Email not in inbox but expected → search gog directly before concluding missing
- Can't draft reply in session → add to NOW.md as `[open]` and archive the email

## Calls
- `nuntius` — Cora CLI reference
