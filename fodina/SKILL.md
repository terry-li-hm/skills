---
name: fodina
description: LLM knowledge mining — extract implicit model knowledge into permanent reference skills as actionable heuristics. Three tiers: single-model interview (quick), consilium adversarial refinement (deep), field validation. Specimen-based mining uses people (Einstein, Munger), traditions (Stoicism, kaizen), and failures (LTCM, Challenger) as concrete entry points — heuristics sort into existing skills, not new containers. Post-mining skill-map review reveals architectural gaps. Use when a topic would benefit from stable, always-loaded heuristics that the model knows but surfaces inconsistently.
user_invocable: true
tags: [meta, knowledge, skills]
---

# /fodina — LLM Knowledge Mining

> *Fodina: Latin "mine" — the place you extract ore.*

Extract implicit knowledge from LLM weights into permanent, version-controlled reference skills. The model knows things it won't reliably surface — mining makes that knowledge explicit and deterministic.

**Output format: heuristics, not theory.** Every mined skill should be actionable — failure modes to watch for, distinctions that change approach, decision points where the wrong default hurts. Minimal framing to make the heuristics cohere, but the test is: "does reading this change what I do?" If it's only interesting but not behaviour-changing, it's too theoretical.

## What to Mine (The Meta-Skill)

The ability to spot minable knowledge is itself a judgment call. Look for:

**Signals that a topic is worth mining:**
- **Inconsistent depth** — the model gives brilliant insight sometimes, shallow output other times. The inconsistency IS the signal that extractable structure exists in the weights.
- **Stable cognitive operations** — things that don't change with tooling. Planning, debugging, evaluating, simplifying — these are the *verbs* of knowledge work. They underlie domain-specific skills and transfer everywhere.
- **Cross-skill leverage** — a reference skill would make multiple other skills better (like bouleusis improves rector, examen, topica). The more skills it wires into, the higher the mining ROI.
- **Repeated re-explanation** — you keep articulating the same concept across sessions without it sticking.

**What to extract — not "how X works" but "what to consider when doing X".** Ten types of actionable knowledge to look for during extraction:

| Type | Example | When it helps |
|------|---------|---------------|
| **Rules** | "Don't park deliverables" | You know what to do but might not do it |
| **Checklists** | "5 quality axes for wrap-ups" | You don't know what to consider |
| **If-then triggers** | "If 'TODO: consider...' in wrap → decide now or delete" | Conditional — fires on recognition |
| **Distinctions** | "Log vs. insight — different audiences, different destinations" | Prevents conflating things that look similar |
| **Anti-patterns / smells** | "Deferred action disguised as capture" | Recognising what's going wrong |
| **Spectrums** | "Scale wrap depth with session complexity" | Prevents binary thinking — there's a dial |
| **Ordering / priority** | "Route: skill > memory > daily note" | Sequence matters |
| **Signals** | "Inconsistent model depth = extractable structure exists" | What to notice before deciding what to do |
| **Defaults with override** | "Always checkpoint at gear shifts — unless session <10 min" | Rule + explicit escape clause |
| **Reframes** | "Wrap-up is state transfer, not documentation" | Changes how you see the task, makes other heuristics cohere |

Most mines naturally contain several types. During extraction, **name the type** — it sharpens what you're pulling out and prevents drift into explanation.

**Don't mine:**
- Volatile knowledge (API versions, tool flags) — that's docs, not heuristics
- Procedural knowledge (how to run X) — that's a regular skill
- Knowledge the model doesn't actually have depth on — test with one probing question first
- Topics where the existing pieces already cover it well enough — diminishing returns

## Specimen-Based Mining

Mining abstract topics ("what is judgment?") works but plateaus. **Specimens** are concrete things you examine to reveal general structure — a thinker, a tradition, a failure. The specimen is drilled into, not preserved. Language matters: "anchor" implies fixity and invites anchoring bias; "specimen" keeps the relationship honest — you're studying it to learn about the class, then discarding the container.

**Three specimen types:**

