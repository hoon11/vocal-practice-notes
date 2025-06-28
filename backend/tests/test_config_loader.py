# tests/test_config_loader.py
import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from modules.config_loader import load_config
import tempfile
import yaml

def test_load_valid_config():
    config = load_config()
    assert "watcher" in config
    assert "transcriber" in config

def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent.yaml")

def test_load_invalid_yaml():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as tmp:
        tmp.write(b": invalid_yaml")
        tmp_path = tmp.name
    with pytest.raises(yaml.YAMLError):
        load_config(tmp_path)
    os.remove(tmp_path)