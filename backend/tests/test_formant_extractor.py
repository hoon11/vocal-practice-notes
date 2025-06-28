import pytest
from modules.formant_extractor import extract_formants
from modules.config_loader import load_config
from pathlib import Path
import json

@pytest.fixture
def test_config(tmp_path):
    config = load_config()
    config.formant.output_dir = str(tmp_path)
    return config

def test_extract_formants_output(test_config):
    test_audio = Path(__file__).parent / "resources" / "test.wav"
    result = extract_formants(test_audio, test_config)
    output_json = Path(test_config.formant.output_dir) / f"{test_audio.stem}_formant.json"
    assert output_json.exists()
    with open(output_json, encoding="utf-8") as f:
        data = json.load(f)
    assert "F1" in data and "F2" in data and "F3" in data
