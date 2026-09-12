"""
Sovereign AI Workbench - Query Router

Responsibilities:
- Identify whether a query is general/public or company/confidential.
- Identify the type of task.
- Decide whether code execution is actually required.
- Decide whether document/image processing is required.
- Decide whether public web research is required.
- Select the appropriate local model.

Important:
- Mentioning Python does NOT automatically mean code execution.
- Asking about exception handling does NOT mean sandbox execution.
- "photo" must not match "photosynthesis".
- Explicit code execution requests go to CODE_SANDBOX.
- Engineering calculations go to CODE_SANDBOX.
"""

from enum import Enum
from typing import Any, Dict
import re


# ============================================================
# QUERY LANES
# ============================================================

class QueryLane(str, Enum):
    LANE_A_GENERAL = "LANE_A_GENERAL"
    LANE_B_COMPANY_CONFIDENTIAL = "LANE_B_COMPANY_CONFIDENTIAL"


# ============================================================
# TASK TYPES
# ============================================================

class TaskType(str, Enum):
    GENERAL_KNOWLEDGE = "GENERAL_KNOWLEDGE"
    CODE_SANDBOX = "CODE_SANDBOX"
    VISION_DOCUMENT = "VISION_DOCUMENT"
    DELIVERABLE_DRAFTING = "DELIVERABLE_DRAFTING"
    INCIDENT_ANALYSIS = "INCIDENT_ANALYSIS"


# ============================================================
# MODEL REGISTRY
# ============================================================

MODEL_REGISTRY = {

    "qwen2.5-coder": {
        "id": "qwen2.5-coder",
        "display_name": "Qwen2.5-Coder",
        "role": "Coding and technical calculations",
        "memory_gb": 5.5,
        "status": "available",
    },

    "qwen2.5-vl": {
        "id": "qwen2.5-vl",
        "display_name": "Qwen2.5-VL",
        "role": "Vision and document understanding",
        "memory_gb": 8.0,
        "status": "future",
    },

    "qwen2.5-14b": {
        "id": "qwen2.5-14b",
        "display_name": "Qwen3 14B",
        "role": "Advanced general reasoning",
        "memory_gb": 10.0,
        "status": "future",
    },

    "qwen2.5-general": {
        "id": "qwen2.5-general",
        "display_name": "Qwen2.5 General",
        "role": "General knowledge and reasoning",
        "memory_gb": 5.0,
        "status": "available",
    },
}


# ============================================================
# CONFIDENTIAL / COMPANY TERMS
# ============================================================

CONFIDENTIAL_TERMS = [

    "confidential",
    "classified",
    "secret",
    "restricted",
    "internal",
    "private",
    "proprietary",

    "company data",
    "company document",
    "company report",

    "internal document",
    "internal report",

    "plant report",
    "inspection report",
    "maintenance report",
    "production report",

    "plant data",
    "internal data",
    "organization data",
]


# ============================================================
# VISION TERMS
# ============================================================

# Important:
#
# We use complete-word matching later.
#
# Therefore:
#
# "photo" -> matches
# "photosynthesis" -> does NOT match
#
# This prevents:
#
#     What is photosynthesis?
#
# from being incorrectly classified as a vision task.

VISION_TERMS = [

    "image",
    "photo",
    "picture",

    "scan",
    "scanned",

    "drawing",
    "diagram",
    "blueprint",
    "chart",

    "visual",
    "handwritten",

    "document image",
]


# ============================================================
# DOCUMENT DRAFTING TERMS
# ============================================================

DRAFTING_TERMS = [

    "approval note",
    "draft approval",

    "official letter",
    "draft letter",

    "prepare a report",
    "generate a report",
    "create a report",
    "write a report",

    "generate document",
    "create document",
    "prepare document",
    "draft document",
]


# ============================================================
# INCIDENT / FAILURE ANALYSIS TERMS
# ============================================================

