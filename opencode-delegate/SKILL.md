---
name: opencode-delegate
description: Delegate coding tasks to OpenCode (GLM-4.7) for background execution on cheaper model.
user_invocable: false
---

# OpenCode Delegate

Delegate coding tasks to OpenCode (Gemini/GLM-powered) for background execution.

## When to Use

- **Cost optimization**: Gemini is ~6x cheaper than Opus
- **Parallel work**: Run tasks in background while continuing conversation
- **Well-defined tasks**: Refactoring phases, code extraction, file reorganization
- **Self-recoverable errors**: Tasks where OpenCode can debug its own mistakes

## When NOT to Use

- Tasks requiring user decisions mid-execution
- Errors needing external context (API keys, environment issues)
- Exploratory work where direction is unclear
- Tasks with heavy dependencies on conversation context

## Commands

### Run headless task (default: GLM-4.7 — unlimited quota)
```bash
# Use lean config (no MCPs) for fast ~15s startup
OPENCODE_HOME=~/.opencode-lean opencode run -m zhipuai-coding-plan/glm-4.7 --title "Task Name" "Detailed prompt" &
```

> **⚠️ Provider Matters:** Use `zhipuai-coding-plan/glm-4.7` (BigModel direct) NOT `opencode/glm-4.7` (OpenCode proxy with separate billing).

> **⚠️ Use Lean Config:** `OPENCODE_HOME=~/.opencode-lean` skips MCP servers (gmail, search, browser, etc.) — cuts startup from ~60s to ~15s. Coding tasks don't need MCPs.

**Best practice**: Always append `&` when running from Claude Code. This backgrounds the task so you can continue working or dispatch more tasks in parallel.

### Run with Gemini 3 Flash (fallback for speed)
```bash
OPENCODE_HOME=~/.opencode-lean opencode run -m opencode/gemini-3-flash --variant high --title "Task Name" "Detailed prompt"
```

### Resume a session
```bash
opencode -s <session-id>
# Or continue last session:
opencode -c
```

> **Note:** Resume uses full `opencode` (not lean) since sessions may need MCP access.

### Terminal alias
For quick interactive use from terminal: `ol` (defined in .zshrc) is equivalent to lean config.

### Find session IDs
```bash
/bin/ls -lt ~/.local/share/opencode/storage/session/
# Then read the session JSON:
cat ~/.local/share/opencode/storage/session/<project-hash>/*.json
```

## PII Masking

When delegating prompts that contain personal information, mask first:

```bash
# Mask sensitive info before delegation
cd /Users/terry/skills/pii-mask
masked=$(uv run mask.py "Prompt with terry@email.com and 6187 2354")

# Then delegate the masked version
OPENCODE_HOME=~/.opencode-lean opencode run -m zhipuai-coding-plan/glm-4.7 --title "Task" "$masked"
```

**Preview what gets masked:**
```bash
uv run mask.py --dry-run "Contact Terry at +852 6187 2354"
```

See `/Users/terry/skills/pii-mask/SKILL.md` for details on what gets detected.

## Prompt Engineering for Delegation

Good delegation prompts include:

1. **Clear scope**: "Execute Phase 2 from docs/plans/X.md"
2. **Specific deliverables**: "Create these files: A, B, C"
3. **Verification command**: "Verify by running: python -c '...'"
4. **Constraints**: "Keep existing patterns", "Don't modify X"

### Example Prompt
```
Execute Phase 2 from docs/plans/refactor-plan.md.

Your task: Extract routes into backend/routes/*.py

Create these files:
1. backend/routes/__init__.py - router exports
2. backend/routes/documents.py - /upload, /documents endpoints
3. backend/routes/system.py - /healthz, /stats endpoints

Then update main.py to import and include the routers.

Verify by running: python -c 'from backend.routes import documents_router'
```

## Session Storage

Sessions are persisted at:
```
~/.local/share/opencode/storage/session/
├── <project-hash>/
│   └── ses_<id>.json  # Contains title, summary, timestamps
└── global/
```

Session JSON includes:
- `id`: Session ID for resume
- `title`: Task name
- `summary`: {additions, deletions, files}
- `time`: {created, updated}

## Model Selection

Use `-m <model>` and optionally `--variant <level>` to select model.

### Default: GLM-4.7 (unlimited quota)
```bash
-m zhipuai-coding-plan/glm-4.7
```
- **Terry has Coding Max annual plan (valid to 2027-01-28) — unlimited quota**
- **MUST use `zhipuai-coding-plan/` prefix** — `opencode/glm-4.7` routes through OpenCode billing (has limits)
- SWE-bench Multilingual: 66.7% — best for TC/SC/EN mixed codebases
- LiveCodeBench V6: 84.9 (beats Claude Sonnet 4.5)
- Preserved Thinking: keeps reasoning across agentic turns
- Good for: most tasks, bilingual projects, Chinese documentation

