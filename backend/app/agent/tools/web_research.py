from typing import Any, Dict, List

import requests

from app.core.config import (
    BRAVE_SEARCH_API_KEY,
    WEB_MAX_RESULTS,
    WEB_SEARCH_TIMEOUT,
    WEB_SEARCH_URL,
    WEB_RESEARCH_ENABLED,
)
from app.services.privacy_filter import inspect_query


def run_web_research(query: str) -> Dict[str, Any]:
    """
    Public web research agent.

    Important:
    The original user query is inspected first.
    Only an approved query is sent to the external provider.
    """

    privacy = inspect_query(query)
    if not WEB_RESEARCH_ENABLED:
     return {
        "success": False,
        "blocked": False,
        "reason": "Web research is disabled by system configuration.",
        "privacy_reasons": [],
        "query_sent": None,
        "results": [],
    }

    if not privacy.allowed:
        return {
            "success": False,
            "blocked": True,
            "reason": "Web research blocked by privacy policy.",
            "privacy_reasons": privacy.reasons,
            "query_sent": None,
            "results": [],
        }

    if not BRAVE_SEARCH_API_KEY:
        return {
            "success": False,
            "blocked": False,
            "reason": "Brave Search API key is not configured.",
            "privacy_reasons": [],
            "query_sent": None,
            "results": [],
        }

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
    }

    params = {
        "q": privacy.sanitized_query,
        "count": WEB_MAX_RESULTS,
        "country": "IN",
        "search_lang": "en",
        "ui_lang": "en-IN",
        "safesearch": "moderate",
    }

    try:
        response = requests.get(
            WEB_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=WEB_SEARCH_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        raw_results = data.get("web", {}).get("results", [])

        results: List[Dict[str, Any]] = []

        for index, item in enumerate(raw_results, start=1):
            results.append(
                {
                    "id": f"WEB-{index}",
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("description", ""),
                }
            )

        return {
            "success": True,
            "blocked": False,
            "reason": None,
            "privacy_reasons": [],
            "query_sent": privacy.sanitized_query,
            "results": results,
        }

    except requests.RequestException as exc:
        return {
            "success": False,
            "blocked": False,
            "reason": f"Web search request failed: {exc}",
            "privacy_reasons": [],
            "query_sent": privacy.sanitized_query,
            "results": [],
        }

    except Exception as exc:
        return {
            "success": False,
            "blocked": False,
            "reason": f"Unexpected web research error: {exc}",
            "privacy_reasons": [],
            "query_sent": privacy.sanitized_query,
            "results": [],
        }


def format_research_context(results: List[Dict[str, Any]]) -> str:
    """
    Converts search results into context for the local LLM.
    """

    if not results:
        return ""

    lines = [
        "PUBLIC WEB RESEARCH RESULTS:",
        "",
        "Use these sources as external evidence.",
        "Do not invent facts that are not supported by these results.",
        "",
    ]

    for result in results:
        lines.append(
            f"[{result['id']}] {result['title']}"
        )
        lines.append(
            f"URL: {result['url']}"
        )
        lines.append(
            f"Snippet: {result['snippet']}"
        )
        lines.append("")

    return "\n".join(lines)