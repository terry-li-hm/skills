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

- **count** (optional): Number of questions. Default varies by phase (see below).
- **topic** (optional): Force a specific topic (e.g., "fairness", "M3", "XAI"). Default: adaptive.

## Phased Schedule

Session length and format shift based on exam proximity. Check the date and apply the right phase.

| Phase | Dates | Default count | Format | Cadence |
|-------|-------|--------------|--------|---------|
| **1: Cruise** | Now → Mar 13 | 5-10Q | Due topics from `rai due` + consolidation. Rapid-fire rounds for label-swap areas. | 3x/week, ~15-20 min |
| **2: Ramp** | Mar 14 → Mar 28 | 15Q | Mixed MCQ sets. One 40Q practice exam mid-phase. | 5x/week, ~30 min |
| **3: Peak** | Mar 29 → Apr 3 | 20Q | Two timed 80Q mocks. Kill-list drill on remaining weak spots. No new material last 72hr. | Daily, ~45 min |

**M1/M2 minimum quota:** Regardless of phase, at least **30% of weekly questions must be M1/M2 topics.** These are 25-45% of the exam — over-drilling M3-M5 risks a silent fail on technical content.

## Workflow

### 1. Read Tracker + Prime Recent Misses

**File check:** If ~/notes/GARP RAI Quiz Tracker.md does not exist, tell the user: 'No quiz tracker found. Run a first quiz session to create it — I will initialize the tracker after your first question.' Then proceed with the quiz using default equal weights for all topics (skip spaced repetition for the first session).

Read `~/notes/GARP RAI Quiz Tracker.md`. Parse:
- Per-topic error counts and rates
- Total stats
- Recent misses (last 10)
- Spaced repetition schedule (interval + next due date per topic)

**Prime the brain:** Before the first question, show the user their last 3-5 misses from the Recent Misses table with the Key Concept column. Format as a quick reminder block:

```
**Recent misses to watch for:**
- LIME = local, SHAP = marginal contribution (Feb 16)
- Equal opportunity = TPR, not predictive rate parity (Feb 16)
- Elastic Net = L1+L2 combined, not LASSO (Feb 16)
```

This costs 2 seconds and prevents the same label-swap errors from recurring. Skip if the user has no recent misses or says "skip priming."

### 2. Pick Topic

**Use the `rai` CLI to check what's due:**
```bash
~/scripts/rai.py due
```
This shows overdue topics sorted by priority, new/untested topics, and suggested session composition. Use its output to pick topics instead of manually parsing the tracker.

**If the CLI is unavailable**, fall back to manual selection:
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
- `M4-ethical-frameworks`, `M4-ethics-principles`, `M4-bias-discrimination`, `M4-privacy-cybersecurity`, `M4-governance-challenges`, `M4-regulatory`
- `M5-data-governance`, `M5-model-governance`, `M5-model-risk-roles`, `M5-model-dev-testing`, `M5-model-validation`, `M5-model-changes-review`, `M5-genai-governance`

### 3. Generate Question

Read the relevant source material for the chosen topic. **Priority order:**

1. **End-of-chapter review questions:** `~/notes/GARP RAI Review Questions.md` — official GARP questions with answers. Prefer these over generated questions. Can adapt them into MCQ format by turning the answer + plausible wrong alternatives into options.
2. **Practice exam:** `~/notes/GARP RAI Practice Exam.md` — real exam-style questions (if unused for this topic).
3. **Raw content files** (for generating new questions):
   - `~/notes/GARP RAI Module 1 - Raw Content.md`
   - `~/notes/GARP RAI Module 2 - Raw Content.md`
   - `~/notes/GARP RAI Module 3 - Raw Content.md`
   - `~/notes/GARP RAI Module 4 - Raw Content.md`
   - `~/notes/GARP RAI Module 5 - Raw Content.md`

**Token efficiency:** Use `~/scripts/rai.py source TOPIC` to pull relevant source material in one command. It searches the correct module file and returns the matching section(s). Supports fuzzy matching (e.g., `rai source fairness`). Only fall back to manual Grep + Read if the CLI output is insufficient.