### Fallback: Gemini 3 Flash (speed)
```bash
-m opencode/gemini-3-flash --variant high
```
- Released Dec 2025, "doctorate-level" reasoning
- 3x faster than GLM-4.7
- ⚠️ Higher hallucination rate — verify outputs in accuracy-critical contexts

### Available Models
| Model | SWE-bench | Use Case |
|-------|-----------|----------|
| `zhipuai-coding-plan/glm-4.7` ⭐ | 73.8% | **Default** — unlimited via BigModel |
| `opencode/glm-4.7` | 73.8% | ❌ Has OpenCode billing limits |
| `opencode/gemini-3-flash` | 78.0% | Speed-critical tasks |
| `opencode/gemini-3-pro` | 76.2% | More capable, slower |
| `opencode/claude-sonnet-4-5` | 77.2% | When you need Claude quality |

### Model Selection Tips
- **Default**: `zhipuai-coding-plan/glm-4.7` (unlimited via BigModel Coding Max)
- **Speed-critical**: Gemini 3 Flash
- **Accuracy-critical banking**: Verify outputs from Gemini (higher hallucination rate)
- **⚠️ Avoid**: `opencode/glm-4.7` has separate billing that depletes

### Variant Levels
- `--variant high` — More reasoning effort (recommended)
- `--variant max` — Maximum reasoning (slower, costlier)
- `--variant minimal` — Fastest, least reasoning

## Monitoring Background Tasks

When launched via Claude Code's Bash with `run_in_background`:
```bash
# Check progress
tail -f /private/tmp/claude-501/-Users-terry/tasks/<task-id>.output

# Or use TaskOutput tool with the task ID
```

**⚠️ Output files are often empty** — OpenCode doesn't reliably capture stdout to the task output file. If the file is empty, check the session JSON instead:
```bash
# Find recent sessions for the project
/bin/ls -lt ~/.local/share/opencode/storage/session/<project-hash>/

# Read session summary (shows additions, deletions, files changed)
cat ~/.local/share/opencode/storage/session/<project-hash>/ses_<id>.json
```

The session JSON's `summary` field tells you if OpenCode actually made changes, even when output is empty.

## Error Handling

OpenCode often self-recovers from errors by:
1. Reading error output
2. Editing the problematic code
3. Retrying

If it fails repeatedly on the same error, take over interactively.

## Compound Engineering Integration

**Best pattern for complex features**: Claude plans, OpenCode executes.

### The Workflow

```
Claude (Planning)                    OpenCode (Execution)
─────────────────                    ────────────────────
/frontier-council
    ↓ (architecture deliberation)
/workflows:plan
    ↓ (structured plan created)
Review plan ──────────────────────→  Execute Phase 1
                                         ↓
                                     Execute Phases 2-4 (parallel)
                                         ↓
/workflows:review ←───────────────  Return results
    ↓
/compound (document learnings)
```

### Why Split This Way?

| Task Type | Tool | Reason |
|-----------|------|--------|
| Architecture decisions | Claude | High-judgment, trade-offs |
| Council deliberation | Claude | Multi-model synthesis |
| Structured planning | Claude | Context aggregation |
| File reads/writes | OpenCode | Bulk work, free |
| Refactoring | OpenCode | Mechanical transforms |
| Code review | Claude | Pattern recognition |

### Execution Pattern

After creating a plan with Claude:

```bash
# Execute phases sequentially (use lean config for fast startup)
OPENCODE_HOME=~/.opencode-lean opencode run -m zhipuai-coding-plan/glm-4.7 --title "Phase 1" \
  "Execute Phase 1 from docs/plans/YYYY-MM-DD-plan.md.
   Read the plan first, then implement."

# Or parallel for independent phases
OPENCODE_HOME=~/.opencode-lean opencode run -m zhipuai-coding-plan/glm-4.7 --title "Phase 2" "Execute Phase 2..." &
OPENCODE_HOME=~/.opencode-lean opencode run -m zhipuai-coding-plan/glm-4.7 --title "Phase 3" "Execute Phase 3..." &
wait
```

### Key Insight

**Plans are prompts.** A well-structured plan (`/workflows:plan`) is essentially a detailed prompt for OpenCode. Include:
- Exact file paths
- Code snippets to create
- Verification commands
- Constraints and patterns to follow

### Cost Comparison

| Approach | Cost (complex feature) |
|----------|------------------------|
| All in Opus | $5-10 |
| Claude plan + OpenCode execute | $2-3 |
| All in OpenCode | $0 but lower quality planning |

The sweet spot: Claude for judgment, OpenCode for execution.
