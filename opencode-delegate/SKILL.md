---
name: opencode-delegate
description: Delegate coding tasks to OpenCode for background execution. Use when user says "delegate to opencode", "run in opencode", or wants to offload well-defined coding tasks to a cheaper model.
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

### Run headless task (recommended: Gemini 3 Flash High)
```bash
opencode run -m opencode/gemini-3-flash --variant high --title "Task Name" "Detailed prompt"
```

### Run with default model
```bash
opencode run --title "Task Name" "Detailed prompt with clear success criteria"
```

### Resume a session
```bash
opencode -s <session-id>
# Or continue last session:
opencode -c
```

### Find session IDs
```bash
/bin/ls -lt ~/.local/share/opencode/storage/session/
# Then read the session JSON:
cat ~/.local/share/opencode/storage/session/<project-hash>/*.json
```

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

### Recommended: Gemini 3 Flash High
```bash
-m opencode/gemini-3-flash --variant high
```
- Released Dec 2025, "doctorate-level" reasoning
- 3x faster than Gemini 2.5 Pro
- Best balance of speed, cost, and capability

### Available Models
| Model | SWE-bench | Use Case |
|-------|-----------|----------|
| `opencode/gemini-3-flash` | 78.0% | Fast, cheap, good for most tasks |
| `opencode/glm-4.7` | 73.8% | Bilingual (TC/SC/EN), multilingual codebases |
| `opencode/gemini-3-pro` | 76.2% | More capable, slower |
| `opencode/claude-sonnet-4-5` | 77.2% | When you need Claude quality |
| `opencode/gpt-5.2-codex` | — | Alternative for coding tasks |

### GLM-4.7 (智谱清言)
```bash
-m opencode/glm-4.7
```
- **SWE-bench Multilingual: 66.7%** — best for TC/SC/EN mixed codebases
- LiveCodeBench V6: 84.9 (beats Claude Sonnet 4.5)
- Preserved Thinking: keeps reasoning across agentic turns
- Terry has Coding Max annual plan (valid to 2027-01-28) — unlimited quota
- Good for: bank-faq-chatbot, bilingual projects, Chinese documentation

### Model Selection Tips
- **Speed-critical**: Gemini 3 Flash
- **Bilingual codebase**: GLM-4.7
- **Accuracy-critical banking**: Verify outputs from Gemini 3 Flash (higher hallucination rate)

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

## Error Handling

OpenCode often self-recovers from errors by:
1. Reading error output
2. Editing the problematic code
3. Retrying

If it fails repeatedly on the same error, take over interactively.
