# /// script
# requires-python = ">=3.10"
# ///
"""
chatbot_tester: Deterministic chatbot testing using agent-browser.
No AI in the loop - just systematic question/answer extraction.
"""

import argparse
import subprocess
import sys
import json
import re
import time


def run_browser(cmd: list[str], verbose: bool = False) -> str:
    """Run agent-browser command and return output."""
    full_cmd = ["agent-browser"] + cmd
    if verbose:
        print(f"  → {' '.join(full_cmd)}", file=sys.stderr)
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    return result.stdout.strip()


def find_ref(snapshot: str, pattern: str, exclude_disabled: bool = True) -> str | None:
    """Find ref for element matching pattern (case-insensitive)."""
    for line in snapshot.split('\n'):
        if pattern.lower() in line.lower():
            if exclude_disabled and '[disabled]' in line:
                continue
            match = re.search(r'\[ref=(e\d+)\]', line)
            if match:
                return f"@{match.group(1)}"
    return None


def find_input_ref(snapshot: str) -> str | None:
    """Find the message input textbox specifically."""
    for line in snapshot.split('\n'):
        if 'textbox' in line.lower() and ('message' in line.lower() or 'type' in line.lower()):
            match = re.search(r'\[ref=(e\d+)\]', line)
            if match:
                return f"@{match.group(1)}"
    return find_ref(snapshot, 'textbox')


def extract_response(snapshot: str, question: str = "") -> str:
    """Extract chatbot response from snapshot."""
    lines = []
    in_chat = False
    skip_patterns = [
        "Try asking about",
        "Copy to clipboard",
        "Restart tour",
        "Welcome to",
        "Let me walk you",
        "This uses the public",
        "Responses come from",
    ]

    for line in snapshot.split('\n'):
        # Look for chat message area
        if 'log "Chat messages"' in line or 'Chat messages' in line:
            in_chat = True
            continue

        # Stop at input area
        if 'contentinfo' in line:
            break

        if in_chat:
            # Extract text content (handle quoted and unquoted)
            text_match = re.search(r'- text: ["\']?(.+?)["\']?\s*$', line)
            if text_match:
                text = text_match.group(1).strip().strip('"\'')

                # Skip UI elements and demo text
                if any(skip in text for skip in skip_patterns):
                    continue
                # Skip single bullet points
                if text == '•':
                    continue
                if text:
                    lines.append(text)

            # Also extract link text (chatbot often shows clickable options)
            link_match = re.search(r'- link "([^"]+)"', line)
            if link_match:
                link_text = link_match.group(1)
                if link_text and 'Restart' not in link_text:
                    lines.append(f"  → {link_text}")

    # Return substantive content, removing the echoed question if present
    result_lines = []
    for line in lines:
        # If line contains the question, extract just the response part
        if question and question.lower() in line.lower():
            # Response usually follows the question
            parts = line.lower().split(question.lower())
            if len(parts) > 1 and parts[1].strip():
                result_lines.append(parts[1].strip().capitalize())
        else:
            result_lines.append(line)

    return '\n'.join(result_lines[-6:]) if result_lines else "No response captured"


def test_question(url: str, question: str, verbose: bool = False) -> dict:
    """Test a single question against the chatbot."""
    result = {"question": question, "response": None, "error": None}

    try:
        # Open URL
        run_browser(["open", url], verbose)
        run_browser(["wait", "2000"], verbose)

        # Click New Chat to reset
        snapshot = run_browser(["snapshot", "-i", "-c"], verbose)
        new_chat_ref = find_ref(snapshot, "New Chat")
        if new_chat_ref:
            run_browser(["click", new_chat_ref], verbose)
            run_browser(["wait", "1500"], verbose)  # Wait for page to fully update

        # Find textbox and type question
        snapshot = run_browser(["snapshot", "-i", "-c"], verbose)
        textbox_ref = find_input_ref(snapshot)
        if verbose:
            print(f"  Found textbox ref: {textbox_ref}", file=sys.stderr)
            # Show relevant lines for debug
            for line in snapshot.split('\n'):
                if 'textbox' in line.lower() or 'send' in line.lower():
                    print(f"    {line.strip()}", file=sys.stderr)
        if not textbox_ref:
            result["error"] = "Could not find textbox"
            return result

        run_browser(["fill", textbox_ref, question], verbose)  # fill triggers input events better than type
        run_browser(["wait", "500"], verbose)  # Wait for send button to enable

        # Find and click send button (re-snapshot since fill may enable it and shift refs)
        snapshot = run_browser(["snapshot", "-i", "-c"], verbose)
        send_ref = find_ref(snapshot, "Send message", exclude_disabled=True)
        if not send_ref:
            send_ref = find_ref(snapshot, "Send", exclude_disabled=True)
        if verbose:
            print(f"  Found send ref: {send_ref}", file=sys.stderr)
            for line in snapshot.split('\n'):
                if 'send' in line.lower():
                    print(f"    {line.strip()}", file=sys.stderr)
        if not send_ref:
            result["error"] = "Could not find enabled send button"
            return result

        run_browser(["click", send_ref], verbose)
        run_browser(["wait", "4000"], verbose)  # Longer wait for response

        # Capture response
        snapshot = run_browser(["snapshot", "-c"], verbose)
        result["response"] = extract_response(snapshot, question)

        if verbose:
            print(f"  Raw snapshot length: {len(snapshot)}", file=sys.stderr)

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Deterministic chatbot tester")
    parser.add_argument("--url", required=True, help="Chatbot URL")
    parser.add_argument("--questions", required=True,
                        help="Comma-separated questions OR path to file (one per line)")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show commands")
    args = parser.parse_args()

    # Parse questions
    if ',' in args.questions and not args.questions.endswith('.txt'):
        questions = [q.strip() for q in args.questions.split(',')]
    else:
        try:
            with open(args.questions) as f:
                questions = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            # Treat as single question
            questions = [args.questions]

    results = []

    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] Testing: {question}")
        result = test_question(args.url, question, args.verbose)
        results.append(result)

        if result["error"]:
            print(f"  ❌ Error: {result['error']}")
        else:
            print(f"  ✓ Response: {result['response'][:200]}...")

        # Brief pause between questions
        if i < len(questions):
            time.sleep(1)

    # Summary
    print(f"\n{'='*50}")
    print(f"Tested {len(results)} questions")
    print(f"  Success: {sum(1 for r in results if not r['error'])}")
    print(f"  Failed: {sum(1 for r in results if r['error'])}")

    # Save output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