| Specimen | Why it works | Example | Output destination |
|----------|-------------|---------|-------------------|
| **People** | A great thinker is a tested integration of heuristics. The life proves the moves cohere. | Einstein, Feynman, Munger | Heuristics sort into existing skills |
| **Traditions** | Like a slow collective person — centuries of refinement. | Stoicism, kaizen, Talmudic debate | Same — tradition is the prompt, skills are the home |
| **Failures** | Anti-patterns cluster tightly around what went wrong. Very concrete. | Challenger, LTCM, Enron | Existing skills gain "don't" entries |

**Specimen types produce different heuristic shapes.** People and traditions yield positive heuristics ("do this") and reveal architectural gaps (homeless heuristics). Failures yield anti-patterns ("don't do this") and reinforce existing skills without revealing new gaps — because failures show where known principles were violated, not where new principles are needed. Mix both types for a complete picture.

**Not good specimens:** Domains (too broad, already `mimesis`), countries (too vague — unless scoped to a tradition), eras (conditions more than moves).

**Process:** Mine the specimen → extract heuristics → sort each heuristic into its natural home skill. The specimen is the drill bit, not the container. **No new skill per specimen.**

**Post-mining: revisit the skill map.** After each specimen, review the heuristic-to-skill mapping. When a heuristic maps to TWO existing skills equally, that's a signal — a concept lives in the cracks between skills. Log these "homeless" heuristics. After 3-4 specimens, review the collection: do they cluster into a concept that deserves its own skill? If yes, the mining has diagnosed a gap in the skill architecture. This is the real payoff — specimens stress-test the skill network, not just enrich it.

**Queue:**
- [x] Einstein → thought experiments, aesthetic selection, productive stubbornness, productive confusion
- [x] Feynman → explanation as understanding, playful formalism, anti-authority heuristics
- [x] Munger → inversion, latticework, circle of competence, avoiding stupidity > seeking brilliance
- [x] Stoicism → premeditatio malorum, dichotomy of control, negative visualisation
- [x] Darwin → disconfirming evidence, exhaustive enumeration, analogy as scaffolding, institutional humility
- [x] Talmudic tradition → structured disagreement, extreme cases, chain of transmission, question > answer, chavruta
- [x] LTCM → model risk blindness, leverage as fragility, genius as risk factor, correlation breakdown, illiquidity, systemic coupling (all anti-patterns → existing skills)
- [ ] Kaizen → (tradition specimen — queued)

## Tier 1: Single-Model Interview

Fast, good for well-understood domains where the model has clear depth.

**Process:**
1. **Probe** — ask the model an open question about the domain ("what is planning?")
2. **Push past first answer** — the second and third layers are where structure lives. Ask "what distinguishes this from X?" or "where does this break down?"
3. **Find the bones** — look for: taxonomy (types/categories), failure modes, axes of improvement, key distinctions
4. **Distill** — capture as a reference skill with `disable-model-invocation: true`
5. **Wire** — add cross-references to skills that would benefit (this is not optional — unwired skills get forgotten)
6. **Publish** — if the insight is non-obvious, `sarcio new` for a garden post

**Step 4.5: Quality gate** — after distilling, ask: "which of these heuristics would actually change behavior?" Most mines produce 80% theory, 20% behavior-changing insight. Flag the 20%. The skill keeps everything (reference is cheap); the garden post carries only the sharp part.

**Step 6 detail: Mine → garden conversion.** Never publish the framework. Publish one distinction, grounded in a specific moment. The skill is the map; the post is the story of discovering one landmark.

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

**Cadence:** One per session. Don't batch — extraction quality degrades within a conversation (fresh context = fresh extraction). Validated: 7 specimens in one session, first 6 strong, 7th felt mechanical.

**Saturation curve:** Specimen-based mining has a saturation curve, not a compounding one. First 3-6 specimens discover architectural gaps. After that, you're adding examples to known categories (enrichment, not discovery). The signal: when you predict the next specimen will produce "more of the same," you've hit saturation. Stop mining, shift to Tier 3 field validation.

## Wiring Checklist

After creating any mined skill:
- [ ] Add cross-references to all skills that would benefit (grep for related triggers)
- [ ] Update this file's Mining Queue with the new skill name
- [ ] Consider a garden post if the insight is non-obvious
- [ ] Commit skill + wiring changes in same session

## Tracking Usage

