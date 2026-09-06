"""
Immutable, append-only audit trail logging for all queries, model routing,
tool calls, retrieval citations, and zero-egress checks.
"""
import sqlite3
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.config import AUDIT_DIR

DB_PATH = AUDIT_DIR / "audit_trail.db"

def init_audit_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id TEXT NOT NULL,
            user_clearance INTEGER NOT NULL,
            query TEXT NOT NULL,
            lane TEXT NOT NULL,
            task_type TEXT NOT NULL,
            model_selected TEXT NOT NULL,
            tools_used TEXT NOT NULL,
            citations TEXT NOT NULL,
            deliverable TEXT,
            egress_packets INTEGER DEFAULT 0,
            execution_time_ms REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_audit_db()

def log_audit_entry(
    user_id: str,
    user_clearance: int,
    query: str,
    lane: str,
    task_type: str,
    model_selected: str,
    tools_used: List[str],
    citations: List[str],
    deliverable: Optional[str],
    egress_packets: int,
    execution_time_ms: float
):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat() + "Z"
    cursor.execute("""
        INSERT INTO audit_logs (
            timestamp, user_id, user_clearance, query, lane, task_type,
            model_selected, tools_used, citations, deliverable, egress_packets, execution_time_ms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now,
        user_id,
        user_clearance,
        query,
        lane,
        task_type,
        model_selected,
        json.dumps(tools_used),
        json.dumps(citations),
        deliverable or "",
        egress_packets,
        round(execution_time_ms, 2)
    ))
    conn.commit()
    conn.close()

def get_recent_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    logs = []
    for r in rows:
        logs.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "user_id": r["user_id"],
            "user_clearance": r["user_clearance"],
            "query": r["query"],
            "lane": r["lane"],
            "task_type": r["task_type"],
            "model_selected": r["model_selected"],
            "tools_used": json.loads(r["tools_used"]),
            "citations": json.loads(r["citations"]),
            "deliverable": r["deliverable"],
            "egress_packets": r["egress_packets"],
            "execution_time_ms": r["execution_time_ms"]
        })
    conn.close()
    return logs
