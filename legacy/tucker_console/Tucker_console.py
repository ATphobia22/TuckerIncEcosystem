#!/usr/bin/env python3
"""Copied utility from ATphobia22/tucker_console.

Source revision: 64dc07edd8e0dfa4e682d781bf66f09722939a3c
Source path: Tucker_console.py

This is retained as a compatibility/reference copy. Production TuckerInc.82
services must use injected credentials, current model adapters, bounded
network timeouts, and structured provenance logging.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import openai
    from anthropic import Anthropic
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError as exc:
    print(f"Missing dependency: {exc}")
    print("Install openai anthropic scikit-learn to run this compatibility utility.")
    sys.exit(1)

LOG_DIR = Path.home() / "tucker_console" / "logs"
LOG_FILE = LOG_DIR / "audit.jsonl"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_api_keys() -> tuple[str, str]:
    """Read credentials from environment variables without persisting them."""
    openai_key = os.getenv("OPENAI_API_KEY")
    claude_key = os.getenv("ANTHROPIC_API_KEY")
    if not openai_key:
        openai_key = input("Enter OpenAI API key: ").strip()
    if not claude_key:
        claude_key = input("Enter Anthropic API key: ").strip()
    if not openai_key or not claude_key:
        raise RuntimeError("Both provider credentials are required.")
    return openai_key, claude_key


def call_gpt(prompt: str, openai_key: str) -> str:
    client = openai.OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
    )
    return (response.choices[0].message.content or "").strip()


def call_claude(prompt: str, claude_key: str) -> str:
    client = Anthropic(api_key=claude_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def score_responses(responses: dict[str, str]) -> dict[str, float]:
    """Score responses by average pairwise TF-IDF cosine similarity."""
    names = list(responses)
    texts = list(responses.values())
    if len(texts) < 2:
        return {names[0]: 100.0} if names else {}
    matrix = TfidfVectorizer(stop_words="english").fit_transform(texts)
    similarities = cosine_similarity(matrix)
    return {
        name: round(
            sum(similarities[index][j] for j in range(len(names)) if j != index)
            / (len(names) - 1)
            * 100,
            1,
        )
        for index, name in enumerate(names)
    }


def length_bonus(text: str) -> float:
    words = len(text.split())
    return 5.0 if 80 <= words <= 400 else 0.0


def log_audit(prompt: str, results: list[dict[str, object]]) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
        "results": [
            {
                "model": result["model"],
                "score": result["score"],
                "output_hash": hashlib.sha256(str(result["output"]).encode()).hexdigest()[:16],
            }
            for result in results
        ],
    }
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def run_comparison(prompt: str, openai_key: str, claude_key: str) -> list[dict[str, object]]:
    outputs: dict[str, str] = {}
    for name, caller, key in (
        ("GPT-4o-mini", call_gpt, openai_key),
        ("Claude", call_claude, claude_key),
    ):
        try:
            outputs[name] = caller(prompt, key)
        except Exception as exc:  # Compatibility utility: preserve per-provider failure.
            outputs[name] = f"[Error: {exc}]"
    base_scores = score_responses(outputs)
    results = [
        {
            "model": model,
            "output": text,
            "score": round(base_scores[model] + length_bonus(text), 1),
        }
        for model, text in outputs.items()
    ]
    log_audit(prompt, results)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Tucker Console compatibility utility")
    parser.add_argument("--prompt", "-p", required=True)
    args = parser.parse_args()
    openai_key, claude_key = get_api_keys()
    for result in run_comparison(args.prompt, openai_key, claude_key):
        print(f"{result['model']}: {result['score']}")


if __name__ == "__main__":
    main()
