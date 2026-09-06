"""
Pydantic API Schemas for Sovereign Industrial AI Workbench.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., description="Prompt or query entered by the industrial user")
    user_id: Optional[str] = Field("eng_rahul", description="User persona ID (eng_rahul, officer_priya, cgm_sharma)")
    clearance_override: Optional[int] = Field(None, description="Clearance tier (1=Internal, 2=Confidential, 3=Secret)")
    has_image: Optional[bool] = Field(False, description="Flag if an image or scanned document was attached")

class CodeExecutionRequest(BaseModel):
    code: str = Field(..., description="Python script to run in the isolated sandbox")
    timeout_seconds: Optional[float] = Field(5.0, description="Max execution timeout")

class DeliverableRequest(BaseModel):
    title: str
    reference_no: str
    requester_name: str
    department: str
    clearance_tier: str
    background_summary: str
    technical_findings: List[Dict[str, str]]
    recommendation: str
