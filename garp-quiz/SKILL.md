---
name: garp-quiz
description: GARP RAI exam quiz with adaptive focus on weak areas. "garp quiz", "quiz me", "rai quiz"
user_invocable: true
model: sonnet
---

# GARP Quiz

Daily quiz skill for GARP RAI exam prep (Apr 4, 2026). Tracks mistakes, adapts focus toward weak areas.

**Model: Sonnet.** This is a formulaic skill (read → generate MCQ → evaluate → update). Opus is overkill — save it for judgment calls.

## Trigger

- "garp quiz", "quiz me", "rai quiz", "study quiz"
- `/garp-quiz` or `/garp-quiz 5` (number = question count)

## Inputs

- **count** (optional): Number of questions. Default 5.
- **topic** (optional): Force a specific topic (e.g., "fairness", "M3", "XAI"). Default: adaptive.

## Workflow

### 1. Read Tracker

**File check:** If ~/notes/GARP RAI Quiz Tracker.md does not exist, tell the user: 'No quiz tracker found. Run a first quiz session to create it — I will initialize the tracker after your first question.' Then proceed with the quiz using default equal weights for all topics (skip spaced repetition for the first session).

Read `~/notes/GARP RAI Quiz Tracker.md`. Parse:
- Per-topic error counts and rates
- Total stats
- Recent misses (last 10)
- Spaced repetition schedule (interval + next due date per topic)

### 2. Pick Topic

**Spaced repetition selection** (unless topic forced):

Priority order:
1. **Overdue topics** — any topic where `next_due ≤ today`, sorted by most overdue first. Among equally overdue, prefer lower success rate.
2. **Undertested topics** — topics with 0 attempts (never scheduled). Weight toward M3/M4/M5.
3. **Random** — if nothing is due and all topics have been tested, pick randomly from topics whose next_due is soonest.

Within a single session, avoid picking the same topic twice unless all due topics have been used.

**Session composition guard:** Cap weak topics (≤50% success rate) at **3 out of 5** questions per session. Fill remaining slots with consolidation topics (>50%). This prevents demoralizing all-weak sessions.

**Same-day cooldown:** Do not retest a topic that was already tested earlier the same day, even across sessions. Spaced repetition needs sleep — same-day retests only measure short-term recall.

**Interval progression (simplified SM-2):**
- **MISS** → interval resets to **1 day**
- **OK** → interval doubles: 1 → 2 → 4 → 8 → 14 (capped at 14 days given exam proximity)
- New topics start at interval **1** after first attempt

Topic categories (map to exam modules):
- `M1-classical-ai`, `M1-ml-types`, `M1-ai-risks`
- `M2-intro-tools`, `M2-data-prep`, `M2-clustering`, `M2-econometric`, `M2-regression-classification`, `M2-semi-supervised`, `M2-neural-networks`, `M2-semi-rl`, `M2-model-estimation`, `M2-model-eval`, `M2-nlp-traditional`, `M2-nlp-genai`
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

**Token efficiency:** Don't read entire module files. Use Grep to find the relevant section heading, then Read with `offset`/`limit` to pull only the ~30-50 lines needed for that topic. For a 5-question session across 2-3 modules, read the TOC (first 30 lines) once per module to locate sections, then targeted reads only.

Also check `~/notes/GARP RAI Practice Exam.md` — if there's an unused practice exam question on the chosen topic, prefer using it (real exam questions > generated ones).

Generate ONE exam-style MCQ:
- Scenario-based where possible (the real exam is "practice oriented")
- 4 answer choices (A-D), one correct
- Distractor answers should be plausible (common misconceptions)
- Match the style/difficulty of the practice exam questions

### 4. Present via AskUserQuestion

Use `AskUserQuestion` with the question text as the `question` field and A-D as `options`.
- `header`: "Q{n}" where n is the session question number
- Each option's `description`: minimal and non-revealing — must not define the concept or give away the answer. Use generic filler like "Select if this is correct" or omit meaningful detail entirely. The label carries the answer text.
- `multiSelect`: false

