import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config_loader import load_config
from whisper_worker.transcriber import transcribe

# Load configuration
# 設定を読み込む
config = load_config()
watcher_cfg = config.get("watcher", {})
input_dir = watcher_cfg.get("input_dir", "audio")
output_dir = watcher_cfg.get("output_dir", "transcripts")
file_extensions = watcher_cfg.get("file_extensions", [".wav"])
recursive = watcher_cfg.get("recursive", False)

class AudioFileHandler(FileSystemEventHandler):
    """
    Handle new file creation events in the watched directory.
    監視対象ディレクトリ内でのファイル作成イベントを処理するクラス
    """

    def on_created(self, event):
        # Skip directories
        # ディレクトリは無視する
        if event.is_directory:
            return

        file_path = event.src_path
        _, ext = os.path.splitext(file_path)

        # Check file extension
        # 対象の拡張子か確認
        if ext.lower() in file_extensions:
            print(f"[INFO] Detected new audio file: {file_path}")
            try:
                output_path = transcribe(file_path, output_dir)
                print(f"[INFO] Transcription saved to: {output_path}")
            except Exception as e:
                print(f"[ERROR] Failed to transcribe {file_path}: {e}")

def start_watching():
    """
    Start watching the configured input directory.
    指定された入力ディレクトリの監視を開始する。
    """
    print(f"[INFO] Watching folder: {input_dir} (recursive={recursive})")
    event_handler = AudioFileHandler()
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=recursive)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watching()
