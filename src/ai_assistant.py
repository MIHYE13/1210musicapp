"""
AI Assistant Module
Uses ChatGPT API to provide intelligent music education assistance
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

from typing import Optional, List, Dict
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
        # Try loading from current directory as fallback
        load_dotenv()
except ImportError:
    pass
except Exception:
    pass

class AIAssistant:
    """AI Assistant using OpenAI API"""
    
    def __init__(self):
        """Initialize AI Assistant"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history: List[Dict[str, str]] = []  # 대화 기록 저장
        if not self.api_key:
            if HAS_STREAMLIT and st:
                st.warning("OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 추가하세요.")
            else:
                print("OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 추가하세요.")
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
    
    def chat(self, message: str, context: Optional[str] = None) -> Optional[str]:
        """
        Chat with AI assistant
        
        Args:
            message: User message
            context: Optional context
            
        Returns:
            AI response or None
        """
        if not self.api_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            messages = [
                {"role": "system", "content": "당신은 초등학교 음악 교육 전문가입니다. 학생과 교사를 도와주세요."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"현재 상황: {context}"})
            
            messages.append({"role": "user", "content": message})
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.error(f"AI 응답 오류: {str(e)}")
            else:
                print(f"AI 응답 오류: {str(e)}")
            return None
    
    def explain_theory(self, concept: str) -> Optional[str]:
        """
        Explain music theory concept
        
        Args:
            concept: Music theory concept to explain
            
        Returns:
            Explanation or None
        """
        if not self.api_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""
            초등학생이 이해할 수 있도록 다음 음악 이론 개념을 설명해주세요:
            {concept}
            
            설명은 다음을 포함해야 합니다:
            1. 간단한 정의
            2. 구체적인 예시
            3. 실용적인 활용 방법
            
            설명은 친근하고 이해하기 쉬운 언어로 작성해주세요.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.error(f"이론 설명 오류: {str(e)}")
            else:
                print(f"이론 설명 오류: {str(e)}")
            return None
    
    def generate_lesson_plan(self, topic: str, grade: int = 3) -> Optional[Dict]:
        """
        Generate lesson plan for music education
        
        Args:
            topic: Lesson topic
            grade: Grade level (1-6)
            
        Returns:
            Lesson plan dictionary or None
        """
        if not self.api_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""
            {grade}학년 초등학생을 위한 음악 수업 계획안을 작성해주세요.
            
            주제: {topic}
            
            수업 계획안은 다음을 포함해야 합니다:
            1. 수업 목표
            2. 준비물
            3. 수업 진행 단계 (도입, 전개, 정리)
            4. 평가 방법
            
            JSON 형식으로 응답해주세요.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON
            try:
                return json.loads(content)
            except:
                return {"plan": content}
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.error(f"수업 계획 생성 오류: {str(e)}")
            else:
                print(f"수업 계획 생성 오류: {str(e)}")
            return None
