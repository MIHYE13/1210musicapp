# 🎵 초등 음악 도우미 (Elementary Music Helper)

초등학생과 교사를 위한 인터랙티브 음악 학습 웹 애플리케이션

## 📋 목차

- [프로젝트 소개](#프로젝트-소개)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [사용 방법](#사용-방법)
- [API 설정](#api-설정)
- [프로젝트 구조](#프로젝트-구조)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 🎯 프로젝트 소개

**초등 음악 도우미**는 초등학생들이 음악을 쉽고 재미있게 배울 수 있도록 돕는 웹 애플리케이션입니다. 피아노 건반을 클릭하여 화음을 만들고, 박자에 맞춰 리듬을 작곡하며, 유명한 클래식 음악을 감상하고 분석할 수 있습니다.

### 핵심 가치

- 🎹 **인터랙티브 학습**: 피아노 건반을 직접 클릭하며 음악을 배움
- 🎼 **자동 악보 생성**: 박자에 맞춰 입력하면 자동으로 악보가 그려짐
- 🤖 **AI 기반 학습**: AI 도우미가 음악 이론을 쉽게 설명
- 📚 **다양한 학습 자료**: 클래식 음악 감상 및 분석 기능
- 👨‍🏫 **교사 지원**: 수업 계획 생성 및 학생 관리 기능

## ✨ 주요 기능

### 1. 🎼 리듬 작곡기

박자에 맞춰 피아노 건반을 클릭하면 자동으로 화음 반주 악보가 그려지는 기능입니다.

**주요 특징:**
- 박자 선택 (4/4, 3/4, 2/4)
- 음표 길이 선택 (16분음표, 8분음표, 4분음표, 2분음표, 온음표)
- 마디 단위 자동 관리
- 화음 자동 분석 및 표시
- 오선 악보 자동 생성
- 자동 재생 기능 (재생 속도 조절 가능)

**사용 방법:**
1. 박자를 선택합니다 (예: 4/4박자)
2. 음표 길이를 선택합니다 (예: 4분음표)
3. 피아노 건반을 클릭하여 음표를 입력합니다
4. 마디가 가득 차면 자동으로 새 마디가 생성됩니다
5. 재생 버튼을 눌러 작곡한 곡을 들어봅니다

### 2. 🎹 화음 구성하기

피아노 건반을 클릭하여 화음을 만들고 분석하는 기능입니다.

**주요 특징:**
- 인터랙티브 피아노 건반 (3옥타브, 4옥타브, 5옥타브)
- 화음 자동 인식 (장3화음, 단3화음, 7화음 등)
- 빠른 화음 구성 (미리 정의된 화음 타입 선택)
- 화음 정보 표시 (구성음, 화음 이름)

**지원하는 화음 타입:**
- 장3화음 (Major)
- 단3화음 (Minor)
- 감3화음 (Diminished)
- 증3화음 (Augmented)
- 서스2 (Sus2)
- 서스4 (Sus4)
- 7화음 (Dominant 7th)
- 장7화음 (Major 7th)
- 단7화음 (Minor 7th)
- 감7화음 (Diminished 7th)

### 3. 🎼 클래식 음악 감상

유명한 클래식 작곡가의 곡을 감상하고 멜로디와 화음을 분석하는 기능입니다.

**주요 특징:**
- 30개 이상의 유명 클래식 곡 제공
- 시대별 분류 (바로크, 고전주의, 낭만주의, 인상주의, 현대음악)
- 난이도별 분류 (초급, 중급, 고급)
- YouTube 영상 임베드
- 멜로디 분석 (피아노 건반에 표시)
- 화음 분석 (화음 진행 표시)
- 학생 활동 제안 (AI 기반)

**제공되는 작곡가:**
- 베토벤, 모차르트, 바흐, 쇼팽, 드뷔시, 비발디, 차이콥스키, 파헬벨, 그리그, 드보르자크 등

### 4. 🤖 AI 도우미

ChatGPT 기반 AI 음악 선생님이 음악 이론을 쉽게 설명하고 수업 계획을 생성합니다.

**주요 특징:**
- 음악 이론 질문 답변
- 수업 계획 자동 생성
- DOCX 파일 다운로드 지원
- 학생 나이에 맞는 맞춤형 설명
- 채팅 기록 관리

**사용 예시:**
- "4/4박자가 뭐예요?"
- "3학년 수업 계획 만들어줘"
- "화음이 뭐예요?"

### 5. 🔍 정보 & 영상

Perplexity AI와 YouTube를 활용하여 음악 교육 자료를 검색하는 기능입니다.

**주요 특징:**
- Perplexity AI 기반 웹 검색
- YouTube 교육 영상 검색
- 신뢰성 있는 영상 필터링 (10만 뷰 이상)
- 악보와 음원이 잘 보이는 영상 우선 추천
- 영상 미리보기 및 바로 재생

### 6. 👨‍🏫 교사 대시보드

교사가 학급과 학생을 관리하고 수업을 기록하는 기능입니다.

**주요 특징:**
- 학급 관리 (학년/반 등록)
- 학생 명단 관리
- 수업 기록 (날짜별 활동 기록)
- 진도 관리 (학생별 학습 진도)
- 통계 리포트

## 🛠 기술 스택

### Frontend
- **React 18** - UI 프레임워크
- **TypeScript** - 타입 안정성
- **Vite** - 빌드 도구
- **React Icons** - 아이콘 라이브러리
- **CSS3** - 스타일링

### Backend
- **Python 3.8+** - 서버 사이드 언어
- **FastAPI** - 웹 프레임워크
- **music21** - 음악 이론 및 악보 처리
- **librosa** - 오디오 분석
- **yt-dlp** - YouTube 오디오 다운로드
- **python-docx** - DOCX 파일 생성

### AI & API
- **OpenAI GPT-4o-mini** - AI 채팅 및 수업 계획 생성
- **Perplexity AI** - 웹 검색 (선택사항)
- **YouTube Data API v3** - 영상 검색 (선택사항)

### 오디오 처리
- **Web Audio API** - 브라우저 오디오 재생
- **FFmpeg** - 오디오 변환 (선택사항)

## 📦 설치 및 실행

### 사전 요구사항

- **Node.js** 18 이상
- **Python** 3.8 이상
- **npm** 또는 **yarn**

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/1210musicapp.git
cd 1210musicapp
```

### 2. Python 가상환경 설정

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. Node.js 패키지 설치

```bash
npm install
```

### 5. 환경 변수 설정 (선택사항)

`.env` 파일을 생성하고 API 키를 설정합니다:

```env
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

> **참고**: API 키가 없어도 기본 기능은 모두 사용 가능합니다. AI 기능만 제한됩니다.

### 6. 서버 실행

#### 방법 1: 개별 실행

**터미널 1 - API 서버:**
```bash
python start_api_server.py
```

**터미널 2 - 프론트엔드:**
```bash
npm run dev
```

#### 방법 2: 동시 실행 (Windows)

```bash
start_all.bat
```

또는 PowerShell:

```bash
start_all.ps1
```

#### 방법 3: npm 스크립트 사용

```bash
npm run start:all
```

### 7. 브라우저에서 접속

- **프론트엔드**: http://localhost:5173
- **API 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 📖 사용 방법

### 리듬 작곡기 사용하기

1. 메뉴에서 "리듬 작곡"을 선택합니다
2. 박자를 선택합니다 (예: 4/4박자)
3. 음표 길이를 선택합니다 (예: 4분음표)
4. 피아노 건반을 클릭하여 음표를 입력합니다
5. 마디가 가득 차면 자동으로 새 마디가 생성됩니다
6. 재생 버튼을 눌러 작곡한 곡을 들어봅니다

### 화음 구성하기

1. 메뉴에서 "화음 구성"을 선택합니다
2. 피아노 건반을 클릭하여 음표를 선택합니다
3. 선택된 음표로 화음이 자동으로 분석됩니다
4. 또는 "빠른 화음 구성"에서 미리 정의된 화음을 선택할 수 있습니다

### 클래식 음악 감상

1. 메뉴에서 "클래식 감상"을 선택합니다
2. 곡 목록에서 원하는 곡을 선택합니다
3. YouTube 영상을 감상합니다
4. "🎵 곡 분석하기" 버튼을 클릭하여 멜로디와 화음을 분석합니다
5. "멜로디", "화음", "학생 활동" 탭을 확인합니다

### AI 도우미 사용하기

1. 메뉴에서 "AI 도우미"를 선택합니다
2. 채팅창에 질문을 입력합니다
3. AI가 답변을 생성합니다
4. 수업 계획이 생성되면 DOCX 파일로 다운로드할 수 있습니다

## 🔑 API 설정

### OpenAI API 키 설정

1. [OpenAI Platform](https://platform.openai.com/)에서 API 키를 발급받습니다
2. `.env` 파일에 추가합니다:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. 또는 환경 변수로 설정합니다:
   ```bash
   # Windows
   set OPENAI_API_KEY=sk-...
   
   # macOS/Linux
   export OPENAI_API_KEY=sk-...
   ```

### Perplexity API 키 설정 (선택사항)

1. [Perplexity AI](https://www.perplexity.ai/)에서 API 키를 발급받습니다
2. `.env` 파일에 추가합니다:
   ```env
   PERPLEXITY_API_KEY=pplx-...
   ```

### YouTube Data API 키 설정 (선택사항)

1. [Google Cloud Console](https://console.cloud.google.com/)에서 API 키를 발급받습니다
2. YouTube Data API v3를 활성화합니다
3. `.env` 파일에 추가합니다:
   ```env
   YOUTUBE_API_KEY=...
   ```

## 📁 프로젝트 구조

```
1210musicapp/
├── src/
│   ├── api_server.py          # FastAPI 서버 (메인)
│   ├── audio_processor.py      # 오디오 처리 모듈
│   ├── score_processor.py     # 악보 처리 모듈
│   ├── chord_analyzer.py       # 화음 분석 모듈
│   ├── chord_generator.py      # 화음 생성 모듈
│   ├── ai_assistant.py         # AI 어시스턴트 모듈
│   ├── perplexity_assistant.py # Perplexity AI 모듈
│   ├── youtube_downloader.py   # YouTube 다운로더
│   ├── youtube_helper.py        # YouTube API 헬퍼
│   ├── omr_service.py          # OMR 서비스 (이미지→악보)
│   ├── pdf_parser.py           # PDF 파서
│   └── frontend/               # React 프론트엔드
│       ├── App.tsx             # 메인 앱 컴포넌트
│       ├── components/         # React 컴포넌트
│       │   ├── RhythmComposer.tsx      # 리듬 작곡기
│       │   ├── ChordAnalysis.tsx       # 화음 구성
│       │   ├── ClassicMusicEducation.tsx # 클래식 감상
│       │   ├── AIAssistant.tsx         # AI 도우미
│       │   ├── PerplexityYouTube.tsx    # 정보 & 영상
│       │   ├── TeacherDashboard.tsx    # 교사 대시보드
│       │   └── PianoKeyboard.tsx        # 피아노 건반
│       └── utils/
│           └── api.ts          # API 클라이언트
├── requirements.txt            # Python 패키지 목록
├── package.json               # Node.js 패키지 목록
├── vite.config.ts             # Vite 설정
├── start_api_server.py        # API 서버 시작 스크립트
├── start_all.bat              # Windows 시작 스크립트
└── README.md                  # 이 파일
```

## 🎨 주요 컴포넌트 설명

### RhythmComposer (리듬 작곡기)
- 박자에 맞춰 음표 입력
- 마디 단위 자동 관리
- 화음 자동 분석
- 악보 자동 생성
- 자동 재생

### ChordAnalysis (화음 구성)
- 인터랙티브 피아노 건반
- 화음 자동 인식
- 빠른 화음 구성

### ClassicMusicEducation (클래식 감상)
- 30개 이상의 클래식 곡 제공
- 멜로디/화음 분석
- 학생 활동 제안

### AIAssistant (AI 도우미)
- ChatGPT 기반 채팅
- 수업 계획 생성
- DOCX 다운로드

### PianoKeyboard (피아노 건반)
- 3-5옥타브 지원
- Web Audio API 재생
- 화음 하이라이트
- 인터랙티브 클릭

## 🐛 문제 해결

### API 서버가 시작되지 않을 때

1. Python 가상환경이 활성화되어 있는지 확인합니다
2. 필요한 패키지가 설치되어 있는지 확인합니다:
   ```bash
   pip install -r requirements.txt
   ```
3. 포트 8000이 사용 중인지 확인합니다

### 프론트엔드가 로드되지 않을 때

1. Node.js 버전을 확인합니다 (18 이상 필요)
2. 패키지를 재설치합니다:
   ```bash
   rm -rf node_modules
   npm install
   ```
3. 포트 5173이 사용 중인지 확인합니다

### music21 모듈 오류

```bash
pip install music21
```

### numpy, soundfile 오류

```bash
pip install numpy soundfile
```

### FFmpeg 오류 (YouTube 다운로드)

Windows에서 FFmpeg를 설치하고 경로를 설정합니다:
1. [FFmpeg 다운로드](https://ffmpeg.org/download.html)
2. `C:\ffmpeg\bin`에 설치
3. 환경 변수에 추가하거나 코드에서 경로 지정

## 🤝 기여하기

프로젝트에 기여하고 싶으시다면:

1. Fork 합니다
2. Feature 브랜치를 만듭니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 엽니다

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- [music21](https://web.mit.edu/music21/) - 음악 이론 라이브러리
- [React](https://react.dev/) - UI 프레임워크
- [FastAPI](https://fastapi.tiangolo.com/) - 웹 프레임워크
- [OpenAI](https://openai.com/) - AI API
- [Vite](https://vitejs.dev/) - 빌드 도구

## 📞 문의

문제가 발생하거나 제안사항이 있으시면 이슈를 등록해주세요.

---

**Made with ❤️ for Elementary Music Education**
