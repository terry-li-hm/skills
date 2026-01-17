---
name: evaluate-job
description: Evaluate LinkedIn job postings for fit. This skill should be used when the user shares a LinkedIn job URL and wants analysis of whether to apply. Triggers on LinkedIn job links, "evaluate this role", or requests to analyze job fit.
---

# Evaluate Job

Analyze LinkedIn job postings against user's background, current pipeline health, and career criteria. Output a recommendation (APPLY/CONSIDER/PASS) with structured reasoning.

## Workflow

1. **Navigate to job posting** — Extract full JD (requirements, responsibilities, preferred qualifications, salary if disclosed, applicant stats)

2. **Load context files** — Check user's CLAUDE.md for background, credentials, differentiators, current situation, and job hunting status

3. **Analyze fit** across dimensions (see Fit Dimensions below)

4. **Factor pipeline health:**
   - **Healthy** (5+ active, interviews scheduled): Maintain standards — PASS on poor fits
   - **Thin** (<5 active, no interviews): Lower bar — CONSIDER "good enough" roles
   - Consider urgency of user's situation when weighing trade-offs

5. **Output recommendation:** APPLY, CONSIDER, or PASS with clear reasoning

6. **If APPLY:** Ask whether to proceed with application

7. **Create vault note:**
   - Filename: `[[Role Title, Company]]`
   - Include: Full JD, fit analysis table, recommendation reasoning

8. **Update job tracking** — Add to appropriate section in user's job hunting notes

## Fit Dimensions

| Dimension | Considerations |
|-----------|----------------|
| **Seniority** | Step up, lateral, or step down from current level? |
| **Role Focus** | Matches core skills (AI/ML, DS, etc.) or pivot (BI, PM, DE)? |
| **Industry** | Strategic value? Transferable credibility? |
| **Tech Stack** | Alignment with user's technical strengths? |
| **Competition** | Applicant count, seniority distribution, education levels |
| **Salary** | Compare to current compensation if known |

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

[From JD]

## Responsibilities

[From JD]

## Fit Analysis

| Dimension | Assessment | Notes |
|-----------|------------|-------|
| Seniority | ✅/⚠️/❌ | |
| Role Focus | ✅/⚠️/❌ | |
| Industry | ✅/⚠️/❌ | |
| Tech Stack | ✅/⚠️/❌ | |
| Competition | ✅/⚠️/❌ | |
| Salary | ✅/⚠️/❌ | |

## Recommendation

**[APPLY/CONSIDER/PASS]**

[Reasoning]
```

## Passed On Format

```
- [[Role Title, Company]] (Date) - [One-line reason]
```
