# modules/pitch_extractor.py
import parselmouth  # Praat interface
from parselmouth.praat import call
import numpy as np
import json
import logging
from pathlib import Path
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def extract_pitch(audio_path: Path, config: dict) -> dict:
    """
    Extract pitch and breathiness (voiced ratio) from an audio file.
    音声ファイルからピッチと無声音比率（ブレス感）を抽出する。
    """
    if not audio_path.exists():
        logger.error(f"Audio file not found: {audio_path}")
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    snd = parselmouth.Sound(str(audio_path))
    pitch_obj = call(snd, "To Pitch", 0.0, 75, 600)  # time step auto, range 75-600Hz
    pitch_values = pitch_obj.selected_array['frequency']
    pitch_values[pitch_values == 0] = np.nan  # Replace unvoiced with NaN

    mean_pitch = np.nanmean(pitch_values)
    min_pitch = np.nanmin(pitch_values)
    max_pitch = np.nanmax(pitch_values)
    unvoiced_ratio = np.sum(np.isnan(pitch_values)) / len(pitch_values)

    result = {
        "mean_pitch": round(float(mean_pitch), 2),
        "min_pitch": round(float(min_pitch), 2),
        "max_pitch": round(float(max_pitch), 2),
        "unvoiced_ratio": round(float(unvoiced_ratio), 3),
        "unit": "Hz"
    }

    output_dir = Path(config["pitch"]["output_dir"])
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
