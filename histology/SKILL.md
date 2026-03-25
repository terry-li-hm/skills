---
name: histology
description: AI system architecture review through cell biology lens. Map components to cell-level names, force one level, find gaps from broken mappings. Use for system design, architecture reviews, consulting workshops. "histology", "cell review", "architecture biopsy", "map to biology".
user_invocable: true
model: opus
context: fork
---

# Histology — Architecture Through the Cell Biology Lens

Histology is the microscopic examination of tissue structure. This skill examines an AI system's architecture by forcing every component into a cell-level biological name. Where the name breaks, the gap is the feature.

## Origin

One morning session (25 Mar 2026) produced: 7 garden posts, 3 tool renames, 3 new features, 1 package rename, and 1 consulting methodology — all from forcing cell-level naming on an AI system.

## The Method

```
1. INVENTORY  → List every component of the system (tools, models, data stores, pipelines, APIs)
2. MAP        → Force a cell-level biological name onto each component
3. BREAK      → Test each mapping at the edges. Where does the name not fit?
4. GAP        → Each break is a design gap. The search for the right name IS the design exercise.
5. BUILD      → Design the gap as a reflex (deterministic), not reasoning (LLM-mediated)
```

## The Constraint: Cell Level Only

All names must be cell-level biology. Not molecular (too low — specialists, not systems). Not organism (too high — different problems). Not neuroscience (implies a brain the system may not need).

**Why cell level?** The cell is the lowest level where organized solutions to information problems are coordinated into a self-maintaining system. Below that, you get specialists. Above that, you get navigation and social problems.

Two naming layers:
- **Chemistry for verbs** — crystallise, dissolve, catalyse, substrate, product (what happens)
- **Cell biology for nouns** — membrane, organelle, exocytosis, reflex, metabolon (how it's organized)

## The Reference Table

Start here. Map the client's system to this table:

| Cell structure | What it solves | System equivalent | Questions to ask |
|---|---|---|---|
| Membrane | What gets in, what doesn't | Auth, filtering, taste | Where are the boundaries? What should be rejected? |
| DNA | Instructions that replicate across instances | Config, rules, constitution | What persists when the system restarts? |
| Organelles | Specialized machinery | Services, tools, modules | What are the specialists? Are they right-sized? |
| Enzymes | Native catalysts for specific reactions | Internal tools, functions | What's built in-house vs. outsourced? |
| Symbiont | External organism the host depends on | LLMs, third-party APIs | What's external? What's the internalisation plan? |
| Reflexes | Deterministic responses to stimuli | Hooks, guards, validators | What should be automatic? What's still manual? |
| Metabolism | Process substrates, produce signal | Data pipelines, ETL | How does raw input become useful output? |
| Respiration | Don't exhaust resources | Rate limits, budgets, pacing | What prevents burnout/overspend? |
| Cytoplasm | Medium where reactions happen | Runtime, conversation, context | What's the execution environment? |
| Exocytosis | Export to environment | Notifications, publishing, API responses | How does output leave the system? |
| Endocytosis | Import from environment | Ingestion, scraping, webhooks | How does input enter the system? |
| Chaperones | Quality control before export | Validation, review, pre-checks | What checks happen before output ships? |
| Golgi | Label, package, route output | Routing, formatting, targeting | Does output go to the right place? |
| DNA repair | Scan and fix instructions | Config drift detection, consistency checks | What monitors rule integrity? |
| Cytoskeleton | Structural integrity under load | Resilience, failover, backpressure | What prevents collapse under stress? |

## The Insight Framework

When a mapping breaks, ask three questions:

1. **What does the cell do here?** — Study the real biology (3-5 key properties)
2. **Does our system do this?** — Check honestly
3. **Should it?** — Not every cell structure is needed. But the missing ones are worth evaluating.

## Client Workshop Format

**Duration:** 2 hours
**Output:** Architecture gap map with prioritised recommendations

1. (20 min) **Inventory** — whiteboard every system component
2. (30 min) **Map** — force cell-level names onto each. Struggle is the point.
3. (20 min) **Break** — identify where names don't fit. These are the gaps.
4. (30 min) **Prioritise** — which gaps matter? Rank by: risk if missing, cost to build, regulatory relevance
5. (20 min) **Roadmap** — maturity model: symbiont → reflex → unnecessary for each component

## The Maturity Model

Every component follows the same lifecycle:

```
Symbiont → Reflex → Unnecessary
(external)  (deterministic)  (the trigger can't occur)
```

- **Symbiont stage:** depends on external LLM/API for this function
- **Reflex stage:** crystallised into deterministic pathway (hook, rule, program)
- **Unnecessary stage:** the system restructured so the stimulus can't occur

This maps to regulatory maturity: symbiont = vendor risk, reflex = auditable, unnecessary = eliminated.

## Validated Examples

| Component | Forced name | Break | Gap found | Built |
|---|---|---|---|---|
| Overnight results check | germination | Spores germinate on conditions, not timers | Batch processing should be conditions-triggered | `check_germination()` with flag file |
| Internal state sensing | proprioception | Cells sense gradients, not static state | Status dumps should show trends over time | JSONL gradient logging |
| Output module | secretory | Secretory pathway has chaperones | No quality control before export | PII/special char/length checks |
| LLM role | symbiont | Enzyme/prosthetic/primer/brain all broke | LLM is external organism, not native organ | Endosymbiosis lifecycle in DESIGN.md |

## Anti-Patterns

- **Forcing names that obviously don't fit** — If every component maps perfectly, you're not forcing hard enough. The breaks are the value.
- **Staying at the comfortable level** — Mixing neuro + cell + molecular feels natural but generates fewer insights than forcing one level.
- **Naming without mining** — A cell-level name without studying the real biology is just a label. Use /morphogenesis to mine each name.
- **Building everything** — Not every gap needs filling. Prioritise by actual need, not biological completeness.
