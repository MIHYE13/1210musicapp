"""
Chord Analyzer and Piano Keyboard Visualizer
Analyzes chords from MIDI and displays them on piano keyboard
"""

from music21 import *
import streamlit as st
from typing import List, Dict, Tuple
import base64
from io import BytesIO

class ChordAnalyzer:
    """Analyze chords and generate piano keyboard visualization"""
    
    # C major scale chord mapping
    CHORD_MAP = {
        'C': ['C', 'E', 'G'],
        'Dm': ['D', 'F', 'A'],
        'Em': ['E', 'G', 'B'],
        'F': ['F', 'A', 'C'],
        'G': ['G', 'B', 'D'],
        'Am': ['A', 'C', 'E'],
        'Bdim': ['B', 'D', 'F']
    }
    
    # Piano key positions (white keys only for simplicity)
    WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    def __init__(self):
        self.chords_by_measure = []
    
    def analyze_midi_chords(self, midi_stream: stream.Stream) -> List[Dict]:
        """
        Analyze MIDI file and extract chords by measure
        
        Args:
            midi_stream: music21 Stream object
            
        Returns:
            List of chord information per measure
        """
        chords_info = []
        
        # Get measures
        measures = midi_stream.parts[0].getElementsByClass('Measure')
        
        for i, measure in enumerate(measures):
            measure_num = i + 1
            
            # Get all notes in this measure
            notes_in_measure = []
            for element in measure.notesAndRests:
                if isinstance(element, note.Note):
                    notes_in_measure.append(element.pitch.name)
                elif isinstance(element, chord.Chord):
                    notes_in_measure.extend([p.name for p in element.pitches])
            
            if notes_in_measure:
                # Analyze chord from notes
                detected_chord = self._detect_chord(notes_in_measure)
                chord_notes = self.CHORD_MAP.get(detected_chord, notes_in_measure[:3])
                
                chords_info.append({
                    'measure': measure_num,
                    'chord_name': detected_chord,
                    'notes': chord_notes,
                    'beat': measure.beat
                })
        
        self.chords_by_measure = chords_info
        return chords_info
    
    def _detect_chord(self, notes: List[str]) -> str:
        """
        Detect chord from notes
        
        Args:
            notes: List of note names
            
        Returns:
            Chord name (C, Dm, Em, F, G, Am, Bdim)
        """
        # Remove duplicates and sort
        unique_notes = sorted(set([n.replace('#', '').replace('♯', '') for n in notes]))
        
        # Simple chord detection based on C major scale
        for chord_name, chord_notes in self.CHORD_MAP.items():
            if set(unique_notes).issubset(set(chord_notes)):
                return chord_name
        
        # Default to C if no match
        if unique_notes:
            root = unique_notes[0]
            # Check if minor (has flat 3rd)
            if len(unique_notes) >= 3:
                interval = (self.WHITE_KEYS.index(unique_notes[1]) - 
                          self.WHITE_KEYS.index(unique_notes[0])) % 7
                if interval == 2:  # Minor third
                    return f"{root}m"
            return root
        
        return 'C'
    
    def generate_chord_chart(self, chords_info: List[Dict]) -> str:
        """
        Generate text-based chord chart
        
        Args:
            chords_info: List of chord information
            
        Returns:
            Formatted chord chart string
        """
        chart = "📊 **화음 진행표**\n\n"
        chart += "| 마디 | 화음 | 구성음 |\n"
        chart += "|------|------|--------|\n"
        
        for chord in chords_info:
            notes_str = ", ".join(chord['notes'])
            chart += f"| {chord['measure']} | **{chord['chord_name']}** | {notes_str} |\n"
        
        return chart
    
    def generate_piano_keyboard_html(self, chord_notes: List[str], 
                                     chord_name: str = "") -> str:
        """
        Generate interactive HTML piano keyboard with highlighted chord
        
        Args:
            chord_notes: List of notes to highlight
            chord_name: Name of the chord
            
        Returns:
            HTML string for piano keyboard
        """
        # Normalize note names
        normalized_notes = [n.replace('♯', '#') for n in chord_notes]
        
        html = f"""
        <div style="text-align: center; margin: 20px 0;">
            <h3 style="color: #1f77b4;">🎹 {chord_name} 코드</h3>
            <p style="color: #666;">구성음: {', '.join(chord_notes)}</p>
        </div>
        
        <div id="piano-container" style="margin: 20px auto; max-width: 800px;">
            <svg width="100%" height="200" viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg">
                <!-- Piano keyboard -->
        """
        
        # Define keyboard layout (2 octaves: C4-B5)
        white_keys = []
        black_keys = []
        
        octaves = [4, 5]
        x_pos = 0
        white_key_width = 50
        white_key_height = 150
        black_key_width = 30
        black_key_height = 100
        
        for octave in octaves:
            for i, note_name in enumerate(self.WHITE_KEYS):
                note_full = f"{note_name}{octave}"
                is_highlighted = note_name in normalized_notes or note_full in normalized_notes
                
                # White key
                fill_color = "#FFD700" if is_highlighted else "#FFFFFF"
                stroke = "#000000"
                stroke_width = "2"
                
                white_keys.append(f'''
                    <rect x="{x_pos}" y="0" width="{white_key_width}" height="{white_key_height}"
                          fill="{fill_color}" stroke="{stroke}" stroke-width="{stroke_width}"
                          class="piano-key white-key" data-note="{note_full}"/>
                    <text x="{x_pos + white_key_width/2}" y="{white_key_height + 20}"
                          text-anchor="middle" font-size="12" fill="#333">{note_name}</text>
                ''')
                
                # Black keys (skip E and B)
                if note_name not in ['E', 'B']:
                    black_note = f"{note_name}#{octave}"
                    is_black_highlighted = (f"{note_name}#" in normalized_notes or 
                                          black_note in normalized_notes)
                    black_fill = "#FFD700" if is_black_highlighted else "#000000"
                    
                    black_keys.append(f'''
                        <rect x="{x_pos + white_key_width - black_key_width/2}" y="0"
                              width="{black_key_width}" height="{black_key_height}"
                              fill="{black_fill}" stroke="#000" stroke-width="1"
                              class="piano-key black-key" data-note="{black_note}"/>
                    ''')
                
                x_pos += white_key_width
        
        # Combine white and black keys (black on top)
        html += ''.join(white_keys)
        html += ''.join(black_keys)
        
        html += """
            </svg>
        </div>
        
        <style>
            .piano-key {
                cursor: pointer;
                transition: all 0.2s;
            }
            .piano-key:hover {
                opacity: 0.8;
            }
            .white-key:hover {
                fill: #f0f0f0;
            }
        </style>
        
        <script>
            document.querySelectorAll('.piano-key').forEach(key => {
                key.addEventListener('click', function() {
                    const note = this.getAttribute('data-note');
                    console.log('Clicked:', note);
                    // Play sound (would need Web Audio API)
                });
            });
        </script>
        """
        
        return html
    
    def generate_all_chords_display(self, chords_info: List[Dict]) -> str:
        """
        Generate HTML display for all chords in sequence
        
        Args:
            chords_info: List of chord information
            
        Returns:
            HTML string with all chord keyboards
        """
        html = "<div style='margin: 20px 0;'>"
        
        for chord in chords_info[:8]:  # Show first 8 measures
            html += f"<div style='margin: 30px 0; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; background: #f9f9f9;'>"
            html += f"<h4 style='color: #1f77b4; margin: 0 0 10px 0;'>📍 마디 {chord['measure']}</h4>"
            html += self.generate_piano_keyboard_html(chord['notes'], chord['chord_name'])
            html += "</div>"
        
        html += "</div>"
        return html
    
    def add_chord_symbols_to_score(self, score: stream.Score, 
                                   chords_info: List[Dict]) -> stream.Score:
        """
        Add chord symbols to score
        
        Args:
            score: music21 Score object
            chords_info: List of chord information
            
        Returns:
            Score with chord symbols added
        """
        if not score.parts:
            return score
        
        top_part = score.parts[0]
        measures = top_part.getElementsByClass('Measure')
        
        for chord_info in chords_info:
            measure_num = chord_info['measure']
            chord_name = chord_info['chord_name']
            
            if measure_num <= len(measures):
                measure = measures[measure_num - 1]
                
                # Add chord symbol at the beginning of measure
                chord_symbol = harmony.ChordSymbol(chord_name)
                chord_symbol.offset = 0
                measure.insert(0, chord_symbol)
        
        return score
    
    def create_chord_progression_summary(self, chords_info: List[Dict]) -> str:
        """
        Create a summary of chord progression
        
        Args:
            chords_info: List of chord information
            
        Returns:
            Formatted summary string
        """
        if not chords_info:
            return "화음 정보가 없습니다."
        
        chord_sequence = [c['chord_name'] for c in chords_info]
        unique_chords = list(dict.fromkeys(chord_sequence))  # Preserve order
        
        summary = f"""
### 🎼 화음 진행 요약

**총 마디 수**: {len(chords_info)}개  
**사용된 화음**: {', '.join(unique_chords)}  
**화음 진행**: {' - '.join(chord_sequence[:12])}{"..." if len(chord_sequence) > 12 else ""}

**난이도**: {"초급" if len(unique_chords) <= 3 else "중급" if len(unique_chords) <= 5 else "고급"}

**연습 팁**:
1. 각 화음의 구성음을 먼저 익히세요
2. 피아노 건반에서 화음 위치를 확인하세요
3. 마디별로 천천히 연습하세요
4. 화음 전환을 부드럽게 연결하세요
"""
        return summary


