import os
import datetime
import whisper
from config_loader import load_config

# Load YAML configuration
# YAML設定を読み込む
config = load_config()

# Check if transcription is enabled
# 文字起こしを有効にするかを確認
if config.get("whisper", {}).get("enabled", False):
    # Get the model size from config (default to "small")
    # 設定ファイルからモデルサイズを取得（デフォルトは"small"）
    model_size = config["whisper"].get("model_size", "small")

    # Load the specified Whisper model
    # 指定されたWhisperモデルを読み込む
    model = whisper.load_model(model_size)
else:
    model = None  # Transcription disabled / 文字起こし無効化

def transcribe(audio_path, output_dir):
    """
    Transcribe the given audio file and save the result as a JSON file.
    オーディオファイルを文字起こしし、結果をJSONファイルとして保存する。
    """
    if model is None:
        raise RuntimeError("Transcription is disabled in config.yaml")

    # Perform transcription using Whisper
    # Whisperを使って文字起こしを実行
    result = model.transcribe(audio_path)

    # Extract base filename without extension
    # 拡張子を除いたファイル名を取得
    base_filename = os.path.splitext(os.path.basename(audio_path))[0]

    # Generate timestamp for output file
    # 出力ファイル用のタイムスタンプを生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create output filename
    # 出力ファイル名を作成
    output_filename = f"{base_filename}_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)

    # Make sure output directory exists
    # 出力フォルダが存在するか確認、なければ作成
    os.makedirs(output_dir, exist_ok=True)

    # Save transcription result to JSON
    # 結果をJSON形式で保存
    with open(output_path, "w", encoding="utf-8") as f:
        import json
        json.dump(result, f, ensure_ascii=False, indent=2)

    return output_path
