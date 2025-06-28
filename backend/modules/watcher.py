import os
import time
import threading
import signal
from pathlib import Path

from backend.modules.config_loader import config  # Adjusted path for project structure

# English: Event to signal the thread to stop
# 日本語: スレッドの停止を通知するためのイベント
stop_event = threading.Event()

# English: Monitor the folder for new .wav files
# 日本語: 新しい.wavファイルを監視するスレッド
def start_watching():
    watched_folder = Path(config["watcher"]["watch_folder"])
    file_extension = config["watcher"]["file_extension"]
    processed_files = set()

    print(f"🔍 Watching folder: {watched_folder} for '*{file_extension}' files...")

    while not stop_event.is_set():
        for file in watched_folder.glob(f"*{file_extension}"):
            if file.name not in processed_files:
                print(f"📁 New file detected: {file.name}")
                processed_files.add(file.name)
                # You can insert your transcription or processing logic here

        time.sleep(1)  # Delay between checks

    print("🛑 Watcher stopped gracefully.")

# English: Signal handler to stop the thread
# 日本語: スレッドを停止するためのシグナルハンドラー
def signal_handler(sig, frame):
    print("🛑 Termination signal received.")
    stop_event.set()

# English: Entry point for starting the watcher with signal handling
# 日本語: シグナル処理付きの監視スレッドのエントリーポイント
def start():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    watch_thread = threading.Thread(target=start_watching)
    watch_thread.start()
    watch_thread.join()