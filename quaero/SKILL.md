---
name: quaero
description: Multi-round research campaign — parallel search tools, verification, cross-source synthesis. Use when a topic needs thorough investigation beyond a single search query. NOT for quick lookups (use indago/WebSearch) or single-query parallel search (use elencho).
trigger: /quaero, "research this thoroughly", "deep dive on", "I need to understand X", or when a topic clearly needs multiple rounds of investigation
disable-model-invocation: true
---

# quaero — Systematic Research Campaign

Multi-round research methodology for topics that need more than a single search. Empirically developed Mar 2026; validated on multi-agent orchestration research (5 agents, 4 tools, 2 verification passes). Adversarially reviewed via cross-model mining (Grok).

## When to Use

- Topic needs cross-source validation (not just one answer)
- Stakes are high enough to justify 15-60 min and $1-5 in search costs
- You need to form a *view*, not just find a *fact*

**Don't use for:** Quick lookups (WebSearch), single parallel query (elencho), topics where one authoritative source exists, or when you need to hold a position (quaero generates doubt, not conviction).

## The Campaign

### Round 0: Frame (2-5 min)

**For unfamiliar topics:** Do a 5-min unstructured scout first (free WebSearch browsing, no agents). Pre-registration is only useful if the prior is grounded — encoding ignorance as structure wastes rounds.

Then write down:
1. **The question** — one sentence
2. **What you expect to find** — your prior (pre-registration; mismatches are your best findings)
3. **What would change your mind** — the inverse evidence you'd need
4. **Entity list** — specific names, models, tools, people, companies relevant to the topic

### Round 1: Broad Sweep (5-10 min)

Launch a **researcher agent** (WebSearch-based) with a comprehensive prompt covering the full topic. This establishes the landscape and surfaces the initial narrative.

While waiting, note: what vocabulary is this topic discussed in? Who are the key names? What are the sub-questions?

### Round 2: Parallel Multi-Tool + Entity Expansion (5-10 min)

Launch **all search tools in parallel** as separate background agents:

| Agent | Tool | What it uniquely surfaces |
|---|---|---|
| Researcher | WebSearch | Broad coverage, free, good honesty filter |
| Exa | `exauro search` / `exauro similar` | Semantic/neural matches, adjacent content, find-similar trails |
| Grok | `grok` / `grok --x-only` | X/Twitter practitioner reports, real-time reactions |
| Noesis | `noesis search` / `noesis ask` | Synthesised answers with citations, structured surveys |

**In the same round**, include entity-specific searches from your Round 0 list (specific names bypass the synonymy problem). Also run **negation queries**: "X doesn't work", "X disappointing", "migrating from X".

**Note:** WebSearch, Noesis, and Exa crawl overlapping web corpora. Grok (X/Twitter) is the only tool with genuine corpus independence. The unique-finding benefit is real but comes more from different synthesis approaches than truly independent indexes.

### Prior Update Checkpoint (2 min)

Before proceeding, explicitly restate your Round 0 prior: **what changed?** "I expected X but found Y. My estimate moved from _ to _ because _." This makes pre-registration do real epistemic work instead of being a document that sits unused.

### Round 3: Targeted Follow-Up (5 min)

Search for **entities discovered in Rounds 1-2** that weren't in your Round 0 list. These are the highest-value targets — names you didn't know to look for.

Also run **negation queries** on key claims: "X doesn't work", "X disappointing", "we stopped using X". Failure reports live in a different lexical neighborhood than success stories.

### Round 4: Verification (5-10 min)

Launch a **separate verification agent** on the 5-7 key claims. For each:
- Does the cited source exist?
- Does it actually say what's claimed? **(Check context, not just existence — the #1 verification failure is confirming a paper exists while missing that the claim was a caveat, not the main finding)**
- What venue? (Workshop ≠ main track. Blog ≠ peer-reviewed.)
- Are the numbers from the main analysis or a subset/caveat?
- Any counter-evidence?

### Round 5: Blind Spot Check (2 min) — GATES SYNTHESIS

**Run this BEFORE synthesising, not after.** If you discover a gap here, fill it before writing conclusions.

- [ ] **Non-English sources?** Search in the language of the community (Chinese for Chinese AI labs, Japanese for niche tech)
- [ ] **Inverse evidence?** Did you search for "when X fails" / "X worse than Y"?
- [ ] **Adjacent domains?** Would researchers in a related field frame this differently?
- [ ] **Temporal coverage?** Are your findings all from one time period?
- [ ] **Who would disagree?** Can you name the strongest critic of your synthesis?
- [ ] **Survivorship?** Are you only seeing success stories? What's the denominator?

