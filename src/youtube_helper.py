"""
YouTube Helper Module
Uses YouTube Data API to find educational videos and resources
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

from typing import Optional, List, Dict
import requests
import os
from pathlib import Path

# Load environment variables from .env file in project root
try:
    from dotenv import load_dotenv
    # Find project root (parent of src directory)
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Fallback: try current directory
        load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars only
except Exception:
    pass  # Failed to load .env, use system env vars only

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
        if HAS_STREAMLIT and st:
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
                                language: str = "ko", min_views: int = 100000) -> List[Dict]:
        """
        Search for educational videos with minimum view count filter
        
        Args:
            query: Search query
            max_results: Maximum number of results (1-50)
            language: Language code (ko, en)
            min_views: Minimum view count (default: 100,000)
            
        Returns:
            List of video information dictionaries (filtered by view count)
        """
        if not self.api_key:
            return self._fallback_video_search(query)
        
        try:
            # 악보와 음원이 포함된 영상을 우선 검색하도록 키워드 추가
            # 여러 검색 쿼리를 시도하여 악보/음원이 잘 나오는 영상 찾기
            search_queries = [
                f"{query} 악보 음원 초등 음악",
                f"{query} 악보 연주 초등",
                f"{query} 악기 연주 악보",
                f"{query} 초등 음악 교육"
            ]
            
            # 더 많은 결과를 가져와서 필터링 (최대 50개)
            search_max_results = min(max_results * 3, 50)  # 필터링을 위해 더 많이 가져옴
            
            all_video_ids = []
            all_video_snippets = {}
            
            # 여러 쿼리로 검색하여 악보/음원 관련 영상 우선 수집
            for enhanced_query in search_queries[:2]:  # 상위 2개 쿼리만 사용
                # Step 1: Search for videos
                search_params = {
                    "part": "snippet",
                    "q": enhanced_query,
                    "type": "video",
                    "maxResults": min(search_max_results // 2, 25),
                    "relevanceLanguage": language,
                    "videoCategoryId": "27",  # Education category
                    "safeSearch": "strict",
                    "order": "viewCount",  # 조회수 순으로 정렬
                    "key": self.api_key
                }
                
                search_response = requests.get(
                    f"{self.base_url}/search",
                    params=search_params,
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    for item in search_data.get('items', []):
                        video_id = item['id']['videoId']
                        if video_id not in all_video_ids:
                            all_video_ids.append(video_id)
                            all_video_snippets[video_id] = item['snippet']
            
            if not all_video_ids:
                # 기본 검색으로 대체
                enhanced_query = f"{query} 초등 음악 교육"
                search_params = {
                    "part": "snippet",
                    "q": enhanced_query,
                    "type": "video",
                    "maxResults": search_max_results,
                    "relevanceLanguage": language,
                    "videoCategoryId": "27",
                    "safeSearch": "strict",
                    "order": "viewCount",
                    "key": self.api_key
                }
                
                search_response = requests.get(
                    f"{self.base_url}/search",
                    params=search_params,
                    timeout=10
                )
                
                if search_response.status_code != 200:
                    if HAS_STREAMLIT and st:
                        st.warning(f"YouTube API 오류: {search_response.status_code}")
                    else:
                        print(f"YouTube API 오류: {search_response.status_code}")
                    return self._fallback_video_search(query)
                
                search_data = search_response.json()
                all_video_ids = [item['id']['videoId'] for item in search_data.get('items', [])]
                for item in search_data.get('items', []):
                    all_video_snippets[item['id']['videoId']] = item['snippet']
            
            if not all_video_ids:
                return []
            
            # Step 2: Get video statistics (view count)
            videos_params = {
                "part": "snippet,statistics",
                "id": ",".join(all_video_ids),
                "key": self.api_key
            }
            
            videos_response = requests.get(
                f"{self.base_url}/videos",
                params=videos_params,
                timeout=10
            )
            
            if videos_response.status_code != 200:
                # 통계 정보를 가져올 수 없으면 기본 정보만 반환
                videos = []
                for item in search_data.get('items', [])[:max_results]:
                    video_info = {
                        "title": item['snippet']['title'],
                        "description": item['snippet']['description'][:200] + "...",
                        "video_id": item['id']['videoId'],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        "thumbnail": item['snippet']['thumbnails']['medium']['url'],
                        "channel": item['snippet']['channelTitle'],
                        "published_at": item['snippet']['publishedAt'][:10],
                        "view_count": 0  # 알 수 없음
                    }
                    videos.append(video_info)
                return videos
            
            videos_data = videos_response.json()
            
            # Step 3: Filter by view count and score by content quality
            videos = []
            score_keywords = {
                '악보': 3,
                '음원': 2,
                '연주': 2,
                '악기': 1,
                '멜로디': 1,
                '반주': 1,
                'MR': 1,
                '악기 연주': 2,
                '피아노': 1,
                '리코더': 1
            }
            
            for item in videos_data.get('items', []):
                view_count = int(item.get('statistics', {}).get('viewCount', 0))
                
                # 10만 뷰 이상인 영상만 포함
                if view_count >= min_views:
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    combined_text = (title + " " + description).lower()
                    
                    # 악보/음원 관련 키워드 점수 계산
                    content_score = 0
                    has_score = False
                    has_audio = False
                    
                    for keyword, score in score_keywords.items():
                        if keyword.lower() in combined_text:
                            content_score += score
                            if keyword in ['악보', '악기 연주']:
                                has_score = True
                            if keyword in ['음원', '연주', '멜로디', '반주', 'MR']:
                                has_audio = True
                    
                    video_info = {
                        "title": title,
                        "description": description[:200] + "...",
                        "video_id": item['id'],
                        "url": f"https://www.youtube.com/watch?v={item['id']}",
                        "thumbnail": item['snippet']['thumbnails']['medium']['url'],
                        "channel": item['snippet']['channelTitle'],
                        "published_at": item['snippet']['publishedAt'][:10],
                        "view_count": view_count,
                        "content_score": content_score,
                        "has_score": has_score,
                        "has_audio": has_audio
                    }
                    videos.append(video_info)
            
            # 콘텐츠 점수와 조회수를 고려하여 정렬
            # 악보/음원이 있는 영상을 우선순위로 정렬
            videos.sort(key=lambda x: (
                x.get('has_score', False) and x.get('has_audio', False),  # 둘 다 있으면 최우선
                x.get('has_score', False) or x.get('has_audio', False),   # 하나라도 있으면 우선
                x.get('content_score', 0),  # 콘텐츠 점수
                x.get('view_count', 0)       # 조회수
            ), reverse=True)
            
            # 요청한 개수만큼만 반환
            videos = videos[:max_results]
            
            return videos
                
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.warning(f"YouTube 검색 오류: {str(e)}")
            else:
                print(f"YouTube 검색 오류: {str(e)}")
            import traceback
            traceback.print_exc()
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
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """
        Get video information by video ID
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video information dictionary with view count, or None if not found
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                "part": "snippet,statistics",
                "id": video_id,
                "key": self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/videos",
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            items = data.get('items', [])
            
            if not items:
                return None
            
            item = items[0]
            view_count = int(item.get('statistics', {}).get('viewCount', 0))
            
            return {
                "video_id": video_id,
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": item['snippet']['thumbnails']['medium']['url'],
                "channel": item['snippet']['channelTitle'],
                "published_at": item['snippet']['publishedAt'][:10],
                "view_count": view_count
            }
        except Exception as e:
            if HAS_STREAMLIT and st:
                st.warning(f"영상 정보 가져오기 오류: {str(e)}")
            else:
                print(f"영상 정보 가져오기 오류: {str(e)}")
            return None
    
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
