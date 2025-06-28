import whisper
from pathlib import Path
import json


# Transcribe audio using Whisper model
# Whisper モデルを使って音声を文字起こしします
def transcribe(audio_path: Path, config):
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    model_size = config["transcriber"]["model_size"]
    model = whisper.load_model(model_size)
    result = model.transcribe(str(audio_path))

    transcripts_dir = config["transcriber"].get("transcripts_dir", "transcripts")
    output_path = Path(transcripts_dir) / (audio_path.stem + ".json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Transcription saved to {output_path}")
