from fastapi import FastAPI
import os

app = FastAPI(
    title="AgentLoopGen",
    version="2.0"
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


# Database health check (simple test endpoint)
@app.get("/db-health")
def db_health():
    return {
        "database": "connected",
        "status": "ok"
    }


# Info endpoint
@app.get("/info")
def info():
    return {
        "app": "AgentLoopGen",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "version": "2.0"
    }
