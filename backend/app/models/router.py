"""
Dynamic Model Router and Dual-Lane Query Classifier.
- Lane A (General Knowledge): Handled by general base model, 0 RAG lookup.
- Lane B (Company-Specific / Confidential): Requires clearance-gated RAG & multi-step agent.
- Model Dispatcher:
    - Coding / Calculations -> Qwen2.5-Coder
    - Vision / Scanned Docs -> Qwen2.5-VL
    - Technical Drafting -> Qwen2.5-14B (with quantized fallback)
"""
import re
from enum import Enum
from typing import Dict, Any, Tuple

class QueryLane(str, Enum):
    LANE_A = "LANE_A_GENERAL"
    LANE_B = "LANE_B_COMPANY_CONFIDENTIAL"

class TaskType(str, Enum):
    GENERAL_KNOWLEDGE = "general_knowledge"
    CODE_SANDBOX = "code_execution"
    VISION_DOCUMENT = "vision_document"
    DELIVERABLE_DRAFTING = "deliverable_drafting"
    INCIDENT_ANALYSIS = "incident_analysis"

# Model Registry with VRAM footprint & specs
MODEL_REGISTRY = {
    "qwen2.5-3b": {
        "name": "qwen2.5:3b",
        "role": "General Knowledge, Industrial RAG, Drafting & Code Assistance",
        "quantization": "Ollama Local",
        "vram_required_gb": 3.0,
        "status": "LOCAL_OLLAMA"
    }
}

# Company-specific industrial keywords triggering Lane B
INDUSTRIAL_SIGNALS = [
    r"\bp-?102\b", r"\bcd-?01\b", r"\bunit-?[0-9]+\b", r"\brefinery\b",
    r"\bvibration\b", r"\boverhaul\b", r"\bcrack\b", r"\bultrasonic\b",
    r"\bstrategic.*crude\b", r"\bisprl\b", r"\bapproval\s*note\b",
    r"\bseam\b", r"\bmawp\b", r"\bsop\b", r"\bcavern\b", r"\bpadur\b",
    r"\bvisakhapatnam\b", r"\bmangalore\b", r"\bindustrial\b", r"\bpsu\b"
]

CODE_SIGNALS = [
    r"\bpython\b", r"\bcode\b", r"\bcalculate\b", r"\bscript\b",
    r"\bformula\b", r"\btolerance\b", r"\bfft\b", r"\bverify\b"
]

VISION_SIGNALS = [
    r"\bscan(ned)?\b", r"\bdrawing\b", r"\bp&id\b", r"\bblueprint\b",
    r"\bimage\b", r"\bphoto\b", r"\bhandwritten\b"
]

DRAFTING_SIGNALS = [
    r"\bapproval\s*note\b", r"\bmemorandum\b", r"\bdraft\b",
    r"\bword\b", r"\bdocx\b", r"\bexcel\b", r"\bpresentation\b", r"\bppt\b"
]

def classify_query(query: str, has_image_attachment: bool = False) -> Tuple[QueryLane, TaskType, str]:
    lower_q = query.lower()

    # 1. Dual-Lane Classification
    is_company = any(re.search(pat, lower_q) for pat in INDUSTRIAL_SIGNALS)
    lane = QueryLane.LANE_B if is_company else QueryLane.LANE_A

    # 2. Task Type Classification
    # For now all text tasks use the locally installed Qwen2.5:3B
    if has_image_attachment or any(re.search(pat, lower_q) for pat in VISION_SIGNALS):
        task_type = TaskType.VISION_DOCUMENT

    elif any(re.search(pat, lower_q) for pat in DRAFTING_SIGNALS):
        task_type = TaskType.DELIVERABLE_DRAFTING

    elif any(re.search(pat, lower_q) for pat in CODE_SIGNALS):
        task_type = TaskType.CODE_SANDBOX

    elif lane == QueryLane.LANE_B:
        task_type = TaskType.INCIDENT_ANALYSIS

    else:
        task_type = TaskType.GENERAL_KNOWLEDGE

    model_id = "qwen2.5-3b"

    return lane, task_type, model_id

def get_routing_info(query: str, has_image: bool = False) -> Dict[str, Any]:
    lane, task_type, model_id = classify_query(query, has_image)
    model_spec = MODEL_REGISTRY[model_id]
    
    return {
        "lane": lane.value,
        "lane_description": "Lane A: General Query (Model Weights Only, 0 RAG Access)" if lane == QueryLane.LANE_A else "Lane B: Sovereign Confidential (Strict Clearance RAG + Tools)",
        "task_type": task_type.value,
        "selected_model": {
            "model_id": model_id,
            "display_name": model_spec["name"],
            "role": model_spec["role"],
            "vram_gb": model_spec["vram_required_gb"],
            "quantization": model_spec["quantization"],
            "status": model_spec["status"]
        }
    }
