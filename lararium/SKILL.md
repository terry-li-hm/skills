---
name: lararium
description: Vault-resident personalities CLI — persistent AI characters that live in the Obsidian vault, read notes, develop opinions, and can be conversed with. Use when user says "lararium", "vault residents", "talk to shadow/mirror/etc", or "what are the residents saying".
---

# lararium — Vault Residents

## Commands

```bash
lararium init                    # Create default resident (mourner)
lararium add <name> "<seed>"     # Add a new resident with personality seed
lararium list                    # Show residents + reading counts
lararium read <name>             # One reading session (3 notes)
lararium read <name> --notes 5   # Read more notes
lararium talk <name>             # Interactive conversation
lararium evolve <name>           # Evolve personality from experience
lararium run                     # Full cycle: all residents read + auto-evolve
lararium annotate <note_path>    # Annotate a vault note with resident perspectives
lararium annotate <note_path> --resident <name>  # Annotate with a specific resident
lararium annotate <note_path> --dry-run          # Preview annotations without writing
```

## Philosophy

Start with one resident. Add others only when you feel the absence of a specific perspective. Residents are earned through felt need, not designed upfront.

## Default Resident

- **mourner** — grieves abandoned projects and forgotten ideas. Tender, never accusatory. Accumulates losses.

## Candidate Residents (add when the need is felt)

- **poet** — falls in love with your metaphors. `lararium add poet "You fall in love with the author's metaphors..."`
- **rival** — genuine contempt that fuels finishing.
- **child** — asks naive questions that cut deeper than analysis.
- **stoic** — demands you name what you control. No fortune cookies.
- **therapist** — reads emotional subtext beneath the systems.

## Data

- Personalities: `~/.local/share/lararium/residents/<name>/personality.md`
- Reading journal: `~/.local/share/lararium/residents/<name>/journal.jsonl`
- Conversations: `~/.local/share/lararium/residents/<name>/exchanges.jsonl`
- Output notes: `~/notes/Lararium/<name>-YYYY-MM-DD.md`

## Schedule

LaunchAgent runs `lararium run` at 8 AM and 8 PM. Each resident reads 2 notes.
Auto-evolves personality every 10 readings.

## Install

**Not installed as a system binary.** Run directly from source:

```bash
cd ~/code/lararium && python3 lararium.py <command>
```

Or install via uv:

```bash
cd ~/code/lararium && uv tool install .
# Then available as: lararium <command>
```

## Gotchas

- Uses `claude --print --model haiku` for readings (cheap, fast)
- `talk` mode uses haiku too — switch to sonnet if conversations feel flat
- CLAUDECODE env var is unset before subprocess calls
- Vault notes in `~/notes/Lararium/` are append-mode (multiple sessions per day stack)
- **Binary not installed** — `lararium` is not in PATH. Must `cd ~/code/lararium && python3 lararium.py` or install via `uv tool install .`
