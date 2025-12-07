# 🚀 배포 및 실행 가이드

## 📋 전체 아키텍처

```
┌─────────────────┐         ┌─────────────────┐
│  React Frontend │  ────►  │  FastAPI Server │
│  (포트 3000)    │  HTTP   │  (포트 8501)    │
└─────────────────┘         └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │  External APIs  │
                            │  - OpenAI       │
                            │  - Perplexity   │
                            │  - YouTube      │
                            └─────────────────┘
```

## 🔧 사전 준비

### 1. Python 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Node.js 의존성 설치

```bash
npm install
```

### 3. API 키 설정

`.env` 파일 생성:

```env
OPENAI_API_KEY=sk-your-key-here
PERPLEXITY_API_KEY=pplx-your-key-here
YOUTUBE_API_KEY=AIza-your-key-here
```

## 🎯 실행 방법

### 방법 1: 두 개의 터미널 사용 (권장)

**터미널 1: API 서버**
```bash
python start_api_server.py
```

**터미널 2: React 프론트엔드**
```bash
npm run dev
```

### 방법 2: 배치 스크립트 사용 (Windows)

`start_all.bat` 파일 생성:

```batch
@echo off
start "API Server" cmd /k "python start_api_server.py"
timeout /t 3
start "React Frontend" cmd /k "npm run dev"
```

## ✅ 확인 사항

### API 서버 확인
- http://localhost:8501/api/health 접속
- 응답: `{"status": "healthy", "message": "API is running"}`

### API 키 상태 확인
- http://localhost:8501/api/keys/status 접속
- 또는 `python check_api_keys.py` 실행

### 프론트엔드 확인
- http://localhost:3000 접속
- 홈 페이지에서 API 키 상태 확인

## 🔄 API 키 활용 흐름

### 1. 프론트엔드 → 백엔드 API 호출
```
React 컴포넌트
  ↓
src/frontend/utils/api.ts
  ↓
HTTP Request → http://localhost:8501/api/...
```

### 2. 백엔드에서 API 키 사용
```
FastAPI 엔드포인트
  ↓
src/ai_assistant.py (OpenAI API 키 사용)
src/perplexity_assistant.py (Perplexity API 키 사용)
src/youtube_helper.py (YouTube API 키 사용)
  ↓
외부 API 호출
```

### 3. 응답 반환
```
외부 API 응답
  ↓
FastAPI 엔드포인트
  ↓
JSON Response
  ↓
React 컴포넌트
```

## 📝 주요 변경 사항

### 1. API 서버 추가
- `src/api_server.py`: FastAPI REST API 서버
- `start_api_server.py`: 서버 시작 스크립트

### 2. 프론트엔드 API 클라이언트 개선
- 실제 API 호출 구현
- 에러 처리 개선
- 로딩 상태 표시

### 3. Streamlit 의존성 제거
- API 서버는 Streamlit 없이 독립 실행 가능
- Streamlit은 기존 Streamlit 앱에서만 사용

## 🐛 문제 해결

### API 서버가 시작되지 않을 때

1. **포트 확인**
   ```bash
   netstat -ano | findstr :8501
   ```

2. **의존성 확인**
   ```bash
   pip list | findstr fastapi
   pip list | findstr uvicorn
   ```

3. **직접 실행하여 오류 확인**
   ```bash
   python start_api_server.py
   ```

### 프론트엔드에서 CORS 오류

1. `src/api_server.py`의 CORS 설정 확인
2. 프론트엔드 URL이 허용 목록에 있는지 확인

### API 키가 작동하지 않을 때

1. `.env` 파일 확인
2. `python check_api_keys.py` 실행
3. API 서버 재시작

## 📚 추가 문서

- `README_API.md`: API 엔드포인트 상세 설명
- `API_SETUP.md`: API 서버 설정 가이드
- `check_api_keys.py`: API 키 검증 스크립트

