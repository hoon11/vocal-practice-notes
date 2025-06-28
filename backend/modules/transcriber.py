import whisper
from pathlib import Path
import json

# Transcribe audio using Whisper model
# Whisper モデルを使って音声を文字起こしします
def transcribe(audio_path: Path, config):
    model_size = config["transcriber"]["model_size"]
    model = whisper.load_model(model_size)
    result = model.transcribe(str(audio_path))

    output_path = Path("transcripts") / (audio_path.stem + ".json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Transcription saved to {output_path}")
