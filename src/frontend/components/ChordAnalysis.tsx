import { useState } from 'react'
import './ChordAnalysis.css'
import PianoKeyboard from './PianoKeyboard'

// 음표 이름 매핑 (반음 단위로 12개)
const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

// 플랫(b)을 샤프(#)로 변환하는 매핑
const FLAT_TO_SHARP: Record<string, string> = {
  'Cb': 'B',
  'Db': 'C#',
  'Eb': 'D#',
  'Fb': 'E',
  'Gb': 'F#',
  'Ab': 'G#',
  'Bb': 'A#'
}

// 화음 타입 및 표시 이름 (초등학생 수준: 장3화음, 단3화음만)
const CHORD_OPTIONS: ChordOption[] = [
  { type: 'major', name: 'major', intervals: [0, 4, 7], displayName: '장3화음 (Major)' },
  { type: 'minor', name: 'minor', intervals: [0, 3, 7], displayName: '단3화음 (Minor)' },
]

// 화음 타입 (호환성 유지 - 현재 사용하지 않음)
// const CHORD_TYPES: Record<string, number[]> = {
//   'major': [0, 4, 7],
//   'minor': [0, 3, 7],
//   'diminished': [0, 3, 6],
//   'augmented': [0, 4, 8],
//   'sus2': [0, 2, 7],
//   'sus4': [0, 5, 7],
//   '7': [0, 4, 7, 10],
//   'maj7': [0, 4, 7, 11],
//   'm7': [0, 3, 7, 10],
//   'dim7': [0, 3, 6, 9],
//   'aug7': [0, 4, 8, 10],
// }

interface ChordOption {
  type: string
  name: string
  intervals: number[]
  displayName: string
}