INCIDENT_TERMS = [

    "incident",
    "accident",

    "failure",
    "fault",
    "breakdown",
    "malfunction",

    "root cause",
    "root-cause",

    "failure analysis",
    "incident analysis",
]


# ============================================================
# EXPLICIT CODE EXECUTION TERMS
# ============================================================

# These are requests to ACTUALLY RUN / EXECUTE code.
#
# Merely asking:
#
#     "What is Python?"
#     "What is exception handling?"
#
# must NOT reach the sandbox.
#
# But:
#
#     "Run this Python code"
#
# MUST reach the sandbox.

CODE_EXECUTION_TERMS = [

    "run this code",
    "execute this code",

    "run the code",
    "execute the code",

    "run the following code",
    "execute the following code",

    # --------------------------------------------------------
    # Python-specific execution
    # --------------------------------------------------------

    "run this python code",
    "execute this python code",

    "run python code",
    "execute python code",

    "run the python code",
    "execute the python code",

    # --------------------------------------------------------
    # Testing
    # --------------------------------------------------------

    "test this code",
    "test the code",

    "test this python code",
    "test the python code",

    # --------------------------------------------------------
    # Program execution
    # --------------------------------------------------------

    "run this program",
    "execute this program",

    "run the program",
    "execute the program",

    # --------------------------------------------------------
    # Output requests
    # --------------------------------------------------------

    "what is the output of this code",
    "tell me the output of this code",

    "what is the output of this python code",
    "tell me the output of this python code",

    # --------------------------------------------------------
    # Python calculations
    # --------------------------------------------------------

    "use python to calculate",
    "calculate using python",

    "execute python",
    "execute python code",

    "run python",
    "run python code",
]


# ============================================================
# NORMAL CODING / PROGRAMMING TERMS
# ============================================================

# These terms indicate a programming-related question,
# but NOT necessarily code execution.
#
# Example:
#
#     "What is Python exception handling?"
#
# should remain GENERAL_KNOWLEDGE.

CODING_TERMS = [

    "python",

    "javascript",
    "typescript",

    "java",

    "c programming",
    "c++",

    "golang",
    "rust",

    "programming",
    "program",

    "code",
    "coding",

    "function",
    "class",
    "variable",

    "loop",
    "array",

    "dictionary",
    "list",
    "tuple",

    "exception",
    "error handling",

    "debugging",

    "algorithm",
    "data structure",

    "api",

    "backend",
    "frontend",

    "fastapi",
    "flask",

    "react",
    "next.js",
]


# ============================================================
# ENGINEERING CALCULATION TERMS
# ============================================================

ENGINEERING_CALCULATION_TERMS = [

    "calculate pressure",
    "calculate mawp",

    "safe operating pressure",
    "operating pressure",
    "design pressure",
    "safe pressure",

    "crack depth",
    "crack penetration",
    "crack length",

    "vibration measurement",
    "rms vibration",
    "vibration level",

    "derating",

    "engineering calculation",
    "stress calculation",
    "load calculation",
    "pressure calculation",
    "equipment calculation",

    "calculate the pressure",
    "calculate safe operating",
]


# ============================================================
# WEB / CURRENT INFORMATION TERMS
# ============================================================

