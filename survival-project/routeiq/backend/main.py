from fastapi import FastAPI
import os

app = FastAPI(
    title="AgentLoopGen",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 2",
        "service": "backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/info")
def info():
    return {
        "service": "AgentLoopGen",
        "version": "1.0",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "platform": "Render"
    }
