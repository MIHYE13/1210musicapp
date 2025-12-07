"""
Elementary Music Helper
초등 음악 도우미 웹앱

Main package initialization
"""

__version__ = "1.0.0"
__author__ = "차미혜"
__description__ = "초등학생과 교사를 위한 AI 기반 음악 학습 지원 웹 애플리케이션"

from .audio_processor import AudioProcessor
from .score_processor import ScoreProcessor
from .chord_generator import ChordGenerator
from .player import MusicPlayer
from .ai_assistant import AIAssistant
from .perplexity_assistant import PerplexityAssistant
from .youtube_helper import YouTubeHelper
from .database import DatabaseManager
from .chord_analyzer import ChordAnalyzer, PianoVisualizer
from .youtube_downloader import YouTubeDownloader
from .pdf_parser import PDFScoreParser

__all__ = [
    'AudioProcessor',
    'ScoreProcessor',
    'ChordGenerator',
    'MusicPlayer',
    'AIAssistant',
    'PerplexityAssistant',
    'YouTubeHelper',
    'DatabaseManager',
    'ChordAnalyzer',
    'PianoVisualizer',
    'YouTubeDownloader',
    'PDFScoreParser'
]
