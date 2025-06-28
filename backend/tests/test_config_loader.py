import pytest
from modules.config_loader import load_config
import pydantic


def test_load_invalid_config(tmp_path):
    config_yaml = f"""
watcher:
  watch_folder: "tests/tmp"
  # file_extension: ".wav"  ← 필드 누락!
transcriber:
  model_size: "base"
  transcripts_dir: "tests/tmp"
pitch:
  output_dir: "tests/tmp"
formant:
  output_dir: "tests/tmp"
emotion:
  output_dir: "tests/tmp"
"""
    config_path = tmp_path / "valid.yaml"
    config_path.write_text(config_yaml, encoding="utf-8")
    from modules.config_loader import load_config

    config = load_config(str(config_path))
    assert config.watcher.file_extension == ".wav"
