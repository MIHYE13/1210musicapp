# CORS 오류 해결 가이드

## 발견된 문제

콘솔에서 다음 오류가 발생했습니다:
```
Access to fetch at 'http://localhost:8501/api/ai/chat' from origin 'http://localhost:5176' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 원인

1. 프론트엔드가 `http://localhost:5176`에서 실행 중
2. CORS 설정에 `localhost:5176`이 포함되지 않았음
3. OPTIONS preflight 요청이 제대로 처리되지 않음

## 해결 방법

### 1. API 서버 재시작 (필수!)

CORS 설정을 변경했으므로 **API 서버를 재시작**해야 합니다:

```bash
# 기존 서버 종료 (Ctrl+C)
# 새로 시작
python start_api_simple.py
```

### 2. CORS 설정 확인

`src/api_server.py`의 CORS 설정에 다음이 포함되어 있는지 확인:
- `http://localhost:5176`
- `http://127.0.0.1:5176`
- `allow_methods`에 `OPTIONS` 포함

### 3. 프론트엔드 포트 확인

Vite가 다른 포트에서 실행 중일 수 있습니다. 확인:
```bash
# package.json 또는 vite.config.ts 확인
npm run dev
```

## 수정된 CORS 설정

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5176",  # 추가됨
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5176",  # 추가됨
        "http://localhost:3001",
        "*",  # 개발 환경에서 모든 origin 허용
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # preflight 캐시 시간
)
```

## 확인 방법

### 1. API 서버 재시작 후 확인
```bash
# 브라우저에서
http://localhost:8501/api/health
```

### 2. OPTIONS 요청 테스트
브라우저 개발자 도구 Network 탭에서:
- OPTIONS 요청이 200 OK로 응답하는지 확인
- 응답 헤더에 `Access-Control-Allow-Origin`이 있는지 확인

### 3. 실제 API 호출 테스트
프론트엔드에서 API를 호출하고 콘솔 오류가 사라졌는지 확인

## 추가 문제 해결

### 문제가 계속되면:

1. **브라우저 캐시 삭제**
   - Ctrl+Shift+Delete
   - 캐시된 이미지 및 파일 삭제

2. **하드 리프레시**
   - Ctrl+Shift+R (Windows)
   - Cmd+Shift+R (Mac)

3. **다른 브라우저에서 테스트**
   - Chrome, Firefox, Edge 등

4. **포트 확인**
   ```powershell
   Get-NetTCPConnection -LocalPort 8501
   Get-NetTCPConnection -LocalPort 5176
   ```

## 예상 결과

수정 후:
- ✅ CORS 오류가 사라짐
- ✅ API 호출이 정상 작동
- ✅ OPTIONS 요청이 200 OK로 응답

