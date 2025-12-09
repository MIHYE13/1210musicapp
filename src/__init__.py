"""
Elementary Music Helper
초등 음악 도우미 웹앱

Main package initialization
"""

__version__ = "1.0.0"
__author__ = "차미혜"
__description__ = "초등학생과 교사를 위한 AI 기반 음악 학습 지원 웹 애플리케이션"

# Lazy imports to avoid streamlit dependency issues
# Import only when needed, not at module level
try:
    from .audio_processor import AudioProcessor
except ImportError:
    AudioProcessor = None

try:
    from .score_processor import ScoreProcessor
except ImportError:
    ScoreProcessor = None

try:
    from .chord_generator import ChordGenerator
except ImportError:
    ChordGenerator = None

try:
    from .player import MusicPlayer
except ImportError:
    MusicPlayer = None

try:
    from .ai_assistant import AIAssistant
except ImportError:
    AIAssistant = None

try:
    from .perplexity_assistant import PerplexityAssistant
except ImportError:
    PerplexityAssistant = None

try:
    from .youtube_helper import YouTubeHelper
except ImportError:
    YouTubeHelper = None

try:
    from .database import DatabaseManager
except ImportError:
    DatabaseManager = None

try:
    from .chord_analyzer import ChordAnalyzer, PianoVisualizer
except ImportError:
    ChordAnalyzer = None
    PianoVisualizer = None

try:
    from .youtube_downloader import YouTubeDownloader
except ImportError:
    YouTubeDownloader = None

try:
    from .pdf_parser import PDFScoreParser
except ImportError:
    PDFScoreParser = None

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
