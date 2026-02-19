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

1. **Quit the app first** (not just close document — `close every document` doesn't reliably release the file):
   ```bash
   osascript -e 'tell application "Keynote" to quit' 2>/dev/null
   osascript -e 'tell application "Microsoft PowerPoint" to quit' 2>/dev/null
   sleep 1
   ```
2. Edit via `uv run --with python-pptx python3` script
3. Reopen: `open "<path>"`
4. **Always quit before reopen** — editing a file while the app has it open can cause stale reads or overwrites

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

## Project & Governance Facts

Full reference: `~/notes/CNCBI Project Facts.md` — authoritative source for all project details, governance approvals, accurate verbs, and impact metrics. Always read that note before making CV edits.

## Changes Log

- 2026-02-19: "to secure second-line approval" in summary -> removed, now reads "enabling peer-level engagement" (cleaner, no overclaim)
- 2026-02-19: "identified 30% of alerts as low-risk for hibernation" in summary -> "safely hibernated 30% of alerts with no degradation in STR capture"
- 2026-02-19: Row 2 detail rephrased to "30% of alerts eligible for hibernation, containing only 0.8% of STRs; informed FCC's risk-based review strategy" (distinct from summary)
- 2026-02-19: "safely hibernated" in summary → "identified 30% of alerts for hibernation" (hibernation not yet operationalised — preparing governance for HKMA submission)
- 2026-02-19: De-editorialised — removed "enabling peer-level engagement" from summary, "the real bottleneck" → "the primary bottleneck" in Row 1, removed "demonstrating audit-led capability transfer" from Row 4, removed "foundation for the data science career" from PwC
- 2026-02-19: Summary tightened — first sentence rewritten for punch, "as project lead" removed (redundant with Role column)
- 2026-02-19: Row 1 bullet 1 rewritten from narrative to impact format; Row 2 trimmed "on investigator-labelled holdout across an 18-month dataset"
- 2026-02-19: Cleanup — arrows to "to", removed 0.8% STR detail from Row 2, RAG removed from Row 1, ~ to "around" in Row 3
- 2026-02-19: "Co-designed" confirmed for Row 5 (data governance team led writing, Terry was SME)
- 2026-02-19: AML sentence split — "zero audit findings" gets its own sentence in summary (council consensus)
- 2026-02-19: Possessives fixed (bank's, HKMA's)
- 2026-02-19: Council full review — 3 fixes applied: Sandbox role "SME and" dropped, employment date 2025→2026, Credit Risk tag → Retail Banking Operations
- 2026-02-19: Council "Consider Later" items (4x STR metric, 0.8% materiality, audit crossover narrative) — all skipped, CV is tight enough

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
