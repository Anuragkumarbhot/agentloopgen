from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI(
    title="AgentLoopGen",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-health")
def db_health():
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
