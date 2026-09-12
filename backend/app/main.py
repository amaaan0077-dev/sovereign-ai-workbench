from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import APP_TITLE, APP_VERSION


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=(
        "Sovereign, on-premise, privacy-first "
        "agentic AI workbench for confidential "
        "industrial knowledge work."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "application": APP_TITLE,
        "version": APP_VERSION,
        "status": "online",
        "architecture": "sovereign-on-premise",
        "network_policy": "local-first",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "sovereign-ai-workbench",
    }


@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("SOVEREIGN INDUSTRIAL AI WORKBENCH")
    print("=" * 60)
    print(f"Application : {APP_TITLE}")
    print(f"Version     : {APP_VERSION}")
    print("Network     : Local / On-Premise")
    print("API         : FastAPI")
    print("=" * 60)