class PianoVisualizer:
    """Interactive piano keyboard visualizer"""
    
    @staticmethod
    def generate_playable_keyboard(chord_notes: List[str] = None) -> str:
        """
        Generate interactive playable piano keyboard
        
        Args:
            chord_notes: Optional notes to highlight
            
        Returns:
            HTML string with interactive keyboard
        """
        highlighted = chord_notes or []
        
        html = """
        <div style="margin: 20px 0;">
            <h3 style="text-align: center; color: #1f77b4;">🎹 인터랙티브 피아노</h3>
            <p style="text-align: center; color: #666;">건반을 클릭하여 소리를 들어보세요!</p>
            
            <div id="interactive-piano" style="margin: 20px auto; max-width: 800px;">
                <svg width="100%" height="220" viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg">
        """
        
        white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        x_pos = 0
        key_width = 50
        
        # White keys
        for i in range(14):  # 2 octaves
            octave = 4 + (i // 7)
            note_name = white_keys[i % 7]
            note = f"{note_name}{octave}"
            
            is_highlighted = note_name in highlighted
            fill = "#FFD700" if is_highlighted else "#FFFFFF"
            
            html += f'''
                <rect x="{x_pos}" y="0" width="{key_width}" height="150"
                      fill="{fill}" stroke="#000" stroke-width="2"
                      class="interactive-key white" data-note="{note}"
                      onmousedown="playNote('{note}')" />
                <text x="{x_pos + 25}" y="170" text-anchor="middle" 
                      font-size="12" fill="#333">{note_name}</text>
            '''
            
            # Black keys
            if note_name not in ['E', 'B']:
                black_note = f"{note_name}#{octave}"
                is_black_highlighted = f"{note_name}#" in highlighted
                black_fill = "#FFD700" if is_black_highlighted else "#000000"
                
                html += f'''
                    <rect x="{x_pos + 35}" y="0" width="30" height="100"
                          fill="{black_fill}" stroke="#000" stroke-width="1"
                          class="interactive-key black" data-note="{black_note}"
                          onmousedown="playNote('{black_note}')" />
                '''
            
            x_pos += key_width
        
        html += """
                </svg>
            </div>
        </div>
        
        <style>
            .interactive-key {
                cursor: pointer;
                transition: all 0.1s;
            }
            .interactive-key.white:hover {
                fill: #e0e0e0;
            }
            .interactive-key.black:hover {
                fill: #333;
            }
            .interactive-key:active {
                transform: translateY(2px);
            }
        </style>
        
        <script>
            // Simple Web Audio API for piano sounds
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Note frequencies (A4 = 440Hz)
            const noteFrequencies = {
                'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
                'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
                'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
                'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
                'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
                'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77
            };
            
            function playNote(note) {
                const frequency = noteFrequencies[note];
                if (!frequency) return;
                
                // Create oscillator
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.value = frequency;
                oscillator.type = 'sine';
                
                // Envelope
                gainNode.gain.setValueAtTime(0, audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(0.3, audioContext.currentTime + 0.01);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 1);
                
                console.log('Playing:', note, frequency + 'Hz');
            }
        </script>
        """
        
        return html
