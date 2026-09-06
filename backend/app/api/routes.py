"""
FastAPI Route Handlers.
"""
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.api.schemas import ChatRequest, CodeExecutionRequest
from app.agent.workflow import execute_agent_pipeline
from app.agent.tools.sandbox_code import execute_sandboxed_code
from app.services.network_monitor import network_monitor
from app.core.audit_logger import get_recent_audit_logs
from app.core.config import DELIVERABLES_DIR
from app.core.security import MOCK_PERSONAS
from app.rag.sample_data import SAMPLE_DOCS
from app.models.router import MODEL_REGISTRY

api_router = APIRouter(prefix="/api")

@api_router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Main Sovereign Agentic Chat Endpoint.
    Executes dual-lane classification, clearance-gated RAG, sandboxed calculation,
    optional Word approval note drafting, and logs to the immutable audit trail.
    """
    try:
        result = execute_agent_pipeline(
            query=req.query,
            user_id=req.user_id,
            clearance_override=req.clearance_override,
            has_image=req.has_image or False
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/sandbox/execute")
async def execute_code_endpoint(req: CodeExecutionRequest):
    """
    Direct endpoint to run and verify code in the isolated, network-disabled sandbox.
    """
    res = execute_sandboxed_code(req.code, req.timeout_seconds or 5.0)
    return res

@api_router.get("/network/status")
async def get_network_status():
    """
    Zero-Egress network telemetry endpoint proving zero outbound traffic to external hosts.
    """
    return network_monitor.inspect_egress()

@api_router.get("/models")
async def list_models():
    """
    Returns on-premise model registry with VRAM allocations and active statuses.
    """
    return MODEL_REGISTRY

@api_router.get("/personas")
async def list_personas():
    """
    Returns pre-configured industrial personas and clearance tiers.
    """
    return [
        {
            "user_id": p.user_id,
            "name": p.name,
            "role": p.role,
            "department": p.department,
            "clearance_tier": p.clearance_tier.name,
            "clearance_level": int(p.clearance_tier)
        }
        for p in MOCK_PERSONAS.values()
    ]

@api_router.get("/documents")
async def list_documents():
    """
    Lists indexed on-premise documents and their clearance tiers.
    """
    docs = []
    for doc in SAMPLE_DOCS:
        docs.append({
            "chunk_id": doc.chunk_id,
            "doc_id": doc.doc_id,
            "title": doc.title,
            "clearance_tier": doc.clearance_tier.name,
            "clearance_level": int(doc.clearance_tier),
            "department": doc.department,
            "page": doc.page
        })
    return docs

@api_router.get("/audit/logs")
async def get_audit_trail(limit: int = Query(50, ge=1, le=200)):
    """
    Returns immutable audit logs.
    """
    return get_recent_audit_logs(limit=limit)

@api_router.get("/deliverables/{filename}")
async def download_deliverable(filename: str):
    """
    Download generated Word .docx or Excel .xlsx deliverable files.
    """
    file_path = DELIVERABLES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Deliverable file not found.")
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
