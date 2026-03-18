---
name: quaero
description: Multi-round research campaign — parallel search tools, verification, cross-source synthesis. Use when a topic needs thorough investigation beyond a single search query. NOT for quick lookups (use indago/WebSearch) or single-query parallel search (use elencho).
trigger: /quaero, "research this thoroughly", "deep dive on", "I need to understand X", or when a topic clearly needs multiple rounds of investigation
disable-model-invocation: true
---

# quaero — Systematic Research Campaign

Multi-round research methodology for topics that need more than a single search. Empirically developed Mar 2026; validated on multi-agent orchestration research (5 agents, 4 tools, 2 verification passes).

## When to Use

- Topic needs cross-source validation (not just one answer)
- Stakes are high enough to justify 15-60 min and $1-5 in search costs
- You need to form a *view*, not just find a *fact*

**Don't use for:** Quick lookups (WebSearch), single parallel query (elencho), or topics where one authoritative source exists.

## The Campaign

### Round 0: Frame (2 min)

Before searching, write down:
1. **The question** — one sentence
2. **What you expect to find** — your prior (pre-registration; mismatches are your best findings)
3. **What would change your mind** — the inverse evidence you'd need
4. **Entity list** — specific names, models, tools, people, companies relevant to the topic

### Round 1: Broad Sweep (5-10 min)

Launch a **researcher agent** (WebSearch-based) with a comprehensive prompt covering the full topic. This establishes the landscape and surfaces the initial narrative.

While waiting, note: what vocabulary is this topic discussed in? Who are the key names? What are the sub-questions?

### Round 2: Parallel Multi-Tool Expansion (5-10 min)

Launch **all search tools in parallel** as separate background agents:

| Agent | Tool | What it uniquely surfaces |
|---|---|---|
| Researcher | WebSearch | Broad coverage, free, good honesty filter |
| Exa | `exauro search` / `exauro similar` | Semantic/neural matches, adjacent content, find-similar trails |
| Grok | `grok` / `grok --x-only` | X/Twitter practitioner reports, real-time reactions |
| Noesis | `noesis search` / `noesis ask` | Synthesised answers with citations, structured surveys |

**Critical:** Each tool surfaces 20-40% unique findings the others miss. Running only one tool leaves systematic blind spots.

### Round 3: Targeted Entity Search (5 min)

Extract every **specific named entity** from Rounds 1-2 (people, model names, tool names, company names, benchmark names) and search for each directly.

**This is the highest-ROI second pass.** Generic searches ("frontier model orchestration") miss what entity searches ("Opus 4.6 multi-agent") find, because entity names bypass the synonymy problem.

Also run **negation queries**: "X doesn't work", "X disappointing", "migrating from X", "X alternatives". Failure reports live in a different lexical neighborhood than success stories.

### Round 4: Verification (5-10 min)

Launch a **separate verification agent** on the 5-7 key claims. For each:
- Does the cited source exist?
- Does it actually say what's claimed? (Check context, not just existence)
- What venue? (Workshop ≠ main track. Blog ≠ peer-reviewed.)
- Are the numbers from the main analysis or a subset/caveat?
- Any counter-evidence?

**Anti-pattern:** Verifying the quotation but not the context. "Paper X found Y" — check whether Y was the main finding, a caveat, or something the paper argued against.

### Round 5: Cross-Source Synthesis (5 min)

For each agent's results, ask:
1. **What did this source uniquely surface?** — If only one source found it, is there a plausible mechanism for unique access?
2. **Where do sources agree?** — Convergence across independent tools = high confidence
3. **Where do they disagree?** — Classify: (a) different definitions, (b) different conditions, (c) different time periods, (d) genuine empirical disagreement. Most conflicts are (a) or (b).

### Round 6: Blind Spot Check (2 min)

Before stopping, check:
- [ ] **Non-English sources?** Search in the language of the community (Chinese for Chinese AI labs, Japanese for niche tech)
- [ ] **Inverse evidence?** Did you search for "when X fails" / "X worse than Y"?
- [ ] **Adjacent domains?** Would researchers in a related field frame this differently?
- [ ] **Temporal coverage?** Are your findings all from one time period?
- [ ] **Who would disagree?** Can you name the strongest critic of your synthesis?
- [ ] **Survivorship?** Are you only seeing success stories? What's the denominator?

### Round 7: Termination Check

Stop when **three consecutive queries yield only findings you've already seen** (same substance, different words). That's your power-law diminishing return signal.

If an important question remains unanswered, that's not a stopping point — it's your most important remaining query. Especially if you're avoiding it because the answer might undermine your narrative.

## Output

Save results to vault note with:
- Synthesis (what we found, organized by confidence level)
- Key sources (with honest evidence quality ratings)
- Open questions (what we couldn't answer and why)
- Blind spots acknowledged
- Practical recommendations

If the findings are interesting → `sarcio new` garden post.

## Heuristics

**Source weighting:** Disinterested observer > person who benefits from being right > person who benefits from you believing them. A vendor saying their product works ≈ zero signal.

**Recency vs authority:** In fast-moving fields (AI/ML), the consensus in search results lags reality by 6-18 months. Weight recent primary sources (tweets, issues) over recent secondary sources (blog posts, papers) for current state.

**Narrative coherence warning:** If your findings form a clean story with no loose ends, you've probably pruned contradictory evidence. Reality is messy. Accurate syntheses have awkward caveats.

**The mechanism test for transfer:** Before applying findings from domain A to domain B, identify the mechanism. Does it exist in domain B? Surface similarity ("both are LLMs") is not sufficient.

**Entity exhaustion before concept exhaustion.** Search for every named entity individually before concluding the concept-level search is done. Entity searches routinely surface 30-40% of total findings.

**The jargon ladder.** Search at three vocabulary levels — expert jargon, practitioner language, layperson phrasing. Each surfaces different source types. The most valuable sources often use vocabulary one rung below what you'd expect.

## Cost Budget

| Round | Typical cost |
|---|---|
| Broad sweep (researcher) | Free (WebSearch) |
| Multi-tool expansion | ~$0.10 (exa + grok + noesis) |
| Entity search | ~$0.10 |
| Verification | Free-$0.10 |
| **Total** | **$0.20-0.50** + agent compute |

## Relationship to Other Skills

- **indago** — tool selection reference (which tool for which query). Quaero is the campaign methodology.
- **elencho** — single parallel query across 3 tools. Quaero is multi-round with verification.
- **heuretes** — agent research org for code exploration. Quaero is for desk research.
- **trutina** — conflicting evidence reconciliation. Invoke from Round 5 when sources genuinely disagree.
- **consilium** — judgment calls. Invoke after quaero when findings need a decision.
