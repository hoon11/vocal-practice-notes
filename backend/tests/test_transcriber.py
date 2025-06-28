import pytest
from pathlib import Path
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.transcriber import transcribe


# Dummy Whisper model for deterministic test
class DummyModel:
    def transcribe(self, audio_path):
        # Always return the same result for testing
        return {"text": "test transcription"}


def dummy_load_model(model_size):
    return DummyModel()


@pytest.fixture
def config():
    """Returns minimal valid config dict"""
    return {"transcriber": {"model_size": "base"}}


def test_transcribe_creates_json(monkeypatch, tmp_path, config):
    """
    Test that transcribe creates a .json file with correct content.
    """
    # Patch whisper.load_model and Path to use tmp_path for output
    monkeypatch.setattr("modules.transcriber.whisper.load_model", dummy_load_model)
    orig_Path = Path

    def custom_Path(arg=""):
        if arg == "transcripts":
            return tmp_path / "transcripts"
        return orig_Path(arg)

    monkeypatch.setattr("modules.transcriber.Path", custom_Path)

    # Create dummy audio file
    audio_file = tmp_path / "sample.wav"
    audio_file.write_bytes(b"RIFF....WAVEfmt ")

    transcribe(audio_file, config)

    output_file = tmp_path / "transcripts" / "sample.json"
    assert output_file.exists(), "Output JSON file must be created"
    with open(output_file, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert result.get("text") == "test transcription"


def test_transcribe_prints_success(monkeypatch, tmp_path, config, capsys):
    """
    Test that transcribe prints the correct output path.
    """
    monkeypatch.setattr("modules.transcriber.whisper.load_model", dummy_load_model)
    orig_Path = Path

    def custom_Path(arg=""):
        if arg == "transcripts":
            return tmp_path / "transcripts"
        return orig_Path(arg)

    monkeypatch.setattr("modules.transcriber.Path", custom_Path)
    audio_file = tmp_path / "test.wav"
    audio_file.write_bytes(b"RIFF....WAVEfmt ")

    transcribe(audio_file, config)
    out = capsys.readouterr()
    assert "Transcription saved to" in out.out


def test_transcribe_handles_nonexistent_file(monkeypatch, tmp_path, config):
    """
    Test that transcribe raises an error when audio file does not exist.
    """
    monkeypatch.setattr("modules.transcriber.whisper.load_model", dummy_load_model)
    orig_Path = Path

    def custom_Path(arg=""):
        if arg == "transcripts":
            return tmp_path / "transcripts"
        return orig_Path(arg)

    monkeypatch.setattr("modules.transcriber.Path", custom_Path)
    non_exist_audio = tmp_path / "not_exist.wav"
    with pytest.raises(Exception):
        transcribe(non_exist_audio, config)
