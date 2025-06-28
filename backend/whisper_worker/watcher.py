import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from whisper_worker.transcriber import transcribe
from whisper_worker.config_loader import load_config

# 설정 로드
config = load_config()
input_dir = config["watcher"]["input_dir"]
output_dir = config["watcher"]["output_dir"]
file_extensions = config["watcher"]["file_extensions"]
recursive = config["watcher"].get("recursive", False)

class AudioHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if any(event.src_path.endswith(ext) for ext in file_extensions):
            print(f"Detected new audio: {event.src_path}")
            output = transcribe(event.src_path, output_dir)
            print(f"Transcription saved to: {output}")

def start_watch():
    event_handler = AudioHandler()
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=recursive)
    observer.start()
    print(f"📡 Watching '{input_dir}' for: {file_extensions}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
