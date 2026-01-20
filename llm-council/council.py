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
    uv run council.py "your question" --context "architecture decision"
"""

import argparse
import asyncio
import httpx
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
GOOGLE_AI_STUDIO_URL = "https://generativelanguage.googleapis.com/v1beta/models"
MOONSHOT_URL = "https://api.moonshot.cn/v1/chat/completions"

# Model configurations (all via OpenRouter, with fallbacks where available)
# Format: (name, openrouter_model, fallback) - fallback is (provider, model) or None
# Providers: "google" = AI Studio, "moonshot" = Moonshot API
COUNCIL = [
    ("Claude", "anthropic/claude-opus-4.5", None),
    ("GPT", "openai/gpt-5.2-pro", None),
    ("Gemini", "google/gemini-3-pro-preview", ("google", "gemini-2.5-pro")),
    ("Grok", "x-ai/grok-4", None),
    ("Kimi", "moonshotai/kimi-k2-thinking", ("moonshot", "kimi-k2")),
]

JUDGE_MODEL = "anthropic/claude-opus-4.5"

# Thinking models don't stream well - use non-streaming for these
# Use exact suffixes to avoid false positives (e.g., "o1" matching "gemini-pro-1.0")
THINKING_MODEL_SUFFIXES = {
    "gemini-3-pro-preview",
    "kimi-k2-thinking",
    "deepseek-r1",
    "o1-preview", "o1-mini", "o1",
    "o3-preview", "o3-mini", "o3",
}


def is_thinking_model(model: str) -> bool:
    """Check if model is a thinking model that doesn't stream well."""
    # Extract model name after provider prefix (e.g., "openai/o1" -> "o1")
    model_name = model.split("/")[-1].lower()
    return model_name in THINKING_MODEL_SUFFIXES


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
        result = query_model_streaming(api_key, model, messages, max_tokens, timeout)
        # If streaming failed (connection drop, etc.), fall through to non-streaming with retries
        if not result.startswith("["):
            return result
        print(f"(Streaming failed, retrying without streaming...)", flush=True)

    # Retry logic for thinking models (can be flaky via OpenRouter)
    for attempt in range(retries + 1):
        try:
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
        except (httpx.RequestError, httpx.RemoteProtocolError) as e:
            if attempt < retries:
                continue  # Retry on connection errors
            return f"[Error: Connection failed for {model}: {e}]"

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


