# modules/watcher.py

from pathlib import Path
import time
import logging
from modules.transcriber import transcribe
from modules.config_loader import load_config

logger = logging.getLogger(__name__)
stop_event = None
config = load_config()

def start_watching():
    """
    Watch the configured folder for new audio files and transcribe them.
    Skips files that already existed at startup.
    """
    watched_folder = Path(config["watcher"]["watch_folder"])
    file_extension = config["watcher"]["file_extension"]

    if not watched_folder.exists():
        logger.error(f"Watch folder does not exist: {watched_folder}")
        return

    processed_files = set(f.name for f in watched_folder.glob(f"*{file_extension}"))
    logger.info(f"Watching folder: {watched_folder} for '*{file_extension}' files...")

    while not stop_event.is_set():
        for file in watched_folder.glob(f"*{file_extension}"):
            if file.name not in processed_files:
                logger.info(f"New file detected: {file.name}")
                processed_files.add(file.name)
                try:
                    transcribe(file, config)
                except Exception as e:
                    logger.error(f"Failed to process {file}: {e}")
        time.sleep(1)

    logger.info("Watcher stopped gracefully.")
