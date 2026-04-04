from fastapi import FastAPI
from database import check_db
import os

app = FastAPI(
    title="AgentLoopGen API",
    version="2.0.0"
)


# Root endpoint
@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 2",
        "service": "backend"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "backend"
    }


# Database health check
@app.get("/db-health")
def db_health():
    return check_db()


# Info endpoint
@app.get("/info")
def info():
    return {
        "app": "AgentLoopGen",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "version": "2.0.0"
    }
