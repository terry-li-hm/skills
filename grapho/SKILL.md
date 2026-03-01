---
name: grapho
description: Manage MEMORY.md — add entries, demote over-budget entries to overflow, promote back, review overflow, scaffold solution files. Use when MEMORY.md is over budget, when adding a new gotcha, or when triaging overflow entries.
user_invocable: false
---

# grapho — Memory System CLI

Write-side of the memory system. Pairs with `cerno` (read) — grapho writes, cerno searches.

## Commands

```bash
grapho status                    # line count, budget, section list (exit 1 if over budget)
grapho status --format json      # machine-readable
grapho add                       # interactive: pick section, enter entry (TTY only)
grapho demote "<search>"         # move entry MEMORY.md → overflow
grapho promote "<search>"        # move entry overflow → MEMORY.md
grapho review                    # list overflow entries by age, prompt p/k/d per entry
grapho solution <name>           # scaffold ~/docs/solutions/<name>.md (dedup check)
```

## Files

```
MEMORY.md     ~/.claude/projects/-Users-terry/memory/MEMORY.md
overflow      ~/docs/solutions/memory-overflow.md
solutions     ~/docs/solutions/
budget        150 lines
```

## When to Use

- **Over budget** (`grapho status` exits 1) → `grapho demote` infrequent entries
- **New gotcha to capture** → `grapho add` (TTY) or edit MEMORY.md directly
- **Weekly review** → `grapho review` to triage overflow (promote 2+ repeat hits)
- **New solutions doc** → `grapho solution <name>` (checks dedup before creating)

## Gotchas

- **Search terms must match entry text exactly (substring).** Use short, unique substrings — `"@import"` not `"@import syntax"`. If too specific, no match.
- **Disambiguation requires TTY.** If >1 match, grapho prompts interactively. Run from a real terminal, not via Bash tool.
- **`add`, `promote`, `review` require TTY.** `status`, `demote`, `solution` work piped.
- **Demoting duplicates:** if an entry already exists in overflow, demote adds it again. Check overflow first with `grep` if unsure.
- **Empty sections stay.** Demoting all entries from a section leaves the `## Header` in MEMORY.md. Not a bug — add new entries to it later or ignore.

## Budget Workflow

```bash
grapho status          # check current count
# if over budget:
grapho demote "<low-frequency entry>"   # repeat until under 150
grapho status          # confirm exit 0
```

## Reference

- Source: `~/code/grapho`
- crates.io: `cargo install grapho`
- Plan: `~/code/grapho/docs/plans/2026-03-02-feat-grapho-memory-cli-plan.md`
