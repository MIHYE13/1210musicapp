"""
API 서버 시작 스크립트
FastAPI 서버를 실행합니다.
"""

import uvicorn
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 초등 음악 도우미 API 서버 시작")
    print("=" * 60)
    print()
    print("📍 API 서버 주소: http://localhost:8501")
    print("📚 API 문서: http://localhost:8501/docs")
    print("🔍 대화형 API 문서: http://localhost:8501/redoc")
    print()
    print("⚠️  React 프론트엔드는 http://localhost:3000 에서 실행하세요")
    print()
    print("=" * 60)
    print()
    
    uvicorn.run(
        "src.api_server:app",
        host="0.0.0.0",
        port=8501,
        reload=True,  # 개발 모드: 코드 변경 시 자동 재시작
        log_level="info"
    )