**Confidence check:** After the user answers, use a second `AskUserQuestion`:
- `header`: "Confidence"
- `question`: "Were you confident in that answer?"
- Options: "Confident" / "Guessing"
- `multiSelect`: false

This affects spaced repetition scoring (see Step 6).

### 5. Evaluate & Explain

After the user answers:
- State **Correct** or **Incorrect** (with the right answer)
- Give a brief explanation (2-3 sentences max)
- If incorrect, highlight the key distinction they missed
- Reference the specific concept from the curriculum
- Check `~/notes/GARP RAI Trap Patterns.md` — if this miss matches an existing pattern, name it (e.g., "This is the 'conditioning on prediction vs truth' trap again")

**Key Concept quality matters** — the History table's Key Concept column doubles as study material. Write each entry as a mini-flashcard with the precise distinction, not a vague description:
- Bad: "Confused fairness measures"
- Good: "Equal opportunity = TPR only. Equalized odds = TPR + TNR. Predictive rate parity = precision."
- Bad: "Wrong about model governance roles"
- Good: "Board sets risk appetite (not model risk function). 3rd line audits the validators."

For correct answers, still capture the core insight — it reinforces retention on review.

### 6. Update Tracker

Update `~/notes/GARP RAI Quiz Tracker.md` **using Edit tool** (surgical edits, not full file rewrites):
- Edit the Summary table (total, correct, rate, sessions)
- Edit the specific Topic Performance rows that changed
- Edit the specific Spaced Repetition Schedule rows that changed
- Append new entries to History table
- If incorrect, append to "Recent Misses" table (cap at 10 entries — drop oldest when exceeding)
- **Spaced Repetition Schedule (confidence-aware):**
  - MISS → set interval to 1, next_due to tomorrow
  - OK + Confident → double the current interval (cap at 14), set next_due to today + new interval
  - OK + Guessing → interval stays at 1, next_due to tomorrow (lucky guess doesn't advance mastery)
  - New topic (no schedule row yet) → add row with interval based on result
- **History table:** Record result as `OK`, `OK-GUESS`, or `MISS` to distinguish confident vs lucky correct answers

**Token efficiency:** Use Edit to modify specific table rows, not Write to rewrite the entire file. The tracker grows over time — full rewrites waste tokens proportional to history length.

### 6b. Update Trap Patterns

If any session misses reveal a **new thinking pattern** (not just a repeat of an existing one), append to `~/notes/GARP RAI Trap Patterns.md` under the appropriate section — or create a new section. Keep entries as mnemonics/decision rules, not verbose explanations.

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

## Spaced Repetition Schedule

| Topic | Interval | Next Due |
|-------|----------|----------|
| M3-fairness-measures | 1 | 2026-02-11 |
| M3-bias-unfairness | 2 | 2026-02-12 |
| M3-xai | 2 | 2026-02-12 |
| M3-autonomy-safety | 2 | 2026-02-12 |

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

## Mode Selection

Choose mode based on topic accuracy:

- **< 50% accuracy:** Use **definition drill mode** (free recall, no MCQ). Present the term, user types what they remember, compare against source. MCQ lets users pattern-match from options — free recall forces actual retrieval and gives honest signal on knowledge gaps. Reference: `~/notes/GARP RAI Definition Drills.md`.
- **>= 50% accuracy:** Use **MCQ quiz mode** (standard AskUserQuestion flow). Tests under exam-like conditions once definitions are solid.

Progression: drill until user can recite definitions cold → then switch to MCQ to test under pressure.

## Notes

- Keep explanations concise — this is a quiz, not a lecture
- Don't repeat the same question within a session
- Practice exam questions are gold standard — use them before generating new ones
- For generated questions, vary the question stems: "Which of the following...", "A bank is...", "An analyst is...", "Which statement correctly..."
- Weight toward M3/M4/M5 (focus modules, 55-75% of exam)
- Track the session's question count in a running variable, don't re-read tracker between questions
- **Run `/compact` between sessions** if doing multiple sessions in one conversation — context snowballs
- **One session = one conversation** is ideal; batch sessions waste tokens on accumulated context
- **Study strategy:** Frontier council + evidence-based research in `~/notes/GARP RAI Study Strategy - Council.md`