def query_google_ai_studio(
    api_key: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 8192,
    timeout: float = 120.0,
    retries: int = 2,
) -> str:
    """Query Google AI Studio directly (fallback for Gemini models)."""
    # Convert OpenAI-style messages to Gemini format
    contents = []
    system_instruction = None

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            system_instruction = content
        elif role == "user":
            contents.append({"role": "user", "parts": [{"text": content}]})
        elif role == "assistant":
            contents.append({"role": "model", "parts": [{"text": content}]})

    # Build request body
    body = {
        "contents": contents,
        "generationConfig": {
            "maxOutputTokens": max_tokens,
        }
    }
    if system_instruction:
        body["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    url = f"{GOOGLE_AI_STUDIO_URL}/{model}:generateContent?key={api_key}"

    for attempt in range(retries + 1):
        try:
            response = httpx.post(url, json=body, timeout=timeout)

            if response.status_code != 200:
                if attempt < retries:
                    continue
                return f"[Error: HTTP {response.status_code} from AI Studio {model}]"

            data = response.json()

            if "error" in data:
                if attempt < retries:
                    continue
                return f"[Error: {data['error'].get('message', data['error'])}]"

            # Extract text from Gemini response format
            candidates = data.get("candidates", [])
            if not candidates:
                if attempt < retries:
                    continue
                return f"[Error: No candidates from AI Studio {model}]"

            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                if attempt < retries:
                    continue
                return f"[Error: No content from AI Studio {model}]"

            content = parts[0].get("text", "")
            if not content.strip():
                if attempt < retries:
                    continue
                return f"[No response from AI Studio {model} after {retries + 1} attempts]"

            return content

        except httpx.TimeoutException:
            if attempt < retries:
                continue
            return f"[Error: Timeout from AI Studio {model}]"
        except httpx.RequestError as e:
            if attempt < retries:
                continue
            return f"[Error: Request failed for AI Studio {model}: {e}]"

    return f"[Error: Failed to get response from AI Studio {model}]"


def query_moonshot(
    api_key: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 8192,
    timeout: float = 120.0,
    retries: int = 2,
) -> str:
    """Query Moonshot API directly (fallback for Kimi models). Uses OpenAI-compatible format."""
    for attempt in range(retries + 1):
        try:
            response = httpx.post(
                MOONSHOT_URL,
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
                    continue
                return f"[Error: HTTP {response.status_code} from Moonshot {model}]"

            data = response.json()

            if "error" in data:
                if attempt < retries:
                    continue
                return f"[Error: {data['error'].get('message', data['error'])}]"

            if "choices" not in data or not data["choices"]:
                if attempt < retries:
                    continue
                return f"[Error: No response from Moonshot {model}]"

            content = data["choices"][0]["message"]["content"]

            if not content or not content.strip():
                if attempt < retries:
                    continue
                return f"[No response from Moonshot {model} after {retries + 1} attempts]"

            return content

        except httpx.TimeoutException:
            if attempt < retries:
                continue
            return f"[Error: Timeout from Moonshot {model}]"
        except httpx.RequestError as e:
            if attempt < retries:
                continue
            return f"[Error: Request failed for Moonshot {model}: {e}]"

    return f"[Error: Failed to get response from Moonshot {model}]"


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
    except (httpx.RequestError, httpx.RemoteProtocolError) as e:
        error_msg = f"[Error: Connection failed for {model}: {e}]"

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


async def query_model_async(
    client: httpx.AsyncClient,
    model: str,
    messages: list[dict],
    name: str,
    fallback: tuple[str, str] | None = None,
    google_api_key: str | None = None,
    moonshot_api_key: str | None = None,
    max_tokens: int = 500,
    retries: int = 2,
) -> tuple[str, str, str]:
    """
    Async query for parallel blind phase.
    Returns (name, model_name, response).
    """
    model_name = model.split("/")[-1]

    for attempt in range(retries + 1):
        try:
            response = await client.post(
                OPENROUTER_URL,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                },
            )

            if response.status_code != 200:
                if attempt < retries:
                    continue
                # Try fallback
                break

            data = response.json()

            if "error" in data:
                if attempt < retries:
                    continue
                break

            if "choices" not in data or not data["choices"]:
                if attempt < retries:
                    continue
                break

            content = data["choices"][0]["message"]["content"]

            if not content or not content.strip():
                if attempt < retries:
                    continue
                break

            # Clean up reasoning model outputs
            if "<think>" in content:
                content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

            return (name, model_name, content)

        except (httpx.RequestError, httpx.RemoteProtocolError):
            if attempt < retries:
                continue
            break

    # Try fallbacks synchronously (they're not async-friendly)
    if fallback:
        fallback_provider, fallback_model = fallback
        if fallback_provider == "google" and google_api_key:
            response = query_google_ai_studio(google_api_key, fallback_model, messages, max_tokens=max_tokens)
            return (name, fallback_model, response)
        elif fallback_provider == "moonshot" and moonshot_api_key:
            response = query_moonshot(moonshot_api_key, fallback_model, messages, max_tokens=max_tokens)
            return (name, fallback_model, response)

    return (name, model_name, f"[No response from {model_name} after {retries + 1} attempts]")


async def run_blind_phase_parallel(
    question: str,
    council_config: list[tuple[str, str, tuple[str, str] | None]],
    api_key: str,
    google_api_key: str | None = None,
    moonshot_api_key: str | None = None,
    verbose: bool = True,
) -> list[tuple[str, str, str]]:
    """
    Parallel blind first-pass: all models stake claims simultaneously.
    Returns list of (name, model_name, claims).
    ~4x faster than sequential (15-25s vs 50-100s).
    """
    blind_system = """You are participating in the BLIND PHASE of a council deliberation.

Stake your initial position on the question BEFORE seeing what others think.
This prevents anchoring bias.

Provide a CLAIM SKETCH (not a full response):
1. Your core position (1-2 sentences)
2. Top 3 supporting claims or considerations
3. Key assumption or uncertainty

Keep it concise (~100 words). The full deliberation comes later."""

    if verbose:
        print("=" * 60)
        print("BLIND PHASE (independent claims)")
        print("=" * 60)
        print()

    messages = [
        {"role": "system", "content": blind_system},
        {"role": "user", "content": f"Question:\n\n{question}"},
    ]

    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=120.0,
    ) as client:
        tasks = [
            query_model_async(
                client, model, messages, name, fallback,
                google_api_key, moonshot_api_key
            )
            for name, model, fallback in council_config
        ]

        if verbose:
            print("(querying all models in parallel...)")

        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results, handling any exceptions
    blind_claims = []
    for i, result in enumerate(results):
        name, model, _ = council_config[i]
        model_name = model.split("/")[-1]

        if isinstance(result, Exception):
            blind_claims.append((name, model_name, f"[Error: {result}]"))
        else:
            blind_claims.append(result)

    # Print results
    if verbose:
        print()
        for name, model_name, claims in blind_claims:
            print(f"### {model_name} (blind)")
            print(claims)
            print()

    return blind_claims


