"""
API 서버 시작 테스트 스크립트
오류를 확인하기 위해 사용
"""

import sys
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

print("=" * 60)
print("[테스트] API 서버 모듈 로드 테스트")
print("=" * 60)
print()

try:
    # 프로젝트 루트를 Python 경로에 추가
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    print("[1단계] 프로젝트 경로 추가 완료")
    print(f"   경로: {project_root}")
    print()
    
    # API 서버 모듈 로드
    print("[2단계] API 서버 모듈 로드 시도...")
    api_server_path = project_root / 'src' / 'api_server.py'
    print(f"   파일 경로: {api_server_path}")
    print(f"   파일 존재: {api_server_path.exists()}")
    
    if not api_server_path.exists():
        print("[ERROR] api_server.py 파일을 찾을 수 없습니다!")
        sys.exit(1)
    
    import importlib.util
    spec = importlib.util.spec_from_file_location("api_server", api_server_path)
    api_server = importlib.util.module_from_spec(spec)
    sys.modules["api_server"] = api_server
    
    print("[3단계] 모듈 실행 중...")
    spec.loader.exec_module(api_server)
    print("[OK] 모듈 로드 성공!")
    print()
    
    # FastAPI app 확인
    print("[4단계] FastAPI app 확인...")
    if hasattr(api_server, 'app'):
        app = api_server.app
        print(f"[OK] FastAPI app 발견: {type(app)}")
        print(f"   제목: {app.title}")
        print(f"   버전: {app.version}")
    else:
        print("[ERROR] FastAPI app을 찾을 수 없습니다!")
        sys.exit(1)
    
    print()
    print("[5단계] Uvicorn 확인...")
    import uvicorn
    print("[OK] Uvicorn 사용 가능")
    print()
    
    print("=" * 60)
    print("[성공] 모든 테스트 통과!")
    print("=" * 60)
    print()
    print("API 서버를 시작할 수 있습니다.")
    print("다음 명령어로 서버를 시작하세요:")
    print("  python start_api_simple.py")
    print()
    
except ImportError as e:
    print(f"[ERROR] 모듈 import 실패: {e}")
    print()
    print("필요한 패키지를 설치하세요:")
    print("  pip install fastapi uvicorn[standard]")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
except Exception as e:
    print(f"[ERROR] 오류 발생: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)

