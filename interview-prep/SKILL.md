---
name: interview-prep
description: Prepare for an upcoming interview by researching the company, pulling relevant stories, and matching experience to role requirements. Use when user says "prep for [company]", "interview prep", or has an interview scheduled.
---

# Interview Prep

Prepare for an upcoming interview by researching the company, pulling relevant stories, and matching experience to role requirements.

## Trigger

Use when:
- Terry has an interview scheduled
- User says "prep for [company]", "interview prep", "prepare for interview"

## Inputs

- **company**: Company name (required)
- **role**: Role title (required)
- **stage** (optional): Phone screen, hiring manager, technical, etc.
- **date** (optional): Interview date/time

## Workflow

1. **Read context files**:
   - `/Users/terry/notes/CLAUDE.md` — personal context
   - `/Users/terry/notes/Core Story Bank.md` — prepared stories (if exists)
   - `/Users/terry/notes/Interview Preparation.md` — general prep notes (if exists)
   - `/Users/terry/notes/Job Hunting.md` — notes on this role/company

2. **Run integrated skills** (in parallel where possible):
   - `/contact-prep` — If interviewer name known, surface relationship history
   - `/counter-intel` — Research interviewer background and style
   - `/narrative-debt` — Check what stories already told to this company

3. **Research company** via web search:
   - **Recent news** — last 3-6 months, anything notable
   - **Tech stack** — especially data/ML infrastructure
   - **Culture signals** — values, work style, reviews
   - **Key people** — who Terry might meet, their background
   - **Challenges** — problems they're likely solving

3. **Map role to experience**:
   | Role Requirement | Terry's Relevant Experience |
   |------------------|----------------------------|
   | [Requirement] | [Matching experience/story] |

4. **Select 3-5 stories** from Core Story Bank most relevant to this role
   - Cross-check with narrative debt log to avoid repetition
   - Prioritize stories NOT yet told to this company

5. **Generate 5-7 questions to ask** (tailored to research findings):
   - Role-specific (day-to-day, expectations, success metrics)
   - Team/culture (how team works, collaboration)
   - Company direction (strategy, challenges, growth)

6. **Flag potential concerns**:
   - Gaps or transitions to address
   - Why leaving current role (clean narrative)
   - Salary expectations if likely to come up
   - Red flags from research

7. **Review with Judge:**
   - Run prep output through `/judge` with `technical` criteria
   - Check: completeness, appropriate_depth, actionable
   - If verdict is `needs_work`: revise (max 2 iterations)
   - Ensures prep is comprehensive and interview-ready

8. **Save prep notes** to vault (optional)

## Integration

This skill integrates with:
- `/contact-prep` — Relationship context for known interviewers
- `/counter-intel` — Interviewer research and profile building
- `/narrative-debt` — Story consistency across interview rounds

After interview, prompt user for `/debrief` to capture signals.

## Error Handling

- **If Core Story Bank doesn't exist**: Note what stories Terry should prepare
- **If company info sparse**: Focus on role requirements and general prep
- **If interview is soon**: Focus on essentials; if days away, go deeper

## Output

**Template:**
```markdown
# Interview Prep: [Company] - [Role]

## Company Briefing
[Concise summary — recent news, tech stack, culture]

## Role Mapping
| Requirement | Your Experience |
|-------------|-----------------|

## Stories to Use
1. [Story name] — [why relevant]

## Questions to Ask
1. [Question]

## Watch Out For
- [Concern and how to address]

## Next Steps
- [Any prep actions before interview]
```

**Location:** `/Users/terry/notes/Interview Prep - [Company].md`

## Examples

**User**: "prep for Stripe"
**Action**: Research Stripe, map experience, select stories, generate questions
**Output**: Interview prep note saved to vault, summary in chat
