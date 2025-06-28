# tests/test_pitch_extractor.py
import sys
import os
import shutil
from pathlib import Path
import pytest
import json
import warnings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

from modules.pitch_extractor import extract_pitch
from modules.config_loader import load_config

def test_extract_pitch_output(tmp_path):
    config = load_config()
    config["pitch"]["output_dir"] = str(tmp_path)

    test_audio = Path(__file__).parent / "resources" / "test_audio.wav"
    result = extract_pitch(test_audio, config)

    output_json = tmp_path / "test_audio_pitch.json"
    output_png = tmp_path / "test_audio_pitch.png"

    assert output_json.exists(), "Pitch JSON output not created"
    assert output_png.exists(), "Pitch PNG output not created"

    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "mean_pitch" in data
    assert "unvoiced_ratio" in data

def test_extract_pitch_missing_file():
    config = load_config()
    fake_path = Path("nonexistent.wav")
    with pytest.raises(FileNotFoundError):
        extract_pitch(fake_path, config)
