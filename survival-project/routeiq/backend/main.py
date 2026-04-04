from fastapi import FastAPI
import os
import psycopg2

app = FastAPI(title="AgentLoopGen")

@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 2",
        "service": "backend"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {"app": "AgentLoopGen", "version": "1.0"}

@app.get("/db-health")
def db_health():
    try:
        conn = psycopg2.connect(
            os.environ.get("DATABASE_URL")
        )
        conn.close()

        return {
            "database": "connected",
            "status": "ok"
        }

    except Exception as e:
        return {
            "database": "error",
            "details": str(e)
        }
