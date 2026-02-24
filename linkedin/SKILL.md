---
name: linkedin
description: Draft LinkedIn comments and posts. Use when user shares a LinkedIn URL to comment on, says "linkedin", or wants to draft/post content.
user_invocable: true
---

# LinkedIn Skill

Draft comments on others' posts and original posts for Terry's LinkedIn.

## Triggers

- User shares a LinkedIn post URL
- "linkedin", "comment on this", "should we comment"
- "draft a post", "linkedin post"
- "post about X"

## Mode Detection

| Signal | Mode |
|--------|------|
| URL shared or "comment on" | **Comment** |
| "draft post", "post about", or topic from Content Ideas | **Post** |

---

## Comment Mode

### 1. Fetch the Post

LinkedIn is login-gated. Always use authenticated browser:

```bash
agent-browser open "<url>" --profile
agent-browser snapshot --profile
agent-browser close --profile
```

Extract: author name/title, verbatim post text, all comments (author + text), engagement counts.

### 2. Research the Author

Quick web search for the author's role, company, and relevance to Terry's network. Check vault too:

```bash
km-ask "<author name>"
```

### 3. Assess: Should Terry Comment?

Answer these before drafting:

1. **Is the topic in Terry's lane?** (AI, financial services, governance, enterprise tech, consulting)
2. **Can Terry add a distinct angle?** (Not just agreement — a practitioner insight, extension, or counterpoint)
3. **Is the author worth engaging?** (Senior practitioner, potential client/referral, thought leader in FS/AI)
4. **Is the timing right?** (Post <48h old? Fresh comments get more visibility)

If any answer is no, say so and suggest skipping or just reacting.

### 4. Find Terry's Angle

Scan existing comments for gaps. Terry's strongest angles (in order of preference):

1. **Practitioner extension** — "I've seen this in banking, and here's what happens next..."
2. **Concrete example** — Specific contrast or data point that proves the abstract claim
3. **The missing failure mode** — What breaks even when you follow the advice
4. **Respectful counterpoint** — "This works for X, but in regulated FS..."

Check vault for supporting material:

```bash
km-ask "<topic>"
```

Draw from real experience (CNCBI governance, HKMA sandbox, AML model, agent architecture) — never fabricate.

### 5. Draft the Comment

**Voice rules:**
- "I've seen" not "I'd add" (observational, not prescriptive)
- Specific > generic (name the committee, the system, the failure mode)
- Build on their framework, don't compete with it
- No hashtags, no "great post!", no engagement bait
- Spelling: match the poster's audience (US spelling for US-based authors, British for UK/HK/APAC)
- Plain text only — LinkedIn comments don't support markdown bold/italic
- Aim for ~50-70 words. Mobile truncation is real; short + substantive beats long + thorough
- 4-8 sentences max — a comment, not a post

**Structure:**
1. Brief validation (one phrase, specific — not "great post")
2. The insight (1-2 sentences — the practitioner pattern)
3. Concrete illustration (the vivid contrast or example)
4. Implication (why this matters — the "so what")
5. Optional: closing question to invite engagement (only if natural)

### 6. Review

**For high-value targets** (senior FS/AI practitioners, potential Capco clients, 1K+ followers):
- Offer consilium `--quick` review (~$0.10) with full post context (verbatim text, all comments, author background)
- The first quick council should always have the actual post — don't summarise. Fetch via agent-browser first.
- For comments worth extra polish: `--deep` (~$0.90) catches logical gaps quick misses (causal direction, platform formatting, over-polishing)
- Key criteria: tone calibration, overstepping risk, engagement likelihood

**For routine engagement:**
- Self-review against voice rules above. Skip consilium.

### 7. Deliver

Create a secret gist for mobile copy:

```bash
gh gist create --public=false -f "linkedin-comment.md" - <<< "<comment text>"
```

Present: the draft, the gist URL, and a one-line rationale for the angle chosen. Delete gist after Terry confirms it's copied.

---

## Post Mode

### 1. Check Content Ideas

Always start from the pipeline:

```bash
cat ~/notes/LinkedIn\ Content\ Ideas.md
```

If the topic exists, use the captured angle/details. If new, capture it first.

### 2. Draft Against Playbook Rules

Read the playbook: `~/notes/LinkedIn Posting Playbook.md`

**Hard rules:**
- No external links in post body (link goes in first comment)
- Don't undersell — "system" not "script" when architecture warrants
- Add a visual recommendation (screenshot, diagram, architecture)
- One solid post per 2-3 weeks cadence

**Post types:**
- "I built X" — credibility through shipping
- "I learned X" — LinkedIn algo loves learning narratives
- "Observation from the field" — Capco-era content (post Mar 16)

**Timing gate:**
- Posts that need "AI Solution Lead" title weight → after Capco start (Mar 16+)
- Builder/personal posts → anytime

### 3. Review

All posts get consilium `--quick` minimum. High-stakes posts (first Capco-era, controversial angle) get full `--council`.

### 4. Deliver

Gist the draft for mobile:

```bash
gh gist create --public=false -f "linkedin-post.md" - <<< "<post text>"
```

Update `[[LinkedIn Content Ideas]]` status to "Draft ready" with date.

---

## Pre-Capco vs Post-Capco

| Timing | What's safe | What to avoid |
|--------|------------|---------------|
| **Now (pre-Mar 16)** | Builder proof, personal stories, practitioner comments | "As an AI Solution Lead at Capco..." |
| **Post-Mar 16** | Enterprise diagnostics, consulting frameworks, client-ready insights | Mentioning specific client names |

## Positioning Reminders

- Terry = practitioner-builder who ships, not consultant who theorises
- Credit sources (Simon Willison, original poster, etc.)
- Specific numbers beat vague claims (198 tests, $0.23 vs $6.62, 1,125 frames)
- Honest about limitations (AI got lens thickness wrong, Speechmatics failed)
- Never "thought leader" language — let the work speak

## Vault References

- `~/notes/LinkedIn Content Ideas.md` — content pipeline
- `~/notes/LinkedIn Posting Playbook.md` — metrics, learnings, cadence
- `~/notes/LinkedIn Profile Updates - Feb 2026.md` — headline/about copy
- `~/notes/Councils/LLM Council - LinkedIn*` — past comment/post reviews
