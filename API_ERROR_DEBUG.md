# API 오류 디버깅 가이드

## 현재 상태 확인

### 1. API 서버 상태 확인
```bash
# 브라우저에서 확인
http://localhost:8501/api/health

# 또는 PowerShell에서
Invoke-WebRequest -Uri http://localhost:8501/api/health
```

**정상 응답:**
```json
{
  "status": "healthy",
  "message": "API is running",
  "modules": {
    "audio_processor": true,
    "score_processor": true,
    ...
  }
}
```

### 2. API 키 상태 확인
```bash
http://localhost:8501/api/keys/status
```

## 일반적인 오류 및 해결 방법

### 오류 1: "API 서버에 연결할 수 없습니다"

**원인:**
- API 서버가 실행되지 않음
- 포트 8501이 다른 프로세스에 의해 사용 중
- 방화벽 차단

**해결:**
1. API 서버 시작:
   ```bash
   python start_api_simple.py
   ```

2. 포트 확인:
   ```powershell
   Get-NetTCPConnection -LocalPort 8501
   ```

3. 프로세스 종료:
   ```powershell
   Stop-Process -Id <PID> -Force
   ```

### 오류 2: CORS 오류

**원인:**
- 프론트엔드와 백엔드의 origin이 다름
- CORS 설정 문제

**해결:**
- API 서버의 CORS 설정 확인 (이미 모든 origin 허용으로 설정됨)
- 프론트엔드가 `http://localhost:5173`에서 실행 중인지 확인

### 오류 3: "모듈을 사용할 수 없습니다"

**원인:**
- 필수 Python 패키지 미설치
- 모듈 import 실패

**해결:**
```bash
pip install -r requirements.txt
```

### 오류 4: "악보 생성에 실패했습니다"

**원인:**
- 파일 형식 문제
- 처리 중 오류 발생

**해결:**
- 파일 형식 확인 (MIDI, MP3, WAV 지원)
- API 서버 로그 확인
- 브라우저 개발자 도구 Network 탭에서 오류 확인

## 디버깅 방법

### 1. 브라우저 개발자 도구
1. F12 키 누르기
2. Network 탭 열기
3. API 요청 확인
4. 오류 응답 확인

### 2. API 서버 로그 확인
API 서버를 실행한 터미널 창에서 오류 메시지 확인

### 3. API 문서 확인
```
http://localhost:8501/docs
```
Swagger UI에서 API 테스트 가능

## 오류 로그 수집

오류 발생 시 다음 정보를 수집하세요:

1. **브라우저 콘솔 오류** (F12 → Console)
2. **Network 탭의 요청/응답** (F12 → Network)
3. **API 서버 로그** (터미널 출력)
4. **오류 메시지 전체 내용**

## 빠른 해결 체크리스트

- [ ] API 서버 실행 중인가? (`python start_api_simple.py`)
- [ ] 포트 8501이 사용 가능한가?
- [ ] 프론트엔드가 `http://localhost:5173`에서 실행 중인가?
- [ ] 필수 패키지가 설치되어 있는가? (`pip list`)
- [ ] `.env` 파일이 있는가?
- [ ] 브라우저 콘솔에 오류가 있는가?

## 추가 도움

문제가 계속되면:
1. API 서버 재시작
2. 브라우저 캐시 삭제
3. 프론트엔드 재빌드: `npm run build`

