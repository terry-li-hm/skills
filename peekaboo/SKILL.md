---
name: peekaboo
description: Capture and automate macOS UI with the Peekaboo CLI. Use when user needs screenshots, UI inspection, mouse/keyboard automation, or app/window management on macOS.
user_invocable: false
github_url: https://github.com/steipete/peekaboo
---

# Peekaboo

macOS UI automation CLI: capture/inspect screens, target UI elements, drive input, and manage apps/windows/menus.

## Prerequisites

- macOS only
- `peekaboo` CLI installed: `brew install steipete/tap/peekaboo`
- Screen Recording + Accessibility permissions granted

## Core Commands

### Screenshots

```bash
# Capture full screen
peekaboo image --screen

# Capture specific window
peekaboo image --window "Safari"

# Capture menu bar region
peekaboo image --menubar
```

### List Apps/Windows

```bash
peekaboo list apps
peekaboo list windows
peekaboo list screens
peekaboo list menubar
peekaboo permissions
```

### Interaction

```bash
# Click by element ID or query
peekaboo click --id "button-123"
peekaboo click --query "Submit Button"
peekaboo click --coords 100,200

# Keyboard
peekaboo type "Hello world"
peekaboo hotkey cmd,shift,t
peekaboo press enter

# Mouse
peekaboo move --coords 100,200
peekaboo scroll down
peekaboo drag --from 100,100 --to 200,200
```

### Capture Video

```bash
peekaboo capture --duration 10 --output video.mp4
```

## JSON Output

Add `--json` or `-j` for machine-readable output.

## Integration

Complements browser automation tools. Use peekaboo for native macOS apps, Claude in Chrome for web pages.
