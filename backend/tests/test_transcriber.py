# tests/test_transcriber.py
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from modules.transcriber import transcribe
from modules.config_loader import load_config
import shutil
import json
import warnings

# Suppress warning about unsupported FP16 on CPU from Whisper
# This does not affect the correctness of the test because FP32 is used as fallback.
warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead"
)


def test_transcribe_creates_json():
    config = load_config()
    test_audio_path = Path(__file__).parent / "resources" / "test_audio.wav"
    tmp_output_dir = Path(__file__).parent / "output_test"
    tmp_output_dir.mkdir(exist_ok=True)
    config["transcriber"]["transcripts_dir"] = str(tmp_output_dir)

    transcribe(test_audio_path, config)

    output_path = tmp_output_dir / "test_audio.json"
    assert output_path.exists(), "Transcription JSON file should be created"

    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "text" in data

    shutil.rmtree(tmp_output_dir)


def test_transcribe_handles_nonexistent_file():
    config = load_config()
    fake_path = Path("not_exist.wav")
    with pytest.raises(FileNotFoundError):
        transcribe(fake_path, config)
