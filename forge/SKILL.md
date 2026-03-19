---
name: forge
description: Weekly career compound machine — produces consulting IP from accumulated sparks. "forge", "weekly forge", "compound machine", "run the forge"
user_invocable: true
---

# The Forge — Weekly Career Compound Machine

Produces consulting intellectual capital from the week's accumulated sparks, AI landscape, and client work.

## Hard Rules

- **LinkedIn: NEVER post, draft full posts, or interact.** Produce seeds only (hook + bullets + angle).
- **Client-identifiable information: NEVER in the library.** Generalize before storing.
- **Quality bar: draft-grade.** All assets created with `maturity: draft`.
- **Autonomous flywheel:** See [[autonomous-flywheel]]. Agents create freely. Terry promotes on demand.

## Prerequisites

Before running, verify:
- `~/notes/Consulting/_sparks.md` has content (daily spark agent has been running)
- `~/notes/Theoria.md` exists (landscape context)
- `~/notes/AI News Log.md` exists (raw news)

If sparks are empty, warn Terry and offer to run a one-off spark generation first.

## Orchestration

### Phase 1: Planning (Opus lead)

Read all inputs and produce a work plan:

**Inputs to read:**
1. `~/notes/Consulting/_sparks.md` — this week's pre-triaged sparks
2. `~/notes/Theoria.md` — AI landscape synthesis
3. `~/notes/North Star.md` — taste filter
4. `~/notes/AI News Log.md` — last 7 days (for context the sparks may have missed)
5. Existing library: `ls ~/notes/Consulting/{Policies,Architectures,"Use Cases",Experiments}/` — for dedup and enrichment
6. Recent client work: `git log --oneline --since="7 days ago" -- ~/notes/Capco/ ~/notes/HSBC/ 2>/dev/null` (if any)

**Plan output:** Which sparks map to which workers. Which existing assets to enrich. What cross-pollination opportunities exist.

### Phase 2: Dispatch Workers (Sonnet, parallel)

Create a team and dispatch 5 parallel workers. Each worker gets:
- Its assigned sparks from the plan
- Read access to existing library (its subdirectory only)
- The frontmatter schema for its asset type
- Instruction to create files as `YYYY-MM-DD-slug.md` with correct frontmatter

**Workers:**

| Worker | Scope | Output directory |
|--------|-------|-----------------|
| content | Garden post drafts (via sarcio) + LinkedIn seeds | `~/notes/Writing/Blog/Published/` + append to `_sparks.md` |
| policy | P&P templates, regulatory deltas, framework updates | `~/notes/Consulting/Policies/` |
| architecture | Reference architectures, patterns, component notes | `~/notes/Consulting/Architectures/` |
| use-case | Use case entries with structured frontmatter | `~/notes/Consulting/Use Cases/` |
| experiment | Experiment designs (NOT execution), technique comparisons | `~/notes/Consulting/Experiments/` |
| intelligence | Weekly brief + competitor lens from `#competitor` sparks | `~/notes/Consulting/_weekly/` (embedded in weekly report) |

**Worker instructions template:**
```
You are the {role} worker for the Career Compound Machine.

Your task: produce draft-grade consulting IP from the assigned sparks.

Assigned sparks:
{sparks}

Existing assets in your directory (for dedup/enrichment):
{existing_files}

Frontmatter schema:
{schema}

Rules:
- One markdown file per asset, named YYYY-MM-DD-slug.md
- Include full frontmatter with maturity: draft
- Draft-grade: substance over polish. Get the ideas down.
- If a spark enriches an existing asset, update the existing file instead of creating a new one.
- Content worker: garden posts go through sarcio. LinkedIn items are seeds only (hook + bullets + angle), appended to _sparks.md with #linkedin-seed tag.
- Experiment worker: design the experiment (hypothesis, method, expected outcome). Do NOT execute.
```

### Phase 3: Synthesis (Sonnet, after all workers complete)

Run a synthesis agent that:
1. Reads all newly created/modified files across all subdirectories
2. Cross-pollinates: flag where one asset should reference another (add `**Related:**` wikilinks)
3. Identifies talk seeds: combinations of experiment + use case + insight that could become a conference talk
4. Regenerates `~/notes/Consulting/_index.md` with updated stats
5. Archives processed sparks: move this week's sections from `_sparks.md` into the weekly report
6. Writes weekly report to `~/notes/Consulting/_weekly/YYYY-WNN.md`
7. Sends Telegram summary via deltos:
   - Assets created/updated (count by stream)
   - Top 3 cross-pollination opportunities
   - Any talk seeds identified
   - Library totals

### Phase 4: Cleanup

- Verify all new files have valid frontmatter
- Confirm `_sparks.md` only contains unprocessed items
- Log run metadata for future reference

## Output

After the forge completes, present Terry with:
1. The Telegram summary (already sent)
2. A one-paragraph prose summary of what was produced and why
3. Any items that need human judgment (experiment execution, client generalization)

## Budget

Target: ~$1-2 per run. Opus lead (~$0.50-1.00) + 5 Sonnet workers (~$0.10 each) + Sonnet synthesis (~$0.10).
First runs may overshoot while prompts tune. Monitor and adjust.
