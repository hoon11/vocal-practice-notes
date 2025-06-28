# modules/event_queue.py
"""
이벤트 큐 및 워커 관리 모듈
イベントキューとワーカ管理モジュール
"""
from queue import Queue
from threading import Thread
from modules.event_types import AnalysisEvent
from modules.transcriber import transcribe
from modules.pitch_extractor import extract_pitch
from modules.formant_extractor import extract_formants
from modules.emotion_analyzer import analyze_emotion
import logging

logger = logging.getLogger(__name__)

# Global event queue
event_queue = Queue()

def handle_event(event: AnalysisEvent):
    """
    이벤트를 받아 실제 분석 함수 호출
    イベントを受けて実際の分析関数を呼び出す
    """
    try:
        if event.event_type == 'transcribe':
            transcribe(event.audio_path, event.config)
        elif event.event_type == 'pitch':
            extract_pitch(event.audio_path, event.config)
        elif event.event_type == 'formant':
            extract_formants(event.audio_path, event.config)
        elif event.event_type == 'emotion':
            analyze_emotion(event.audio_path, event.config)
        else:
            logger.warning(f"Unknown event type: {event.event_type}")
    except Exception as e:
        logger.error(f"Error processing {event.event_type}: {e}")
    finally:
        event_queue.task_done()

def start_workers(num_workers=4):
    """
    워커 스레드를 지정된 개수만큼 시작
    ワーカスレッドを指定数だけ開始
    """
    for _ in range(num_workers):
        Thread(target=event_worker, daemon=True).start()

def event_worker():
    """
    큐에서 이벤트를 받아 처리하는 워커
    キューからイベントを取得して処理するワーカー
    """
    while True:
        event = event_queue.get()
        handle_event(event)
