# API 서버 설정 가이드

## 🚀 API 서버 실행

### 방법 1: Python 스크립트로 실행 (권장)

```bash
python start_api_server.py
```

### 방법 2: uvicorn 직접 실행

```bash
uvicorn src.api_server:app --host 0.0.0.0 --port 8501 --reload
```

## 📋 API 엔드포인트

### 기본 정보
- **Base URL**: `http://localhost:8501`
- **API 문서**: `http://localhost:8501/docs` (Swagger UI)
- **대화형 문서**: `http://localhost:8501/redoc`

### 주요 엔드포인트

#### 1. 오디오 처리
```
POST /api/audio/process
Content-Type: multipart/form-data
Body: file (MP3, WAV)
```

#### 2. 악보 처리
```
POST /api/score/process
Content-Type: multipart/form-data
Body: 
  - file (MIDI, MusicXML, ABC)
  - options (JSON string)
```

#### 3. AI 채팅
```
POST /api/ai/chat
Content-Type: application/json
Body: {
  "question": "질문 내용",
  "context": "선택적 컨텍스트"
}
```

#### 4. 음악 이론 설명
```
POST /api/ai/explain-theory
Content-Type: application/json
Body: {
  "topic": "계이름",
  "age": 10
}
```

#### 5. 수업 계획 생성
```
POST /api/ai/lesson-plan
Content-Type: application/json
Body: {
  "songTitle": "학교종",
  "grade": "3-4학년",
  "duration": 40
}
```

#### 6. Perplexity 검색
```
POST /api/perplexity/search
Content-Type: application/json
Body: {
  "query": "검색어",
  "searchType": "음악 이론 조사"
}
```

#### 7. YouTube 검색
```
POST /api/youtube/search
Content-Type: application/json
Body: {
  "query": "검색어",
  "maxResults": 5
}
```

#### 8. 화음 분석
```
POST /api/chord/analyze
Content-Type: multipart/form-data
Body:
  - file (MIDI)
  - fileType: "midi"
```

## 🔧 환경 변수 설정

`.env` 파일에 다음을 설정하세요:

```env
OPENAI_API_KEY=sk-your-key-here
PERPLEXITY_API_KEY=pplx-your-key-here
YOUTUBE_API_KEY=AIza-your-key-here
```

## 🔄 프론트엔드와 연동

React 프론트엔드의 `src/frontend/utils/api.ts`에서 API Base URL을 설정하세요:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8501/api'
```

## 📝 실행 순서

1. **API 서버 시작**
   ```bash
   python start_api_server.py
   ```

2. **React 프론트엔드 시작** (새 터미널)
   ```bash
   npm run dev
   ```

3. **브라우저에서 확인**
   - 프론트엔드: http://localhost:3000
   - API 문서: http://localhost:8501/docs

## ⚠️ 주의사항

1. API 서버는 포트 8501에서 실행됩니다
2. React 프론트엔드는 포트 3000에서 실행됩니다
3. CORS는 localhost:3000과 localhost:5173에서만 허용됩니다
4. 프로덕션 배포 시 CORS 설정을 수정해야 합니다

