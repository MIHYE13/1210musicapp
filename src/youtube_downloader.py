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
from pathlib import Path

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
            # Check if yt-dlp is installed
            result = subprocess.run(
                ['yt-dlp', '--dump-json', '--no-playlist', url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'id': info.get('id', ''),
                }
            else:
                return None
                
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            st.warning(f"yt-dlp를 사용할 수 없습니다: {str(e)}")
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
            # Use yt-dlp to download
            result = subprocess.run([
                'yt-dlp',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', '0',
                '--output', str(output_path.with_suffix('')),
                '--no-playlist',
                url
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and output_path.exists():
                return str(output_path)
            else:
                st.error(f"다운로드 실패: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            st.error("다운로드 시간 초과 (2분)")
            return None
        except FileNotFoundError:
            st.error("yt-dlp가 설치되지 않았습니다. pip install yt-dlp")
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
