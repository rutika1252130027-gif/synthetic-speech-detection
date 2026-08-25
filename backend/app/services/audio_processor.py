import librosa
import numpy as np


def extract_audio_features(file_path: str):
    """
    Load an audio file and extract basic audio features.
    """

    # Load audio
    audio, sample_rate = librosa.load(
        file_path,
        sr=16000,
        mono=True
    )

    # Calculate duration
    duration = librosa.get_duration(
        y=audio,
        sr=sample_rate
    )

    # Extract 13 MFCC features
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sample_rate,
        n_mfcc=13
    )

    return {
        "sample_rate": sample_rate,
        "duration": round(float(duration), 2),
        "samples": len(audio),

        "mfcc_shape": list(mfcc.shape),

        "mfcc_mean": np.mean(
            mfcc,
            axis=1
        ).round(4).tolist(),

        "mfcc_std": np.std(
            mfcc,
            axis=1
        ).round(4).tolist()
    }