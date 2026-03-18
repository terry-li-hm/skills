---
name: sapor
description: Reference heuristics for taste-based model routing — when model capability affects output quality in ways prompts cannot specify. Consult from copia, cohors, rector, or any agent dispatch decision.
user_invocable: false
disable-model-invocation: true
---

# Sapor — Taste-Based Model Routing Heuristics

> *Sapor: Latin for "taste, discernment."*
> Mined via fodina Tier 1. Complements cohors (team structure) and the claude-model-guide (benchmarks). This file addresses the harder question: not which model scores higher, but **when the score difference shows up in your output.**

---

## 1. The Taste Boundary

The dangerous failure mode is not wrong output — that gets caught. It is **correct-but-wrong** output: right facts, wrong framing; complete but missing the point; technically accurate but tonally dead. A weaker model produces this when the task requires implicit judgment the prompt cannot fully specify.

### Task Properties That Predict Taste Failure

| Property | What happens with a weaker model | Example |
|---|---|---|
| **Audience-dependent framing** | Model optimises for generic reader, not the actual one | LinkedIn post aimed at HK banking executives reads like a Medium tutorial |
| **Omission as signal** | Model includes everything asked for but cannot judge what to leave out | Research brief buries the insight under comprehensive-but-flat coverage |
| **Register shifts within a piece** | Model locks into one register and cannot modulate | Consulting deck that needs gravitas in exec summary but accessibility in appendix |
| **Irony, understatement, or negative space** | Model plays it straight or over-explains | Jeeves-voice that becomes butler-cosplay instead of understated wit |
| **"When to break format"** | Model follows the template even when the content demands deviation | Bullet-point summary of something that needs a single devastating sentence |
| **Implicit prioritisation** | Model treats all inputs as equally important | Synthesis that gives equal weight to a throwaway mention and a core argument |
| **Calibrated confidence** | Model hedges uniformly or asserts uniformly | "May potentially" on established facts; no hedging on speculative claims |
| **Reading the room** | Model cannot infer social context from content cues | Drafting a follow-up email with the wrong urgency because it missed subtext |

### The Litmus Test

Before routing to Sonnet, ask: **"If this output is 90% right, will I notice the 10% that's off — or will it pass my review and embarrass me later?"**

- If you'd catch it (code that fails tests, facts you can verify, formats you can eyeball) → Sonnet is fine.
- If it would pass your review but fail with the actual audience (client reads it differently, LinkedIn post gets no engagement, email lands wrong) → Opus.

### The Specificity Paradox

You might think: "I'll just prompt more precisely." This works for some dimensions but not others.

**Promptable** (more detail in spec → better output from any model):
- Output structure (headings, length, format)
- Factual scope (include X, exclude Y)
- Explicit constraints (no jargon, active voice, ≤800 words)
- Mechanical transformations (summarise, translate, reformat)

**Prompt-resistant** (more detail in spec → diminishing returns or worse):
- When to violate the spec you just gave (the best outputs know when to break rules)
- Proportional emphasis (how much weight to give each point)
- What's interesting about the input (weak models summarise; strong models notice)
- Voice consistency under pressure (maintaining persona when content gets technical)
- Elegance (the difference between correct and good is not specifiable)
- Knowing when to stop (weak models pad; strong models end)

**The deeper principle:** prompt-resistant quality dimensions are those where the judgment about *what to do* cannot be separated from the act of *doing it*. You cannot tell a model "be elegant" any more than you can tell a writer "write well." The capability is architectural, not instructional.

---

## 2. Prompt-Resistant Quality Dimensions

These are output qualities that emerge from model capability and resist being engineered via prompt design.

### 2.1 Structural Judgment

The ability to choose the right structure for the content, not just fill a given structure.

- **Weak model:** follows the template faithfully. If the template says "3 sections," you get 3 sections even when the content naturally wants 2 or 5.
- **Strong model:** recognises when the template is wrong for this specific input and adapts.
- **Why it resists prompting:** you cannot enumerate in advance all the ways a template might be wrong. The judgment is case-specific.

### 2.2 Relevance Gradient

The ability to weight information by importance rather than by order of appearance or explicit labelling.

- **Weak model:** treats all inputs flatly. First item gets most space. Or: items explicitly marked "important" get space; everything else is treated equally.
- **Strong model:** infers importance from context, even when nothing is explicitly flagged. Gives a throwaway detail that happens to be pivotal more space than a comprehensively documented triviality.
- **Why it resists prompting:** you'd have to pre-digest the importance ranking yourself — at which point you've done the intellectual work and the model is just typing.

### 2.3 Tonal Calibration Under Constraint

Maintaining the right tone when the content fights the tone.

- **Weak model:** either drops the tone when content gets complex ("let me explain...") or maintains tone at the expense of clarity.
- **Strong model:** modulates — slightly more direct when explaining, returns to register for conclusions. The persona bends but doesn't break.
- **Why it resists prompting:** you cannot specify every inflection point. "Stay in Jeeves voice but be clearer when discussing technical architecture" is a spec that requires judgment at every sentence.

