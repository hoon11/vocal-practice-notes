# tests/test_watcher.py
import sys
import os
from pathlib import Path
import warnings

# Suppress warning about unsupported FP16 on CPU from Whisper
# This does not affect the correctness of the test because FP32 is used as fallback.
warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead"
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import threading
import time
import modules.watcher as watcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_watcher_ignores_existing_files(tmp_path, caplog):
    test_file = tmp_path / "already.wav"
    test_file.write_bytes(b"dummy")
    watcher.config["watcher"]["watch_folder"] = str(tmp_path)
    watcher.config["watcher"]["file_extension"] = ".wav"

    watcher.stop_event = threading.Event()
    watcher_thread = threading.Thread(target=watcher.start_watching)
    watcher_thread.start()

    time.sleep(2)
    watcher.stop_event.set()
    watcher_thread.join()

    logs = caplog.text
    assert "New file detected" not in logs


def test_watcher_detects_new_file(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    watcher.config["watcher"]["watch_folder"] = str(tmp_path)
    watcher.config["watcher"]["file_extension"] = ".wav"

    watcher.stop_event = threading.Event()
    watcher_thread = threading.Thread(target=watcher.start_watching)
    watcher_thread.start()

    new_file = tmp_path / "new.wav"
    test_audio = Path(__file__).parent / "resources" / "test_audio.wav"
    new_file.write_bytes(test_audio.read_bytes())

    time.sleep(3)
    watcher.stop_event.set()
    watcher_thread.join()

    logs = caplog.text
    assert "New file detected" in logs