Mined skills are only valuable if they get consulted. Track in `memory/decay-tracker.md` (same as MEMORY.md entries):
- When a mined skill is consulted in a session, log it
- If a skill hasn't fired after 4 weeks → either wiring is wrong (fix cross-references) or the skill isn't useful (demote or delete)
- Tier column in Completed Mines tracks provenance strength — Tier 1 (hold lightly), Tier 2 (consilium-tested), Tier 3 (field-validated)
- The specific source (which model, which council) doesn't matter — content either proves useful or it doesn't. Track the tier, not the genealogy.

## Completed Mines

| Topic | Skill | Tier | Wired to | Garden post |
|-------|-------|------|----------|-------------|
| Planning | `bouleusis` | 1 | rector, examen, topica | [Mining Your LLM](https://terryli.hm/posts/mining-your-llm) |
| Debugging | `diagnosis` | 1 | rector | — |
| Experimentation | `peirasmos` | 1 | peira, judex, examen, topica | [[The Persona Paradox in AI Agent Teams]] |
| Simplification | `parsimonia` | 1 | rector | — |
| Delegation | `mandatum` | 1 | rector | — |
| Evaluation | `kritike` | 1 | judex, peira | — |
| Heuristics | `praecepta` | 1 | topica, gnome, mandatum, consilium | "Delegation Is Delegation", "The Heuristic Library" |
| Wrap-ups | `conclusio` | 1 | legatum (inlined), eow, daily | — |
| Toddler school refusal | `parens` | 1 | — (vault: Theo - Development & Parenting Notes) | — |
| Truth-seeking | `zetetike` | 1 | fodina, elencho, consilium, peira, rector | — |
| Judgment | `phronesis` | 1 | consilium, gnome, examen, zetetike, rector, praecepta | — |
| Creativity | `poiesis` | 1 | brainstorming, rector, consilium, diagnosis | — |
| Systems thinking | `systema` | 1 | rector, diagnosis, phronesis, poiesis, zetetike | — |
| Communication | `hermenia` | 1 | cursus, storyteller, agoras, consilium, mandatum, meeting-prep | — |
| Learning | `mathesis` | 1 | dokime, rector, fodina, parens, eow, daily, phronesis | — |
| Self-awareness | `syneidesis` | 1 | phronesis, enkrateia, praecepta, all operations | — |
| Self-regulation | `enkrateia` | 1 | syneidesis, phronesis, sopor, kairos, mora, parens | — |
| Empathy | `sympatheia` | 1 | hermenia, mandatum, meeting-prep, cursus, phronesis, parens | — |
| Task management | `negotium` | 1 | sched, kairos, legatum, todo | — |
| AI governance consulting | `gubernatio` | 1 | rector, meeting-prep, capco-prep, consilium | "Governance Is a Tax" |
| Regulatory comparison | `regulatio` | 1 | meeting-prep, capco-prep, gubernatio | — |
| Technical credibility | `auctoritas` | 1 | meeting-prep, capco-prep, cursus, gubernatio | — |
| Agent team orchestration | `cohors` | 1 | copia, rector, mandatum, heuretes, opifex | — |
| Deployed system verification | `probatio` | 1 | verify, peira, topica | "The Pipeline Paradox" |
| Consulting communication | `relatio` | 1 | hermenia, meeting-prep, capco-prep, gubernatio, cursus, auctoritas, stilus | — |
| Representation shifting | `metanoia` | 1 (specimen) | diagnosis, poiesis, hermenia, topica, mimesis | — |
| Productive not-knowing | `aporia` | 1 (specimen) | syneidesis, zetetike, examen, phronesis, consilium, kritike | — |
| Extreme-case testing | `reductio` | 1 (specimen) | zetetike, peira, examen, aporia, topica | — |

## Relationship to Other Skills

- **artifex** — designs skills (structure, naming). fodina is specifically about *extracting knowledge from model weights* into skills.
- **consilium** — the engine for Tier 2 refinement. fodina tells you *when and how* to use it for knowledge extraction.
- **scrinium** — routes knowledge to the right layer. fodina always produces reference skills, not MEMORY.md or docs.
- **topica** — mental models catalog. Mined skills often feed new entries into topica.
