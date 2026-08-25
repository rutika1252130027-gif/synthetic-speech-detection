from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId

from app.services.audio_processor import extract_audio_features
from app.services.prediction_service import predict_audio
from app.database.mongodb import audio_analysis_collection


router = APIRouter()
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg"}



# Folder where uploaded audio files will be stored
UPLOAD_FOLDER = Path("app/uploads")

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):

    # Check if a file was selected
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    # Get and validate file extension
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Please upload WAV, MP3, FLAC, or OGG audio."
            )
        )

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = UPLOAD_FOLDER / unique_filename

    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract audio features
        audio_features = extract_audio_features(
            str(file_path)
        )

        # Get prediction
        prediction_result = predict_audio(
            str(file_path)
        )

        # Create MongoDB document
        analysis_document = {
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_path": str(file_path),

            "audio_info": {
                "sample_rate": audio_features["sample_rate"],
                "duration": audio_features["duration"],
                "samples": audio_features["samples"]
            },

            "prediction": prediction_result["prediction"],
            "confidence": prediction_result["confidence"],
            "analysis": prediction_result["analysis"],

            "created_at": datetime.utcnow()
        }

        # Save analysis to MongoDB
        result = audio_analysis_collection.insert_one(
            analysis_document
        )

        return {
            "message": "Audio uploaded and processed successfully",

            "analysis_id": str(result.inserted_id),

            "filename": unique_filename,
            "original_filename": file.filename,

            "audio_features": audio_features,
            "prediction": prediction_result
        }

    except HTTPException:
        raise

    except Exception as e:

        # Remove uploaded file if processing fails
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=f"Unable to process the audio file: {str(e)}"
        )

    finally:
        await file.close()
        
@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: str):

    # Check whether the MongoDB ObjectId is valid
    try:
        object_id = ObjectId(analysis_id)

    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis ID"
        )

    # Find the analysis in MongoDB
    analysis = audio_analysis_collection.find_one(
        {"_id": object_id}
    )

    # If no analysis exists
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    # Convert ObjectId to string so it can be returned as JSON
    analysis["_id"] = str(analysis["_id"])

    return analysis

@router.get("/history")
def get_analysis_history(limit: int = 10):

    # Get analyses sorted by newest first
    analyses = list(
        audio_analysis_collection
        .find()
        .sort("created_at", -1)
        .limit(limit)
    )

    # Convert MongoDB values to JSON-compatible values
    for analysis in analyses:

        analysis["_id"] = str(analysis["_id"])

        if "created_at" in analysis:
            analysis["created_at"] = analysis["created_at"].isoformat()

    return {
        "total_analyses": len(analyses),
        "analyses": analyses
    }