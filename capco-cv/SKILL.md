---
name: capco-cv
description: Edit and review the Capco onboarding CV (06 pptx). Use when user says "capco cv", "open cv", "edit cv", or references the 06 CV.
user_invocable: true
---

# Capco CV Editor

Edit the Capco onboarding CV PowerPoint programmatically.

## File

`/Users/terry/notes/Capco/Onboarding Documents/06 CV - Terry Li.pptx`

## Workflow

1. Close any open instance first: `osascript -e 'tell application "Keynote" to close every document' 2>/dev/null; osascript -e 'tell application "Microsoft PowerPoint" to close every document' 2>/dev/null`
2. Edit via `uv run --with python-pptx python3` script
3. Reopen: `open "<path>"`

## Structure (2 slides)

### Slide 1
- **Summary paragraph** (single text run): Name, tagline, CPA/CIA, governance frameworks, three headline achievements (AML 21%->88%, chatbot 3.5x, HKMA Sandbox 1-of-10)
- **Competency tags**: FS Industry, Functional, Technical, Governance
- **Career history** (text): CNCBI 3yr, DBS 4yr, PwC 4.5yr
- **Credentials**: CPA, CIA, BBA HKUST
- **Languages**: Cantonese, English, Mandarin
- **Project table** (6 rows):
  - Row 1: Call Centre Agent-Assist Chatbot (GenAI) — 6 months, project lead
  - Row 2: AML Alert Prioritisation Model — 12 months, project lead
  - Row 3: HKMA GenAI Sandbox (SME Financing) — 6 months, SME and technical lead
  - Row 4: DBS AML Audit Analytics Model — 6 months, project lead
  - Row 5: AI Governance Framework — 6 months, Lead SME

### Slide 2 (Additional Experience)
- Row 1: PwC IT Audit & Risk Assurance — 4.5 years
- Row 2: DBS Localisation of Group Data Science Tools — 12 months

## Governance Facts (accuracy reference)

### Call Centre Agent-Assist Chatbot
- RCSA completed, addressing each OWASP Top 10 LLM risk
- **IT Governance & Controls** (IT department) — reviewed and approved (first line)
- **Retail Banking control team** — approved (first line)
- **Tech Risk in RMG** (second line) — reviewed but did NOT formally sign off
- No formal second-line sign-off was required given the limited scope of phase one (no customer data, no core system integration, retrieval from curated FAQs only)
- Accurate verbs: "completed RCSA with IT controls and business approval" (NOT "secured second-line approval")

### AML Alert Prioritisation Model
- **FCC (Financial Crime Compliance)** — signed off before go-live (first line)
- High-level conversation with **IT Risk and Controls head** regarding access controls
- Terry designed his own production controls: restricted production project folder to admin account, automated deployment from GitLab
- Excluded demographic features (e.g. gender) for fairness
- Full model documentation pack with monitoring procedures
- **Zero audit findings** after full audit cycle
- **Hibernation**: Model identified 30% of alerts containing only 0.8% of STRs — but hibernation NOT yet operationalised. Currently preparing governance process for HKMA submission. Accurate verb: "identified for hibernation" (NOT "hibernated")

### AI Governance Standards & Procedures
- **Data governance team** led the writing of the standards and procedures document
- **Terry** provided lead SME input — the AI-specific expertise (model lifecycle, risk classification, validation, monitoring)
- Standards WERE signed off by **second-line risk (RMG/Tech Risk)**
- Framework adopted as bank's standard for AI/ML deployment approvals
- Accurate verb: "Co-designed" (NOT "authored" or "defined" — Terry was SME, not lead author)

### HKMA GenAI Sandbox (SME Financing)
- Selected as 1 of 10 banks from 40+ proposals; sole bank focusing on loan financing
- POC with Baidu as technology partner; Cyberport provided compute resources
- 3-week execution window; Terry navigated cybersecurity clearance for HKMA VPN
- Compressed 10-hour credit assessment to ~15 minutes; quality matched 5-year credit veterans
- Terry authored technical report submitted to HKMA
- Project initially parked post-POC (no business sponsor for production); business has recently come back to explore implementation

## Changes Log

- 2026-02-19: "to secure second-line approval" in summary -> removed, now reads "enabling peer-level engagement" (cleaner, no overclaim)
- 2026-02-19: "identified 30% of alerts as low-risk for hibernation" in summary -> "safely hibernated 30% of alerts with no degradation in STR capture"
- 2026-02-19: Row 2 detail rephrased to "30% of alerts eligible for hibernation, containing only 0.8% of STRs; informed FCC's risk-based review strategy" (distinct from summary)
- 2026-02-19: "safely hibernated" in summary → "identified 30% of alerts for hibernation" (hibernation not yet operationalised — preparing governance for HKMA submission)
- 2026-02-19: De-editorialised — removed "enabling peer-level engagement" from summary, "the real bottleneck" → "the primary bottleneck" in Row 1, removed "demonstrating audit-led capability transfer" from Row 4, removed "foundation for the data science career" from PwC

## CV Source Code

The HTML-generated job-hunting CV lives at `~/notes/CV Source Code.md`. Keep both in sync when making content changes.

## Style Principle

**Facts over self-selling.** State what you did and the impact; let the reader draw conclusions. If you have to explain why something is impressive, it isn't. Remove:
- Clauses that tell the reader what to think ("enabling peer-level engagement", "demonstrating capability transfer")
- Editorialising adjectives ("the real bottleneck" → "the primary bottleneck")
- Narrative framing ("foundation for the career that followed")

Numbers sell themselves: "21% → 88%", "3.5×", "zero audit findings", "1 of 10 from 40+".

## Expiry

Delete this skill after Capco onboarding is complete (likely May 2026).
