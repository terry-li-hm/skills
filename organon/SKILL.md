---
name: organon
description: Truth-seeking toolkit router — selects the right epistemic tool for getting ground truth. Consult when facing uncertainty, before deliberating, or when ground truth would resolve a question faster than opinions. Not user-invocable.
user_invocable: false
---

# Organon — Truth-Seeking Toolkit

From Aristotle's *Ὄργανον* — the instruments of thought. Routes to the right epistemic tool when you need ground truth rather than opinions.

**Not user-invocable.** Consulted internally by consilium, gnome, kairos, and any judgment-heavy task when evidence would resolve the question faster than deliberation.

## The Core Principle

> **Before deliberating, ask: can this be resolved empirically?** If yes, reach for the right instrument. Opinions are cheap; evidence compounds.

## Routing Table

| You need... | Route to | What it does |
|-------------|----------|--------------|
| "What are peers/competitors actually doing?" | **specula** | Scan peer implementations, extract transferable patterns, route to domains |
| "Do multiple sources agree on this fact?" | **elencho** | Parallel search across all tools, synthesise agreements/disagreements |
| "These sources contradict — which to trust?" | **trutina** | Conflicting evidence reconciliation, evidence weighting |
| "Can I just test this instead of debating?" | **judex** | Empirical validation — run both, measure, pick winner |
| "Can I run a controlled experiment?" | **peira** | Autonomous experiment-optimize loop for measurable targets |
| "What am I assuming without checking?" | **examen** | Premise audit — surface and test load-bearing assumptions |
| "What does the model already know implicitly?" | **fodina** | LLM knowledge mining — extract implicit knowledge into heuristics |
| "What pattern from another domain applies here?" | **mimesis** | Cross-domain analogical transfer (biology → systems, etc.) |

## Decision Flow

```
Facing uncertainty?
├─ Is the answer measurable?
│  ├─ Can run both options → judex
│  ├─ Can run controlled experiments → peira
│  └─ Need to check facts → elencho
├─ Do I have conflicting evidence?
│  └─ trutina
├─ Am I making assumptions?
│  └─ examen
├─ Could another domain have solved this?
│  └─ mimesis
├─ What are others in this space doing?
│  └─ specula
└─ Model knows this but surfaces it inconsistently?
   └─ fodina
```

## Anti-Pattern

Reaching for **consilium** (deliberation) when any organon tool would give a faster, more reliable answer. Deliberation is for genuine judgment calls where evidence is unavailable or ambiguous. If evidence exists or can be gathered — gather it first, deliberate on what remains.

## Companion Skills

- **topica** — mental models catalog (thinking *lenses*, not evidence-gathering *tools*)
- **indago** — web search tool selection (a sub-routing for the search step within elencho/specula)
- **consilium** — deliberation (reach for this *after* organon when evidence alone doesn't resolve)
