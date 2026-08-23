from fastapi import APIRouter
from app.database.mongodb import client

router = APIRouter()


@router.get("/")
def health_check():
    try:
        # Check MongoDB connection
        client.admin.command("ping")

        return {
            "status": "healthy",
            "database": "connected",
            "message": "Synthetic Speech Detection API is running"
        }

    except Exception:
        return {
            "status": "healthy",
            "database": "disconnected",
            "message": "API is running, but database connection failed"
        }