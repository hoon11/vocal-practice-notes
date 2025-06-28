# modules/pitch_extractor.py
"""
Pitch extraction and breathiness ratio analyzer (Praat+Parselmouth) with pydantic config support.
ピッチ抽出・無声音比率解析（Praat+Parselmouth）: pydantic設定対応・多言語注釈。
"""
import matplotlib
matplotlib.use("Agg")  # Headless 환경(화면 없는 서버)에서는 Agg가 표준
import matplotlib.pyplot as plt
import parselmouth
from parselmouth.praat import call
import numpy as np
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_pitch(audio_path: Path, config) -> dict:
    """
    Extract pitch and breathiness from an audio file using Praat engine.
    Praatエンジンで音声ファイルからピッチ・ブレス感を抽出。
    """
    audio_path = Path(audio_path)
    # config: AppConfig 객체 또는 dict 모두 지원
    try:
        output_dir = getattr(config.pitch, "output_dir", None)
    except AttributeError:
        output_dir = config["pitch"]["output_dir"]
    output_dir = Path(output_dir)
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    snd = parselmouth.Sound(str(audio_path))
    # (75~600Hz는 일반 성인 남녀 음성 범위, 추가 설명 가능)
    pitch_obj = call(snd, "To Pitch", 0.0, 75, 600)
    pitch_values = pitch_obj.selected_array['frequency']
    pitch_values[pitch_values == 0] = np.nan  # 무성구간을 NaN으로 대체

    mean_pitch = np.nanmean(pitch_values)  # 전체 평균, 보통 성별/감정 변별에 활용
    min_pitch = np.nanmin(pitch_values)
    max_pitch = np.nanmax(pitch_values)
    unvoiced_ratio = np.sum(np.isnan(pitch_values)) / len(pitch_values)  # 숨, breathiness, 발음불분명, 피로감 해석에 중요

    result = {
        "mean_pitch": round(float(mean_pitch), 2),
        "min_pitch": round(float(min_pitch), 2),
        "max_pitch": round(float(max_pitch), 2),
        "unvoiced_ratio": round(float(unvoiced_ratio), 3),  # 무성비(숨/쉼표/기침 등)
        "unit": "Hz"
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{audio_path.stem}_pitch.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    logger.info(f"Pitch analysis saved to {json_path}")

    # Visualization
    times = pitch_obj.xs()
    plt.figure(figsize=(10, 4))
    plt.plot(times, pitch_values, label="Pitch contour")
    plt.xlabel("Time (s)")
    plt.ylabel("Pitch (Hz)")
    plt.title("Pitch Contour")
    plt.grid(True)
    plt.savefig(output_dir / f"{audio_path.stem}_pitch.png")
    plt.close()

    return result
