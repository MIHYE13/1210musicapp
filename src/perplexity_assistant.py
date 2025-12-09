"""
Perplexity AI Assistant Module
Uses Perplexity API for web-based music education research and latest information
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

from typing import Optional, Dict, List
import requests
import json
import os
from pathlib import Path

# Load environment variables from .env file in project root
try:
    from dotenv import load_dotenv
    # Find project root (parent of src directory)
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Fallback: try current directory
        load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars only
except Exception:
    pass  # Failed to load .env, use system env vars only

class PerplexityAssistant:
    """Perplexity AI for real-time music education research"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Perplexity assistant
        
        Args:
            api_key: Perplexity API key (optional, can use st.secrets)
        """
        self.api_key = api_key or self._get_api_key()
        self.base_url = "https://api.perplexity.ai/chat/completions"
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from multiple sources (priority order)"""
        # 1. Try Streamlit secrets (for cloud deployment)
        if HAS_STREAMLIT and st:
            try:
                key = st.secrets.get("PERPLEXITY_API_KEY")
                if key:
                    return key
            except:
                pass
        
        # 2. Try environment variable (from .env file or system)
        key = os.getenv("PERPLEXITY_API_KEY")
        if key:
            return key
        
        # 3. No key found
        return None
    
    def search_music_theory(self, topic: str, depth: str = "basic") -> str:
        """
        Search for music theory information with latest sources
        
        Args:
            topic: Music theory topic to research
            depth: Level of depth (basic, intermediate, advanced)
            
        Returns:
            Research results with sources
        """
        if not self.api_key:
            return self._fallback_theory_search(topic)
        
        try:
            prompt = f"""음악 이론 주제 '{topic}'에 대해 초등학교 음악 교육에 적합한 정보를 찾아주세요.

난이도: {depth}
포함 내용:
1. 기본 개념 설명
2. 실제 교육 사례
3. 최신 교수법
4. 참고 자료

초등학생과 교사가 이해하기 쉽게 정리해주세요."""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {
                            "role": "system",
                            "content": "당신은 초등학교 음악 교육 전문가입니다. 최신 정보와 신뢰할 수 있는 출처를 기반으로 답변합니다."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 응답 구조 확인
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    
                    # Extract sources if available
                    citations = result.get('citations', [])
                    if citations:
                        content += "\n\n**참고 자료:**\n"
                        for i, citation in enumerate(citations[:3], 1):
                            content += f"{i}. {citation}\n"
                    
                    return content
                else:
                    # 응답 구조가 예상과 다른 경우
                    error_msg = f"Perplexity API 응답 형식 오류: {result}"
                    print(f"[WARN] {error_msg}")
                    return self._fallback_theory_search(topic)
            else:
                # HTTP 오류 응답 처리
                error_text = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('error', {}).get('message', error_text)
                except:
                    error_msg = error_text
                
                print(f"[ERROR] Perplexity API 오류 (HTTP {response.status_code}): {error_msg}")
                return self._fallback_theory_search(topic)
                
        except requests.exceptions.Timeout:
            error_msg = "Perplexity API 요청 시간이 초과되었습니다. 네트워크 연결을 확인하세요."
            if HAS_STREAMLIT and st:
                st.warning(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            return self._fallback_theory_search(topic)
        except requests.exceptions.RequestException as e:
            error_msg = f"Perplexity API 네트워크 오류: {str(e)}"
            if HAS_STREAMLIT and st:
                st.warning(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            return self._fallback_theory_search(topic)
        except Exception as e:
            error_msg = f"Perplexity 검색 오류: {str(e)}"
            if HAS_STREAMLIT and st:
                st.warning(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            import traceback
            print(traceback.format_exc())
            return self._fallback_theory_search(topic)
    
    def research_song_background(self, song_title: str) -> str:
        """
        Research background information about a song
        
        Args:
            song_title: Title of the song
            
        Returns:
            Song background information
        """
        if not self.api_key:
            return self._fallback_song_background(song_title)
        
        try:
            prompt = f"""'{song_title}' 곡에 대한 배경 정보를 초등학교 음악 수업용으로 조사해주세요:

포함 내용:
1. 곡의 작곡가와 시대
2. 곡의 의미와 배경
3. 교육적 활용 방안
4. 재미있는 사실

초등학생이 흥미를 가질 수 있게 작성해주세요."""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": "음악 교육 전문가로서 정확하고 흥미로운 정보를 제공합니다."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 800
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    print(f"[WARN] Perplexity API 응답 형식 오류: {result}")
                    return self._fallback_song_background(song_title)
            else:
                error_text = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('error', {}).get('message', error_text)
                except:
                    error_msg = error_text
                print(f"[ERROR] Perplexity API 오류 (HTTP {response.status_code}): {error_msg}")
                return self._fallback_song_background(song_title)
                
        except requests.exceptions.Timeout:
            print("[ERROR] Perplexity API 요청 시간 초과")
            return self._fallback_song_background(song_title)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Perplexity API 네트워크 오류: {str(e)}")
            return self._fallback_song_background(song_title)
        except Exception as e:
            print(f"[ERROR] Perplexity 검색 오류: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return self._fallback_song_background(song_title)
    
    def find_teaching_resources(self, topic: str, grade_level: str) -> str:
        """
        Find latest teaching resources and materials
        
        Args:
            topic: Teaching topic
            grade_level: Student grade level
            
        Returns:
            Teaching resource recommendations
        """
        if not self.api_key:
            return self._fallback_teaching_resources(topic, grade_level)
        
        try:
            prompt = f"""초등학교 {grade_level} 학생을 위한 '{topic}' 교육 자료를 추천해주세요:

포함 내용:
1. 최신 교육 자료 (웹사이트, 앱 등)
2. 무료 리소스
3. 활용 방법
4. 주의사항

실제로 사용 가능한 최신 자료 위주로 추천해주세요."""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": "교육 자료 전문가로서 최신 정보를 제공합니다."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    
                    # Add citations
                    citations = result.get('citations', [])
                    if citations:
                        content += "\n\n**추천 링크:**\n"
                        for i, citation in enumerate(citations[:5], 1):
                            content += f"{i}. {citation}\n"
                    
                    return content
                else:
                    print(f"[WARN] Perplexity API 응답 형식 오류: {result}")
                    return self._fallback_teaching_resources(topic, grade_level)
            else:
                error_text = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('error', {}).get('message', error_text)
                except:
                    error_msg = error_text
                print(f"[ERROR] Perplexity API 오류 (HTTP {response.status_code}): {error_msg}")
                return self._fallback_teaching_resources(topic, grade_level)
                
        except requests.exceptions.Timeout:
            print("[ERROR] Perplexity API 요청 시간 초과")
            return self._fallback_teaching_resources(topic, grade_level)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Perplexity API 네트워크 오류: {str(e)}")
            return self._fallback_teaching_resources(topic, grade_level)
        except Exception as e:
            print(f"[ERROR] Perplexity 검색 오류: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return self._fallback_teaching_resources(topic, grade_level)
    
    def get_latest_education_trends(self, area: str = "초등 음악 교육") -> str:
        """
        Get latest education trends and research
        
        Args:
            area: Education area to research
            
        Returns:
            Latest trends and research findings
        """
        if not self.api_key:
            return "Perplexity API 키를 설정하면 최신 교육 트렌드를 확인할 수 있습니다."
        
        try:
            prompt = f"""{area} 분야의 최신 트렌드와 연구 결과를 요약해주세요:

포함 내용:
1. 최근 1년 내 주요 트렌드
2. 혁신적인 교수법
3. 기술 활용 사례
4. 전문가 의견

한국 교육 현장에 적용 가능한 내용 위주로 작성해주세요."""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": "교육 트렌드 분석 전문가입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    print(f"[WARN] Perplexity API 응답 형식 오류: {result}")
                    return "최신 트렌드 정보를 가져오는데 실패했습니다."
            else:
                error_text = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('error', {}).get('message', error_text)
                except:
                    error_msg = error_text
                print(f"[ERROR] Perplexity API 오류 (HTTP {response.status_code}): {error_msg}")
                return f"최신 트렌드 정보를 가져오는데 실패했습니다: {error_msg}"
                
        except requests.exceptions.Timeout:
            return "요청 시간이 초과되었습니다. 네트워크 연결을 확인하세요."
        except requests.exceptions.RequestException as e:
            return f"네트워크 오류가 발생했습니다: {str(e)}"
        except Exception as e:
            print(f"[ERROR] Perplexity 검색 오류: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return f"오류가 발생했습니다: {str(e)}"
    
    def compare_teaching_methods(self, method1: str, method2: str) -> str:
        """
        Compare different teaching methods with research
        
        Args:
            method1: First teaching method
            method2: Second teaching method
            
        Returns:
            Comparison with research-backed information
        """
        if not self.api_key:
            return "Perplexity API 키를 설정하면 교수법 비교 분석이 가능합니다."
        
        try:
            prompt = f"""초등 음악 교육에서 '{method1}'와 '{method2}' 교수법을 비교 분석해주세요:

비교 항목:
1. 각 방법의 특징
2. 장단점
3. 적용 대상
4. 효과성 연구 결과
5. 실제 적용 사례

객관적이고 연구 기반 정보로 작성해주세요."""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": "음악 교육 연구자로서 객관적 분석을 제공합니다."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1200
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    print(f"[WARN] Perplexity API 응답 형식 오류: {result}")
                    return "교수법 비교 정보를 가져오는데 실패했습니다."
            else:
                error_text = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('error', {}).get('message', error_text)
                except:
                    error_msg = error_text
                print(f"[ERROR] Perplexity API 오류 (HTTP {response.status_code}): {error_msg}")
                return f"교수법 비교 정보를 가져오는데 실패했습니다: {error_msg}"
                
        except requests.exceptions.Timeout:
            return "요청 시간이 초과되었습니다. 네트워크 연결을 확인하세요."
        except requests.exceptions.RequestException as e:
            return f"네트워크 오류가 발생했습니다: {str(e)}"
        except Exception as e:
            print(f"[ERROR] Perplexity 검색 오류: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return f"오류가 발생했습니다: {str(e)}"
    
    # Fallback methods
    
    def _fallback_theory_search(self, topic: str) -> str:
        """Basic theory information without API"""
        return f"""**{topic}** 기본 정보

Perplexity API를 설정하면 최신 연구 자료와 교육 사례를 포함한 
상세한 정보를 제공받을 수 있습니다.

기본 설명:
- {topic}는 음악의 기초 이론 중 하나입니다
- 초등학교 음악 교육에서 중요한 개념입니다
- 실제 곡을 통해 배우면 더 효과적입니다

💡 API를 설정하여 더 자세한 정보를 확인하세요."""
    
    def _fallback_song_background(self, song_title: str) -> str:
        """Basic song information without API"""
        return f"""**'{song_title}' 곡 정보**

Perplexity API를 설정하면 곡의 배경, 작곡가 정보, 
교육적 활용 방안 등 상세한 정보를 제공받을 수 있습니다.

💡 API를 설정하여 더 자세한 곡 정보를 확인하세요."""
    
    def _fallback_teaching_resources(self, topic: str, grade_level: str) -> str:
        """Basic resource suggestions without API"""
        return f"""**{topic} 교육 자료 ({grade_level})**

기본 추천:
1. 유튜브 교육 채널
2. 음악 교육 관련 블로그
3. 무료 악보 사이트

💡 Perplexity API를 설정하면 최신 교육 자료와 
   실제 링크를 포함한 맞춤 추천을 받을 수 있습니다."""
    
    def get_api_status(self) -> Dict:
        """Get API status"""
        return {
            "has_key": self.api_key is not None,
            "key_length": len(self.api_key) if self.api_key else 0,
            "service": "Perplexity AI"
        }
