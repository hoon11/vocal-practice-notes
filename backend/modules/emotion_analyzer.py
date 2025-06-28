# modules/emotion_analyzer.py
"""
감정 인식(SER) 모듈 - opensmile 기반, 추후 교체도 쉬움
"""
import opensmile
import pandas as pd
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def analyze_emotion(audio_path: Path, config) -> dict:
    audio_path = Path(audio_path)
    output_dir = Path(config.emotion.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    # 기본 이모션 피쳐 + SVM model 적용 (ex. emobase)
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    feats = smile.process_file(str(audio_path))
    # 예시: 간단히 energy-based 감정 분류(정밀 분류는 모델 추가)
    mean_energy = feats.iloc[0].mean()
    emotion = "neutral"
    if mean_energy > 0.1:
        emotion = "happy"
    elif mean_energy < -0.1:
        emotion = "sad"
    result = {
        "mean_energy": float(mean_energy),
        "predicted_emotion": emotion,
        "features": feats.iloc[0].to_dict(),
    }
    # Save json
    json_path = output_dir / f"{audio_path.stem}_emotion.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    logger.info(f"Emotion analysis saved: {json_path}")
    return result
