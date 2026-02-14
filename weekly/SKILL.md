---
name: weekly
description: Weekly synthesis and review. Use when user says "weekly", "weekly review", "week in review", or on Fridays.
user_invocable: true
---

# Weekly Synthesis

Create a weekly synthesis of work, thinking, and progress.

## Triggers

- "weekly", "weekly review", "week in review"
- Friday afternoon — end-of-week reflection before weekend (weekends reserved for Theo)

## Workflow

1. **Determine the week range** (Mon-Sun, HKT)

2. **Gather the week's data**:
   - Read daily notes for the week: `~/notes/YYYY-MM-DD.md`
   - Read `~/notes/Capco Transition.md` for transition status
   - Read `~/notes/TODO.md` for completed/outstanding items
   - Scan `~/notes/Learnings Inbox.md` for entries this week
   - Check git log for skills/vault commits: `cd ~/skills && git log --oneline --since="7 days ago"`
   - Check `~/logs/` for cron output logs

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

### Inbox Triage (do every week)

Review `~/notes/Learnings Inbox.md` and for each entry:
- **Promote** → Move to a proper note (e.g., topic note, `~/docs/solutions/`, MEMORY.md) if it has lasting value
- **Keep** → Leave in inbox if too fresh to judge (< 1 week old)
- **Delete** → Remove if outdated, wrong, or already captured elsewhere

Target: inbox stays under 15 active entries. If it's growing, triage harder.

## Health & Recovery

Run `oura trend` for the week's scores, then correlate with daily notes:

```bash
oura trend --days 7
```

Analyse:
- **Sleep trend** — improving, declining, or stable? Flag any score <70
- **HRV pattern** — leading indicator of stress. Drops below 50 warrant attention
- **Bedtime drift** — are bedtimes creeping past 22:30? (Theo school drop-off = fixed wake-up, bedtime is the only lever)
- **Correlation with activity** — cross-reference low-score nights with that day's daily note. Look for: resignation conversations, late-night coding sessions, career rumination, insomnia entries
- **Stress data** — note any days with elevated stress_high (>1h)

Include in weekly note:

```markdown
## Health

| Day | Sleep | Readiness | HRV | Bedtime | Note |
|-----|-------|-----------|-----|---------|------|
| Mon | 86 | 81 | 69 | 23:40 | — |
| ... | | | | | |

**Pattern:** [1-2 sentence summary of the week's health trend and any correlations found]
**Action:** [Anything to adjust, or "Steady"]
```

Keep it brief — the value is pattern recognition over weeks, not daily obsessing.

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

## AI Tooling Health (weekly)

Run these checks every Friday and include results in the weekly note under `## Tooling Health`:

1. **CLAUDE.md & MEMORY.md content review** — Check line counts (`wc -l`). Flag if CLAUDE.md >300 or MEMORY.md >150. Then do a staleness scan:
   - Read both files and flag sections referencing past dates, completed transitions, retired tools, or situations that no longer apply
   - Check "Current Situation", "Current Projects", and any date-anchored content in CLAUDE.md
   - Check MEMORY.md for entries about tools/projects no longer in use
   - Present a concrete list: "Remove X", "Update Y", "Keep Z" — don't just flag, recommend actions
   - During transition periods (job changes, major project shifts), this is the most valuable check
2. **Skills inventory** — `ls ~/skills/*/SKILL.md | wc -l` for total count. `cd ~/skills && git log --oneline --since="7 days ago"` for changes. Flag skills not invoked in 30+ days (check `~/.claude/history.jsonl` for recent `/skill` usage).
3. **MCP servers** — `claude mcp list` to verify health. Flag any disconnected, orphaned from experiments, or version-drifted servers.
4. **Token consumption** — Run `cu` alias for Max20 usage stats. Note weekly trend and any spikes.
5. **Oghma health** — `oghma_stats` for DB size, memory count, extraction backlog.
6. **Cron scripts** — Check `~/scripts/crons/` and `~/logs/cron-*.log` for failures or stale output.
7. **QMD index** — `qmd status` for collection health and staleness.

Include a summary table in the weekly note:

```markdown
## Tooling Health

| Metric | Value | Status |
|--------|-------|--------|
| CLAUDE.md lines | X | ✅/⚠️ |
| MEMORY.md lines | X | ✅/⚠️ |
| Skills (total) | X | — |
| Skills (changed this week) | X | — |
| MCP servers | X connected | ✅/⚠️ |
| Max20 usage | X% weekly | ✅/⚠️ |
| Oghma memories | X | — |
| Cron scripts (healthy/total) | X/Y | — |
```

## Friday Reset Checklist

Run this alongside the synthesis every Friday:

1. **TODO.md prune** — Clear completed items, flag anything untouched for 2+ weeks (stale → delete or reschedule)
2. **Transition status** — Update [[Capco Transition]] (PILON, onboarding, handover)
3. **Networking status** — Who's in motion, who needs follow-up? (BOCHK bridge, Capco contacts)
4. **Priorities for the week** — Top 2-3 actions
7. **AI landscape** — Run `/ai-review` for weekly synthesis (client talking points). `/ai-news` feeds it raw material.
8. **First Friday only** — Monthly maintenance (add `/ai-review` deep monthly review):
   - `/skill-review` — Audit skills for staleness, drift, gaps
   - **Vault hygiene** (inline checklist):
     a. Learnings Inbox — deep consolidation pass (weekly triage keeps it manageable; monthly pass catches stragglers)
     b. Decay report — `uv run ~/scripts/vault-decay-report.py` for orphans/cold notes
     c. Daily note archival — archive notes >60 days old to `~/notes/.archive/dailies/`
     d. Broken links — verify `[[wikilinks]]` in CLAUDE.md still resolve
     e. QMD reindex — `qmd update && qmd status` (run `qmd embed` in background if stale)

[[Capco Transition]] is source of truth for exit/onboarding; [[Job Hunting]] is the archive.

## Notes

- Create `~/notes/Weekly/` directory if it doesn't exist
- Link back to daily notes and relevant vault notes
- The synthesis captures the broader picture; the reset checklist is action-oriented
- The energy audit is the most valuable section long-term — it reveals what work is sustainable
