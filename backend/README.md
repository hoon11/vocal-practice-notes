# ボーカルフィードバックシステム - ステップ1設計概要
# Voice Feedback System - Step 1 Design Summary
# 보컬 피드백 시스템 - 1단계 설계 요약

---

## 🎯 プロジェクト目標 | Project Goal | 프로젝트 목표

Whisperを用いて録音された音声ファイルからテキストを自動生成し、後続のボーカルフィードバック分析に活用するベース構築。
→ ディレクトリを監視し、自動で文字起こし。

Automatically transcribe recorded `.wav` files using OpenAI's Whisper model and prepare data for detailed vocal feedback analysis.  
→ Monitors folder and auto-transcribes audio input.

녹음된 `.wav` 파일을 Whisper로 자동 텍스트 변환하여, 피드백 분석을 위한 기초 데이터를 구축함.  
→ 지정 폴더 감시 및 자동 변환 처리

---

## 📁 ディレクトリ構成 | Project Structure | 프로젝트 구조

```
vocal-practice-notes/
├─ frontend/
└─ backend/
   ├─ config.yaml                  # 全体設定ファイル / Global configuration
   ├─ config_loader.py             # 設정 로더
   ├─ watcher.py                   # .wav 감지 및 트리거
   └─ whisper_worker/
      └─ transcriber.py           # Whisper 모델로 음성 → 텍스트 변환
```

---

## ⚙️ 環境設定ファイル | Configuration (config.yaml)

```yaml
watcher:
  input_dir: "audio"                # 📁 監視対象フォルダ / Input folder to watch
  output_dir: "transcripts"         # 📁 出力先フォルダ / Output transcript folder
  file_extensions: [".wav"]         # 📂 対象拡張子 / Target audio extensions
  recursive: false                  # 🔄 サブフォルダを含むか / Include subfolders

whisper:
  enabled: true                     # ✅ 文字起こしを有効化 / Enable transcription
  model_size: "small"               # 🤖 使用モデル選択 / Select Whisper model

  # モデル選択肢 / Model options:
  # - tiny:   Fastest, lowest accuracy (~39MB)
  # - base:   Fast, slightly better (~74MB)
  # - small:  Balanced (~244MB)
  # - medium: Slower, better (~769MB)
  # - large:  Slowest, best accuracy (~1550MB)
```

---

## 🧪 使用技術 | Tech Stack | 기술 스택

- Python 3.10+
- [OpenAI Whisper](https://github.com/openai/whisper)
- watchdog
- PyYAML
- ffmpeg (Whisper 用必須)

---

## 🚀 実行方法 | How to Run | 실행 방법

```bash
cd backend
pip install -r requirements.txt

# config.yaml 설정 확인 후 실행
python watcher.py
```

---

## 🔜 次のステップ | Next Step | 다음 단계

- 감정 분석, 포먼트 추출 및 시각화 도입
- 실시간 감지 → 결과 DB 저장 및 API 연동
