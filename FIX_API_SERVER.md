# API 서버 오류 수정 가이드

## 발견된 문제

1. **필수 패키지 미설치**: music21, soundfile 등이 설치되지 않음
2. **Python 환경 문제**: setuptools 빌드 메타 오류
3. **포트 설정 불일치**: vite.config.ts가 3000으로 설정되어 있었음 (5173으로 수정됨)

## 수정된 내용

### 1. vite.config.ts
- 포트를 5173으로 변경
- API 프록시 설정 추가 (`/api` -> `http://localhost:8501`)

### 2. src/api_server.py
- CORS 설정 개선
- HTTP 메서드 명시적 지정

### 3. start_api_server.py
- Windows 콘솔 인코딩 문제 수정 (이모지 제거)

## 다음 단계

### 1. 필수 패키지 설치

```powershell
# 가상환경 사용 (권장)
python -m venv venv
.\venv\Scripts\Activate.ps1

# pip 업그레이드
python -m pip install --upgrade pip setuptools wheel

# 필수 패키지 설치
pip install fastapi uvicorn[standard] python-multipart python-dotenv
pip install openai requests
pip install music21 basic-pitch mido pretty-midi
pip install soundfile librosa numpy scipy
```

### 2. API 서버 실행

```powershell
python start_api_server.py
```

서버가 정상적으로 시작되면:
- `http://localhost:8501`에서 API 서버 실행
- `http://localhost:8501/docs`에서 API 문서 확인 가능

### 3. 프론트엔드 실행

```powershell
npm run dev
```

프론트엔드가 정상적으로 시작되면:
- `http://localhost:5173`에서 웹앱 실행
- API 호출은 자동으로 `http://localhost:8501/api`로 프록시됨

## 확인 방법

### API 서버 확인
```powershell
Invoke-WebRequest -Uri http://localhost:8501/api/health
```

정상 응답:
```json
{"status": "healthy", "message": "API is running"}
```

### 프론트엔드에서 API 호출 확인
브라우저 개발자 도구 (F12) -> Network 탭에서:
- API 요청이 `http://localhost:8501/api`로 전송되는지 확인
- CORS 오류가 없는지 확인

## 문제 해결

### 패키지 설치 오류
- Python 버전 확인 (3.10 또는 3.11 권장)
- 가상환경 사용
- `pip install --upgrade pip setuptools wheel` 실행

### API 서버 연결 실패
- 포트 8501이 사용 중인지 확인
- 방화벽 설정 확인
- 다른 프로세스가 포트를 사용 중인지 확인

### CORS 오류
- 브라우저 콘솔에서 오류 메시지 확인
- API 서버의 CORS 설정 확인
- 프론트엔드 URL이 CORS 허용 목록에 있는지 확인

