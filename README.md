# 초등 음악 도우미 웹앱 🎵

초등학생과 교사를 위한 AI 기반 음악 학습 지원 웹 애플리케이션

## 📋 프로젝트 개요

음악 수업에서 교사가 제시한 곡을 학생 수준에 맞게 자동으로 변환하는 웹 애플리케이션입니다.
- **오선 악보 자동 생성**
- **계이름 자동 기재** (도, 레, 미...)
- **다장조로 단순화**
- **기본 화음 반주 추가**
- **자동 재생 기능**
- **🆕 AI 음악 선생님** (ChatGPT 기반)

## 🎯 주요 기능

### 1. 오디오 → 악보 변환
- MP3, WAV 파일 업로드
- AI 기반 멜로디 추출 (basic-pitch)
- 오선 악보 자동 생성

### 2. 악보 처리
- MIDI, MusicXML, ABC 형식 지원
- 자동 계이름 기재
- 다장조(C major) 변환
- 리듬 양자화

### 3. 반주 생성
- 1마디 단위 자동 화음 분석
- I, IV, V, vi 코드 기반 반주
- 왼손 블록 코드 스타일

### 4. 재생 기능
- 브라우저 기반 재생
- 박자, 리듬 정확한 재현
- 멜로디 + 반주 동시 재생

### 5. 🆕 AI 음악 도우미 (ChatGPT 기반)
- **악보 자동 분석**: 난이도, 학습 포인트, 연습 방법 제안
- **AI 선생님 채팅**: 음악 이론 질문에 답변
- **맞춤형 설명**: 학생 나이에 맞는 쉬운 음악 이론 설명
- **수업 계획 생성**: 학년별 맞춤 수업 계획 자동 작성
- **화음 개선 제안**: 더 나은 반주 진행 추천

### 6. 🆕 Perplexity & YouTube (v3.0)
- **웹 조사**: 최신 음악 교육 연구 및 곡 배경 정보
- **교육 영상**: YouTube에서 교육 영상 자동 검색

### 7. 🆕 교사용 대시보드 (v4.0)
- **학급 관리**: 학년/반 등록 및 관리
- **학생 명단**: 학생 정보 등록 및 수정
- **수업 기록**: 날짜별 활동 및 수업 내용 기록
- **진도 관리**: 학생별 학습 진도 및 평가 기록
- **통계 리포트**: 학급별/학생별 통계 및 분석

> **참고**: AI 기능은 OpenAI API 키가 필요합니다. 없어도 기본 기능은 모두 사용 가능합니다.  
> 자세한 설정 방법은 [API 설정 가이드](docs/api_setup.md)를 참조하세요.

## 🚀 시작하기

### 필요 사항
- Python 3.8 이상
- pip 패키지 관리자

### 설치

```bash
# 저장소 클론
git clone https://github.com/yourusername/elementary-music-helper.git
cd elementary-music-helper

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# MuseScore 설치 (악보 렌더링용)
# macOS: brew install musescore
# Ubuntu: sudo apt-get install musescore3
# Windows: https://musescore.org 에서 다운로드
```

### API 키 설정 (선택사항)

**🔐 방법 1: .env 파일 (권장)**

```bash
# env.template을 .env로 복사
# Windows:
copy env.template .env
# macOS/Linux:
cp env.template .env

# 편집기로 열어 API 키 입력
# Windows: notepad .env
# macOS/Linux: nano .env
```

`.env` 파일 예시:
```env
OPENAI_API_KEY=sk-proj-your-key-here
PERPLEXITY_API_KEY=pplx-your-key-here  
YOUTUBE_API_KEY=AIza-your-key-here
```

**📚 자세한 설정**:
- [.env 파일 사용법](docs/env_setup.md) 🆕
- [API 키 발급 방법](docs/api_setup.md)

### 실행

```bash
streamlit run src/app.py
```

브라우저에서 `http://localhost:8501` 접속

## 📁 프로젝트 구조

```
elementary-music-helper/
├── src/
│   ├── app.py                 # 메인 Streamlit 앱
│   ├── audio_processor.py     # 오디오 → 악보 변환
│   ├── score_processor.py     # 악보 처리 및 단순화
│   ├── chord_generator.py     # 반주 생성
│   └── player.py             # 재생 기능
├── utils/
│   ├── music_utils.py        # 음악 이론 유틸리티
│   └── file_utils.py         # 파일 처리 유틸리티
├── assets/
│   └── styles.css            # 커스텀 스타일
├── docs/
│   └── user_guide.md         # 사용자 가이드
├── requirements.txt          # Python 패키지 목록
├── .cursorrules             # Cursor AI 설정
├── .gitignore
└── README.md
```

## 🛠️ 기술 스택

- **Frontend**: Streamlit 1.38+
- **AI/ML**:
  - ChatGPT API (OpenAI) - 음악 교육 도우미
  - basic-pitch (Spotify) - 오디오 → 멜로디 추출
- **음악 처리**: 
  - music21 (악보 파싱, 이조, 계이름)
  - soundfile (오디오 로드)
- **배포**: Streamlit Community Cloud
- **형상 관리**: GitHub

## 👥 대상 사용자

- **초등학생**: 집/학교에서 곡 따라 하기, 시청각 연습
- **초등 교사**: 수업 자료 빠른 제작
- **음악 비전공 교사**: 계이름·조성 변환 자동화
- **음악 수업 담당자**: 단순화 악보 필요 시

## 🎓 기대 효과

1. **수업 준비 시간 단축**: 반복 업무 자동화
2. **학생 자기주도 학습**: 집에서도 곡 연습 가능
3. **비전공 교사 지원**: 전문 지식 없이도 악보 제작
4. **학교 간 공유**: URL만으로 쉬운 배포
5. **AI 교육 활용**: 디지털 역량 교육 자료

## 📝 사용 방법

### 오디오 파일로 악보 만들기
1. 왼쪽 패널에서 "오디오 업로드" 선택
2. MP3/WAV 파일 업로드
3. "악보 생성" 버튼 클릭
4. 생성된 악보 확인

### 기존 악보 단순화하기
1. 오른쪽 패널에서 "악보 업로드" 선택
2. MIDI/MusicXML 파일 업로드
3. 원하는 옵션 선택 (계이름, 반주 등)
4. "처리하기" 버튼 클릭
5. 재생 버튼으로 확인

## 🤝 기여하기

기여를 환영합니다! Pull Request를 보내주세요.

## 📄 라이선스

MIT License

## 👤 개발자

- **차미혜** - 웹앱 기획 및 개발

## 📞 문의

이슈나 질문이 있으시면 GitHub Issues를 이용해주세요.

---

**Note**: PDF 악보는 웹앱에서 직접 처리하지 않습니다. Audiveris 등으로 MusicXML로 변환 후 업로드해주세요.
