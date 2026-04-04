from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI(
    title="AgentLoopGen",
    version="1.0"
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 3",
        "service": "backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-health")
def db_health():
    if engine is None:
        return {
            "database": "not configured"
        }

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "error",
            "message": str(e)
        }
