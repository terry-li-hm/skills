---
name: research-protocol
description: Reference for conducting rigorous research. Not user-invocable — consult automatically when doing multi-step research or when user asks to "research" something.
user_invocable: false
---

# Research Protocol

Ensures research goes beyond confident-sounding synthesis to actually-verified conclusions. Consult this skill whenever conducting research with 2+ search calls.

## The Core Problem

AI search tools (Perplexity, WebSearch) produce coherent narratives from thin sources. More tools won't fix this — the gap is process, not coverage.

## Step 1: Classify the Question

| Type | Example | Searchable? |
|------|---------|-------------|
| **Empirical** | "Does multitasking reduce productivity?" | Yes — peer-reviewed evidence exists |
| **Comparative** | "Best framework for X?" | Partially — specs are facts, "best" is context-dependent |
| **Subjective/personal** | "Best hair product for me?" | No — AI synthesis of marketing copy, not testable truth |

For **subjective** questions: shortlist only (3-5 candidates), then redirect to human experts (shop staff, forums, someone who owns it). Do not over-research.

## Step 2: Survey (already doing this)

Use `perplexity_research` for depth or `perplexity_ask` for structured overview. See `web-search` skill for tool selection.

## Step 3: Counter-Search (the step we skip)

After getting initial synthesis, explicitly search for disconfirming evidence:

```
perplexity_ask: "criticism of [claim/framework/product]"
perplexity_ask: "[specific finding] replication failure OR debunked OR limitations"
WebSearch: "[product] problems OR returns OR disappointed"
```

If you can't find counter-arguments, flag that too — absence of criticism for popular things is suspicious.

## Step 4: Spot-Check Key Claims

Pick the 2-3 boldest statistical claims from Step 2. Verify against primary source:

- Use `WebFetch` on the cited paper/study URL
- Check: Is the stat from a peer-reviewed study or a blog post? Sample size? Replication?
- Round numbers ("40% improvement", "75% reduction") are red flags — real research produces messy numbers

## Step 5: Synthesize with Source Quality

Present findings with source hierarchy visible:

- **Tier 1:** Peer-reviewed, replicated (PMC, Nature, APA) — cite confidently
- **Tier 2:** Credible single studies, authoritative reviews (Wirecutter, Cook's Illustrated) — cite with context
- **Tier 3:** Blog posts, SEO content, AI-synthesized summaries — use for direction only, never as evidence

## Quick Checklist

Before presenting research conclusions, verify:

- [ ] Counter-arguments explicitly searched?
- [ ] Boldest claim verified against primary source?
- [ ] Source tier visible in presentation?
- [ ] Subjective questions redirected to human experts rather than over-researched?

## Anti-Patterns

- **More tools = better research.** No. Tavily, Exa, Serper return the same SEO-dominated index. The gap is critical evaluation, not source volume.
- **Perplexity confidence = reliability.** It synthesizes thin sources into authoritative-sounding prose. 60 citations doesn't mean 60 independent sources — often 3-4 blog posts recycled.
- **Research and decision in same session.** For purchases and irreversible decisions, sleep on it. Same-session research → purchase is a pattern we've identified as consistently suboptimal.
- **Skipping red-team for things we like.** Confirmation bias is strongest when the initial result matches our preference. Always search "[thing] problems" before committing.
- **Adding tools before testing process.** Resist researching new search tools until the protocol has been tested enough to reveal a specific gap.

## Usage Log

Track each use to evaluate whether the protocol adds value. After ~10 entries, review for patterns.

<!-- Format: date | topic | type | counter-search found something? | spot-check changed conclusion? | notes -->
| Date | Topic | Type | Counter-Search Hit? | Spot-Check Changed Conclusion? | Notes |
|------|-------|------|---------------------|-------------------------------|-------|
| *awaiting first use* | | | | | |
