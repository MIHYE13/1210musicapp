# Changelog

모든 주요 변경 사항이 이 파일에 문서화됩니다.

## [5.0.0] - 2024-12-03

### 🆕 추가됨 - 차별화 기능!
- **화음 분석 & 피아노 연주 페이지**
  - `src/chord_analyzer.py`: MIDI 화음 자동 분석 모듈
  - `src/youtube_downloader.py`: YouTube 오디오 다운로더
  - `src/pdf_parser.py`: PDF 악보 파서 (OMR 지원)
  - `pages/2_🎹_화음_분석_피아노.py`: 새로운 멀티페이지

- **MIDI 반주 음원 분석**
  - 화음 자동 추출 및 분석
  - 다장조(C major) 자동 변환
  - 마디별 화음 진행 표시
  - 화음 코드 차트 생성

- **인터랙티브 피아노 건반**
  - 화음을 피아노 건반에 시각화
  - 클릭하여 소리 재생 (Web Audio API)
  - SVG 기반 고품질 렌더링
  - 흰 건반/검은 건반 구분
  - 화음 구성음 하이라이트 (금색)

- **YouTube 음원 지원**
  - YouTube URL에서 오디오 추출
  - yt-dlp 통합
  - 자동/수동 다운로드 가이드
  - 화음 분석 워크플로우

- **PDF 악보 지원**
  - PDF 악보 업로드
  - OMR (Optical Music Recognition) 가이드
  - Audiveris, MuseScore 연동 방법
  - MusicXML 변환 워크플로우

### 📝 변경됨
- `requirements.txt`: PyPDF2, pdf2image, yt-dlp 추가
- `src/__init__.py`: 새 모듈 export
- 다장조 변환 기능 강화
- 화음 분석 알고리즘 추가

### 🔧 개선됨
- 음악 학습 경험 혁신
- 시각적 화음 학습
- 실시간 인터랙티브 연주
- 다양한 입력 형식 지원 (MIDI, YouTube, PDF)

### 🎯 차별화 포인트
1. **자동 화음 분석** - 다른 앱에 없는 기능
2. **피아노 건반 시각화** - 학습 효과 극대화
3. **인터랙티브 연주** - 클릭으로 소리 재생
4. **다양한 입력** - MIDI/YouTube/PDF 모두 지원
5. **다장조 통일** - 초보자 최적화

## [4.0.0] - 2024-12-03

### 🆕 추가됨
- **교사용 대시보드**
  - `src/database.py`: SQLite 데이터베이스 관리
  - `pages/1_👨‍🏫_교사_대시보드.py`: 멀티페이지 대시보드
  - 학급 관리: 학년/반 등록 및 관리
  - 학생 명단: 학생 정보 CRUD
  - 수업 기록: 날짜별 활동 및 수업 내용 기록
  - 진도 관리: 학생별 학습 진도 및 평가 기록
  - 통계 리포트: 학급별/학생별 통계 및 분석
  - CSV 다운로드: 학생 명단 내보내기

- **GitHub Streamlit Cloud 배포**
  - `docs/github_deployment.md`: 완벽한 배포 가이드
  - 자동 배포 설정 방법
  - Secrets 관리
  - 문제 해결 가이드
  - 모니터링 및 유지보수

### 📝 변경됨
- `src/app.py`: 대시보드 링크 안내 추가
- `.gitignore`: data/ 폴더 및 데이터베이스 파일 추가
- `README.md`: 대시보드 기능 설명 추가

### 🔧 개선됨
- Streamlit 멀티페이지 구조 활용
- 데이터베이스 기반 데이터 관리
- 교사 워크플로우 최적화
- 학급 단위 통계 및 분석

## [3.1.0] - 2024-12-03

### 🆕 추가됨
- **.env 파일 지원**
  - `python-dotenv` 패키지 추가
  - `.env.example` 템플릿 파일
  - 모든 AI 모듈에서 .env 파일 자동 로드
  - 로컬 개발 환경에서 API 키 관리 간편화

- **문서**
  - `docs/env_setup.md`: .env 파일 사용 완벽 가이드
    - 빠른 시작 방법
    - 보안 모범 사례
    - 문제 해결
    - 팀 협업 가이드

### 📝 변경됨
- `requirements.txt`: python-dotenv 추가
- `src/ai_assistant.py`: .env 파일 로드 기능
- `src/perplexity_assistant.py`: .env 파일 로드 기능
- `src/youtube_helper.py`: .env 파일 로드 기능
- API 키 우선순위: Streamlit Secrets → .env 파일 → 없음
- `README.md`: .env 설정 방법 추가
- `QUICKSTART.md`: .env 빠른 시작 추가

### 🔧 개선됨
- API 키 관리 더 쉬워짐 (코드 수정 불필요)
- 로컬 개발 환경 설정 간소화
- .gitignore에 .env 이미 포함 (보안)
- 개발자 경험 향상

## [3.0.0] - 2024-12-03

### 🆕 추가됨
- **Perplexity API 통합**
  - `src/perplexity_assistant.py`: 웹 기반 음악 교육 조사 모듈
  - 음악 이론 실시간 웹 조사
  - 곡 배경 정보 상세 조사
  - 최신 교육 자료 검색
  - 음악 교육 트렌드 분석
  - 교수법 비교 분석
  - 출처 링크 포함

