"""
FastAPI REST API Server
Provides REST endpoints for the React frontend
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
import os
import sys
from pathlib import Path
import tempfile
import json
import asyncio

# Windows 콘솔 인코딩 설정 (이모지 출력 오류 방지)
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables from .env file in project root
try:
    from dotenv import load_dotenv
    # Find project root (parent of src directory)
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[OK] .env 파일을 로드했습니다: {env_path}")
    else:
        print(f"[WARN] .env 파일을 찾을 수 없습니다: {env_path}")
        print("   프로젝트 루트에 .env 파일을 생성하고 API 키를 설정하세요.")
        # Try loading from current directory as fallback
        load_dotenv()
except ImportError:
    print("[WARN] python-dotenv가 설치되지 않았습니다. 환경 변수만 사용합니다.")
except Exception as e:
    print(f"[WARN] .env 파일 로드 중 오류: {str(e)}")

# Optional imports with error handling
try:
    from audio_processor import AudioProcessor
    HAS_AUDIO_PROCESSOR = True
except ImportError as e:
    print(f"[WARN] audio_processor를 불러올 수 없습니다: {e}")
    HAS_AUDIO_PROCESSOR = False
    AudioProcessor = None

try:
    from score_processor import ScoreProcessor
    HAS_SCORE_PROCESSOR = True
except ImportError as e:
    print(f"[WARN] score_processor를 불러올 수 없습니다: {e}")
    HAS_SCORE_PROCESSOR = False
    ScoreProcessor = None

try:
    from chord_generator import ChordGenerator
    HAS_CHORD_GENERATOR = True
except ImportError as e:
    print(f"[WARN] chord_generator를 불러올 수 없습니다: {e}")
    HAS_CHORD_GENERATOR = False
    ChordGenerator = None

try:
    from ai_assistant import AIAssistant
    HAS_AI_ASSISTANT = True
except ImportError as e:
    print(f"[WARN] ai_assistant를 불러올 수 없습니다: {e}")
    HAS_AI_ASSISTANT = False
    AIAssistant = None

try:
    from perplexity_assistant import PerplexityAssistant
    HAS_PERPLEXITY_ASSISTANT = True
except ImportError as e:
    print(f"[WARN] perplexity_assistant를 불러올 수 없습니다: {e}")
    HAS_PERPLEXITY_ASSISTANT = False
    PerplexityAssistant = None

try:
    from youtube_helper import YouTubeHelper
    HAS_YOUTUBE_HELPER = True
except ImportError as e:
    print(f"[WARN] youtube_helper를 불러올 수 없습니다: {e}")
    HAS_YOUTUBE_HELPER = False
    YouTubeHelper = None

try:
    from chord_analyzer import ChordAnalyzer
    HAS_CHORD_ANALYZER = True
except ImportError as e:
    print(f"[WARN] chord_analyzer를 불러올 수 없습니다: {e}")
    HAS_CHORD_ANALYZER = False
    ChordAnalyzer = None

# PDF Parser (optional)
try:
    from pdf_parser import PDFScoreParser
    HAS_PDF_PARSER = True
except ImportError:
    HAS_PDF_PARSER = False
    PDFScoreParser = None

# Initialize FastAPI app
app = FastAPI(title="초등 음악 도우미 API", version="1.0.0")

# CORS 설정 - React 프론트엔드에서 접근 가능하도록
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5176",  # Vite 개발 서버 다른 포트
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5176",
        "http://localhost:3001",
        "*",  # 개발 환경에서 모든 origin 허용
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # preflight 캐시 시간
)

# 전역 예외 핸들러 추가
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """전역 예외 처리"""
    import traceback
    error_detail = str(exc)
    print(f"[ERROR] 전역 예외 발생: {error_detail}")
    print(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": f"서버 오류가 발생했습니다: {error_detail}",
            "detail": error_detail
        }
    )

# Initialize processors (singleton pattern) with error handling
audio_processor = AudioProcessor() if HAS_AUDIO_PROCESSOR else None
score_processor = ScoreProcessor() if HAS_SCORE_PROCESSOR else None
chord_generator = ChordGenerator() if HAS_CHORD_GENERATOR else None
ai_assistant = AIAssistant() if HAS_AI_ASSISTANT else None
perplexity_assistant = PerplexityAssistant() if HAS_PERPLEXITY_ASSISTANT else None
youtube_helper = YouTubeHelper() if HAS_YOUTUBE_HELPER else None
chord_analyzer = ChordAnalyzer() if HAS_CHORD_ANALYZER else None

# Temporary storage for processed scores
score_storage = {}

@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "초등 음악 도우미 API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "keys": "/api/keys/status",
            "audio": "/api/audio/process",
            "score": "/api/score/process",
            "ai": "/api/ai/chat",
            "perplexity": "/api/perplexity/search",
            "youtube": "/api/youtube/search",
            "chord": "/api/chord/analyze",
        }
    }

@app.get("/api/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "message": "API is running",
        "modules": {
            "audio_processor": HAS_AUDIO_PROCESSOR,
            "score_processor": HAS_SCORE_PROCESSOR,
            "chord_generator": HAS_CHORD_GENERATOR,
            "ai_assistant": HAS_AI_ASSISTANT,
            "perplexity_assistant": HAS_PERPLEXITY_ASSISTANT,
            "youtube_helper": HAS_YOUTUBE_HELPER,
            "chord_analyzer": HAS_CHORD_ANALYZER,
        }
    }

@app.get("/api/keys/status")
async def get_api_keys_status():
    """API 키 상태 확인"""
    statuses = []
    
    if HAS_AI_ASSISTANT and ai_assistant:
        statuses.append({
            "name": "OpenAI",
            "status": "valid" if ai_assistant.api_key else "not_set",
            "message": "정상" if ai_assistant.api_key else "API 키가 설정되지 않았습니다"
        })
    else:
        statuses.append({
            "name": "OpenAI",
            "status": "not_available",
            "message": "AI Assistant 모듈을 불러올 수 없습니다"
        })
    
    if HAS_PERPLEXITY_ASSISTANT and perplexity_assistant:
        statuses.append({
            "name": "Perplexity",
            "status": "valid" if perplexity_assistant.api_key else "not_set",
            "message": "정상" if perplexity_assistant.api_key else "API 키가 설정되지 않았습니다"
        })
    else:
        statuses.append({
            "name": "Perplexity",
            "status": "not_available",
            "message": "Perplexity Assistant 모듈을 불러올 수 없습니다"
        })
    
    if HAS_YOUTUBE_HELPER and youtube_helper:
        statuses.append({
            "name": "YouTube",
            "status": "valid" if youtube_helper.api_key else "not_set",
            "message": "정상" if youtube_helper.api_key else "API 키가 설정되지 않았습니다"
        })
    else:
        statuses.append({
            "name": "YouTube",
            "status": "not_available",
            "message": "YouTube Helper 모듈을 불러올 수 없습니다"
        })
    
    return {"statuses": statuses}

# ==================== Audio Processing ====================

@app.post("/api/audio/process")
async def process_audio(file: UploadFile = File(...)):
    """오디오 또는 MIDI 파일을 악보로 변환"""
    try:
        # 파일 확장자 확인
        file_ext = file.filename.split('.')[-1].lower()
        
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # MIDI 파일인 경우 직접 악보로 변환
            if file_ext in ['mid', 'midi']:
                if not HAS_SCORE_PROCESSOR or not score_processor:
                    raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
                
                from music21 import converter
                score = converter.parse(tmp_path)
                score = score_processor.transpose_to_c_major(score)
                
                score_id = f"score_{len(score_storage)}"
                score_storage[score_id] = score
                
                return {
                    "success": True,
                    "scoreId": score_id,
                    "message": "MIDI 파일이 악보로 변환되었습니다.",
                    "note": "MIDI 파일은 직접 악보로 변환됩니다."
                }
            
            # 오디오 파일 처리
            if file_ext not in ['mp3', 'wav', 'mpeg']:
                raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다. MP3, WAV, 또는 MIDI 파일을 업로드하세요.")
            
            # 오디오 처리 모듈 확인
            if not HAS_AUDIO_PROCESSOR or not audio_processor:
                raise HTTPException(status_code=503, detail="Audio Processor 모듈을 사용할 수 없습니다.")
            
            # 오디오 처리
            try:
                score = audio_processor.process_audio_from_path(tmp_path)
            except Exception as e:
                import traceback
                error_detail = f"오디오 처리 중 오류 발생: {str(e)}"
                print(f"[ERROR] {error_detail}")
                print(traceback.format_exc())
                raise HTTPException(
                    status_code=500, 
                    detail=f"악보 생성에 실패했습니다. {error_detail}. basic-pitch가 설치되어 있는지 확인해주세요."
                )
            
            if score:
                score_id = f"score_{len(score_storage)}"
                score_storage[score_id] = score
                
                return {
                    "success": True,
                    "scoreId": score_id,
                    "message": "악보가 생성되었습니다.",
                    "note": "실제 악보 렌더링은 클라이언트에서 처리됩니다."
                }
            else:
                raise HTTPException(
                    status_code=500, 
                    detail="악보 생성에 실패했습니다. 오디오 파일을 확인해주세요. basic-pitch가 설치되어 있는지 확인하세요: pip install basic-pitch"
                )
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"오디오 처리 오류: {str(e)}"
        print(f"[ERROR] {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_detail)

# ==================== Score Processing ====================

@app.post("/api/score/process")
async def process_score(
    file: UploadFile = File(...),
    options: Optional[str] = Form(None)
):
    """악보 파일 처리"""
    try:
        # 옵션 파싱
        if options:
            try:
                options_dict = json.loads(options)
            except:
                options_dict = {}
        else:
            options_dict = {}
        
        addSolfege = options_dict.get("addSolfege", True)
        simplifyRhythm = options_dict.get("simplifyRhythm", True)
        transposeC = options_dict.get("transposeC", True)
        addChords = options_dict.get("addChords", True)
        
        # 파일 확장자 확인
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['mid', 'midi', 'xml', 'mxl', 'abc', 'musicxml']:
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
        
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Score Processor 모듈 확인
            if not HAS_SCORE_PROCESSOR or not score_processor:
                raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
            
            # 악보 로드
            score = score_processor.load_score_from_path(tmp_path)
            
            if not score:
                raise HTTPException(status_code=400, detail="악보를 불러올 수 없습니다. 파일 형식을 확인해주세요.")
            
            # 처리 옵션 적용
            if simplifyRhythm:
                score = score_processor.simplify_rhythm(score)
            
            if transposeC:
                score = score_processor.transpose_to_c_major(score)
            
            if addSolfege:
                score = score_processor.add_solfege(score)
            
            if addChords:
                if not HAS_CHORD_GENERATOR or not chord_generator:
                    print("[WARN] Chord Generator를 사용할 수 없어 화음 추가를 건너뜁니다.")
                else:
                    score = chord_generator.add_accompaniment(score)
            
            # 저장
            score_id = f"processed_{len(score_storage)}"
            score_storage[score_id] = score
            
            return {
                "success": True,
                "scoreId": score_id,
                "message": "악보 처리가 완료되었습니다.",
                "options": {
                    "addSolfege": addSolfege,
                    "simplifyRhythm": simplifyRhythm,
                    "transposeC": transposeC,
                    "addChords": addChords
                }
            }
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except:
                    pass
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"악보 처리 오류: {str(e)}"
        print(f"[ERROR] {error_detail}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/api/score/{score_id}/export/midi")
async def export_midi(score_id: str):
    """MIDI 파일을 MP3로 변환하여 내보내기"""
    if score_id not in score_storage:
        raise HTTPException(status_code=404, detail="악보를 찾을 수 없습니다.")
    
    if not HAS_SCORE_PROCESSOR or not score_processor:
        raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
    
    try:
        score = score_storage[score_id]
        midi_bytes = score_processor.export_midi(score)
        
        if midi_bytes:
            # MIDI를 MP3로 변환
            mp3_bytes = await convert_midi_to_mp3(midi_bytes)
            
            if mp3_bytes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(mp3_bytes)
                    tmp_path = tmp_file.name
                
                return FileResponse(
                    tmp_path,
                    media_type="audio/mpeg",
                    filename="processed_score.mp3"
                )
            else:
                # MP3 변환 실패 시 MIDI 파일 반환
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp_file:
                    tmp_file.write(midi_bytes)
                    tmp_path = tmp_file.name
                
                return FileResponse(
                    tmp_path,
                    media_type="audio/midi",
                    filename="processed_score.mid"
                )
        else:
            raise HTTPException(status_code=500, detail="MIDI 내보내기 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 내보내기 오류: {str(e)}")

async def convert_pdf_or_image_to_score(file_path: str, file_ext: str):
    """PDF 또는 이미지 파일을 악보로 변환"""
    try:
        from music21 import converter
        import shutil
        
        # PDF 파일인 경우
        if file_ext == 'pdf':
            if HAS_PDF_PARSER and PDFScoreParser:
                pdf_parser = PDFScoreParser()
                
                # 방법 1: Audiveris를 사용한 OMR (가능한 경우)
                xml_path = pdf_parser.parse_pdf_with_audiveris(file_path)
                if xml_path and os.path.exists(xml_path):
                    score = converter.parse(xml_path)
                    return score
                
                # 방법 2: PDF를 이미지로 변환 후 처리
                image_paths = pdf_parser.convert_pdf_to_images(file_path)
                if image_paths:
                    # 첫 번째 페이지 이미지로 처리
                    return await convert_image_to_score(image_paths[0])
            else:
                print("PDF 파서가 사용할 수 없습니다.")
                return None
        
        # 이미지 파일인 경우
        elif file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            return await convert_image_to_score(file_path)
        
        return None
        
    except Exception as e:
        print(f"PDF/이미지 변환 오류: {str(e)}")
        return None

async def convert_image_to_score(image_path: str):
    """이미지 파일을 악보로 변환 (OMR 사용)"""
    try:
        from music21 import converter
        import subprocess
        import shutil
        
        # 방법 1: Audiveris를 사용한 OMR
        if shutil.which('audiveris'):
            output_dir = tempfile.mkdtemp()
            try:
                result = subprocess.run([
                    'audiveris',
                    '-batch',
                    '-export',
                    '-output', output_dir,
                    image_path
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    # 생성된 MusicXML 파일 찾기
                    xml_files = []
                    for ext in ['*.mxl', '*.xml']:
                        xml_files.extend(Path(output_dir).glob(ext))
                    
                    if xml_files:
                        score = converter.parse(str(xml_files[0]))
                        return score
            finally:
                # 임시 디렉토리 정리
                import shutil
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir, ignore_errors=True)
        
        # 방법 2: 기본 악보 생성 (실제 OMR 없이)
        # 실제 구현에서는 OMR 라이브러리 필요
        # 여기서는 기본 구조만 반환
        print("OMR 도구가 필요합니다. Audiveris를 설치하거나 이미지를 MusicXML로 변환해주세요.")
        return None
        
    except Exception as e:
        print(f"이미지 변환 오류: {str(e)}")
        return None

async def convert_midi_to_mp3(midi_bytes: bytes) -> Optional[bytes]:
    """MIDI 파일을 MP3로 변환 (Python 라이브러리 사용)"""
    try:
        # pydub와 simpleaudio를 사용한 변환 시도
        try:
            from pydub import AudioSegment
            from pydub.utils import which
            import subprocess
            import shutil
            
            # MIDI를 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as midi_file:
                midi_file.write(midi_bytes)
                midi_path = midi_file.name
            
            # 방법 1: ffmpeg를 사용하여 직접 MIDI -> MP3 변환
            if shutil.which('ffmpeg'):
                mp3_path = midi_path.replace('.mid', '.mp3')
                try:
                    subprocess.run(
                        ['ffmpeg', '-i', midi_path, '-acodec', 'libmp3lame', '-ab', '192k', mp3_path, '-y'],
                        check=True,
                        capture_output=True,
                        timeout=30
                    )
                    
                    with open(mp3_path, 'rb') as f:
                        mp3_bytes = f.read()
                    
                    # 임시 파일 정리
                    for path in [midi_path, mp3_path]:
                        if os.path.exists(path):
                            os.unlink(path)
                    
                    return mp3_bytes
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    # 변환 실패 시 정리
                    for path in [midi_path, mp3_path]:
                        if os.path.exists(path):
                            try:
                                os.unlink(path)
                            except:
                                pass
                    return None
            
            # 방법 2: timidity + ffmpeg 사용
            if shutil.which('timidity') and shutil.which('ffmpeg'):
                wav_path = midi_path.replace('.mid', '.wav')
                try:
                    # MIDI -> WAV
                    subprocess.run(
                        ['timidity', midi_path, '-Ow', '-o', wav_path],
                        check=True,
                        capture_output=True,
                        timeout=30
                    )
                    
                    # WAV -> MP3
                    mp3_path = wav_path.replace('.wav', '.mp3')
                    subprocess.run(
                        ['ffmpeg', '-i', wav_path, '-acodec', 'libmp3lame', '-ab', '192k', mp3_path, '-y'],
                        check=True,
                        capture_output=True,
                        timeout=30
                    )
                    
                    with open(mp3_path, 'rb') as f:
                        mp3_bytes = f.read()
                    
                    # 임시 파일 정리
                    for path in [midi_path, wav_path, mp3_path]:
                        if os.path.exists(path):
                            try:
                                os.unlink(path)
                            except:
                                pass
                    
                    return mp3_bytes
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    # 변환 실패 시 정리
                    for path in [midi_path, wav_path]:
                        if os.path.exists(path):
                            try:
                                os.unlink(path)
                            except:
                                pass
                    return None
            
            # 변환 도구가 없으면 MIDI 파일 정리 후 None 반환
            if os.path.exists(midi_path):
                os.unlink(midi_path)
            return None
            
        except ImportError:
            # pydub가 없으면 외부 도구만 사용
            import subprocess
            import shutil
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as midi_file:
                midi_file.write(midi_bytes)
                midi_path = midi_file.name
            
            if shutil.which('ffmpeg'):
                mp3_path = midi_path.replace('.mid', '.mp3')
                try:
                    subprocess.run(
                        ['ffmpeg', '-i', midi_path, '-acodec', 'libmp3lame', '-ab', '192k', mp3_path, '-y'],
                        check=True,
                        capture_output=True,
                        timeout=30
                    )
                    
                    with open(mp3_path, 'rb') as f:
                        mp3_bytes = f.read()
                    
                    for path in [midi_path, mp3_path]:
                        if os.path.exists(path):
                            try:
                                os.unlink(path)
                            except:
                                pass
                    
                    return mp3_bytes
                except:
                    if os.path.exists(midi_path):
                        os.unlink(midi_path)
                    return None
            
            if os.path.exists(midi_path):
                os.unlink(midi_path)
            return None
        
    except Exception as e:
        print(f"MIDI to MP3 변환 오류: {str(e)}")
        return None

@app.get("/api/score/{score_id}/export/mp3")
async def export_mp3(score_id: str):
    """MP3 파일로 내보내기 (MIDI를 MP3로 변환)"""
    if score_id not in score_storage:
        raise HTTPException(status_code=404, detail="악보를 찾을 수 없습니다.")
    
    if not HAS_SCORE_PROCESSOR or not score_processor:
        raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
    
    try:
        score = score_storage[score_id]
        midi_bytes = score_processor.export_midi(score)
        
        if midi_bytes:
            # MIDI를 MP3로 변환
            mp3_bytes = await convert_midi_to_mp3(midi_bytes)
            
            if mp3_bytes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(mp3_bytes)
                    tmp_path = tmp_file.name
                
                return FileResponse(
                    tmp_path,
                    media_type="audio/mpeg",
                    filename="processed_score.mp3"
                )
            else:
                raise HTTPException(
                    status_code=500, 
                    detail="MP3 변환에 실패했습니다. ffmpeg 또는 timidity가 설치되어 있는지 확인하세요."
                )
        else:
            raise HTTPException(status_code=500, detail="MIDI 내보내기 실패")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MP3 내보내기 오류: {str(e)}")

@app.get("/api/score/{score_id}/export/musicxml")
async def export_musicxml(score_id: str):
    """MusicXML 파일로 내보내기"""
    if score_id not in score_storage:
        raise HTTPException(status_code=404, detail="악보를 찾을 수 없습니다.")
    
    if not HAS_SCORE_PROCESSOR or not score_processor:
        raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
    
    try:
        score = score_storage[score_id]
        xml_bytes = score_processor.export_musicxml(score)
        
        if xml_bytes:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp_file:
                tmp_file.write(xml_bytes)
                tmp_path = tmp_file.name
            
            return FileResponse(
                tmp_path,
                media_type="application/xml",
                filename="processed_score.xml"
            )
        else:
            raise HTTPException(status_code=500, detail="MusicXML 내보내기 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MusicXML 내보내기 오류: {str(e)}")

# ==================== AI Assistant ====================

@app.post("/api/ai/chat")
async def ai_chat(request: dict):
    """AI 채팅"""
    question = request.get("question")
    context = request.get("context")
    
    if not question:
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")
    
    try:
        # 최신 OpenAI API 사용
        if not HAS_AI_ASSISTANT or not ai_assistant:
            return {
                "success": False,
                "error": "AI Assistant 모듈을 사용할 수 없습니다."
            }
        
        if not HAS_AI_ASSISTANT or not ai_assistant:
            return {
                "success": False,
                "error": "AI Assistant 모듈을 사용할 수 없습니다."
            }
        
        if not ai_assistant.api_key:
            return {
                "success": False,
                "error": "OpenAI API 키가 설정되지 않았습니다."
            }
        
        from openai import OpenAI
        client = OpenAI(api_key=ai_assistant.api_key)
        
        messages = [
            {"role": "system", "content": "당신은 초등학교 음악 교육 전문가입니다. 학생과 교사를 도와주세요."}
        ]
        
        if context:
            messages.append({"role": "system", "content": f"현재 상황: {context}"})
        
        # 대화 기록 추가
        messages.extend(ai_assistant.conversation_history[-5:])
        messages.append({"role": "user", "content": question})
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # 대화 기록 업데이트
        ai_assistant.conversation_history.append({"role": "user", "content": question})
        ai_assistant.conversation_history.append({"role": "assistant", "content": ai_response})
        
        return {
            "success": True,
            "response": ai_response
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"AI 채팅 오류: {str(e)}"
        }

@app.post("/api/ai/explain-theory")
async def explain_theory(request: dict):
    """음악 이론 설명"""
    topic = request.get("topic")
    age = request.get("age", 10)
    
    if not topic:
        raise HTTPException(status_code=400, detail="주제를 입력해주세요.")
    
    try:
        if not HAS_AI_ASSISTANT or not ai_assistant:
            return {
                "success": False,
                "error": "AI Assistant 모듈을 사용할 수 없습니다."
            }
        
        if not ai_assistant.api_key:
            return {
                "success": False,
                "error": "OpenAI API 키가 설정되지 않았습니다."
            }
        
        from openai import OpenAI
        client = OpenAI(api_key=ai_assistant.api_key)
        
        prompt = f"""{age}살 초등학생에게 '{topic}'에 대해 쉽게 설명해주세요.

