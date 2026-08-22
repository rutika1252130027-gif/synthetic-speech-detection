from fastapi import FastAPI
from app.routes import health

app = FastAPI(
    title="Synthetic Speech Detection API",
    description="Backend API for detecting human, synthetic, and partially synthetic speech.",
    version="1.0.0"
)

app.include_router(
    health.router,
    prefix="/api/health",
    tags=["Health"]
)