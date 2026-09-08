"""
Sovereign AI Planner / Router

The router determines:
1. Whether the request needs private company knowledge.
2. Whether current/public information is required.
3. Which specialized capabilities are required.
4. Which local model should handle the final reasoning.

IMPORTANT:
This router does NOT send user data to the internet.
Web research will be handled by a separate privacy-controlled agent.
"""

import re
from enum import Enum
from typing import Dict, Any, Tuple, List


class QueryLane(str, Enum):
    LANE_A = "LANE_A_GENERAL"
    LANE_B = "LANE_B_COMPANY_CONFIDENTIAL"


class TaskType(str, Enum):
    GENERAL_KNOWLEDGE = "general_knowledge"
    WEB_RESEARCH = "web_research"
    PRIVATE_RAG = "private_rag"
    CODE_SANDBOX = "code_execution"
    VISION_DOCUMENT = "vision_document"
    DOCUMENT_ANALYSIS = "document_analysis"
    DELIVERABLE_DRAFTING = "deliverable_drafting"
    INCIDENT_ANALYSIS = "incident_analysis"
    DATA_ANALYSIS = "data_analysis"


# ---------------------------------------------------------
# Model registry
# ---------------------------------------------------------

MODEL_REGISTRY = {

    "qwen2.5-3b": {
        "name": "Qwen2.5 3B",
        "role": "General local reasoning and development model",
        "vram_required_gb": 3.0,
        "status": "ACTIVE_DEVELOPMENT_MODEL"
    },

    "qwen2.5-coder": {
        "name": "Qwen2.5-Coder",
        "role": "Coding and sandboxed calculations",
        "vram_required_gb": 6.0,
        "status": "CONFIGURABLE"
    },

    "qwen3-14b": {
        "name": "Qwen3 14B",
        "role": "Primary reasoning and agentic model",
        "vram_required_gb": 9.5,
        "status": "FUTURE_UPGRADE"
    }
}


# ---------------------------------------------------------
# Detection signals
# ---------------------------------------------------------

INDUSTRIAL_SIGNALS = [
    r"\bp-?102\b",
    r"\bcd-?01\b",
    r"\bunit-?[0-9]+\b",
    r"\brefinery\b",
    r"\bvibration\b",
    r"\boverhaul\b",
    r"\bcrack\b",
    r"\bultrasonic\b",
    r"\bstrategic.*crude\b",
    r"\bisprl\b",
    r"\bapproval\s*note\b",
    r"\bseam\b",
    r"\bmawp\b",
    r"\bsop\b",
    r"\bcavern\b",
    r"\bpadur\b",
    r"\bvisakhapatnam\b",
    r"\bmangalore\b",
    r"\bindustrial\b",
    r"\bpsu\b",
]

PRIVATE_SIGNALS = [
    r"\bour company\b",
    r"\binternal\b",
    r"\bconfidential\b",
    r"\bprivate\b",
    r"\bcompany document\b",
    r"\binternal document\b",
    r"\binspection report\b",
    r"\binternal report\b",
    r"\bour report\b",
    r"\bour plant\b",
    r"\bour facility\b",
    r"\bour data\b",
    r"\bsop\b",
    r"\bmaintenance report\b",
]

CURRENT_SIGNALS = [
    r"\blatest\b",
    r"\bcurrent\b",
    r"\btoday\b",
    r"\byesterday\b",
    r"\brecent\b",
    r"\bnewest\b",
    r"\bthis week\b",
    r"\bthis month\b",
    r"\b2026\b",
    r"\bnews\b",
    r"\brecent developments?\b",
    r"\bwhat changed\b",
    r"\bcurrently\b",
    r"\bup[- ]to[- ]date\b",
]

CODE_SIGNALS = [
    r"\bpython\b",
    r"\bcode\b",
    r"\bscript\b",
    r"\bcalculate\b",
    r"\bcalculation\b",
    r"\bformula\b",
    r"\btolerance\b",
    r"\bfft\b",
    r"\bverify\b",
    r"\bprogram\b",
    r"\balgorithm\b",
]

VISION_SIGNALS = [
    r"\bscan(ned)?\b",
    r"\bdrawing\b",
    r"\bp&id\b",
    r"\bblueprint\b",
    r"\bimage\b",
    r"\bphoto\b",
    r"\bhandwritten\b",
    r"\bdiagram\b",
]

DOCUMENT_SIGNALS = [
    r"\bdocument\b",
    r"\breport\b",
    r"\bpdf\b",
    r"\bdocx\b",
    r"\bfile\b",
    r"\binspection\b",
    r"\banalyze.*document\b",
]

DRAFTING_SIGNALS = [
    r"\bapproval\s*note\b",
    r"\bmemorandum\b",
    r"\bdraft\b",
    r"\bword\b",
    r"\bdocx\b",
    r"\breport\b",
    r"\bpresentation\b",
    r"\bppt\b",
    r"\bcreate.*report\b",
    r"\bgenerate.*report\b",
]

DATA_SIGNALS = [
    r"\bexcel\b",
    r"\bxlsx\b",
    r"\bcsv\b",
    r"\bspreadsheet\b",
    r"\bdata analysis\b",
    r"\banalyze.*data\b",
    r"\bstatistics\b",
    r"\bchart\b",
    r"\bgraph\b",
]


def matches_any(query: str, patterns: List[str]) -> bool:
    return any(re.search(pattern, query, re.IGNORECASE) for pattern in patterns)


