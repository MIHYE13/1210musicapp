"""
Chord Analysis & Piano Play Page
Revolutionary feature for chord analysis and interactive piano visualization
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from chord_analyzer import ChordAnalyzer, PianoVisualizer
from youtube_downloader import YouTubeDownloader, get_youtube_download_guide
from pdf_parser import PDFScoreParser, get_pdf_parsing_guide, create_pdf_upload_section
from audio_processor import AudioProcessor
from score_processor import ScoreProcessor
from music21 import converter, stream

# Page config
st.set_page_config(
    page_title="화음 분석 & 피아노 연주",
    page_icon="🎹",
    layout="wide"
)

# Initialize
if 'chord_analyzer' not in st.session_state:
    st.session_state.chord_analyzer = ChordAnalyzer()
if 'youtube_dl' not in st.session_state:
    st.session_state.youtube_dl = YouTubeDownloader()
if 'pdf_parser' not in st.session_state:
    st.session_state.pdf_parser = PDFScoreParser()

# Header
st.title("🎹 화음 분석 & 피아노 연주")
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
    <h3 style="margin: 0; color: white;">🎯 차별화 기능!</h3>
    <p style="margin: 10px 0 0 0;">
        • MIDI/YouTube/PDF → 화음 자동 분석<br>
        • 모두 다장조로 변환<br>
        • 피아노 건반에 화음 표시<br>
        • 클릭하여 소리 재생
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs for different input methods
tab1, tab2, tab3 = st.tabs([
    "🎵 MIDI 반주 분석",
    "📺 YouTube 음원",
    "📄 PDF 악보"
])

# ============================================
# TAB 1: MIDI 파일 업로드
# ============================================
with tab1:
    st.header("🎵 MIDI 반주 음원 분석")
    
    st.info("""
    **기능:**
    1. MIDI 파일의 화음을 자동 분석
    2. 다장조(C major)로 자동 변환
    3. 화음 코드를 피아노 건반에 표시
    4. 마디별 화음 진행 확인
    5. 건반을 클릭하여 연주 가능
    """)
    
    midi_file = st.file_uploader(
        "MIDI 파일 업로드",
        type=['mid', 'midi'],
        key="midi_chord_analysis"
    )
    
    if midi_file:
        try:
            # Save file
            midi_path = Path("temp/midi") / midi_file.name
            midi_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(midi_path, 'wb') as f:
                f.write(midi_file.getvalue())
            
            st.success("✅ MIDI 파일이 업로드되었습니다!")
            
            # Load and process
            with st.spinner("악보를 불러오는 중..."):
                score = converter.parse(str(midi_path))
            
            # Convert to C major
            with st.spinner("다장조로 변환 중..."):
                processor = ScoreProcessor()
                score_in_c = processor.transpose_to_c_major(score)
            
            st.success("✅ 다장조로 변환 완료!")
            
            # Analyze chords
            with st.spinner("화음을 분석하는 중..."):
                chords_info = st.session_state.chord_analyzer.analyze_midi_chords(score_in_c)
            
            if chords_info:
                st.success(f"✅ {len(chords_info)}개 마디의 화음을 분석했습니다!")
                
                # Display summary
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📊 화음 진행 요약")
                    summary = st.session_state.chord_analyzer.create_chord_progression_summary(chords_info)
                    st.markdown(summary)
                
                with col2:
                    st.markdown("### 📋 화음 진행표")
                    chart = st.session_state.chord_analyzer.generate_chord_chart(chords_info)
                    st.markdown(chart)
                
                # Display piano keyboards for each measure
                st.markdown("---")
                st.markdown("### 🎹 마디별 피아노 화음 (처음 8마디)")
                
                keyboards_html = st.session_state.chord_analyzer.generate_all_chords_display(chords_info)
                st.markdown(keyboards_html, unsafe_allow_html=True)
                
                # Interactive piano
                st.markdown("---")
                st.markdown("### 🎼 인터랙티브 피아노 연습")
                
                measure_num = st.slider(
                    "연습할 마디 선택",
                    1,
                    min(len(chords_info), 16),
                    1
                )
                
                selected_chord = chords_info[measure_num - 1]
                st.markdown(f"**마디 {measure_num}: {selected_chord['chord_name']} 코드**")
                
                keyboard_html = PianoVisualizer.generate_playable_keyboard(
                    selected_chord['notes']
                )
                st.markdown(keyboard_html, unsafe_allow_html=True)
                
                # Download options
                st.markdown("---")
                st.markdown("### 💾 다운로드")
                
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    # Add chord symbols to score
                    score_with_chords = st.session_state.chord_analyzer.add_chord_symbols_to_score(
                        score_in_c, chords_info
                    )
                    
                    # Save as MIDI
                    output_midi = Path("temp/output") / "chords_analyzed.mid"
                    output_midi.parent.mkdir(parents=True, exist_ok=True)
                    score_with_chords.write('midi', fp=str(output_midi))
                    
                    with open(output_midi, 'rb') as f:
                        st.download_button(
                            label="📥 화음 악보 다운로드 (MIDI)",
                            data=f,
                            file_name="chord_analysis.mid",
                            mime="audio/midi"
                        )
                
                with col_d2:
                    # Save as MusicXML
                    output_xml = Path("temp/output") / "chords_analyzed.musicxml"
                    score_with_chords.write('musicxml', fp=str(output_xml))
                    
                    with open(output_xml, 'rb') as f:
                        st.download_button(
                            label="📥 화음 악보 다운로드 (MusicXML)",
                            data=f,
                            file_name="chord_analysis.musicxml",
                            mime="application/xml"
                        )
            
            else:
                st.warning("화음을 분석할 수 없습니다. 멜로디만 있는 파일일 수 있습니다.")
        
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

# ============================================
# TAB 2: YouTube 음원
# ============================================
with tab2:
    st.header("📺 YouTube 음원 화음 분석")
    
    st.info("""
    **기능:**
    1. YouTube 링크에서 오디오 추출
    2. AI로 멜로디 추출 (basic-pitch)
    3. 다장조로 변환
    4. 화음 자동 분석
    5. 피아노 건반에 표시
    """)
    
    youtube_url = st.text_input(
        "YouTube URL 입력",
        placeholder="https://www.youtube.com/watch?v=...",
        help="음악 영상의 YouTube 링크를 입력하세요"
    )
    
    if youtube_url:
        if st.session_state.youtube_dl.validate_url(youtube_url):
            st.success("✅ 유효한 YouTube URL입니다!")
            
            # Get video info
            with st.spinner("영상 정보를 가져오는 중..."):
                video_info = st.session_state.youtube_dl.get_video_info(youtube_url)
            
            if video_info:
                st.write(f"**제목**: {video_info['title']}")
                st.write(f"**길이**: {video_info['duration']}초")
                st.write(f"**업로더**: {video_info['uploader']}")
                
                if st.button("🎵 오디오 다운로드 및 분석 시작"):
                    # Download audio
                    with st.spinner("오디오를 다운로드하는 중... (최대 2분)"):
                        audio_path = st.session_state.youtube_dl.download_with_fallback(youtube_url)
                    
                    if audio_path:
                        st.success("✅ 오디오 다운로드 완료!")
                        
                        # Process like audio file
                        st.info("이제 메인 페이지의 '오디오 → 악보 변환'과 동일하게 처리됩니다.")
                        st.info("화음 분석을 위해 MIDI 파일로 변환 후 위의 'MIDI 반주 분석' 탭을 사용하세요!")
            else:
                st.warning("영상 정보를 가져올 수 없습니다.")
                st.markdown("### 📖 수동 다운로드 가이드")
                st.markdown(get_youtube_download_guide(youtube_url))
        
        else:
            st.error("유효하지 않은 YouTube URL입니다.")

# ============================================
# TAB 3: PDF 악보
# ============================================
with tab3:
    st.header("📄 PDF 악보 화음 분석")
    
    st.info("""
    **기능:**
    1. PDF 악보를 MusicXML로 변환
    2. 다장조로 변환
    3. 화음 자동 분석
    4. 피아노 건반에 표시
    """)
    
    pdf_path = create_pdf_upload_section()
    
    if pdf_path:
        st.info("""
        **현재 단계:**
        
        PDF 파일이 업로드되었습니다. 
        
        **다음 작업:**
        1. MuseScore 등으로 이 PDF를 MusicXML로 변환
        2. 메인 페이지 또는 'MIDI 반주 분석' 탭에서 MusicXML 업로드
        3. 자동으로 화음 분석 및 피아노 건반 표시
        
        **또는:**
        - 위의 가이드에 따라 MuseScore 사용
        - Audiveris로 자동 변환 시도
        """)

# Sidebar info
with st.sidebar:
    st.markdown("### 🎯 이 페이지의 특징")
    st.markdown("""
    **차별화된 기능:**
    
    1. **화음 자동 분석**
       - MIDI에서 화음 추출
       - 마디별 코드 표시
    
    2. **다장조 변환**
       - 모든 곡을 C major로
       - 초보자 학습 최적화
    
    3. **피아노 건반 표시**
       - 시각적 화음 학습
       - 클릭하여 소리 재생
    
    4. **인터랙티브 연주**
       - Web Audio API 사용
       - 실시간 사운드
    
    **활용 방법:**
    - 화음 학습
    - 반주 연습
    - 코드 진행 분석
    - 피아노 연주 익히기
    """)
    
    st.markdown("---")
    st.markdown("**버전**: 5.0.0")
    st.markdown("**새 기능**: 화음 분석 & 피아노")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>🎹 화음 분석 & 피아노 연주</strong></p>
    <p>초등 음악 도우미의 차별화된 기능입니다!</p>
</div>
""", unsafe_allow_html=True)
