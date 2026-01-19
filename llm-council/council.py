#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "agent-framework-core>=1.0.0b260106",
#     "openai>=1.0.0",
# ]
# ///
"""
LLM Council - Karpathy-style multi-model deliberation using Microsoft Agent Framework.

Multiple LLMs debate a question and a judge synthesizes the consensus.

Usage:
    uv run council.py "Should I use microservices or monolith?"
    uv run council.py "your question" --cheap
    uv run council.py "your question" --rounds 2
"""

import argparse
import asyncio
import os
import sys

from agent_framework import (
    ChatAgent,
    GroupChatBuilder,
    GroupChatState,
    GroupChatResponseReceivedEvent,
    AgentRunUpdateEvent,
)
from agent_framework.openai import OpenAIChatClient


# Model configurations via OpenRouter
EXPENSIVE_COUNCIL = [
    ("Claude", "anthropic/claude-sonnet-4"),
    ("GPT", "openai/gpt-4o"),
    ("Gemini", "google/gemini-2.0-flash-001"),
]

CHEAP_COUNCIL = [
    ("Claude", "anthropic/claude-3.5-haiku"),
    ("GPT", "openai/gpt-4o-mini"),
    ("Gemini", "google/gemini-2.0-flash-lite-001"),
]

JUDGE_MODEL = "anthropic/claude-sonnet-4"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def create_chat_client(model: str, api_key: str) -> OpenAIChatClient:
    """Create an OpenAIChatClient for Microsoft Agent Framework via OpenRouter."""
    return OpenAIChatClient(
        model_id=model,
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
    )


def create_council_agents(
    council_config: list[tuple[str, str]],
    api_key: str,
) -> list[ChatAgent]:
    """Create council member agents, each with a different model."""
    agents = []

    for name, model in council_config:
        chat_client = create_chat_client(model, api_key)
        agent = ChatAgent(
            chat_client=chat_client,
            name=f"{name}Agent",
            instructions=f"""You are {name}, a council member in a multi-model deliberation.

Your role:
1. Share your perspective on the question
2. Respond to other council members' points - agree, disagree, or build on them
3. Be concise but substantive (2-3 paragraphs max per turn)
4. If you agree with the emerging consensus, say so explicitly

Be direct. Don't be sycophantic. If you disagree with another model, say why.""",
        )
        agents.append(agent)

    return agents


def create_judge_agent(api_key: str, model: str = JUDGE_MODEL) -> ChatAgent:
    """Create the judge who synthesizes the council's deliberation."""
    chat_client = create_chat_client(model, api_key)
    return ChatAgent(
        chat_client=chat_client,
        name="Judge",
        instructions="""You are the Judge, responsible for synthesizing the council's deliberation.

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

Be balanced and fair. Acknowledge minority views. Don't just pick a winner.""",
    )


def create_speaker_selector(council_names: list[str], rounds: int):
    """Create a speaker selection function for round-robin + judge."""
    total_council_turns = len(council_names) * rounds
    total_turns = total_council_turns + 1  # +1 for judge

    def select_next_speaker(state: GroupChatState) -> str:
        """Round-robin through council members, then judge."""
        round_idx = state.current_round

        # Council members take turns for `rounds` iterations
        if round_idx < total_council_turns:
            speaker_idx = round_idx % len(council_names)
            return council_names[speaker_idx]

        # Judge speaks once after council deliberation
        return "Judge"

    return select_next_speaker, total_turns


async def run_council(
    question: str,
    council_config: list[tuple[str, str]],
    api_key: str,
    rounds: int = 1,
    verbose: bool = True,
) -> str:
    """Run the council deliberation using Microsoft Agent Framework."""

    # Create agents
    council_agents = create_council_agents(council_config, api_key)
    judge = create_judge_agent(api_key)

    # All participants
    all_agents = council_agents + [judge]
    council_names = [a.name for a in council_agents]

    if verbose:
        print(f"Council members: {council_names}")
        print(f"Rounds: {rounds}")
        print(f"Question: {question[:100]}{'...' if len(question) > 100 else ''}")
        print()
        print("=" * 60)
        print("COUNCIL DELIBERATION")
        print("=" * 60)
        print()

    # Create speaker selector and get total turns
    speaker_selector, total_turns = create_speaker_selector(council_names, rounds)

    # Build the group chat workflow
    workflow = (
        GroupChatBuilder()
        .with_select_speaker_func(speaker_selector)
        .with_max_rounds(total_turns)
        .participants(all_agents)
        .build()
    )

    # Run the deliberation and collect responses
    output_lines = []
    current_speaker = None
    current_text_parts = []

    async for event in workflow.run_stream(question):
        # Handle streaming updates from agents
        if isinstance(event, AgentRunUpdateEvent):
            speaker = event.executor_id
            # Get text from event.data (AgentResponseUpdate)
            text = ""
            if event.data and hasattr(event.data, 'text'):
                if isinstance(event.data.text, str):
                    text = event.data.text
                elif hasattr(event.data.text, 'text'):
                    text = event.data.text.text or ""

            # New speaker - print previous one and start collecting new
            if speaker != current_speaker:
                if current_speaker and current_text_parts:
                    full_text = "".join(current_text_parts).strip()
                    if full_text and verbose:
                        print(f"### {current_speaker}")
                        print(full_text)
                        print()
                    if full_text:
                        output_lines.append(f"### {current_speaker}\n{full_text}")
                current_speaker = speaker
                current_text_parts = []

            if text:
                current_text_parts.append(text)

    # Don't forget the last speaker
    if current_speaker and current_text_parts:
        full_text = "".join(current_text_parts).strip()
        if full_text and verbose:
            print(f"### {current_speaker}")
            print(full_text)
            print()
        if full_text:
            output_lines.append(f"### {current_speaker}\n{full_text}")

    return "\n\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Council - Multi-model deliberation using Microsoft Agent Framework"
    )
    parser.add_argument("question", help="The question for the council to deliberate")
    parser.add_argument(
        "--cheap",
        action="store_true",
        help="Use cheaper/faster models",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=1,
        help="Number of deliberation rounds before judge synthesizes (default: 1)",
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

    # Select council configuration
    council_config = CHEAP_COUNCIL if args.cheap else EXPENSIVE_COUNCIL
    mode = "cheap" if args.cheap else "expensive"

    if not args.quiet:
        print(f"Running LLM Council [{mode}] with Microsoft Agent Framework...")

    # Run council
    try:
        asyncio.run(run_council(
            question=args.question,
            council_config=council_config,
            api_key=api_key,
            rounds=args.rounds,
            verbose=not args.quiet,
        ))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
