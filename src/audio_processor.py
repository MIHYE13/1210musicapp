"""
Audio Processing Module
Converts audio files to musical scores using basic-pitch
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

import soundfile as sf
import numpy as np
from io import BytesIO
from music21 import stream, note, tempo, meter, key
from typing import Optional
import tempfile
import os

class AudioProcessor:
    """Process audio files and convert to musical notation"""
    
    def __init__(self):
        """Initialize audio processor"""
        self.sample_rate = 22050
        self.model = None
    
    def _load_basic_pitch_model(self):
        """Load basic-pitch model"""
        try:
            from basic_pitch.inference import predict
            return predict
        except ImportError as e:
            error_msg = f"basic-pitch 라이브러리가 설치되지 않았습니다. pip install basic-pitch를 실행해주세요. 오류: {str(e)}"
            if HAS_STREAMLIT and st:
                st.error(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            return None
        except Exception as e:
            error_msg = f"basic-pitch 모델 로드 중 오류 발생: {str(e)}"
            if HAS_STREAMLIT and st:
                st.error(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            return None
    
    def process_audio(self, audio_file) -> Optional[stream.Score]:
        """
        Process audio file and convert to music21 score
        
        Args:
            audio_file: Uploaded audio file (mp3, wav)
            
        Returns:
            music21.stream.Score object or None if failed
        """
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_file.read())
                tmp_path = tmp_file.name
            
            # Load basic-pitch model
            predict = self._load_basic_pitch_model()
            if predict is None:
                return None
            
            # Predict MIDI from audio
            model_output, midi_data, note_events = predict(tmp_path)
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            # Convert MIDI to music21 score
            score = self._midi_to_score(midi_data, note_events)
            
            return score
            
        except Exception as e:
            try:
                import st
                st.error(f"오디오 처리 오류: {str(e)}")
            except:
                print(f"오디오 처리 오류: {str(e)}")
            return None
    
    def process_audio_from_path(self, audio_path: str) -> Optional[stream.Score]:
        """
        Process audio file from file path and convert to music21 score
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            music21.stream.Score object or None if failed
        """
        try:
            # Load basic-pitch model
            predict = self._load_basic_pitch_model()
            if predict is None:
                return None
            
            # Predict MIDI from audio
            model_output, midi_data, note_events = predict(audio_path)
            
            # Convert MIDI to music21 score
            score = self._midi_to_score(midi_data, note_events)
            
            return score
            
        except Exception as e:
            try:
                import st
                st.error(f"오디오 처리 오류: {str(e)}")
            except:
                print(f"오디오 처리 오류: {str(e)}")
            return None
    
    def _midi_to_score(self, midi_data, note_events) -> stream.Score:
        """
        Convert MIDI data to music21 score
        
        Args:
            midi_data: MIDI data from basic-pitch
            note_events: Note events from basic-pitch
            
        Returns:
            music21.stream.Score object
        """
        s = stream.Score()
        
        # Add metadata
        s.metadata = stream.metadata.Metadata()
        s.metadata.title = "추출된 멜로디"
        
        # Create a part for melody
        melody_part = stream.Part()
        
        # Add time signature and tempo
        melody_part.append(meter.TimeSignature('4/4'))
        melody_part.append(tempo.MetronomeMark(number=120))
        melody_part.append(key.Key('C'))
        
        # Convert note events to music21 notes
        for note_event in note_events:
            start_time = note_event['start_time_s']
            duration = note_event['duration_s']
            pitch_midi = note_event['pitch_midi']
            
            # Create note
            n = note.Note()
            n.pitch.midi = int(pitch_midi)
            n.quarterLength = duration * 2  # Convert to quarter notes
            n.offset = start_time * 2
            
            melody_part.append(n)
        
        # Simplify to monophonic if needed
        melody_part = self._make_monophonic(melody_part)
        
        s.append(melody_part)
        
        return s
    
    def _make_monophonic(self, part: stream.Part) -> stream.Part:
        """
        Ensure part is monophonic (one note at a time)
        
        Args:
            part: music21.stream.Part
            
        Returns:
            Monophonic part
        """
        monophonic = stream.Part()
        
        # Copy metadata
        for elem in part.getElementsByClass(['TimeSignature', 'KeySignature', 'Tempo']):
            monophonic.append(elem)
        
        # Get all notes sorted by offset
        notes = sorted(part.flat.notes, key=lambda x: x.offset)
        
        last_end = 0
        for n in notes:
            # Only add if doesn't overlap with previous
            if n.offset >= last_end:
                new_note = note.Note(n.pitch.midi)
                new_note.quarterLength = n.quarterLength
                new_note.offset = n.offset
                monophonic.append(new_note)
                last_end = n.offset + n.quarterLength
        
        return monophonic
    
    def render_score(self, score: stream.Score) -> Optional[bytes]:
        """
        Render score as PNG image
        
        Args:
            score: music21.stream.Score object
            
        Returns:
            PNG image bytes or None
        """
        try:
            # Try to render using music21's built-in methods
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_path = tmp_file.name
            
            # Write score as PNG
            score.write('musicxml.png', fp=tmp_path)
            
            # Read the image
            with open(tmp_path, 'rb') as f:
                img_bytes = f.read()
            
            # Clean up
            os.unlink(tmp_path)
            
            return img_bytes
            
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.warning(f"악보 렌더링 실패: {str(e)}")
                st.info("MuseScore가 설치되어 있는지 확인해주세요.")
            else:
                print(f"악보 렌더링 실패: {str(e)}")
                print("MuseScore가 설치되어 있는지 확인해주세요.")
            return None
    
    def load_audio(self, audio_file) -> tuple[np.ndarray, int]:
        """
        Load audio file
        
        Args:
            audio_file: Uploaded audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            audio_bytes = audio_file.read()
            audio_data, sample_rate = sf.read(BytesIO(audio_bytes))
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            return audio_data, sample_rate
            
        except Exception as e:
            raise Exception(f"오디오 로딩 실패: {str(e)}")
    
    def get_audio_info(self, audio_file) -> dict:
        """
        Get information about audio file
        
        Args:
            audio_file: Uploaded audio file
            
        Returns:
            Dictionary with audio information
        """
        try:
            audio_data, sample_rate = self.load_audio(audio_file)
            duration = len(audio_data) / sample_rate
            
            return {
                'sample_rate': sample_rate,
                'duration': duration,
                'samples': len(audio_data),
                'channels': 1 if len(audio_data.shape) == 1 else audio_data.shape[1]
            }
            
        except Exception as e:
            return {'error': str(e)}
