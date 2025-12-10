import { useState } from 'react'
import './ChordAnalysis.css'
import PianoKeyboard from './PianoKeyboard'

// 음표 이름 매핑
const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
const NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

// 화음 타입
const CHORD_TYPES: Record<string, number[]> = {
  'major': [0, 4, 7],
  'minor': [0, 3, 7],
  'diminished': [0, 3, 6],
  'augmented': [0, 4, 8],
  'sus2': [0, 2, 7],
  'sus4': [0, 5, 7],
  '7': [0, 4, 7, 10],
  'maj7': [0, 4, 7, 11],
  'm7': [0, 3, 7, 10],
  'dim7': [0, 3, 6, 9],
  'aug7': [0, 4, 8, 10],
}

const ChordAnalysis = () => {
  const [selectedNotes, setSelectedNotes] = useState<Set<string>>(new Set())
  const [chordName, setChordName] = useState<string>('')
  const [chordType, setChordType] = useState<string>('major')
  const [octave, setOctave] = useState<number>(4)

  // 선택된 음표를 화음 이름으로 변환
  const analyzeChord = (notes: string[]): string => {
    if (notes.length === 0) return ''
    
    // 음표를 MIDI 번호로 변환 (C4 = 60)
    const midiNotes = notes
      .map(note => {
        const match = note.match(/([A-G]#?b?)(\d)/)
        if (!match) return null
        
        const noteName = match[1]
        const oct = parseInt(match[2])
        
        // 음표 이름을 인덱스로 변환
        let noteIndex = NOTE_NAMES.findIndex(n => n === noteName || n === noteName.replace('b', '#'))
        if (noteIndex === -1) {
          // 플랫 처리
          const flatIndex = NOTE_NAMES_FLAT.findIndex(n => n === noteName)
          if (flatIndex !== -1) {
            noteIndex = flatIndex
          }
        }
        
        if (noteIndex === -1) return null
        
        return (oct - 4) * 12 + noteIndex + 60
      })
      .filter((n): n is number => n !== null)
      .sort((a, b) => a - b)
    
    if (midiNotes.length === 0) return ''
    
    // 루트 음 찾기 (가장 낮은 음)
    const rootMidi = midiNotes[0]
    const rootNote = NOTE_NAMES[rootMidi % 12]
    
    // 다른 음들과의 간격 계산
    const intervals = midiNotes.map(n => n - rootMidi)
    
    // 화음 타입 매칭
    for (const [type, pattern] of Object.entries(CHORD_TYPES)) {
      if (intervals.length === pattern.length) {
        const matches = pattern.every(p => intervals.includes(p))
        if (matches) {
          if (type === 'major') {
            return rootNote
          } else if (type === 'minor') {
            return `${rootNote}m`
          } else {
            return `${rootNote}${type}`
          }
        }
      }
    }
    
    // 정확히 매칭되지 않으면 선택된 음표 표시
    return notes.join(' ')
  }

  const handleKeyClick = (note: string) => {
    setSelectedNotes(prev => {
      const newSet = new Set(prev)
      if (newSet.has(note)) {
        newSet.delete(note)
      } else {
        newSet.add(note)
      }
      
      // 화음 분석
      const notesArray = Array.from(newSet)
      const analyzed = analyzeChord(notesArray)
      setChordName(analyzed)
      
      return newSet
    })
  }

  const handleClear = () => {
    setSelectedNotes(new Set())
    setChordName('')
  }

  const handleBuildChord = () => {
    // 선택된 화음 타입으로 음표 구성
    const rootNote = NOTE_NAMES[0] // C를 기본으로
    const pattern = CHORD_TYPES[chordType] || CHORD_TYPES['major']
    
    const chordNotes = pattern.map(interval => {
      const noteIndex = interval % 12
      const noteName = NOTE_NAMES[noteIndex]
      return `${noteName}${octave}`
    })
    
    setSelectedNotes(new Set(chordNotes))
    setChordName(analyzeChord(chordNotes))
  }

  const selectedNotesArray = Array.from(selectedNotes)

  return (
    <div className="chord-analysis">
      <h2>🎹 화음 구성하기</h2>
      
      <div className="chord-builder-section">
        <div className="piano-section">
          <h3>피아노 건반을 클릭하여 화음을 만들어보세요!</h3>
          <PianoKeyboard
            chordNotes={selectedNotesArray}
            chordName={chordName || '화음을 구성해주세요'}
            interactive={true}
            octaves={[3, 4, 5]}
            onKeyClick={handleKeyClick}
          />
        </div>

        <div className="chord-controls">
          <div className="control-group">
            <h3>선택된 음표</h3>
            {selectedNotesArray.length > 0 ? (
              <div className="selected-notes">
                {selectedNotesArray.map((note, i) => (
                  <span key={i} className="note-badge">{note}</span>
                ))}
              </div>
            ) : (
              <p className="hint">건반을 클릭하여 음표를 선택하세요</p>
            )}
          </div>

          {chordName && (
            <div className="chord-result">
              <h3>인식된 화음</h3>
              <div className="chord-name-display">{chordName}</div>
            </div>
          )}

          <div className="control-group">
            <h3>빠른 화음 구성</h3>
            <div className="chord-builder-controls">
              <select
                className="form-control"
                value={chordType}
                onChange={(e) => setChordType(e.target.value)}
              >
                <option value="major">장3화음 (Major)</option>
                <option value="minor">단3화음 (Minor)</option>
                <option value="diminished">감3화음 (Diminished)</option>
                <option value="augmented">증3화음 (Augmented)</option>
                <option value="sus2">서스2 (Sus2)</option>
                <option value="sus4">서스4 (Sus4)</option>
                <option value="7">7화음 (Dominant 7th)</option>
                <option value="maj7">장7화음 (Major 7th)</option>
                <option value="m7">단7화음 (Minor 7th)</option>
                <option value="dim7">감7화음 (Diminished 7th)</option>
              </select>
              
              <select
                className="form-control"
                value={octave}
                onChange={(e) => setOctave(parseInt(e.target.value))}
              >
                <option value={3}>3옥타브</option>
                <option value={4}>4옥타브</option>
                <option value={5}>5옥타브</option>
              </select>
              
              <button className="action-button" onClick={handleBuildChord}>
                🎵 화음 구성하기
              </button>
            </div>
          </div>

          <div className="control-group">
            <button className="secondary-button" onClick={handleClear}>
              🗑️ 모두 지우기
            </button>
          </div>
        </div>
      </div>

      {chordName && (
        <div className="chord-info-section">
          <h3>📚 화음 정보</h3>
          <div className="info-box">
            <p><strong>화음 이름:</strong> {chordName}</p>
            <p><strong>구성음:</strong> {selectedNotesArray.join(', ')}</p>
            <p className="hint">
              💡 이 화음을 사용하여 곡을 연주하거나, 다른 화음과 조합하여 화음 진행을 만들어보세요!
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default ChordAnalysis
