---
name: systema
description: Systems thinking — feedback loops, delays, leverage points, emergent properties. Consult when side effects surprise you, when a fix makes things worse, or when "and then what?" matters. Not user-invocable.
type: reference
disable-model-invocation: true
---

# Systema — Seeing the Whole

> *Systema (σύστημα): an organised whole. Seeing relationships, feedback loops, and second-order effects — the behaviour of the system is not the sum of its parts but the product of their interactions.*

Analysis takes things apart. Systems thinking sees how the parts interact when assembled.

## Five Tools

### 1. Feedback Loops

Two types. Most people see the reinforcing loop and miss the balancing one.

- **Reinforcing** (growth or collapse): More users → more content → more users. More bugs → more patches → more complexity → more bugs.
- **Balancing** (stability): More features → more complexity → fewer users → pressure to simplify. Thermostat: too hot → cooling → temperature drops → heating.

**Heuristic:** Every growth story has a balancing loop. If you can't find it, you're not looking hard enough.

### 2. Stocks and Flows

What accumulates (stock) vs what moves (flow).

- Bank balance = stock. Income and expenses = flows.
- Technical debt = stock. Feature pressure = inflow. Refactoring = outflow.
- Trust = stock. Reliability = inflow. Broken promises = outflow.

**Heuristic:** Most people try to fix stocks by changing flows without understanding the delay between them.

### 3. Delays

The time between cause and effect. Source of most bad decisions.

- "We hired 10 people, why isn't productivity up?" — 3-month onboarding delay.
- "We launched the feature, why no growth?" — adoption delay.
- "I started exercising, why don't I feel better?" — physiological delay.

**Heuristic:** When results don't match expectations, ask "where's the delay?" before concluding the intervention failed.

### 4. Leverage Points

Where a small change produces large effects. Donella Meadows' hierarchy (weakest → strongest):

| Level | Example | Leverage |
|-------|---------|----------|
| Parameters | Adjusting a threshold | Weakest — tuning knobs |
| Buffers | Increasing inventory / slack | Low |
| Structure | Reorganising who reports to whom | Medium |
| Rules | Changing incentives | High |
| Goals | Redefining what success means | Higher |
| Paradigms | Shifting the mental model | Strongest — but hardest |

**Heuristic:** Most interventions are at the parameter level (weakest). Ask "what level am I intervening at?" — then look one level up.

### 5. Emergent Properties

Behaviour that exists at the system level but not in any component.

- Consciousness from neurons. Culture from individuals. Traffic jams from cars.
- You can't understand the system by studying the parts in isolation.
- You can't fix emergent problems by fixing individual components.

**Heuristic:** If the problem persists after fixing every component, the problem is in the interactions, not the components.

## The One Question

**"And then what?"**

The simplest systems thinking tool. Ask it three times after any proposed action:

1. "We'll add a cache" → And then what? → "Reads get faster"
2. And then what? → "More users hit the cache" → And then what?
3. "Cache invalidation becomes the bottleneck"

Three rounds usually surfaces the second-order effect that first-order thinking misses.

## Failure Modes

| Failure | What's happening | Fix |
|---------|-----------------|-----|
| **Seeing systems that aren't there** | Imposing feedback narratives on simple cause-effect | Not everything is a system. Check if the "loop" actually feeds back. |
| **Everything connects** | Analysis paralysis from refusing to draw boundaries | Draw the boundary explicitly. The boundary IS the model. |
| **Ignoring the parts** | Using "it's a system" as excuse not to understand details | The system is made of parts. The parts matter. |
| **Over-abstracting** | "Complex adaptive system" explains everything and nothing | Name the specific loops, stocks, and delays. |
| **Intervening at the wrong level** | Tuning parameters when structure is the problem | Meadows' hierarchy — look one level up. |

## Wiring

Consult systema from:
- **rector** — before planning, ask "what are the second-order effects of this architecture?"
- **diagnosis** — when a fix makes things worse, look for the balancing loop you disrupted
- **phronesis** — judgment about where to intervene (parameters vs structure vs goals)
- **poiesis** — systems thinking reveals constraints that drive creative solutions
- **zetetike** — "and then what?" applied to knowledge gathering — what happens after you learn this?
