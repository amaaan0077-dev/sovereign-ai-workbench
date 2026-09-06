"""
Clearance-Filtered Sovereign Vector Store.
Enforces hard pre-filtering so that higher-clearance chunks are NEVER
matched or returned to users with lower clearance tiers.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from app.rag.embeddings import get_embedding, cosine_similarity
from app.core.security import ClearanceTier

class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        title: str,
        clearance_tier: ClearanceTier,
        department: str,
        page: int,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.title = title
        self.clearance_tier = clearance_tier
        self.department = department
        self.page = page
        self.content = content
        self.metadata = metadata or {}
        self.embedding = get_embedding(content + " " + title + " " + department)

class SovereignVectorStore:
    def __init__(self):
        self.chunks: List[DocumentChunk] = []

    def add_chunk(self, chunk: DocumentChunk):
        self.chunks.append(chunk)

    def search(
        self,
        query: str,
        user_clearance: ClearanceTier,
        top_k: int = 3,
        threshold: float = 0.15
    ) -> List[Dict[str, Any]]:
        """
        PRE-RETRIEVAL CLEARANCE FILTER:
        Drops chunks where chunk.clearance_tier > user_clearance before calculating
        or returning matches.
        """
        query_vec = get_embedding(query)
        matches = []

        for chunk in self.chunks:
            # 1. HARD SECURITY CLEARANCE GATE
            if int(chunk.clearance_tier) > int(user_clearance):
                # Completely excluded - zero leakage
                continue

            # 2. SEMANTIC SIMILARITY
            score = cosine_similarity(query_vec, chunk.embedding)
            if score >= threshold:
                matches.append({
                    "chunk_id": chunk.chunk_id,
                    "doc_id": chunk.doc_id,
                    "title": chunk.title,
                    "clearance_tier": chunk.clearance_tier.name,
                    "clearance_level": int(chunk.clearance_tier),
                    "department": chunk.department,
                    "page": chunk.page,
                    "content": chunk.content,
                    "score": round(score, 4),
                    "citation": f"[{chunk.doc_id}, p.{chunk.page}]"
                })

        # Sort descending by score
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:top_k]

    def count_by_clearance(self) -> Dict[str, int]:
        counts = {"INTERNAL": 0, "CONFIDENTIAL": 0, "SECRET": 0}
        for chunk in self.chunks:
            counts[chunk.clearance_tier.name] = counts.get(chunk.clearance_tier.name, 0) + 1
        return counts

# Global singleton store instance
vector_store = SovereignVectorStore()
