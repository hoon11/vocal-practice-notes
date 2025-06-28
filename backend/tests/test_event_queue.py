import pytest
from queue import Queue
from pathlib import Path

from modules.event_types import AnalysisEvent

@pytest.fixture
def dummy_config():
    """
    더미 Config 객체(Mock)
    ダミーConfigオブジェクト（モック）
    """
    class DummyConfig:
        pass
    return DummyConfig()

def test_analysis_event_fields(dummy_config):
    """
    AnalysisEvent 필드/생성 검증  
    AnalysisEventのフィールド/生成検証
    """
    event = AnalysisEvent('pitch', Path('audio.wav'), dummy_config)
    assert event.event_type == 'pitch'
    assert event.audio_path == Path('audio.wav')
    assert event.config is dummy_config

def test_event_queue_put_get(dummy_config):
    """
    큐에 이벤트 put/get 동작 테스트  
    キューへのイベントput/get動作テスト
    """
    q = Queue()
    event = AnalysisEvent('formant', Path('audio2.wav'), dummy_config)
    q.put(event)
    out_event = q.get()
    assert isinstance(out_event, AnalysisEvent)
    assert out_event.event_type == 'formant'
    assert out_event.audio_path == Path('audio2.wav')
    assert out_event.config is dummy_config

def test_multiple_events(dummy_config):
    """
    여러 이벤트를 순서대로 큐에 넣고 꺼내는 동작 테스트  
    複数イベントを順番にキューに入れ取得する動作テスト
    """
    q = Queue()
    events = [
        AnalysisEvent('transcribe', Path('a.wav'), dummy_config),
        AnalysisEvent('pitch', Path('b.wav'), dummy_config),
        AnalysisEvent('formant', Path('c.wav'), dummy_config),
        AnalysisEvent('emotion', Path('d.wav'), dummy_config),
    ]
    for e in events:
        q.put(e)
    for e_ref in events:
        e = q.get()
        assert e.event_type == e_ref.event_type
        assert e.audio_path == e_ref.audio_path
        assert e.config is dummy_config
