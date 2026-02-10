---
name: garp-quiz
description: GARP RAI exam quiz with adaptive focus on weak areas. "garp quiz", "quiz me", "rai quiz"
---

# GARP Quiz

Daily quiz skill for GARP RAI exam prep (Apr 4, 2026). Tracks mistakes, adapts focus toward weak areas.

## Trigger

- "garp quiz", "quiz me", "rai quiz", "study quiz"
- `/garp-quiz` or `/garp-quiz 5` (number = question count)

## Inputs

- **count** (optional): Number of questions. Default 5.
- **topic** (optional): Force a specific topic (e.g., "fairness", "M3", "XAI"). Default: adaptive.

## Workflow

### 1. Read Tracker

Read `~/notes/GARP RAI Quiz Tracker.md`. Parse:
- Per-topic error counts and rates
- Total stats
- Recent misses (last 10)

### 2. Pick Topic

**Adaptive selection** (unless topic forced):
- 60% chance: pick from weakest topics (highest error rate, minimum 2 attempts)
- 30% chance: pick from undertested topics (fewest attempts)
- 10% chance: random topic

Topic categories (map to exam modules):
- `M1-classical-ai`, `M1-ml-types`, `M1-ai-risks`
- `M2-data-prep`, `M2-clustering`, `M2-regression-classification`, `M2-neural-networks`, `M2-semi-rl`, `M2-model-eval`, `M2-nlp-genai`
- `M3-bias-unfairness`, `M3-fairness-measures`, `M3-xai`, `M3-autonomy-safety`, `M3-reputational-existential`, `M3-genai-risks`
- `M4-ethical-frameworks`, `M4-ethics-principles`, `M4-regulatory`
- `M5-data-governance`, `M5-model-governance`, `M5-model-risk-roles`, `M5-genai-governance`

### 3. Generate Question

Read the relevant raw content file for the chosen topic:
- `~/notes/GARP RAI Module 1 - Raw Content.md`
- `~/notes/GARP RAI Module 2 - Raw Content.md`
- `~/notes/GARP RAI Module 3 - Raw Content.md`
- `~/notes/GARP RAI Module 4 - Raw Content.md`
- `~/notes/GARP RAI Module 5 - Raw Content.md`

Also check `~/notes/GARP RAI Practice Exam.md` — if there's an unused practice exam question on the chosen topic, prefer using it (real exam questions > generated ones).

Generate ONE exam-style MCQ:
- Scenario-based where possible (the real exam is "practice oriented")
- 4 answer choices (A-D), one correct
- Distractor answers should be plausible (common misconceptions)
- Match the style/difficulty of the practice exam questions

### 4. Present via AskUserQuestion

Use `AskUserQuestion` with the question text as the `question` field and A-D as `options`.
- `header`: "Q{n}" where n is the session question number
- Each option's `description`: keep brief (the label carries the answer text)
- `multiSelect`: false

### 5. Evaluate & Explain

After the user answers:
- State **Correct** or **Incorrect** (with the right answer)
- Give a brief explanation (2-3 sentences max)
- If incorrect, highlight the key distinction they missed
- Reference the specific concept from the curriculum

### 6. Update Tracker

Append to `~/notes/GARP RAI Quiz Tracker.md`:
- Add entry to History table
- Update per-topic stats
- Update total stats
- If incorrect, add to "Recent Misses" section with the key concept

### 7. Loop or Finish

- If more questions remain in the requested count, go to step 2
- After last question, show session summary:
  - Score (e.g., "4/5 — 80%")
  - Weak areas identified
  - Suggest next focus area

## Tracker File Format

The tracker file (`~/notes/GARP RAI Quiz Tracker.md`) uses this structure:

```markdown
# GARP RAI Quiz Tracker

## Summary

| Metric | Value |
|--------|-------|
| Total Questions | 5 |
| Correct | 4 |
| Rate | 80% |
| Sessions | 1 |

## Topic Performance

| Topic | Attempts | Correct | Rate |
|-------|----------|---------|------|
| M3-fairness-measures | 2 | 1 | 50% |
| M3-bias-unfairness | 1 | 1 | 100% |
| M3-xai | 1 | 1 | 100% |
| M3-autonomy-safety | 1 | 1 | 100% |

## Recent Misses

| Date | Topic | Key Concept |
|------|-------|-------------|
| 2026-02-10 | M3-fairness-measures | Predictive rate parity = equal precision, NOT demographic parity |

## History

| Date | Topic | Result | Key Concept |
|------|-------|--------|-------------|
| 2026-02-10 | M3-bias-unfairness | OK | Historical bias vs sampling bias |
| 2026-02-10 | M3-fairness-measures | MISS | Confused demographic parity with predictive rate parity |
| 2026-02-10 | M3-xai | OK | LIME = local interpretable model |
| 2026-02-10 | M3-fairness-measures | OK | Demographic parity ignores correctness |
| 2026-02-10 | M3-autonomy-safety | OK | Three forms of opaqueness |
```

## Error Handling

- **If tracker file doesn't exist**: Create it with empty tables
- **If raw content file missing**: Fall back to practice exam questions or generate from glossary
- **If user wants to stop mid-session**: Save progress, show partial score

## Output

- Questions presented via `AskUserQuestion` (interactive MCQ UI)
- Results tracked in `~/notes/GARP RAI Quiz Tracker.md`
- Session summary in chat after final question

## Notes

- Keep explanations concise — this is a quiz, not a lecture
- Don't repeat the same question within a session
- Practice exam questions are gold standard — use them before generating new ones
- For generated questions, vary the question stems: "Which of the following...", "A bank is...", "An analyst is...", "Which statement correctly..."
- Weight toward M3/M4/M5 (focus modules, 55-75% of exam)
- Track the session's question count in a running variable, don't re-read tracker between questions
