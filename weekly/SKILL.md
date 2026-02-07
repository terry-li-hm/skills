---
name: weekly
description: Weekly synthesis and review. Use when user says "weekly", "weekly review", "week in review", or on Sundays.
user_invocable: true
---

# Weekly Synthesis

Create a weekly synthesis of work, thinking, and progress.

## Triggers

- "weekly", "weekly review", "week in review"
- Sunday weekly reset (complements the existing Sunday protocol in vault CLAUDE.md)

## Workflow

1. **Determine the week range** (Mon-Sun, HKT)

2. **Gather the week's data**:
   - Read daily notes for the week: `~/notes/YYYY-MM-DD.md`
   - Read `~/notes/Active Pipeline.md` for pipeline changes
   - Read `~/notes/TODO.md` for completed/outstanding items
   - Scan `~/notes/Learnings Inbox.md` for entries this week
   - Check git log for skills/vault commits: `cd ~/skills && git log --oneline --since="7 days ago"`
   - Check `~/notes/memory/` for OpenClaw daily logs

3. **Synthesize into themes** — don't just list events, find patterns:
   - What topics kept coming up?
   - What moved forward vs what stalled?
   - Where did energy go?

4. **Create weekly note** at `~/notes/Weekly/YYYY-Www.md` (e.g., `2026-W06.md`):

```markdown
# Week of YYYY-MM-DD

## At a Glance

- Days active: X/7
- Daily notes: [list]
- Pipeline changes: [summary]

## Key Themes

### [Theme 1]
- Where it appeared: [contexts]
- Progress: [what moved]
- Next: [what's next]

### [Theme 2]
...

## Progress

### Job Hunt
- Applications: [count]
- Interviews: [count]
- Pipeline changes: [moved forward / stalled / new leads]

### Skills & Tools
- New/updated skills: [list]
- Tool changes: [any]

### Projects
- [Project]: [status change]

## Learnings Captured

- [Summary of Learnings Inbox entries from this week]

## Energy Audit

- What gave energy: [activities, wins]
- What drained: [friction, blockers]
- Adjust next week: [what to do differently]

## Open Loops

- [ ] [Unresolved items carrying into next week]

## Next Week's Focus

1. [Primary]
2. [Secondary]
3. [Explore]
```

5. **Keep it honest** — this is for pattern recognition, not performance reporting. Short weeks with little output are fine to note as such.

## Sunday Reset Checklist

Run this alongside the synthesis every Sunday:

1. **Pipeline status** — Update [[Active Pipeline]] (offer, interviewing, warm leads, dead)
2. **Networking status** — Who's in motion, who needs follow-up?
3. **Follow-ups due** — Applications or contacts to nudge this week?
4. **Applications to send** — Any "noted but not applied" worth pursuing?
5. **Priorities for the week** — Top 2-3 actions
6. **AI news** — Run `/ai-news` to stay current (interview talking points)
7. **First Sunday only** — Monthly maintenance:
   - `/skill-review` — Audit skills for staleness, drift, gaps
   - **Vault hygiene** (inline checklist):
     a. Learnings Inbox — consolidate entries into topic notes, target <15 active
     b. Decay report — `uv run ~/scripts/vault-decay-report.py` for orphans/cold notes
     c. Daily note archival — archive notes >60 days old to `~/notes/.archive/dailies/`
     d. Broken links — verify `[[wikilinks]]` in CLAUDE.md still resolve
     e. QMD reindex — `qmd update && qmd status` (run `qmd embed` in background if stale)

[[Active Pipeline]] is source of truth for live pipeline; [[Job Hunting]] is the archive.

## Notes

- Create `~/notes/Weekly/` directory if it doesn't exist
- Link back to daily notes and relevant vault notes
- The synthesis captures the broader picture; the reset checklist is action-oriented
- The energy audit is the most valuable section long-term — it reveals what work is sustainable
