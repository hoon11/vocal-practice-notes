import threading
import time
import pathlib
from modules.watcher import DirectoryWatcher

def test_watcher_detects_new_wav(tmp_path):
    events = []
    shutdown = threading.Event()
    watcher = DirectoryWatcher(str(tmp_path), events.append, shutdown)
    t = threading.Thread(target=watcher.start, daemon=True)
    t.start()
    time.sleep(0.2)  # 감시 준비 시간 확보!

    test_file = tmp_path / "test.wav"
    test_file.write_bytes(b"dummy data")

    # 최대 5초간 polling (Windows/FS buffer 이슈까지 대응)
    deadline = time.time() + 5
    target_path = str(test_file.resolve())
    while time.time() < deadline:
        # 모든 이벤트를 절대경로(resolve)로 비교
        if any(pathlib.Path(e).resolve() == pathlib.Path(target_path) for e in events):
            break
        time.sleep(0.05)
    shutdown.set()
    t.join(timeout=2)

    assert any(pathlib.Path(e).resolve() == pathlib.Path(target_path) for e in events), f"{target_path} not in {events}"
