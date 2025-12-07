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
    # Windows 콘솔 인코딩 설정
    import sys
    import io
    if sys.platform == 'win32':
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        except:
            pass
    
    print("=" * 60)
    print("[API] 초등 음악 도우미 API 서버 시작")
    print("=" * 60)
    print()
    print("[주소] API 서버: http://localhost:8501")
    print("[문서] API 문서: http://localhost:8501/docs")
    print("[문서] 대화형 API: http://localhost:8501/redoc")
    print()
    print("[참고] React 프론트엔드는 http://localhost:5173 에서 실행하세요")
    print()
    print("=" * 60)
    print()
    
    uvicorn.run(
        "src.api_server:app",
        host="0.0.0.0",
        port=8501,
        reload=False,  # Python 3.14 호환성 문제로 reload 비활성화
        log_level="info"
    )

