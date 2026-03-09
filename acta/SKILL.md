---
name: acta
description: "Guided inbox triage session — review Gmail inbox together with Terry, prioritise actionable items, action each one, and archive noise. Use when Terry says 'review inbox', 'check emails', 'email review', or 'acta'."
user_invocable: true
---

# Acta — Email Review Session

A collaborative inbox triage. Claude pulls the inbox and all unread briefs, reads everything, and works through items with Terry one by one.

## Step 1 — Load the inbox and briefs

Run in parallel:
```bash
cora brief                                      # list all briefs — check for unread ones
gog gmail search "in:inbox" --limit 30          # full inbox list
gog gmail search "label:Cora/Action" --limit 20 # Cora-flagged actions outside inbox
```

**`Cora/Action` emails must be triaged** even though they're not in inbox — Cora explicitly flagged them as requiring action but strips the INBOX label. Treat them identically to inbox items.

Then read **all unread briefs** before triaging:
```bash
cora brief show <id>    # for each unread brief
```

If `cora brief show` errors, note it but continue with the inbox. If multiple unread briefs, read newest first — older ones may be superseded.

## Step 2 — Triage and present

Categorise every email into one of three buckets:

| Bucket | Criteria | Action |
|---|---|---|
| **Action required** | Needs a reply, decision, or follow-up | Present with context |
| **Monitor / waiting** | Ball is in someone else's court | Note and archive if clean |
| **Archive now** | Transactional, automated, or already handled | Archive without presenting |

**Archive now without asking:** OTPs, login notifications, password resets, automated "pending request" emails that have been superseded, booking confirmations already actioned.

**Cora Briefs emails — read before archiving.** Each brief email in the inbox represents unread digest content. Read the brief via `cora brief show <id>` first, extract any action items, then archive the email. Never batch-archive briefs without reading them.

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

After working through all action items, batch-archive the identified noise using `gog` — **not** `cora email archive` (Cora updates its own DB but does not reliably remove the Gmail INBOX label):
```bash
gog gmail thread modify <id1> --remove INBOX
gog gmail thread modify <id2> --remove INBOX
# ...
```

Verify with `gog gmail search "in:inbox" --limit 20` at the end — if anything remains, remove INBOX label directly.

Confirm count: "Archived X emails. Inbox zero."

**Note:** Gmail's unread badge in "All Mail" will still show a count — Cora intentionally never marks emails as read (the brief is the reading interface, not Gmail). Inbox zero is the goal; All Mail unread count is expected noise.

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
