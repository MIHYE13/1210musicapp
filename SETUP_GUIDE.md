# API 서버 설정 가이드

## 문제 진단

현재 API 서버가 실행되지 않는 주요 원인:
1. **필수 Python 패키지 미설치**: music21, soundfile 등
2. **Python 환경 문제**: setuptools 빌드 메타 오류

## 해결 방법

### 방법 1: 가상환경 사용 (권장)

```powershell
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 패키지 설치
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 방법 2: 개별 패키지 설치

```powershell
# 필수 패키지만 설치
pip install --upgrade pip setuptools wheel
pip install fastapi uvicorn[standard] python-multipart python-dotenv
pip install openai requests
pip install music21 basic-pitch mido pretty-midi
pip install soundfile librosa numpy
```

### 방법 3: Python 버전 확인

Python 3.14는 일부 패키지와 호환성 문제가 있을 수 있습니다.
Python 3.10 또는 3.11 사용을 권장합니다.

## API 서버 실행 확인

```powershell
# 서버 시작
python start_api_server.py

# 다른 터미널에서 확인
Invoke-WebRequest -Uri http://localhost:8501/api/health
```

## 프론트엔드 설정

프론트엔드는 다음 설정으로 구성되어 있습니다:

- **포트**: 5173 (vite.config.ts에서 설정)
- **API Base URL**: http://localhost:8501/api
- **프록시**: vite.config.ts에 프록시 설정 추가됨

## 문제 해결 체크리스트

- [ ] Python 가상환경 생성 및 활성화
- [ ] requirements.txt 패키지 설치 완료
- [ ] API 서버가 http://localhost:8501에서 실행 중
- [ ] 프론트엔드가 http://localhost:5173에서 실행 중
- [ ] .env 파일에 API 키 설정 (선택사항)
- [ ] 브라우저 콘솔에서 CORS 오류 확인

