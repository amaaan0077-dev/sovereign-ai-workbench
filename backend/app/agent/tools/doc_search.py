"""
Clearance-aware Document Retrieval Tool for Agent Execution.
"""
from typing import List, Dict, Any
from app.rag.vector_store import vector_store
from app.core.security import ClearanceTier

def run_doc_search(query: str, clearance_tier: ClearanceTier, top_k: int = 3) -> Dict[str, Any]:
    matches = vector_store.search(query=query, user_clearance=clearance_tier, top_k=top_k)
    return {
        "query": query,
        "clearance_applied": clearance_tier.name,
        "match_count": len(matches),
        "results": matches
    }
