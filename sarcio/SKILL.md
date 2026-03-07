---
name: sarcio
description: >
  Manage the terryli.hm digital garden (sarcio = Latin "to patch/mend").
  Use for creating, publishing, revising, and listing garden posts.
  Source: ~/code/sarcio/. Posts live in ~/notes/Writing/Blog/Published/.
triggers:
  - "garden post"
  - "sarcio"
  - "new post"
  - "publish post"
  - "revise post"
---

# sarcio — Garden CLI

Manages posts in `~/notes/Writing/Blog/Published/`. The sync LaunchAgent
pushes them to `~/code/blog` and live at terryli.hm every 5 min.

## Commands

```bash
# Create a new draft post (opens in $EDITOR)
sarcio new "Title of Post"

# List all posts with date, draft status, word count
sarcio list

# Publish a draft (flips draft: true → false)
sarcio publish <slug>

# Revise a published post (bumps modDatetime, sets revisionNote)
sarcio revise <slug> --note "What changed and why"

# Open a post in $EDITOR
sarcio open <slug>

# Regenerate ~/notes/terryli.hm.md vault index
sarcio index
```

## Workflow

**New post from session insight:**
1. `sarcio new "Title"` — scaffolds with correct frontmatter
2. Write the post (prose style per ~/code/blog/CLAUDE.md)
3. **Run judge** — `article` criteria; fix any `needs_work` before publishing (max 1 iteration)
4. `sarcio publish <slug>` when ready
5. Sync picks it up within 5 min → live at terryli.hm

**Revise an existing post:**
```bash
sarcio revise autonomous-vs-monitored-agents --note "Added Karpathy follow-up example"
```
Shows revised date + note on the post automatically.

**Find the slug:**
```bash
sarcio list | grep <keyword>
```

## Cadence

Flag "garden post?" whenever something interesting surfaces in a session.
Draft to publishable quality; Terry does quick skim only.
Flag factual claims that need verification before publishing.

## Gotchas

- `serde_yaml` is deprecated upstream but works fine — may need migration eventually
- Frontmatter revision uses string matching, not full YAML round-trip — keys must be consistently formatted (no extra whitespace)
- Slug derived from title: lowercase, spaces → `-`, non-alphanumeric stripped
- `sarcio index` regenerates `~/notes/terryli.hm.md` — also runs automatically on every blog sync (via `sync-from-vault.sh`)
- Add `sarcio` to exclude list in `~/code/Cargo.toml` — already done

## Files

- Binary: `~/.cargo/bin/sarcio`
- Source: `~/code/sarcio/`
- Posts: `~/notes/Writing/Blog/Published/`
- Index: `~/notes/terryli.hm.md`
- Sync script: `~/code/blog/sync-from-vault.sh`