WEB_RESEARCH_TERMS = [

    "latest",
    "current",
    "currently",

    "recent",
    "recently",

    "today",
    "this week",
    "this month",
    "this year",

    "new developments",

    "latest developments",
    "latest news",
    "current news",

    "what happened",

    "as of 2026",
    "in 2026",
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def _normalize(text: str) -> str:
    """
    Normalize text before matching.

    Example:

        "  RUN   Python   CODE  "

    becomes:

        "run python code"
    """

    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()


# ============================================================
# SAFE PHRASE MATCHING
# ============================================================

def _contains_phrase(
    text: str,
    phrase: str,
) -> bool:
    """
    Match a complete word or phrase.

    This is important because simple substring matching causes
    bugs such as:

        "photo" in "photosynthesis"

    which is TRUE with normal substring matching.

    With this function:

        "photo" matches "photo"
        "photo" does NOT match "photosynthesis"
    """

    text = _normalize(text)
    phrase = _normalize(phrase)

    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return re.search(
        pattern,
        text,
    ) is not None


# ============================================================
# CHECK MULTIPLE TERMS
# ============================================================

def _contains_any(
    text: str,
    terms: list[str],
) -> bool:
    """
    Return True when at least one complete term/phrase
    appears in the text.
    """

    return any(
        _contains_phrase(text, term)
        for term in terms
    )


# ============================================================
# WEB RESEARCH DECISION
# ============================================================

def requires_web_research(
    query: str,
) -> bool:
    """
    Determine whether the user is asking for current/latest
    information.
    """

    return _contains_any(
        query,
        WEB_RESEARCH_TERMS,
    )


# ============================================================
# LANE CLASSIFICATION
# ============================================================

def classify_lane(
    query: str,
) -> tuple[str, str]:
    """
    Determine whether the request is:

        Lane A = general/public

    or:

        Lane B = company/private/confidential
    """

    if _contains_any(
        query,
        CONFIDENTIAL_TERMS,
    ):

        return (
            QueryLane.LANE_B_COMPANY_CONFIDENTIAL.value,

            "Company/private query. "
            "Local clearance-filtered RAG is required.",
        )

    return (
        QueryLane.LANE_A_GENERAL.value,

        "General/public knowledge query. "
        "Private company RAG is bypassed.",
    )


# ============================================================
# TASK CLASSIFICATION
# ============================================================

def classify_task(
    query: str,
    has_image: bool = False,
) -> str:
    """
    Determine what type of task the agent needs to perform.

    Priority:

        1. Uploaded image
        2. Vision request
        3. Document drafting
        4. Incident analysis
        5. Explicit code execution
        6. Engineering calculation
        7. Normal programming discussion
        8. General knowledge
    """

    # --------------------------------------------------------
    # 1. Actual uploaded image
    # --------------------------------------------------------

    if has_image:

        return TaskType.VISION_DOCUMENT.value


    # --------------------------------------------------------
    # 2. Vision / image request
    # --------------------------------------------------------

    if _contains_any(
        query,
        VISION_TERMS,
    ):

        return TaskType.VISION_DOCUMENT.value


    # --------------------------------------------------------
    # 3. Document generation
    # --------------------------------------------------------

    if _contains_any(
        query,
        DRAFTING_TERMS,
    ):

        return TaskType.DELIVERABLE_DRAFTING.value


    # --------------------------------------------------------
    # 4. Incident analysis
    # --------------------------------------------------------

    if _contains_any(
        query,
        INCIDENT_TERMS,
    ):

        return TaskType.INCIDENT_ANALYSIS.value


    # --------------------------------------------------------
    # 5. Explicit code execution
    # --------------------------------------------------------

    if _contains_any(
        query,
        CODE_EXECUTION_TERMS,
    ):

        return TaskType.CODE_SANDBOX.value


    # --------------------------------------------------------
    # 6. Engineering calculation
    # --------------------------------------------------------

    if _contains_any(
        query,
        ENGINEERING_CALCULATION_TERMS,
    ):

        return TaskType.CODE_SANDBOX.value


    # --------------------------------------------------------
    # 7. Normal programming question
    # --------------------------------------------------------
    #
    # Example:
    #
    # "What is Python exception handling?"
    #
    # This is a knowledge question.
    #
    # It does NOT execute code.

    if _contains_any(
        query,
        CODING_TERMS,
    ):

        return TaskType.GENERAL_KNOWLEDGE.value


    # --------------------------------------------------------
    # 8. Default
    # --------------------------------------------------------

    return TaskType.GENERAL_KNOWLEDGE.value


# ============================================================
# MODEL SELECTION
# ============================================================

def select_model(
    task_type: str,
    has_image: bool = False,
) -> Dict[str, Any]:
    """
    Select the appropriate local model.

    Current development setup:

        General → Qwen2.5 General
        Code → Qwen2.5-Coder
        Vision → Qwen2.5-VL (future)

    Later the actual Ollama model can be changed through
    configuration without rewriting the router.
    """

    # --------------------------------------------------------
    # Vision
    # --------------------------------------------------------

    if (
        has_image
        or task_type
        == TaskType.VISION_DOCUMENT.value
    ):

        return MODEL_REGISTRY[
            "qwen2.5-vl"
        ].copy()


    # --------------------------------------------------------
    # Code / calculation
    # --------------------------------------------------------

    if (
        task_type
        == TaskType.CODE_SANDBOX.value
    ):

        return MODEL_REGISTRY[
            "qwen2.5-coder"
        ].copy()


    # --------------------------------------------------------
    # Everything else
    # --------------------------------------------------------

    return MODEL_REGISTRY[
        "qwen2.5-general"
    ].copy()


# ============================================================
# COMPLETE ROUTING INFORMATION
# ============================================================

def get_routing_info(
    query: str,
    has_image: bool = False,
) -> Dict[str, Any]:
    """
    Main router entry point.

    Returns all information required by the agent workflow.
    """

    # --------------------------------------------------------
    # Lane
    # --------------------------------------------------------

    lane, lane_description = classify_lane(
        query
    )


    # --------------------------------------------------------
    # Task
    # --------------------------------------------------------

    task_type = classify_task(
        query=query,
        has_image=has_image,
    )


    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    selected_model = select_model(
        task_type=task_type,
        has_image=has_image,
    )


    # --------------------------------------------------------
    # Web requirement
    # --------------------------------------------------------

    web_required = requires_web_research(
        query
    )


    # --------------------------------------------------------
    # Routing explanation
    # --------------------------------------------------------

    routing_reasons = []


    # --------------------------------------------------------
    # Security lane reason
    # --------------------------------------------------------

    if (
        lane
        == QueryLane.LANE_B_COMPANY_CONFIDENTIAL.value
    ):

        routing_reasons.append(
            "confidential/company indicators detected"
        )

    else:

        routing_reasons.append(
            "no obvious confidential/company indicators detected"
        )


    # --------------------------------------------------------
    # Task reason
    # --------------------------------------------------------

    if (
        task_type
        == TaskType.VISION_DOCUMENT.value
    ):

        routing_reasons.append(
            "vision/image/document indicators detected"
        )

    elif (
        task_type
        == TaskType.DELIVERABLE_DRAFTING.value
    ):

        routing_reasons.append(
            "document drafting indicators detected"
        )

    elif (
        task_type
        == TaskType.INCIDENT_ANALYSIS.value
    ):

        routing_reasons.append(
            "incident/failure analysis indicators detected"
        )

    elif (
        task_type
        == TaskType.CODE_SANDBOX.value
    ):

        routing_reasons.append(
            "explicit code execution or engineering "
            "calculation indicators detected"
        )

    elif _contains_any(
        query,
        CODING_TERMS,
    ):

        routing_reasons.append(
            "coding/programming discussion detected; "
            "execution not requested"
        )

    else:

        routing_reasons.append(
            "general knowledge query"
        )


    # --------------------------------------------------------
    # Web reason
    # --------------------------------------------------------

    if web_required:

        routing_reasons.append(
            "current/latest information requested"
        )


    # --------------------------------------------------------
    # Final routing object
    # --------------------------------------------------------

    return {

        "lane": lane,

        "lane_description": lane_description,

        "task_type": task_type,

        "selected_model": selected_model,

        "requires_web": web_required,

        "routing_reasons": routing_reasons,

        "has_image": has_image,
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

def get_available_models() -> Dict[str, Dict[str, Any]]:
    """
    Return a copy of the model registry.
    """

    return {
        model_id: model.copy()
        for model_id, model in MODEL_REGISTRY.items()
    }