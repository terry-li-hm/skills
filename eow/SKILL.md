---
name: eow
description: End-of-work checkpoint. Synthesise the work day, capture work mood, note unfinished threads. Use when user says "eow", "end of work", "done for the day" (before evening).
user_invocable: true
---

# End of Work

Work-day close — the gap between per-session `/wrap` and bedtime `/daily`.

## Triggers

- "eow", "end of work", "done working", "closing work"
- After the last work session of the day (before evening personal time)

## What This Is

A checkpoint that looks at the **whole work day** as a unit. `/wrap` handles individual sessions. `/daily` handles the full day before bed. This sits between them: "how was the work day?"

## What This Is NOT

- Not a session wrap (that's `/wrap`)
- Not the daily close (that's `/daily` — handles tomorrow preview, WORKING.md reset, bedtime mood)
- Does not reset WORKING.md or write the Tomorrow section

## Workflow

1. **Get today's date** — run `date` (HKT)

2. **Read today's daily note** (`~/notes/Daily/YYYY-MM-DD.md`)
   - Session logs from `/wrap` should already be there
   - If empty/missing, delegate history scan to a subagent (same as daily skill fallback)

3. **Synthesise work themes** — cluster work sessions into 3-5 themes. For each: one line with key actions and outcomes. Present to Terry.

4. **Review with Terry:**
   - Show themes — "Here's how the work day groups..."
   - Ask: anything missing from work sessions?
   - Ask: **work mood** (1-5 or a word) — energy, focus, satisfaction with what got done
   - Ask: what's unfinished / carrying over?

5. **Append to daily note:**

```markdown
---

## End of Work

**Themes:** [comma-separated theme labels]

[2-3 sentence synthesis — what the work day was about, what moved, what's stuck. Honest assessment, not a status report.]

**Unfinished:**
- [ ] [Threads carrying over — brief, actionable]

**Work mood:** [1-5 or word, with colour if offered]
```

6. **TODO sweep** — quick scan: anything completed today that should be marked in `~/notes/TODO.md`? Any new commitments? Same as wrap's TODO sweep but day-scoped.

7. Done. No WORKING.md reset, no tomorrow preview — `/daily` handles those before bed.

## Output

Short prose summary of the work day themes and mood. Mention what was written to the daily note. Keep it to 3-4 sentences.

## Notes

- If `/wrap` wasn't run on the last session, do a quick session log first (step 2 of wrap), then proceed
- If Terry runs `/daily` without running `/eow` first, daily should still work fine — eow is additive, not required
- The work mood is separate from the daily mood — work might be frustrating but the evening great, or vice versa
- Keep it fast — this is a 1-minute checkpoint, not a retrospective
