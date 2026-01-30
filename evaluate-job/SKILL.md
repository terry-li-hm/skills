---
name: evaluate-job
description: Evaluate LinkedIn job postings for fit. This skill should be used when the user shares a LinkedIn job URL and wants analysis of whether to apply. Triggers on LinkedIn job links, "evaluate this role", or requests to analyze job fit.
---

# Evaluate Job

Analyze LinkedIn job postings against user's background, current pipeline health, and career criteria. Output a recommendation (APPLY/CONSIDER/PASS) with structured reasoning.

## Workflow

1. **Navigate to job posting:**
   - **OpenClaw:** Use `browser` tool → `snapshot` or `screenshot` to read the page
   - **Claude Code:** Use Chrome extension (`profile="chrome"`) or `web_fetch`
   - **Fallback:** `mcporter call tavily.tavily-extract urls='["URL"]'`
   - Extract: company name, role title, requirements, responsibilities, preferred qualifications, salary if disclosed, applicant stats

   **Why browser over fetch for LinkedIn:**
   - Fetch/extract misses **applicant stats** (count, seniority breakdown) — requires being logged in
   - Browser sees the full page as logged-in user, including competition metrics
   - Can click "Show more" to expand full JD if needed

   **Extraction tip:** `read_page` captures the full accessibility tree including content below the viewport — no scrolling needed. Just navigate, wait 2 seconds for load, then `read_page` once to get the complete JD.

2. **Check for duplicates** (before full analysis):
   - Search vault for existing note matching company + role (e.g., `[[*Role* - *Company*]]`)
   - Check [[Job Hunting]] "Applied Jobs" and "Passed On" sections for the company name
   - If match found:
     - Show user what was found (existing note, application status, date)
     - Ask: "Already evaluated/applied to [match]. Proceed with analysis anyway?"
     - If user says no, stop early — no further analysis needed
   - This prevents duplicate work and catches related roles at the same company

3. **Load context files** (can run in parallel with step 1) — Check user's CLAUDE.md for background, credentials, differentiators, current situation, and job hunting status

4. **Analyze fit** across dimensions (see Fit Dimensions below)

5. **Factor pipeline health:**
   - **Healthy** (5+ active, interviews scheduled): Maintain standards — PASS on poor fits
   - **Thin** (<5 active, no interviews): Lower bar — CONSIDER "good enough" roles
   - Consider urgency of user's situation when weighing trade-offs

6. **Check for red flags** (feedback loop from `/debrief`):
   - Review [[Job Hunting]] → Market Signals for relevant patterns:
     - **Objections:** What got pushback in similar roles?
     - **Wins:** What hooks landed that this role could use?
     - **Persona Mismatches:** Did similar roles expect different positioning?
   - Review [[Job Hunting]] → Anti-Signals for known rejection patterns
   - If role matches a pattern, flag it in analysis and factor into recommendation

7. **Output recommendation:** APPLY, CONSIDER, or PASS with clear reasoning

8. **Review with Judge:**
   - Run evaluation through `/judge` with `job-eval` criteria
   - Check: fit_analysis, red_flags, specificity, recommendation, career_direction
   - If verdict is `needs_work`: revise analysis (max 2 iterations)
   - Ensures recommendation is specific and actionable, not vague

9. **Create vault note — MANDATORY for ALL outcomes:**
   - **Do this immediately after giving recommendation — don't wait for user to ask**
   - Filename: `[[Role Title - Company]]`
   - **MUST include full JD details:** Copy requirements, responsibilities, qualifications verbatim from the posting
   - Include: Fit analysis table, recommendation reasoning
   - This creates a record for future reference, pattern recognition, and duplicate detection

10. **Update job tracking:**
    - **APPLY:** Add to "Applied Jobs" or "To Apply" section in [[Job Hunting]]
    - **PASS:** Add to "Passed On" section with one-line reason
    - **CONSIDER:** Note in appropriate section with context

11. **If APPLY:**
    - **Easy Apply roles:** Ask whether to proceed with application now
    - **Company website roles:** Add to "To Apply" list (external ATS requires more effort; note for later)

**Note:** No reliable way to close browser tabs via MCP — leave tab open for user to close manually.

## Fit Dimensions

| Dimension | Considerations |
|-----------|----------------|
| **Seniority** | Step up, lateral, or step down from current level? |
| **Role Focus** | Matches core skills (AI/ML, DS, etc.) or pivot (BI, PM, DE)? |
| **Industry** | Strategic value? Transferable credibility? |
| **Tech Stack** | Alignment with user's technical strengths? |
| **Competition** | Applicant count, seniority distribution, education levels |
| **Salary** | Compare to current compensation if known |
| **Anti-Signal** | Does this match a known rejection pattern? |

## Note Template

```markdown
# [Role Title], [Company]

**Source:** [LinkedIn URL]
**Discovered:** [Date]
**Status:** [Applied/Passed/Considering]

## Job Details

**Title:**
**Company:**
**Location:**
**Salary:** [if disclosed]
**Applicants:** [count] ([seniority breakdown])

## Requirements

[COPY FULL REQUIREMENTS FROM JD - verbatim bullet points]

## Responsibilities

[COPY FULL RESPONSIBILITIES FROM JD - verbatim bullet points]

## Preferred/Nice-to-Have

[If listed separately in JD]

## Fit Analysis

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| Seniority | ✅/⚠️/❌ | |
| Role Focus | ✅/⚠️/❌ | |
| Industry | ✅/⚠️/❌ | |
| Tech Stack | ✅/⚠️/❌ | |
| Competition | ✅/⚠️/❌ | |
| Salary | ✅/⚠️/❌ | |
| Anti-Signal | ✅/⚠️/❌ | |

## Recommendation

**[APPLY/CONSIDER/PASS]**

[Reasoning]
```

## Passed On Format

```
- [[Role Title - Company]] (Date) - [One-line reason]
```

## Batch Processing

For multiple jobs, run this skill sequentially on each URL. Start with quick duplicate check before full analysis.

## Related Skills

- `chrome-automation` — Browser best practices (read_page, wait times, tab creation)
- `vault-pathfinding` — Vault paths and conventions (where to read/write notes)
- `/review-saved-jobs` — Batch processing of LinkedIn saved jobs (chains to this skill)
- `/debrief` — Captures interview signals that feed back into this skill's red flag check
