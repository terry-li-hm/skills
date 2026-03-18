---
name: mimesis
description: Cross-domain analogical transfer — apply patterns from biology, physics, economics, or other domains to find gaps in your systems. Consult when stuck on a design problem, reviewing architecture, or when a metaphor surfaces naturally in conversation. NOT for brainstorming features (use brainstorm) or mining LLM knowledge (use fodina).
user_invocable: false
---

# Mimesis — Analogical Transfer

*Mimesis* (Greek: imitation, representation) — finding structure in one domain and applying it to another.

Not metaphor as decoration. Metaphor as engineering tool. When you say "this system needs an immune response," you're not being poetic — you're identifying a specific structural gap (sensor without memory) that the source domain has already solved.

## When to consult

- A metaphor surfaces naturally in conversation ("this is like inflammation")
- A system has a recurring problem that resists direct fixes
- You're reviewing architecture and want fresh angles
- Topica models feel too abstract — you need a richer source domain

## The process

### 1. Choose the source domain

Not randomly. Match the domain to the *type* of complexity:

| Your system's property | Source domain | Why |
|---|---|---|
| Many agents, emergent behaviour | **Biology** (ecology, immunology) | Evolution solved multi-agent coordination |
| Feedback loops, oscillation | **Control theory** (engineering) | PID controllers, damping, stability |
| Scarce resources, competing actors | **Economics** (markets, game theory) | Allocation under constraint |
| Cascading failures, resilience | **Ecology** (food webs, keystone species) | Interdependence and collapse |
| Information flow, signal/noise | **Neuroscience** | Attention, filtering, salience |
| Growth, compounding, limits | **Physics** (thermodynamics) | Entropy, energy, phase transitions |
| Trust, reputation, coordination | **Political science** | Institutions, governance, legitimacy |
| Sequential decisions under uncertainty | **Military strategy** | OODA loops, fog of war |

Biology is the richest source for complex adaptive systems because it's had 4 billion years of R&D on exactly these problems. Physics is simpler (few rules, clean math) — use it when your system actually IS simple. Most interesting systems aren't.

### 2. Map concepts explicitly

Write a table. Don't hand-wave.

```
| Source (biology)      | Target (my system)           |
|-----------------------|------------------------------|
| Immune memory         | Skill trigger map            |
| Inflammation          | Hook fire log                |
| Homeostasis           | Tier 1 auto-fix              |
| Pain signal           | Tier 2 surfacing             |
| Conscious decision    | Tier 3 human-only            |
| Chronic inflammation  | Rule that fires without learning |
```

The discipline of writing the table forces precision. "It's like the immune system" is vague. The table tells you exactly which component maps to what.

### 3. Find where the metaphor breaks

This is where the value lives. For each row in the mapping table, ask:

- **Does my system have this component?** If not — that's a gap to consider filling.
- **Does my system have something the source domain doesn't?** That's a potential over-engineering signal.
- **Where does the analogy NOT hold?** That's the boundary of the metaphor's usefulness. Don't force it past this point.

### 4. Build only what the gap analysis justifies

Not everything in the source domain needs a target equivalent. The question is: does filling this gap solve a problem I actually have?

**Good:** "Biology has immune memory; my hooks don't learn between sessions. The fire rate should trend down but doesn't. → Add a reconciler."

**Bad:** "Biology has DNA replication; my system should have self-replicating configs." (No actual problem solved.)

## Rich source domains for AI tooling

Based on what's worked:

### Biology
- **Immune system** → self-healing, memory, tiered response (auto-fix/detect/escalate)
- **Homeostasis** → steady-state maintenance, negative feedback loops
- **Ecology** → niche competition between tools, keystone dependencies
- **Evolution** → variation/selection/retention for iterating on prompts or configs
- **Circadian rhythm** → time-gated processes, daily/weekly cycles

### Economics
- **Opportunity cost** → choosing which task to automate (cost of NOT automating)
- **Diminishing returns** → when to stop optimising (5th post in a session)
- **Market signals** → usage data as price signals for skill investment

### Control theory
- **PID controllers** → proportional response to drift (don't overcorrect)
- **Damping** → preventing oscillation in feedback loops
- **Dead zones** → intentional insensitivity to noise (don't alert on trivial)

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| **Decorative metaphor** | "Our system is like a garden" with no structural mapping → poetic but useless |
| **Forced completeness** | Trying to map every concept in the source domain → over-engineering |
| **Wrong domain** | Using physics (simple rules) for a complex adaptive system → false precision |
| **Metaphor lock-in** | Refusing to abandon the analogy when it stops generating insights |

## Output

The output of a mimesis session is either:
1. **A gap list** — specific components your system lacks that the source domain has (and that solve real problems)
2. **A garden post** — if the analogy is rich enough to be worth sharing
3. **Both** — build the gaps, publish the insight

## Calls
- `topica` — mental models catalog (mimesis is the generative process; topica is the lookup)
- `fodina` — mines LLM knowledge (different input; mimesis mines structural analogies from domains)
- `gyrus` — flywheel design pattern (the primary output of today's biology → engineering mimesis)
