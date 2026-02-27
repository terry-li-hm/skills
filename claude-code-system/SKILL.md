---
name: system-design
description: Architecture of the Claude Code enforcement and knowledge system. Consult when adding hooks, rules, or deciding where knowledge lives.
---

# System Design

How the Claude Code setup enforces rules, stores knowledge, and compounds learning. Consult before adding a new hook, rule, or knowledge artifact.

## Architecture Overview

Five layers, three hard gates, two soft gates:

| Layer | Mechanism | Strength | Adds friction? |
|-------|-----------|----------|----------------|
| OS Sandbox | Kernel filesystem/network restrictions | Hard gate | Silent |
| Hooks (bash-guard.js) | PreToolUse code, exit 2 = block | Hard gate | Deny message |
| Permission rules | settings.json deny/ask/allow | Hard gate | Prompt |
| CLAUDE.md + MEMORY.md | Always in context, every turn | Soft gate | None |
| Skills + Vault | Loaded on demand | Soft gate | None |

Full details: `~/docs/solutions/enforcement-ladder.md`

## When to Hook vs When to Rule

**Hook immediately (first violation)** if ALL of these are true:
- Mechanically enforceable (regex pattern on a Bash command)
- Near-zero false positives (unambiguous signal)
- The deny message can teach the correct alternative

Examples: tool selection (resurface not python), command flags (--chat with wacli), dangerous ops (safe_rm before rm -rf).

**MEMORY.md rule first** if ANY of these are true:
- Detection is fuzzy or context-dependent
- Judgment is required (tone, approach, timing)
- No clean Bash command to intercept

Escalate to hook after 2 entries in `~/docs/solutions/rule-violation-log.md`.

**Why lean aggressive on hooks:** Hooks fire on an AI agent, not humans. No morale cost, no workaround culture. The deny message is the teaching mechanism. False positives are cheap — explain and adjust. (Oxford council, Feb 2026.)

## Where Knowledge Lives

| Type | Location | Loaded | Example |
|------|----------|--------|---------|
| Hard rule ("always/never") | CLAUDE.md | Every turn | "Never run tccutil reset" |
| Gotcha ("X breaks when Y") | MEMORY.md | Every turn | "Glob ** on ~ times out" |
| Procedure (trigger + steps) | Skill | On invocation | `/wrap`, `/morning` |
| Deep reference | `~/docs/solutions/` | On lookup | Browser automation patterns |
| Project context | Vault notes | On lookup | `[[Capco Transition]]` |
| Conversation memory | Oghma | Via `km-ask` | "What did we discuss about X" |
| Vault semantic search | QMD | Via `km-ask` | Note discovery |

**The one-sentence test:** If it fits in one sentence → MEMORY.md. If it has a trigger + multiple steps → skill. If it's deep reference → solutions. See `design-skill` for full placement heuristics.

**MEMORY.md budget:** 200-line hard truncation, **150-line target**. Currently ~120 lines with 30-line buffer. Overflow doc: `~/docs/solutions/memory-overflow.md`.

**Three tiers of permanence:**
- **Permanent** — errors I'd repeat weekly without the reminder (date/time, specs, grep scoping). Never demote.
- **Active** — gotchas tied to current projects or tools. Demote when project ends or tool changes.
- **Provisional** — single-incident lessons. If not cited in 2 weeks → demote to overflow doc.

**Weekly review (in `/weekly`):** Scan MEMORY.md entries against the week's sessions. Any provisional entry not cited this week gets flagged. Two consecutive weeks uncited → demote to `~/docs/solutions/memory-overflow.md`. Overflow entries cited 2+ weeks running → promote back. At ~120 lines, review takes ~2 minutes — if it feels slow, the file is too long.

## Hook Design Patterns

All hooks live in `~/.claude/hooks/`, configured in `~/.claude/settings.json`.

### bash-guard.js (PreToolUse, Bash only)

Pattern: regex match on `data.tool_input.command`, call `deny(reason)` to block.

```javascript
// Good: high-precision, unambiguous signal, teaches the alternative
if (/\.claude\/projects\//.test(cmd) && /\.jsonl/.test(cmd)) {
  deny('Use `resurface search "query" --deep` instead of hand-parsing session JSONL files.');
}

// Bad: too broad, would block legitimate uses
if (/python3/.test(cmd)) {
  deny('Don\'t use Python.');  // False positive nightmare
}
```

**Design rules:**
- Deny message MUST include the correct alternative (not just "don't do this")
- Test with `echo '{"tool_input":{"command":"..."}}' | node ~/.claude/hooks/bash-guard.js`
- Hooks are cached at session start — edits take effect next session
- Never use `npx` fallbacks in hooks — latency fires on every edit

### PostToolUse hooks

Run formatters after edits: prettier (JS/TS), tsc (TS), ruff (Python). Keep fast — they fire on every tool call.

## Enforcement Anti-Patterns

- **Rule without enforcement path:** "Be concise" in MEMORY.md with no way to detect violations. Either accept it's advisory or find a hookable proxy.
- **Hook without deny message:** Silent blocks confuse the agent. Always explain what to do instead.
- **Duplicated rules:** Same rule in MEMORY.md AND a skill AND solutions. Pick one canonical location, reference from others.
- **MEMORY.md bloat:** Budget is ~150 lines (120 current). Aggressive hooks *reduce* MEMORY.md pressure by moving enforcement to a hard gate. Overflow → `~/docs/solutions/memory-overflow.md`.
- **Soft rule for a hard problem:** If the same MEMORY.md rule gets violated twice, it's proven that soft guidance isn't enough. Don't add a third line to MEMORY.md — build a hook.
- **Over-engineering hooks for one-time mistakes:** Not every error is a pattern. If it won't recur, don't hook it.

## Learning Capture Flow

```
Discovery during session
    ↓
UserPromptSubmit hook reminds: "capture non-obvious learnings"
    ↓
Route to most specific location:
    Tool gotcha → ~/docs/solutions/
    Cross-session context → MEMORY.md
    Skill workflow → the skill's SKILL.md
    Rule violation → ~/docs/solutions/rule-violation-log.md
    ↓
/wrap meta-sweep catches anything missed
    ↓
Weekly /skill-review checks for staleness
```

## Compounding Patterns

- **Instance → Pattern → Principle:** Most learnings stop at instance. Explicitly ask "is this a pattern?" after the third occurrence.
- **Promote Oghma hits to MEMORY.md:** If km-ask surfaces the same Oghma memory 3+ times, it's stable enough for MEMORY.md.
- **Demote stale MEMORY.md entries:** Weekly review in `/weekly`. Two weeks uncited → demote to overflow. Overflow cited 2+ weeks → promote back.
- **Hook as MEMORY.md pressure relief:** Every rule that graduates to a hook is one fewer line competing for attention in MEMORY.md.

## See Also

- `~/docs/solutions/enforcement-ladder.md` — full ladder with examples
- `~/docs/solutions/rule-violation-log.md` — violation tracking
- `~/skills/design-skill/SKILL.md` — how to design skills
- `~/notes/Councils/LLM Council - Hook-First Enforcement - 2026-02-27.md` — Oxford debate on hook aggressiveness
