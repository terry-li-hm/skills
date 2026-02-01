# /// script
# dependencies = ["openai"]
# ///
"""
flash-browse: Cheap browser automation using Gemini Flash via OpenRouter.
Uses agent-browser CLI for browser control, Gemini 2.0 Flash as the brain.
"""

import argparse
import subprocess
import sys
import os

try:
    import openai
except ImportError:
    print("Run with: uv run flash_browse.py", file=sys.stderr)
    sys.exit(1)


SYSTEM_PROMPT = """You control a browser via agent-browser CLI. Output exactly ONE command per turn.

Commands:
  click @e5        Click element with ref=e5
  type @e3 "text"  Type text into element with ref=e3
  scroll down      Scroll down
  scroll up        Scroll up
  wait 2000        Wait 2 seconds
  done [message]   Task complete, optional final message

Examples:
  Snapshot: button "Submit" [ref=e7]
  Task: click submit → Output: click @e7

  Snapshot: textbox "email" [ref=e4]
  Task: enter test@example.com → Output: type @e4 "test@example.com"

  Task complete → Output: done The form was submitted successfully

Rules:
- Output ONLY the command, no explanation
- Use exact @ref values from the snapshot
- Say 'done' when the task is complete or cannot proceed"""


def run_agent_browser(cmd: list[str], verbose: bool = False) -> str:
    """Run an agent-browser command and return output."""
    full_cmd = ["agent-browser"] + cmd
    if verbose:
        print(f"  → {' '.join(full_cmd)}", file=sys.stderr)

    result = subprocess.run(full_cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_snapshot(verbose: bool = False) -> str:
    """Get accessibility snapshot of current page."""
    return run_agent_browser(["snapshot", "-i", "-c"], verbose)


def execute_command(cmd: str, verbose: bool = False) -> bool:
    """Execute a browser command. Returns True if should continue."""
    cmd = cmd.strip()

    if cmd.startswith("done"):
        message = cmd[4:].strip()
        if message:
            print(f"\nResult: {message}")
        return False

    parts = cmd.split(maxsplit=2)
    if not parts:
        return True

    action = parts[0]

    if action == "click" and len(parts) >= 2:
        run_agent_browser(["click", parts[1]], verbose)
    elif action == "type" and len(parts) >= 3:
        ref = parts[1]
        # Extract text from quotes
        text = parts[2].strip('"\'')
        run_agent_browser(["type", ref, text], verbose)
    elif action == "scroll" and len(parts) >= 2:
        run_agent_browser(["scroll", parts[1]], verbose)
    elif action == "wait" and len(parts) >= 2:
        run_agent_browser(["wait", parts[1]], verbose)
    else:
        if verbose:
            print(f"  Unknown command: {cmd}", file=sys.stderr)

    return True


def main():
    parser = argparse.ArgumentParser(description="Browser automation with Gemini Flash")
    parser.add_argument("--url", required=True, help="URL to open")
    parser.add_argument("--task", required=True, help="Task to perform")
    parser.add_argument("--max-steps", type=int, default=20, help="Max steps (default: 20)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print each step")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Open URL
    if args.verbose:
        print(f"Opening {args.url}...", file=sys.stderr)
    run_agent_browser(["open", args.url], args.verbose)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    for step in range(args.max_steps):
        # Get snapshot
        snapshot = get_snapshot(args.verbose)
        if not snapshot:
            print("Error: Empty snapshot", file=sys.stderr)
            break

        # Build prompt
        user_msg = f"Task: {args.task}\n\nCurrent page snapshot:\n{snapshot}"
        messages.append({"role": "user", "content": user_msg})

        if args.verbose:
            print(f"\nStep {step + 1}:", file=sys.stderr)

        # Ask Gemini
        try:
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-001",
                messages=messages,
                max_tokens=100
            )
            cmd = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling Gemini: {e}", file=sys.stderr)
            break

        if args.verbose:
            print(f"  Gemini: {cmd}", file=sys.stderr)

        messages.append({"role": "assistant", "content": cmd})

        # Execute command
        if not execute_command(cmd, args.verbose):
            break

        # Trim context if getting long
        if len(messages) > 10:
            messages = [messages[0]] + messages[-6:]

    else:
        print(f"Reached max steps ({args.max_steps})", file=sys.stderr)


if __name__ == "__main__":
    main()
