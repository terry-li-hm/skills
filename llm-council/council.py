#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""
LLM Council - Multi-model deliberation via OpenRouter.

5 frontier models debate a question and a judge synthesizes the consensus.
Models: Claude Opus 4.5, GPT-5.2, Gemini 3 Pro, Grok 4, Kimi K2 Thinking

Usage:
    uv run council.py "Should I use microservices or monolith?"
    uv run council.py "your question" --rounds 2
"""

import argparse
import httpx
import os
import re
import sys
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model configurations (all via OpenRouter)
COUNCIL = [
    ("Claude", "anthropic/claude-opus-4.5"),
    ("GPT", "openai/gpt-5.2-pro"),
    ("Gemini", "google/gemini-3-pro-preview"),
    ("Grok", "x-ai/grok-4"),
    ("Kimi", "moonshotai/kimi-k2-thinking"),
]

JUDGE_MODEL = "anthropic/claude-opus-4.5"

# Thinking models don't stream well - use non-streaming for these
THINKING_MODELS = {"gemini-3-pro", "kimi-k2-thinking", "deepseek-r1", "o1", "o3"}


def is_thinking_model(model: str) -> bool:
    """Check if model is a thinking model that doesn't stream well."""
    model_lower = model.lower()
    return any(tm in model_lower for tm in THINKING_MODELS)


def query_model(
    api_key: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 1500,  # Higher for thinking models (reasoning + content)
    timeout: float = 120.0,
    stream: bool = False,
    retries: int = 2,  # Retry for thinking models that can be flaky
) -> str:
    """Query a model via OpenRouter with retry logic for flaky models."""
    # Thinking models don't stream well - fall back to non-streaming
    if stream and not is_thinking_model(model):
        return query_model_streaming(api_key, model, messages, max_tokens, timeout)

    # Retry logic for thinking models (can be flaky via OpenRouter)
    for attempt in range(retries + 1):
        response = httpx.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
            },
            timeout=timeout,
        )

        if response.status_code != 200:
            if attempt < retries:
                continue  # Retry on HTTP errors
            return f"[Error: HTTP {response.status_code} from {model}]"

        data = response.json()

        if "error" in data:
            if attempt < retries:
                continue  # Retry on API errors
            return f"[Error: {data['error'].get('message', data['error'])}]"

        if "choices" not in data or not data["choices"]:
            if attempt < retries:
                continue  # Retry on empty choices
            return f"[Error: No response from {model}]"

        content = data["choices"][0]["message"]["content"]

        # Check for empty content (thinking models can return empty)
        if not content or not content.strip():
            if attempt < retries:
                continue  # Retry on empty content
            return f"[No response from {model} after {retries + 1} attempts]"

        # Clean up reasoning model outputs (DeepSeek R1's <think> tags)
        if "<think>" in content:
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

        return content

    return f"[Error: Failed to get response from {model}]"


def query_model_streaming(
    api_key: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 1500,  # Higher for thinking models
    timeout: float = 120.0,
) -> str:
    """Query a model with streaming output - prints tokens as they arrive."""
    import json as json_module

    full_content = []
    in_think_block = False
    error_msg = None

    try:
        with httpx.stream(
            "POST",
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "stream": True,
            },
            timeout=timeout,
        ) as response:
            # Check for HTTP errors
            if response.status_code != 200:
                error_msg = f"[Error: HTTP {response.status_code} from {model}]"
            else:
                for line in response.iter_lines():
                    if not line or line.startswith(":"):
                        continue  # Skip empty lines and SSE comments

                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        if data_str.strip() == "[DONE]":
                            break

                        try:
                            data = json_module.loads(data_str)
                            # Check for API error in response
                            if "error" in data:
                                error_msg = f"[Error: {data['error'].get('message', data['error'])}]"
                                break

                            if "choices" in data and data["choices"]:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    # Handle <think> blocks - don't print them
                                    if "<think>" in content:
                                        in_think_block = True
                                    if in_think_block:
                                        if "</think>" in content:
                                            in_think_block = False
                                            content = content.split("</think>", 1)[-1]
                                        else:
                                            continue  # Skip content inside think block

                                    if content:
                                        print(content, end="", flush=True)
                                        full_content.append(content)
                        except json_module.JSONDecodeError:
                            pass  # Skip malformed JSON

    except httpx.TimeoutException:
        error_msg = f"[Error: Timeout from {model}]"
    except httpx.RequestError as e:
        error_msg = f"[Error: Request failed for {model}: {e}]"

    print()  # Newline after streaming completes

    # Handle errors or empty responses
    if error_msg:
        print(error_msg)
        return error_msg

    if not full_content:
        empty_msg = f"[No response from {model}]"
        print(empty_msg)
        return empty_msg

    return "".join(full_content)


