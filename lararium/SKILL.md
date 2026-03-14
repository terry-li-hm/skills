---
name: lararium
description: Vault-resident personalities CLI — persistent AI characters that live in the Obsidian vault, read notes, develop opinions, and can be conversed with. Use when user says "lararium", "vault residents", "talk to shadow/mirror/etc", or "what are the residents saying".
---

# lararium — Vault Residents

## Commands

```bash
lararium init                    # Create 5 default residents
lararium list                    # Show residents + reading counts
lararium read <name>             # One reading session (3 notes)
lararium read <name> --notes 5   # Read more notes
lararium talk <name>             # Interactive conversation
lararium evolve <name>           # Evolve personality from experience
lararium run                     # Full cycle: all residents read + auto-evolve
```

## Residents

- **mirror** — reflects patterns, names recurring themes
- **shadow** — surfaces what you avoid
- **contrarian** — catches inconsistency between notes
- **archivist** — finds hidden connections
- **stranger** — reads as an outsider

## Data

- Personalities: `~/.local/share/lararium/residents/<name>/personality.md`
- Reading journal: `~/.local/share/lararium/residents/<name>/journal.jsonl`
- Conversations: `~/.local/share/lararium/residents/<name>/exchanges.jsonl`
- Output notes: `~/notes/Lararium/<name>-YYYY-MM-DD.md`

## Schedule

LaunchAgent runs `lararium run` at 8 AM and 8 PM. Each resident reads 2 notes.
Auto-evolves personality every 10 readings.

## Gotchas

- Uses `claude --print --model haiku` for readings (cheap, fast)
- `talk` mode uses haiku too — switch to sonnet if conversations feel flat
- CLAUDECODE env var is unset before subprocess calls
- Vault notes in `~/notes/Lararium/` are append-mode (multiple sessions per day stack)