요구사항:
- 쉬운 단어 사용
- 실생활 예시 포함
- 3-4문장으로 간단하게
- 재미있고 이해하기 쉽게"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 어린이에게 음악을 가르치는 선생님입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )
        
        explanation = response.choices[0].message.content.strip()
        
        return {
            "success": True,
            "explanation": explanation
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"이론 설명 오류: {str(e)}"
        }

@app.post("/api/ai/lesson-plan")
async def generate_lesson_plan(request: dict):
    """수업 계획 생성"""
    song_title = request.get("songTitle")
    grade = request.get("grade", "3-4학년")
    duration = request.get("duration", 40)
    
    if not song_title:
        raise HTTPException(status_code=400, detail="곡 제목을 입력해주세요.")
    
    try:
        if not HAS_AI_ASSISTANT or not ai_assistant:
            return {
                "success": False,
                "error": "AI Assistant 모듈을 사용할 수 없습니다."
            }
        
        if not ai_assistant.api_key:
            return {
                "success": False,
                "error": "OpenAI API 키가 설정되지 않았습니다."
            }
        
        from openai import OpenAI
        client = OpenAI(api_key=ai_assistant.api_key)
        
        prompt = f"""초등학교 {grade} 학생들을 대상으로 '{song_title}'를 가르치는 {duration}분 수업 계획을 작성해주세요.

다음 형식으로 작성:
도입 (5분): [활동 설명]
전개 (25분): [단계별 활동]
정리 (10분): [마무리 활동]

각 부분은 2-3문장으로 간단하게 작성해주세요."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 경험 많은 초등학교 음악 교사입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        lesson_plan = response.choices[0].message.content.strip()
        
        return {
            "success": True,
            "plan": lesson_plan
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"수업 계획 생성 오류: {str(e)}"
        }

# ==================== Perplexity ====================

@app.post("/api/perplexity/search")
async def perplexity_search(request: dict):
    """Perplexity 검색"""
    query = request.get("query")
    search_type = request.get("searchType", "음악 이론 조사")
    
    if not query:
        raise HTTPException(status_code=400, detail="검색어를 입력해주세요.")
    
    try:
        # 검색 유형에 따라 다른 메서드 호출
        if search_type == "음악 이론 조사":
            result = perplexity_assistant.search_music_theory(query)
        elif search_type == "곡 배경 정보":
            result = perplexity_assistant.research_song_background(query)
        elif search_type == "교육 자료 찾기":
            result = perplexity_assistant.find_teaching_resources(query, "3-4학년")
        elif search_type == "최신 트렌드":
            if hasattr(perplexity_assistant, 'get_latest_education_trends'):
                result = perplexity_assistant.get_latest_education_trends(query)
            else:
                result = perplexity_assistant.search_music_theory(f"{query} 최신 트렌드")
        elif search_type == "교수법 비교":
            if hasattr(perplexity_assistant, 'compare_teaching_methods'):
                # 두 개의 교수법이 필요하므로 기본 검색 사용
                result = perplexity_assistant.search_music_theory(f"{query} 교수법 비교")
            else:
                result = perplexity_assistant.search_music_theory(f"{query} 교수법 비교")
        else:
            result = perplexity_assistant.search_music_theory(query)
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Perplexity 검색 오류: {str(e)}")

# ==================== YouTube ====================

@app.post("/api/youtube/search")
async def youtube_search(request: dict):
    """YouTube 검색"""
    query = request.get("query")
    max_results = request.get("maxResults", 5)
    
    if not query:
        raise HTTPException(status_code=400, detail="검색어를 입력해주세요.")
    
    try:
        videos = youtube_helper.search_education_videos(query, max_results)
        return {
            "success": True,
            "videos": videos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YouTube 검색 오류: {str(e)}")

# ==================== Chord Analysis ====================

@app.post("/api/chord/analyze")
async def analyze_chord(
    file: UploadFile = File(...),
    fileType: str = Form("midi")
):
    """화음 분석"""
    try:
        # 임시 파일로 저장
        file_ext = file.filename.split('.')[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            score = None
            
            # 모듈 확인
            if not HAS_SCORE_PROCESSOR or not score_processor:
                raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
            
            # 파일 타입에 따라 처리
            if fileType == "midi" or file_ext in ['mid', 'midi']:
                # MIDI 파일 직접 처리
                from music21 import converter
                score = converter.parse(tmp_path)
                score = score_processor.transpose_to_c_major(score)
                
            elif fileType == "audio" or file_ext in ['mp3', 'wav', 'mpeg']:
                # 오디오 파일을 MIDI로 변환 후 처리
                if not HAS_AUDIO_PROCESSOR or not audio_processor:
                    raise HTTPException(status_code=503, detail="Audio Processor 모듈을 사용할 수 없습니다.")
                
                score = audio_processor.process_audio_from_path(tmp_path)
                if score:
                    score = score_processor.transpose_to_c_major(score)
                else:
                    raise HTTPException(status_code=500, detail="오디오 파일을 MIDI로 변환하는데 실패했습니다.")
            
            elif fileType == "pdf" or file_ext == 'pdf':
                # PDF 파일을 악보로 변환
                score = await convert_pdf_or_image_to_score(tmp_path, file_ext)
                if score:
                    score = score_processor.transpose_to_c_major(score)
                else:
                    raise HTTPException(status_code=500, detail="PDF 파일을 악보로 변환하는데 실패했습니다. OMR 도구가 필요할 수 있습니다.")
            
            elif fileType == "image" or file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                # 이미지 파일을 악보로 변환
                score = await convert_pdf_or_image_to_score(tmp_path, file_ext)
                if score:
                    score = score_processor.transpose_to_c_major(score)
                else:
                    raise HTTPException(status_code=500, detail="이미지 파일을 악보로 변환하는데 실패했습니다. OMR 도구가 필요할 수 있습니다.")
            
            if score:
                # 화음 분석
                if not HAS_CHORD_ANALYZER or not chord_analyzer:
                    raise HTTPException(status_code=503, detail="Chord Analyzer 모듈을 사용할 수 없습니다.")
                
                chords_info = chord_analyzer.analyze_midi_chords(score)
                
                if chords_info:
                    chords = [chord['chord_name'] for chord in chords_info[:8]]
                    
                    # 각 화음의 음표 정보를 포함하여 반환
                    chords_info_with_notes = []
                    for chord_info in chords_info[:8]:
                        chord_data = {
                            'measure': chord_info.get('measure', 0),
                            'chord_name': chord_info.get('chord_name', ''),
                            'notes': chord_info.get('notes', []),
                            'root': chord_info.get('root', ''),
                            'quality': chord_info.get('quality', '')
                        }
                        chords_info_with_notes.append(chord_data)
                    
                    return {
                        "success": True,
                        "message": f"화음 분석이 완료되었습니다. {len(chords_info)}개 마디를 분석했습니다.",
                        "chords": chords,
                        "chordsInfo": chords_info_with_notes,  # 음표 정보 포함
                        "totalMeasures": len(chords_info)
                    }
                else:
                    raise HTTPException(status_code=500, detail="화음 분석에 실패했습니다.")
            else:
                raise HTTPException(status_code=500, detail="악보를 생성할 수 없습니다.")
                
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"화음 분석 오류: {str(e)}")

@app.post("/api/chord/analyze-youtube")
async def analyze_chord_youtube(request: dict):
    """YouTube URL에서 화음 분석"""
    youtube_url = request.get("youtubeUrl")
    
    if not youtube_url:
        raise HTTPException(status_code=400, detail="YouTube URL을 입력해주세요.")
    
    # YouTube URL 검증
    import re
    youtube_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, youtube_url)
    if not match:
        raise HTTPException(status_code=400, detail="유효한 YouTube URL을 입력해주세요.")
    
    video_id = match.group(1)
    temp_audio_path = None
    
    try:
        # yt-dlp를 사용하여 오디오 다운로드
        import subprocess
        import shutil
        
        if not shutil.which('yt-dlp'):
            raise HTTPException(status_code=500, detail="yt-dlp가 설치되지 않았습니다. 서버에 yt-dlp를 설치해주세요.")
        
        # 임시 오디오 파일 경로
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        
        # YouTube 오디오 다운로드
        result = subprocess.run([
            'yt-dlp',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--audio-quality', '0',
            '--output', temp_audio_path.replace('.mp3', ''),
            '--no-playlist',
            youtube_url
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"YouTube 오디오 다운로드 실패: {result.stderr}")
        
        # 실제 다운로드된 파일 경로 찾기 (yt-dlp가 확장자를 추가할 수 있음)
        possible_paths = [
            temp_audio_path,
            temp_audio_path.replace('.mp3', ''),
            temp_audio_path.replace('.mp3', '.m4a'),
            temp_audio_path.replace('.mp3', '.webm'),
        ]
        
        actual_audio_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_audio_path = path
                break
        
        if not actual_audio_path:
            raise HTTPException(status_code=500, detail="다운로드된 오디오 파일을 찾을 수 없습니다.")
        
        # 모듈 확인
        if not HAS_AUDIO_PROCESSOR or not audio_processor:
            raise HTTPException(status_code=503, detail="Audio Processor 모듈을 사용할 수 없습니다.")
        
        if not HAS_SCORE_PROCESSOR or not score_processor:
            raise HTTPException(status_code=503, detail="Score Processor 모듈을 사용할 수 없습니다.")
        
        if not HAS_CHORD_ANALYZER or not chord_analyzer:
            raise HTTPException(status_code=503, detail="Chord Analyzer 모듈을 사용할 수 없습니다.")
        
        # 오디오를 MIDI로 변환
        score = audio_processor.process_audio_from_path(actual_audio_path)
        if not score:
            raise HTTPException(status_code=500, detail="오디오 파일을 MIDI로 변환하는데 실패했습니다.")
        
        # 다장조로 변환
        score = score_processor.transpose_to_c_major(score)
        
        # 화음 분석
        chords_info = chord_analyzer.analyze_midi_chords(score)
        
        if chords_info:
            chords = [chord['chord_name'] for chord in chords_info[:8]]
            
            # 각 화음의 음표 정보를 포함하여 반환
            chords_info_with_notes = []
            for chord_info in chords_info[:8]:
                chord_data = {
                    'measure': chord_info.get('measure', 0),
                    'chord_name': chord_info.get('chord_name', ''),
                    'notes': chord_info.get('notes', []),
                    'root': chord_info.get('root', ''),
                    'quality': chord_info.get('quality', '')
                }
                chords_info_with_notes.append(chord_data)
            
            return {
                "success": True,
                "message": f"YouTube 음원 화음 분석이 완료되었습니다. {len(chords_info)}개 마디를 분석했습니다.",
                "chords": chords,
                "chordsInfo": chords_info_with_notes,
                "totalMeasures": len(chords_info)
            }
        else:
            raise HTTPException(status_code=500, detail="화음 분석에 실패했습니다.")
            
    except HTTPException:
        raise
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="YouTube 오디오 다운로드 시간이 초과되었습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YouTube 화음 분석 오류: {str(e)}")
    finally:
        # 임시 파일 정리
        if temp_audio_path:
            for path in [temp_audio_path, temp_audio_path.replace('.mp3', ''), 
                         temp_audio_path.replace('.mp3', '.m4a'), 
                         temp_audio_path.replace('.mp3', '.webm')]:
                if os.path.exists(path):
                    try:
                        os.unlink(path)
                    except:
                        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)

