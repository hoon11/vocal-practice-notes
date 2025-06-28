# modules/event_types.py
"""
Analysis Event 객체 및 타입 정의
分析イベントオブジェクトとタイプ定義
"""
from pathlib import Path

class AnalysisEvent:
    """
    Analysis event for queue processing
    キュー処理用分析イベント
    """
    def __init__(self, event_type: str, audio_path: Path, config):
        self.event_type = event_type  # 'transcribe', 'pitch', 'formant', 'emotion'
        self.audio_path = audio_path
        self.config = config
