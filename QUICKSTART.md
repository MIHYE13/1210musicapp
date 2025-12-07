# 빠른 시작 가이드

## 5분만에 시작하기! 🚀

### 방법 1: 로컬에서 실행 (권장)

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/elementary-music-helper.git
cd elementary-music-helper

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 실행!
streamlit run src/app.py
```

브라우저에서 `http://localhost:8501` 열림!

#### 🔐 API 키 설정 (선택사항)

**가장 쉬운 방법: .env 파일**

```bash
# 1. 템플릿 복사
cp .env.example .env

# 2. 편집기로 열어 API 키 입력
nano .env  # 또는 code .env

# 3. 저장 후 앱 재시작
```

**자세히**: [.env 가이드](docs/env_setup.md) | [API 발급](docs/api_setup.md)

### 방법 2: Streamlit Cloud (배포)

1. GitHub에 코드 푸시
2. https://share.streamlit.io 방문
3. "New app" → 저장소 선택 → `src/app.py` 선택
4. "Deploy!" 클릭
5. 5분 후 URL 생성됨!

## 첫 번째 악보 만들기

### 예제 1: 오디오에서 악보 생성

1. 왼쪽 패널에서 "오디오 파일 업로드" 클릭
2. MP3/WAV 파일 선택 (예: 동요, 간단한 멜로디)
3. "🎼 악보 생성하기" 버튼 클릭
4. 30초 정도 기다리면 악보 완성! ✨

### 예제 2: MIDI 파일 처리

1. 오른쪽 패널에서 "악보 파일 업로드" 클릭
2. MIDI 파일 선택
3. 옵션 선택:
   - ✅ 계이름 추가
   - ✅ 다장조 변환
   - ✅ 반주 추가
4. "🎵 처리하기" 버튼 클릭
5. 완성! 재생하고 다운로드하세요!

## 테스트용 샘플 파일

프로젝트에 샘플 파일이 없다면 다음을 시도하세요:

### 간단한 MIDI 만들기

Python으로 간단한 MIDI 생성:

```python
from music21 import stream, note

# 도레미파솔 악보 만들기
s = stream.Score()
part = stream.Part()

notes = ['C4', 'D4', 'E4', 'F4', 'G4']
for n in notes:
    part.append(note.Note(n, quarterLength=1))

s.append(part)
s.write('midi', 'test.mid')
```

또는 무료 MIDI 파일:
- https://www.midiworld.com/
- https://freemidi.org/

## 주요 기능 한눈에 보기

| 기능 | 설명 | 위치 |
|------|------|------|
| 🎤 오디오 → 악보 | MP3/WAV를 악보로 변환 | 왼쪽 패널 |
| 🎵 계이름 추가 | 도레미... 자동 표시 | 오른쪽 - 옵션 |
| 🎹 다장조 변환 | C major로 자동 이조 | 오른쪽 - 옵션 |
| 🎼 반주 생성 | 기본 화음 반주 추가 | 오른쪽 - 옵션 |
| ▶️ 재생 | 브라우저에서 즉시 재생 | 완성 후 |
| 💾 다운로드 | MIDI/MusicXML 저장 | 완성 후 |
| 🆕 🤖 AI 도우미 | ChatGPT 음악 선생님 | 하단 섹션 |

## 문제가 생겼나요?

### "악보 생성 실패"
→ 더 간단하고 명확한 멜로디 시도

### "모듈을 찾을 수 없습니다"
→ `pip install -r requirements.txt` 다시 실행

### "MuseScore 오류"
→ 악보 이미지는 안 보여도 MIDI 다운로드는 가능!

### "AI 기능이 작동하지 않아요"
→ [API 설정 가이드](docs/api_setup.md) 참조 (선택사항)

### 더 많은 도움말
- [상세 설치 가이드](docs/installation.md)
- [사용자 가이드](docs/user_guide.md)
- [API 설정 가이드](docs/api_setup.md) - AI 기능 활성화
- [GitHub Issues](https://github.com/yourusername/elementary-music-helper/issues)

## 🆕 AI 기능 사용하기 (선택사항)

### AI 기능이란?
ChatGPT를 활용한 음악 교육 도우미 기능입니다:
- 악보 자동 분석 및 난이도 평가
- 음악 이론 질문 답변
- 맞춤형 연습 방법 제안
- 수업 계획 자동 생성

### 활성화 방법
1. **OpenAI API 키 발급** ([상세 가이드](docs/api_setup.md))
2. **설정 방법 선택**:
   - 로컬: `.streamlit/secrets.toml`에 추가
   - 배포: Streamlit Cloud Secrets에 추가

```toml
OPENAI_API_KEY = "sk-proj-your-key-here"
```

3. **앱 재시작**
4. **AI 섹션에서 "✅ AI 기능 활성화됨" 확인**

### API 키 없이도 사용 가능!
AI 기능은 선택사항입니다. 없어도:
- ✅ 모든 악보 변환 기능 사용 가능
- ✅ 계이름, 반주, 재생 모두 정상 작동
- ❌ AI 분석/채팅만 제한적

### 예상 비용
- 한 달 $3-10 정도 (사용량에 따라)
- 악보 분석 1회: ~$0.01
- 자세한 내용: [API 설정 가이드](docs/api_setup.md)

## 다음 단계

1. ✅ 앱 실행 완료!
2. 📚 [사용자 가이드](docs/user_guide.md) 읽기
3. 🎵 첫 악보 만들어보기
4. 🚀 [배포하기](docs/deployment.md) (선택사항)
5. 🌟 GitHub에 Star 주기!

## 교사를 위한 팁

### 수업 준비
```
1. 노래 선정 → 2. 오디오 업로드 → 3. 악보 생성 → 4. 계이름 추가 → 5. 수업 자료 완성!
```

### 학생 과제
```
URL만 공유하면 학생들이 집에서 연습 가능!
```

### 저장 및 공유
```
MIDI/MusicXML 다운로드 → Google Drive/OneDrive에 보관 → 언제든 재사용
```

## 학생을 위한 팁

1. **계이름 보며 노래하기** 🎤
2. **재생 버튼으로 여러 번 듣기** 🔄
3. **친구와 함께 연습하기** 👯
4. **선생님께 질문하기** 🙋

---

**즐거운 음악 학습 되세요! 🎵✨**

문의: GitHub Issues | 이메일: your-email@example.com
