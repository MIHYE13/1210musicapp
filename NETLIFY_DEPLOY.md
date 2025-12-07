# Netlify 배포 가이드

## 📋 배포 정보

### Branch to Deploy
- **기본 브랜치**: `main`
- Netlify는 기본적으로 `main` 브랜치를 자동으로 배포합니다.

## 🚀 배포 방법

### 방법 1: Netlify 대시보드에서 배포 (권장)

1. **Netlify 계정 생성**
   - https://app.netlify.com 접속
   - GitHub 계정으로 로그인

2. **새 사이트 추가**
   - "Add new site" → "Import an existing project" 클릭
   - GitHub 저장소 선택

3. **빌드 설정**
   - **Branch to deploy**: `main`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

4. **환경 변수 설정** (선택사항)
   - Site settings → Environment variables
   - 프론트엔드에서 필요한 환경 변수 추가:
     ```
     VITE_API_BASE_URL=https://your-backend-url.com/api
     ```

5. **배포**
   - "Deploy site" 클릭
   - 자동으로 빌드 및 배포 시작

### 방법 2: Netlify CLI로 배포

```bash
# Netlify CLI 설치
npm install -g netlify-cli

# 로그인
netlify login

# 배포
netlify deploy --prod
```

## ⚙️ 설정 파일

### netlify.toml
프로젝트 루트에 `netlify.toml` 파일이 있습니다. 이 파일에 다음 설정이 포함되어 있습니다:

- **Branch**: `main` (배포할 브랜치)
- **Build command**: `npm run build`
- **Publish directory**: `dist`
- **SPA 리다이렉트**: React Router 지원

### public/_redirects
SPA 라우팅을 위한 리다이렉트 규칙이 포함되어 있습니다.

## 🔧 빌드 설정 요약

| 항목 | 값 |
|------|-----|
| Branch to deploy | `main` |
| Build command | `npm run build` |
| Publish directory | `dist` |
| Node version | 18 (권장) |

## 📝 주의사항

1. **환경 변수**
   - `.env` 파일은 Git에 커밋하지 마세요 (이미 .gitignore에 포함됨)
   - Netlify 대시보드에서 환경 변수를 설정하세요

2. **API 엔드포인트**
   - 프론트엔드는 백엔드 API를 호출합니다
   - `VITE_API_BASE_URL` 환경 변수로 백엔드 URL을 설정하세요

3. **빌드 오류**
   - 빌드가 실패하면 Netlify 대시보드의 "Deploy log"에서 확인하세요
   - 로컬에서 `npm run build`로 먼저 테스트하세요

## 🔗 유용한 링크

- [Netlify 문서](https://docs.netlify.com/)
- [Vite 배포 가이드](https://vitejs.dev/guide/static-deploy.html#netlify)
- [React Router 배포](https://reactrouter.com/en/main/start/overview#deployment)

## ✅ 배포 확인

배포가 완료되면:
1. Netlify가 자동으로 URL을 생성합니다 (예: `your-site.netlify.app`)
2. 커스텀 도메인을 설정할 수 있습니다
3. `main` 브랜치에 푸시할 때마다 자동으로 재배포됩니다

