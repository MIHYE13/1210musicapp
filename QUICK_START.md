# 빠른 시작 가이드

## API 서버 연결 오류 해결

### 문제: "API 서버에 연결할 수 없습니다"

이 오류는 API 서버가 실행되지 않아서 발생합니다.

## 해결 방법

### 방법 1: 자동 시작 스크립트 사용 (권장)

#### Windows PowerShell
```powershell
.\start_all.ps1
```

#### Windows CMD
```cmd
start_all.bat
```

이 스크립트는 API 서버와 프론트엔드를 자동으로 시작합니다.

### 방법 2: 수동 시작

#### 1단계: API 서버 시작
새 터미널 창을 열고:
```bash
python start_api_simple.py
```

서버가 시작되면:
- API 서버: http://localhost:8501
- API 문서: http://localhost:8501/docs

#### 2단계: 프론트엔드 시작
또 다른 새 터미널 창을 열고:
```bash
npm run dev
```

프론트엔드가 시작되면:
- 웹앱: http://localhost:5173

## 확인 방법

### API 서버 확인
브라우저에서 다음 주소를 열어보세요:
- http://localhost:8501/api/health

정상 응답:
```json
{"status":"healthy","message":"API is running"}
```

### 프론트엔드 확인
브라우저에서 다음 주소를 열어보세요:
- http://localhost:5173

## 문제 해결

### 포트가 이미 사용 중인 경우
```powershell
# 포트 8501 사용 중인 프로세스 확인
Get-NetTCPConnection -LocalPort 8501

# 프로세스 종료 (PID 확인 후)
Stop-Process -Id <PID> -Force
```

### Python 모듈 오류
```bash
pip install -r requirements.txt
```

### Node 모듈 오류
```bash
npm install
```

## 정상 작동 확인

1. ✅ API 서버: http://localhost:8501/api/health → 정상 응답
2. ✅ 프론트엔드: http://localhost:5173 → 웹앱 표시
3. ✅ API 연결: 웹앱에서 기능 사용 시 오류 없음

## 다음 단계

서버가 정상적으로 시작되면:
1. 웹앱에서 MIDI/MP3 파일 업로드
2. 악보 생성 및 처리
3. 화음 분석 및 피아노 시각화

