from fastapi import FastAPI

app = FastAPI(
    title="AgentLoopGen",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 1",
        "service": "backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
