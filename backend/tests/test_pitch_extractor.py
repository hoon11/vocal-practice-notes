# tests/test_pitch_extractor.py
import pytest
from modules.pitch_extractor import extract_pitch
from modules.config_loader import load_config
from pathlib import Path
import json

@pytest.fixture
def test_config(tmp_path):
    config = load_config()
    config.pitch.output_dir = str(tmp_path)
    return config

def test_extract_pitch_output(test_config):
    """
    피치 분석 결과 파일 생성 체크
    Pitch extraction output file creation check
    ピッチ抽出結果ファイルの生成チェック
    """
    test_audio = Path(__file__).parent / "resources" / "test.wav"
    result = extract_pitch(test_audio, test_config)
    output_json = Path(test_config.pitch.output_dir) / "test_pitch.json"
    output_png = Path(test_config.pitch.output_dir) / "test_pitch.png"
    assert output_json.exists(), "Pitch JSON output not created"
    assert output_png.exists(), "Pitch PNG output not created"
    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "mean_pitch" in data
    assert "unvoiced_ratio" in data

def test_extract_pitch_missing_file(test_config):
    """
    존재하지 않는 파일 입력시 에러 체크
    Check error on nonexistent file input
    存在しないファイル入力時のエラーチェック
    """
    fake_path = Path("nonexistent.wav")
    with pytest.raises(FileNotFoundError):
        extract_pitch(fake_path, test_config)
