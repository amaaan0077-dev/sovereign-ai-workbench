"""
Local Ollama LLM Provider.

All LLM inference happens through the local Ollama server.

The model is configurable so that development can use:
    qwen2.5:3b

and deployment can later use:
    qwen3:14b
"""

import requests
from typing import Optional

from app.core.config import OLLAMA_BASE_URL


OLLAMA_TIMEOUT = 120.0


def is_ollama_online() -> bool:
    """
    Check whether the local Ollama server is running.
    """

    try:
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/version",
            timeout=2.0
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def query_local_ollama(
    prompt: str,
    model_name: str,
    system_prompt: Optional[str] = None
) -> Optional[str]:

    if not is_ollama_online():
        print("Ollama is not available.")
        return None

    final_prompt = prompt

    if system_prompt:
        final_prompt = (
            f"{system_prompt}\n\n"
            f"USER REQUEST:\n{prompt}"
        )

    try:

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",

            json={
                "model": model_name,
                "prompt": final_prompt,
                "stream": False
            },

            timeout=OLLAMA_TIMEOUT
        )

        if response.status_code != 200:
            print(
                "Ollama error:",
                response.status_code,
                response.text
            )
            return None

        data = response.json()

        return data.get("response")

    except requests.RequestException as exc:

        print("Ollama request failed:", exc)

        return None


def generate_local_response(
    query: str,
    lane: str,
    task_type: str,
    model_name: str,
    retrieved_chunks: list,
    user_name: str,
    clearance_tier: str,
    research_context: Optional[str] = None
) -> str:

    context_parts = []

    if retrieved_chunks:

        context_parts.append(
            "AUTHORIZED INTERNAL KNOWLEDGE:\n"
            + "\n\n".join(
                chunk.get("content", "")
                for chunk in retrieved_chunks
            )
        )

    if research_context:

        context_parts.append(
            "PUBLIC RESEARCH RESULTS:\n"
            + research_context
        )

    context = "\n\n".join(context_parts)

    system_prompt = """
You are the local reasoning engine of the Sovereign Industrial AI Workbench.

You are running locally through Ollama.

Security rules:

1. Never invent company information.
2. Treat internal retrieved information as confidential.
3. Use only authorized internal context.
4. Public research may be used only when explicitly supplied by the
   research agent.
5. If current information is not supplied, do not pretend that you
   know today's information.
6. Clearly distinguish internal evidence from public evidence.
7. If evidence is insufficient, say so.
8. Do not claim that you accessed the internet unless research results
   were actually supplied.
9. Produce a useful, structured answer.
"""

    if context:

        user_prompt = f"""
USER:
{query}

AVAILABLE EVIDENCE:
{context}

Provide the best answer using the evidence above.
Clearly identify important sources when possible.
"""

    else:

        user_prompt = f"""
USER:
{query}

No external research or internal documents were supplied.

Answer using your model knowledge only.
If the user asks for latest/current information, explicitly explain
that current web evidence is required.
"""

    response = query_local_ollama(
        prompt=user_prompt,
        model_name=model_name,
        system_prompt=system_prompt
    )

    if response:
        return response

    return (
        "The local Ollama model could not be reached. "
        "Please confirm that Ollama is running and that the configured "
        f"model '{model_name}' is installed."
    )