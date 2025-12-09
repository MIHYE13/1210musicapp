@echo off
chcp 65001 >nul
echo ========================================
echo 초등 음악 도우미 앱 시작
echo ========================================
echo.

echo [1/2] API 서버 시작...
start "API 서버" cmd /k "python start_api_simple.py"

timeout /t 3 /nobreak >nul

echo [2/2] React 프론트엔드 시작...
start "React 프론트엔드" cmd /k "npm run dev"

echo.
echo ========================================
echo 시작 완료!
echo ========================================
echo.
echo API 서버: http://localhost:8501
echo 프론트엔드: http://localhost:5173
echo.
echo 창을 닫지 마세요!
echo.
pause
