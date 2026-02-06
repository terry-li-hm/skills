---
name: warp-cli
description: Run Warp Ambient Agents via CLI. Use when delegating coding tasks to Warp's agents, running background agents on remote environments, or integrating Warp agents into automated workflows. Trigger phrases: "warp agent", "run with warp", "use warp".
github_url: https://docs.warp.dev/reference/cli/cli
---

# Warp CLI

Warp CLI is the command-line tool that lets you run [Ambient Agents](https://docs.warp.dev/agent-platform/ambient-agents/ambient-agents-overview) from anywhere — terminals, scripts, automated systems, or services.

## Installation

### Bundled with Warp
If you have Warp desktop app installed, CLI is included. To add to PATH:

**macOS:** Open Command Palette (CMD+P), select `Install Warp CLI Command`

**Standalone (macOS):**
```bash
brew tap warpdotdev/warp
brew install --cask warp-cli
```

## Authentication

### Interactive (local)
```bash
warp login
# Opens browser to authenticate
```

### API Key (automated)
```bash
export WARP_API_KEY="wk-xxx..."
```

Generate keys in Warp → Settings → Platform → API Keys

## Common Usage Patterns

### Local Agent Run
```bash
# Basic local execution
warp agent run --prompt "summarize this directory"

# Run from different directory
warp agent run --cwd /path/to/dir --prompt "fix the tests"

# Share session with team
warp agent run --share team:edit --prompt "implement feature X"
```

### Using Agent Profiles
```bash
# List available profiles
warp agent profile list

# Run with specific profile
warp agent run --profile <PROFILE_ID> --prompt "analyze this codebase"
```

### With MCP Servers
```bash
# List available MCP servers
warp mcp list

# Run with GitHub MCP
warp agent run --mcp-server <MCP_UUID> --prompt "who last updated README?"
```

### Using Saved Prompts
```bash
# Run saved prompt by ID (from Warp Drive URL)
warp agent run --saved-prompt sgNpbUgDkmp2IImUVDc8kR
```

### Remote/Ambient Run
```bash
warp agent run-ambient \
  --environment <ENVIRONMENT_ID> \
  --name "Repo summary" \
  --prompt "Summarize this repo and list the top 5 risky areas" \
  --open
```

## Key Flags

| Flag | Description |
|------|-------------|
| `--prompt` | Agent task description |
| `--cwd` | Run from different directory (local only) |
| `--profile` | Use specific agent profile |
| `--mcp-server` | Start MCP server(s) by UUID |
| `--saved-prompt` | Use saved prompt from Warp Drive |
| `--share` | Share session with users/team |
| `--open` | Open session in Warp (ambient runs) |

## When to Use vs OpenCode

| Warp CLI | OpenCode |
|----------|----------|
| Background/ambient tasks | Bulk file operations |
| Remote environments | Refactoring, tests |
| MCP integration (GitHub, Linear) | Simple execution |
| Session sharing | Free, unlimited quota |

## Troubleshooting

**CLI not found:** Check installation path and verify version: `warp --version`

**Auth issues:** Ensure `warp login` completed or `WARP_API_KEY` is set correctly

**Agent/MCP errors:** Verify agent profile permissions and MCP server configuration
