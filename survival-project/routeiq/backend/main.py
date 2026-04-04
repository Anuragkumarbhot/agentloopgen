from fastapi import FastAPI

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


@app.get("/info")
def info():
    return {
        "service": "AgentLoopGen",
        "version": "1.0",
        "environment": "production"
    }
