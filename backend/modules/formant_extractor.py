# modules/formant_extractor.py
"""
Formant(F1~F3) 추출 및 저장, 시각화 지원 모듈
"""
import parselmouth
from parselmouth.praat import call
import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def extract_formants(audio_path: Path, config) -> dict:
    audio_path = Path(audio_path)
    output_dir = Path(config.formant.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    snd = parselmouth.Sound(str(audio_path))
    formant = call(snd, "To Formant (burg)", 0.02, 5, 5500, 0.025, 50)
    duration = snd.get_total_duration()
    times = np.linspace(0, duration, formant.get_number_of_frames())
    f1 = [formant.get_value_at_time(1, t) for t in times]
    f2 = [formant.get_value_at_time(2, t) for t in times]
    f3 = [formant.get_value_at_time(3, t) for t in times]

    result = {
        "F1": {"mean": float(np.nanmean(f1)), "std": float(np.nanstd(f1))},
        "F2": {"mean": float(np.nanmean(f2)), "std": float(np.nanstd(f2))},
        "F3": {"mean": float(np.nanmean(f3)), "std": float(np.nanstd(f3))},
        "frames": [{"time": float(t), "F1": float(f1i) if f1i else None, "F2": float(f2i) if f2i else None, "F3": float(f3i) if f3i else None} for t, f1i, f2i, f3i in zip(times, f1, f2, f3)],
    }
    # Save json
    json_path = output_dir / f"{audio_path.stem}_formant.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    # Visualization
    plt.figure(figsize=(10, 4))
    plt.plot(times, f1, label="F1")
    plt.plot(times, f2, label="F2")
    plt.plot(times, f3, label="F3")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Formant Tracks (F1~F3)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / f"{audio_path.stem}_formant.png")
    plt.close()
    logger.info(f"Formant analysis saved: {json_path}")
    return result
