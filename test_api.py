"""
API 서버 테스트 스크립트
"""

import requests
import json

BASE_URL = "http://localhost:8501"

def test_health():
    """헬스 체크 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"✅ 헬스 체크: {response.status_code}")
        print(f"   응답: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ 헬스 체크 실패: {e}")
        return False

def test_api_keys_status():
    """API 키 상태 확인"""
    try:
        response = requests.get(f"{BASE_URL}/api/keys/status", timeout=5)
        print(f"\n✅ API 키 상태: {response.status_code}")
        data = response.json()
        for status in data.get('statuses', []):
            icon = "✅" if status['status'] == 'valid' else "❌"
            print(f"   {icon} {status['name']}: {status['message']}")
        return True
    except Exception as e:
        print(f"❌ API 키 상태 확인 실패: {e}")
        return False

def test_ai_chat():
    """AI 채팅 테스트"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/chat",
            json={"question": "계이름이 뭐예요?", "context": None},
            timeout=30
        )
        print(f"\n✅ AI 채팅 테스트: {response.status_code}")
        data = response.json()
        if data.get('success'):
            print(f"   응답: {data.get('response', '')[:100]}...")
        else:
            print(f"   오류: {data.get('error', 'Unknown error')}")
        return data.get('success', False)
    except Exception as e:
        print(f"❌ AI 채팅 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API 서버 테스트")
    print("=" * 60)
    print()
    
    health_ok = test_health()
    keys_ok = test_api_keys_status()
    
    if health_ok and keys_ok:
        print("\n🔄 AI 채팅 테스트 실행 중...")
        ai_ok = test_ai_chat()
        
        print("\n" + "=" * 60)
        print("📊 테스트 결과")
        print("=" * 60)
        print(f"헬스 체크: {'✅' if health_ok else '❌'}")
        print(f"API 키 상태: {'✅' if keys_ok else '❌'}")
        print(f"AI 채팅: {'✅' if ai_ok else '❌'}")
    else:
        print("\n⚠️  API 서버가 실행 중이지 않거나 연결할 수 없습니다.")
        print("   python start_api_server.py 명령으로 서버를 시작하세요.")

