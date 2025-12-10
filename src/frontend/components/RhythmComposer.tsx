import { useState, useRef, useEffect } from 'react'
import './RhythmComposer.css'
import PianoKeyboard from './PianoKeyboard'

interface Note {
  note: string
  duration: number // 1 = 4분음표, 0.5 = 8분음표, 2 = 2분음표
  time: number // 마디 내 위치 (0부터 시작)
}

interface Measure {
  notes: Note[]
  chord?: string
  chordNotes?: string[]
}

const RhythmComposer = () => {
  const [timeSignature, setTimeSignature] = useState<'4/4' | '3/4' | '2/4'>('4/4')
  const [measures, setMeasures] = useState<Measure[]>([{ notes: [] }])
  const [currentMeasureIndex, setCurrentMeasureIndex] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackSpeed, setPlaybackSpeed] = useState(1)
  const [selectedNoteDuration, setSelectedNoteDuration] = useState<number>(1) // 4분음표 기본
  const audioContextRef = useRef<AudioContext | null>(null)
  const playbackTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const shouldStopRef = useRef<boolean>(false)

  useEffect(() => {
    // Web Audio API 초기화
    if (typeof window !== 'undefined') {
      try {
        audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)()
      } catch (e) {
        console.warn('Web Audio API를 사용할 수 없습니다:', e)
      }
    }

    return () => {
      if (playbackTimeoutRef.current) {
        clearTimeout(playbackTimeoutRef.current)
      }
    }
  }, [])

  // 박자에 따른 마디 길이 계산
  const getMeasureLength = (): number => {
    switch (timeSignature) {
      case '4/4': return 4
      case '3/4': return 3
      case '2/4': return 2
      default: return 4
    }
  }

  // 음표 주파수 매핑
  const noteFrequencies: Record<string, number> = {
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56,
    'E3': 164.81, 'F3': 174.61, 'F#3': 185.00, 'G3': 196.00,
    'G#3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
    'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
    'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
    'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
  }

  // 음표 재생
  const playNote = (note: string, duration: number = 0.5) => {
    if (!audioContextRef.current) return

    const frequency = noteFrequencies[note]
    if (!frequency) return

    try {
      const oscillator = audioContextRef.current.createOscillator()
      const gainNode = audioContextRef.current.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(audioContextRef.current.destination)

      oscillator.frequency.value = frequency
      oscillator.type = 'sine'

      const now = audioContextRef.current.currentTime
      gainNode.gain.setValueAtTime(0, now)
      gainNode.gain.linearRampToValueAtTime(0.3, now + 0.01)
      gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration * playbackSpeed)

      oscillator.start(now)
      oscillator.stop(now + duration * playbackSpeed)
    } catch (e) {
      console.warn('음표 재생 실패:', e)
    }
  }

  // 화음 분석 (간단한 버전)
  const analyzeChord = (notes: string[]): { chord: string; chordNotes: string[] } => {
    if (notes.length === 0) return { chord: '', chordNotes: [] }

    // 음표를 MIDI 번호로 변환
    const midiNotes = notes
      .map(note => {
        const match = note.match(/([A-G]#?b?)(\d)/)
        if (!match) return null
        const noteName = match[1].replace('b', '#')
        const oct = parseInt(match[2])
        const noteIndex = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].indexOf(noteName)
        if (noteIndex === -1) return null
        return (oct - 4) * 12 + noteIndex + 60
      })
      .filter((n): n is number => n !== null)
      .sort((a, b) => a - b)

    if (midiNotes.length === 0) return { chord: '', chordNotes: [] }

    const rootMidi = midiNotes[0]
    const rootNote = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][rootMidi % 12]
    const intervals = midiNotes.map(n => n - rootMidi)

    // 간단한 화음 패턴 매칭
    if (intervals.includes(0) && intervals.includes(4) && intervals.includes(7)) {
      return { chord: rootNote, chordNotes: notes }
    } else if (intervals.includes(0) && intervals.includes(3) && intervals.includes(7)) {
      return { chord: `${rootNote}m`, chordNotes: notes }
    }

    return { chord: rootNote, chordNotes: notes }
  }

  // 건반 클릭 핸들러
  const handleKeyClick = (note: string) => {
    const measureLength = getMeasureLength()
    const currentMeasure = measures[currentMeasureIndex]
    const remainingTime = measureLength - currentTime

    if (remainingTime < selectedNoteDuration) {
      // 현재 마디가 가득 찬 경우 새 마디 추가
      const chordAnalysis = analyzeChord(currentMeasure.notes.map(n => n.note))
      const updatedMeasures = [...measures]
      updatedMeasures[currentMeasureIndex] = {
        ...currentMeasure,
        chord: chordAnalysis.chord,
        chordNotes: chordAnalysis.chordNotes
      }
      
      setMeasures([...updatedMeasures, { notes: [] }])
      setCurrentMeasureIndex(updatedMeasures.length)
      setCurrentTime(0)
    } else {
      // 현재 마디에 음표 추가
      const newNote: Note = {
        note,
        duration: Math.min(selectedNoteDuration, remainingTime),
        time: currentTime
      }

      const updatedMeasures = [...measures]
      updatedMeasures[currentMeasureIndex] = {
        ...currentMeasure,
        notes: [...currentMeasure.notes, newNote]
      }

      // 화음 분석
      const allNotes = [...currentMeasure.notes, newNote].map(n => n.note)
      const chordAnalysis = analyzeChord(allNotes)
      
      updatedMeasures[currentMeasureIndex] = {
        ...updatedMeasures[currentMeasureIndex],
        chord: chordAnalysis.chord,
        chordNotes: chordAnalysis.chordNotes
      }

      setMeasures(updatedMeasures)
      setCurrentTime(currentTime + newNote.duration)

      // 음표 재생
      playNote(note, newNote.duration)
    }
  }

  // 마디 재생
  const playMeasure = async (measureIndex: number, shouldStopRef: { current: boolean }) => {
    const measure = measures[measureIndex]
    if (!measure || measure.notes.length === 0) return

    for (const note of measure.notes) {
      if (shouldStopRef.current) break
      playNote(note.note, note.duration)
      await new Promise(resolve => setTimeout(resolve, note.duration * 1000 / playbackSpeed))
    }
  }

  // 전체 재생
  const handlePlayAll = async () => {
    if (isPlaying) {
      shouldStopRef.current = true
      setIsPlaying(false)
      return
    }

    shouldStopRef.current = false
    setIsPlaying(true)
    
    try {
      for (let i = 0; i < measures.length; i++) {
        if (shouldStopRef.current) break
        await playMeasure(i, shouldStopRef)
        // 마디 간 간격
        if (!shouldStopRef.current && i < measures.length - 1) {
          await new Promise(resolve => setTimeout(resolve, 200 / playbackSpeed))
        }
      }
    } finally {
      setIsPlaying(false)
      shouldStopRef.current = false
    }
  }

  // 마디 삭제
  const handleDeleteMeasure = (index: number) => {
    if (measures.length === 1) {
      setMeasures([{ notes: [] }])
      setCurrentMeasureIndex(0)
      setCurrentTime(0)
    } else {
      const newMeasures = measures.filter((_, i) => i !== index)
      setMeasures(newMeasures)
      if (currentMeasureIndex >= newMeasures.length) {
        setCurrentMeasureIndex(newMeasures.length - 1)
      }
    }
  }

  // 리셋
  const handleReset = () => {
    setMeasures([{ notes: [] }])
    setCurrentMeasureIndex(0)
    setCurrentTime(0)
    setIsPlaying(false)
  }

  // 악보 렌더링
  const renderScore = () => {
    return (
      <div className="score-display">
        <div className="score-header">
          <span className="time-signature">{timeSignature}</span>
          <span className="key-signature">C Major</span>
        </div>
        {measures.map((measure, measureIndex) => (
          <div key={measureIndex} className="measure-container">
            <div className="measure-header">
              <span className="measure-number">마디 {measureIndex + 1}</span>
              {measure.chord && (
                <span className="chord-label">{measure.chord}</span>
              )}
              <button
                className="delete-measure-btn"
                onClick={() => handleDeleteMeasure(measureIndex)}
                title="마디 삭제"
              >
                ✕
              </button>
            </div>
            <div className="measure-content">
              <div className="staff-container">
                <div className="staff">
                  {/* 오선 */}
                  {[0, 1, 2, 3, 4].map(line => (
                    <div
                      key={line}
                      className="staff-line"
                      style={{ bottom: `${line * 20 + 50}px` }}
                    />
                  ))}
                  {/* 음표 */}
                  {measure.notes.map((note, noteIndex) => {
                    const notePosition = getNotePosition(note.note)
                    const noteWidth = note.duration * 50
                    const noteLeft = note.time * 50
                    
                    return (
                      <div
                        key={noteIndex}
                        className="note-element"
                        style={{
                          left: `${noteLeft}px`,
                          bottom: `${notePosition * 10 + 50}px`,
                          width: `${noteWidth}px`
                        }}
                        title={`${note.note} (${note.duration}박)`}
                      >
                        <div className="note-head"></div>
                        {note.duration < 1 && <div className="note-flag"></div>}
                        {note.duration >= 2 && <div className="note-stem"></div>}
                        <span className="note-name">{note.note}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
              {measure.chordNotes && measure.chordNotes.length > 0 && (
                <div className="chord-display">
                  <PianoKeyboard
                    chordNotes={measure.chordNotes}
                    chordName={measure.chord || ''}
                    interactive={false}
                    octaves={[3, 4, 5]}
                  />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    )
  }

  // 음표 위치 계산 (간단한 버전)
  const getNotePosition = (note: string): number => {
    const match = note.match(/([A-G]#?)(\d)/)
    if (!match) return 0
    
    const noteName = match[1]
    const octave = parseInt(match[2])
    
    const notePositions: Record<string, number> = {
      'C': 0, 'C#': 0.5, 'D': 1, 'D#': 1.5,
      'E': 2, 'F': 2.5, 'F#': 3, 'G': 3.5,
      'G#': 4, 'A': 4.5, 'A#': 5, 'B': 5.5
    }
    
    const basePosition = notePositions[noteName] || 0
    return basePosition + (octave - 4) * 7
  }

  const currentMeasure = measures[currentMeasureIndex]
  const measureLength = getMeasureLength()
  const remainingTime = measureLength - currentTime

  return (
    <div className="rhythm-composer">
      <h2>🎼 리듬 작곡기</h2>
      <p className="subtitle">박자에 맞춰 건반을 클릭하면 자동으로 화음 반주 악보가 그려집니다!</p>

      <div className="composer-controls">
        <div className="control-group">
          <label>박자</label>
          <select
            className="form-control"
            value={timeSignature}
            onChange={(e) => {
              setTimeSignature(e.target.value as '4/4' | '3/4' | '2/4')
              setCurrentTime(0)
            }}
          >
            <option value="4/4">4/4박자</option>
            <option value="3/4">3/4박자</option>
            <option value="2/4">2/4박자</option>
          </select>
        </div>

        <div className="control-group">
          <label>음표 길이</label>
          <select
            className="form-control"
            value={selectedNoteDuration}
            onChange={(e) => setSelectedNoteDuration(parseFloat(e.target.value))}
          >
            <option value={0.25}>16분음표 (0.25박)</option>
            <option value={0.5}>8분음표 (0.5박)</option>
            <option value={1}>4분음표 (1박)</option>
            <option value={2}>2분음표 (2박)</option>
            <option value={4}>온음표 (4박)</option>
          </select>
        </div>

        <div className="control-group">
          <label>재생 속도</label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={playbackSpeed}
            onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
            className="speed-slider"
          />
          <span className="speed-value">{playbackSpeed.toFixed(1)}x</span>
        </div>

        <div className="control-group">
          <button
            className={`play-button ${isPlaying ? 'playing' : ''}`}
            onClick={handlePlayAll}
            disabled={measures.every(m => m.notes.length === 0)}
          >
            {isPlaying ? '⏸ 정지' : '▶ 재생'}
          </button>
          <button className="reset-button" onClick={handleReset}>
            🔄 초기화
          </button>
        </div>
      </div>

      <div className="composer-main">
        <div className="piano-section">
          <h3>피아노 건반</h3>
          <div className="current-measure-info">
            <p>
              <strong>현재 마디:</strong> {currentMeasureIndex + 1} / {measures.length}
            </p>
            <p>
              <strong>남은 박자:</strong> {remainingTime.toFixed(2)} / {measureLength}
            </p>
          </div>
          <PianoKeyboard
            chordNotes={currentMeasure.notes.map(n => n.note)}
            chordName={currentMeasure.chord || '음표를 입력하세요'}
            interactive={true}
            octaves={[3, 4, 5]}
            onKeyClick={handleKeyClick}
          />
        </div>

        <div className="score-section">
          <h3>생성된 악보</h3>
          {renderScore()}
        </div>
      </div>

      <div className="instructions">
        <h4>📖 사용 방법</h4>
        <ol>
          <li>박자를 선택하세요 (4/4, 3/4, 2/4)</li>
          <li>음표 길이를 선택하세요 (4분음표, 8분음표 등)</li>
          <li>피아노 건반을 클릭하여 음표를 입력하세요</li>
          <li>마디가 가득 차면 자동으로 새 마디가 생성됩니다</li>
          <li>각 마디의 화음이 자동으로 분석되어 표시됩니다</li>
          <li>재생 버튼을 눌러 작곡한 곡을 들어보세요!</li>
        </ol>
      </div>
    </div>
  )
}

export default RhythmComposer

