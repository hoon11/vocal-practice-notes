# modules/transcriber.py
import whisper
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

def transcribe(audio_path: Path, config):
    """
    Transcribe an audio file using the Whisper model.
    Outputs the transcription result to a JSON file.
    """
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        model_size = config["transcriber"]["model_size"]
        model = whisper.load_model(model_size)
    except Exception as e:
        logger.error(f"Failed to load Whisper model [{model_size}]: {e}")
        raise

    try:
        result = model.transcribe(str(audio_path))
    except Exception as e:
        logger.error(f"Transcription failed for {audio_path}: {e}")
        raise

    transcripts_dir = config["transcriber"].get("transcripts_dir", "transcripts")
    output_path = Path(transcripts_dir) / (audio_path.stem + ".json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"Transcription saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to write transcription to {output_path}: {e}")
        raise