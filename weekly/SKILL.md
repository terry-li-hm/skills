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
   - If date computation fails, default to "last 7 days" and note the fallback.

2. **Gather the week's data** (recursive — read distilled layers, not raw):
   - Read the **## Reflection**, **## Follow-ups**, and **## Mood** sections from each daily note `~/notes/YYYY-MM-DD.md` (not the full session logs — those are raw context, already distilled into the reflection)
   - Read this week's **AI Landscape weekly snapshot** from `~/notes/AI Landscape.md` (written by `/ai-review`). Reference it in the synthesis — don't re-derive AI themes from the raw AI News Log.
   - Read `~/notes/Capco Transition.md` for transition status
   - Read `~/notes/TODO.md` for completed/outstanding items
   - Check `~/docs/solutions/` and `MEMORY.md` for entries this week
   - Check git log for skills/vault commits: `cd ~/skills && git log --oneline --since="7 days ago"`
   - Check `~/logs/` for cron output logs
   - Check CSB job monitor results: `tail -20 ~/logs/cron-csb-jobs.log` and `cat ~/.local/share/csb-jobs/seen.json | python3 -c "import sys,json; print(len(json.load(sys.stdin)),'jobs tracked')"`
   - If any source file is missing/unreadable, note it as unavailable and continue with remaining sources.
   - If a command fails, do not retry repeatedly; record one-line failure and continue.

3. **Synthesize into themes** — don't just list events, find patterns:
   - **Maximum 3-4 themes.** If the week had 6 themes, the skill is logging, not synthesising. Pick the 3 that matter next week.
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

### Career / Capco
- Onboarding progress: [status]
- Client engagements: [any updates]
- Network: [new contacts, follow-ups]

### Skills & Tools
- New/updated skills: [list]
- Tool changes: [any]

### Projects
- [Project]: [status change]

## Learnings Captured

- [Summary of learnings routed to `~/docs/solutions/`, `MEMORY.md`, or skills this week]

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

If all 7 days are within normal range (Sleep >75, HRV >50, bedtime <23:00), collapse to: "**Health: Stable week.** Sleep avg X, HRV avg Y. No flags." Don't enumerate 7 identical rows.

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

## System & Tooling Health (weekly)

Run these checks every Friday and include results in the weekly note under `## System Health`.
If a check command fails, mark that metric as `Unavailable` in the table and continue.

### Infrastructure Services

8. **wacli daemon** — `launchctl list com.terry.wacli-sync`. Check exit code (0 = running, 113 = dead). If dead, flag for restart.
9. **Vault git backup** — Check recency: `cd ~/notes && git log -1 --format='%ci'`. Flag if last commit >2h old (cron runs every 30 min).
10. **Vault link health** — Run two passes:
    - Broken links: `nexis ~/notes --exclude Archive --exclude "Waking Up" --exclude memory 2>/dev/null`. Flag if broken link count >30 or increased from last week.
    - Asymmetric links: `nexis ~/notes --asymmetry --exclude Archive --exclude "Waking Up" --exclude memory 2>/dev/null`. Surface notes that link out but have no backlinks — add backlinks inline if obvious, defer to `/nexis` session if large volume.
    Full triage (atomicity, restructuring) is a separate `/nexis` session — don't do it inline here.
11. **Agent-browser profile** — `ls -la ~/.agent-browser-profile/Default/Cookies 2>/dev/null && echo "OK" || echo "MISSING"`. Flag if profile directory is missing or Cookies file absent.

### AI Tooling

1. **CLAUDE.md & MEMORY.md content review** — Check line counts (`wc -l`). Flag if CLAUDE.md >200 or MEMORY.md >150. Then:
   - **Staleness scan:** Flag sections referencing past dates, completed transitions, retired tools, or situations that no longer apply. Check "Current Situation", "Current Projects", date-anchored content in CLAUDE.md. Check MEMORY.md for entries about tools/projects no longer in use.
   - **MEMORY.md frequency review:** Scan entries and ask: "Which of these fired this week?" Entries have three tiers — permanent (weekly use, never demote), active (current project, demote when project ends), provisional (single-incident). Any provisional entry not cited 2 consecutive weeks → demote to `~/docs/solutions/memory-overflow.md`. Any overflow entry cited 2+ weeks → promote back. Budget: ~150 lines (200 is hard truncation).
   - Present a concrete list: "Remove X", "Demote Y to overflow", "Promote Z from overflow", "Keep W" — don't just flag, recommend actions.
   - During transition periods (job changes, major project shifts), this is the most valuable check
