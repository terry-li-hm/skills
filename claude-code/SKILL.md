---
name: claude-code
description: High-reasoning agentic operations via the Claude Code CLI (Opus 4.5). Use for complex analysis, structural coding tasks, and strategic decision making that requires the Max reasoning plan.
requires: bin:claude
---

# Claude Code

This skill provides a programmatic bridge to the Claude Code CLI, allowing OpenClaw to delegate high-stakes tasks to Opus 4.5.

## Usage

1. **Direct Task:**
   - Use `exec` to call `claude --dangerously-skip-permissions "<task>"`
   - Always include context relevant to the task (e.g., specific file paths or vault locations).

2. **Integration Patterns:**
   - **Job Evaluation:** `claude "evaluate-job <URL> --vault ~/notes"`
   - **Strategic Synthesis:** `claude "Review the last 3 interview debriefs in ~/notes and synthesize my primary weak points."`

## Best Practices

- **Skip Permissions:** Always use `--dangerously-skip-permissions` for background/cron runs to avoid TTY stalls.
- **Model Lock:** If specific reasoning is required, explicitly prompt Claude Code to use "Opus" or "4.5" within the task string.
- **Reporting:** Instruct Claude to write its output to a specific file or the vault so OpenClaw can retrieve and relay the results.

