---
name: scan-career-sites
description: This skill scans company career sites for AI/Data Science roles that may not be posted on LinkedIn. Run periodically to discover opportunities outside LinkedIn.
---

# Scan Career Sites

Scan target company career sites for AI/Data Science roles that may not be posted on LinkedIn.

## Target Sites to Scan

These companies are known to post roles on their own career sites that don't always appear on LinkedIn:

### Priority 1: Statutory Bodies & Government-Adjacent

| Company | Career URL | Keywords |
|---------|-----------|----------|
| Cyberport | https://www.cyberport.hk/en/news/career_opportunities/ | AI, Data Science, Manager |
| HKSTP | https://www.hkstp.org/en/about-us/career/ | AI, Data Science, Innovation |
| Airport Authority HK | https://www.hongkongairport.com/en/airport-authority/careers/ | AI, Innovation, Data |
| HKMA | https://www.hkma.gov.hk/eng/about-us/join-us/current-vacancies/ | AI, Data, Fintech |
| WKCDA | https://wd3.myworkdaysite.com/recruiting/wkcda/External | Data, AI, Architecture |
| MTR | https://www.mtr.com.hk/en/corporate/careers/career_opportunities.html | AI, Data Science, Digitalisation |

### Priority 2: Banks (Check Their Own Portals)

| Company | Career URL | Notes |
|---------|-----------|-------|
| DBS | https://www.dbs.com/careers | Posts some roles only on their site |
| Standard Chartered | https://jobs.standardchartered.com | Good AI/Data roles |
| Hang Seng | https://www.hangseng.com/en-hk/about/careers/job-openings/ | Uses SuccessFactors |
| BOC HK | https://www.bochk.com/en/career/opportunities.html | Check periodically |
| HKEX | https://www.hkexgroup.com/Careers | Limited but strategic |

### Priority 3: Insurance & Other

| Company | Career URL | Notes |
|---------|-----------|-------|
| Manulife | https://careers.manulife.com/global/en/hong-kong | Good AI roles |
| AIA | https://www.aia.com/en/careers | Check Hong Kong filter |
| AXA | https://careers.axa.com | Filter by Hong Kong |
| Prudential | https://www.prudentialplc.com/en/careers | Asia Pacific roles |
| Swire Properties | https://careers.swireproperties.com/en-hk/jobs/ | Non-FS option |
| Cathay Pacific | https://careers.cathaypacific.com/en/careers/jobs | Digital/IT roles |

### Job Boards (Non-LinkedIn)

| Site | Search URL | Notes |
|------|-----------|-------|
| Indeed HK | https://hk.indeed.com | Search: "AI lead" OR "data science director" |
| Jobsdb | https://hk.jobsdb.com | Search: "AI" + "senior manager" |

## How to Scan

1. **Use browser automation** to visit each career site
2. **Search/filter** for AI, Data Science, Machine Learning keywords
3. **Check posting dates** - prioritize recent postings
4. **Compare against Job Hunting.md** - skip already-applied roles
5. **Report new findings** with quick fit assessment

## Quick Fit Criteria for Terry

**Strong Fit Signals:**
- Senior Manager / Director / Head / VP level
- AI/ML/GenAI focus (not just BI/analytics)
- Banking/FS/Insurance domain
- Hong Kong based
- Leadership role (not IC)

**Pass Signals:**
- Manager or below (step down from AGM)
- Pure data engineering / architecture (not ML)
- Master's/PhD required
- Heavy quant/trading focus
- Relocation required

## Output Format

For each new role found, report:

```
### [Company] - [Role Title]
- **URL:** [direct link]
- **Posted:** [date if visible]
- **Fit:** HIGH / MEDIUM / LOW / PASS
- **Notes:** [1-2 sentence assessment]
- **Action:** Apply / Skip / Research more
```

## When to Run

- Weekly during active job search
- After hearing about company hiring news
- Before networking calls (check if target company is hiring)
