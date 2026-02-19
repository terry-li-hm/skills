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

- **Chatbot**: RCSA completed with IT Governance & Controls (IT dept, first line) + Retail Banking control team (first line). Tech Risk in RMG (second line) reviewed but did NOT formally sign off. No formal second-line sign-off required given limited scope.
- **AI Governance Standards**: Terry authored. WERE signed off by second-line risk (RMG). This is the stronger claim.
- **AML Model**: First-line sign-off (FCC). High-level conversation with IT Risk and Controls head regarding access controls.

## Changes Log

- 2026-02-19: "to secure second-line approval" in summary -> removed, now reads "enabling peer-level engagement" (cleaner, no overclaim)
- 2026-02-19: "identified 30% of alerts as low-risk for hibernation" in summary -> "safely hibernated 30% of alerts with no degradation in STR capture"
- 2026-02-19: Row 2 detail rephrased to "30% of alerts eligible for hibernation, containing only 0.8% of STRs; informed FCC's risk-based review strategy" (distinct from summary)
- 2026-02-19: "safely hibernated" in summary → "identified 30% of alerts for hibernation" (hibernation not yet operationalised — preparing governance for HKMA submission)

## CV Source Code

The HTML-generated job-hunting CV lives at `~/notes/CV Source Code.md`. Keep both in sync when making content changes.

## Expiry

Delete this skill after Capco onboarding is complete (likely May 2026).
