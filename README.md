# ボーカルフィードバックシステム - ステップ1設計概要

## 📌 プロジェクト目標
- 特定のフォルダに新しい `.wav` ファイルが追加されたら自動で検知する  
- Whisper モデルを使って音声をテキストに変換する  
- 結果を `.json` ファイルとして保存し、後の分析に利用する  
- GitHub へのアップロードや機能拡張を想定した構成にする  

## 📁 フォルダ構成
```
voice-feedback-system/
├── main.py                  # 検知・実行スクリプト  
├── audio/                   # 音声ファイル保存フォルダ  
├── transcripts/             # 文字起こし結果保存フォルダ  
├── utils/
│   └── whisper_runner.py    # Whisper 実行ロジック  
├── requirements.txt         # 依存関係リスト  
└── README.md                # プロジェクト概要
```

## ⚙️ 環境セットアップ
1. Python 3.10+ が必要  
2. 仮想環境を作成  
   ```bash
   python -m venv venv  
   source venv/bin/activate  # Windows は venv\Scripts\activate
   ```
3. 必要パッケージのインストール  
   ```bash
   pip install git+https://github.com/openai/whisper.git  
   pip install watchdog  
   pip install openai  
   ```
4. `requirements.txt` の内容
   ```
   git+https://github.com/openai/whisper.git  
   watchdog  
   openai  
   ```

## 🧠 Whisper の処理フロー
- `whisper_runner.py` で Whisper モデル（base）を読み込み  
- `transcribe_audio(path)` を呼び出して音声を文字起こし  
- 結果は `transcripts/` フォルダに `.json` ファイルとして保存される

## 🔍 ファイル検知ロジック
- `audio/` フォルダをリアルタイムで監視  
- `.wav` ファイルが追加されると自動的に Whisper を実行  
- 結果は `transcripts/` に保存される

## 📝 Git 初期化
```bash
git init  
git add .  
git commit -m "init: wav detection + Whisper transcription"  
git remote add origin https://github.com/yourusername/voice-feedback-system.git  
git push -u origin main
```

## ✅ 動作テスト
- `audio/` に `.wav` ファイルを追加  
- `$ python main.py` を実行  
- `.json` 結果ファイルが `transcripts/` に自動生成される

## 🔧 使用言語
- Python 3.10+  
- 音声処理、自動化、GPT 連携に最適

## 📌 今後の拡張予定
- GPT フィードバックとの統合  
- フォルマント分析（Praat）  
- 感情曲線の可視化  
- Streamlit によるダッシュボード構築

---

# Voice Feedback System - Step 1 Design Summary

## 📌 Project Goal
- Automatically detect when a new `.wav` file is added to a specific folder  
- Convert the audio to text using the Whisper model  
- Save the result as a `.json` file for further analysis  
- Design the structure with GitHub deployment and future feature expansion in mind  

## 📁 Folder Structure
```
voice-feedback-system/
├── main.py                  # File watcher and runner  
├── audio/                   # Folder to store input .wav files  
├── transcripts/             # Folder to store Whisper results  
├── utils/
│   └── whisper_runner.py    # Whisper execution logic  
├── requirements.txt         # Dependency list  
└── README.md                # Project overview
```

## ⚙️ Environment Setup
1. Requires Python 3.10+  
2. Create a virtual environment  
   ```bash
   python -m venv venv  
   source venv/bin/activate  # on Windows: venv\Scripts\activate  
   ```
3. Install required packages  
   ```bash
   pip install git+https://github.com/openai/whisper.git  
   pip install watchdog  
   pip install openai  
   ```
4. Contents of `requirements.txt`
   ```
   git+https://github.com/openai/whisper.git  
   watchdog  
   openai  
   ```

## 🧠 Whisper Processing Flow
- Load the Whisper model (e.g., base) in `whisper_runner.py`  
- Call `transcribe_audio(path)` to transcribe the audio  
- Save the result as `.json` in the `transcripts/` folder

## 🔍 File Watcher Logic
- Monitor the `audio/` folder in real-time  
- Automatically run Whisper when a new `.wav` file is added  
- Save the result in `transcripts/`

## 📝 Git Setup
```bash
git init  
git add .  
git commit -m "init: wav detection + Whisper transcription"  
git remote add origin https://github.com/yourusername/voice-feedback-system.git  
git push -u origin main
```

## ✅ Usage Test
- Add a `.wav` file to the `audio/` folder  
- Run `$ python main.py`  
- A `.json` result file will be created in `transcripts/`

## 🔧 Programming Language
- Python 3.10+  
- Best suited for audio processing, automation, and GPT integration

## 📌 Next Features
- GPT feedback integration  
- Formant analysis (Praat)  
- Emotion curve visualization  
- Streamlit-based dashboard

---

# 보컬 피드백 시스템 - 1단계 설계 요약

## 📌 프로젝트 목표
- 특정 폴더에 새로운 `.wav` 파일이 생기면 자동 감지  
- Whisper 모델을 통해 오디오를 텍스트로 변환  
- 결과를 `.json` 파일로 저장해 이후 분석에 활용  
- GitHub 업로드 및 기능 확장을 고려한 구조 설계

## 📁 폴더 구조
```
voice-feedback-system/
├── main.py                  # 파일 감지 및 실행 스크립트  
├── audio/                   # 입력 음성 파일 저장 폴더  
├── transcripts/             # Whisper 결과 저장 폴더  
├── utils/
│   └── whisper_runner.py    # Whisper 실행 로직  
├── requirements.txt         # 의존성 목록  
└── README.md                # 프로젝트 설명
```

## ⚙️ 환경 설정
1. Python 3.10+ 필요  
2. 가상환경 생성  
   ```bash
   python -m venv venv  
   source venv/bin/activate  # Windows는 venv\Scripts\activate  
   ```
3. 필수 패키지 설치  
   ```bash
   pip install git+https://github.com/openai/whisper.git  
   pip install watchdog  
   pip install openai  
   ```
4. requirements.txt 내용
   ```
   git+https://github.com/openai/whisper.git  
   watchdog  
   openai  
   ```

## 🧠 Whisper 처리 흐름
- whisper_runner.py에서 Whisper 모델(base)을 로딩  
- `transcribe_audio(path)` 호출로 텍스트 변환  
- 결과는 `transcripts/` 폴더에 `.json`으로 저장됨

## 🔍 파일 감지 로직
- `audio/` 폴더를 실시간 감시  
- `.wav` 파일이 추가되면 Whisper 자동 실행  
- 결과는 `transcripts/`에 저장됨

## 📝 Git 초기화
```bash
git init  
git add .  
git commit -m "init: wav detection + Whisper transcription"  
git remote add origin https://github.com/yourusername/voice-feedback-system.git  
git push -u origin main
```

## ✅ 작동 테스트
- `audio/` 폴더에 `.wav` 파일 추가  
- `$ python main.py` 실행  
- `transcripts/`에 `.json` 결과 파일이 자동 생성됨

## 🔧 사용 언어
- Python 3.10+  
- 오디오 분석, 자동화, GPT 연동에 최적화된 언어

## 📌 향후 확장 예정
- GPT 피드백 연동  
- 포먼트 분석 (Praat)  
- 감정 곡선 시각화  
- Streamlit 기반 대시보드 구성
