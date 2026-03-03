---
name: vault-notes
description: Reference for vault note structure — atomicity, interlinking, hub vs. detail, when to split, where notes live. Not user-invocable — consult when creating or refactoring vault notes.
---

# Vault Note Structure

Reference skill for how to structure notes in `~/notes/`. Covers atomicity, interlinking, placement, and anti-patterns. Consult before creating a new note or when a note feels too large.

## Core Principles

1. **One concern per note.** A note that covers two distinct topics should be two notes with a wikilink between them. Signal: if the title needs "and" or "/", it's probably two notes.

2. **Hub notes are thin pointers.** Tracker notes (NOW.md, TODO.md, Capco Transition) hold status and links — not detail. Detail lives in child notes. Hub grows? Split it.

3. **Link generously.** Dense `[[wikilinks]]` let Claude walk the graph for context. Sparse links = dead ends. Every note should have a **Related:** line.

4. **Facts age, rules don't.** Time-sensitive facts (dates, amounts, status) belong in vault notes, not CLAUDE.md. CLAUDE.md = rules. Vault = reference.

5. **Dated updates over status blocks.** Use `**Update (Feb X):**` headers in note bodies as the natural changelog — grep-surfaceable, no separate status section needed.

## Note Types

| Type | Purpose | Example |
|------|---------|---------|
| **Reference** | Stable facts, numbers, technical detail | `AML Triage Model - Reference.md` |
| **Angles / Positioning** | How to talk about something, audience-specific framing | `AML Triage Model - Capco Angles.md` |
| **Tracker / Hub** | Live status, pointers to child notes | `Capco Transition.md`, `NOW.md` |
| **Profile** | Person or org — background, relationship, context | `Bertie Haskins Profile.md` |
| **Story / STAR** | Interview/narrative ready — what happened, impact | `The AML Alert Prioritisation Story.md` |
| **Daily** | Activity log — what happened this session | `2026-03-03.md` |
| **Conversation Card** | 30-second refresh before a meeting | `Responsible AI and MRM.md` |

## Where Notes Live

- `~/notes/` — general vault root (project-agnostic, career, personal)
- `~/notes/Capco/` — Capco-facing: positioning, client work, onboarding
- `~/notes/Capco/Conversation Cards/` — pre-meeting refresh cards
- `~/notes/Career/` — CV, interview prep, performance reviews
- `~/notes/Daily/` — daily logs
- `~/notes/Research/` — external research, clippings

**Rule:** If a note is about a CNCBI project operationally → vault root. If it's about how to use that project at Capco → `notes/Capco/`.

## When to Split a Note

Split when:
- Title needs "and" or "/"
- Note covers both facts and positioning (split into Reference + Angles)
- Note covers both status and detail (split into Hub + child)
- Note is >150 lines and growing

Don't split when:
- Note is actively being iterated (wait until stable)
- The two concerns are always read together (keep, add clear sections)

## Interlinking Patterns

Every note should have a **Related:** line at the top (below frontmatter):
```
**Related:** [[Note A]] | [[Note B]] | [[Note C]]
```

When one note supersedes another's facts, add a pointer at the stale location rather than deleting:
```
(Feb 25–Feb 26 actuals: 34.33% — see [[AML Triage Model - Reference]])
```

Conversation Cards and positioning notes → link to the Reference note for facts. Never repeat numbers inline without linking to the source.

## Anti-Patterns

- **God note:** One 1000+ line note covering multiple concerns (e.g. `Capco - Principal Consultant, AI Solution Lead.md`). Tolerate when actively iterating; split after stabilising.
- **Orphan note:** Created but not linked from anywhere — invisible to graph traversal. Always add to at least one Related: line.
- **Stale inline facts:** Numbers repeated in multiple notes without linking to a canonical source. One source of truth; others link.
- **CLAUDE.md fact creep:** Time-sensitive data (dates, amounts, status) written into CLAUDE.md instead of vault. Facts age; rules don't.

## Learnings

- **Capco vs. vault root split (Mar 2026):** Operational project notes (CNCBI work) → vault root. Capco-facing angles/positioning → `notes/Capco/`. Caught when `AML Triage Model - Reference.md` was initially placed in `notes/Capco/`.
- **Seed skills early.** Don't wait for three note-structure corrections — the pattern is clear after the first. (This skill exists because of that.)
