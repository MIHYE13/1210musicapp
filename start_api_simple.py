"""
API 서버 시작 스크립트 (간단 버전)
FastAPI 서버를 실행합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

if __name__ == "__main__":
    print("=" * 60)
    print("[API] 초등 음악 도우미 API 서버 시작")
    print("=" * 60)
    print()
    print("[주소] API 서버: http://localhost:8501")
    print("[문서] API 문서: http://localhost:8501/docs")
    print()
    print("=" * 60)
    print()
    
    try:
        from src.api_server import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8501,
            log_level="info"
        )
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        input("계속하려면 Enter를 누르세요...")