def detect_consensus(conversation: list[tuple[str, str]], council_size: int) -> tuple[bool, str]:
    """Detect if council has converged. Returns (converged, reason)."""
    if len(conversation) < council_size:
        return False, "insufficient responses"

    recent = [text for _, text in conversation[-council_size:]]

    # Check for explicit CONSENSUS signals
    consensus_count = sum(1 for text in recent if "CONSENSUS:" in text.upper())
    if consensus_count >= council_size - 1:  # 4 of 5
        return True, "explicit consensus signals"

    # Check for strong agreement language (avoid false positives from "building on")
    agreement_phrases = ["i agree with", "i concur", "we all agree", "consensus emerging"]
    agreement_count = sum(
        1 for text in recent
        if any(phrase in text.lower() for phrase in agreement_phrases)
    )
    if agreement_count >= council_size - 1:
        return True, "agreement language detected"

    return False, "no consensus"


def run_council(
    question: str,
    council_config: list[tuple[str, str]],
    api_key: str,
    rounds: int = 1,
    verbose: bool = True,
    anonymous: bool = True,
) -> str:
    """Run the council deliberation."""

    council_names = [name for name, _ in council_config]

    # Anonymous mode: use "Speaker 1", "Speaker 2", etc. (Karpathy-style)
    if anonymous:
        display_names = {name: f"Speaker {i+1}" for i, (name, _) in enumerate(council_config)}
    else:
        display_names = {name: name for name, _ in council_config}

    if verbose:
        print(f"Council members: {council_names}")
        if anonymous:
            print("(Models see each other as Speaker 1, 2, etc. to prevent bias)")
        print(f"Rounds: {rounds}")
        print(f"Question: {question[:100]}{'...' if len(question) > 100 else ''}")
        print()
        print("=" * 60)
        print("COUNCIL DELIBERATION")
        print("=" * 60)
        print()

    # Build conversation history
    conversation = []
    output_parts = []

    # First speaker prompt (no prior speakers to reference)
    first_speaker_system = """You are {name}, speaking first in Round {round_num} of a council deliberation.

As the first speaker, stake a clear position on the question. Be specific and substantive so others can engage with your points.

End with 2-3 key claims that others should respond to."""

    # Subsequent speaker prompt (must engage with previous speakers)
    council_system = """You are {name}, participating in Round {round_num} of a council deliberation.

REQUIREMENTS for your response:
1. Reference at least ONE previous speaker by name (e.g., "I agree with Claude that..." or "GPT's point about X overlooks...")
2. State explicitly: AGREE, DISAGREE, or BUILD ON their specific point
3. Add ONE new consideration not yet raised

If you fully agree with emerging consensus, say: "CONSENSUS: [the agreed position]"

Previous speakers this round: {previous_speakers}

Be direct. Challenge weak arguments. Don't be sycophantic."""

    # Run deliberation rounds
    for round_num in range(rounds):
        round_speakers = []  # Track speakers in this round (display names)
        for idx, (name, model) in enumerate(council_config):
            dname = display_names[name]  # Use anonymous name if enabled

            # Choose prompt based on position
            if idx == 0 and round_num == 0:
                # First speaker of first round - no one to reference
                system_prompt = first_speaker_system.format(name=dname, round_num=round_num + 1)
            else:
                # All others must engage with previous speakers
                # For first speaker of round 2+, reference all previous speakers
                if round_speakers:
                    previous = ", ".join(round_speakers)
                else:
                    previous = ", ".join([display_names[n] for n, _ in council_config])
                system_prompt = council_system.format(
                    name=dname,
                    round_num=round_num + 1,
                    previous_speakers=previous
                )

            # Build messages for this agent
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question for the council:\n\n{question}"},
            ]

            # Add conversation history (using display names)
            for speaker, text in conversation:
                speaker_dname = display_names[speaker]
                messages.append({
                    "role": "assistant" if speaker == name else "user",
                    "content": f"[{speaker_dname}]: {text}" if speaker != name else text,
                })

            if verbose:
                # Show real name in output even when models see anonymous names
                print(f"### {name}")
                if is_thinking_model(model):
                    print("(thinking...)", flush=True)

            # Stream output live when verbose (thinking models use non-streaming)
            response = query_model(api_key, model, messages, stream=verbose)

            # Print response for thinking models (since they don't stream)
            if verbose and is_thinking_model(model):
                print(response)
            conversation.append((name, response))  # Store real name internally
            round_speakers.append(dname)

            if verbose:
                print()  # Extra newline after streamed response

            output_parts.append(f"### {name}\n{response}")

        # Check for consensus after each completed round
        converged, reason = detect_consensus(conversation, len(council_config))
        if converged:
            if verbose:
                print(f">>> CONSENSUS DETECTED ({reason}) - proceeding to judge\n")
            break

    # Judge synthesizes
    judge_system = """You are the Judge, responsible for synthesizing the council's deliberation.

After the council members have shared their perspectives, you:
1. Identify points of AGREEMENT across all members
2. Identify points of DISAGREEMENT and explain the different views
3. Provide a SYNTHESIS that captures the council's collective wisdom
4. Give a final RECOMMENDATION based on the deliberation

Format your response as:

## Points of Agreement
[What the council agrees on]

## Points of Disagreement
[Where views differ and why]

## Synthesis
[The integrated perspective]

## Recommendation
[Your final recommendation based on the deliberation]

Be balanced and fair. Acknowledge minority views. Don't just pick a winner."""

    # Build judge's view of the conversation (using display names)
    deliberation_text = "\n\n".join(
        f"**{display_names[speaker]}**: {text}" for speaker, text in conversation
    )

    judge_messages = [
        {"role": "system", "content": judge_system},
        {"role": "user", "content": f"Question:\n{question}\n\n---\n\nCouncil Deliberation:\n\n{deliberation_text}"},
    ]

    if verbose:
        print("### Judge")

    # Stream output live when verbose
    judge_response = query_model(api_key, JUDGE_MODEL, judge_messages, max_tokens=1200, stream=verbose)

    if verbose:
        print()  # Extra newline after streamed response

    output_parts.append(f"### Judge\n{judge_response}")

    # Post-process: replace anonymous names with real names in output for readability
    # (Models deliberated anonymously to prevent bias, but output is readable)
    if anonymous:
        final_output = "\n\n".join(output_parts)
        for name, _ in council_config:
            anon_name = display_names[name]
            # Replace "[Speaker 1]" -> "[Claude]", "Speaker 1's" -> "Claude's", etc.
            final_output = final_output.replace(f"### {anon_name}", f"### {name}")
            final_output = final_output.replace(f"[{anon_name}]", f"[{name}]")
            final_output = final_output.replace(f"**{anon_name}**", f"**{name}**")
            final_output = final_output.replace(f"with {anon_name}", f"with {name}")
            final_output = final_output.replace(f"{anon_name}'s", f"{name}'s")
        return final_output

    return "\n\n".join(output_parts)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Council - Multi-model deliberation"
    )
    parser.add_argument("question", help="The question for the council to deliberate")
    parser.add_argument(
        "--rounds",
        type=int,
        default=2,
        help="Number of deliberation rounds (default: 2, exits early on consensus)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )
    parser.add_argument(
        "--output", "-o",
        help="Save transcript to file",
    )
    parser.add_argument(
        "--named",
        action="store_true",
        help="Show real model names instead of anonymous Speaker 1, 2, etc.",
    )
    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        mode = "named mode" if args.named else "anonymous mode"
        print(f"Running LLM Council ({mode})...")
        print()

    # Run council
    try:
        transcript = run_council(
            question=args.question,
            council_config=COUNCIL,
            api_key=api_key,
            rounds=args.rounds,
            verbose=not args.quiet,
            anonymous=not args.named,
        )

        # Save transcript if requested
        if args.output:
            Path(args.output).write_text(transcript)
            if not args.quiet:
                print(f"Transcript saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
