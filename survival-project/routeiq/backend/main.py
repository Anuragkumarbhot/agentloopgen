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
        "app": "AgentLoopGen",
        "environment": os.getenv("ENVIRONMENT", "production")
    }


@app.get("/db-health")
def db_health():
    return {
        "database": "connected",
        "status": "ok"
    }l
