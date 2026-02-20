---
name: capco-drill
description: Capco readiness drill — daily articulation practice for HSBC engagement. "capco drill", "drill me", "readiness drill"
user_invocable: true
model: haiku
---

# Capco Readiness Drill

Daily active recall for articulating AI governance concepts, HSBC context, regulatory landscape, and consulting delivery patterns before Capco start (Mar 16 / Apr 8).

**Model: Haiku.** Simple randomization + self-rating — cheapest model is fine.

## Trigger

- "capco drill", "drill me", "readiness drill"
- `/capco-drill` or `/capco-drill 5` (number = question count, default 3)

## Data

- **Questions:** `~/notes/Capco/Capco Readiness Drill.md` — 40 numbered questions in 7 categories (A-G)
- **State:** `~/notes/Capco/.capco-drill-state.json` — drill history and ratings
- **Reference:** Questions link to source material in `~/notes/Capco/` — read if user asks "what's the answer?"

## Workflow

### 1. Load State

Read `~/notes/Capco/.capco-drill-state.json`. If it doesn't exist, create it:

```json
{
  "drills": {},
  "sessions": 0,
  "last_session": null
}
```

Where `drills` maps question numbers (strings) to:
```json
{
  "last_drilled": "2026-02-21",
  "rating": "shaky",
  "times_drilled": 2
}
```

### 2. Pick Questions

Select N questions (default 3) using this priority:

1. **Never asked** — questions with no entry in `drills` (pick randomly)
2. **Rated "blank"** — couldn't articulate at all (highest priority for repeat)
3. **Rated "shaky"** — partial articulation, needs practice
4. **Least recently drilled** — among "confident" questions, pick the oldest
5. **Random** — if all questions are recently drilled and confident

Ensure no two questions from the same category (A-G) in one session when possible.

### 3. Present Questions

Read the question bank file. For each selected question:

1. Show the **category letter and question number** (e.g., "**B.8**")
2. Show the **full question text**
3. Say: "Answer out loud, then rate yourself: confident / shaky / blank"

Present **one at a time**. Wait for the user's self-rating before showing the next question.

**Do NOT provide the answer.** This is active recall, not a quiz with feedback. If the user explicitly asks "what's the answer?" or says they're stuck, then read the relevant source material and give a model answer.

### 4. Record Rating

After the user self-rates each question, update the state:

```json
{
  "last_drilled": "2026-02-21",
  "rating": "confident",
  "times_drilled": 3
}
```

Valid ratings: `confident`, `shaky`, `blank`

### 5. After Last Question

Update `sessions` count and `last_session` date in state. Save state file.

Show a brief summary:
```
Session 4 done. 2 confident, 1 shaky.
Shaky: B.8 (regulatory developments)
Next weak spot to revisit: F.30 (agentic frameworks)
```

If all 40 questions have been drilled at least once, congratulate and suggest reviewing the shaky/blank ones.

## Error Handling

- **If question bank file missing:** Tell user to check `~/notes/Capco/Capco Readiness Drill.md`
- **If state file corrupt:** Delete and recreate empty state
- **If user gives a rating not in (confident/shaky/blank):** Map synonyms — "good"/"solid"/"yes" → confident, "ok"/"partial"/"sort of" → shaky, "no"/"nothing"/"skip" → blank

## Notes

- Keep it brisk. No lectures, no elaborate feedback. This is a 5-minute morning drill.
- If the user says "rapid fire" — present all questions at once, user rates in batch
- Self-rating is the point. Don't second-guess the user's rating.
- This skill expires when Capco engagement starts (real work replaces practice). Delete after Day 1.