### Round 6: Cross-Source Synthesis (5 min)

For each agent's results, ask:
1. **What did this source uniquely surface?** — If only one source found it, is there a plausible mechanism for unique access?
2. **Where do sources agree?** — Convergence across independent tools = high confidence. **But check source genealogy:** are 5 sources agreeing independently, or are 5 sources quoting one original? The BBC quoting Reuters quoting a single spokesperson is three sources of one claim.
3. **Where do they disagree?** — Classify: (a) different definitions, (b) different conditions, (c) different time periods, (d) genuine empirical disagreement. Most conflicts are (a) or (b).
4. **Tag every claim with its time vintage.** In fast-moving fields, a finding from 18 months ago may be directionally reversed today.

### Round 7: Termination Check

Stop when **three consecutive queries yield only findings you've already seen** AND the blind spot checklist has been run AND at least one adversarial query per key claim has returned nothing new.

If an important question remains unanswered, that's not a stopping point — it's your most important remaining query. Especially if you're avoiding it because the answer might undermine your narrative.

**Beware lazy stopping:** "three queries yielded nothing new" can mean the topic is exhausted, or your queries got bad. Ask: am I stopping because the evidence is exhausted, or because my questions got lazy?

## Output

Save results to vault note with:
- Synthesis (what we found, organized by confidence level)
- Key sources (with honest evidence quality ratings and time vintage)
- Open questions (what we couldn't answer and why)
- Blind spots acknowledged
- Practical recommendations

If the findings are interesting → `sarcio new` garden post.

## Heuristics

**Source weighting:** In adversarial/commercial contexts: disinterested observer > motivated believer > motivated seller. A vendor saying their product works ≈ zero signal. **But in technical/practitioner contexts:** a motivated practitioner with skin in the game (production system, not a weekend project) is often higher-signal than a disinterested observer who doesn't use it. Disinterested ≠ expert.

**Recency vs authority:** In fast-moving fields, the consensus in search results lags reality by 6-18 months. Primary sources (tweets, issues) are higher in signal *potential* but also higher in noise. Use them for current state; use synthesised secondary sources for baseline understanding and calibration.

**Narrative coherence warning:** If your findings form a clean story with no loose ends, you've probably pruned contradictory evidence. **But:** coherence is suspicious when the domain is genuinely messy; coherence is expected when the domain is well-understood. The warning fires on *surprising* coherence given expectations of messiness, not coherence per se.

**The mechanism test for transfer:** Before applying findings from domain A to domain B, identify the mechanism. Does it exist in domain B? Check boundary conditions — findings are stated as universals but are actually bounded.

**Entity exhaustion before concept exhaustion.** Search for every named entity individually before concluding the concept-level search is done. **Caveat:** only high-ROI when your entity list was built from Round 1-2 breadth, not just pre-registered guesses from Round 0.

**The jargon ladder.** Search at three vocabulary levels — expert jargon, practitioner language, layperson phrasing. Each surfaces different source types.

**Source genealogy.** When multiple sources converge, trace the claim to its origin. Independent convergence is strong evidence; citation cascades from one original source are not.

## Cost Budget

| Round | Typical cost |
|---|---|
| Broad sweep (researcher) | Free (WebSearch) |
| Multi-tool expansion | ~$0.10 (exa + grok + noesis) |
| Entity search | ~$0.10 |
| Verification | Free-$0.10 |
| **Total** | **$0.20-0.50** + agent compute |

## Optional: Mine Heuristics with fodina

After synthesis, consider running `/fodina` to extract implicit model knowledge about the research domain. **Use cross-model mining** (consilium adversarial tier, not same-model interview) — same model interviewing itself produces less novel output than a different model challenging assumptions. See `fodina` skill.

## Relationship to Other Skills

- **indago** — tool selection reference (which tool for which query). Quaero is the campaign methodology.
- **elencho** — single parallel query across 3 tools. Quaero is multi-round with verification.
- **fodina** — mine implicit model knowledge into permanent heuristics. Use after synthesis to fill gaps. Cross-model mining preferred.
- **heuretes** — agent research org for code exploration. Quaero is for desk research.
- **trutina** — conflicting evidence reconciliation. Invoke from Round 6 when sources genuinely disagree.
- **consilium** — judgment calls. Invoke after quaero when findings need a decision.
