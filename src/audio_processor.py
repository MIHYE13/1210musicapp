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

try:
    import soundfile as sf
except ImportError:
    sf = None
    print("[WARN] soundfile이 설치되지 않았습니다. pip install soundfile를 실행해주세요.")

import numpy as np
from io import BytesIO

try:
    from music21 import stream, note, tempo, meter, key
except ImportError:
    print("[WARN] music21이 설치되지 않았습니다. pip install music21을 실행해주세요.")
    stream = note = tempo = meter = key = None

from typing import Optional
import tempfile
import os
from pathlib import Path

class AudioProcessor:
    """Process audio files and convert to musical notation"""
    
    def __init__(self):
        """Initialize audio processor"""
        # Check required dependencies
        if sf is None:
            raise ImportError("soundfile이 설치되지 않았습니다. pip install soundfile를 실행해주세요.")
        if stream is None or note is None:
            raise ImportError("music21이 설치되지 않았습니다. pip install music21을 실행해주세요.")
        
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
                print(f"[WARN] {error_msg}")
            return None
        except Exception as e:
            error_msg = f"basic-pitch 모델 로드 중 오류 발생: {str(e)}"
            if HAS_STREAMLIT and st:
                st.error(error_msg)
            else:
                print(f"[WARN] {error_msg}")
            return None
    
    def _process_audio_with_librosa(self, audio_path: str) -> Optional[stream.Score]:
        """
        Process audio using librosa (fallback method when basic-pitch is not available)
        This is a simpler method that extracts pitch using librosa's pitch detection
        """
        try:
            import librosa
            import librosa.display
            
            print("[INFO] librosa를 사용하여 오디오 파일 로드 중...")
            # Load audio file with better error handling
            try:
                y, sr = librosa.load(audio_path, sr=22050, mono=True, duration=60.0)  # 최대 60초만 처리
            except Exception as e:
                print(f"[ERROR] 오디오 파일 로드 실패: {str(e)}")
                # 다른 샘플 레이트로 시도
                try:
                    y, sr = librosa.load(audio_path, sr=None, mono=True)
                    y = librosa.resample(y, orig_sr=sr, target_sr=22050)
                    sr = 22050
                except Exception as e2:
                    print(f"[ERROR] 오디오 파일 재시도 실패: {str(e2)}")
                    return None
            
            if len(y) == 0:
                print("[ERROR] 오디오 파일이 비어있습니다.")
                return None
            
            print(f"[INFO] 오디오 길이: {len(y)/sr:.2f}초, 샘플 레이트: {sr}Hz")
            
            # Extract pitch using librosa's pyin algorithm with better parameters
            print("[INFO] 피치 추출 중...")
            try:
                f0, voiced_flag, voiced_probs = librosa.pyin(
                    y,
                    fmin=librosa.note_to_hz('C3'),  # C3부터 시작 (더 낮은 음 제외)
                    fmax=librosa.note_to_hz('C6'),  # C6까지 (더 높은 음 제외)
                    frame_length=2048,
                    hop_length=512,
                    threshold=0.1  # 더 낮은 임계값으로 더 많은 음표 감지
                )
            except Exception as e:
                print(f"[ERROR] 피치 추출 실패: {str(e)}")
                # 대안: chroma feature 사용
                try:
                    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
                    # 간단한 멜로디 추출 시도
                    print("[INFO] chroma feature를 사용하여 멜로디 추출 시도...")
                    # chroma에서 가장 강한 음을 찾기
                    chroma_mean = np.mean(chroma, axis=1)
                    # 이 방법은 복잡하므로 기본 방법으로 돌아감
                    return None
                except:
                    return None
            
            # Create score
            s = stream.Score()
            s.metadata = stream.metadata.Metadata()
            s.metadata.title = "추출된 멜로디 (librosa)"
            
            # Create part
            part = stream.Part()
            part.append(meter.TimeSignature('4/4'))
            part.append(tempo.MetronomeMark(number=120))
            part.append(key.Key('C'))
            
            # Convert pitch to notes with better filtering
            time_step = 0.25  # 0.25초 간격으로 더 세밀하게
            hop_samples = len(y) // len(f0) if len(f0) > 0 else 512
            time_per_frame = hop_samples / sr
            
            notes_added = 0
            last_note = None
            note_duration = 0.0
            
            for i, pitch_hz in enumerate(f0):
                if not np.isnan(pitch_hz) and voiced_flag[i] and pitch_hz > 0:
                    # Convert Hz to MIDI note number
                    midi_num = librosa.hz_to_midi(pitch_hz)
                    
                    # Round to nearest semitone and clamp to valid range
                    midi_num = int(round(midi_num))
                    midi_num = max(48, min(84, midi_num))  # C3 to C6 범위
                    
                    current_time = i * time_per_frame
                    
                    # 같은 음이면 duration 증가, 다른 음이면 새 노트 추가
                    if last_note is not None and last_note.pitch.midi == midi_num:
                        note_duration += time_per_frame
                    else:
                        # 이전 노트 저장
                        if last_note is not None:
                            last_note.quarterLength = max(0.25, min(2.0, note_duration * 2))
                            part.append(last_note)
                            notes_added += 1
                        
                        # 새 노트 생성
                        n = note.Note(midi=midi_num)
                        n.offset = current_time
                        last_note = n
                        note_duration = time_per_frame
            
            # 마지막 노트 추가
            if last_note is not None:
                last_note.quarterLength = max(0.25, min(2.0, note_duration * 2))
                part.append(last_note)
                notes_added += 1
            
            # If no notes found, return None
            if notes_added == 0:
                print("[WARN] librosa로 음표를 추출할 수 없습니다. 오디오 파일에 명확한 멜로디가 없을 수 있습니다.")
                return None
            
            print(f"[INFO] {notes_added}개의 음표를 추출했습니다.")
            s.append(part)
            return s
            
        except ImportError as e:
            print(f"[ERROR] librosa가 설치되지 않았습니다: {str(e)}")
            print("설치 방법: pip install librosa")
            return None
        except Exception as e:
            print(f"[ERROR] librosa 오디오 처리 오류: {str(e)}")
            import traceback
            traceback.print_exc()
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
            # Try basic-pitch first (more accurate)
            predict = self._load_basic_pitch_model()
            if predict is not None:
                try:
                    # Predict MIDI from audio
                    model_output, midi_data, note_events = predict(audio_path)
                    
                    # Convert MIDI to music21 score
                    score = self._midi_to_score(midi_data, note_events)
                    
                    if score and len(score.flat.notes) > 0:
                        return score
                except Exception as e:
                    print(f"[WARN] basic-pitch 처리 실패, librosa로 대체 시도: {str(e)}")
            
            # Fallback to librosa if basic-pitch is not available or failed
            print("[INFO] librosa를 사용하여 오디오 처리 중...")
            score = self._process_audio_with_librosa(audio_path)
            
            if score and len(score.flat.notes) > 0:
                return score
            else:
                print("[ERROR] 오디오에서 음표를 추출할 수 없습니다.")
                return None
            
        except Exception as e:
            try:
                import st
                st.error(f"오디오 처리 오류: {str(e)}")
            except:
                print(f"[ERROR] 오디오 처리 오류: {str(e)}")
            import traceback
            traceback.print_exc()
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
    
    def download_youtube_audio(self, youtube_url: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Download audio from YouTube and convert to MP3 using yt-dlp
        
        Args:
            youtube_url: YouTube video URL
            output_path: Optional output file path (if None, uses temp file)
            
        Returns:
            Path to downloaded MP3 file or None if failed
        """
        try:
            # Import yt-dlp
            try:
                import yt_dlp
            except ImportError:
                error_msg = "yt-dlp가 설치되지 않았습니다. pip install yt-dlp를 실행해주세요."
                if HAS_STREAMLIT and st:
                    st.error(error_msg)
                else:
                    print(f"[ERROR] {error_msg}")
                raise ImportError(error_msg)
            
            # FFmpeg 경로 확인
            FFMPEG_PATH = r"C:\ffmpeg\bin"
            ffmpeg_bin_path = Path(FFMPEG_PATH)
            
            # FFmpeg 존재 여부 확인
            ffmpeg_exists = (ffmpeg_bin_path / "ffmpeg.exe").exists() or (ffmpeg_bin_path / "ffmpeg").exists()
            
            if not ffmpeg_exists:
                # 환경 변수나 PATH에서도 확인
                import shutil
                ffmpeg_exe = shutil.which("ffmpeg")
                if ffmpeg_exe:
                    ffmpeg_bin_path = Path(ffmpeg_exe).parent
                    ffmpeg_exists = True
                else:
                    error_msg = (
                        f"FFmpeg를 찾을 수 없습니다.\n\n"
                        f"FFmpeg 설치 방법:\n"
                        f"1. FFmpeg를 다운로드: https://ffmpeg.org/download.html\n"
                        f"2. C:\\ffmpeg\\bin 폴더에 ffmpeg.exe와 ffprobe.exe를 설치하세요.\n"
                        f"3. 또는 시스템 PATH에 FFmpeg를 추가하세요.\n\n"
                        f"현재 확인한 경로: {FFMPEG_PATH}"
                    )
                    if HAS_STREAMLIT and st:
                        st.error(error_msg)
                    else:
                        print(f"[ERROR] {error_msg}")
                    raise FileNotFoundError("FFmpeg를 찾을 수 없습니다. FFmpeg를 설치해주세요.")
            
            # 출력 경로 설정
            if output_path is None:
                output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                output_path = output_file.name
                output_file.close()
            
            base_path = str(Path(output_path).with_suffix(''))
            
            # yt-dlp 옵션 설정
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": base_path + '.%(ext)s',
                "ffmpeg_location": str(ffmpeg_bin_path),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "no_warnings": True,
            }
            
            print(f"[INFO] YouTube 오디오 다운로드 시작: {youtube_url}")
            print(f"[INFO] FFmpeg 경로: {ffmpeg_bin_path}")
            
            # YouTube 오디오 다운로드
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_url])
            except Exception as e:
                error_msg = (
                    f"YouTube 오디오 다운로드 실패: {str(e)}\n\n"
                    f"가능한 원인:\n"
                    f"1. YouTube URL이 유효하지 않습니다.\n"
                    f"2. 네트워크 연결 문제가 있습니다.\n"
                    f"3. FFmpeg 경로가 올바르지 않습니다: {ffmpeg_bin_path}\n"
                    f"4. FFmpeg가 제대로 설치되지 않았습니다."
                )
                if HAS_STREAMLIT and st:
                    st.error(error_msg)
                else:
                    print(f"[ERROR] {error_msg}")
                raise
            
            # 다운로드된 파일 찾기
            possible_paths = [
                base_path + '.mp3',
                output_path,
                base_path + '.m4a',
                base_path + '.webm',
                base_path + '.opus',
            ]
            
            for path_str in possible_paths:
                path = Path(path_str)
                if path.exists():
                    # MP3가 아니면 변환 필요 (이미 yt-dlp가 처리했을 가능성이 높음)
                    if path.suffix != '.mp3' and path_str != output_path:
                        # MP3로 변환 시도
                        import shutil
                        if shutil.which('ffmpeg') or ffmpeg_exists:
                            import subprocess
                            mp3_path = Path(output_path)
                            try:
                                subprocess.run([
                                    str(ffmpeg_bin_path / "ffmpeg.exe") if (ffmpeg_bin_path / "ffmpeg.exe").exists() else "ffmpeg",
                                    '-i', str(path),
                                    '-acodec', 'libmp3lame', '-ab', '192k',
                                    str(mp3_path), '-y'
                                ], check=True, capture_output=True, timeout=60)
                                if mp3_path.exists():
                                    path.unlink()  # 원본 파일 삭제
                                    return str(mp3_path)
                            except Exception as conv_e:
                                print(f"[WARN] MP3 변환 실패: {conv_e}")
                    return str(path)
            
            error_msg = "다운로드는 완료되었지만 파일을 찾을 수 없습니다."
            if HAS_STREAMLIT and st:
                st.error(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            return None
            
        except ImportError:
            raise  # yt-dlp import 오류는 그대로 전달
        except FileNotFoundError:
            raise  # FFmpeg 오류는 그대로 전달
        except Exception as e:
            error_msg = f"YouTube 오디오 다운로드 중 예상치 못한 오류: {str(e)}"
            if HAS_STREAMLIT and st:
                st.error(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            raise
