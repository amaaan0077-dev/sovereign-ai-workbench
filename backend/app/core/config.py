"""
Core configuration enforcing zero-egress, air-gapped settings,
and hardware-aware model registry endpoints.
"""
import os
from pathlib import Path

# ENFORCE ZERO TELEMETRY ACROSS POPULAR LIBRARIES
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["DO_NOT_TRACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DELIVERABLES_DIR = STORAGE_DIR / "deliverables"
AUDIT_DIR = STORAGE_DIR / "audit"
DOCUMENTS_DIR = STORAGE_DIR / "documents"

DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Model serving endpoints (vLLM or Ollama local endpoints)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv(
    "OLLAMA_CHAT_MODEL",
    "qwen2.5:3b"
)
VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")

# Default clearance level if not specified
DEFAULT_CLEARANCE = 1  # 1: INTERNAL, 2: CONFIDENTIAL, 3: SECRET

APP_TITLE = "Sovereign Industrial AI Workbench"
APP_VERSION = "1.0.0 (SIH Air-Gapped Edition)"
