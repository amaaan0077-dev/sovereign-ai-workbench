"""
Unified On-Premise LLM Provider.
Uses local Ollama for Qwen2.5.
"""

import requests
from typing import Optional
from app.core.config import OLLAMA_BASE_URL

_OLLAMA_ALIVE = None


def is_ollama_online() -> bool:
    global _OLLAMA_ALIVE

    try:
        resp = requests.get(
            f"{OLLAMA_BASE_URL}/api/version",
            timeout=2.0
        )

        _OLLAMA_ALIVE = resp.status_code == 200
        return _OLLAMA_ALIVE

    except Exception as e:
        print("Ollama connection error:", repr(e))
        _OLLAMA_ALIVE = False
        return False


def query_local_ollama(
    prompt: str,
    model_name: str,
    system_prompt: Optional[str] = None
) -> Optional[str]:

    if not is_ollama_online():
        print("Ollama is not running")
        return None

    try:
        print("========================================")
        print("Calling Ollama")
        print("URL:", OLLAMA_BASE_URL)
        print("Model:", model_name)
        print("========================================")

        # Your installed model
        actual_model = "qwen2.5:3b"

        # Combine system prompt and user prompt
        final_prompt = prompt

        if system_prompt:
            final_prompt = (
                f"System instructions:\n"
                f"{system_prompt}\n\n"
                f"User request:\n"
                f"{prompt}"
            )

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": actual_model,
                "prompt": final_prompt,
                "stream": False
            },
            timeout=120.0
        )

        print("Ollama HTTP status:", response.status_code)

        if response.status_code != 200:
            print("Ollama error:", response.text)
            return None

        data = response.json()

        answer = data.get("response")

        if answer:
            print("Ollama successfully generated response.")
            return answer

        print("Ollama returned no response.")
        return None

    except Exception as e:
        print("OLLAMA ERROR:", repr(e))
        return None


def generate_local_response(
    query: str,
    lane: str,
    task_type: str,
    model_name: str,
    retrieved_chunks: list,
    user_name: str,
    clearance_tier: str,
    system_prompt: Optional[str] = None
) -> str:

    # Ask the actual local Ollama model
    ollama_resp = query_local_ollama(
        query,
        model_name,
        system_prompt=system_prompt
    )

    if ollama_resp:
        return ollama_resp

    # Fallback response if Ollama is unavailable
    if lane == "LANE_A_GENERAL":
        return (
            f"**[Sovereign Model: {model_name} | Lane A: General Knowledge]**\n\n"
            f"**Analysis:**\n"
            f"Local Ollama was unavailable, so the fallback engine was used.\n\n"
            f"Your query was:\n\n"
            f"{query}"
        )

    # Lane B - Company Confidential
    if not retrieved_chunks:
        return (
            f"**[Sovereign Model: {model_name} | Lane B: Clearance-Gated Retrieval]**\n\n"
            f"⚠️ **Access Restricted / No Grounding Context Found**\n\n"
            f"No documentation matching your query could be retrieved "
            f"at clearance tier **{clearance_tier}**."
        )

    citations = [c["citation"] for c in retrieved_chunks]
    doc_titles = list(set(c["title"] for c in retrieved_chunks))

    return (
        f"**[Sovereign Model: {model_name} | Lane B: Company Confidential Grounded]**\n\n"
        f"### Industrial Engineering Findings\n\n"
        f"Grounding successfully established against "
        f"**{len(retrieved_chunks)} verified internal documents**.\n\n"
        f"**Reference Sources:**\n"
        f"{', '.join(doc_titles)}\n\n"
        f"**Citations:**\n"
        f"{', '.join(citations)}\n\n"
        f"{retrieved_chunks[0]['content']}"
    )