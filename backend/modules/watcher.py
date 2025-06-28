# modules/watcher.py (중요 부분만)
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

logger = logging.getLogger(__name__)

class AudioFileEventHandler(FileSystemEventHandler):
    """
    Handles new audio file creation events
    新しい音声ファイル作成イベントを処理する
    """
    def __init__(self, on_new_audio, file_extension=".wav"):
        self.on_new_audio = on_new_audio
        self.file_extension = file_extension

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_extension):
            logger.info(f"New audio file detected: {event.src_path}")
            self.on_new_audio(Path(event.src_path))

class DirectoryWatcher:
    """
    폴더 감시 스레드 관리 클래스
    ディレクトリ監視スレッド管理クラス
    """
    def __init__(self, watch_folder, on_new_audio, shutdown_event=None, file_extension=".wav"):
        self.watch_folder = Path(watch_folder)
        self.on_new_audio = on_new_audio
        self.shutdown_event = shutdown_event or threading.Event()
        self.file_extension = file_extension

    def start(self):
        event_handler = AudioFileEventHandler(self.on_new_audio, self.file_extension)
        observer = Observer()
        observer.schedule(event_handler, str(self.watch_folder), recursive=False)
        observer.start()
        logger.info(f"Started watcher on: {self.watch_folder} (*{self.file_extension})")
        try:
            while not self.shutdown_event.is_set():
                time.sleep(0.5)
        finally:
            observer.stop()
            observer.join()
            logger.info("Watcher stopped.")
