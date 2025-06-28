# tests/test_emotion_analyzer.py
import pytest
from modules.emotion_analyzer import analyze_emotion
from modules.config_loader import load_config
from pathlib import Path
import json

@pytest.fixture
def test_config(tmp_path):
    config = load_config()
    config.emotion.output_dir = str(tmp_path)
    return config

def test_analyze_emotion_output(test_config):
    """
    감정 분석 결과 생성 및 필드 체크
    Emotion analysis result generation and field check
    感情分析結果の生成およびフィールドチェック
    """
    test_audio = Path(__file__).parent / "resources" / "test.wav"
    result = analyze_emotion(test_audio, test_config)
    output_json = Path(test_config.emotion.output_dir) / f"{test_audio.stem}_emotion.json"
    assert output_json.exists()
    with open(output_json, encoding="utf-8") as f:
        data = json.load(f)
    assert "predicted_emotion" in data
