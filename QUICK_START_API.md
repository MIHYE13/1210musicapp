# 🚀 빠른 시작 가이드 - API 재설계 완료

## ✅ 완료된 작업

### 1. FastAPI REST API 서버 구축
- `src/api_server.py`: 모든 기능을 REST API로 제공
- `start_api_server.py`: 서버 시작 스크립트
- CORS 설정 완료 (React 프론트엔드 접근 가능)

### 2. 프론트엔드 API 연동
- 실제 API 호출 구현
- 에러 처리 개선
- 로딩 상태 표시

### 3. API 키 활용 구조
- **백엔드에서만 API 키 사용** (보안)
- 프론트엔드는 백엔드 API를 통해 간접 사용
- 환경 변수에서 자동 로드

## 🎯 실행 방법

### 1단계: API 서버 시작

```bash
python start_api_server.py
```

**확인**: http://localhost:8501/api/health 접속

### 2단계: React 프론트엔드 시작 (새 터미널)

```bash
npm run dev
```

**확인**: http://localhost:3000 접속

### 3단계: 기능 테스트

1. **홈 페이지**: API 키 상태 확인
2. **AI 도우미**: 질문하기 기능 테스트
3. **오디오 → 악보**: 파일 업로드 테스트

## 📋 API 엔드포인트 목록

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/health` | GET | 헬스 체크 |
| `/api/keys/status` | GET | API 키 상태 |
| `/api/audio/process` | POST | 오디오 처리 |
| `/api/score/process` | POST | 악보 처리 |
| `/api/ai/chat` | POST | AI 채팅 |
| `/api/ai/explain-theory` | POST | 음악 이론 설명 |
| `/api/ai/lesson-plan` | POST | 수업 계획 생성 |
| `/api/perplexity/search` | POST | Perplexity 검색 |
| `/api/youtube/search` | POST | YouTube 검색 |
| `/api/chord/analyze` | POST | 화음 분석 |

## 🔑 API 키 설정 확인

```bash
python check_api_keys.py
```

**예상 결과**:
```
✅ OpenAI: 정상
✅ Perplexity: 정상
✅ YouTube: 정상
```

## 🐛 문제 해결

### API 서버가 시작되지 않을 때

1. **의존성 설치**
   ```bash
   pip install fastapi uvicorn
   ```

2. **포트 확인**
   ```bash
   netstat -ano | findstr :8501
   ```

3. **직접 실행하여 오류 확인**
   ```bash
   python start_api_server.py
   ```

### 프론트엔드에서 API 호출 실패

1. **API 서버 실행 확인**
   - http://localhost:8501/api/health 접속

2. **브라우저 콘솔 확인**
   - F12 → Console 탭
   - CORS 오류 확인

3. **환경 변수 확인**
   - `.env` 파일 존재 여부
   - API 키 설정 확인

## 📝 주요 변경 사항

### Before (이전)
- 프론트엔드에서 직접 API 키 사용 시도
- 백엔드 API 없음
- 시뮬레이션 모드만 작동

### After (현재)
- ✅ FastAPI 백엔드 서버 구축
- ✅ 프론트엔드 → 백엔드 API 호출
- ✅ 백엔드에서 API 키 사용
- ✅ 실제 기능 작동

## 🎉 다음 단계

1. **API 서버 시작**: `python start_api_server.py`
2. **프론트엔드 시작**: `npm run dev`
3. **기능 테스트**: 각 페이지에서 실제 기능 사용
4. **API 문서 확인**: http://localhost:8501/docs

모든 기능이 실제 API를 통해 작동합니다! 🚀

