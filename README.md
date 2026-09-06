# Sovereign On-Premise Agentic AI Workbench for Confidential Industrial Work
**SIH Hackathon Edition** | Air-Gapped | Multi-Model Dynamic Routing | Proven Zero-Egress

---

## 🏛️ Project Architecture & Overview

This system provides a sovereign, air-gapped AI platform designed for Refineries, PSUs (ONGC, IOCL, GAIL), Defense setups, and Government bodies handling classified knowledge work:
- **Zero-Egress Enforcement:** All third-party telemetry (`HF_HUB_DISABLE_TELEMETRY`, `LANGCHAIN_TRACING_V2`, etc.) disabled at the process level. Real-time socket inspector validates 0 outbound packets.
- **Dual-Lane Routing:**
  - **Lane A (General Knowledge):** Model weights only, 0 database lookup.
  - **Lane B (Company Confidential):** Grounded strictly via clearance-gated local RAG.
- **Pre-Retrieval Clearance Access Control:** Documents tagged with `INTERNAL`, `CONFIDENTIAL`, or `SECRET`. Lower clearance users are hard-filtered at the vector-search layer (complete mathematical exclusion, not a prompt refusal).
- **Sandboxed Code Execution:** Network-disabled, resource-capped execution of engineering calculations.
- **Deliverable Generation:** Compiles native Microsoft Word `.docx` Approval Notes and `.xlsx` calculation sheets with formal government/PSU headers, math breakdowns, and verifiable citations.
- **Industrial Control Console UI:** Precision-engineered React/Vite dashboard modeled after plant DCS control panels (IBM Plex Sans + JetBrains Mono, live air-gap telemetry badge, tri-column layout).

---

## 📂 Project Structure (Located at `D:\sovereign-ai-workbench`)

```
D:\sovereign-ai-workbench/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py           # Air-gap flags & storage directories
│   │   │   ├── security.py         # Clearance tiers (Internal, Confidential, Secret) & Personas
│   │   │   └── audit_logger.py     # SQLite append-only audit trail
│   │   ├── models/
│   │   │   └── router.py           # Lane A/B classifier & dynamic model registry (Qwen2.5-Coder/VL/14B)
│   │   ├── rag/
│   │   │   ├── embeddings.py       # 100% offline local dense semantic vectorizer
│   │   │   ├── vector_store.py     # Clearance-filtered vector store
│   │   │   └── sample_data.py      # Seed industrial SOPs, crack reports, crude quotas
│   │   ├── agent/
│   │   │   ├── workflow.py         # Multi-step agent loop (Plan -> RAG -> Code -> DocGen)
│   │   │   └── tools/
│   │   │       ├── doc_search.py   # Clearance-gated search tool
│   │   │       ├── sandbox_code.py # Isolated network-blocked code sandbox
│   │   │       └── doc_gen.py      # Native Word (.docx) approval note compiler
│   │   ├── services/
│   │   │   ├── network_monitor.py  # Live socket monitor proving 0 outbound packets
│   │   │   └── llm_provider.py     # Local Ollama/vLLM integration + offline air-gap fallback
│   │   └── api/
│   │       ├── schemas.py          # Pydantic request/response schemas
│   │       └── routes.py           # FastAPI REST API endpoints
│   ├── storage/
│   │   ├── deliverables/           # Generated .docx approval notes
│   │   └── audit/                  # SQLite audit database (audit_trail.db)
│   ├── requirements.txt
│   ├── run.py                      # FastAPI server launcher
│   └── test_demo.py                # Automated Hackathon validation suite
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TopRail.jsx         # Persistent air-gap status, sockets & clearance switcher
│   │   │   ├── GroundingPanel.jsx  # Clearance-gated document repository & model registry
│   │   │   ├── WorkspacePanel.jsx  # Interactive operator console & 1-click evaluation presets
│   │   │   ├── AuditProvenancePanel.jsx # Hero deliverable (.docx) card & network socket audit
│   │   │   └── SystemFooter.jsx    # Air-gap mandate & hardware profile footer
│   │   ├── services/
│   │   │   └── api.js              # Backend REST API client
│   │   ├── App.jsx
│   │   ├── index.css               # Industrial styling & CSS variables
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🚀 How to Run the Complete Stack

### Terminal 1: Start the Backend
```powershell
cd D:\sovereign-ai-workbench\backend
python run.py
```
*Backend runs on `http://127.0.0.1:8000` (API Docs: `http://127.0.0.1:8000/docs`)*

### Terminal 2: Start the Frontend UI
```powershell
cd D:\sovereign-ai-workbench\frontend
npm run dev
```
*Frontend runs on `http://localhost:5173`*

---

## 🎯 Hackathon Judge Evaluation Flow (in UI)

1. **Step 1: Point to Top Rail**
   - Show the **`AIR-GAP INTEGRITY: [VERIFIED ZERO-EGRESS]`** badge and the active socket count (`0 WAN PACKETS`).
2. **Step 2: Test Lane A (General Knowledge)**
   - Click preset **`TEST LANE A (GENERAL PHYSICS)`**.
   - Show how the agent uses model weights only and **completely bypasses the vector store (0 database operations)**.
3. **Step 3: Test Adversarial Clearance Gate**
   - Select operator **Rahul Verma (INTERNAL - L1)**.
   - Click preset **`ADVERSARIAL CLEARANCE TEST`** (queries Strategic Crude Reserves).
   - Show that the Secret document is **mathematically dropped at the vector pre-search layer** (returns 0 citations, 0 leakage).
   - Now switch operator to **Dr. V. K. Sharma (SECRET - L3)** and run it again: the document is retrieved with full citations!
4. **Step 4: The Hero Deliverable Demo**
   - Click preset **`HERO DEMO: AGENTIC APPROVAL NOTE`**.
   - Watch the multi-step execution trace:
     - Retrieves ultrasonic crack measurements from Unit-4.
     - Runs the derating formula inside the network-disabled sandbox (`socket.socket = blocked`).
     - Autonomously compiles a native Microsoft Word **Approval Note (`.docx`)**.
   - Click **`DOWNLOAD VERIFIED .DOCX`** in the right panel to open the real, formatted Word document on your laptop!