### 2.4 The Right Amount of Nothing

Knowing when to not say something.

- **Weak model:** fills all available space. If you say "800-1200 words," you get 1150. Asked for "3-5 recommendations," you get 5. Silence is not in the repertoire.
- **Strong model:** produces 600 words when that's what the content warrants, even within a 800-1200 range. Gives 2 recommendations when only 2 are strong, rather than padding to 3.
- **Why it resists prompting:** you can set ceilings but not teach restraint. "Only include strong recommendations" presupposes the model can judge strength — which is the capability gap.

### 2.5 Error Recovery in Context

When the model makes a wrong move mid-generation, can it course-correct?

- **Weak model:** commits to initial framing. If it starts a paragraph wrong, it finishes the paragraph wrong and compensates later (or doesn't).
- **Strong model:** mid-sentence pivots are invisible in the final output. The internal reasoning catches drift before it reaches the surface.
- **Why it resists prompting:** you cannot prompt for "if you start going the wrong way, stop." The model either has the meta-awareness or it doesn't.

---

## 3. The Delegation Tax

Splitting work across agents introduces costs beyond token spend. These are the hidden taxes.

### 3.1 Context Loss Tax

Every delegation boundary is a lossy compression point. The orchestrator understands why the work matters; the delegate sees only the spec.

| Context type lost at delegation | Impact | Mitigation |
|---|---|---|
| **Why this matters** (strategic context) | Output optimises for spec compliance, not actual goal | Include one sentence: "this will be used for X by audience Y" |
| **What was already tried** | Agent re-explores dead ends | List failures explicitly: "we already tried X; it failed because Y" |
| **Taste preferences** (voice, emphasis) | Output is generic | Reference file: "match the style of /path/to/example.md" |
| **Adjacent constraints** (what other agents are producing) | Outputs don't compose | Wiring instructions: "agent B is producing X; your output must integrate with it at boundary Z" |

**The compounding problem:** each delegation hop loses ~15-25% of intent fidelity. Two hops (orchestrator → lead → worker) can lose 30-45%. This is why hierarchical teams need strong leads — the lead must reconstruct intent, not just relay instructions.

### 3.2 Scope Mismatch Tax

The orchestrator decomposes the problem one way; the agent would have decomposed it differently. The mismatch creates dead zones (things neither party handles) and overlaps (things both handle, differently).

**Symptoms:**
- Agent output answers a question you didn't quite ask
- Agent ignores something "obviously" in scope (it wasn't obvious from the spec)
- Agent produces excellent work on the wrong axis

**Heuristic:** if you find yourself wanting to say "no, I meant..." after reading agent output, you paid the scope mismatch tax. The fix is spec quality, not model quality — but a stronger model is more forgiving of ambiguous specs because it infers intent.

### 3.3 Integration Tax

N independent outputs rarely compose into a coherent whole without merge work. This tax is paid by the orchestrator or lead and is proportional to:

- **Stylistic variance** across agents (multiplied by whether a human will read the merged output)
- **Structural incompatibility** (agents chose different structures for parallel content)
- **Redundancy** (agents independently produced overlapping content that must be deduplicated)

**When delegation tax exceeds parallelism gain:**

| Scenario | Delegate | Do it yourself |
|---|---|---|
| 5 independent research briefs on different topics | Yes — near-zero integration tax | No |
| One coherent 3000-word essay | No — integration of fragments is harder than writing it | Yes |
| 10 code files in isolated modules | Yes — tests verify integration | No |
| One code file requiring deep architectural understanding | No — context transfer cost exceeds coding cost | Yes |
| Draft that needs Terry's voice | No — voice cannot be delegated, only approximated | Yes (or: delegate research, write yourself) |

**Rule of thumb:** delegate when outputs are **additive** (more is better, combine by concatenation). Do it yourself when outputs are **integrative** (the whole must be coherent, combination requires judgment).

---

## 4. Compound Judgment — Where Weak Steps Corrupt the Chain

In multi-step tasks, quality doesn't degrade linearly. Some positions in the chain are force-multipliers for error.

### 4.1 The Corruption Points

| Position | Risk level | Why |
|---|---|---|
| **Problem framing** (step 1) | Critical | A wrong frame propagates through every subsequent step. If step 1 misunderstands what "governance framework" means in this context, steps 2-5 are flawless work on the wrong problem. |
| **Synthesis / integration** (final step) | Critical | The last step determines what the human sees. A weak synthesis can make strong inputs look weak. A strong synthesis can rescue mediocre inputs. |
| **Filtering / selection** (any step that decides what to keep) | High | Selection is taste — and taste failures are invisible until the audience reacts. A weak model filters by surface relevance; a strong model filters by importance. |
| **Execution** (middle steps — collect, format, transform) | Low | These are verification-friendly. Wrong execution gets caught by tests, schemas, or spot checks. |
| **Research / collection** (early steps) | Low-Medium | Missing something is worse than including too much, but collection can be verified by coverage checks. The risk is subtle: a weak model collects the obvious and misses the non-obvious. |

### 4.2 The Asymmetry

**A strong first step + weak middle steps + strong final step** dramatically outperforms **uniform medium-capability steps.** This is the Opus-Sonnet-Opus sandwich and it is the structurally correct team topology.

- **Opus frames the problem:** decides what to research, how to decompose, what "good" looks like
- **Sonnet executes:** collects, formats, implements, transforms — following the frame
- **Opus synthesises:** reads all outputs, selects what matters, produces the final artifact

The worst topology is **Sonnet frames → Opus executes.** You're paying premium tokens for execution (where Sonnet ties) while getting commodity judgment on the framing (where Opus leads by 43 Arena Elo).

### 4.3 Contamination Heuristics

| Signal that a weak step contaminated downstream | What to do |
|---|---|
| Final output is comprehensive but unsurprising | Framing step was too literal — it asked the obvious questions |
| Final output answers the stated question but misses the real question | Framing step lacked the context to infer intent |
| Research is thorough but synthesis feels thin | Synthesis step couldn't distinguish signal from noise in the research |
| Multiple agents produced similar outputs despite different briefs | Decomposition step created overlapping scopes |
| Output is good prose but wrong emphasis | Selection/filtering step treated importance as binary (in/out) rather than weighted |

---

## 5. Routing Decision Framework

### The Quick Check (before dispatching any agent)

```
1. Will a human read this without editing?
   YES → taste matters → Opus for generation, or at minimum Opus for final pass
   NO  → only correctness matters → Sonnet

2. Does the task require deciding what to do, or just doing it?
   DECIDING → Opus (framing, selection, synthesis, architecture)
   DOING    → Sonnet (implementation, collection, formatting)

3. Could I write a rubric that fully captures "good" for this task?
   YES → Sonnet can follow rubrics
   NO  → the un-rubricable remainder is taste → Opus

4. If the output is subtly wrong, when will I find out?
   IMMEDIATELY (tests, review, verification) → Sonnet
   TOO LATE (audience reaction, missed opportunity, embarrassment) → Opus
```

### The Compound Task Pattern

For multi-step work, don't route the whole task to one tier. Route by step:

```
Frame the problem          → Opus (or human)
Decompose into tasks       → Opus (with cohors heuristics)
Execute tasks              → Sonnet (parallel, verified)
Filter / select / rank     → Opus
Synthesise into deliverable → Opus
Verify correctness          → Sonnet (mechanical checks)
Polish for audience         → Opus (only if human reads without editing)
```

### What This Means for Existing Skills

| Skill | Step that needs taste | Routing implication |
|---|---|---|
| **copia** prospecting | Scoring candidates (Value × Autonomy × Compound) | Opus prospectors are correct — scoring is judgment |
| **copia** execution | Research collection vs synthesis | Collection → Sonnet. Synthesis → Opus. Already in copia but worth reinforcing. |
| **rector** decomposition | Deciding scope and acceptance criteria for delegates | Opus. A wrong decomposition wastes every downstream token. |
| **cohors** merge | Combining N agent outputs into coherent artifact | Opus lead. Sonnet cannot judge what to keep from competing outputs. |
| **consilium** | Entire flow | Opus throughout — every step is judgment |
| **sarcio** garden posts | Draft generation | Opus if zero-touch publish. Sonnet + human review if Terry edits before posting. |
| **delegate** code tasks | Writing the spec vs writing the code | Spec = taste (Opus). Code = execution (Sonnet/Gemini/Codex). |

---

## 6. Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| **"Opus for everything"** | Burns quota on tasks where it adds no value. Sonnet ties on execution benchmarks. | Route by step, not by task. |
| **"Sonnet + detailed prompt"** | Prompts hit diminishing returns on taste dimensions. More detail → more rigidity → worse output when the content needs flexibility. | Accept that some quality is architectural, not instructional. Use Opus for those steps. |
| **"Opus for first draft, Sonnet to refine"** | Refining requires taste — knowing what to change. Sonnet "refines" by following explicit instructions, not by noticing what's off. | Opus for both draft and refine, or Sonnet draft → Opus refine (but not the reverse). |
| **"Let the model pick its own difficulty"** | Models don't self-report capability gaps accurately. Sonnet will attempt taste-dependent tasks without flagging that it's operating outside its strength. | Routing is the orchestrator's job, not the agent's. |
| **"Same model for consistency"** | Sacrifices quality for stylistic uniformity. Better: different models for different cognitive demands, Opus lead for consistency pass. | Consistency is a merge problem, not a routing problem. |

---

## Cross-References

- **cohors** — team structure, parallelism, merge patterns (structural decisions)
- **claude-model-guide** (`~/docs/solutions/claude-model-guide.md`) — benchmarks, pricing, speed (quantitative basis)
- **mandatum** — spec quality, delegation theory (the other half of the delegation tax)
- **copia** — autonomous work menu (consumes sapor for model routing within burns)
- **rector** — on-ramp that should consult sapor before choosing model tier for delegates
