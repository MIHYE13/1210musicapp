"""
API 키 검증 스크립트
모든 API 키의 설정 상태와 유효성을 확인합니다.
"""

import os
import sys
from pathlib import Path

# .env 파일 로드 시도
try:
    from dotenv import load_dotenv
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ .env 파일을 찾았습니다.\n")
    else:
        print("⚠️  .env 파일을 찾을 수 없습니다.\n")
except ImportError:
    print("⚠️  python-dotenv가 설치되지 않았습니다. 환경 변수만 확인합니다.\n")

def check_openai_key():
    """OpenAI API 키 확인"""
    print("=" * 60)
    print("🤖 OpenAI API 키 확인")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
        print("   환경 변수 또는 .env 파일에 OPENAI_API_KEY를 추가하세요.")
        return False
    
    # API 키 형식 검증 (sk-로 시작하는지 확인)
    if not api_key.startswith("sk-"):
        print(f"⚠️  API 키 형식이 올바르지 않을 수 있습니다: {api_key[:10]}...")
        print("   OpenAI API 키는 보통 'sk-'로 시작합니다.")
    else:
        print(f"✅ API 키가 설정되어 있습니다: {api_key[:10]}...")
    
    # 실제 API 호출 테스트
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        # 간단한 테스트 요청
        print("\n🔄 API 연결 테스트 중...")
        response = client.models.list()
        print("✅ OpenAI API 연결 성공!")
        print(f"   사용 가능한 모델 수: {len(response.data)}")
        return True
    except ImportError:
        print("⚠️  openai 라이브러리가 설치되지 않았습니다.")
        print("   pip install openai 명령으로 설치하세요.")
        return False
    except Exception as e:
        print(f"❌ API 연결 실패: {str(e)}")
        if "Incorrect API key" in str(e) or "Invalid API key" in str(e):
            print("   API 키가 유효하지 않습니다. 올바른 키를 입력하세요.")
        elif "Rate limit" in str(e):
            print("   ⚠️  Rate limit에 도달했습니다. 잠시 후 다시 시도하세요.")
        else:
            print("   네트워크 오류일 수 있습니다. 인터넷 연결을 확인하세요.")
        return False

def check_perplexity_key():
    """Perplexity API 키 확인"""
    print("\n" + "=" * 60)
    print("🔍 Perplexity API 키 확인")
    print("=" * 60)
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        print("❌ PERPLEXITY_API_KEY가 설정되지 않았습니다.")
        print("   환경 변수 또는 .env 파일에 PERPLEXITY_API_KEY를 추가하세요.")
        return False
    
    # API 키 형식 검증
    if not api_key.startswith("pplx-"):
        print(f"⚠️  API 키 형식이 올바르지 않을 수 있습니다: {api_key[:10]}...")
        print("   Perplexity API 키는 보통 'pplx-'로 시작합니다.")
    else:
        print(f"✅ API 키가 설정되어 있습니다: {api_key[:10]}...")
    
    # 실제 API 호출 테스트
    try:
        import requests
        print("\n🔄 API 연결 테스트 중...")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 여러 모델 이름 시도
        models_to_try = [
            "llama-3.1-sonar-large-128k-online",
            "llama-3.1-sonar-small-128k-online",
            "sonar",
            "llama-3.1-sonar-large-128k-chat",
        ]
        
        for model in models_to_try:
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": "test"
                    }
                ]
            }
            
            try:
                response = requests.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"✅ Perplexity API 연결 성공! (모델: {model})")
                    return True
                elif response.status_code == 401:
                    print("❌ API 키가 유효하지 않습니다.")
                    return False
                elif response.status_code == 400:
                    # 모델 이름 오류, 다음 모델 시도
                    continue
            except Exception as e:
                continue
        
        print(f"⚠️  사용 가능한 모델을 찾을 수 없습니다.")
        print(f"   Perplexity API 문서를 확인하세요: https://docs.perplexity.ai/getting-started/models")
        print(f"   API 키는 유효하지만 모델 이름을 확인해야 합니다.")
        return False
    except ImportError:
        print("⚠️  requests 라이브러리가 설치되지 않았습니다.")
        print("   pip install requests 명령으로 설치하세요.")
        return False
    except Exception as e:
        print(f"❌ API 연결 실패: {str(e)}")
        return False

def check_youtube_key():
    """YouTube API 키 확인"""
    print("\n" + "=" * 60)
    print("📺 YouTube API 키 확인")
    print("=" * 60)
    
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key:
        print("❌ YOUTUBE_API_KEY가 설정되지 않았습니다.")
        print("   환경 변수 또는 .env 파일에 YOUTUBE_API_KEY를 추가하세요.")
        return False
    
    # API 키 형식 검증
    if not api_key.startswith("AIza"):
        print(f"⚠️  API 키 형식이 올바르지 않을 수 있습니다: {api_key[:10]}...")
        print("   YouTube API 키는 보통 'AIza'로 시작합니다.")
    else:
        print(f"✅ API 키가 설정되어 있습니다: {api_key[:10]}...")
    
    # 실제 API 호출 테스트
    try:
        import requests
        print("\n🔄 API 연결 테스트 중...")
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": api_key,
            "part": "snippet",
            "q": "test",
            "maxResults": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ YouTube API 연결 성공!")
            data = response.json()
            if "items" in data:
                print(f"   테스트 검색 결과: {len(data['items'])}개")
            return True
        elif response.status_code == 403:
            print("❌ API 키가 유효하지 않거나 권한이 없습니다.")
            print("   YouTube Data API v3가 활성화되어 있는지 확인하세요.")
            return False
        elif response.status_code == 400:
            print("❌ API 요청이 잘못되었습니다.")
            print(f"   응답: {response.text[:200]}")
            return False
        else:
            print(f"⚠️  API 응답 오류: {response.status_code}")
            return False
    except ImportError:
        print("⚠️  requests 라이브러리가 설치되지 않았습니다.")
        print("   pip install requests 명령으로 설치하세요.")
        return False
    except Exception as e:
        print(f"❌ API 연결 실패: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("🔐 API 키 검증 도구")
    print("=" * 60)
    print()
    
    results = {
        "OpenAI": False,
        "Perplexity": False,
        "YouTube": False
    }
    
    # 각 API 키 확인
    results["OpenAI"] = check_openai_key()
    results["Perplexity"] = check_perplexity_key()
    results["YouTube"] = check_youtube_key()
    
    # 요약
    print("\n" + "=" * 60)
    print("📊 검증 결과 요약")
    print("=" * 60)
    
    for service, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service}: {'정상' if status else '설정 필요'}")
    
    print("\n" + "=" * 60)
    print("💡 팁")
    print("=" * 60)
    print("1. .env 파일을 프로젝트 루트에 생성하세요.")
    print("2. 다음 형식으로 API 키를 입력하세요:")
    print("   OPENAI_API_KEY=sk-your-key-here")
    print("   PERPLEXITY_API_KEY=pplx-your-key-here")
    print("   YOUTUBE_API_KEY=AIza-your-key-here")
    print("3. API 키 발급 방법은 docs/api_setup.md를 참조하세요.")
    print()

if __name__ == "__main__":
    main()

