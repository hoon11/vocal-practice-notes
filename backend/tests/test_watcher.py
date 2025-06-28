import os
import signal
import time
import threading

from backend.modules import watcher

def test_watcher_graceful_shutdown():
    # Start watcher in a separate thread
    watcher_thread = threading.Thread(target=watcher.start)
    watcher_thread.start()

    # Give it a moment to initialize
    time.sleep(2)

    # Send SIGINT to simulate Ctrl+C
    os.kill(os.getpid(), signal.SIGINT)

    # Wait for watcher to shutdown
    watcher_thread.join(timeout=5)

    assert not watcher_thread.is_alive(), "🛑 Watcher did not shut down gracefully."