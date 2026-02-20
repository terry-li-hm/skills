---
name: monthly
description: Monthly maintenance — content digests, skill review, AI deep review, vault hygiene. Run on first Friday or anytime in the first week.
user_invocable: true
---

# Monthly Maintenance

Everything that runs once a month. Can trigger on first Friday (via `/weekly`) or independently anytime.

## Trigger

- "monthly", "monthly maintenance", "run monthly"
- First Friday of month (prompted by `/weekly`)

## Checklist

Run each section in order. Report results as a summary table at the end.

### 1. Content Digest

Fetch and extract insights from subscribed YouTube channels.

```bash
# Preview what's new
digest --dry-run

# Run full digest (transcripts + insight extraction)
digest
```

Output: `~/notes/Health/{source}/{YYYY-MM} Digest.md`
Sources configured in `~/skills/digest/sources.yaml`.

### 2. AI Landscape Deep Review

Run `/ai-review` in monthly mode (deep review, not weekly synthesis):
- Update Current Landscape section
- Append monthly review entry
- Flag shifts relevant to Capco consulting conversations

### 3. Skill Review

Run `/skill-review`:
- Audit skills for staleness, drift, gaps
- Check skill count and recent changes
- Flag skills not invoked in 30+ days

### 4. Vault Hygiene

Run inline — no separate skill needed:

a. **Solutions KB** — regenerate index (`python3 ~/scripts/generate-solutions-index.py`) then review for stale or duplicate entries
b. **Decay report** — `uv run ~/scripts/vault-decay-report.py` for orphans/cold notes
c. **Daily note archival** — archive notes >60 days old to `~/notes/.archive/dailies/`
d. **Broken links** — verify `[[wikilinks]]` in CLAUDE.md still resolve
e. **QMD reindex** — `qmd update && qmd status` (run `qmd embed` in background if stale)

### 5. Oghma Hygiene

Check for noise from abandoned experiments or stale imports:

```bash
oghma stats
```

Flag any source with >100 entries that isn't `claude_code`, `opencode`, or `codex` — these are likely stale imports (e.g., MemU, openclaw) that should be archived:

```python
python3 -c "
import sqlite3, os
conn = sqlite3.connect(os.path.expanduser('~/.oghma/oghma.db'))
c = conn.cursor()
c.execute(\"\"\"SELECT source_tool, COUNT(*) as cnt FROM memories
    WHERE status='active' GROUP BY source_tool HAVING cnt > 100
    ORDER BY cnt DESC\"\"\")
legit = {'claude_code', 'claude-code', 'opencode', 'codex'}
for tool, cnt in c.fetchall():
    flag = '' if tool in legit else ' ⚠️  REVIEW'
    print(f'{tool}: {cnt}{flag}')
conn.close()
"
```

If flagged sources exist, archive them:
```python
# python3 -c "import sqlite3, os; conn = sqlite3.connect(os.path.expanduser('~/.oghma/oghma.db')); conn.execute(\"UPDATE memories SET status='archived' WHERE source_tool='SOURCE_NAME' AND status='active'\"); conn.commit(); print('Done')"
```

### 6. Housekeeping

- Purge orphaned agent files: `/usr/bin/find ~/.claude/todos -name "*.json" -mtime +7 -delete`
- Check MEMORY.md line count (`wc -l`). Flag if >150 — trim or demote to vault.
- Check CLAUDE.md for stale references (completed transitions, retired projects)

## Summary Template

After running all sections, present:

```markdown
## Monthly Maintenance — YYYY-MM

| Section | Status | Notes |
|---------|--------|-------|
| Content Digest | X episodes across Y sources | [vault paths] |
| AI Deep Review | Done | [key shifts] |
| Skill Review | X active / Y archived | [changes] |
| Vault Hygiene | X notes archived, Y orphans | [actions] |
| Housekeeping | MEMORY.md: X lines, agents purged | [flags] |
```

## Notes

- Total time: ~15-20 min (mostly waiting on digest API calls)
- Digest is the heaviest step — can run backgrounded while doing the rest
- If short on time, at minimum run `/digest` and `/skill-review`
