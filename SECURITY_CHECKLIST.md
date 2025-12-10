# 🔒 보안 체크리스트

Netlify 배포 전 환경 변수 보안 확인 사항

## ✅ 필수 확인 사항

### 1. .gitignore 확인
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있음
- [ ] `.env.local` 파일이 `.gitignore`에 포함되어 있음
- [ ] `.env` 파일이 Git 저장소에 커밋되지 않았음
  ```bash
  # 확인 명령어
  git ls-files | grep .env
  # 결과가 없어야 함
  ```

### 2. 환경 변수 사용 패턴
- [ ] 프론트엔드에서 `VITE_` 접두사만 사용
- [ ] API 키가 프론트엔드 코드에 하드코딩되지 않음
- [ ] `process.env.OPENAI_API_KEY` 같은 패턴이 없음
- [ ] `import.meta.env.VITE_*` 패턴만 사용

### 3. 코드 검색
다음 명령어로 API 키가 코드에 포함되어 있는지 확인:
```bash
# 프론트엔드 코드에서 API 키 검색
grep -r "OPENAI_API_KEY\|PERPLEXITY_API_KEY\|YOUTUBE_API_KEY" src/frontend/
# 결과가 없어야 함

# 하드코딩된 API 키 검색
grep -r "sk-[a-zA-Z0-9]\{32,\}\|pplx-[a-zA-Z0-9]\{32,\}\|AIza[a-zA-Z0-9_-]\{32,\}" src/frontend/
# 결과가 없어야 함
```

### 4. 빌드 결과물 확인
```bash
# 빌드 실행
npm run build

# 빌드 결과물에서 API 키 검색
grep -r "OPENAI_API_KEY\|PERPLEXITY_API_KEY\|YOUTUBE_API_KEY" dist/
# 결과가 없어야 함

# JavaScript 번들 파일 확인
find dist -name "*.js" -exec grep -l "sk-\|pplx-\|AIza" {} \;
# 결과가 없어야 함
```

### 5. Netlify 설정
- [ ] Netlify 대시보드에서 환경 변수 설정 완료
- [ ] `VITE_API_BASE_URL` 환경 변수 설정됨
- [ ] 환경 변수 범위가 올바르게 설정됨 (Production/Preview)

## 🚨 보안 위험 패턴

### ❌ 절대 하지 말아야 할 것들

1. **프론트엔드에서 API 키 직접 사용**
   ```typescript
   // ❌ 잘못된 예시
   const apiKey = "sk-1234567890abcdef..."
   const apiKey = process.env.OPENAI_API_KEY
   const apiKey = import.meta.env.OPENAI_API_KEY
   ```

2. **VITE_ 접두사로 API 키 노출**
   ```typescript
   // ❌ 잘못된 예시
   const apiKey = import.meta.env.VITE_OPENAI_API_KEY
   ```

3. **코드에 API 키 하드코딩**
   ```typescript
   // ❌ 잘못된 예시
   const config = {
     openaiKey: "sk-1234567890abcdef..."
   }
   ```

### ✅ 올바른 사용 패턴

1. **프론트엔드: API Base URL만 사용**
   ```typescript
   // ✅ 올바른 예시
   const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8501/api'
   ```

2. **백엔드: 환경 변수에서 API 키 로드**
   ```python
   # ✅ 올바른 예시
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

## 📋 배포 전 최종 체크리스트

- [ ] `.env` 파일이 Git에 커밋되지 않았음
- [ ] API 키가 프론트엔드 코드에 없음
- [ ] 빌드 결과물에 API 키가 포함되지 않음
- [ ] Netlify 환경 변수 설정 완료
- [ ] 프로덕션 빌드 테스트 완료
- [ ] 브라우저 개발자 도구에서 API 키 확인 (없어야 함)

## 🔍 문제 발견 시 조치

1. **API 키가 코드에 발견된 경우**
   - 즉시 해당 키 재발급
   - 코드에서 제거
   - Git 히스토리에서 제거 (필요시)
   - Netlify 환경 변수 업데이트

2. **빌드 결과물에 API 키가 포함된 경우**
   - 빌드 설정 확인
   - 환경 변수 접두사 확인
   - Vite 설정 확인

3. **환경 변수가 작동하지 않는 경우**
   - Netlify 대시보드 설정 확인
   - 환경 변수 이름 확인 (대소문자 구분)
   - 배포 재실행

## 📚 참고 문서

- [NETLIFY_DEPLOY.md](./NETLIFY_DEPLOY.md) - Netlify 배포 가이드
- [Vite 환경 변수 문서](https://vitejs.dev/guide/env-and-mode.html)
- [Netlify 환경 변수 문서](https://docs.netlify.com/environment-variables/overview/)

