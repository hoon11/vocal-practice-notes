# tests/test_transcriber.py
import pytest
from pathlib import Path
from modules.transcriber import transcribe, get_whisper_model
from modules.config_loader import load_config
import json
import shutil

@pytest.fixture
def test_config(tmp_path):
    config = load_config()
    config.transcriber.transcripts_dir = str(tmp_path)
    return config

def test_transcribe_creates_json(test_config):
    test_path = Path(__file__).parent / "resources" / "test.wav"
    output_path = transcribe(test_path, test_config)
    assert output_path.exists()
    with open(output_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "text" in data
    assert isinstance(data["text"], str)
    if output_path.exists():
        output_path.unlink()

def test_transcribe_returns_correct_path(test_config):
    test_path = Path(__file__).parent / "resources" / "test.wav"
    result_path = transcribe(test_path, test_config)
    assert str(result_path).endswith(".json")
    assert result_path.exists()
    if result_path.exists():
        result_path.unlink()

def test_transcribe_handles_nonexistent_file(test_config):
    fake_path = Path("not_exist.wav")
    with pytest.raises(FileNotFoundError):
        transcribe(fake_path, test_config)

def test_transcribe_invalid_config(tmp_path):
    test_path = Path(__file__).parent / "resources" / "test.wav"
    class DummyConfig:
        pass
    bad_config = DummyConfig()
    with pytest.raises(AttributeError):
        transcribe(test_path, bad_config)

def test_model_caching(test_config):
    from modules.transcriber import _loaded_models
    _loaded_models.clear()
    model_size = test_config.transcriber.model_size
    model1 = get_whisper_model(model_size)
    model2 = get_whisper_model(model_size)
    assert model1 is model2, "Whisper model should be cached and reused"

@pytest.fixture(autouse=True)
def clean_output_dir(test_config):
    yield
    out_dir = Path(test_config.transcriber.transcripts_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir, ignore_errors=True)
