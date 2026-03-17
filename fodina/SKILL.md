---
name: fodina
description: LLM knowledge mining — extract implicit model knowledge into permanent reference skills. Two tiers: single-model interview (quick) and consilium adversarial refinement (deep). Use when a topic would benefit from stable, always-loaded theory that the model knows but surfaces inconsistently.
user_invocable: true
tags: [meta, knowledge, skills]
---

# /fodina — LLM Knowledge Mining

> *Fodina: Latin "mine" — the place you extract ore.*

Extract implicit knowledge from LLM weights into permanent, version-controlled reference skills. The model knows things it won't reliably surface — mining makes that knowledge explicit and deterministic.

## When to Mine

- You notice the model gives brilliant insight on a topic sometimes, mediocre insight other times
- A domain has stable theory (debugging, planning, writing) that doesn't change with tooling
- You keep re-explaining the same concept across sessions
- A reference skill would make multiple other skills better (like bouleusis improves rector, examen, topica)

**Don't mine:**
- Volatile knowledge (API versions, tool flags) — that's docs, not theory
- Procedural knowledge (how to run X) — that's a regular skill
- Knowledge the model doesn't actually have depth on — test with one probing question first

## Tier 1: Single-Model Interview

Fast, good for well-understood domains where the model has clear depth.

**Process:**
1. **Probe** — ask the model an open question about the domain ("what is planning?")
2. **Push past first answer** — the second and third layers are where structure lives. Ask "what distinguishes this from X?" or "where does this break down?"
3. **Find the bones** — look for: taxonomy (types/categories), failure modes, axes of improvement, key distinctions
4. **Distill** — capture as a reference skill with `disable-model-invocation: true`
5. **Wire** — add cross-references to skills that would benefit (this is not optional — unwired skills get forgotten)
6. **Publish** — if the insight is non-obvious, `sarcio new` for a garden post

**Output:** One reference skill file. ~50-100 lines. Stable knowledge, not procedures.

## Tier 2: Consilium Adversarial Refinement

Deeper. Multiple models debate the extracted knowledge, find gaps, challenge assumptions. Use for high-stakes theory or when Tier 1 output feels thin.

**Process:**
1. **Run Tier 1 first** — you need a draft to refine
2. **Feed draft to consilium** — `consilium "Review this theory of <X>. What's missing? What's wrong? What failure modes aren't listed? What distinctions are false?" --vault`
3. **Synthesise** — the council will surface blind spots, edge cases, and counterarguments. Merge into the skill.
4. **Adversarial pass** — ask specifically: "What would someone who disagrees with this framework say? What domains does it fail in?"
5. **Update skill + re-wire** if the structure changed significantly

**Output:** A battle-tested reference skill. The council catches things a single model misses: blind spots, false distinctions, missing failure modes.

## Tier 3: Field Validation

The only tier that touches reality. Tiers 1-2 are still theory — extracted and stress-tested, but untested in practice.

**Process:**
1. **Use the skill in real work** — let it load into sessions, observe when it fires
2. **Track hits and misses** — when the skill helps, note it. When it's wrong or missing something, note that too. Log in the skill's own file or `decay-tracker.md`.
3. **Revise from evidence** — after 2-4 weeks of use, update the skill based on what actually happened, not what the models thought would happen
4. **Prune false distinctions** — theory that sounded right but never proved useful in practice gets cut

**Output:** A field-tested skill. The difference between Tier 2 and Tier 3 is the difference between a peer-reviewed paper and a practitioner's handbook.

**Cadence:** Passive — runs in the background as you work. Review each mined skill in `/weekly` or `/monthly`.

## Mining Queue

Topics identified as worth mining (stable theory, currently in weights only):

1. ~~Theory of debugging~~ → `diagnosis` (done)
2. ~~Theory of simplification~~ → `parsimonia` (done)
3. ~~Theory of delegation~~ → `mandatum` (done)
4. ~~Theory of evaluation~~ → `kritike` (done)

**Cadence:** One per session. Don't batch — each needs a fresh conversation for depth.

## Wiring Checklist

After creating any mined skill:
- [ ] Add cross-references to all skills that would benefit (grep for related triggers)
- [ ] Update this file's Mining Queue with the new skill name
- [ ] Consider a garden post if the insight is non-obvious
- [ ] Commit skill + wiring changes in same session

## Completed Mines

| Topic | Skill | Tier | Wired to | Garden post |
|-------|-------|------|----------|-------------|
| How planning works | `bouleusis` | 1 | rector, examen, topica | [Mining Your LLM](https://terryli.hm/posts/mining-your-llm) |
| How debugging works | `diagnosis` | 1 | rector | — |
| How experimentation works | `peirasmos` | 1 | peira, judex, examen, topica | [[The Persona Paradox in AI Agent Teams]] |
| How simplification works | `parsimonia` | 1 | rector | — |
| How delegation works | `mandatum` | 1 | rector | — |
| How evaluation works | `kritike` | 1 | judex, peira | — |

## Relationship to Other Skills

- **artifex** — designs skills (structure, naming). fodina is specifically about *extracting knowledge from model weights* into skills.
- **consilium** — the engine for Tier 2 refinement. fodina tells you *when and how* to use it for knowledge extraction.
- **scrinium** — routes knowledge to the right layer. fodina always produces reference skills, not MEMORY.md or docs.
- **topica** — mental models catalog. Mined skills often feed new entries into topica.
