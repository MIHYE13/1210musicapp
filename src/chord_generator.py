"""
Chord Generation Module
Automatically generates simple accompaniment for melodies
"""

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    st = None

# Import music21 with error handling
try:
    from music21 import stream, note, chord, key, pitch
    HAS_MUSIC21 = True
except ImportError as e:
    HAS_MUSIC21 = False
    if HAS_STREAMLIT and st:
        st.error(f"music21이 설치되지 않았습니다: {e}. pip install music21을 실행해주세요.")
    else:
        print(f"[ERROR] music21이 설치되지 않았습니다: {e}. pip install music21을 실행해주세요.")
    # Create dummy classes to prevent import errors
    stream = None
    note = None
    chord = None
    key = None
    pitch = None

from typing import List, Optional

class ChordGenerator:
    """Generate simple chord accompaniment for melodies"""
    
    # Basic chord progressions in C major
    CHORD_NOTES = {
        'I': ['C4', 'E4', 'G4'],      # C major (도)
        'ii': ['D4', 'F4', 'A4'],     # D minor
        'iii': ['E4', 'G4', 'B4'],    # E minor
        'IV': ['F4', 'A4', 'C5'],     # F major (파)
        'V': ['G4', 'B4', 'D5'],      # G major (솔)
        'vi': ['A4', 'C5', 'E5'],     # A minor (라)
        'vii°': ['B4', 'D5', 'F5'],   # B diminished
    }
    
    # Simplified chord choices for elementary students
    SIMPLE_CHORDS = ['I', 'IV', 'V', 'vi']
    
    def __init__(self):
        """Initialize chord generator"""
        pass
    
    def add_accompaniment(self, score: stream.Score) -> stream.Score:
        """
        Add simple block chord accompaniment to a melody
        
        Args:
            score: music21.stream.Score with melody
            
        Returns:
            Score with melody and accompaniment
        """
        new_score = stream.Score()
        
        # Process each part (should be melody)
        for part in score.parts:
            # Keep the melody part
            new_score.append(part)
            
            # Generate accompaniment part
            accompaniment = self._generate_accompaniment(part)
            new_score.append(accompaniment)
        
        return new_score
    
    def _generate_accompaniment(self, melody_part: stream.Part) -> stream.Part:
        """
        Generate accompaniment part for a melody
        
        Args:
            melody_part: Melody part to accompany
            
        Returns:
            Accompaniment part
        """
        accompaniment = stream.Part()
        accompaniment.partName = "반주"
        
        # Copy time signature and key
        for elem in melody_part.getElementsByClass(['TimeSignature', 'KeySignature', 'Clef']):
            accompaniment.append(elem)
        
        # Analyze melody by measures
        measures = melody_part.getElementsByClass('Measure')
        
        if not measures:
            # If no measures, create chords for whole part
            measures = [melody_part]
        
        for measure in measures:
            # Get notes in this measure
            measure_notes = measure.flat.notes
            
            if not measure_notes:
                # Add rest if no notes
                r = note.Rest()
                r.quarterLength = 4.0  # Whole note rest
                accompaniment.append(r)
                continue
            
            # Determine best chord for this measure
            chord_symbol = self._choose_chord(measure_notes)
            
            # Create block chord (half notes)
            measure_duration = measure.duration.quarterLength
            num_chords = int(measure_duration / 2)  # Half note chords
            
            for i in range(max(1, num_chords)):
                c = self._create_chord(chord_symbol)
                c.quarterLength = 2.0  # Half note
                accompaniment.append(c)
        
        return accompaniment
    
    def _choose_chord(self, notes: List[note.Note]) -> str:
        """
        Choose best chord for a group of notes
        
        Args:
            notes: List of notes in a measure
            
        Returns:
            Chord symbol (I, IV, V, vi)
        """
        if not notes:
            return 'I'
        
        # Count pitch classes
        pitch_classes = {}
        for n in notes:
            if isinstance(n, note.Note):
                pc = n.pitch.pitchClass
                pitch_classes[pc] = pitch_classes.get(pc, 0) + 1
        
        # Simple heuristic: choose chord based on most common pitch class
        if not pitch_classes:
            return 'I'
        
        most_common = max(pitch_classes, key=pitch_classes.get)
        
        # Map pitch class to chord
        # C=0, D=2, E=4, F=5, G=7, A=9, B=11
        chord_map = {
            0: 'I',   # C -> I
            2: 'V',   # D -> V (has D)
            4: 'I',   # E -> I (has E)
            5: 'IV',  # F -> IV
            7: 'V',   # G -> V
            9: 'vi',  # A -> vi
            11: 'V'   # B -> V (has B)
        }
        
        return chord_map.get(most_common, 'I')
    
    def _create_chord(self, chord_symbol: str) -> chord.Chord:
        """
        Create a chord object from symbol
        
        Args:
            chord_symbol: Chord symbol (I, IV, V, vi)
            
        Returns:
            music21.chord.Chord object
        """
        chord_pitches = self.CHORD_NOTES.get(chord_symbol, self.CHORD_NOTES['I'])
        
        # Create chord
        c = chord.Chord(chord_pitches)
        
        return c
    
    def analyze_harmony(self, melody_part: stream.Part) -> List[str]:
        """
        Analyze melody and suggest chord progression
        
        Args:
            melody_part: Melody to analyze
            
        Returns:
            List of chord symbols
        """
        progression = []
        
        measures = melody_part.getElementsByClass('Measure')
        if not measures:
            measures = [melody_part]
        
        for measure in measures:
            notes = measure.flat.notes
            chord_symbol = self._choose_chord(notes)
            progression.append(chord_symbol)
        
        return progression
    
    def create_bass_line(self, chord_progression: List[str]) -> stream.Part:
        """
        Create simple bass line from chord progression
        
        Args:
            chord_progression: List of chord symbols
            
        Returns:
            Bass line part
        """
        bass = stream.Part()
        bass.partName = "베이스"
        
        for chord_symbol in chord_progression:
            # Get root note of chord
            root_pitch = self._get_chord_root(chord_symbol)
            
            # Create bass note (whole note)
            bass_note = note.Note(root_pitch)
            bass_note.quarterLength = 4.0
            bass_note.octave = 3  # Bass octave
            
            bass.append(bass_note)
        
        return bass
    
    def _get_chord_root(self, chord_symbol: str) -> str:
        """
        Get root note of chord
        
        Args:
            chord_symbol: Chord symbol
            
        Returns:
            Root note name
        """
        root_map = {
            'I': 'C',
            'ii': 'D',
            'iii': 'E',
            'IV': 'F',
            'V': 'G',
            'vi': 'A',
            'vii°': 'B'
        }
        
        return root_map.get(chord_symbol, 'C')
    
    def simplify_progression(self, progression: List[str]) -> List[str]:
        """
        Simplify chord progression to use only I, IV, V, vi
        
        Args:
            progression: Original chord progression
            
        Returns:
            Simplified progression
        """
        simplified = []
        
        substitution_map = {
            'ii': 'IV',
            'iii': 'I',
            'vii°': 'V'
        }
        
        for chord_symbol in progression:
            if chord_symbol in self.SIMPLE_CHORDS:
                simplified.append(chord_symbol)
            else:
                simplified.append(substitution_map.get(chord_symbol, 'I'))
        
        return simplified
    
    def get_chord_info(self, chord_symbol: str) -> dict:
        """
        Get information about a chord
        
        Args:
            chord_symbol: Chord symbol
            
        Returns:
            Dictionary with chord information
        """
        info = {
            'symbol': chord_symbol,
            'root': self._get_chord_root(chord_symbol),
            'notes': self.CHORD_NOTES.get(chord_symbol, []),
            'korean': self._get_korean_name(chord_symbol)
        }
        
        return info
    
    def _get_korean_name(self, chord_symbol: str) -> str:
        """Get Korean name for chord"""
        names = {
            'I': '으뜸화음 (도)',
            'IV': '버금딸림화음 (파)',
            'V': '딸림화음 (솔)',
            'vi': '가온음화음 (라)'
        }
        
        return names.get(chord_symbol, chord_symbol)
