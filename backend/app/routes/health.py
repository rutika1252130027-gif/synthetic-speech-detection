from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Synthetic Speech Detection API is running"
    }