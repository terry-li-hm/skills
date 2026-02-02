---
name: linkedin-job-search
description: LinkedIn job search tips and strategies. Reference skill for optimizing job discovery.
user_invocable: false
---

# LinkedIn Job Search

Reference skill for effective LinkedIn job searching.

## Search Strategy

**Broad vs Specific:**
- **Broad keyword + location** (e.g., "AI" + Hong Kong) — Better for discovery. Catches non-standard titles like "Product Lead - AI", "Strategy Manager, AI", "Principal Engineer (ML)".
- **Specific title alerts** (e.g., "VP Data Science") — Better for passive monitoring. Notifies when exact-match roles post.

Use both: broad search for weekly manual scanning, specific alerts for notifications.

## Filtering for Sponsorship (Overseas)

When searching for roles that might sponsor visas:
- Add keywords: "relocation", "visa support", "visa sponsorship"
- Filter by company size (larger companies sponsor more often)
- Check job description for "must have right to work" (usually means no sponsorship) vs silence on visa (might sponsor)

## Applicant Stats Interpretation

LinkedIn shows applicant seniority breakdown. Notes:
- 50% entry-level doesn't mean the role IS junior — juniors spray-and-pray on everything
- Low VP/Director % suggests senior people don't see this as a fit
- Use as one signal among many, not definitive proof of seniority level

## Saved Jobs

Use LinkedIn's "Save" feature to batch jobs for later review. See `/review-saved-jobs` skill for systematic review workflow.

## Company Filter Caveat

**`f_C=` company filter is unreliable.** Often returns "No matching jobs" even when roles exist.

**Better approach:** Search by role title keywords + location, not by company ID.

## Terry-Specific Search Patterns (Overseas)

Tested and working searches for roles matching Terry's background:

| Background | Search Keywords | Location | Example Result |
|------------|-----------------|----------|----------------|
| AML/Financial Crime | `AVP Financial Crime` | Toronto | TD Bank AVP role |
| AML/Financial Crime | `Financial Crime AI` | Toronto, London | - |
| AML/Financial Crime | `AML AI automation` | Toronto, London | - |
| Audit + AI | `Senior Audit Manager AI` | Toronto | CIBC Audit role |
| Audit + AI | `Audit Manager Data AI` | Toronto, London | - |
| Audit + AI | `AI Risk Audit` | Toronto, London | - |
| AI Governance | `AI Governance` | Toronto, Dublin, London | Gartner, Intact |
| AI Governance | `Responsible AI` | Toronto, London | - |
| AI Governance | `AI Risk` | Toronto, London | - |

## Target Companies (Canadian Big Five)

For banking AI roles in Canada, prioritize these employers:

| Bank | Alumni (CNCBI/HKUST) | Notes |
|------|---------------------|-------|
| TD Bank | 12 / 31 | Strong Financial Crime AI |
| CIBC | 7 / 18 | AI Audit roles |
| Scotiabank | Check | Model Validation |
| RBC | Check | Largest Canadian bank |
| BMO | Check | - |

## Weekly Monitoring Routine (Overseas)

1. Run each domain keyword search once/week
2. Filter by "Past week" (Date posted → Past week, or `f_TPR=r604800` in URL)
3. Save promising roles to LinkedIn "Saved Jobs"
4. Cross-check alumni count (CNCBI/HKUST) for referral potential
5. For strong matches, create vault note with fit analysis
