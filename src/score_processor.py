"""
Score Processing Module
Handles score loading, simplification, transposition, and solfege addition
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

from music21 import stream, note, chord, key, interval, converter
from typing import Optional
import tempfile
import os
from io import BytesIO

class ScoreProcessor:
    """Process musical scores - simplify, transpose, add solfege"""
    
    # Solfege mapping for C major scale
    SOLFEGE_MAP = {
        'C': '도',
        'D': '레',
        'E': '미',
        'F': '파',
        'G': '솔',
        'A': '라',
        'B': '시'
    }
    
    # Chromatic solfege (with accidentals)
    SOLFEGE_CHROMATIC = {
        'C': '도', 'C#': '도#', 'C-': '도♭',
        'D': '레', 'D#': '레#', 'D-': '레♭',
        'E': '미', 'E#': '미#', 'E-': '미♭',
        'F': '파', 'F#': '파#', 'F-': '파♭',
        'G': '솔', 'G#': '솔#', 'G-': '솔♭',
        'A': '라', 'A#': '라#', 'A-': '라♭',
        'B': '시', 'B#': '시#', 'B-': '시♭'
    }
    
    def __init__(self):
        """Initialize score processor"""
        pass
    
    def load_score(self, score_file) -> Optional[stream.Score]:
        """
        Load score from uploaded file
        
        Args:
            score_file: Uploaded file (MIDI, MusicXML, ABC)
            
        Returns:
            music21.stream.Score object or None
        """
        try:
            # Get file extension
            file_ext = score_file.name.split('.')[-1].lower()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}') as tmp_file:
                tmp_file.write(score_file.read())
                tmp_path = tmp_file.name
            
            # Parse with music21
            score = converter.parse(tmp_path)
            
            # Clean up
            os.unlink(tmp_path)
            
            return score
            
        except Exception as e:
            try:
                import st
                st.error(f"악보 로딩 오류: {str(e)}")
            except:
                print(f"악보 로딩 오류: {str(e)}")
            return None
    
    def load_score_from_path(self, score_path: str) -> Optional[stream.Score]:
        """
        Load score from file path
        
        Args:
            score_path: Path to score file (MIDI, MusicXML, ABC)
            
        Returns:
            music21.stream.Score object or None
        """
        try:
            # Parse with music21
            score = converter.parse(score_path)
            return score
            
        except Exception as e:
            try:
                import st
                st.error(f"악보 로딩 오류: {str(e)}")
            except:
                print(f"악보 로딩 오류: {str(e)}")
            return None
    
    def simplify_rhythm(self, score: stream.Score, 
                       allowed_durations: list = [0.5, 1.0, 2.0, 4.0]) -> stream.Score:
        """
        Simplify rhythm by quantizing to allowed durations
        
        Args:
            score: music21.stream.Score
            allowed_durations: List of allowed quarter note durations
            
        Returns:
            Simplified score
        """
        simplified = stream.Score()
        
        for part in score.parts:
            new_part = stream.Part()
            
            # Copy metadata
            for elem in part.getElementsByClass(['TimeSignature', 'KeySignature', 'Clef']):
                new_part.append(elem)
            
            # Process notes
            for element in part.flat.notesAndRests:
                if isinstance(element, note.Note):
                    # Quantize duration
                    quantized_duration = self._quantize_duration(
                        element.quarterLength, 
                        allowed_durations
                    )
                    
                    new_note = note.Note(element.pitch.midi)
                    new_note.quarterLength = quantized_duration
                    new_part.append(new_note)
                    
                elif isinstance(element, note.Rest):
                    # Keep rests but simplify duration
                    quantized_duration = self._quantize_duration(
                        element.quarterLength, 
                        allowed_durations
                    )
                    
                    new_rest = note.Rest()
                    new_rest.quarterLength = quantized_duration
                    new_part.append(new_rest)
            
            simplified.append(new_part)
        
        return simplified
    
    def _quantize_duration(self, duration: float, allowed: list) -> float:
        """
        Quantize duration to nearest allowed value
        
        Args:
            duration: Original duration in quarter notes
            allowed: List of allowed durations
            
        Returns:
            Quantized duration
        """
        # Find nearest allowed duration
        nearest = min(allowed, key=lambda x: abs(x - duration))
        return nearest
    
    def transpose_to_c_major(self, score: stream.Score) -> stream.Score:
        """
        Transpose score to C major and constrain to C4-C5 range
        
        Args:
            score: music21.stream.Score
            
        Returns:
            Transposed score
        """
        transposed = stream.Score()
        target_key = key.Key('C')
        
        for part in score.parts:
            new_part = stream.Part()
            
            # Analyze current key
            try:
                current_key = part.analyze('key')
            except:
                # If analysis fails, assume C major
                current_key = key.Key('C')
            
            # Calculate interval for transposition
            trans_interval = interval.Interval(current_key.tonic, target_key.tonic)
            
            # Transpose part
            transposed_part = part.transpose(trans_interval)
            
            # Constrain to C4-C5 range
            constrained_part = self._constrain_range(transposed_part, 60, 72)  # C4 to C5
            
            transposed.append(constrained_part)
        
        return transposed
    
    def _constrain_range(self, part: stream.Part, min_midi: int, max_midi: int) -> stream.Part:
        """
        Constrain notes to specified MIDI range
        
        Args:
            part: music21.stream.Part
            min_midi: Minimum MIDI number (e.g., 60 for C4)
            max_midi: Maximum MIDI number (e.g., 72 for C5)
            
        Returns:
            Constrained part
        """
        constrained = stream.Part()
        
        # Copy metadata
        for elem in part.getElementsByClass(['TimeSignature', 'KeySignature', 'Clef']):
            constrained.append(elem)
        
        # Process notes
        for element in part.flat.notesAndRests:
            if isinstance(element, note.Note):
                midi_num = element.pitch.midi
                
                # Transpose by octaves to fit range
                while midi_num < min_midi:
                    midi_num += 12
                while midi_num > max_midi:
                    midi_num -= 12
                
                new_note = note.Note()
                new_note.pitch.midi = midi_num
                new_note.quarterLength = element.quarterLength
                constrained.append(new_note)
                
            elif isinstance(element, note.Rest):
                constrained.append(element)
        
        return constrained
    
    def add_solfege(self, score: stream.Score) -> stream.Score:
        """
        Add solfege syllables (do, re, mi...) as lyrics
        
        Args:
            score: music21.stream.Score
            
        Returns:
            Score with solfege lyrics
        """
        score_with_solfege = stream.Score()
        
        for part in score.parts:
            new_part = stream.Part()
            
            # Copy all elements
            for element in part.flat:
                if isinstance(element, note.Note):
                    new_note = note.Note(element.pitch.midi)
                    new_note.quarterLength = element.quarterLength
                    
                    # Add solfege as lyric
                    pitch_name = element.pitch.name
                    solfege = self.SOLFEGE_CHROMATIC.get(pitch_name, pitch_name)
                    new_note.lyric = solfege
                    
                    new_part.append(new_note)
                else:
                    new_part.append(element)
            
            score_with_solfege.append(new_part)
        
        return score_with_solfege
    
    def render_score(self, score: stream.Score) -> Optional[bytes]:
        """
        Render score as image
        
        Args:
            score: music21.stream.Score
            
        Returns:
            Image bytes or None
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_path = tmp_file.name
            
            # Try to render
            score.write('musicxml.png', fp=tmp_path)
            
            with open(tmp_path, 'rb') as f:
                img_bytes = f.read()
            
            os.unlink(tmp_path)
            return img_bytes
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.warning(f"악보 이미지 생성 실패: {str(e)}")
            else:
                print(f"악보 이미지 생성 실패: {str(e)}")
            return None
    
    def export_midi(self, score: stream.Score) -> Optional[bytes]:
        """
        Export score as MIDI file
        
        Args:
            score: music21.stream.Score
            
        Returns:
            MIDI file bytes
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mid') as tmp_file:
                tmp_path = tmp_file.name
            
            score.write('midi', fp=tmp_path)
            
            with open(tmp_path, 'rb') as f:
                midi_bytes = f.read()
            
            os.unlink(tmp_path)
            return midi_bytes
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.error(f"MIDI 내보내기 실패: {str(e)}")
            else:
                print(f"MIDI 내보내기 실패: {str(e)}")
            return None
    
    def export_musicxml(self, score: stream.Score) -> Optional[bytes]:
        """
        Export score as MusicXML file
        
        Args:
            score: music21.stream.Score
            
        Returns:
            MusicXML file bytes
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp_file:
                tmp_path = tmp_file.name
            
            score.write('musicxml', fp=tmp_path)
            
            with open(tmp_path, 'rb') as f:
                xml_bytes = f.read()
            
            os.unlink(tmp_path)
            return xml_bytes
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.error(f"MusicXML 내보내기 실패: {str(e)}")
            else:
                print(f"MusicXML 내보내기 실패: {str(e)}")
            return None
    
    def get_score_info(self, score: stream.Score) -> dict:
        """
        Get information about the score
        
        Args:
            score: music21.stream.Score
            
        Returns:
            Dictionary with score information
        """
        try:
            info = {
                'parts': len(score.parts),
                'measures': 0,
                'notes': 0,
                'duration': 0
            }
            
            if score.parts:
                part = score.parts[0]
                info['measures'] = len(part.getElementsByClass('Measure'))
                info['notes'] = len(part.flat.notes)
                info['duration'] = part.duration.quarterLength
            
            return info
            
        except:
            return {'error': 'Could not analyze score'}