**M2 label-swap risk:** For M2 topics, generate MCQ distractors that test terminology confusion (e.g., Ridge vs LASSO vs Elastic Net, self-training vs co-training, normalization vs standardization). These are the highest-value questions — the user's intuitions are correct but label swaps cause errors under pressure.

Generate ONE exam-style MCQ:
- Scenario-based where possible (the real exam is "practice oriented")
- 4 answer choices (A-D), one correct
- Distractor answers should be plausible (common misconceptions)
- Match the style/difficulty of the practice exam questions

### 4. Present Question

**MCQ mode (>= 70% accuracy):**

Use `AskUserQuestion` with the question text as the `question` field and A-D as `options`.
- `header`: "Q{n}" where n is the session question number
- Each option's `description`: minimal and non-revealing — must not define the concept or give away the answer. Use generic filler like "Select if this is correct" or omit meaningful detail entirely. The label carries the answer text.
- `multiSelect`: false

**Scenario free-recall mode (50-69% accuracy):**

Present the scenario as a chat message ending with a bolded question (e.g., **"Which fairness measure, and why?"**). The user types their answer — no AskUserQuestion, no options to select from. Evaluate their typed response for correctness.

**Definition drill mode (< 50% accuracy):**

Present the term/concept as a chat message (e.g., "What is Ridge Regression and what does it do to coefficients?"). User types what they recall. Compare against source and fill gaps.

**No confidence menu.** Infer confidence from the answer itself — don't interrupt flow with AskUserQuestion after every question. See Step 6 for rating inference rules.

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

Use the `rai` CLI (`~/scripts/rai.py`) to record results. This handles FSRS scheduling, markdown tracker updates, and history in one call.

```bash
~/scripts/rai.py record TOPIC RATING
```

**Rating inference (no menu — infer from answer quality):**
- **MISS** (wrong answer) → `again`
- **OK but brief/incomplete** (got the concept but missing key details) → `hard`
- **OK solid** (correct with adequate detail) → `good`
- **OK instant/detailed** (clearly knew it cold, fast + precise) → `easy`

**Example Bash calls:**
```bash
~/scripts/rai.py record M3-fairness-measures again
~/scripts/rai.py record M2-semi-rl good
```

Run one `record` call per question. The CLI updates both the FSRS state (JSON) and the markdown tracker (summary, topic performance, history) in a single operation.

