from fastapi import UploadFile, HTTPException

ALLOWED_AUDIO_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/flac",
    "audio/ogg",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def validate_audio_file(file: UploadFile):
    # Check whether a file was uploaded
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No audio file was uploaded."
        )

    # Check file type
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid audio format. Supported formats: WAV, MP3, FLAC, OGG."
        )

    # Check file size
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the maximum limit of 10 MB."
        )

    # Reset file position so the next service can read it
    await file.seek(0)

    return True