2. **Skills inventory** — `ls ~/skills/*/SKILL.md | wc -l` for total count. `cd ~/skills && git log --oneline --since="7 days ago"` for changes. Flag skills not invoked in 30+ days (check `~/.claude/anam.jsonl` for recent `/skill` usage). Check for overdue retirements: `grep -rl "retire_after:" ~/skills/*/SKILL.md | xargs grep "retire_after:" | awk -F': ' '{print $1, $NF}'` — delete any skill whose `retire_after` date has passed.
3. **MCP servers** — `claude mcp list` to verify health. Flag any disconnected, orphaned from experiments, or version-drifted servers.
4. **Token consumption** — Run `cu` alias for Max20 usage stats. Note weekly trend and any spikes.
5. **Oghma health** — `oghma_stats` for DB size, memory count, extraction backlog.
6. **Cron scripts** — Check `~/scripts/crons/` and `~/logs/cron-*.log` for failures or stale output.
7. **QMD index** — `qmd cleanup && qmd update` to prune stale entries and re-index. Then `qmd status` for collection health.

Include a summary table in the weekly note:

```markdown
## System Health

| Metric | Value | Status |
|--------|-------|--------|
| wacli daemon | running/dead | ✅/🔴 |
| Vault backup | Xm ago | ✅/⚠️ |
| Vault broken links (signal) | X | ✅/⚠️ |
| Agent-browser profile | present/missing | ✅/⚠️ |
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
4. **CSB job monitor** — Any new AI-related government vacancies this week? Check `~/logs/cron-csb-jobs.log` for matches
5. **Conversation Cards refresh** — Scan `~/notes/Capco/Conversation Cards/*.md` (governance, agentic, cost, responsible AI/MRM). Check: any data points outdated? Any new vault material that should feed in? Update `Last updated` date on any card you touch. 60-second scan per card — if nothing changed, move on.
6. **Priorities for the week** — Top 2-3 actions
7. **AI landscape** — Run `/lustro --deep` first to pull full source sweep, then `/ai-review` for weekly synthesis (client talking points).
8. **Capco intel sweep** (until start date only — remove after onboarding):
   - Search: "Capco HK" or "Capco Asia" news this week
   - Search: HKMA AI/fintech guidance, GenAI deployments at HK banks
   - Search: competitor moves in HK FSI (Accenture, EY, KPMG, Deloitte)
   - Synthesize into 3 bullets: Capco firm news | AI x banking | Competitor signal
   - Feed anything useful into `~/notes/Capco/Conversation Cards/` if it's a durable talking point
9. **ClawHub scan** — Browse [clawhub.ai](https://clawhub.ai) for new/notable skills using semantic search. Focus areas: messaging, health/biometrics, calendar, finance, relationship/CRM. Surface 1-3 ideas worth building; append to `~/notes/Awesome OpenClaw Skills - Evaluation.md` if notable. Skip if nothing new since last week.

10. **First Friday only** — Run `/monthly` (content digests, skill review, AI deep review, vault hygiene)
   - If a checklist command fails, keep the item open and note the failure reason in the weekly note.

[[Capco Transition]] is source of truth for exit/onboarding; [[Job Hunting]] is the archive.

## Notes

- Create `~/notes/Weekly/` directory if it doesn't exist
- Link back to daily notes and relevant vault notes
- The synthesis captures the broader picture; the reset checklist is action-oriented
- The energy audit is the most valuable section long-term — it reveals what work is sustainable

## Boundaries

- Do NOT run full remediation workflows inline (e.g., full nexis triage or large refactors); only surface and flag.
- Do NOT expand beyond the current week scope.
- Stop after weekly note + reset checklist outputs; do not start execution tasks unless explicitly asked.

## Example

> Week of 2026-03-02: 5/7 active days. Themes were Capco transition prep, skill-system hardening, and inbox/process hygiene. Main carry-over is one unresolved architecture decision and two overdue admin items. System health is mostly green with one unavailable check (MCP list failed).
