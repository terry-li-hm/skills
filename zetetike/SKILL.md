---
name: zetetike
description: Truth-seeking methodology — source selection, sufficiency, and reconciliation before acting. Consult before fodina, elencho, consilium, or any knowledge-gathering task. Not user-invocable.
type: reference
disable-model-invocation: true
---

# Zetetike — The Art of Seeking

> *Zetetike (ζητητική): the method of inquiry. Selecting and sequencing knowledge sources to reach sufficient confidence before acting.*

Not "find all truth" — but "know enough to act well, and know what you don't know."

## The Eight Sources

| Source | Best for | Tool | Cost |
|--------|----------|------|------|
| **Mine LLM** | Tacit patterns, stable heuristics, cross-domain structure | fodina | Free, instant |
| **Research online** | Published practitioner knowledge, post-cutoff facts | elencho, WebSearch | Free, minutes |
| **Cross-domain analogy** | Novel framing, patterns from other fields | consilium, manual | Low, minutes |
| **Community / practitioners** | What people actually do (vs. what they publish) | forums, Discord, WebSearch | Low-medium |
| **Existing implementations** | How mature projects handle it in practice | code archaeology, GitHub | Medium, 30min+ |
| **Experiment** | "Does it work?" — any empirical question | peira, judex | High, hours |
| **Adversarial refinement** | Finding gaps in what you think you know | consilium, redarguo | Low, minutes |
| **Field use** | Whether theory survives contact with reality | retrospectives, docs/solutions | High, weeks |

## Source Selection: "What type of question is this?"

Ask this BEFORE choosing a source. The question type determines the best source:

| Question type | Example | Best source | Trap |
|---------------|---------|-------------|------|
| **Factual / verifiable** | "Does Gmail support label wildcards?" | Experiment > research > LLM | Trusting LLM on verifiable facts |
| **Tacit / pattern-based** | "What are the failure modes of agent-written tests?" | Mine LLM > practitioners > research | Skipping the mine, going straight to research |
| **Empirical** | "Does two-agent TDD catch more bugs?" | Experiment, always | Researching instead of testing |
| **Social / practice** | "What do teams actually do for agent QA?" | Community > research > LLM | Treating published best practices as ground truth |
| **Strategic / judgment** | "Should we build a CLI or keep it as skill steps?" | consilium > cross-domain > mine LLM | Deciding alone without challenge |
| **Novel / uncharted** | "How should we test agent-written code?" | Cross-domain analogy > mine LLM > research | Assuming someone has already solved it |

## Sequencing: Cheap Before Expensive

Default order: LLM mine → online research → community → cross-domain → experiment → field use.

**Override:** If the question is empirical, skip straight to experiment. Cheaper sources can't answer "does it work?" — they can only answer "should it work?"

**Adversarial refinement** is not a source — it's a quality pass. Run it after you have a draft from other sources, before committing.

## Sufficiency: When to Stop

| Signal | Meaning |
|--------|---------|
| Two independent sources converge | Probably enough for low-stakes decisions |
| Sources disagree | Need a third source, or invoke trutina |
| Single source, high stakes | Insufficient regardless of source quality |
| Each new source teaches something new | Keep going — you're still in discovery |
| Each new source confirms what you know | Stop — you're procrastinating, not learning |
| You're avoiding a source | That's probably the one you need |

**Persistence threshold:** Anything that will persist (skill, CLAUDE.md, solutions doc) needs a two-source minimum. One source is a hypothesis.

## Reconciliation: When Sources Conflict

Before invoking trutina, check:
1. **Same question?** Sources often disagree because they're answering different questions
2. **Shared provenance?** Two sources citing the same original study = one source, not two
3. **Recency?** For fast-moving domains, newer usually wins. For stable theory, age is irrelevant
4. **Disagreement is signal.** Two sources disagreeing tells you more than two agreeing — it reveals the boundary conditions

## Key Heuristics

- **"Am I learning or confirming?"** The moment you're confirming, stop gathering.
- **The source you're avoiding is probably the one you need.** Experiment feels expensive, so you research instead. Practitioners feel awkward, so you mine the LLM.
- **Cheap before expensive, but empirical trumps all.** If you can test it, test it.
- **Echo chambers compound.** LLM trained on the same blog posts you're searching — apparent multi-source agreement might be single-source echo.
- **Don't research what you can test. Don't test what you can look up. Don't look up what you already know.**

## Anti-Patterns

| Anti-pattern | What's happening | Fix |
|-------------|-----------------|-----|
| **Source defaulting** | Always using the same source (usually LLM or WebSearch) | Ask "what type of question?" first |
| **Premature closure** | "Two sources agree, done" without checking independence | Check for shared provenance |
| **Infinite regress** | Never confident enough, always one more source | Apply sufficiency signals above |
| **Authority worship** | Published > empirical, or big name > evidence | Weight by question type, not source prestige |
| **Research as procrastination** | Gathering feels productive, avoids the hard part (deciding/building) | "Am I learning or confirming?" |

## Wiring

Consult zetetike from:
- **fodina** — before mining, ask "is the LLM the right source for this?"
- **elencho** — before parallel research, ask "what type of question?"
- **rector Step 1** — the cerno/research step should be governed by source selection
- **consilium** — before deliberation, ensure sufficient raw material
- **peira** — experiment is a source; zetetike tells you when to skip cheaper sources and go straight to it
