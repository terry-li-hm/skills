---
name: budding
description: Manage the terryli.hm garden — create, publish, revise, list posts. Use for any garden post work.
model: sonnet
triggers:
  - "garden post"
  - "publish"
  - "new post"
  - "publish post"
  - "revise post"
context: fork
---

# publish — Garden CLI

Manages posts in `~/notes/Writing/Blog/Published/`. LaunchAgent syncs to `~/code/blog` and terryli.hm every 5 min.

## Commands

```bash
publish new "Title of Post"           # Create draft
publish list                          # List all posts
publish publish <slug>                # Flip draft → published
publish publish <slug> --push         # Publish + sync immediately
publish push                          # Sync now (bypass 5-min daemon)
publish revise <slug> --note "Why"    # Bump modDatetime + note
publish open <slug>                   # Open in $EDITOR
publish index                         # Regenerate ~/notes/terryli.hm.md
```

## Workflow

1. `publish new "Title"` — scaffolds with frontmatter
2. Write the post (prose style per ~/code/blog/CLAUDE.md)
3. **Skip judge for standard garden posts.** Only run judge for: factual claims, sensitive topics, front-stage content.
4. `publish publish <slug> --push` — **run in background** (fire and forget)

**Brainstorming:** Skip full transcription skill. One angle-check question max, then draft. Garden posts are low-risk.

## Auto-Publish Protocol

Draft autonomously when ALL of:
- Non-obvious observation emerged naturally
- Clear one-sentence thesis
- Terry's lane: AI, work, tools, personal systems, consulting
- No factual claims needing verification
- No real names, companies, or time-sensitive content
- **Insider test:** Would details identify the author at a specific institution? If yes → generalise.

## Telemetry

After publishing, append one row to `~/notes/Meta/Content Telemetry.md`:

```
| {date} | garden | {slug} | {title} | {source-skill} | {tags} |
```

- **date**: ISO date (YYYY-MM-DD)
- **slug**: the publish slug
- **title**: post title
- **source-skill**: which skill triggered this (e.g. `budding`, `expression`, `exocytosis`)
- **tags**: frontmatter tags as comma-separated string

If the file doesn't exist, create it with this header first:

```markdown
# Content Telemetry

| date | channel | slug | title | source-skill | tags |
|------|---------|------|-------|--------------|------|
```

## Gotchas

- `publish new` scaffolds with `draft: true`. Use `publish publish <slug>` to go live.
- Slug derived from title: lowercase, spaces → `-`, non-alphanumeric stripped.
- **Quality degrades after ~5 posts per session.** Cap at 5.
- Binary: `~/bin/publish` (Python). Posts: `~/notes/Writing/Blog/Published/`.
