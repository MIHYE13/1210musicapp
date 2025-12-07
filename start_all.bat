@echo off
echo ========================================
echo 초등 음악 도우미 시작
echo ========================================
echo.

echo [1/2] API 서버 시작 중...
start "API Server" cmd /k "python start_api_server.py"

echo [2/2] 3초 후 React 프론트엔드 시작...
timeout /t 3 /nobreak >nul

echo React 프론트엔드 시작 중...
start "React Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo 모든 서버가 시작되었습니다!
echo ========================================
echo.
echo API 서버: http://localhost:8501
echo 프론트엔드: http://localhost:3000
echo.
pause