**After the last question in a session**, also increment the Sessions count in the tracker manually (the CLI doesn't track session boundaries):
- Edit the Summary table: `Sessions` += 1

**Spaced repetition schedule rows in the markdown are now informational only** — the FSRS JSON state (`~/notes/.garp-fsrs-state.json`) is the source of truth for scheduling. The markdown Spaced Repetition Schedule table no longer needs to be maintained.

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

- **MCQ mode:** Questions via `AskUserQuestion` (interactive UI)
- **Free-recall mode:** Questions as chat messages, user types answer
- **Definition drill:** Terms as chat messages, user types recall
- **Mock exam:** All MCQ via `AskUserQuestion`, debrief at end
- Results recorded via `~/scripts/rai.py record TOPIC RATING` (updates FSRS + markdown tracker)
- Session summary in chat after final question

## Mode Selection

Choose mode based on topic accuracy:

- **< 50% accuracy:** Use **definition drill mode** (free recall, no MCQ). Present the term, user types what they remember, compare against source. MCQ lets users pattern-match from options — free recall forces actual retrieval and gives honest signal on knowledge gaps. Reference: `~/notes/GARP RAI Definition Drills.md`.
- **50-69% accuracy:** Use **scenario free-recall mode**. Present a scenario, user types the answer and reasoning — no MCQ options. This forces retrieval without the crutch of pattern-matching from options. Still use the confidence check afterward. Score as OK/MISS based on whether the user identified the correct concept and gave valid reasoning.
- **>= 70% accuracy:** Use **MCQ quiz mode** (standard AskUserQuestion flow). Tests under exam-like conditions once retrieval is solid.

Progression: definition drill → scenario free-recall → MCQ. Each mode builds on the previous.

**Rapid-fire mode (any accuracy, triggered manually or after label-swap misses):**

Trigger: user says "rapid fire", or after 2+ label-swap misses in the same session on related concepts (e.g., mixing up fairness measures, regularization types, XAI techniques).

Format: Present a one-line description, user names the concept. No MCQ options, no scenario — pure term recognition. 5-8 questions in rapid succession, no recording to FSRS (this is reinforcement, not assessment). Example:

```
**R1.** Equal true positive rates across groups?
> Equal opportunity

**R2.** L1 penalty, can zero out coefficients?
> LASSO

**R3.** Local, model-agnostic, fits simple model around one prediction?
> LIME
```

After the rapid-fire round, resume normal mode. If user gets all correct, the labels are locked in. If misses persist, note in trap patterns file.

**Why 70% not 50%:** Session on 2026-02-16 showed that MCQ at 50-69% enables pattern-matching that masks weak retrieval. Free-recall caught the gap — user went 8/10 on free-recall scenarios after failing the MCQ version of the same topic.

## Topic Graduation Criteria

A topic is "graduated" (safe to deprioritise) only when BOTH conditions are met:
1. **≥85% accuracy over the last 20 questions** on that topic
2. **FSRS state = Review** with interval ≥ 8 days

A topic is "red" (daily until fixed) when:
- **<70% accuracy** over last 10 questions, OR
- **Missed twice in 7 days** on the same concept

Red topics get scheduled every session until they hit 5 consecutive correct answers under time.

## Decision Rules

After each session, apply these automatically:
- **Timed set <75%** → next session is 100% remediation on missed topics (no new topics)
- **Average >3 min/question** on timed set → next session is speed drill (15Q at 90 sec/question, forced answer, then review)
- **Topic missed twice in 7 days** → becomes daily item until cleared

## Timed Mock Exam Mode

Trigger: `/garp-quiz mock` or "mock exam", "timed quiz"

Simulates exam conditions for readiness testing. Use when overall accuracy is >70% and exam is <3 weeks away.

### Rules

- **20 questions, 30 minutes.** State the clock at the start: "30 minutes starts now. I'll track time."
- **All MCQ** — regardless of topic accuracy. The exam is MCQ, so mock must be too.
- **Mixed topics** — random selection weighted toward M3/M4/M5 (exam weighting). No two consecutive questions from the same module.
- **No explanations during the mock.** Just "Noted." after each answer. Explanations come in the debrief.
- **Track time:** After every 5 questions, state elapsed time and questions remaining.
- **At 30 minutes:** Stop wherever you are. Unanswered questions count as MISS.

### Debrief

After the mock (or at 30 min cutoff):
1. Show score: "14/20 — 70%"
2. List all misses with brief explanations
3. Identify weakest module in this mock
4. Compare to overall tracker rate — improving or declining?
5. Update tracker with all results (batch update at end, not per-question)

### Readiness Signal

- **>= 80% on two consecutive mocks** → exam-ready, shift to maintenance mode (1 session every 3 days)
- **60-79%** → continue daily sessions, focus on missed topics
- **< 60%** → drop back to free-recall/drill mode, not ready for mock yet

---

## Key Files

- **Prep plan:** `~/notes/GARP RAI Exam Prep.md` — phased schedule, exam weights, confirmed weak spots, study strategy
- **Quiz tracker:** `~/notes/GARP RAI Quiz Tracker.md` — per-topic stats, history, recent misses
- **FSRS state:** `~/notes/.garp-fsrs-state.json` — source of truth for spaced repetition scheduling
- **Review questions:** `~/notes/GARP RAI Review Questions.md` — official end-of-chapter questions with answers (all 5 modules)
- **Practice exam:** `~/notes/GARP RAI Practice Exam.md` — 40Q official practice exam
- **Trap patterns:** `~/notes/GARP RAI Trap Patterns.md` — recurring mistake patterns
- **Raw content:** `~/notes/GARP RAI Module {1-5} - Raw Content.md`
- **CLI:** `~/scripts/rai.py` (run via `uv run --script`) — `due`, `record`, `stats`, `topics`

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
