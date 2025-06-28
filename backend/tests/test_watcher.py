import pytest
import threading
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import modules.watcher as watcher

@pytest.fixture
def temp_watch_dir(tmp_path):
    """Create a temporary directory for watcher testing."""
    return tmp_path

def test_watcher_detects_new_file(monkeypatch, temp_watch_dir):
    """
    Test that start_watching detects new files and prints the correct message.
    """
    # Patch config to use temp dir and .wav extension
    fake_config = {
        "watcher": {
            "watch_folder": str(temp_watch_dir),
            "file_extension": "wav"
        }
    }
    monkeypatch.setattr(watcher, "config", fake_config)

    # Track print output
    output = []
    monkeypatch.setattr("builtins.print", lambda x: output.append(x))

    # Patch stop_event to a new Event instance for each test
    event = threading.Event()
    monkeypatch.setattr(watcher, "stop_event", event)

    # Run watcher in a thread (as in start())
    thread = threading.Thread(target=watcher.start_watching)
    thread.start()
    time.sleep(0.5)  # Let watcher start

    # Add new wav file
    test_wav = temp_watch_dir / "test123.wav"
    test_wav.write_bytes(b"RIFF....WAVEfmt ")
    time.sleep(1.5)  # Give time for watcher to detect

    # Stop watcher
    event.set()
    thread.join(timeout=2)

    # Check that watcher printed detection message
    detected = any("New file detected" in msg for msg in output)
    assert detected, "Watcher must print detection message for new file"

def test_watcher_graceful_stop(monkeypatch, temp_watch_dir):
    """
    Test that watcher stops gracefully when stop_event is set.
    """
    fake_config = {
        "watcher": {
            "watch_folder": str(temp_watch_dir),
            "file_extension": "wav"
        }
    }
    monkeypatch.setattr(watcher, "config", fake_config)
    event = threading.Event()
    monkeypatch.setattr(watcher, "stop_event", event)

    thread = threading.Thread(target=watcher.start_watching)
    thread.start()
    time.sleep(0.5)
    event.set()  # Request graceful stop
    thread.join(timeout=2)
    assert not thread.is_alive(), "Watcher thread must exit gracefully"

def test_watcher_ignores_existing_files(monkeypatch, temp_watch_dir):
    """
    Test that watcher does not re-detect files already processed.
    """
    fake_config = {
        "watcher": {
            "watch_folder": str(temp_watch_dir),
            "file_extension": "wav"
        }
    }
    monkeypatch.setattr(watcher, "config", fake_config)
    event = threading.Event()
    monkeypatch.setattr(watcher, "stop_event", event)
    output = []
    monkeypatch.setattr("builtins.print", lambda x: output.append(x))

    # Pre-create a file before watcher starts
    preexisting = temp_watch_dir / "existing.wav"
    preexisting.write_bytes(b"RIFF....WAVEfmt ")

    thread = threading.Thread(target=watcher.start_watching)
    thread.start()
    time.sleep(1)
    event.set()
    thread.join(timeout=2)

    # It should NOT print detection for preexisting file
    detected = any("New file detected" in msg for msg in output)
    assert not detected, "Watcher should not detect already existing files"
