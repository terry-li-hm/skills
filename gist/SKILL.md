---
name: gist
description: Create, update, and manage secret GitHub gists. Use when sharing code/text for mobile copy-paste, or when user says "gist", "/gist".
user_invocable: true
---

# Gist Management

All gists MUST be secret (`--public=false`). Never create public gists.

## Operations

### Create

```bash
gh gist create --public=false -f <filename> <filepath> -d "<description>"
```

**Always write content to `/tmp/<filename>` first, then create from that path.** Never pipe content via `<<<`, `printf`, or `echo` — zsh escapes `!` and other metacharacters even in single quotes, resulting in `boss\!` instead of `boss!` in the gist.

### Update

**`gh gist edit -f <name> < file` silently fails.** Stdin piping does not work — the gist appears updated but content is unchanged.

**Workaround:** Delete and recreate.

```bash
gh gist delete <id> --yes
gh gist create --public=false -f <filename> <filepath> -d "<description>"
```

Always verify after update via API (not `gh gist view`, which can also escape characters):

```bash
gh api gists/<new-id> --jq '.files["<filename>"].content'
```

### List active gists

```bash
gh gist list --limit 20
```

### Cleanup

Delete gists after use. Don't leave drafts, internal notes, or sensitive content in GitHub.

```bash
gh gist delete <id> --yes
```

## When to use gists

- Sharing code/text for Terry to copy from mobile (Blink SSH can't select long inline text)
- Anything longer than 2-3 lines that Terry needs to copy-paste
- Draft messages, step-by-step instructions for CDSW, etc.

## When NOT to use gists

- Short inline answers (just type them)
- Permanent documentation (use vault notes)
- Anything with secrets/credentials (even secret gists are accessible via URL)
