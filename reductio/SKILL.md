---
name: reductio
description: Extreme-case testing — push variables to limits, invert, pre-mortem, reductio ad absurdum. Consult when evaluating a rule, design, or strategy — test at the boundaries before trusting the middle. NOT for experimentation (use peira) or truth-seeking method (use zetetike).
user_invocable: false
disable-model-invocation: true
tags: [reference, cognition, mined]
---

# Reductio — Extreme-Case Testing

> *Reductio: Latin — leading back to the limit, testing by pushing to extremes.*

Rules, designs, and strategies are tested at their boundaries, not their centres. Push one variable to its limit and watch what breaks. The break IS the insight.

## The Core Move

Take the thing you're evaluating. Push one dimension to an extreme — zero, infinity, worst case, best case, absurd case. If it breaks, you've found a boundary condition. If it holds, you've found robustness. Either way, you know more than the middle case told you.

## Heuristics

**Gedankenexperimente.** (Einstein) Respect known constraints, push ONE variable to an extreme, look for the paradox. "What would you see riding a beam of light?" The paradox reveals where the theory is incomplete. Don't push multiple variables — isolate one. [Type: rule]

**Inversion.** (Munger, Jacobi) "Tell me where I'm going to die so I won't go there." Instead of asking "how do I succeed?" ask "how would I guarantee failure?" Then avoid those paths. Avoidance is more reliable than achievement. [Type: reframe]

**Premeditatio malorum.** (Stoicism) Systematically imagine the worst outcome before it happens. Not pessimism — inoculation. Pre-experiencing loss reduces its power AND surfaces contingencies you wouldn't have planned for. Pre-mortems > post-mortems. [Type: checklist]

**Reductio through extreme cases.** (Talmud) Push a rule to its absurd limit to test if it holds. "If this applies to X, does it also apply to Y?" If the extreme case produces absurdity, the rule needs refinement. This is Gedankenexperimente from a legal tradition — convergent discovery. [Type: if-then trigger]

**Boundary-zone danger.** (Munger — circle of competence) The most dangerous position isn't ignorance — it's the boundary where you know enough to be confident but not enough to be right. Test your confidence at the edges. [Type: signal]

## When to Consult

- Evaluating a rule or policy — does it hold at the extremes?
- Designing a system — what happens at 0 users? At 10M users?
- Making a strategy — what's the failure mode? What guarantees failure?
- Feeling confident about a plan — test at the boundary of your knowledge
- Pre-mortem time — before committing, enumerate how it dies

## Anti-Patterns

- **Testing only comfortable extremes.** Push toward the uncomfortable cases — the ones you hope won't happen. Those are the informative ones.
- **Extreme-case paralysis.** The point is to find boundaries, not to prove everything fails. Most things survive most extremes. Note the break points and proceed.
- **Pushing multiple variables at once.** Isolate one. Multivariate extremes are uninterpretable.

## Cross-References

- `zetetike` — truth-seeking includes extreme-case testing; reductio isolates this specific move
- `peira` — experimentation runs real tests; reductio runs mental ones
- `examen` — premise audit uses extreme cases as one tool; reductio is the full toolkit
- `aporia` — knowing what you don't know; reductio is one method for discovering the boundaries of your knowledge
- `topica` — inversion is already a mental model in topica; reductio provides the full practice