const ChordAnalysis = () => {
  const [rootNote, setRootNote] = useState<string>('') // 선택된 루트 음
  const [selectedChordType, setSelectedChordType] = useState<string>('') // 선택된 화음 타입
  const [chordNotes, setChordNotes] = useState<string[]>([]) // 생성된 화음 구성음
  const [chordScore, setChordScore] = useState<Array<{ measure: number; chord: string; notes: string[] }>>([]) // 화음 악보
  const [octave, setOctave] = useState<number>(4)

  // 플랫(b)을 샤프(#)로 변환
  const convertFlatToSharp = (noteName: string): string => {
    if (noteName.includes('b')) {
      return FLAT_TO_SHARP[noteName] || noteName.replace('b', '#')
    }
    return noteName
  }

  // 음표에서 루트 음 추출 (플랫을 샤프로 변환)
  const extractRootNote = (note: string): string => {
    const match = note.match(/([A-G]#?b?)/)
    if (!match) return ''
    const rootName = match[1]
    return convertFlatToSharp(rootName)
  }

  // 루트 음과 화음 타입으로 구성음 생성
  const generateChordNotes = (root: string, chordType: string, baseOctave: number): string[] => {
    const rootMatch = root.match(/([A-G]#?b?)/)
    if (!rootMatch) return []
    
    let rootName = rootMatch[1]
    // 플랫을 샤프로 변환
    rootName = convertFlatToSharp(rootName)
    
    // NOTE_NAMES 배열에서 루트 음의 인덱스 찾기
    const rootIndex = NOTE_NAMES.findIndex(n => n === rootName)
    if (rootIndex === -1) {
      console.warn(`루트 음을 찾을 수 없습니다: ${rootName}`)
      return []
    }
    
    const chordOption = CHORD_OPTIONS.find(opt => opt.type === chordType)
    if (!chordOption) {
      console.warn(`화음 타입을 찾을 수 없습니다: ${chordType}`)
      return []
    }
    
    return chordOption.intervals.map(interval => {
      // 반음 단위로 interval을 더함
      const totalSemitones = rootIndex + interval
      // 12로 나눈 나머지로 음표 인덱스 계산 (0-11 범위)
      const noteIndex = totalSemitones % 12
      const noteName = NOTE_NAMES[noteIndex]
      // 옥타브 계산: 12 반음이 넘어가면 다음 옥타브
      const noteOctave = baseOctave + Math.floor(totalSemitones / 12)
      return `${noteName}${noteOctave}`
    })
  }

  // 화음 이름 생성
  const getChordName = (root: string, chordType: string): string => {
    const rootName = extractRootNote(root)
    const chordOption = CHORD_OPTIONS.find(opt => opt.type === chordType)
    if (!chordOption) return rootName
    
    if (chordType === 'major') {
      return rootName
    } else if (chordType === 'minor') {
      return `${rootName}m`
    } else {
      return `${rootName}${chordType}`
    }
  }

  // 건반 클릭 핸들러 - 루트 음 선택
  const handleKeyClick = (note: string) => {
    // const root = extractRootNote(note) // 사용하지 않음
    const noteOctave = parseInt(note.match(/\d/)?.[0] || '4')
    
    setRootNote(note)
    setSelectedChordType('') // 화음 타입 초기화
    setChordNotes([])
    setOctave(noteOctave)
  }

  // 화음 타입 선택 핸들러
  const handleChordTypeSelect = (chordType: string) => {
    if (!rootNote) return
    
    setSelectedChordType(chordType)
    const notes = generateChordNotes(rootNote, chordType, octave)
    setChordNotes(notes)
  }

  // 화음을 악보에 추가
  const handleAddToScore = () => {
    if (!rootNote || !selectedChordType || chordNotes.length === 0) return
    
    const chordName = getChordName(rootNote, selectedChordType)
    const newMeasure = {
      measure: chordScore.length + 1,
      chord: chordName,
      notes: chordNotes
    }
    
    setChordScore([...chordScore, newMeasure])
  }

  // 악보 초기화
  const handleClearScore = () => {
    setChordScore([])
  }

  // 개별 마디 삭제
  const handleDeleteMeasure = (index: number) => {
    setChordScore(chordScore.filter((_, i) => i !== index).map((m, i) => ({ ...m, measure: i + 1 })))
  }

  // 사용 가능한 화음 옵션 가져오기
  const getAvailableChords = (): ChordOption[] => {
    return CHORD_OPTIONS
  }

  return (
    <div className="chord-analysis">
      <h2>🎹 화음 구성하기</h2>
      <p className="subtitle">피아노 건반을 클릭하면 해당 음을 기반으로 연주할 수 있는 화음형이 표시됩니다!</p>
      
      <div className="chord-builder-section">
        <div className="piano-section">
          <h3>1️⃣ 피아노 건반을 클릭하세요</h3>
          <PianoKeyboard
            chordNotes={chordNotes}
            chordName={rootNote ? `${extractRootNote(rootNote)} 음을 기반으로 화음을 선택하세요` : '건반을 클릭하여 루트 음을 선택하세요'}
            interactive={true}
            octaves={[3, 4, 5]}
            onKeyClick={handleKeyClick}
          />
        </div>

        <div className="chord-controls">
          {rootNote && (
            <>
              <div className="control-group">
                <h3>2️⃣ 선택된 루트 음</h3>
                <div className="selected-root">
                  <span className="root-badge">{extractRootNote(rootNote)}</span>
                  <span className="root-octave">옥타브 {octave}</span>
                </div>
              </div>

              <div className="control-group">
                <h3>3️⃣ 화음 타입 선택</h3>
                <div className="chord-options-grid">
                  {getAvailableChords().map((chordOption) => (
                    <button
                      key={chordOption.type}
                      className={`chord-option-button ${selectedChordType === chordOption.type ? 'active' : ''}`}
                      onClick={() => handleChordTypeSelect(chordOption.type)}
                    >
                      {chordOption.displayName}
                    </button>
                  ))}
                </div>
              </div>

              {selectedChordType && chordNotes.length > 0 && (
                <div className="control-group">
                  <h3>4️⃣ 생성된 화음</h3>
                  <div className="chord-result">
                    <div className="chord-name-display">
                      {getChordName(rootNote, selectedChordType)}
                    </div>
                    <div className="chord-notes-display">
                      <p><strong>구성음:</strong></p>
                      <div className="selected-notes">
                        {chordNotes.map((note, i) => (
                          <span key={i} className="note-badge">{note}</span>
                        ))}
                      </div>
                    </div>
                    <button 
                      className="action-button" 
                      onClick={handleAddToScore}
                      style={{ marginTop: '1rem' }}
                    >
                      ➕ 악보에 추가하기
                    </button>
                  </div>
                </div>
              )}
            </>
          )}

          {!rootNote && (
            <div className="control-group">
              <p className="hint">💡 피아노 건반을 클릭하여 루트 음을 선택하세요!</p>
            </div>
          )}
        </div>
      </div>

      {chordScore.length > 0 && (
        <div className="chord-score-section">
          <div className="score-header">
            <h3>📜 화음 악보</h3>
            <button className="secondary-button" onClick={handleClearScore}>
              🗑️ 악보 초기화
            </button>
          </div>
          <div className="score-measures">
            {chordScore.map((measure, index) => (
              <div key={index} className="score-measure">
                <div className="measure-header">
                  <span className="measure-number">마디 {measure.measure}</span>
                  <span className="chord-label">{measure.chord}</span>
                  <button
                    className="delete-measure-btn"
                    onClick={() => handleDeleteMeasure(index)}
                    title="마디 삭제"
                  >
                    ✕
                  </button>
                </div>
                <div className="measure-content">
                  <PianoKeyboard
                    chordNotes={measure.notes}
                    chordName={measure.chord}
                    interactive={false}
                    octaves={[3, 4, 5]}
                  />
                  <div className="chord-notes-list">
                    {measure.notes.map((note, i) => (
                      <span key={i} className="note-badge-small">{note}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ChordAnalysis
