"""
개선된 오디오 업로드 및 악보 변환 엔드포인트
MP3 -> WAV -> MIDI -> MusicXML 변환 파이프라인
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import tempfile
import os
from pathlib import Path
from typing import Optional
import traceback

# 의존성 확인 및 import
try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    print("[WARN] pydub가 설치되지 않았습니다. pip install pydub를 실행해주세요.")

try:
    from basic_pitch.inference import predict as basic_pitch_predict
    HAS_BASIC_PITCH = True
except ImportError:
    HAS_BASIC_PITCH = False
    print("[WARN] basic-pitch가 설치되지 않았습니다. pip install basic-pitch를 실행해주세요.")

try:
    from music21 import converter
    HAS_MUSIC21 = True
except ImportError:
    HAS_MUSIC21 = False
    print("[WARN] music21이 설치되지 않았습니다. pip install music21을 실행해주세요.")


async def upload_audio_to_musicxml(
    file: UploadFile,
    output_format: str = "musicxml"
) -> dict:
    """
    오디오 파일을 업로드하여 MusicXML로 변환
    
    Args:
        file: 업로드된 오디오 파일
        output_format: 출력 형식 ("musicxml" 또는 "midi")
        
    Returns:
        dict: 변환 결과 및 파일 경로 정보
    """
    temp_files = []  # 정리할 임시 파일 목록
    
    try:
        # 1. 파일 확장자 확인
        file_ext = file.filename.split('.')[-1].lower() if file.filename else 'mp3'
        if file_ext not in ['mp3', 'wav', 'mpeg', 'wma', 'flac', 'ogg']:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 파일 형식입니다: {file_ext}. MP3, WAV 파일을 업로드해주세요."
            )
        
        # 2. 임시 파일로 저장
        with tempfile.NamedTemporaryFile(suffix=f".{file_ext}", delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            mp3_path = tmp.name
            temp_files.append(mp3_path)
        
        # 3. MP3 -> WAV 변환 (pydub 사용)
        if not HAS_PYDUB:
            raise HTTPException(
                status_code=503,
                detail="pydub가 설치되지 않았습니다. pip install pydub를 실행해주세요."
            )
        
        try:
            audio = AudioSegment.from_file(mp3_path, format=file_ext)
            wav_path = mp3_path.replace(f".{file_ext}", ".wav")
            audio.export(wav_path, format="wav")
            temp_files.append(wav_path)
            print(f"[INFO] WAV 변환 완료: {wav_path}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"오디오 파일 변환 실패: {str(e)}"
            )
        
        # 4. WAV -> MIDI 변환 (basic-pitch)
        if not HAS_BASIC_PITCH:
            raise HTTPException(
                status_code=503,
                detail="basic-pitch가 설치되지 않았습니다. pip install basic-pitch를 실행해주세요."
            )
        
        midi_path = wav_path.replace(".wav", ".mid")
        try:
            # basic-pitch로 MIDI 생성
            basic_pitch_predict(wav_path, midi_path)
            temp_files.append(midi_path)
            print(f"[INFO] MIDI 변환 완료: {midi_path}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"MIDI 변환 실패: {str(e)}. 오디오 파일에 명확한 멜로디가 있는지 확인해주세요."
            )
        
        # 5. MIDI -> MusicXML 변환 (music21)
        if not HAS_MUSIC21:
            raise HTTPException(
                status_code=503,
                detail="music21이 설치되지 않았습니다. pip install music21을 실행해주세요."
            )
        
        musicxml_path = midi_path.replace(".mid", ".musicxml")
        try:
            score = converter.parse(midi_path)
            score.write("musicxml", fp=musicxml_path)
            temp_files.append(musicxml_path)
            print(f"[INFO] MusicXML 변환 완료: {musicxml_path}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"MusicXML 변환 실패: {str(e)}"
            )
        
        # 6. 결과 반환
        result = {
            "success": True,
            "message": "오디오 파일이 성공적으로 악보로 변환되었습니다.",
            "files": {
                "original": file.filename,
                "wav": os.path.basename(wav_path),
                "midi": os.path.basename(midi_path),
                "musicxml": os.path.basename(musicxml_path)
            },
            "paths": {
                "wav_path": wav_path,
                "midi_path": midi_path,
                "musicxml_path": musicxml_path
            },
            "temp_files": temp_files  # 정리용 (실제로는 반환하지 않아도 됨)
        }
        
        return result
        
    except HTTPException:
        # HTTPException은 그대로 전달
        raise
    except Exception as e:
        # 예상치 못한 오류 발생 시 임시 파일 정리
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception:
                pass
        
        error_detail = str(e)
        print(f"[ERROR] 오디오 변환 중 오류 발생: {error_detail}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"오디오 처리 중 오류가 발생했습니다: {error_detail}"
        )


def cleanup_temp_files(file_paths: list):
    """
    임시 파일 정리
    
    Args:
        file_paths: 삭제할 파일 경로 목록
    """
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                print(f"[INFO] 임시 파일 삭제: {file_path}")
        except Exception as e:
            print(f"[WARN] 임시 파일 삭제 실패 ({file_path}): {str(e)}")


# 사용 예시 (api_server.py에 통합할 경우):
"""
@app.post("/api/audio/upload-to-musicxml")
async def upload_audio_to_musicxml_endpoint(file: UploadFile = File(...)):
    \"\"\"오디오 파일을 업로드하여 MusicXML로 변환\"\"\"
    result = await upload_audio_to_musicxml(file)
    
    # MusicXML 파일 다운로드 제공
    return FileResponse(
        result["paths"]["musicxml_path"],
        media_type="application/xml",
        filename=result["files"]["musicxml"]
    )

@app.get("/api/audio/download/{file_type}")
async def download_converted_file(file_type: str, file_path: str):
    \"\"\"변환된 파일 다운로드\"\"\"
    if file_type not in ["wav", "midi", "musicxml"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    media_types = {
        "wav": "audio/wav",
        "midi": "audio/midi",
        "musicxml": "application/xml"
    }
    
    return FileResponse(
        file_path,
        media_type=media_types.get(file_type, "application/octet-stream"),
        filename=os.path.basename(file_path)
    )
"""

