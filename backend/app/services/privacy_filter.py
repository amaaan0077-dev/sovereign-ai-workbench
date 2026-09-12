import re
from dataclasses import dataclass
from typing import List


@dataclass
class PrivacyCheck:
    allowed: bool
    sanitized_query: str
    reasons: List[str]


# Patterns that should NEVER be sent to a public search provider.
SENSITIVE_PATTERNS = [
    (
        "email address",
        re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
    ),
    (
        "phone number",
        re.compile(
            r"\b(?:\+?\d[\d\s-]{8,}\d)\b"
        ),
    ),
    (
        "API key / token",
        re.compile(
            r"\b(?:api[_-]?key|token|secret|password|passwd)"
            r"\s*[:=]\s*\S+",
            re.IGNORECASE,
        ),
    ),
    (
        "private file path",
        re.compile(
            r"(?:[A-Za-z]:\\|/home/|/mnt/|/var/|\\\\)"
            r"[^\s]+",
            re.IGNORECASE,
        ),
    ),
]


CONFIDENTIAL_TERMS = [
    "confidential",
    "secret",
    "internal",
    "classified",
    "restricted",
    "private",
    "proprietary",
    "plant report",
    "inspection report",
    "internal report",
    "company report",
    "internal document",
    "company document",
]


def inspect_query(query: str) -> PrivacyCheck:
    """
    Conservative privacy inspection.

    The default policy is BLOCK:
    if the query contains obvious sensitive information,
    it will not be sent to the public web.
    """

    reasons = []

    for name, pattern in SENSITIVE_PATTERNS:
        if pattern.search(query):
            reasons.append(name)

    lowered = query.lower()

    for term in CONFIDENTIAL_TERMS:
        if term in lowered:
            reasons.append(f"confidential indicator: {term}")

    if reasons:
        return PrivacyCheck(
            allowed=False,
            sanitized_query="",
            reasons=list(dict.fromkeys(reasons)),
        )

    # Basic normalization for safe public queries.
    sanitized = re.sub(r"\s+", " ", query).strip()

    # Brave currently accepts up to 600 characters / 75 words.
    sanitized = sanitized[:600]

    return PrivacyCheck(
        allowed=True,
        sanitized_query=sanitized,
        reasons=[],
    )