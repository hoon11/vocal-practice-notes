
# Vocal Practice Notes  
ボーカル練習用個人Practiceツール

## 🇯🇵 日本語

**プロジェクト説明**  
ボーカル練習のための個人用練習ツールです。  
自分の歌声を録音し、ピッチ分析を視覚化し、曲ごとに練習メモを記録できます。

**機能**  
- 🎙️ 歌声の録音と再生
- 🎼 ピッチ分析とグラフ表示
- 📝 曲ごとの練習メモ作成
- 🎻 楽譜との比較機能（今後追加予定）
- 🎹 練習履歴の管理

**目的**  
- ボーカル練習の個人記録を保持する  
- 視覚的フィードバックによりピッチの精度を向上させる  
- 繰り返し練習の効果を高める

## 🇬🇧 English

**Project Description**  
This is a personal practice tool for vocal training.  
You can record your singing, visualize pitch analysis, and write practice notes for each song.

**Features**  
- 🎙️ Record and playback singing
- 🎼 Pitch analysis and visualization
- 📝 Write practice notes per song
- 🎻 Score comparison feature (planned)
- 🎹 Practice history management

**Purpose**  
- Keep a personal record of vocal practice  
- Improve pitch accuracy with visual feedback  
- Enhance the effectiveness of repeated practice

## 🇰🇷 한국어

**프로젝트 설명**  
노래 연습용으로 나만의 연습 기록 및 피드백 툴입니다.  
Pitch 분석을 통해 정확한 음정을 확인하고, 곡별 연습 메모를 기록할 수 있습니다.

**기능**  
- 🎙️ 노래 녹음 및 재생
- 🎼 Pitch 분석 및 그래프 표시
- 📝 곡별 연습 메모 작성
- 🎻 악보 비교 기능 (향후 추가 예정)
- 🎹 연습 이력 관리

**사용 목적**  
- 개인 노래 연습 기록  
- 시각적 피드백으로 음정 교정  
- 반복 연습의 효과 향상

## 📋 技術スタック / Tech Stack / 기술 스택

- Frontend: React + Vite + TypeScript
- Audio: Web Audio API + MediaRecorder API
- Pitch Analysis: pitchfinder.js / meyda (for advanced features)
- Chart: Chart.js + react-chartjs-2
- Backend: Node.js + Express
- DB: SQLite
- Test: Jest + React Testing Library + Cypress (for E2E)

## 📋 進捗状況 / Progress / 진행 상황

- [x] プロジェクト初期構成 / Initial project setup / 프로젝트 초기 구조 세팅
- [x] 録音機能実装 / Recording feature implemented / 녹음 기능 구현
- [ ] ピッチ分析実装中 / Pitch analysis in progress / Pitch 분석 기능 구현 중
- [ ] ピッチグラフ表示 / Pitch graph visualization / Pitch 그래프 표시
- [ ] 曲ごとのメモ機能 / Song-specific notes / 곡별 메모 기능
- [ ] 楽譜比較機能 / Score comparison / 악보 비교 기능
