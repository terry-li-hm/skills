---
name: evaluate-job
description: Evaluate LinkedIn job postings for fit. This skill should be used when the user shares a LinkedIn job URL and wants analysis of whether to apply. Triggers on LinkedIn job links, "evaluate this role", or requests to analyze job fit.
---

# Evaluate Job

Analyze LinkedIn job postings against user's background, current pipeline health, and career criteria. Output a recommendation (APPLY/CONSIDER/PASS) with structured reasoning.

## Workflow

1. **Navigate to job posting:**
   - **Prefer Chrome:** `tabs_create_mcp` → create new tab → `navigate` → `get_page_text`
   - **Fallback (Chrome unavailable):** Use `tavily-extract` with `extract_depth: advanced`
   - Extract: requirements, responsibilities, preferred qualifications, salary if disclosed, applicant stats

   **Why Chrome over Tavily for LinkedIn:**
   - Tavily with `extract_depth: advanced` gets the full JD text, but **misses applicant stats** (count, seniority breakdown, education distribution) — these require being logged in
   - Chrome sees the full page as logged-in user, including competition metrics critical for fit analysis
   - Can click "Show more" to expand full JD if needed

2. **Load context files** (can run in parallel with step 1) — Check user's CLAUDE.md for background, credentials, differentiators, current situation, and job hunting status

3. **Analyze fit** across dimensions (see Fit Dimensions below)

4. **Factor pipeline health:**
   - **Healthy** (5+ active, interviews scheduled): Maintain standards — PASS on poor fits
   - **Thin** (<5 active, no interviews): Lower bar — CONSIDER "good enough" roles
   - Consider urgency of user's situation when weighing trade-offs

5. **Check anti-signals**:
   - Read Anti-Signals section from [[Job Hunting]]
   - If role matches a known pattern, add warning
   - Factor into recommendation (APPLY → CONSIDER if pattern match)

6. **Output recommendation:** APPLY, CONSIDER, or PASS with clear reasoning

7. **If APPLY:**
   - **Easy Apply roles:** Ask whether to proceed with application now
   - **Company website roles:** Add to "To Apply" list in job tracking (external ATS requires more effort; note for later)

8. **Create vault note (ALWAYS, even for PASS):**
   - Filename: `[[Role Title - Company]]`
   - **MUST include full JD details:** Copy requirements, responsibilities, qualifications verbatim from the posting
   - Include: Fit analysis table, recommendation reasoning
   - This creates a record for future reference and pattern recognition

9. **Update job tracking** — Add to appropriate section in user's job hunting notes

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
- [[Role Title, Company]] (Date) - [One-line reason]
```

## Batch Processing (Job Alert Emails)

For processing multiple jobs from LinkedIn alert emails, use `/process-job-alerts` skill instead. It handles batch filtering and calls this skill for deep-dives on promising roles.
