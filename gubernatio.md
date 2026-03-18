---
name: gubernatio
description: AI governance consulting heuristics for financial services — what clients care about, how assessments create value, credibility signals, failure modes. Reference skill consulted by rector, meeting-prep, capco-prep, consilium when engagement involves governance.
disable-model-invocation: true
---

# Gubernatio — AI Governance Consulting Heuristics

> Mined via fodina Tier 1. Field-validate over first Capco engagements.

## Core Reframe

Governance is a tax. The consultant's job is to minimize the tax while achieving the risk objective. Clients don't want governance — they want to deploy AI without getting hurt. Frame everything as enabling, not constraining.

## Key Distinctions

| Looks similar | Actually different | Why it matters |
|---|---|---|
| Governance vs. ethics | Governance = risk management + regulatory readiness. Ethics = principles + values. | Lead with governance. Ethics follows if needed. Leading with ethics loses the room. |
| Policy vs. operationalization | Every bank has an AI policy. Almost none can demonstrate compliance. | The gap between document and practice is where 80% of engagement value lives. |
| Model risk vs. AI risk | MRM (SR 11-7) = individual models. AI governance = the system: pipelines, deployment, monitoring, vendor deps, feedback loops. | MRM teams are natural allies. Extend their muscle memory, don't replace it. |
| Inventory vs. assessment | Inventory = what do we have? Assessment = how risky is it? | Inventory first. Always. Without it, assessment is fiction. |
| Framework adoption vs. framework mapping | Adoption = implement NIST/ISO wholesale. Mapping = use existing framework vocab to organize what you already do. | Mapping is 5x faster and clients accept it. Adoption is a multi-year program. |

## What Each Stakeholder Actually Buys

| Stakeholder | Real concern | What they'll fund | Anti-pattern |
|---|---|---|---|
| CRO | No regulatory findings, no surprises | Gap assessment, exam readiness, board reporting | Don't pitch innovation — pitch protection |
| CDO/CTO | Don't block AI deployment, show innovation + control | Governance framework that's lightweight enough to not slow teams | Don't pitch heavy process — pitch proportional controls |
| Board | "Can we say we have AI governance if asked?" | Board-ready dashboard, policy + evidence package | Don't go deep technical — they need the 1-pager |
| Business lines | Don't slow us down | Pre-approved use-case templates, fast-track classification | Don't pitch governance TO them — make governance invisible |
| MRM/validation | Scale existing discipline to AI/ML without more headcount | Tooling, templates, classification that maps to SR 11-7 tiers | Don't treat them as the problem — they're the solution under-resourced |

## The Assessment Playbook

**Ordering: what to do first, second, third.**

1. **Inventory** — what AI/ML exists? Include shadow AI (LLMs, copilots, spreadsheet models, vendor-embedded AI). This alone justifies the engagement.
2. **Classify by risk** — not all AI is equal. Use-case + data sensitivity + autonomy level → risk tier. EU AI Act classification is useful even outside EU — regulators like risk-based.
3. **Map to existing controls** — what's already governed via MRM, data governance, vendor management? The delta is smaller than clients expect.
4. **Gap analysis on the delta** — what's genuinely ungoverned? Usually: GenAI usage, third-party AI, business-unit experiments.
5. **Prioritize by regulatory exposure** — what would the examiner ask about first?
6. **Operationalize top gaps** — not a 50-slide framework. Working processes: intake form, risk classification tool, monitoring dashboard.

**Default with override:** Always start with inventory. Override only when the client has a regulatory exam in <3 months — then start with gap analysis on what the regulator will ask.

## Credibility Signals

**What separates "AI consultant who can talk" from "AI consultant who can build":**

- **Lead with failures, not frameworks.** "Here's what I've seen go wrong" beats "Here's the NIST AI RMF" every time.
- **Translate fluently.** Same concept, three versions: board (1 sentence), CRO (risk framing), engineering (technical specifics). Do this live.
- **Know the regulatory landscape cold.** Not just your jurisdiction — know MAS, HKMA, APRA, EU comparisons. Cross-border is where generalists drown.
- **Build things.** A working inventory tool in a spreadsheet beats a 50-slide governance framework deck. Demonstrate you can operationalize, not just advise.
- **Name the model.** If a client says "we use AI for credit scoring" — ask which model, what features, what validation was done, what monitoring exists. Technical specificity = instant credibility.
- **Know what governance is in disguise.** Half of "AI governance" problems are actually procurement, vendor management, data quality, or change management wearing an AI hat. Name it.

## Failure Modes (Anti-patterns)

| Smell | What's happening | Fix |
|---|---|---|
| Framework shopping | Recommending NIST/ISO without knowing what client already has | Map first, adopt later |
| Boil the ocean | Trying to govern everything at once | Prioritize by regulatory exposure, not completeness |
| Paper tiger | Beautiful policy documents nobody follows | Operationalize one process end-to-end before writing the next policy |
| Tech-blind governance | Policies written by people who can't read the code | Pair governance consultant with ML engineer on every assessment |
| Governance theater | Doing it for the regulator, not for actual risk | Ask "would this catch the problem?" not "would this satisfy the examiner?" |
| Permanent assessment | Engagement that never transitions from assessing to building | Time-box assessment to 4-6 weeks. After that, you're building or you're stalling. |
| Innovation theater | Governance framed as "enabling responsible AI innovation" with no concrete output | Deliverables, not decks. Working tools, not frameworks. |

## If-Then Triggers

- **If client says "we need an AI governance framework"** → ask what triggered this. Regulatory exam? Board question? Incident? The trigger tells you what they actually need.
- **If MRM team exists and is competent** → build on their processes. Extension, not replacement.
- **If MRM team doesn't exist** → the engagement just tripled in scope. Flag this early.
- **If client has >100 models** → inventory is a project, not a task. Scope accordingly.
- **If client says "we don't use AI"** → they do. They just don't call it AI. Look for: ML in fraud detection, NLP in complaints, vendor tools with AI inside, Excel models that are effectively ML.
- **If the engagement is post-incident** → governance is now a remediation exercise. Different tone, different urgency, different stakeholder dynamic.

## The MRM Bridge (Spectrum)

Financial services is unique: MRM discipline already exists. The question is how far to extend it.

```
Pure MRM extension ←————————→ Greenfield AI governance
(faster, familiar,              (comprehensive, future-proof,
 misses system-level risks)      slow, unfamiliar, adoption risk)
```

**Default:** Start MRM-adjacent (classification, validation, monitoring) and expand scope incrementally. Override: if the regulator has specifically asked for AI-specific governance beyond MRM, go greenfield from the start.

## Consulting Opportunities (Where the Money Is)

Ranked by client willingness to pay × urgency:

1. **Regulatory exam prep** — immediate, high urgency, clear scope
2. **GenAI policy + guardrails** — board is asking, everyone's nervous
3. **AI inventory + classification** — foundational, large scope, recurring
4. **MRM extension to ML/AI** — natural evolution, MRM teams are buyers
5. **Third-party AI risk** — vendors embedding AI everywhere, nobody's governing it
6. **Cross-border regulatory mapping** — regional banks need this, few can do it well
