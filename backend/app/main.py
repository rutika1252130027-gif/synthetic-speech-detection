from fastapi import FastAPI
from app.routes import health, audio

app = FastAPI(
    title="Synthetic Speech Detection API",
    description="Backend API for detecting human and synthetic speech",
    version="1.0.0"
)

app.include_router(
    health.router,
    prefix="/api/health",
    tags=["Health"]
)

app.include_router(
    audio.router,
    prefix="/api/audio",
    tags=["Audio"]
)