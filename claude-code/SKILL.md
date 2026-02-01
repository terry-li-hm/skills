---
name: claude-code
description: High-reasoning agentic operations via the Claude Code CLI (Opus 4.5). MUST use --dangerously-skip-permissions for all background tasks. Use for complex analysis and strategic decisions.
user_invocable: true
---

# Claude Code

Programmatic bridge to the Claude Code CLI, delegating high-stakes reasoning tasks to Opus 4.5.

## When to Use

- **Strategic Analysis**: Evaluating job fit, synthesizing interview signals, or career planning.
- **Structural Coding**: Large-scale refactors or complex debugging that exceeds GLM-4.7 capabilities.
- **Max Reasoning**: Any task where the "Consultant" persona is required over the "Mechanical" one.

## Usage Patterns

| Task Type | Command Pattern | Reference Skill |
|-----------|-----------------|-----------------|
| Job Eval | `claude --dangerously-skip-permissions "evaluate-job <URL> --vault ~/notes"` | `evaluate-job` |
| Strategic Review | `claude --dangerously-skip-permissions "Analyze [[Active Pipeline]] for blockers"` | `vault-pathfinding` |
| Code Audit | `claude --dangerously-skip-permissions "Run a security audit on ./src"` | `codebase-cleanup` |

## Best Practices

- **Zero-Interaction**: Always include `--dangerously-skip-permissions` in `exec` calls to prevent hanging on TTY prompts during background/cron runs.
- **Explicit Model**: Instruct Claude Code within the prompt string to use "Opus" or "4.5" for high-stakes reasoning.
- **Reporting**: Always instruct Claude to write output to a specific vault path so it can be retrieved by OpenClaw.

## Related Skills

- `llm-routing` — Guidance on when to escalate to Claude Code vs OpenCode.
- `evaluate-job` — Primary consumer of the Claude Code bridge.
- `vault-pathfinding` — Standard paths for reading/writing results.
