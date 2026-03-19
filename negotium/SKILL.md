---
name: negotium
description: Task routing and attention allocation heuristics — Due vs TODO vs calendar vs let-it-go. Consult from sched, kairos, legatum, or any task-routing decision.
disable-model-invocation: true
tags: reference, task-management, mined
---

# Negotium — Task Management Heuristics

> *Negotium: Latin "business, task" — the thing that demands your care.*

Reference skill. Mined from model weights (Tier 1, 2026-03-18). Consult when routing tasks to Due, TODO, calendar, or the void.

## The Core Reframe

The question is NOT "how important is this?"

It's: **"What happens if I forget, and to what?"**

Importance is a feeling. Consequence of forgetting is testable. Route by consequence, not by gut.

## The Routing Filters

Run in order. Each filter narrows the routing decision.

### Filter 1: Am I committed?

**Committed** = signed, promised, scheduled, or someone is depending on me.
**Uncommitted** = exploring, considering, keeping options open.

**Rule:** Uncommitted paths get no push notifications. Ever. Optionality on an uncommitted path is not urgency — it's comfort disguised as diligence.

**Signal:** If you catch yourself saying "I should follow up just in case" on something you haven't committed to — that's optionality hoarding, not task management.

### Filter 2: Reactive-safe or proactive-required?

**Reactive-safe** = if this matters, someone will contact me. I can respond when triggered.
**Proactive-required** = if I don't initiate, the opportunity/obligation silently expires.

**Rule:** Reactive-safe tasks need no tracking at all unless you've committed (Filter 1). Don't build systems to remind yourself about things that will remind you.

**Examples:**
- Job interview follow-up when you've signed elsewhere → reactive-safe, drop it
- Tax filing deadline → proactive-required, nobody will chase you until it's too late
- Friend's birthday → proactive-required (they won't remind you)
- Client responded to your email → reactive-safe (it's in your inbox)

### Filter 3: What's the consequence of forgetting?

| Consequence | Route to |
|-------------|----------|
| Damage to a committed path (missed deadline, broken promise, financial loss) | **Due** (push) or **Calendar** (time-blocked) |
| Missed optionality on an uncommitted path | **Nothing** — let it go |
| Slow decay but no cliff (refactor, habit, nice-to-have) | **TODO.md** (pull) |
| Compounding value (the longer you wait, the more it costs) | **Do it now** |

**The Due test (tightened):** Would forgetting this cause damage to something I've chosen? If yes → Due. If it only costs unchosen optionality → drop or TODO at most.

### Filter 4: Push or pull?

Only after passing Filters 1-3 do you decide push vs pull.

| System | Mechanism | Attention cost | Use when |
|--------|-----------|---------------|----------|
| **Due** | Push notification | High — interrupts morning focus | Forgetting = damage to commitment. Needs specific timing. |
| **Calendar** | Time-blocked | Medium — visible in day view | Appointment with others, or work requiring a specific slot |
| **TODO.md** | Pull (checked by `/kairos`) | Low — only surfaces when you look | Persistent, no cliff, do-whenever |
| **Nothing** | — | Zero | Reactive-safe + uncommitted, or not worth tracking cost |

**Rule:** Morning attention is the scarcest resource. What you put in Due determines what captures your best hours. Guard that channel ruthlessly.

### Filter 5: The 2-minute override

If routing the task takes longer than doing it → just do it. This overrides all filters.

## Failure Modes

### Optionality hoarding
Keeping doors open as emotional comfort, not strategic value. Feels responsible ("what if?"). Costs attention on every review cycle. **Test:** If the door closed tomorrow and you'd shrug, you're hoarding.

### Priority inversion via notification
Due items feel more urgent than TODO items regardless of actual importance, because push > pull. Putting a low-stakes item in Due hijacks your morning with something that doesn't deserve it.

### Sunk cost routing
"I already invested 3 interviews in this, so I should follow up." Past investment should not drive forward routing. The only question is: does the future path justify the tracking cost?

### Zombie tasks
Items re-snoozed or re-read 3+ times without action. Either not important enough (delete) or not concrete enough (rewrite with a verb and a specific next action). **Rule:** Third snooze = delete or rewrite. No fourth chance.

### System as procrastination
Organising, re-routing, and refining task lists instead of executing. The task system should take <2 min/day to maintain. If you're spending more, you're avoiding the work.

### Routing anxiety
Spending more energy deciding where to put a task than the task would take. **Default:** if unsure, TODO.md. It's the lowest-commitment option that still captures the item. Upgrade to Due only with clear justification.

## The Attention Budget

You can hold ~3 active priorities. Everything else is either:
- In a system (Due, TODO, calendar) and trusted to surface when needed
- Dropped — explicitly decided not to track

If your active list exceeds 3, you're not prioritising — you're listing. Force-rank and push the rest to pull systems.

## Decay Profiles

Match routing to how the task ages:

| Profile | Behaviour | Route |
|---------|-----------|-------|
| **Cliff** | Worthless after date X (filing deadline, event RSVP) | Due with specific date |
| **Decay** | Loses value gradually (follow-up window, networking intro) | TODO with `due:` if committed, else drop |
| **Stable** | Same value whenever (refactor, learn a skill, read a book) | TODO, no date |
| **Compound** | Gets harder/costlier the longer you wait (tech debt, health) | Do now or scheduled recurring |

## Principles

1. **Every tracked item has carrying cost.** Tracking is not free. Be ruthless about what earns a slot.
2. **The best task system has fewer items, not more.** Capture is cheap; attention is expensive.
3. **"Let it go" is a valid routing decision.** Most systems have no explicit "don't do this" path. Build one.
4. **Route by forward value, not past investment.** Sunk costs are sunk.
5. **Push notifications are attention interrupts.** Treat them like you'd treat someone tapping your shoulder at your desk. Would this warrant that?
