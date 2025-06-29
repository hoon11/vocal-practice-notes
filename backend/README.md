# Whisper Worker - Backend Module (vocal-practice-notes)

[Image | Codecov Coverage](https://codecov.io/gh/hoon11/vocal-practice-notes/branch/develop/graph/badge.svg)

## File Tree

```\nbackend/\i️\n\t|__whisper_]\n\t|\_will  '__init__.py\n\t|| watcher.py\n\t| | transcriber.py\n\t** aaudio/\n\t** transcripts/\n\t|| main.py\n\t| |requirements.txt\n```
This reflects the module designed for audio transcription tasks with OpenAI Whisper

## Key Features

- Watch for new audio files in `base/audio` directory
- Transcribe with OpenAI Whisper
- Save transcript output to `transcripts`/` as .json
- Designed with future extension targets (emo detection, feedback)

## Roadmap

- Integrate core with FastAPI
- Add service dashboard with Streamlit
- Enable automated GPT-based feedback