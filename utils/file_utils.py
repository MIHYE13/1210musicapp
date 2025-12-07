"""
File Utilities
Helper functions for file handling and validation
"""

import os
from typing import Optional, List
import tempfile
from pathlib import Path

class FileUtils:
    """Utility functions for file operations"""
    
    # Supported file formats
    AUDIO_FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
    SCORE_FORMATS = ['.mid', '.midi', '.xml', '.mxl', '.musicxml', '.abc']
    PDF_FORMATS = ['.pdf']
    
    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
        """
        Validate file type by extension
        
        Args:
            filename: Name of file to validate
            allowed_types: List of allowed extensions (with dot)
            
        Returns:
            True if file type is allowed
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in allowed_types
    
    @staticmethod
    def is_audio_file(filename: str) -> bool:
        """Check if file is an audio file"""
        return FileUtils.validate_file_type(filename, FileUtils.AUDIO_FORMATS)
    
    @staticmethod
    def is_score_file(filename: str) -> bool:
        """Check if file is a score file"""
        return FileUtils.validate_file_type(filename, FileUtils.SCORE_FORMATS)
    
    @staticmethod
    def is_pdf_file(filename: str) -> bool:
        """Check if file is a PDF file"""
        return FileUtils.validate_file_type(filename, FileUtils.PDF_FORMATS)
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """
        Validate file size
        
        Args:
            file_size: File size in bytes
            
        Returns:
            True if file size is acceptable
        """
        return file_size <= FileUtils.MAX_FILE_SIZE
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted string (e.g., "1.5 MB")
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing unsafe characters
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path separators and other unsafe characters
        unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        
        sanitized = filename
        for char in unsafe_chars:
            sanitized = sanitized.replace(char, '_')
        
        return sanitized
    
    @staticmethod
    def create_temp_file(suffix: str = '') -> str:
        """
        Create a temporary file and return its path
        
        Args:
            suffix: File suffix/extension
            
        Returns:
            Path to temporary file
        """
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp_file.close()
        return tmp_file.name
    
    @staticmethod
    def cleanup_temp_file(filepath: str):
        """
        Delete a temporary file
        
        Args:
            filepath: Path to file to delete
        """
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
        except:
            pass  # Ignore cleanup errors
    
    @staticmethod
    def get_file_info(file) -> dict:
        """
        Get information about an uploaded file
        
        Args:
            file: Streamlit uploaded file object
            
        Returns:
            Dictionary with file information
        """
        info = {
            'name': file.name,
            'size': file.size,
            'size_formatted': FileUtils.format_file_size(file.size),
            'type': file.type,
            'extension': os.path.splitext(file.name)[1].lower()
        }
        
        # Add file category
        if FileUtils.is_audio_file(file.name):
            info['category'] = 'audio'
        elif FileUtils.is_score_file(file.name):
            info['category'] = 'score'
        elif FileUtils.is_pdf_file(file.name):
            info['category'] = 'pdf'
        else:
            info['category'] = 'unknown'
        
        return info
    
    @staticmethod
    def suggest_output_filename(input_filename: str, suffix: str = '_processed') -> str:
        """
        Suggest output filename based on input
        
        Args:
            input_filename: Original filename
            suffix: Suffix to add before extension
            
        Returns:
            Suggested output filename
        """
        name, ext = os.path.splitext(input_filename)
        return f"{name}{suffix}{ext}"
    
    @staticmethod
    def ensure_extension(filename: str, required_ext: str) -> str:
        """
        Ensure filename has the required extension
        
        Args:
            filename: Original filename
            required_ext: Required extension (with dot)
            
        Returns:
            Filename with correct extension
        """
        name, ext = os.path.splitext(filename)
        
        if ext.lower() != required_ext.lower():
            return f"{name}{required_ext}"
        
        return filename
    
    @staticmethod
    def create_download_filename(base_name: str, file_type: str) -> str:
        """
        Create a download filename with timestamp
        
        Args:
            base_name: Base name for file
            file_type: File type/extension
            
        Returns:
            Download filename
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sanitized_base = FileUtils.sanitize_filename(base_name)
        
        return f"{sanitized_base}_{timestamp}.{file_type}"
    
    @staticmethod
    def get_supported_formats_text() -> str:
        """
        Get text description of supported formats
        
        Returns:
            Description string
        """
        audio = ', '.join(FileUtils.AUDIO_FORMATS)
        score = ', '.join(FileUtils.SCORE_FORMATS)
        
        return f"""
        **지원 형식:**
        - 오디오: {audio}
        - 악보: {score}
        - PDF: MusicXML 변환 후 업로드 필요
        """
    
    @staticmethod
    def validate_upload(file, expected_category: str = None) -> tuple[bool, str]:
        """
        Validate uploaded file
        
        Args:
            file: Streamlit uploaded file object
            expected_category: Expected file category ('audio', 'score', etc.)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if file is None:
            return False, "파일이 업로드되지 않았습니다."
        
        # Check file size
        if not FileUtils.validate_file_size(file.size):
            max_size = FileUtils.format_file_size(FileUtils.MAX_FILE_SIZE)
            return False, f"파일 크기가 너무 큽니다. 최대 {max_size}까지 지원합니다."
        
        # Check file type if category specified
        if expected_category:
            info = FileUtils.get_file_info(file)
            if info['category'] != expected_category:
                return False, f"잘못된 파일 형식입니다. {expected_category} 파일을 업로드해주세요."
        
        return True, ""
