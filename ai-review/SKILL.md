---
name: ai-review
description: Weekly and monthly AI landscape review for consulting conversations. Use when user says "ai review", "ai landscape", "what's happening in AI", or on Fridays alongside weekly review.
user_invocable: true
---

# AI Landscape Review

Synthesize AI developments into opinionated, client-ready talking points. Not a news dump — a consultant's briefing.

## Trigger

- "ai review", "ai landscape", "what's happening in AI"
- Friday weekly reviews (suggest alongside `/weekly`)
- Before client meetings or interviews
- First Friday of month triggers deep monthly review

## Lens: AI Solution Lead at Capco

Every item passes through: **"Would this change how I advise a bank CTO this week?"**

Filter categories:
1. **Model & infrastructure shifts** — new capabilities that unlock use cases (not benchmarks for their own sake)
2. **Regulatory & governance** — HKMA, MAS, EU AI Act, OCC guidance
3. **Banking-specific AI** — fraud, credit, ops, customer service, document processing
4. **Agentic / coding AI** — what Capco's delivery teams should know
5. **China ecosystem** — relevant for HK-based clients with mainland exposure

## Output: `~/notes/AI Landscape.md`

Single persistent note, always fresh. Structure:
- **Current Landscape** (top) — overwritten each monthly review
- **Weekly Snapshots** — appended weekly, reverse-chronological
- **Monthly Reviews** — appended monthly, reverse-chronological

## Weekly Review (light, ~10 min)

Run every Friday or on demand.

### Step 1: Gather

- Read `[[AI News Log]]` entries from the past 7 days
- Check `/ai-news` state: `~/.cache/ai-news-state.json` for last scan
- If log is stale (>3 days no entries), flag cron issue but proceed with what's there
- **Always supplement with 2-3 WebSearches** to backfill gaps (crons break, log may be partial):
  - "AI news banking financial services [month] [year]"
  - "HKMA AI regulation [month] [year]"
  - "major AI announcements [date range]"
- Track provenance: note which items came from the log vs live search. Terry will ask.

### Step 2: Synthesize

Pick 3-5 most significant items. For each:
- **What happened** (1 sentence)
- **So what for banking clients** (1 sentence)
- **Source** (link if available)

Skip anything that's just a version bump, benchmark improvement, or PR announcement without substance.

### Step 3: Write snapshot

Append to `[[AI Landscape]]` under `## Weekly Snapshots`:

```markdown
### Week of YYYY-MM-DD

**Top developments:**
1. [Development] — [Banking implication]. ([Source])
2. ...

**Also notable (from [[AI News Log]]):**
- [Items that didn't make top 5 but worth tracking — 3-5 bullet points]

**Pattern watch:** [Any recurring theme across sources this week]

**Worth reading in full:** [0-2 links to genuinely good articles]

**Sources:** [X items from AI News Log, Y from live WebSearch]
```

### Step 4: Suggest

Cross-reference findings with active pipeline:
- Check `~/notes/TODO.md` for upcoming meetings/interviews
- Check `[[Capco Transition]]` for HSBC engagement prep
- If a development is particularly relevant to an upcoming meeting, interview, or client, flag it explicitly with the specific talking point and where to use it
- For interview prep notes (e.g. `[[DBS Data Management Interview Prep]]`), add a "Fresh intel" section with 3-4 bullet points and a best drop point

### Step 5: Update Current Landscape (first run + monthly)

On **first run** (Current Landscape section is empty), populate Hot Takes, Client Questions, and Should-Be-Asking sections based on the weekly synthesis. On subsequent weekly runs, leave Current Landscape alone — it's refreshed monthly only.

## Monthly Review (deep, ~30 min)

Run on first Friday of each month.

### Step 1: Gather broadly

- Read all weekly snapshots from the past month
- Read `[[AI News Log]]` for the full month
- WebSearch for: "AI in banking [month] 2026", "HKMA AI [month]", "AI regulation Asia 2026"
- Check Evident Banking Brief for bank AI rankings/news (scrape `evidentinsights.com/bankingbrief/` — no RSS, email unsubscribed)

### Step 2: Thematic synthesis

Identify 3-5 **themes** (not events). A theme is a direction, not a headline.

Bad: "Anthropic released Opus 4.6"
Good: "The coding agent gap is closing — implications for bank software delivery"

For each theme:
- **What's shifting** (2-3 sentences)
- **Evidence** (specific developments from the month)
- **Banking implication** (what this means for Capco clients)
- **Contrarian take** (what the consensus gets wrong, or what's overhyped)
- **Talking point** (one sentence you'd say to a client CTO)

### Step 3: Update Current Landscape

**Overwrite** the "Current Landscape" section in `[[AI Landscape]]`:
- Refresh "Hot Takes" with 3-5 defensible positions
- Refresh "What Clients Are Asking About"
- Refresh "What Clients Should Be Asking About (But Aren't)"

### Step 4: Archive

Append the full monthly review under `## Monthly Reviews`:

```markdown
### YYYY-MM — [Month Theme Title]

#### Themes

**1. [Theme]**
- Shift: ...
- Evidence: ...
- Banking implication: ...
- Contrarian: ...
- Talking point: "..."

**2. [Theme]**
...

#### Radar

- **Accelerating:** [trends gaining momentum]
- **Plateau:** [overhyped, slowing down]
- **Emerging:** [early signals worth watching]

#### Key Numbers

- [2-3 statistics worth remembering for conversations]
```

## Integration with Other Skills

- `/weekly` should suggest `/ai-review` on Fridays
- `/ai-news` feeds the raw material; this skill synthesizes it
- `/meeting-prep` can reference `[[AI Landscape]]` for talking points

## Anti-Patterns

- **Don't be comprehensive.** 5 opinionated items beats 20 neutral summaries.
- **Don't benchmark-chase.** "Model X scores 3% higher on HumanEval" is not a talking point.
- **Don't repeat the news log.** This adds the "so what" layer.
- **Don't hedge everything.** Take positions. A consultant who says "it depends" adds no value.
