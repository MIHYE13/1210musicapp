"""
Music Utilities
Helper functions for music theory and processing
"""

from music21 import pitch, interval, key
from typing import List, Tuple

class MusicUtils:
    """Utility functions for music theory"""
    
    # Note names in Korean
    NOTE_NAMES_KR = {
        'C': '도', 'D': '레', 'E': '미', 'F': '파',
        'G': '솔', 'A': '라', 'B': '시'
    }
    
    # Scale degrees
    SCALE_DEGREES = {
        'I': 1, 'ii': 2, 'iii': 3, 'IV': 4,
        'V': 5, 'vi': 6, 'vii': 7
    }
    
    @staticmethod
    def midi_to_note_name(midi_number: int) -> str:
        """
        Convert MIDI number to note name with octave
        
        Args:
            midi_number: MIDI note number (0-127)
            
        Returns:
            Note name with octave (e.g., 'C4')
        """
        p = pitch.Pitch(midi=midi_number)
        return p.nameWithOctave
    
    @staticmethod
    def note_name_to_midi(note_name: str) -> int:
        """
        Convert note name to MIDI number
        
        Args:
            note_name: Note name with octave (e.g., 'C4')
            
        Returns:
            MIDI note number
        """
        p = pitch.Pitch(note_name)
        return p.midi
    
    @staticmethod
    def get_solfege(note_name: str, in_key: str = 'C') -> str:
        """
        Get solfege syllable for a note in a given key
        
        Args:
            note_name: Note name (e.g., 'C')
            in_key: Key name (e.g., 'C', 'G')
            
        Returns:
            Solfege syllable in Korean
        """
        # Get pitch class only (without octave)
        if len(note_name) > 1 and note_name[-1].isdigit():
            note_name = note_name[:-1]
        
        # For C major, use simple mapping
        if in_key == 'C':
            return MusicUtils.NOTE_NAMES_KR.get(note_name[0], note_name)
        
        # For other keys, calculate scale degree
        try:
            k = key.Key(in_key)
            p = pitch.Pitch(note_name)
            degree = k.getScaleDegreeFromPitch(p)
            
            # Map to solfege
            solfege_map = ['도', '레', '미', '파', '솔', '라', '시']
            if 1 <= degree <= 7:
                return solfege_map[degree - 1]
            return note_name
        except:
            return note_name
    
    @staticmethod
    def transpose_interval(from_key: str, to_key: str) -> int:
        """
        Calculate semitone interval for transposition
        
        Args:
            from_key: Original key
            to_key: Target key
            
        Returns:
            Number of semitones to transpose
        """
        from_pitch = pitch.Pitch(from_key)
        to_pitch = pitch.Pitch(to_key)
        
        i = interval.Interval(from_pitch, to_pitch)
        return i.semitones
    
    @staticmethod
    def is_in_range(midi_number: int, min_midi: int = 60, max_midi: int = 72) -> bool:
        """
        Check if MIDI number is in specified range
        
        Args:
            midi_number: MIDI number to check
            min_midi: Minimum MIDI number (default C4 = 60)
            max_midi: Maximum MIDI number (default C5 = 72)
            
        Returns:
            True if in range
        """
        return min_midi <= midi_number <= max_midi
    
    @staticmethod
    def get_chord_tones(chord_symbol: str, in_key: str = 'C') -> List[str]:
        """
        Get the notes in a chord
        
        Args:
            chord_symbol: Roman numeral chord symbol (I, IV, V, etc.)
            in_key: Key signature
            
        Returns:
            List of note names
        """
        # Map chord symbols to scale degrees
        degree_map = {
            'I': [1, 3, 5],
            'ii': [2, 4, 6],
            'iii': [3, 5, 7],
            'IV': [4, 6, 1],
            'V': [5, 7, 2],
            'vi': [6, 1, 3],
            'vii': [7, 2, 4]
        }
        
        if chord_symbol not in degree_map:
            return ['C', 'E', 'G']
        
        # Get scale for key
        k = key.Key(in_key)
        scale = k.getPitches()
        
        # Get chord tones
        degrees = degree_map[chord_symbol]
        chord_tones = [scale[d - 1].name for d in degrees]
        
        return chord_tones
    
    @staticmethod
    def simplify_note_name(note_name: str) -> str:
        """
        Simplify note name (remove octave, enharmonic)
        
        Args:
            note_name: Full note name
            
        Returns:
            Simplified note name
        """
        # Remove octave number
        if note_name[-1].isdigit():
            note_name = note_name[:-1]
        
        # Handle enharmonics (prefer sharps over flats for display)
        enharmonic_map = {
            'C#': 'C#', 'Db': 'C#',
            'D#': 'D#', 'Eb': 'D#',
            'F#': 'F#', 'Gb': 'F#',
            'G#': 'G#', 'Ab': 'G#',
            'A#': 'A#', 'Bb': 'A#'
        }
        
        return enharmonic_map.get(note_name, note_name)
    
    @staticmethod
    def calculate_duration_beats(quarter_length: float) -> Tuple[int, str]:
        """
        Convert quarter length to beats and note type
        
        Args:
            quarter_length: Duration in quarter notes
            
        Returns:
            Tuple of (beats, note_type_name)
        """
        duration_map = {
            0.25: (0.25, "16분음표"),
            0.5: (0.5, "8분음표"),
            1.0: (1, "4분음표"),
            2.0: (2, "2분음표"),
            4.0: (4, "온음표")
        }
        
        return duration_map.get(quarter_length, (quarter_length, "음표"))
    
    @staticmethod
    def get_key_signature_info(key_name: str) -> dict:
        """
        Get information about a key signature
        
        Args:
            key_name: Key name (e.g., 'C', 'G', 'F')
            
        Returns:
            Dictionary with key information
        """
        try:
            k = key.Key(key_name)
            
            info = {
                'name': key_name,
                'tonic': k.tonic.name,
                'mode': k.mode,
                'sharps': k.sharps if k.sharps > 0 else 0,
                'flats': abs(k.sharps) if k.sharps < 0 else 0,
                'scale': [p.name for p in k.getPitches()]
            }
            
            return info
        except:
            return {'error': 'Invalid key name'}
    
    @staticmethod
    def format_time(quarter_length: float, tempo: int = 120) -> str:
        """
        Convert quarter length to time string (MM:SS)
        
        Args:
            quarter_length: Duration in quarter notes
            tempo: Tempo in BPM
            
        Returns:
            Time string in MM:SS format
        """
        # Calculate seconds
        seconds = (quarter_length / tempo) * 60
        
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        
        return f"{minutes:02d}:{secs:02d}"