def sanitize_speaker_content(content: str) -> str:
    """
    Sanitize speaker content to prevent prompt injection.
    Wraps content in a way that prevents it from being interpreted as instructions.
    """
    # Strip any explicit instruction-like patterns
    sanitized = content.replace("SYSTEM:", "[SYSTEM]:")
    sanitized = sanitized.replace("INSTRUCTION:", "[INSTRUCTION]:")
    sanitized = sanitized.replace("IGNORE PREVIOUS", "[IGNORE PREVIOUS]")
    sanitized = sanitized.replace("OVERRIDE:", "[OVERRIDE]:")

    return sanitized


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


def run_blind_phase(
    question: str,
    council_config: list[tuple[str, str, tuple[str, str] | None]],
    api_key: str,
    google_api_key: str | None = None,
    moonshot_api_key: str | None = None,
    verbose: bool = True,
) -> list[tuple[str, str, str]]:
    """
    Blind first-pass: each model stakes claims independently without seeing others.
    Returns list of (name, model_name, claims).
    """
    blind_system = """You are participating in the BLIND PHASE of a council deliberation.

Stake your initial position on the question BEFORE seeing what others think.
This prevents anchoring bias.

Provide a CLAIM SKETCH (not a full response):
1. Your core position (1-2 sentences)
2. Top 3 supporting claims or considerations
3. Key assumption or uncertainty

Keep it concise (~100 words). The full deliberation comes later."""

    blind_claims = []

    if verbose:
        print("=" * 60)
        print("BLIND PHASE (independent claims)")
        print("=" * 60)
        print()

    for name, model, fallback in council_config:
        model_name = model.split("/")[-1]

        if verbose:
            print(f"### {model_name} (blind)")
            if is_thinking_model(model):
                print("(thinking...)", flush=True)

        messages = [
            {"role": "system", "content": blind_system},
            {"role": "user", "content": f"Question:\n\n{question}"},
        ]

        response = query_model(api_key, model, messages, max_tokens=500, stream=verbose)

        # Try fallback if needed
        if response.startswith("[") and fallback:
            fallback_provider, fallback_model = fallback
            if fallback_provider == "google" and google_api_key:
                if verbose:
                    print(f"(fallback: {fallback_model}...)", flush=True)
                response = query_google_ai_studio(google_api_key, fallback_model, messages, max_tokens=500)
                model_name = fallback_model
            elif fallback_provider == "moonshot" and moonshot_api_key:
                if verbose:
                    print(f"(fallback: {fallback_model}...)", flush=True)
                response = query_moonshot(moonshot_api_key, fallback_model, messages, max_tokens=500)
                model_name = fallback_model

        if verbose and is_thinking_model(model):
            print(response)
        if verbose:
            print()

        blind_claims.append((name, model_name, response))

    return blind_claims


