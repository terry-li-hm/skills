---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development (Local Override)

**MARKER FILE — Plugin Skill Override Test**

This file exists to verify whether `~/skills/superpowers/subagent-driven-development/SKILL.md` takes precedence over the plugin-cached version at `~/.claude/plugins/cache/claude-plugins-official/superpowers/*/skills/subagent-driven-development/SKILL.md`.

If you are reading this text, the local override is active. The presence of the phrase "MARKER FILE — Plugin Skill Override Test" confirms that Claude Code loaded this file instead of the plugin version.

## Test Procedure

1. **Ensure this file exists** at `~/skills/superpowers/subagent-driven-development/SKILL.md`
2. **Start a new Claude Code session** (skills load at startup only — reloading mid-session won't work)
3. **Invoke the skill:** type `/superpowers:subagent-driven-development` or trigger it contextually
4. **Check which version loaded:**
   - If the response references "MARKER FILE" or this override text → **local override works**
   - If the response references the full subagent-driven-development workflow (dispatch subagents, two-stage review) → **plugin version loaded, override did NOT work**
5. **Record result** in `~/docs/solutions/skill-architecture-decisions.md` under LRN-20260305-002

## After Testing

- If override **works**: Update LRN-20260305-002 to confirm the mechanism. Consider using it for rector routing.
- If override **does not work**: Confirm the safer alternative (routing in rector) is the correct path. Delete this marker file.
- Either way: remove this marker file after the test is conclusive.
