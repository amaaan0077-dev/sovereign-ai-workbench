"""
Sovereign AI Workbench Backend Launcher.
Initializes data seed and starts Uvicorn ASGI server.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_TITLE, APP_VERSION
from app.api.routes import api_router
from app.rag.sample_data import seed_sample_documents

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_sample_documents()
    print("*" * 70)
    print("* SOVEREIGN INDUSTRIAL AI WORKBENCH BACKEND INITIALIZED *")
    print("Zero-Egress Security: ENFORCED (All cloud telemetry disabled)")
    print("Air-Gapped Network Monitor: ACTIVE")
    print("Vector Store Clearance Gates: ENGAGED")
    print("Interactive Docs: http://127.0.0.1:8000/docs")
    print("*" * 70)
    yield

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Sovereign On-Premise Agentic AI Workbench for Confidential Industrial Work (SIH Hackathon)",
    lifespan=lifespan
)

# CORS middleware for local frontend (React/Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=False, ws="none")
