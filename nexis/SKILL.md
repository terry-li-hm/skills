---
name: nexis
description: "Obsidian vault link health — scan, triage broken links, surface orphans. Use when running nexis CLI or triaging vault link issues."
user_invocable: true
cli: nexis
cli_version: 0.2.3
---

# /nexis — Vault Link Health

Two modes: **scan** (quick health check) and **triage** (fix broken links interactively).

## Triggers

- `/nexis` — scan vault, summary view
- `/nexis triage [--folder <subfolder>]` — interactive broken link triage
- `/nexis orphans` — surface non-noise orphans worth reviewing

---

## Mode: Scan

Quick health check. Always exclude noise dirs by default.

```bash
# Summary (default — counts only)
nexis ~/notes --exclude Archive --exclude "Waking Up"

# Full vault (with noise context)
nexis ~/notes
```

**Interpreting results:**
- Broken links: Archive + Waking Up = noise. Signal = everything else.
- Orphans: Daily notes + Archive = expected. Flag active notes with no connections.
- Embeds: Informational — embeds count toward connectivity.

---

## Mode: Triage

Fix broken links interactively. Works on unique *targets* (not sources) — same target broken in 5 files = one decision, one batch fix.

### Step 1: Scope the run

```bash
# Scoped to a subfolder (recommended — avoids noise)
nexis ~/notes --broken 2>/dev/null | grep "^  <Folder>/"

# Or full vault excluding noise
nexis ~/notes --exclude Archive --exclude "Waking Up" --broken 2>/dev/null
```

### Step 2: Extract unique broken targets

```bash
nexis ~/notes --broken 2>/dev/null | grep "^  <Folder>/" \
  | sed 's/.*: //' | sort -u
```

### Step 3: For each unique broken target, classify

For each `[[Target]]`:

1. **Search vault for likely redirect:**
```bash
find ~/notes -name "*.md" 2>/dev/null \
  | grep -i "<keyword from target>" \
  | grep -v ".obsidian\|Archive"
```

2. **Check if intentional placeholder** — read the source line for context:
```bash
grep -rn "Target" ~/notes/<Folder>/ 2>/dev/null | head -5
```

3. **Classify as one of:**
   - **Redirect** — note exists under different name → propose rename
   - **Placeholder** — note was planned, never written → leave untouched
   - **Stale/remove** — reference is dead, link adds no value → propose removal

### Step 4: Present batch proposal before touching anything

Present a summary table:

| Target | Classification | Proposed action |
|--------|---------------|----------------|
| `[[Simon Eltringham - HSBC Interview Prep]]` | Redirect | → `[[Simon Eltringham - HSBC Profile]]` (5 files) |
| `[[Decision-Making Under Pressure]]` | Placeholder | Leave — planned note |
| `[[str-relabelling skill]]` | Stale | Remove from Related field |

**Do not make any edits until user confirms the table.**

### Step 5: Apply confirmed fixes

For redirects and removes, use `sed -i ''` to batch-replace across all source files:

```bash
# Redirect
sed -i '' 's/\[\[Old Name\]\]/[[New Name]]/g' file1.md file2.md ...

# Remove from pipe-delimited Related field
sed -i '' 's/ | \[\[Dead Link\]\]//g; s/\[\[Dead Link\]\] | //g' file.md
```

Verify with a follow-up nexis run on the same scope.

---

## Mode: Orphans

Surface non-noise orphans that might need attention.

**Default (summary only):** The total orphan count includes 8K+ Daily/Archive/Books noise. Use `--orphan-days` to get actionable signal immediately.

```bash
# Recency filter — the right default (v0.2.2+)
nexis ~/notes --orphan-days 30 2>/dev/null

# Full orphan list (noisy — use grep to filter)
nexis ~/notes --orphans 2>/dev/null \
  | grep -v "^  Archive/\|^  Daily/\|^  Waking Up/\|^Vault\|^  Orphans\|^  Broken\|^  Embeds\|^===" \
  | grep -v "^$" \
  | head -30
```

`--orphan-days 7` → orphans modified in the last 7 days (recently active, not yet connected)
`--orphan-days 30` → broader recent window — catches notes that drifted disconnected over the past month

**What's worth acting on:**
- Active project notes with no links (disconnected knowledge)
- Draft posts / articles that were never linked from a hub
- Recent notes (< 30 days) that haven't been connected yet

**What to ignore:**
- Template files, scratch notes, one-off exports
- Books/, Daily/, Archive/ — expected orphans even with `--orphan-days`

---

## Known Patterns

| Pattern | Meaning | Fix |
|---------|---------|-----|
| Note renamed "X - Interview Prep" → "X - Profile" | Rename during transition | Redirect |
| `[[skill-name]]` in vault Related fields | Points to Claude skill, not vault | Remove |
| `[[Note#Section]]` resolves fine (v0.2.1+) | Anchor stripped, stem matched | No action |
| `warning: duplicate stem "X"` (v0.2.3+) | Two notes share same filename in different folders | One wins; the other is unlinkable by `[[X]]` — rename or use path-qualified links |
| Stray `-->` in note without `<!--` opener | Garbled/corrupted content — NOT a comment block | Links below it are real broken links |
| HTML comment `<!-- [[link]] -->` (v0.2.2+) | Stripped before parsing — never false-positive | No action |
| Running `nexis` on subfolder | Cross-folder links appear broken | Always run on vault root, filter by path |
| Archive/Waking Up dominate broken count | Expected noise | Use `--exclude` to see signal |

## Gotchas

- **Never run `nexis ~/notes/<subfolder>`** — links to notes outside the subfolder will always appear broken. Run on vault root, filter output by path.
- **Broken count drops ~70 with v0.2.1** anchor fix. If seeing high counts on older versions: `cargo install nexis` to upgrade.
- **`--exclude` names match path components exactly** — case-sensitive. `--exclude Archive` works; `--exclude archive` does not.
