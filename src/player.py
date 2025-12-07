"""
Music Player Module
Handles playback of musical scores
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None
from music21 import stream, midi
import tempfile
import os
from typing import Optional

class MusicPlayer:
    """Play music21 scores"""
    
    def __init__(self):
        """Initialize music player"""
        self.is_playing = False
        self.current_score = None
    
    def play(self, score: stream.Score) -> bool:
        """
        Play a musical score
        
        Args:
            score: music21.stream.Score to play
            
        Returns:
            True if playback started successfully
        """
        try:
            # Convert score to MIDI for playback
            midi_data = self._score_to_midi(score)
            
            if midi_data:
                self.current_score = score
                self.is_playing = True
                
                # Display audio player in Streamlit
                st.audio(midi_data, format='audio/midi')
                return True
            
            return False
            
        except Exception as e:
            st.error(f"재생 오류: {str(e)}")
            return False
    
    def _score_to_midi(self, score: stream.Score) -> Optional[bytes]:
        """
        Convert score to MIDI bytes
        
        Args:
            score: music21.stream.Score
            
        Returns:
            MIDI file bytes
        """
        try:
            # Create temporary MIDI file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mid') as tmp_file:
                tmp_path = tmp_file.name
            
            # Write score as MIDI
            mf = midi.translate.music21ObjectToMidiFile(score)
            mf.open(tmp_path, 'wb')
            mf.write()
            mf.close()
            
            # Read MIDI bytes
            with open(tmp_path, 'rb') as f:
                midi_bytes = f.read()
            
            # Clean up
            os.unlink(tmp_path)
            
            return midi_bytes
            
        except Exception as e:
            st.error(f"MIDI 변환 오류: {str(e)}")
            return None
    
    def pause(self):
        """Pause playback"""
        self.is_playing = False
        st.info("일시정지 기능은 브라우저의 재생 컨트롤을 사용해주세요.")
    
    def stop(self):
        """Stop playback"""
        self.is_playing = False
        self.current_score = None
        st.info("정지 기능은 브라우저의 재생 컨트롤을 사용해주세요.")
    
    def get_playback_info(self) -> dict:
        """
        Get information about current playback
        
        Returns:
            Dictionary with playback information
        """
        info = {
            'is_playing': self.is_playing,
            'has_score': self.current_score is not None
        }
        
        if self.current_score:
            info['duration'] = self.current_score.duration.quarterLength
            info['tempo'] = 120  # Default tempo
        
        return info
    
    def create_playback_html(self, score: stream.Score) -> str:
        """
        Create HTML for enhanced playback using OSMD
        (Optional - requires additional setup)
        
        Args:
            score: music21.stream.Score
            
        Returns:
            HTML string for embedding
        """
        # This is a placeholder for future OSMD integration
        # Would require converting score to MusicXML and embedding OSMD player
        
        html = """
        <div id="music-player">
            <p>고급 재생 기능은 추후 업데이트 예정입니다.</p>
            <p>현재는 기본 MIDI 재생을 사용해주세요.</p>
        </div>
        """
        
        return html
    
    def export_audio(self, score: stream.Score, format: str = 'midi') -> Optional[bytes]:
        """
        Export score as audio file
        
        Args:
            score: music21.stream.Score
            format: Output format ('midi' only for now)
            
        Returns:
            Audio file bytes
        """
        if format == 'midi':
            return self._score_to_midi(score)
        else:
            st.error(f"지원하지 않는 형식: {format}")
            return None
