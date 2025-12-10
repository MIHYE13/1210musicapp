"""
YouTube Audio Downloader
Download audio from YouTube for music analysis
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

from typing import Optional, Dict
import re
import requests
import subprocess
import os
import shutil
from pathlib import Path

def get_ffmpeg_path() -> Optional[str]:
    """
    FFmpeg 경로 찾기
    1. 환경 변수 FFMPEG_PATH 확인
    2. 일반적인 설치 경로 확인
    3. PATH에서 ffmpeg 찾기
    
    Returns:
        FFmpeg bin 디렉토리 경로 또는 None
    """
    # 1. 환경 변수에서 확인
    ffmpeg_path = os.getenv("FFMPEG_PATH")
    if ffmpeg_path:
        ffmpeg_bin = Path(ffmpeg_path) / "bin"
        if (ffmpeg_bin / "ffmpeg.exe").exists() or (ffmpeg_bin / "ffmpeg").exists():
            return str(ffmpeg_bin)
    
    # 2. 일반적인 Windows 경로 확인
    common_paths = [
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
    ]
    
    for path_str in common_paths:
        path = Path(path_str)
        if (path / "ffmpeg.exe").exists():
            return str(path)
    
    # 3. PATH에서 ffmpeg 찾기
    ffmpeg_exe = shutil.which("ffmpeg")
    if ffmpeg_exe:
        ffmpeg_path = Path(ffmpeg_exe).parent
        return str(ffmpeg_path)
    
    return None

class YouTubeDownloader:
    """Download audio from YouTube videos"""
    
    def __init__(self):
        self.download_dir = Path("temp/youtube")
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID or None
        """
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """
        Get video information using yt-dlp
        
        Args:
            url: YouTube URL
            
        Returns:
            Dictionary with video info
        """
        try:
            # Use yt-dlp Python module
            try:
                import yt_dlp
            except ImportError:
                if HAS_STREAMLIT and st:
                    st.warning("yt-dlp가 설치되지 않았습니다. pip install yt-dlp를 실행해주세요.")
                else:
                    print("[WARN] yt-dlp가 설치되지 않았습니다.")
                return None
            
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'id': info.get('id', ''),
                }
                
        except Exception as e:
            error_msg = f"yt-dlp를 사용할 수 없습니다: {str(e)}"
            if HAS_STREAMLIT and st:
                st.warning(error_msg)
            else:
                print(f"[WARN] {error_msg}")
            return None
    
    def download_audio(self, url: str) -> Optional[str]:
        """
        Download audio from YouTube
        
        Args:
            url: YouTube URL
            
        Returns:
            Path to downloaded audio file
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            return None
        
        output_path = self.download_dir / f"{video_id}.mp3"
        
        # Check if already downloaded
        if output_path.exists():
            return str(output_path)
        
        try:
            # Use yt-dlp Python module to download
            try:
                import yt_dlp
            except ImportError:
                if HAS_STREAMLIT and st:
                    st.error("yt-dlp가 설치되지 않았습니다. pip install yt-dlp를 실행해주세요.")
                else:
                    print("[ERROR] yt-dlp가 설치되지 않았습니다. pip install yt-dlp를 실행해주세요.")
                return None
            
            # yt-dlp 옵션 설정
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": str(output_path.with_suffix('')) + '.%(ext)s',
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "no_warnings": True,
            }
            
            # FFmpeg 경로 설정 (있는 경우)
            ffmpeg_path = get_ffmpeg_path()
            if ffmpeg_path:
                ydl_opts["ffmpeg_location"] = ffmpeg_path
                print(f"[INFO] FFmpeg 경로 설정: {ffmpeg_path}")
            else:
                print("[WARN] FFmpeg 경로를 찾을 수 없습니다. PATH에 ffmpeg가 있는지 확인하세요.")
            
            # YouTube 오디오 다운로드
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 다운로드된 파일 찾기
            possible_paths = [
                output_path,
                output_path.with_suffix('.m4a'),
                output_path.with_suffix('.webm'),
                output_path.with_suffix('.opus'),
            ]
            
            for path in possible_paths:
                if path.exists():
                    # MP3가 아니면 변환 필요
                    if path.suffix != '.mp3':
                        # FFmpeg로 변환 (있는 경우)
                        if shutil.which('ffmpeg'):
                            import subprocess
                            subprocess.run([
                                'ffmpeg', '-i', str(path), 
                                '-acodec', 'libmp3lame', '-ab', '192k',
                                str(output_path), '-y'
                            ], capture_output=True, timeout=30)
                            if output_path.exists():
                                path.unlink()  # 원본 파일 삭제
                                return str(output_path)
                    return str(path)
            
            return None
                
        except Exception as e:
            error_msg = f"다운로드 실패: {str(e)}"
            if HAS_STREAMLIT and st:
                st.error(error_msg)
            else:
                print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            return None
        except Exception as e:
            st.error(f"다운로드 오류: {str(e)}")
            return None
    
    def download_with_fallback(self, url: str) -> Optional[str]:
        """
        Download with fallback methods
        
        Args:
            url: YouTube URL
            
        Returns:
            Path to audio file or None
        """
        # Method 1: Try yt-dlp
        audio_path = self.download_audio(url)
        if audio_path:
            return audio_path
        
        # Method 2: Inform user about manual download
        st.info("""
        **자동 다운로드가 실패했습니다.**
        
        수동으로 다운로드하는 방법:
        1. YouTube 영상 열기
        2. 온라인 YouTube to MP3 변환기 사용
           - https://ytmp3.cc
           - https://www.y2mate.com
        3. 다운로드한 MP3 파일을 여기에 업로드
        """)
        
        return None
    
    def validate_url(self, url: str) -> bool:
        """
        Validate YouTube URL
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid YouTube URL
        """
        patterns = [
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/',
            r'(https?://)?(www\.)?youtube\.com/watch\?v=',
            r'(https?://)?(www\.)?youtu\.be/'
        ]
        
        return any(re.match(pattern, url) for pattern in patterns)


# Fallback: YouTube URL to downloadable audio guide
def get_youtube_download_guide(url: str) -> str:
    """Generate guide for manual YouTube download"""
    
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    video_id = video_id.group(1) if video_id else ''
    
    return f"""
## 📺 YouTube 음원 다운로드 가이드

**영상 링크**: {url}

### 방법 1: yt-dlp 설치 (권장)

로컬 환경에서 다음 명령어 실행:

```bash
# yt-dlp 설치
pip install yt-dlp

# 오디오 다운로드
yt-dlp -x --audio-format mp3 "{url}"
```

### 방법 2: 온라인 변환기

1. **ytmp3.cc** 방문
   - URL: https://ytmp3.cc
   - YouTube 링크 붙여넣기
   - "Convert" 클릭
   - MP3 다운로드

2. **y2mate.com** 방문
   - URL: https://www.y2mate.com
   - 링크 입력
   - "Start" 클릭
   - MP3 다운로드

3. **다운로드한 파일을 왼쪽 '오디오 → 악보 변환'에 업로드**

### 방법 3: 브라우저 확장 프로그램

- Chrome: "YouTube Audio Downloader"
- Firefox: "YouTube Audio"

---

다운로드 후 메인 페이지의 **"오디오 → 악보 변환"**에서 파일을 업로드하세요!
"""
