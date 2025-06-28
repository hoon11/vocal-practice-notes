# tests/test_config_loader.py
import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from modules.config_loader import load_config
import tempfile
import yaml

def test_load_valid_config(tmp_path):
    cfg = tmp_path / "valid.yaml"
    cfg.write_text("""
    whisper_model: base
    use_whisper: true
    watch_folder: ./audio
    output_folder: ./output
    """, encoding="utf-8")
    from modules import config_loader
    config = config_loader.load_config(str(cfg))
    assert config.whisper_model == "base"
    assert config.use_whisper is True

def test_env_override(monkeypatch, tmp_path):
    cfg = tmp_path / "valid.yaml"
    cfg.write_text("""
    whisper_model: base
    use_whisper: false
    watch_folder: ./audio
    output_folder: ./output
    """, encoding="utf-8")
    monkeypatch.setenv("USE_WHISPER", "true")
    from modules import config_loader
    config = config_loader.load_config(str(cfg))
    assert config.use_whisper is True
