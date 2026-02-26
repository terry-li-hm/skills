---
name: consulting-prep
description: Daily consulting readiness drill — scenarios, reading prompts, observation logging. "consulting prep", "prep drill", "consulting drill"
user_invocable: true
model: sonnet
---

# Consulting Prep

Daily practice skill for building consulting mental models before Capco start. Three modes based on day of week. ~15 minutes per session.

**Data:** `~/notes/Career/Consulting Readiness Program.md` (master program, reading list, scenario bank)
**State:** `~/notes/Career/.consulting-prep-state.json` (progress tracking)
**Log target:** Today's daily note at `~/notes/Daily/YYYY-MM-DD.md`

**Expires:** When Terry starts at Capco (Mar 16 or Apr 8). After that, suggest switching to the live observation format described in the program note.

## Trigger

- "consulting prep", "consulting drill", "prep drill"
- `/consulting-prep`

## Workflow

### 1. Check State & Determine Mode

Read the state file. If it doesn't exist, initialise it:

```json
{
  "readings_completed": [],
  "scenarios_completed": [],
  "sessions": 0,
  "last_session": null
}
```

Determine today's mode from day of week:
- **Mon / Wed / Fri** → Read & Extract
- **Tue / Thu** → Scenario Practice
- **Sat / Sun** → User's choice (offer both, or skip)

Show a one-line status: `Session #N | Readings: X/15 | Scenarios: Y/10 | Mode: [today's mode]`

### 2A. Read & Extract Mode (Mon/Wed/Fri)

1. Read the program note's reading list
2. Pick the next unread item (sequential order)
3. **If it's a book:** Give a 2-3 paragraph summary of the key concepts relevant to Terry's situation. Focus on one actionable principle.
4. **If it's a search topic:** Run a web search, find the best piece, summarise in 2-3 paragraphs.
5. After presenting the material, ask Terry:

```
What's the one principle you'd take from this?
And how does it apply to HSBC specifically?
```

6. Wait for Terry's response. Don't judge it — this is extraction practice, not a quiz.
7. Log to daily note and update state.

### 2B. Scenario Practice Mode (Tue/Thu)

1. Read the program note's scenario bank
2. Pick a scenario Terry hasn't done recently (prioritise unplayed, then least recent)
3. Present the scenario. Set the scene in 2-3 sentences — make it vivid enough to feel real.

```
🎯 Scenario #N: [title]

[2-3 sentence scene-setting. Put Terry in the room.]

What do you do?
```

4. Wait for Terry's response (his instinct).
5. After he responds, do THREE things:

   **a. Acknowledge what's good about his instinct.** Don't just correct — the instinct often has something right.

   **b. Name the gap.** What would the Career Principles frameworks suggest differently? Reference the specific principle (doctor model, defend the problem, private preview test, etc.)

   **c. Ask one follow-up question** that forces him to go deeper:
   - "What question would you ask before doing that?"
   - "Who in the room might feel threatened by that move?"
   - "What's the version of this that makes [stakeholder] look good?"

6. Wait for follow-up response, then close with a one-line takeaway.
7. Log to daily note and update state.

### 3. Log & Close

**Daily note entry** (append under a `## Consulting Prep` heading):

For Read & Extract:
```markdown
## Consulting Prep
📖 [title/source]
→ Principle: [Terry's extraction]
→ HSBC application: [Terry's application]
```

For Scenario Practice:
```markdown
## Consulting Prep
🎯 Scenario #N: [title]
→ My instinct: [summary of Terry's response]
→ Gap: [what the frameworks suggest]
→ Takeaway: [one line]
```

**Update state file:**
- Add reading/scenario to completed list
- Increment session count
- Update last_session date

**Close with:**
- If both readings and scenarios are progressing well: one encouraging line, no fluff
- If a pattern is emerging across sessions (e.g., consistently jumping to solutions): name it directly
- Remind of any GARP RAI quiz due today (check `~/scripts/rai.py today`)

### 4. Observation Prompt (Every Session)

Before closing, regardless of mode:

```
👁️ Quick check: did you notice anything today about listening, selling,
   power dynamics, or pushback — in any interaction, not just work?
```

If Terry has something, log it. If not, move on — don't force it.

## Scenario Bank

Stored in the program note. If Terry exhausts all 10, generate new ones based on:
- Patterns from his actual HSBC prep (Capco Transition note, First 30 Days)
- Emerging weak areas from previous sessions
- Escalating difficulty (early scenarios are simpler dynamics, later ones combine multiple principles)

## Notes

- **Sonnet is fine.** This is structured prompting, not judgment-heavy work.
- **Keep it under 15 minutes.** If Terry is going deep, that's fine — but don't prompt for more than one reading or one scenario per session.
- **Don't lecture.** The Career Principles note has the frameworks. Reference them, don't repeat them.
- **Track patterns across sessions.** If Terry's instinct consistently jumps to building/fixing before asking, name that trend explicitly by session 3-4.
- **This skill expires.** Once Capco starts, suggest retiring it and switching to the live observation log format in the program note.
