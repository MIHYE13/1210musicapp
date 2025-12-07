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
        # Fallback: try current directory
        load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars only
except Exception:
    pass  # Failed to load .env, use system env vars only

class AIAssistant:
    """ChatGPT-powered music education assistant"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI assistant
        
        Args:
            api_key: OpenAI API key (optional, can use st.secrets)
        """
        self.api_key = api_key or self._get_api_key()
        self.conversation_history = []
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from multiple sources (priority order)"""
        # 1. Try Streamlit secrets (for cloud deployment)
        if HAS_STREAMLIT and st:
            try:
                key = st.secrets.get("OPENAI_API_KEY")
                if key:
                    return key
            except:
                pass
        
        # 2. Try environment variable (from .env file or system)
        key = os.getenv("OPENAI_API_KEY")
        if key:
            return key
        
        # 3. No key found
        return None
    
    def analyze_score(self, score_info: Dict) -> str:
        """
        Analyze a musical score and provide educational insights
        
        Args:
            score_info: Dictionary with score information (key, tempo, duration, etc.)
            
        Returns:
            AI-generated analysis and teaching suggestions
        """
        if not self.api_key:
            return self._fallback_analysis(score_info)
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""당신은 초등학교 음악 교사입니다. 다음 악보 정보를 분석하고 교육적 조언을 제공해주세요:

조성: {score_info.get('key', 'C major')}
템포: {score_info.get('tempo', 120)} BPM
음표 수: {score_info.get('notes', 0)}개
길이: {score_info.get('duration', 0)}박자

다음 내용을 포함해서 짧고 명확하게 답변해주세요:
1. 이 곡의 난이도 (초등 저/중/고학년)
2. 주요 학습 포인트 2-3가지
3. 연습 방법 제안
4. 주의할 점

답변은 존댓말로, 200자 이내로 작성해주세요."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 친절한 초등학교 음악 교사입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.warning(f"AI 분석 오류: {str(e)}")
            return self._fallback_analysis(score_info)
    
    def suggest_practice_method(self, difficulty: str, student_level: str) -> str:
        """
        Suggest practice methods based on difficulty and student level
        
        Args:
            difficulty: Song difficulty (easy, medium, hard)
            student_level: Student level (low, mid, high grade)
            
        Returns:
            AI-generated practice suggestions
        """
        if not self.api_key:
            return self._fallback_practice_suggestion(difficulty, student_level)
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""초등학교 {student_level} 학생이 {difficulty} 난이도의 곡을 연습하려고 합니다.
효과적인 연습 방법을 3단계로 제안해주세요. 각 단계는 한 문장으로 간단하게.

예시:
1단계: 리듬부터 손뼉으로 쳐보기
2단계: 계이름으로 천천히 노래 부르기
3단계: 악기로 연주하며 완성하기"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 초등학생을 위한 음악 연습 코치입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._fallback_practice_suggestion(difficulty, student_level)
    
    def explain_music_theory(self, topic: str, student_age: int = 10) -> str:
        """
        Explain music theory concepts in age-appropriate language
        
        Args:
            topic: Music theory topic to explain
            student_age: Student's age for appropriate explanation
            
        Returns:
            AI-generated explanation
        """
        if not self.api_key:
            return self._fallback_theory_explanation(topic)
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""{student_age}살 초등학생에게 '{topic}'에 대해 쉽게 설명해주세요.

요구사항:
- 쉬운 단어 사용
- 실생활 예시 포함
- 3-4문장으로 간단하게
- 재미있고 이해하기 쉽게"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 어린이에게 음악을 가르치는 선생님입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._fallback_theory_explanation(topic)
    
    def generate_lesson_plan(self, song_title: str, grade_level: str, 
                           duration_minutes: int = 40) -> str:
        """
        Generate a lesson plan for teaching a song
        
        Args:
            song_title: Title of the song
            grade_level: Student grade level
            duration_minutes: Lesson duration in minutes
            
        Returns:
            AI-generated lesson plan
        """
        if not self.api_key:
            return self._fallback_lesson_plan(song_title, grade_level, duration_minutes)
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""초등학교 {grade_level} 학생들을 대상으로 '{song_title}'를 가르치는 {duration_minutes}분 수업 계획을 작성해주세요.

다음 형식으로 작성:
도입 (5분): [활동 설명]
전개 (25분): [단계별 활동]
정리 (10분): [마무리 활동]

각 부분은 2-3문장으로 간단하게 작성해주세요."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 경험 많은 초등학교 음악 교사입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self._fallback_lesson_plan(song_title, grade_level, duration_minutes)
    
    def chat(self, user_message: str, context: Optional[str] = None) -> str:
        """
        General chat interface with AI assistant
        
        Args:
            user_message: User's question or message
            context: Optional context about current score/activity
            
        Returns:
            AI response
        """
        if not self.api_key:
            return "죄송합니다. AI 채팅 기능을 사용하려면 OpenAI API 키가 필요합니다."
        
        try:
            import openai
            openai.api_key = self.api_key
            
            # Build conversation with context
            messages = [
                {"role": "system", "content": "당신은 초등학교 음악 교육 전문가입니다. 학생과 교사를 도와주세요."}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"현재 상황: {context}"})
            
            # Add conversation history (last 5 messages)
            messages.extend(self.conversation_history[-5:])
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=500,
                temperature=0.8
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"죄송합니다. 오류가 발생했습니다: {str(e)}"
    
    def improve_chord_progression(self, current_progression: List[str]) -> Dict:
        """
        Suggest improvements to chord progression
        
        Args:
            current_progression: Current chord progression (e.g., ['I', 'V', 'vi', 'IV'])
            
        Returns:
            Dictionary with improved progression and explanation
        """
        if not self.api_key:
            return self._fallback_chord_improvement(current_progression)
        
        try:
            import openai
            openai.api_key = self.api_key
            
            progression_str = " → ".join(current_progression)
            
            prompt = f"""현재 화음 진행: {progression_str}

