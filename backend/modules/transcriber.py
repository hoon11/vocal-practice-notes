"""
modules/transcriber.py

Whisper transcription with config validation, model caching, and multilingual comments.
Whisper音声認識: 設定バリデーション・モデルキャッシュ・多言語コメント。
"""

import whisper
from pathlib import Path
import json
import logging
import threading

logger = logging.getLogger(__name__)

_model_lock = threading.Lock()
_loaded_models = {}

def get_whisper_model(model_size: str):
    """
    Load and cache Whisper model by size.
    Whisperモデルをキャッシュして再利用
    """
    with _model_lock:
        if model_size not in _loaded_models:
            try:
                _loaded_models[model_size] = whisper.load_model(model_size)
                logger.info(f"Loaded Whisper model: {model_size}")
            except Exception as e:
                logger.error(f"Failed to load Whisper model [{model_size}]: {e}")
                raise
        return _loaded_models[model_size]

def transcribe(audio_path: Path, config):
    """
    Transcribe an audio file using Whisper, output JSON.
    Whisperで音声ファイルをテキスト化し、結果をJSONで保存。
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        model_size = config.transcriber.model_size
        model = get_whisper_model(model_size)
    except Exception as e:
        logger.error(f"Model load/config failed: {e} / config: {config}")
        raise

    try:
        result = model.transcribe(str(audio_path))
    except Exception as e:
        logger.error(f"Transcription failed: {audio_path} / {e}")
        raise

    transcripts_dir = config.transcriber.transcripts_dir
    output_path = Path(transcripts_dir) / (audio_path.stem + ".json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"Transcription saved: {output_path}")
    except Exception as e:
        logger.error(f"Failed to write transcription: {output_path} / {e}")
        raise

    return output_path