- **YouTube Data API 통합**
  - `src/youtube_helper.py`: 교육 영상 검색 모듈
  - 교육 영상 자동 검색 (안전 검색 적용)
  - 악기 튜토리얼 찾기
  - 음악 이론 설명 영상 추천
  - 연습용 반주(MR) 검색
  - 교육 채널 큐레이션
  - 재생목록 관리
  - 완전 무료! (일일 10,000 쿼리)

- **통합 리소스 센터**
  - 메인 앱에 "🔍 최신 정보 & 영상 자료" 섹션 추가
  - 웹 조사(Perplexity)와 영상 검색(YouTube) 한곳에서
  - 5가지 조사 유형 지원
  - 5가지 영상 검색 유형 지원

- **문서 업데이트**
  - `docs/api_setup.md`: 3개 API 통합 설정 가이드
    - Perplexity API 키 발급 방법
    - YouTube API 설정 (Google Cloud Console)
    - 3개 API 통합 secrets 관리
    - API별 비용 분석 및 비교

### 📝 변경됨
- `requirements.txt`: requests 패키지 추가 (v2.31.0)
- `src/app.py`: Perplexity와 YouTube 탭 통합
- `src/__init__.py`: 새 모듈 export 추가
- `README.md`: v3.0 기능 소개 업데이트
- `.cursorrules`: 3개 API 통합 개발 가이드 추가

### 🔧 개선됨
- API 독립성: 각 API를 개별적으로 활성화 가능
- Fallback 메커니즘: API 없어도 기본 정보 제공
- 에러 처리: 네트워크 오류 및 API 실패 대응
- 비용 효율성: YouTube 무료, Perplexity 선택적 사용

### 💰 비용 구조
- YouTube API: **완전 무료** (일일 10,000 쿼리)
- Perplexity API: $5-20/월 (적극 사용 시)
- ChatGPT API: $3-10/월 (기존)
- **전체**: $8-30/월 (모든 기능 사용 시)

## [2.0.0] - 2024-12-03

### 🆕 추가됨
- **ChatGPT AI 음악 도우미 통합**
  - `src/ai_assistant.py`: AI 어시스턴트 핵심 모듈
  - 악보 자동 분석 및 난이도 평가
  - 실시간 음악 질문 답변 채팅
  - 학생 나이별 맞춤 음악 이론 설명
  - 학년별 수업 계획 자동 생성
  - 화음 진행 개선 제안
  
- **문서**
  - `docs/api_setup.md`: OpenAI API 설정 완벽 가이드
    - API 키 발급 방법
    - 보안 모범 사례
    - 로컬/배포 환경 설정
    - 문제 해결 가이드
    - 비용 관리 팁

- **UI 개선**
  - 메인 앱에 "🤖 AI 음악 도우미" 섹션 추가
  - 3개 탭: 질문하기, 음악 이론, 수업 계획
  - 악보 처리 완료 시 자동 AI 분석
  - API 키 상태 표시 및 안내

### 📝 변경됨
- `requirements.txt`: openai 패키지 추가 (v1.12.0)
- `README.md`: AI 기능 소개 섹션 추가
- `QUICKSTART.md`: AI 사용법 및 설정 가이드 추가
- `.cursorrules`: AI 통합 개발 가이드 추가
- `src/__init__.py`: AIAssistant 클래스 export
- `src/app.py`: AI 기능 UI 통합

### 🔧 개선됨
- API 키 없어도 모든 기본 기능 사용 가능
- AI 기능 사용 시 fallback 메커니즘 제공
- 에러 처리 강화 (API 실패 시 대체 답변)
- 사용자 친화적인 안내 메시지

### 📚 문서
- 모든 문서에 AI 기능 섹션 추가
- API 설정 상세 가이드 작성
- 비용 및 보안 정보 추가

## [1.0.0] - 2024-12-03

### 🎉 초기 릴리스
- **핵심 기능**
  - 오디오 → 악보 변환 (basic-pitch)
  - 계이름 자동 기재
  - 다장조 자동 변환
  - 기본 반주 생성
  - 브라우저 재생
  - MIDI/MusicXML 다운로드

- **모듈**
  - `src/audio_processor.py`: 오디오 처리
  - `src/score_processor.py`: 악보 변환
  - `src/chord_generator.py`: 반주 생성
  - `src/player.py`: 재생 기능
  - `utils/music_utils.py`: 음악 이론 도구
  - `utils/file_utils.py`: 파일 처리 도구

- **문서**
  - README.md: 프로젝트 소개
  - QUICKSTART.md: 빠른 시작 가이드
  - docs/installation.md: 설치 가이드
  - docs/user_guide.md: 사용자 매뉴얼
  - docs/deployment.md: 배포 가이드

- **개발 환경**
  - .cursorrules: Cursor AI 개발 가이드
  - requirements.txt: Python 패키지 목록
  - .streamlit/config.toml: Streamlit 설정

---

## 버전 관리 규칙

이 프로젝트는 [Semantic Versioning](https://semver.org/)을 따릅니다:
- **MAJOR** (2.x.x): 호환되지 않는 API 변경
- **MINOR** (x.2.x): 하위 호환되는 기능 추가
- **PATCH** (x.x.2): 하위 호환되는 버그 수정

## 변경 사항 카테고리

- **추가됨**: 새로운 기능
- **변경됨**: 기존 기능의 변경
- **폐기 예정**: 곧 제거될 기능
- **제거됨**: 제거된 기능
- **수정됨**: 버그 수정
- **보안**: 보안 관련 수정
