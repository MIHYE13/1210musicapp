# API 서버 설정 및 실행 가이드

## 🎯 개요

이 프로젝트는 **React 프론트엔드**와 **FastAPI 백엔드**로 구성되어 있습니다.

- **프론트엔드**: React + Vite (포트 3000)
- **백엔드**: FastAPI (포트 8501)
- **API 키**: 백엔드에서만 사용 (프론트엔드에서 직접 접근 불가)

## 🚀 실행 방법

### 1. API 서버 시작 (필수)

```bash
python start_api_server.py
```

또는

```bash
uvicorn src.api_server:app --host 0.0.0.0 --port 8501 --reload
```

서버가 시작되면:
- API 서버: http://localhost:8501
- API 문서: http://localhost:8501/docs
- 대화형 문서: http://localhost:8501/redoc

### 2. React 프론트엔드 시작 (새 터미널)

```bash
npm run dev
```

프론트엔드: http://localhost:3000

## 🔑 API 키 설정

`.env` 파일에 다음을 설정하세요:

```env
OPENAI_API_KEY=sk-your-key-here
PERPLEXITY_API_KEY=pplx-your-key-here
YOUTUBE_API_KEY=AIza-your-key-here
```

## 📋 API 엔드포인트

### 헬스 체크
```
GET /api/health
```

### API 키 상태
```
GET /api/keys/status
```

### 오디오 처리
```
POST /api/audio/process
Content-Type: multipart/form-data
Body: file (MP3, WAV)
```

### 악보 처리
```
POST /api/score/process
Content-Type: multipart/form-data
Body:
  - file (MIDI, MusicXML, ABC)
  - options (JSON string)
```

### AI 채팅
```
POST /api/ai/chat
Content-Type: application/json
Body: {
  "question": "질문",
  "context": "선택적 컨텍스트"
}
```

### 음악 이론 설명
```
POST /api/ai/explain-theory
Content-Type: application/json
Body: {
  "topic": "계이름",
  "age": 10
}
```

### 수업 계획 생성
```
POST /api/ai/lesson-plan
Content-Type: application/json
Body: {
  "songTitle": "학교종",
  "grade": "3-4학년",
  "duration": 40
}
```

### Perplexity 검색
```
POST /api/perplexity/search
Content-Type: application/json
Body: {
  "query": "검색어",
  "searchType": "음악 이론 조사"
}
```

### YouTube 검색
```
POST /api/youtube/search
Content-Type: application/json
Body: {
  "query": "검색어",
  "maxResults": 5
}
```

### 화음 분석
```
POST /api/chord/analyze
Content-Type: multipart/form-data
Body:
  - file (MIDI)
  - fileType: "midi"
```

## 🧪 API 테스트

```bash
python test_api.py
```

## ⚠️ 문제 해결

### API 서버가 시작되지 않을 때

1. **포트 충돌 확인**
   ```bash
   netstat -ano | findstr :8501
   ```

2. **의존성 설치 확인**
   ```bash
   pip install -r requirements.txt
   ```

3. **오류 로그 확인**
   - 터미널에서 직접 실행하여 오류 메시지 확인

### 프론트엔드에서 API 호출 실패

1. **API 서버가 실행 중인지 확인**
   - http://localhost:8501/api/health 접속

2. **CORS 오류 확인**
   - 브라우저 개발자 도구 콘솔 확인
   - `netlify.toml`의 CORS 설정 확인

3. **환경 변수 확인**
   - `.env` 파일에 API 키가 설정되어 있는지 확인
   - `python check_api_keys.py` 실행

## 📝 개발 워크플로우

1. **API 서버 시작** (터미널 1)
   ```bash
   python start_api_server.py
   ```

2. **프론트엔드 시작** (터미널 2)
   ```bash
   npm run dev
   ```

3. **브라우저에서 확인**
   - 프론트엔드: http://localhost:3000
   - API 문서: http://localhost:8501/docs

## 🔒 보안 주의사항

1. **API 키는 절대 프론트엔드에 노출하지 마세요**
   - 모든 API 키는 백엔드에서만 사용
   - 프론트엔드는 백엔드 API를 통해 간접적으로 사용

2. **프로덕션 배포 시**
   - CORS 설정을 실제 도메인으로 제한
   - HTTPS 사용
   - API 키는 환경 변수로 관리

