---
name: analyze-link
description: Universal link analyzer with auto-routing. Use when user shares any URL. Detects content type (article, job, repo, company, paper, video) and routes to appropriate handler. Triggers on any URL share, "check this", "what is this", or "analyze this link".
---

# Analyze Link

Universal entry point for any URL. Detects content type, routes to specialized handler or graceful fallback. Removes cognitive load of choosing the right skill.

## Workflow

1. **Fetch & Classify** — Get URL content, detect type from URL pattern + page structure
2. **Route** — Send to appropriate handler (specialized, lightweight, or fallback)
3. **Ontology Injection** — Before generating note, grep vault for existing tags/MOCs to use
4. **Save** — Write note with type-appropriate YAML frontmatter
5. **Log** — Append to telemetry for future optimization

## Content Type Detection

| Pattern | Type | Handler |
|---------|------|---------|
| `github.com/*/*` | repo | Lightweight |
| `linkedin.com/jobs/*` | job | → `/evaluate-job` |
| `linkedin.com/company/*` | company | Lightweight |
| `linkedin.com/in/*` | profile | Lightweight |
| `*.substack.com`, `medium.com/*`, `*blog*` | article | Specialized |
| `arxiv.org/*`, `papers.*`, `*.pdf` | paper | Specialized |
| `youtube.com/*`, `youtu.be/*` | video | Lightweight |
| Company career/about pages | company | Lightweight |
| Everything else | unknown | Check content, then fallback |

**Fallback logic:** If URL pattern unclear, fetch content and look for signals:
- Has "Key Ideas" / thesis structure → article
- Has job requirements / responsibilities → job
- Has code/commits/stars → repo
- Otherwise → unclassified

## Three-Tier Handlers

### Tier 1: Specialized (full evaluation)

**Articles** — Use /evaluate-article logic (without /judge step):
- Worth Noting check
- Key Ideas (3-5 bullets)
- My Take (2-4 sentences)
- Interlink with vault

**Jobs** — Route to `/evaluate-job`

### Tier 2: Lightweight (basic extraction)

**Repos:**
```yaml
---
source: [URL]
type: repo
fetched_at: [timestamp]
language: [primary language]
stars: [count]
last_commit: [date]
license: [if present]
related_company: [if identifiable]
tags: []
---

## Overview
[1-2 sentence description from README]

## Signals
- **Activity:** [active/stale/abandoned based on commit recency]
- **Quality:** [docs, tests, CI badges]
- **Relevance:** [why this matters for interview prep / learning]
```

**Company Pages:**
```yaml
---
source: [URL]
type: company
fetched_at: [timestamp]
company: [name]
industry: [sector]
size: [if available]
stage: [startup/growth/enterprise]
tags: []
---

## Overview
[What they do, 2-3 sentences]

## Signals
- **Tech Stack:** [if mentioned]
- **Culture:** [any signals from about/careers]
- **Red Flags:** [if any]
```

**Profiles (LinkedIn):**
```yaml
---
source: [URL]
type: profile
fetched_at: [timestamp]
name: [person name]
role: [current title]
company: [current company]
connection_context: [why relevant - recruiter, hiring manager, etc.]
tags: []
---

## Background
[Brief summary of experience]

## Notes
[Why saving this profile - interview prep, networking, etc.]
```

**Videos:**
```yaml
---
source: [URL]
type: video
fetched_at: [timestamp]
title: [video title]
channel: [creator]
duration: [length]
tags: []
---

## Summary
[Key points from transcript if available, otherwise from title/description]

## Timestamps
[Notable sections if identifiable]
```

### Tier 3: Generic Fallback

For anything unclassified:
```yaml
---
source: [URL]
type: unclassified
fetched_at: [timestamp]
domain: [source domain]
tags: []
---

## Content
[Title and brief summary]

## Why Saved
[User's apparent intent - to review later, reference, etc.]
```

## Ontology Injection

Before generating any note, run:
```bash
grep -r "^tags:" ~/notes/*.md | cut -d: -f2 | tr ',' '\n' | sort -u | head -50
```

Also check for relevant MOCs:
```bash
ls ~/notes/*MOC*.md ~/notes/Maps/*.md 2>/dev/null
```

**Rule:** Only use tags that already exist in vault. Never invent new tags. If no existing tag fits, leave tags empty — better than fragmenting the graph.

## Telemetry

Append to `~/notes/Meta/Link Analyzer Telemetry.md`:
```
| [date] | [URL] | [detected_type] | [confidence] | [override?] |
```

Review weekly to see which content types need specialized handlers.

## Skip Conditions

Don't create a note if:
- URL is a login wall with no content
- Content is pure marketing fluff (announce and exit)
- Already exists in vault (check by URL)

For skips, output:
> **Skip** — [reason]
> Domain: [source]

## Edge Cases

**Hybrid content** (e.g., blog post about a repo): Ask user which type to prioritize, or create note with primary type and link to related.

**Paywalled:** Report clearly, offer to wait for user to paste content.

**Failed fetch:** Try WebFetch first, fall back to asking user to paste.

## Integration

This skill supersedes direct invocation of `/evaluate-article` for new links. Users can still call `/evaluate-article` directly if they know it's an article.

`/evaluate-job` remains separate for LinkedIn job URLs — this router just dispatches to it.