def run_council(
    question: str,
    council_config: list[tuple[str, str, tuple[str, str] | None]],
    api_key: str,
    google_api_key: str | None = None,
    moonshot_api_key: str | None = None,
    rounds: int = 1,
    verbose: bool = True,
    anonymous: bool = True,
    blind: bool = True,
    context: str | None = None,
) -> str:
    """Run the council deliberation."""

    council_names = [name for name, _, _ in council_config]
    blind_claims = []

    # Run blind phase first if enabled (now parallel!)
    if blind:
        blind_claims = asyncio.run(run_blind_phase_parallel(
            question, council_config, api_key, google_api_key, moonshot_api_key, verbose
        ))

    # Anonymous mode: use "Speaker 1", "Speaker 2", etc. (Karpathy-style)
    if anonymous:
        display_names = {name: f"Speaker {i+1}" for i, (name, _, _) in enumerate(council_config)}
    else:
        display_names = {name: name for name, _, _ in council_config}

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

    # Add blind claims to output if we have them
    if blind_claims:
        for name, model_name, claims in blind_claims:
            output_parts.append(f"### {model_name} (blind)\n{claims}")

    # Build blind claims context for deliberation prompts (sanitized)
    blind_context = ""
    if blind_claims:
        blind_lines = []
        for name, _, claims in blind_claims:
            dname = display_names[name]
            blind_lines.append(f"**{dname}**: {sanitize_speaker_content(claims)}")
        blind_context = "\n\n".join(blind_lines)

    # First speaker prompt when blind phase was run (has context of all blind claims)
    first_speaker_with_blind = """You are {name}, speaking first in Round {round_num} of a council deliberation.

You've seen everyone's BLIND CLAIMS (their independent initial positions). Now engage:
1. Reference at least ONE other speaker's blind claim
2. Agree, disagree, or build on their position
3. Develop your own position further based on what you've learned

Be direct. Challenge weak arguments. Don't be sycophantic."""

    # First speaker prompt (no blind phase, no prior speakers to reference)
    first_speaker_system = """You are {name}, speaking first in Round {round_num} of a council deliberation.

As the first speaker, stake a clear position on the question. Be specific and substantive so others can engage with your points.

End with 2-3 key claims that others should respond to."""

    # Subsequent speaker prompt (must engage with previous speakers)
    council_system = """You are {name}, participating in Round {round_num} of a council deliberation.

REQUIREMENTS for your response:
1. Reference at least ONE previous speaker by name (e.g., "I agree with Speaker 1 that..." or "Speaker 2's point about X overlooks...")
2. State explicitly: AGREE, DISAGREE, or BUILD ON their specific point
3. Add ONE new consideration not yet raised

If you fully agree with emerging consensus, say: "CONSENSUS: [the agreed position]"

Previous speakers this round: {previous_speakers}

Be direct. Challenge weak arguments. Don't be sycophantic."""

    # Run deliberation rounds
    for round_num in range(rounds):
        round_speakers = []  # Track speakers in this round (display names)
        for idx, (name, model, fallback) in enumerate(council_config):
            dname = display_names[name]  # Use anonymous name if enabled

            # Choose prompt based on position and whether blind phase ran
            if idx == 0 and round_num == 0:
                if blind_claims:
                    # First speaker with blind context
                    system_prompt = first_speaker_with_blind.format(name=dname, round_num=round_num + 1)
                else:
                    # First speaker of first round - no one to reference
                    system_prompt = first_speaker_system.format(name=dname, round_num=round_num + 1)
            else:
                # All others must engage with previous speakers
                # For first speaker of round 2+, reference all previous speakers
                if round_speakers:
                    previous = ", ".join(round_speakers)
                else:
                    previous = ", ".join([display_names[n] for n, _, _ in council_config])
                system_prompt = council_system.format(
                    name=dname,
                    round_num=round_num + 1,
                    previous_speakers=previous
                )

            # Build messages for this agent
            user_content = f"Question for the council:\n\n{question}"
            if blind_context:
                user_content += f"\n\n---\n\nBLIND CLAIMS (independent initial positions):\n\n{blind_context}"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ]

            # Add conversation history (using display names, sanitized)
            for speaker, text in conversation:
                speaker_dname = display_names[speaker]
                sanitized_text = sanitize_speaker_content(text)
                messages.append({
                    "role": "assistant" if speaker == name else "user",
                    "content": f"[{speaker_dname}]: {sanitized_text}" if speaker != name else sanitized_text,
                })

            # Extract model name without provider prefix (e.g., "claude-opus-4.5" from "anthropic/claude-opus-4.5")
            model_name = model.split("/")[-1]

            if verbose:
                # Show full model name in output
                print(f"### {model_name}")
                if is_thinking_model(model):
                    print("(thinking...)", flush=True)

            # Stream output live when verbose (thinking models use non-streaming)
            response = query_model(api_key, model, messages, stream=verbose)

            # Try fallback if OpenRouter failed and fallback is available
            used_fallback = False
            if response.startswith("[") and fallback:
                fallback_provider, fallback_model = fallback

                if fallback_provider == "google" and google_api_key:
                    if verbose:
                        print(f"(OpenRouter failed, trying AI Studio fallback: {fallback_model}...)", flush=True)
                    response = query_google_ai_studio(google_api_key, fallback_model, messages)
                    used_fallback = True
                    model_name = fallback_model

                elif fallback_provider == "moonshot" and moonshot_api_key:
                    if verbose:
                        print(f"(OpenRouter failed, trying Moonshot fallback: {fallback_model}...)", flush=True)
                    response = query_moonshot(moonshot_api_key, fallback_model, messages)
                    used_fallback = True
                    model_name = fallback_model

            # Print response for thinking models (since they don't stream)
            if verbose and (is_thinking_model(model) or used_fallback):
                print(response)
            conversation.append((name, response))  # Store short name internally for reference tracking
            round_speakers.append(dname)

            if verbose:
                print()  # Extra newline after streamed response

            output_parts.append(f"### {model_name}\n{response}")

        # Check for consensus after each completed round
        converged, reason = detect_consensus(conversation, len(council_config))
        if converged:
            if verbose:
                print(f">>> CONSENSUS DETECTED ({reason}) - proceeding to judge\n")
            break

    # Judge synthesizes
    # Build judge system prompt with optional context
    context_hint = ""
    if context:
        context_hint = f"\n\nContext about this question: {context}\nConsider this context when weighing perspectives and forming recommendations."

    judge_system = f"""You are the Judge, responsible for synthesizing the council's deliberation.{context_hint}

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

    # Build judge's view of the conversation (using display names, sanitized)
    deliberation_text = "\n\n".join(
        f"**{display_names[speaker]}**: {sanitize_speaker_content(text)}" for speaker, text in conversation
    )

    judge_messages = [
        {"role": "system", "content": judge_system},
        {"role": "user", "content": f"Question:\n{question}\n\n---\n\nCouncil Deliberation:\n\n{deliberation_text}"},
    ]

    judge_model_name = JUDGE_MODEL.split("/")[-1]

    if verbose:
        print(f"### Judge ({judge_model_name})")

    # Stream output live when verbose
    judge_response = query_model(api_key, JUDGE_MODEL, judge_messages, max_tokens=1200, stream=verbose)

    if verbose:
        print()  # Extra newline after streamed response

    output_parts.append(f"### Judge ({judge_model_name})\n{judge_response}")

    # Post-process: replace anonymous names with real model names in output for readability
    # (Models deliberated anonymously to prevent bias, but output is readable)
    if anonymous:
        final_output = "\n\n".join(output_parts)
        for name, model, _ in council_config:
            anon_name = display_names[name]
            model_name = model.split("/")[-1]
            # Replace "[Speaker 1]" -> "[claude-opus-4.5]", "Speaker 1's" -> "claude-opus-4.5's", etc.
            final_output = final_output.replace(f"### {anon_name}", f"### {model_name}")
            final_output = final_output.replace(f"[{anon_name}]", f"[{model_name}]")
            final_output = final_output.replace(f"**{anon_name}**", f"**{model_name}**")
            final_output = final_output.replace(f"with {anon_name}", f"with {model_name}")
            final_output = final_output.replace(f"{anon_name}'s", f"{model_name}'s")
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
    parser.add_argument(
        "--no-blind",
        action="store_true",
        help="Skip blind first-pass (faster, but more anchoring bias)",
    )
    parser.add_argument(
        "--context", "-c",
        help="Context hint for the judge (e.g., 'architecture decision', 'ethics question')",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Upload transcript to secret GitHub Gist and print URL",
    )
    args = parser.parse_args()

    # Get API keys
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Optional: fallback API keys
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    moonshot_api_key = os.environ.get("MOONSHOT_API_KEY")

    use_blind = not args.no_blind

    if not args.quiet:
        mode_parts = []
        mode_parts.append("named" if args.named else "anonymous")
        mode_parts.append("blind first-pass" if use_blind else "no blind phase")
        print(f"Running LLM Council ({', '.join(mode_parts)})...")
        fallbacks = []
        if google_api_key:
            fallbacks.append("Gemini→AI Studio")
        if moonshot_api_key:
            fallbacks.append("Kimi→Moonshot")
        if fallbacks:
            print(f"(Fallbacks enabled: {', '.join(fallbacks)})")
        print()

    # Run council
    try:
        transcript = run_council(
            question=args.question,
            council_config=COUNCIL,
            api_key=api_key,
            google_api_key=google_api_key,
            moonshot_api_key=moonshot_api_key,
            rounds=args.rounds,
            verbose=not args.quiet,
            anonymous=not args.named,
            blind=use_blind,
            context=args.context,
        )

        # Save transcript if requested
        if args.output:
            Path(args.output).write_text(transcript)
            if not args.quiet:
                print(f"Transcript saved to: {args.output}")

        # Upload to secret gist if requested
        if args.share:
            try:
                # Create temp file with transcript
                import tempfile
                with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.md', prefix='council-', delete=False
                ) as f:
                    # Add header with question
                    f.write(f"# LLM Council Deliberation\n\n")
                    f.write(f"**Question:** {args.question}\n\n")
                    if args.context:
                        f.write(f"**Context:** {args.context}\n\n")
                    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n")
                    f.write(transcript)
                    temp_path = f.name

                # Use gh CLI to create secret gist
                result = subprocess.run(
                    ["gh", "gist", "create", temp_path, "--desc", f"LLM Council: {args.question[:50]}"],
                    capture_output=True, text=True
                )
                os.unlink(temp_path)  # Clean up temp file

                if result.returncode == 0:
                    gist_url = result.stdout.strip()
                    print(f"\n🔗 Shared: {gist_url}")
                else:
                    print(f"Gist creation failed: {result.stderr}", file=sys.stderr)
            except FileNotFoundError:
                print("Error: 'gh' CLI not found. Install with: brew install gh", file=sys.stderr)

        # Log to JSONL history (include gist URL if created)
        gist_url = None
        if args.share:
            try:
                gist_url = result.stdout.strip() if result.returncode == 0 else None
            except NameError:
                pass  # result not defined if gh CLI not found
        history_file = Path(__file__).parent / "council_history.jsonl"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": args.question[:200],  # Truncate long questions
            "gist": gist_url,
            "context": args.context,
            "rounds": args.rounds,
            "blind": use_blind,
            "models": [name for name, _, _ in COUNCIL],
        }
        with open(history_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