# ---------------------------------------------------------
# Main planner
# ---------------------------------------------------------

def classify_query(
    query: str,
    has_image_attachment: bool = False
) -> Tuple[QueryLane, TaskType, str]:

    lower_q = query.lower()

    is_private = (
        matches_any(lower_q, INDUSTRIAL_SIGNALS)
        or matches_any(lower_q, PRIVATE_SIGNALS)
    )

    needs_web = matches_any(lower_q, CURRENT_SIGNALS)

    # Company/private lane takes priority for access control.
    lane = (
        QueryLane.LANE_B
        if is_private
        else QueryLane.LANE_A
    )

    # Capability priority
    if has_image_attachment or matches_any(lower_q, VISION_SIGNALS):
        task_type = TaskType.VISION_DOCUMENT

    elif matches_any(lower_q, DATA_SIGNALS):
        task_type = TaskType.DATA_ANALYSIS

    elif matches_any(lower_q, CODE_SIGNALS):
        task_type = TaskType.CODE_SANDBOX

    elif matches_any(lower_q, DRAFTING_SIGNALS):
        task_type = TaskType.DELIVERABLE_DRAFTING

    elif matches_any(lower_q, DOCUMENT_SIGNALS):
        task_type = (
            TaskType.PRIVATE_RAG
            if is_private
            else TaskType.DOCUMENT_ANALYSIS
        )

    elif needs_web:
        task_type = TaskType.WEB_RESEARCH

    elif lane == QueryLane.LANE_B:
        task_type = TaskType.INCIDENT_ANALYSIS

    else:
        task_type = TaskType.GENERAL_KNOWLEDGE

    # Development model for now.
    #
    # Later we can change this to qwen3-14b
    # without redesigning the application.
    model_id = "qwen2.5-3b"

    return lane, task_type, model_id


# ---------------------------------------------------------
# Detailed agent plan
# ---------------------------------------------------------

def build_agent_plan(
    query: str,
    lane: QueryLane,
    task_type: TaskType,
    has_image: bool = False
) -> Dict[str, Any]:

    lower_q = query.lower()

    needs_web = matches_any(lower_q, CURRENT_SIGNALS)

    needs_private = (
        lane == QueryLane.LANE_B
        or matches_any(lower_q, PRIVATE_SIGNALS)
        or matches_any(lower_q, INDUSTRIAL_SIGNALS)
    )

    plan = []

    # Private information
    if needs_private:
        plan.append({
            "agent": "private_knowledge_agent",
            "purpose": "Retrieve clearance-authorized internal knowledge",
            "network_access": False
        })

    # Current public information
    if needs_web:
        plan.append({
            "agent": "web_research_agent",
            "purpose": "Retrieve current public information",
            "network_access": True,
            "privacy_filter_required": True
        })

    # Vision
    if has_image or task_type == TaskType.VISION_DOCUMENT:
        plan.append({
            "agent": "vision_agent",
            "purpose": "Analyze image, scan, drawing or diagram",
            "network_access": False
        })

    # Code
    if task_type == TaskType.CODE_SANDBOX:
        plan.append({
            "agent": "coding_agent",
            "purpose": "Generate and verify code in sandbox",
            "network_access": False
        })

    # Data
    if task_type == TaskType.DATA_ANALYSIS:
        plan.append({
            "agent": "data_agent",
            "purpose": "Analyze spreadsheet or structured data",
            "network_access": False
        })

    # Documents
    if task_type in [
        TaskType.DOCUMENT_ANALYSIS,
        TaskType.DELIVERABLE_DRAFTING
    ]:
        plan.append({
            "agent": "document_agent",
            "purpose": "Read and analyze user documents",
            "network_access": False
        })

    # Reports
    if task_type == TaskType.DELIVERABLE_DRAFTING:
        plan.append({
            "agent": "report_agent",
            "purpose": "Generate professional deliverable",
            "network_access": False
        })

    # Always verify
    plan.append({
        "agent": "verification_agent",
        "purpose": "Check evidence, calculations and unsupported claims",
        "network_access": False
    })

    return {
        "plan": plan,
        "requires_web": needs_web,
        "requires_private_data": needs_private,
        "privacy_mode": (
            "CONTROLLED_WEB_RESEARCH"
            if needs_web
            else "LOCAL_ONLY"
        )
    }


# ---------------------------------------------------------
# Public routing API
# ---------------------------------------------------------

def get_routing_info(
    query: str,
    has_image: bool = False
) -> Dict[str, Any]:

    lane, task_type, model_id = classify_query(
        query,
        has_image
    )

    model_spec = MODEL_REGISTRY[model_id]

    agent_plan = build_agent_plan(
        query,
        lane,
        task_type,
        has_image
    )

    return {
        "lane": lane.value,

        "lane_description": (
            "Lane A: General/Public Knowledge"
            if lane == QueryLane.LANE_A
            else
            "Lane B: Sovereign Confidential / Clearance-Gated"
        ),

        "task_type": task_type.value,

        "selected_model": {
            "model_id": model_id,
            "display_name": model_spec["name"],
            "role": model_spec["role"],
            "vram_gb": model_spec["vram_required_gb"],
            "status": model_spec["status"]
        },

        "agent_plan": agent_plan["plan"],

        "requires_web": agent_plan["requires_web"],

        "requires_private_data": agent_plan["requires_private_data"],

        "privacy_mode": agent_plan["privacy_mode"]
    }