---
name: sorting
description: Triage email inbox — categorise, drill, filter, archive, update tracker. Golgi sorting of incoming cargo to the right compartment.
user_invocable: false
model: sonnet
context: fork
---

# Sorting — Email Triage

Golgi protein sorting: incoming cargo gets classified and routed to the right compartment. That's email triage.

## Gather

Two queries in parallel:

```bash
gog gmail search "is:unread in:inbox" --plain
gog gmail search "newer_than:1d -in:inbox -from:briefs@cora.computer" --plain
```

First is the working set (what Cora left). Second is the safety net (what Cora archived — check for misclassifications).

Also read: `~/notes/Email Threads Tracker.md` for active thread context.

## Categorise

Present each email with a verdict:

| Bucket | Action |
|--------|--------|
| **Action required** | Drill into thread (`gog gmail thread get <id> --full`), present with context, draft reply if needed |
| **Borderline** | One-line mention, ask Terry |
| **Monitor** | Note in Email Threads Tracker, archive |
| **Archive now** | Silent archive |

Work through emails one at a time or in small batches — Terry decides the pace.

## Drill

When drilling into a thread:
- `gog gmail thread get <threadId> --full` for full content
- Summarise what matters, flag action items
- Draft replies but NEVER send

## Filter

When a pattern emerges (recurring noise from same sender/subject):
1. `gog gmail labels create "<Category>/<Name>"` if label doesn't exist
2. `gog gmail settings filters create --from="<sender>" --subject="<pattern>" --archive --mark-read --add-label="<label>"` with `--dry-run` first
3. Apply after Terry confirms

## Close

After triage:
1. Batch mark-read: `gog gmail mark-read <id1> <id2> ...`
2. Batch archive: `gog gmail archive <id1> <id2> ...`
3. Update `~/notes/Email Threads Tracker.md` — add new threads, update status, move resolved

## Gotchas

- `gog gmail thread get` not `gog gmail get` for full thread view
- Gmail negation queries (`-in:inbox`) must be a single string argument, not separate tokens
- `gog gmail read` truncates — always use `--full`
- Cora actively archives emails, not just summarises — safety-net query is essential
- Draft only — never send anything

## Boundaries

- No deep research or follow-up work — triage only
- Flag action items for Terry, don't execute them
- If >20 unread, offer to batch by category rather than one-by-one
