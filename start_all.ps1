# 초등 음악 도우미 앱 시작 스크립트

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "초등 음악 도우미 앱 시작" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] API 서버 시작..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host '[API] 초등 음악 도우미 API 서버' -ForegroundColor Green; Write-Host ''; Write-Host '[주소] API 서버: http://localhost:8501' -ForegroundColor Yellow; Write-Host '[문서] API 문서: http://localhost:8501/docs' -ForegroundColor Yellow; Write-Host ''; python start_api_simple.py"

Start-Sleep -Seconds 3

Write-Host "[2/2] React 프론트엔드 시작..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host '[React] 초등 음악 도우미 프론트엔드' -ForegroundColor Green; Write-Host ''; Write-Host '[주소] 프론트엔드: http://localhost:5173' -ForegroundColor Yellow; Write-Host ''; npm run dev"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "시작 완료!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API 서버: http://localhost:8501" -ForegroundColor Yellow
Write-Host "프론트엔드: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "브라우저에서 http://localhost:5173 을 열어주세요." -ForegroundColor White
Write-Host ""
Write-Host "서버를 중지하려면 각 창을 닫으세요." -ForegroundColor Gray
Write-Host ""

