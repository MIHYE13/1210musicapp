"""
초등 음악 도우미 웹앱
Main Streamlit Application
"""

import streamlit as st
from pathlib import Path
import sys

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from audio_processor import AudioProcessor
from score_processor import ScoreProcessor
from chord_generator import ChordGenerator
from player import MusicPlayer
from ai_assistant import AIAssistant
from perplexity_assistant import PerplexityAssistant
from youtube_helper import YouTubeHelper

# Page configuration
st.set_page_config(
    page_title="초등 음악 도우미",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #f0f2f6;
        border-radius: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'audio_processor' not in st.session_state:
    st.session_state.audio_processor = AudioProcessor()
if 'score_processor' not in st.session_state:
    st.session_state.score_processor = ScoreProcessor()
if 'chord_generator' not in st.session_state:
    st.session_state.chord_generator = ChordGenerator()
if 'music_player' not in st.session_state:
    st.session_state.music_player = MusicPlayer()
if 'ai_assistant' not in st.session_state:
    st.session_state.ai_assistant = AIAssistant()
if 'perplexity' not in st.session_state:
    st.session_state.perplexity = PerplexityAssistant()
if 'youtube' not in st.session_state:
    st.session_state.youtube = YouTubeHelper()

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🎵 초등 음악 도우미</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p>오디오나 악보를 업로드하면 초등학생이 배우기 쉬운 형태로 변환해드립니다!</p>
        <p><strong>계이름 기재 · 다장조 변환 · 반주 추가 · 자동 재생</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard link
    st.info("👨‍🏫 **교사이신가요?** 왼쪽 사이드바에서 '교사 대시보드'를 선택하여 학급과 학생을 관리하세요!")
    
    # Create two columns for different input types
    col1, col2 = st.columns(2)
    
    # Left column: Audio to Score
    with col1:
        st.markdown('<div class="section-header">🎤 오디오 → 악보 변환</div>', unsafe_allow_html=True)
        
        audio_file = st.file_uploader(
            "오디오 파일 업로드",
            type=['mp3', 'wav'],
            key="audio_upload",
            help="MP3 또는 WAV 파일을 업로드하세요. 멜로디를 자동으로 추출합니다."
        )
        
        if audio_file:
            st.audio(audio_file, format=f'audio/{audio_file.name.split(".")[-1]}')
            
            col_a1, col_a2 = st.columns([2, 1])
            with col_a1:
                if st.button("🎼 악보 생성하기", key="generate_score"):
                    with st.spinner("멜로디를 추출하고 악보를 생성하는 중..."):
                        try:
                            # Process audio to score
                            score = st.session_state.audio_processor.process_audio(audio_file)
                            
                            if score:
                                st.session_state['generated_score'] = score
                                st.success("✅ 악보가 생성되었습니다!")
                            else:
                                st.error("악보 생성에 실패했습니다. 다른 파일을 시도해주세요.")
                        except Exception as e:
                            st.error(f"오류가 발생했습니다: {str(e)}")
        
        # Display generated score
        if 'generated_score' in st.session_state:
            st.markdown("### 📄 생성된 악보")
            score = st.session_state['generated_score']
            
            # Show score image
            try:
                score_img = st.session_state.audio_processor.render_score(score)
                if score_img:
                    st.image(score_img, use_container_width=True)
            except Exception as e:
                st.warning(f"악보 이미지 표시 실패: {str(e)}")
            
            # Option to process further
            if st.button("➡️ 오른쪽에서 계속 처리하기", key="continue_process"):
                st.session_state['score_to_process'] = score
                st.info("오른쪽 패널에서 계이름 추가, 반주 생성 등을 진행하세요!")
    
    # Right column: Score Processing
    with col2:
        st.markdown('<div class="section-header">🎼 악보 → 계이름·반주 추가</div>', unsafe_allow_html=True)
        
        score_file = st.file_uploader(
            "악보 파일 업로드",
            type=['mid', 'midi', 'xml', 'mxl', 'abc'],
            key="score_upload",
            help="MIDI, MusicXML, ABC 형식의 악보를 업로드하세요."
        )
        
        # Check if score comes from left panel or uploaded
        score_to_process = None
        if score_file:
            with st.spinner("악보를 불러오는 중..."):
                try:
                    score_to_process = st.session_state.score_processor.load_score(score_file)
                    if score_to_process:
                        st.success("✅ 악보를 불러왔습니다!")
                except Exception as e:
                    st.error(f"악보 로딩 오류: {str(e)}")
        elif 'score_to_process' in st.session_state:
            score_to_process = st.session_state['score_to_process']
            st.info("왼쪽에서 생성된 악보를 처리합니다.")
        
        if score_to_process:
            st.markdown("### ⚙️ 처리 옵션")
            
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                add_solfege = st.checkbox("계이름 추가 (도레미)", value=True)
                simplify_rhythm = st.checkbox("리듬 단순화", value=True)
            with col_opt2:
                transpose_c = st.checkbox("다장조 변환", value=True)
                add_chords = st.checkbox("반주 추가", value=True)
            
            if st.button("🎵 처리하기", key="process_score"):
                with st.spinner("악보를 처리하는 중..."):
                    try:
                        processed_score = score_to_process
                        
                        # Simplify rhythm
                        if simplify_rhythm:
                            processed_score = st.session_state.score_processor.simplify_rhythm(
                                processed_score
                            )
                        
                        # Transpose to C major
                        if transpose_c:
                            processed_score = st.session_state.score_processor.transpose_to_c_major(
                                processed_score
                            )
                        
                        # Add solfege
                        if add_solfege:
                            processed_score = st.session_state.score_processor.add_solfege(
                                processed_score
                            )
                        
                        # Generate accompaniment
                        if add_chords:
                            processed_score = st.session_state.chord_generator.add_accompaniment(
                                processed_score
                            )
                        
                        st.session_state['final_score'] = processed_score
                        st.success("✅ 처리가 완료되었습니다!")
                        
                        # AI Analysis (if enabled)
                        if st.session_state.ai_assistant.get_api_status()['has_key']:
                            with st.expander("🤖 AI 악보 분석 보기", expanded=False):
                                with st.spinner("AI가 악보를 분석하는 중..."):
                                    score_info = st.session_state.score_processor.get_score_info(processed_score)
                                    analysis = st.session_state.ai_assistant.analyze_score(score_info)
                                    st.markdown(analysis)
                        
                    except Exception as e:
                        st.error(f"처리 중 오류: {str(e)}")
            
            # Display final score
            if 'final_score' in st.session_state:
                st.markdown("### 📄 완성된 악보")
                final_score = st.session_state['final_score']
                
                try:
                    # Show score image
                    score_img = st.session_state.score_processor.render_score(final_score)
                    if score_img:
                        st.image(score_img, use_container_width=True)
                    
                    # Playback controls
                    st.markdown("### 🎹 재생")
                    col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
                    
                    with col_p1:
                        if st.button("▶️ 재생", key="play"):
                            try:
                                st.session_state.music_player.play(final_score)
                                st.info("재생 중...")
                            except Exception as e:
                                st.error(f"재생 오류: {str(e)}")
                    
                    with col_p2:
                        if st.button("⏸️ 일시정지", key="pause"):
                            st.session_state.music_player.pause()
                    
                    with col_p3:
                        if st.button("⏹️ 정지", key="stop"):
                            st.session_state.music_player.stop()
                    
                    # Download options
                    st.markdown("### 💾 다운로드")
                    col_d1, col_d2 = st.columns(2)
                    
                    with col_d1:
                        # Export as MIDI
                        midi_bytes = st.session_state.score_processor.export_midi(final_score)
                        if midi_bytes:
                            st.download_button(
                                label="🎹 MIDI 다운로드",
                                data=midi_bytes,
                                file_name="processed_score.mid",
                                mime="audio/midi"
                            )
                    
                    with col_d2:
                        # Export as MusicXML
                        xml_bytes = st.session_state.score_processor.export_musicxml(final_score)
                        if xml_bytes:
                            st.download_button(
                                label="📄 MusicXML 다운로드",
                                data=xml_bytes,
                                file_name="processed_score.xml",
                                mime="application/xml"
                            )
                
                except Exception as e:
                    st.error(f"악보 표시 오류: {str(e)}")
    
    # Footer with instructions
    st.markdown("---")
    
    # AI Assistant Section
    st.markdown('<div class="section-header">🤖 AI 음악 도우미</div>', unsafe_allow_html=True)
    
    ai_tab1, ai_tab2, ai_tab3 = st.tabs(["💬 질문하기", "📖 음악 이론", "📝 수업 계획"])
    
    # Add new section for Perplexity and YouTube
    st.markdown('<div class="section-header">🔍 최신 정보 & 영상 자료</div>', unsafe_allow_html=True)
    
    resource_tab1, resource_tab2 = st.tabs(["🌐 웹 조사 (Perplexity)", "📺 교육 영상 (YouTube)"])
    
    with ai_tab1:
        st.markdown("### 💬 AI 선생님께 질문하기")
        
        # Check API key status
        api_status = st.session_state.ai_assistant.get_api_status()
        
        if not api_status['has_key']:
            st.info("""
            🔑 **AI 기능 활성화 방법:**
            1. OpenAI API 키 발급: https://platform.openai.com/api-keys
            2. Streamlit secrets에 `OPENAI_API_KEY` 추가
            3. 또는 환경 변수로 설정
            
            API 키 없이도 기본 기능은 사용 가능합니다.
            """)
        else:
            st.success("✅ AI 기능이 활성화되었습니다!")
        
        # Context selection
        context_option = st.selectbox(
            "질문 맥락",
            ["일반 질문", "현재 악보에 대해", "연습 방법", "수업 준비"],
            help="AI가 더 정확한 답변을 제공하도록 맥락을 선택하세요"
        )
        
        # Chat input
        user_question = st.text_area(
            "질문을 입력하세요",
            placeholder="예: 이 곡을 초등학교 3학년이 배우기에 적절한가요?",
            height=100
        )
        
        col_chat1, col_chat2 = st.columns([3, 1])
        
        with col_chat1:
            if st.button("💬 질문하기", key="ask_ai"):
                if user_question.strip():
                    with st.spinner("AI가 답변을 생성하는 중..."):
                        # Build context
                        context = None
                        if 'final_score' in st.session_state and context_option == "현재 악보에 대해":
                            score_info = st.session_state.score_processor.get_score_info(
                                st.session_state['final_score']
                            )
                            context = f"현재 악보: {score_info}"
                        
                        # Get AI response
                        response = st.session_state.ai_assistant.chat(user_question, context)
                        
                        st.markdown("### 🎵 AI 답변")
                        st.markdown(response)
                else:
                    st.warning("질문을 입력해주세요.")
        
        with col_chat2:
            if st.button("🗑️ 대화 초기화", key="clear_chat"):
                st.session_state.ai_assistant.clear_history()
                st.success("대화가 초기화되었습니다!")
    
    with ai_tab2:
        st.markdown("### 📖 음악 이론 설명")
        
        col_theory1, col_theory2 = st.columns([2, 1])
        
        with col_theory1:
            theory_topic = st.selectbox(
                "알고 싶은 음악 이론",
                [
                    "계이름",
                    "박자",
                    "화음",
                    "장조와 단조",
                    "음표와 쉼표",
                    "셈여림",
                    "빠르기말",
                    "음정",
                    "리듬",
                    "직접 입력"
                ]
            )
        
        with col_theory2:
            student_age = st.number_input(
                "학생 나이",
                min_value=6,
                max_value=13,
                value=10,
                help="나이에 맞는 설명을 제공합니다"
            )
        
        if theory_topic == "직접 입력":
            custom_topic = st.text_input("설명받고 싶은 주제를 입력하세요")
            theory_topic = custom_topic if custom_topic else "음악"
        
        if st.button("📖 설명 듣기", key="explain_theory"):
            with st.spinner("AI가 설명을 준비하는 중..."):
                explanation = st.session_state.ai_assistant.explain_music_theory(
                    theory_topic, 
                    student_age
                )
                
                st.markdown(f"### 🎵 '{theory_topic}' 설명")
                st.info(explanation)
    
    with ai_tab3:
        st.markdown("### 📝 수업 계획 생성")
        
        col_lesson1, col_lesson2 = st.columns(2)
        
        with col_lesson1:
            song_title = st.text_input(
                "곡 제목",
                value="현재 악보" if 'final_score' in st.session_state else "",
                help="수업할 곡의 제목을 입력하세요"
            )
            
            grade_level = st.selectbox(
                "학년",
                ["1-2학년", "3-4학년", "5-6학년"]
            )
        
        with col_lesson2:
            lesson_duration = st.slider(
                "수업 시간 (분)",
                min_value=20,
                max_value=60,
                value=40,
                step=5
            )
        
        if st.button("📝 수업 계획 생성", key="generate_lesson"):
            if song_title.strip():
                with st.spinner("AI가 수업 계획을 작성하는 중..."):
                    lesson_plan = st.session_state.ai_assistant.generate_lesson_plan(
                        song_title,
                        grade_level,
                        lesson_duration
                    )
                    
                    st.markdown("### 📋 생성된 수업 계획")
                    st.markdown(lesson_plan)
                    
                    # Download button
                    st.download_button(
                        label="💾 수업 계획 다운로드",
                        data=lesson_plan,
                        file_name=f"lesson_plan_{song_title}.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("곡 제목을 입력해주세요.")
    
    # Perplexity and YouTube resource tabs
    with resource_tab1:
        st.markdown("### 🌐 최신 음악 교육 정보 조사 (Perplexity)")
        
        perplexity_status = st.session_state.perplexity.get_api_status()
        
        if not perplexity_status['has_key']:
            st.info("""
            🔑 **Perplexity API 활성화 방법:**
            1. Perplexity API 키 발급: https://www.perplexity.ai/settings/api
            2. Streamlit secrets에 `PERPLEXITY_API_KEY` 추가
            
            최신 음악 교육 연구, 곡 배경 정보, 교육 자료 등을 실시간으로 조사할 수 있습니다.
            """)
        else:
            st.success("✅ Perplexity 기능이 활성화되었습니다!")
        
        search_type = st.selectbox(
            "조사 유형",
            ["음악 이론 조사", "곡 배경 정보", "교육 자료 찾기", "최신 트렌드", "교수법 비교"]
        )
        
        if search_type == "음악 이론 조사":
            col_p1, col_p2 = st.columns([3, 1])
            
            with col_p1:
                theory_query = st.text_input(
                    "조사할 음악 이론 주제",
                    placeholder="예: 3화음의 구성과 활용"
                )
            
            with col_p2:
                depth = st.selectbox("깊이", ["basic", "intermediate", "advanced"])
            
            if st.button("🔍 조사하기", key="perplexity_theory"):
                if theory_query:
                    with st.spinner("최신 정보를 조사하는 중..."):
                        result = st.session_state.perplexity.search_music_theory(theory_query, depth)
                        st.markdown("### 📚 조사 결과")
                        st.markdown(result)
        
        elif search_type == "곡 배경 정보":
            song_query = st.text_input(
                "곡 제목",
                placeholder="예: 학교종이 땡땡땡"
            )
            
            if st.button("🔍 배경 조사", key="perplexity_song"):
                if song_query:
                    with st.spinner("곡 배경을 조사하는 중..."):
                        result = st.session_state.perplexity.research_song_background(song_query)
                        st.markdown("### 🎵 곡 배경 정보")
                        st.markdown(result)
        
        elif search_type == "교육 자료 찾기":
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                resource_topic = st.text_input(
                    "주제",
                    placeholder="예: 리듬 교육"
                )
            
            with col_r2:
                resource_grade = st.selectbox(
                    "대상 학년",
                    ["1-2학년", "3-4학년", "5-6학년"]
                )
            
            if st.button("🔍 자료 찾기", key="perplexity_resources"):
                if resource_topic:
                    with st.spinner("최신 교육 자료를 찾는 중..."):
                        result = st.session_state.perplexity.find_teaching_resources(
                            resource_topic, resource_grade
                        )
                        st.markdown("### 📚 추천 교육 자료")
                        st.markdown(result)
        
        elif search_type == "최신 트렌드":
            trend_area = st.text_input(
                "분야",
                value="초등 음악 교육"
            )
            
            if st.button("🔍 트렌드 조사", key="perplexity_trends"):
                with st.spinner("최신 트렌드를 조사하는 중..."):
                    result = st.session_state.perplexity.get_latest_education_trends(trend_area)
                    st.markdown("### 📈 최신 교육 트렌드")
                    st.markdown(result)
        
        elif search_type == "교수법 비교":
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                method1 = st.text_input(
                    "첫 번째 교수법",
                    placeholder="예: 오르프 교수법"
                )
            
            with col_m2:
                method2 = st.text_input(
                    "두 번째 교수법",
                    placeholder="예: 코다이 교수법"
                )
            
            if st.button("🔍 비교 분석", key="perplexity_compare"):
                if method1 and method2:
                    with st.spinner("교수법을 비교 분석하는 중..."):
                        result = st.session_state.perplexity.compare_teaching_methods(method1, method2)
                        st.markdown("### 📊 교수법 비교")
                        st.markdown(result)
    
    with resource_tab2:
        st.markdown("### 📺 음악 교육 영상 찾기 (YouTube)")
        
        youtube_status = st.session_state.youtube.get_api_status()
        
        if not youtube_status['has_key']:
            st.info("""
            🔑 **YouTube API 활성화 방법:**
            1. Google Cloud Console에서 프로젝트 생성
            2. YouTube Data API v3 활성화
            3. API 키 생성
            4. Streamlit secrets에 `YOUTUBE_API_KEY` 추가
            
            교육 영상 자동 검색, 튜토리얼 추천 등을 제공받을 수 있습니다.
            """)
        else:
            st.success("✅ YouTube 기능이 활성화되었습니다!")
        
        video_search_type = st.selectbox(
            "영상 유형",
            ["일반 검색", "악기 튜토리얼", "음악 이론 영상", "연습용 반주", "추천 채널"]
        )
        
        if video_search_type == "일반 검색":
            search_query = st.text_input(
                "검색어",
                placeholder="예: 계이름 배우기"
            )
            
            max_results = st.slider("결과 개수", 3, 10, 5)
            
            if st.button("🔍 영상 검색", key="youtube_search"):
                if search_query:
                    with st.spinner("교육 영상을 검색하는 중..."):
                        videos = st.session_state.youtube.search_education_videos(
                            search_query, max_results
                        )
                        
                        if videos and videos[0].get('video_id'):
                            st.markdown("### 📺 검색 결과")
                            for i, video in enumerate(videos, 1):
                                with st.expander(f"{i}. {video['title']}", expanded=i==1):
                                    col_v1, col_v2 = st.columns([1, 2])
                                    
                                    with col_v1:
                                        if video.get('thumbnail'):
                                            st.image(video['thumbnail'])
                                    
                                    with col_v2:
                                        st.markdown(f"**채널**: {video['channel']}")
                                        st.markdown(f"**게시일**: {video['published_at']}")
                                        st.markdown(video['description'])
                                        st.markdown(f"[영상 보기]({video['url']})")
                        else:
                            st.info("API 키를 설정하면 자동으로 영상을 검색할 수 있습니다.")
        
        elif video_search_type == "악기 튜토리얼":
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                instrument = st.selectbox(
                    "악기",
                    ["피아노", "리코더", "멜로디언", "실로폰", "우쿨렐레", "기타", "바이올린"]
                )
            
            with col_t2:
                tutorial_song = st.text_input(
                    "곡 제목 (선택)",
                    placeholder="특정 곡의 연주법"
                )
            
            if st.button("🔍 튜토리얼 찾기", key="youtube_tutorial"):
                with st.spinner("튜토리얼을 찾는 중..."):
                    videos = st.session_state.youtube.find_tutorial_videos(
                        instrument, tutorial_song if tutorial_song else None
                    )
                    
                    if videos and videos[0].get('video_id'):
                        st.markdown(f"### 🎹 {instrument} 튜토리얼")
                        for video in videos:
                            st.markdown(st.session_state.youtube.format_video_card(video))
                            st.markdown("---")
        
        elif video_search_type == "음악 이론 영상":
            theory_video_topic = st.selectbox(
                "음악 이론 주제",
                ["계이름", "박자", "리듬", "음표와 쉼표", "음정", "화음", "조성"]
            )
            
            if st.button("🔍 이론 영상 찾기", key="youtube_theory"):
                with st.spinner("음악 이론 영상을 찾는 중..."):
                    videos = st.session_state.youtube.find_solfege_videos(theory_video_topic)
                    
                    if videos and videos[0].get('video_id'):
                        st.markdown(f"### 📖 {theory_video_topic} 영상")
                        for video in videos:
                            st.markdown(st.session_state.youtube.format_video_card(video))
                            st.markdown("---")
        
        elif video_search_type == "연습용 반주":
            practice_song = st.text_input(
                "곡 제목",
                placeholder="예: 학교종"
            )
            
            if st.button("🔍 반주 찾기", key="youtube_practice"):
                if practice_song:
                    with st.spinner("연습용 반주를 찾는 중..."):
                        videos = st.session_state.youtube.find_practice_videos(practice_song)
                        
                        if videos and videos[0].get('video_id'):
                            st.markdown(f"### 🎵 {practice_song} 반주")
                            for video in videos:
                                st.markdown(st.session_state.youtube.format_video_card(video))
                                st.markdown("---")
        
        elif video_search_type == "추천 채널":
            st.markdown("### ⭐ 추천 음악 교육 채널")
            
            channels = st.session_state.youtube.recommend_channels()
            
            for channel in channels:
                with st.expander(f"📺 {channel['name']}", expanded=True):
                    st.markdown(f"**설명**: {channel['description']}")
                    st.markdown(f"**주요 주제**: {', '.join(channel['topics'])}")
                    
                    if st.button(f"🔍 영상 보기", key=f"channel_{channel['name']}"):
                        videos = st.session_state.youtube.search_education_videos(
                            channel['search_query'], 3
                        )
                        
                        if videos and videos[0].get('video_id'):
                            for video in videos:
                                st.markdown(f"- [{video['title']}]({video['url']})")
    
    st.markdown("---")
    
    with st.expander("📚 사용 방법"):
        st.markdown("""
        ### 오디오에서 악보 만들기 (왼쪽)
        1. MP3 또는 WAV 파일을 업로드하세요
        2. "악보 생성하기" 버튼을 클릭하세요
        3. AI가 멜로디를 추출하여 악보를 만듭니다
        4. "오른쪽에서 계속 처리하기"로 이동하세요
        
        ### 악보 처리하기 (오른쪽)
        1. MIDI, MusicXML 또는 ABC 파일을 업로드하세요 (또는 왼쪽에서 생성한 악보 사용)
        2. 원하는 옵션을 선택하세요:
           - **계이름 추가**: 각 음표에 도, 레, 미... 표시
           - **리듬 단순화**: 복잡한 리듬을 간단하게
           - **다장조 변환**: 모든 곡을 다장조로
           - **반주 추가**: 기본 화음 반주 생성
        3. "처리하기" 버튼을 클릭하세요
        4. 완성된 악보를 재생하고 다운로드하세요!
        
        ### PDF 악보는?
        PDF 악보는 먼저 MusicXML로 변환해야 합니다.
        - Audiveris (무료): https://audiveris.github.io/
        - MuseScore (무료): https://musescore.org/
        변환 후 MusicXML 파일을 업로드하세요.
        """)
    
    with st.expander("ℹ️ 정보"):
        st.markdown("""
        - **개발**: 차미혜
        - **목적**: 초등학생과 교사를 위한 음악 학습 지원
        - **기술**: Python, Streamlit, music21, basic-pitch
        - **GitHub**: [프로젝트 저장소](#)
        - **피드백**: 개선 사항이 있으면 알려주세요!
        """)

if __name__ == "__main__":
    main()
