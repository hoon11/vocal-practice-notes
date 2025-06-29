[Codecov Coverage](https://codecov.io/gh/hoon11/vocal-practice-notes/branch/develop/graph/badge.svg)

# Whisper Worker - Backend Module (vocal-practice-notes)

## 📁 디렉토리 구조

```
backend/
├── whisper_worker/
│   ├── __init__.py
│   ├── watcher.py
│   └── transcriber.py
├── audio/
├── transcripts/
├── main.py
├── requirements.txt
└── README.md
```

## 🧩 기능 요약

- `audio/` 폴더에 새로운 `.wav` 파일이 생기면 자동 감지
- Whisper로 텍스트 변환
- 겠과를 `transcripts/`에 `.json`으로 저잕
- 추후 GPT 피드백, 슬픔 감정선 분석 등 확장 가능

## ✅ 향후 계획

- FastAPI 연동으로 백엔드 서버화
- Streamlit으로 대시보드 구성
- GPT API 연결로 피드백 자동화
