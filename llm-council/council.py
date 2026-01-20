#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""
LLM Council - Multi-model deliberation with direct API calls.

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

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model configurations
COUNCIL = [
    ("Claude", "anthropic/claude-opus-4.5"),
    ("GPT", "openai/gpt-5.2-pro"),
    ("Gemini", "google/gemini-3-pro-preview"),
    ("Grok", "x-ai/grok-4"),
    ("Kimi", "moonshotai/kimi-k2-thinking"),
]

JUDGE_MODEL = "anthropic/claude-opus-4.5"


def query_model(
    api_key: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 800,
    timeout: float = 120.0,
) -> str:
    """Query a model via OpenRouter and return the response text."""
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
    data = response.json()

    if "error" in data:
        return f"[Error: {data['error'].get('message', data['error'])}]"

    if "choices" not in data or not data["choices"]:
        return f"[Error: No response from {model}]"

    content = data["choices"][0]["message"]["content"]

    # Clean up reasoning model outputs (DeepSeek R1's <think> tags)
    if "<think>" in content:
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

    return content


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
) -> str:
    """Run the council deliberation."""

    council_names = [name for name, _ in council_config]

    if verbose:
        print(f"Council members: {council_names}")
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
        round_speakers = []  # Track speakers in this round
        for idx, (name, model) in enumerate(council_config):
            # Choose prompt based on position
            if idx == 0 and round_num == 0:
                # First speaker of first round - no one to reference
                system_prompt = first_speaker_system.format(name=name, round_num=round_num + 1)
            else:
                # All others must engage with previous speakers
                # For first speaker of round 2+, reference all previous speakers
                if round_speakers:
                    previous = ", ".join(round_speakers)
                else:
                    previous = ", ".join([n for n, _ in council_config])  # All from prior round
                system_prompt = council_system.format(
                    name=name,
                    round_num=round_num + 1,
                    previous_speakers=previous
                )

            # Build messages for this agent
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question for the council:\n\n{question}"},
            ]

            # Add conversation history
            for speaker, text in conversation:
                messages.append({
                    "role": "assistant" if speaker == name else "user",
                    "content": f"[{speaker}]: {text}" if speaker != name else text,
                })

            if verbose:
                print(f"### {name}Agent")

            response = query_model(api_key, model, messages)
            conversation.append((name, response))
            round_speakers.append(name)

            if verbose:
                print(response)
                print()

            output_parts.append(f"### {name}Agent\n{response}")

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

    # Build judge's view of the conversation
    deliberation_text = "\n\n".join(
        f"**{speaker}**: {text}" for speaker, text in conversation
    )

    judge_messages = [
        {"role": "system", "content": judge_system},
        {"role": "user", "content": f"Question:\n{question}\n\n---\n\nCouncil Deliberation:\n\n{deliberation_text}"},
    ]

    if verbose:
        print("### Judge")

    judge_response = query_model(api_key, JUDGE_MODEL, judge_messages, max_tokens=1200)

    if verbose:
        print(judge_response)
        print()

    output_parts.append(f"### Judge\n{judge_response}")

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
    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    if not args.quiet:
        print("Running LLM Council...")
        print()

    # Run council
    try:
        run_council(
            question=args.question,
            council_config=COUNCIL,
            api_key=api_key,
            rounds=args.rounds,
            verbose=not args.quiet,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
