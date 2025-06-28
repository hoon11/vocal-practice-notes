"""
modules/watcher.py

Directory watcher for .wav files using watchdog, with DI/event support.
.wavファイル専用のディレクトリ監視 (DI・イベント指向拡張可能)。
"""

import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AudioFileEventHandler(FileSystemEventHandler):
    """
    Handles .wav file creation events and triggers the provided callback.
    .wavファイル作成イベント時にコールバック実行
    """
    def __init__(self, on_new_audio):
        super().__init__()
        self.on_new_audio = on_new_audio
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.wav'):
            self.on_new_audio(event.src_path)

class DirectoryWatcher:
    """
    Watches a directory for .wav files and emits events via callback or queue.
    .wavファイルの新規作成を監視し、コールバック/キューで通知
    """
    def __init__(self, watch_folder, on_new_audio, shutdown_event=None):
        self.watch_folder = str(watch_folder)
        self.on_new_audio = on_new_audio  # 외부에서 주입: 콜백 or 큐.put
        self.shutdown_event = shutdown_event or threading.Event()
        self.observer = Observer()
        self.event_handler = AudioFileEventHandler(self.on_new_audio)
    
    def start(self):
        """Start watching the directory. ディレクトリ監視開始"""
        self.observer.schedule(self.event_handler, self.watch_folder, recursive=False)
        self.observer.start()
        try:
            while not self.shutdown_event.is_set():
                self.shutdown_event.wait(1)
        except Exception as e:
            print(f"Watcher exception: {e}")
        finally:
            self.observer.stop()
            self.observer.join()
    
    def stop(self):
        """Gracefully stop watching. 監視を停止"""
        self.shutdown_event.set()
        self.observer.stop()
        self.observer.join()

# ---- 예시 사용법 / 使用例 ----
if __name__ == "__main__":
    import queue
    import time

    # 이벤트 큐 활용 예시 (확장성 대비)
    audio_event_queue = queue.Queue()

    def on_new_audio(filepath):
        print(f"Detected: {filepath}")
        audio_event_queue.put(filepath)

    shutdown = threading.Event()
    watcher = DirectoryWatcher("./audio", on_new_audio, shutdown)
    thread = threading.Thread(target=watcher.start, daemon=True)
    thread.start()

    try:
        time.sleep(10)  # 예시: 10초간 감시
    finally:
        shutdown.set()
        thread.join()
