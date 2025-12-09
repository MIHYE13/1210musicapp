# 악보 생성 기능 설정 가이드

## 현재 상태

### ✅ 작동하는 기능
- **MIDI 파일 → 악보 변환**: music21만으로 작동합니다
- **악보 처리** (리듬 단순화, 다장조 변환, 계이름 추가): 정상 작동
- **화음 분석**: MIDI 파일 기준으로 정상 작동

### ⚠️ 추가 설정이 필요한 기능
- **오디오 파일 (MP3, WAV) → 악보 변환**: `basic-pitch` 설치 필요

## 필수 패키지 설치

### 1. 기본 패키지 (이미 설치됨)
```bash
pip install music21 soundfile numpy
```

### 2. 오디오 처리 패키지 (설치 필요)
```bash
pip install basic-pitch
```

**주의**: Python 3.14에서는 `basic-pitch` 설치가 실패할 수 있습니다. 이 경우:
- Python 3.10, 3.11, 또는 3.12 사용 권장
- 또는 가상환경에서 Python 3.12로 설정

## 앱 구현 가능 여부

### ✅ 완전히 구현 가능한 기능

1. **MIDI 파일 업로드 → 악보 생성**
   - music21만으로 작동
   - 즉시 사용 가능

2. **악보 처리 및 변환**
   - 리듬 단순화
   - 다장조로 변환
   - 계이름(도레미) 추가
   - 화음 반주 추가

3. **악보 내보내기**
   - MIDI 파일
   - MusicXML 파일
   - MP3 파일 (ffmpeg 또는 timidity 필요)

4. **화음 분석**
   - MIDI 파일 기준
   - 피아노 키보드 시각화

### ⚠️ 추가 설정이 필요한 기능

1. **오디오 파일 (MP3, WAV) → 악보**
   - `basic-pitch` 설치 필요
   - Python 버전 호환성 확인 필요

2. **PDF/이미지 → 악보 (OMR)**
   - Audiveris 또는 다른 OMR 도구 필요
   - 현재는 제한적으로 작동

## 권장 설정

### 옵션 1: Python 3.12 가상환경 사용 (권장)
```bash
# Python 3.12 설치 후
python3.12 -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 옵션 2: 현재 환경에서 MIDI만 사용
- MIDI 파일 업로드 기능은 즉시 사용 가능
- 오디오 파일 처리는 나중에 설정

## 테스트 방법

```bash
# 필수 모듈 테스트
python test_score_generation.py
```

## 문제 해결

### basic-pitch 설치 실패 시
1. Python 버전 확인: `python --version`
2. Python 3.10-3.12 사용 권장
3. 가상환경에서 재시도

### 악보 생성 실패 시
1. API 서버 로그 확인
2. 파일 형식 확인 (MIDI는 확실히 작동)
3. 오류 메시지 확인

## 결론

**앱은 구현 가능합니다!**

- MIDI 파일 처리는 즉시 작동
- 오디오 파일 처리는 `basic-pitch` 설치 후 작동
- 대부분의 핵심 기능은 현재 환경에서 사용 가능

