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

**Better approach:** Use company name as keyword + "AI" + location.

Example: `TD AI` + Toronto (390 results) is more reliable than `f_C=1482` filter.

## Seniority Filter Caveat

**`f_E=4` (Mid-Senior level) can miss relevant senior roles.**

Example: `RBC AI` + Toronto with Mid-Senior filter → **0 results**. Without filter → **454 results**, including:
- Senior Manager, AI Governance
- Sr. Director, Data Science
- Associate Director, Data Analytics & ML
- Lead Data Scientist, Fraud AI

**Why:** Companies classify levels differently. "Associate Director" or "Lead" may not map to LinkedIn's "Mid-Senior" category.

**Recommendation: Don't use seniority filter by default.**
1. Search **without** `f_E=4` to see full market
2. Scan titles manually for senior roles (Senior Manager, Director, VP, AVP)
3. Only add filter if results exceed 500+ and need narrowing

**URL parameter reference:**
- `f_E=4` = Mid-Senior level (unreliable)
- `f_TPR=r604800` = Posted in past week
- `sortBy=R` = Sort by relevance

## Best Search Pattern: Company + AI + City

| Target | Search | Location | Results (Feb 2026, no filter) |
|--------|--------|----------|------------------------------|
| Scotiabank AI roles | `Scotiabank AI` | Toronto | 486 |
| RBC AI roles | `RBC AI` | Toronto | 454 |
| TD Bank AI roles | `TD AI` | Toronto | 390 |
| BMO AI roles | `BMO AI` | Toronto | 272 |
| Barclays AI roles | `Barclays AI` | United Kingdom | 133 |
| CIBC AI roles | `CIBC AI` | Toronto | 111 |

This catches all AI-related roles at the company, then you scan the list for senior titles (AVP, VP, Director, Senior Manager).

**Important:** Search WITHOUT seniority filter. RBC/BMO show 0 with filter, 400+ without.

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

| Bank | Alumni (CNCBI/HKUST) | AI Roles (no filter) | Best Finds |
|------|---------------------|----------------------|------------|
| Scotiabank | ? / 27 | 486 | Senior Manager AI & Ethics Governance |
| RBC | ? / 46 | 454 | Senior Manager AI Governance, Sr. Director Data Science |
| TD Bank | 12 / 31 | 390 | AVP Financial Crime AI, Senior Manager AI Vulnerability |
| BMO | ? / 26 | 272 | Senior Manager GenAI, VP AI Engineer |
| CIBC | 7 / 18 | 111 | Senior Audit Manager Data & AI Risk, Sr. AI Scientist |

**Note:** All counts are WITHOUT seniority filter. With `f_E=4` filter, RBC and BMO show 0.

**Priority for Terry:** TD (AVP Financial Crime) > Scotiabank (AI Governance) > RBC (AI Governance) > BMO (GenAI) > CIBC (Audit)

## Weekly Monitoring Routine (Overseas)

1. Run each domain keyword search once/week
2. Filter by "Past week" (Date posted → Past week, or `f_TPR=r604800` in URL)
3. Save promising roles to LinkedIn "Saved Jobs"
4. Cross-check alumni count (CNCBI/HKUST) for referral potential
5. For strong matches, create vault note with fit analysis
