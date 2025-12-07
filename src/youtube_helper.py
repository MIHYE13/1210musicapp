"""
YouTube Helper Module
Uses YouTube Data API to find educational videos and resources
"""

import streamlit as st
from typing import Optional, List, Dict
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class YouTubeHelper:
    """YouTube API helper for finding music education videos"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize YouTube helper
        
        Args:
            api_key: YouTube Data API key (optional, can use st.secrets)
        """
        self.api_key = api_key or self._get_api_key()
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from multiple sources (priority order)"""
        # 1. Try Streamlit secrets (for cloud deployment)
        try:
            key = st.secrets.get("YOUTUBE_API_KEY")
            if key:
                return key
        except:
            pass
        
        # 2. Try environment variable (from .env file or system)
        key = os.getenv("YOUTUBE_API_KEY")
        if key:
            return key
        
        # 3. No key found
        return None
    
    def search_education_videos(self, query: str, max_results: int = 5,
                                language: str = "ko") -> List[Dict]:
        """
        Search for educational videos
        
        Args:
            query: Search query
            max_results: Maximum number of results (1-50)
            language: Language code (ko, en)
            
        Returns:
            List of video information dictionaries
        """
        if not self.api_key:
            return self._fallback_video_search(query)
        
        try:
            # Add educational keywords to query
            enhanced_query = f"{query} 초등 음악 교육"
            
            params = {
                "part": "snippet",
                "q": enhanced_query,
                "type": "video",
                "maxResults": max_results,
                "relevanceLanguage": language,
                "videoCategoryId": "27",  # Education category
                "safeSearch": "strict",
                "key": self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                videos = []
                
                for item in data.get('items', []):
                    video_info = {
                        "title": item['snippet']['title'],
                        "description": item['snippet']['description'][:200] + "...",
                        "video_id": item['id']['videoId'],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        "thumbnail": item['snippet']['thumbnails']['medium']['url'],
                        "channel": item['snippet']['channelTitle'],
                        "published_at": item['snippet']['publishedAt'][:10]
                    }
                    videos.append(video_info)
                
                return videos
            else:
                st.warning(f"YouTube API 오류: {response.status_code}")
                return self._fallback_video_search(query)
                
        except Exception as e:
            st.warning(f"YouTube 검색 오류: {str(e)}")
            return self._fallback_video_search(query)
    
    def find_tutorial_videos(self, instrument: str, song_title: str = None) -> List[Dict]:
        """
        Find instrument tutorial videos
        
        Args:
            instrument: Instrument name (피아노, 리코더, etc.)
            song_title: Optional specific song
            
        Returns:
            List of tutorial videos
        """
        if song_title:
            query = f"{instrument} {song_title} 연주법 초등"
        else:
            query = f"{instrument} 기초 연주법 초등학생"
        
        return self.search_education_videos(query, max_results=5)
    
    def find_solfege_videos(self, topic: str = "계이름") -> List[Dict]:
        """
        Find solfege and music theory videos
        
        Args:
            topic: Specific topic (계이름, 박자, 리듬, etc.)
            
        Returns:
            List of educational videos
        """
        query = f"{topic} 초등 음악 이론"
        return self.search_education_videos(query, max_results=5)
    
    def find_practice_videos(self, song_title: str) -> List[Dict]:
        """
        Find practice/backing track videos for a song
        
        Args:
            song_title: Song title
            
        Returns:
            List of practice videos
        """
        query = f"{song_title} 반주 MR 초등"
        return self.search_education_videos(query, max_results=3)
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict]:
        """
        Get information about an educational channel
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Channel information dictionary
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                "part": "snippet,statistics",
                "id": channel_id,
                "key": self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/channels",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    item = data['items'][0]
                    return {
                        "title": item['snippet']['title'],
                        "description": item['snippet']['description'],
                        "subscriber_count": item['statistics'].get('subscriberCount', 'N/A'),
                        "video_count": item['statistics'].get('videoCount', 'N/A'),
                        "url": f"https://www.youtube.com/channel/{channel_id}"
                    }
            
            return None
            
        except Exception as e:
            return None
    
    def recommend_channels(self) -> List[Dict]:
        """
        Recommend educational music channels for elementary students
        
        Returns:
            List of recommended channels
        """
        # Curated list of good educational channels
        recommendations = [
            {
                "name": "초등 음악 교실",
                "description": "초등학교 음악 교육 전문 채널",
                "topics": ["계이름", "리듬", "악기 연주"],
                "search_query": "초등 음악 교실"
            },
            {
                "name": "음악샘",
                "description": "음악 선생님의 교육 영상",
                "topics": ["음악 이론", "노래 부르기", "악보 읽기"],
                "search_query": "음악샘 초등"
            },
            {
                "name": "키즈 뮤직",
                "description": "어린이를 위한 음악 교육",
                "topics": ["동요", "리듬 놀이", "악기 체험"],
                "search_query": "키즈 뮤직 교육"
            }
        ]
        
        return recommendations
    
    def get_video_embed_html(self, video_id: str, width: int = 560, 
                            height: int = 315) -> str:
        """
        Generate HTML for embedding a YouTube video
        
        Args:
            video_id: YouTube video ID
            width: Video width
            height: Video height
            
        Returns:
            HTML embed code
        """
        return f"""
        <iframe width="{width}" height="{height}" 
                src="https://www.youtube.com/embed/{video_id}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
        """
    
    def format_video_card(self, video: Dict) -> str:
        """
        Format video information as a card
        
        Args:
            video: Video information dictionary
            
        Returns:
            Formatted markdown string
        """
        return f"""
### 📺 {video['title']}

**채널**: {video['channel']}  
**게시일**: {video['published_at']}

{video['description']}

[영상 보기]({video['url']})
"""
    
    def search_by_difficulty(self, topic: str, difficulty: str) -> List[Dict]:
        """
        Search videos by difficulty level
        
        Args:
            topic: Topic to search
            difficulty: Difficulty level (쉬움, 보통, 어려움)
            
        Returns:
            List of videos
        """
        difficulty_map = {
            "쉬움": "초급 기초",
            "보통": "중급",
            "어려움": "고급 심화"
        }
        
        level = difficulty_map.get(difficulty, "기초")
        query = f"{topic} {level} 초등"
        
        return self.search_education_videos(query, max_results=5)
    
    def _fallback_video_search(self, query: str) -> List[Dict]:
        """Provide basic search suggestions without API"""
        return [
            {
                "title": f"'{query}' 관련 영상을 찾으려면",
                "description": "YouTube API 키를 설정하면 자동으로 교육 영상을 검색하고 추천받을 수 있습니다.",
                "video_id": "",
                "url": f"https://www.youtube.com/results?search_query={query}+초등+음악+교육",
                "thumbnail": "",
                "channel": "YouTube 검색",
                "published_at": ""
            }
        ]
    
    def get_api_status(self) -> Dict:
        """Get API status"""
        return {
            "has_key": self.api_key is not None,
            "key_length": len(self.api_key) if self.api_key else 0,
            "service": "YouTube Data API"
        }
    
    def get_playlist_videos(self, playlist_id: str, max_results: int = 10) -> List[Dict]:
        """
        Get videos from a playlist
        
        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos
            
        Returns:
            List of videos in playlist
        """
        if not self.api_key:
            return []
        
        try:
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": max_results,
                "key": self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/playlistItems",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                videos = []
                
                for item in data.get('items', []):
                    video_info = {
                        "title": item['snippet']['title'],
                        "description": item['snippet']['description'][:200] + "...",
                        "video_id": item['snippet']['resourceId']['videoId'],
                        "url": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
                        "thumbnail": item['snippet']['thumbnails']['medium']['url'],
                        "channel": item['snippet']['channelTitle'],
                        "position": item['snippet']['position']
                    }
                    videos.append(video_info)
                
                return videos
            
            return []
            
        except Exception as e:
            return []
