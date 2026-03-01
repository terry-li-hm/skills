---
name: linkedin-engage
description: Draft LinkedIn comments and posts. Use when user shares a LinkedIn URL to comment on, says "linkedin comment", "linkedin post", or wants to draft/post content.
user_invocable: true
---

# LinkedIn Skill

Draft comments on others' posts and original posts for Terry's LinkedIn.

## Triggers

URL-based triggers are handled by the `url-skill-router` hook (auto-injects reminder on LinkedIn URLs).
Keyword triggers: "linkedin", "comment on this", "should we comment", "draft a post", "post about X".

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

Web search for the author's **full background** — current role AND prior career. Current title undersells domain overlap (e.g. a healthcare AI founder may have previously built FS AI). Check vault too:

```bash
cerno "<author name>"
```

Key things to surface: prior companies, domain expertise accumulated before current role, any FS/banking background. This prevents explaining someone's own domain back to them.

### 3. Assess: Should Terry Comment?

Answer these before drafting:

1. **Is the topic in Terry's lane?** (AI, financial services, governance, enterprise tech, consulting)
2. **Can Terry add a distinct angle?** (Not just agreement — a practitioner insight, extension, or counterpoint)
3. **Is the author worth engaging?** (Senior practitioner, potential client/referral, thought leader in FS/AI)
4. **Is the timing right?** (Post <48h old? Fresh comments get more visibility. Also check `resurface search "<author/company>" --deep` — if Terry already commented on this person/company today, skip. Double-engaging same day looks over-eager.)
5. **Is the post worth Terry's comment?** If Terry's comment would be smarter than the post itself, react and move on. Comment when the post pulls the conversation *up* — original frameworks, genuine depth, substantive takes. Skip well-packaged platitudes, repackaged concepts, and content-mill series. Terry's practitioner insights should add to something strong, not carry something thin.

If any answer is no, say so and suggest skipping or just reacting.

### 4. Find Terry's Angle

Scan existing comments for gaps. Terry's strongest angles (in order of preference):

1. **Practitioner extension** — "I've seen this in banking, and here's what happens next..."
2. **Concrete example** — Specific contrast or data point that proves the abstract claim
3. **The missing failure mode** — What breaks even when you follow the advice
4. **Respectful counterpoint** — "This works for X, but in regulated FS..."

Check vault for supporting material:

```bash
cerno "<topic>"
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

Present the draft in chat with a one-line rationale for the angle chosen. **Stop here and wait for input.**

### 6. Checkpoint: Consilium Review?

Ask Terry whether to run a consilium review before finalising. Suggest the appropriate tier based on the target:

- **High-value target** (senior FS/AI practitioner, potential Capco client, 1K+ followers): recommend `--quick` (~$0.10)
- **Worth extra polish** (controversial angle, sensitive topic): offer `--deep` (~$0.90)
- **Routine engagement**: self-review against voice rules is sufficient — say so and let Terry decide

Do not run consilium without explicit confirmation. If Terry says go ahead, run with full post context (verbatim text, all comments, author background) — never summarise the post for the council.

### 7. Finalise and Deliver

Only create a gist once Terry confirms the draft is ready to post. Include **both the original post and the draft comment** so Terry can review them side by side on mobile:

```bash
gh gist create --public=false -f "linkedin-review.md" - << EOF
## Original Post — <Author Name>

<post URL>

<verbatim post text>

---

## Draft Comment — Terry Li

<draft comment text>
EOF
```

Delete gist after Terry confirms it's copied.

---

## Post Mode

### 1. Check Content Ideas (MANDATORY — do not skip)

**Every LinkedIn post draft MUST have an entry in `[[LinkedIn Content Ideas]]` BEFORE any draft file or gist is created.** This is the single source of truth for the content pipeline.

```bash
cat ~/notes/LinkedIn\ Content\ Ideas.md
```

If the topic exists, use the captured angle/details. If new, add the entry first (hook, angle, status, timing gate), then create the draft file linked from it.

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

All posts get consilium `--council` (~$0.50) — posts are public and reputation-building, `--quick` doesn't catch tone/positioning risks. High-stakes posts (first Capco-era, controversial angle) get `--deep` (~$0.90) or `--redteam` (~$0.20) to stress-test the angle.

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