초등학생이 연주하기 좋은 더 나은 화음 진행을 제안해주세요.
I, IV, V, vi 중에서만 사용하고, 다음 형식으로 답변:

개선된 진행: [화음들]
설명: [한 문장으로 왜 더 좋은지]"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 음악 이론 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            
            return {
                "suggestion": result,
                "original": progression_str
            }
            
        except Exception as e:
            return self._fallback_chord_improvement(current_progression)
    
    # Fallback methods when API is not available
    
    def _fallback_analysis(self, score_info: Dict) -> str:
        """Provide basic analysis without AI"""
        notes = score_info.get('notes', 0)
        
        if notes < 20:
            difficulty = "초등 저학년"
        elif notes < 40:
            difficulty = "초등 중학년"
        else:
            difficulty = "초등 고학년"
        
        return f"""**난이도**: {difficulty}

**학습 포인트**:
- 박자를 정확하게 지키며 연주하기
- 계이름을 보면서 음정 익히기

**연습 방법**:
1. 손뼉으로 리듬 먼저 연습
2. 계이름으로 노래 불러보기
3. 천천히 악기로 연주하기

💡 AI 분석 기능을 사용하려면 OpenAI API 키를 설정하세요."""
    
    def _fallback_practice_suggestion(self, difficulty: str, student_level: str) -> str:
        """Provide basic practice suggestion without AI"""
        return """**연습 방법 3단계**:

1단계: 리듬 익히기 - 손뼉을 치며 박자를 익혀보세요
2단계: 계이름 노래 - 악보를 보며 계이름으로 천천히 노래하세요  
3단계: 악기 연주 - 배운 리듬과 음정으로 악기를 연주하세요

💡 더 자세한 맞춤 조언은 AI 기능을 활성화하세요."""
    
    def _fallback_theory_explanation(self, topic: str) -> str:
        """Provide basic theory explanation without AI"""
        explanations = {
            "계이름": "도, 레, 미, 파, 솔, 라, 시는 음악의 음높이를 나타내는 이름이에요. 계단처럼 하나씩 올라간다고 해서 '계이름'이라고 불러요!",
            "박자": "박자는 음악의 속도감을 만드는 규칙적인 박동이에요. 시계의 똑딱똑딱 소리처럼 일정하게 반복되죠.",
            "화음": "화음은 여러 음을 동시에 내는 것이에요. 혼자 노래하는 것보다 친구들과 같이 부르면 더 풍성하게 들리는 것처럼요!"
        }
        
        return explanations.get(topic, f"{topic}에 대해 더 자세히 알고 싶으시면 AI 기능을 활성화해주세요.")
    
    def _fallback_lesson_plan(self, song_title: str, grade_level: str, 
                             duration_minutes: int) -> str:
        """Provide basic lesson plan without AI"""
        return f"""**'{song_title}' 수업 계획 ({duration_minutes}분)**

**도입 (5분)**
- 노래 감상 및 느낌 이야기하기
- 박자 맞추며 손뼉 치기

**전개 (30분)**
- 계이름 익히기 (10분)
- 리듬 연습 (10분)  
- 악기로 연주하기 (10분)

**정리 (5분)**
- 오늘 배운 내용 복습
- 다음 시간 예고

💡 더 상세한 맞춤 수업 계획은 AI 기능을 활성화하세요."""
    
    def _fallback_chord_improvement(self, current_progression: List[str]) -> Dict:
        """Provide basic chord improvement without AI"""
        progression_str = " → ".join(current_progression)
        
        return {
            "suggestion": f"현재 진행: {progression_str}\n\n기본적으로 I → IV → V → I 진행이 초등학생에게 가장 배우기 쉽습니다.",
            "original": progression_str
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_api_status(self) -> Dict:
        """Get API key status"""
        return {
            "has_key": self.api_key is not None,
            "key_length": len(self.api_key) if self.api_key else 0,
            "conversation_length": len(self.conversation_history)
        }
