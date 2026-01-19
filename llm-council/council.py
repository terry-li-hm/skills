#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "autogen-agentchat>=0.4",
#     "autogen-ext[openai]>=0.4",
# ]
# ///
"""
LLM Council - Karpathy-style multi-model deliberation using AutoGen.

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

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Model configurations
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

MODEL_INFO = {
    "vision": False,
    "function_calling": True,
    "json_output": True,
    "family": "unknown",
    "structured_output": True,
}


def create_model_client(model: str, api_key: str) -> OpenAIChatCompletionClient:
    """Create OpenRouter-compatible model client."""
    return OpenAIChatCompletionClient(
        model=model,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model_info=MODEL_INFO,
    )


def create_council_agents(
    council_config: list[tuple[str, str]],
    api_key: str,
) -> list[AssistantAgent]:
    """Create council member agents, each with a different model."""
    agents = []

    for name, model in council_config:
        agent = AssistantAgent(
            name=f"{name}Agent",
            model_client=create_model_client(model, api_key),
            system_message=f"""You are {name}, a council member in a multi-model deliberation.

Your role:
1. Share your perspective on the question
2. Respond to other council members' points - agree, disagree, or build on them
3. Be concise but substantive (2-3 paragraphs max per turn)
4. If you agree with the emerging consensus, say so explicitly

Be direct. Don't be sycophantic. If you disagree with another model, say why.""",
        )
        agents.append(agent)

    return agents


def create_judge_agent(api_key: str, model: str = "anthropic/claude-sonnet-4") -> AssistantAgent:
    """Create the judge who synthesizes the council's deliberation."""
    return AssistantAgent(
        name="Judge",
        model_client=create_model_client(model, api_key),
        system_message="""You are the Judge, responsible for synthesizing the council's deliberation.

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


async def run_council(
    question: str,
    council_config: list[tuple[str, str]],
    api_key: str,
    rounds: int = 1,
    verbose: bool = True,
) -> str:
    """Run the council deliberation."""

    # Create agents
    council_agents = create_council_agents(council_config, api_key)
    judge = create_judge_agent(api_key)

    # All participants: council members + judge
    all_agents = council_agents + [judge]

    # Calculate max messages: initial task + each council member speaks `rounds` times + judge
    # RoundRobin cycles through all agents, first message is the task
    max_messages = 1 + (len(council_agents) * rounds) + 1  # task + council rounds + judge

    if verbose:
        print(f"Council members: {[a.name for a in council_agents]}")
        print(f"Rounds: {rounds}")
        print(f"Question: {question[:100]}{'...' if len(question) > 100 else ''}")
        print()

    # Create the council as RoundRobinGroupChat
    council = RoundRobinGroupChat(
        participants=all_agents,
        termination_condition=MaxMessageTermination(max_messages),
    )

    # Run the deliberation
    if verbose:
        print("=" * 60)
        print("COUNCIL DELIBERATION")
        print("=" * 60)
        print()

    result = await council.run(task=question)

    # Extract and display messages
    output_lines = []
    for msg in result.messages:
        if verbose:
            print(f"### {msg.source}")
            print(msg.content)
            print()
        output_lines.append(f"### {msg.source}\n{msg.content}")

    return "\n\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Council - Multi-model deliberation using AutoGen"
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
        print(f"Running LLM Council [{mode}]...")

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
        sys.exit(1)


if __name__ == "__main__":
    main()
