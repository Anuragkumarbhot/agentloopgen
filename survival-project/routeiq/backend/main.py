from fastapi import FastAPI
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0"
)


@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


@app.get("/info")
def info():
    return {
        "app": settings.APP_NAME,
        "env": settings.ENVIRONMENT,
        "port": settings.PORT
    }
