import { useState, useRef, useEffect } from 'react'
import './RhythmComposer.css'
import PianoKeyboard from './PianoKeyboard'

interface Note {
  note: string
  duration: number // 1 = 4분음표, 0.5 = 8분음표, 2 = 2분음표
  time: number // 마디 내 위치 (0부터 시작)
}

interface AccompanimentNote {
  note: string
  duration: number
  time: number
}

interface Measure {
  notes: Note[]
  chord?: string
  chordNotes?: string[]
  accompaniment?: AccompanimentNote[] // 자동 생성된 반주
}

const RhythmComposer = () => {
  const [timeSignature, setTimeSignature] = useState<'4/4' | '3/4' | '2/4'>('4/4')
  const [measures, setMeasures] = useState<Measure[]>([{ notes: [] }])
  const [currentMeasureIndex, setCurrentMeasureIndex] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [playbackSpeed, setPlaybackSpeed] = useState(1)
  const [selectedNoteDuration, setSelectedNoteDuration] = useState<number>(1) // 4분음표 기본
  const [inputMode, setInputMode] = useState<'piano' | 'notes'>('piano') // 입력 모드
  const [selectedOctave, setSelectedOctave] = useState<number>(4) // 선택된 옥타브
  const audioContextRef = useRef<AudioContext | null>(null)
  const playbackTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const shouldStopRef = useRef<boolean>(false)

  // 계이름 매핑 (도레미파솔라시)
  const solfegeNotes: Record<string, string> = {
    '도': 'C',
    '레': 'D',
    '미': 'E',
    '파': 'F',
    '솔': 'G',
    '라': 'A',
    '시': 'B'
  }

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

  // 화음 분석 및 반주 생성
  const analyzeChordAndGenerateAccompaniment = (notes: Note[]): { 
    chord: string
    chordNotes: string[]
    accompaniment: AccompanimentNote[]
  } => {
    if (notes.length === 0) return { chord: '', chordNotes: [], accompaniment: [] }

    // 음표를 MIDI 번호로 변환
    const midiNotes = notes
      .map(n => {
        const match = n.note.match(/([A-G]#?b?)(\d)/)
        if (!match) return null
        const noteName = match[1].replace('b', '#')
        const oct = parseInt(match[2])
        const noteIndex = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].indexOf(noteName)
        if (noteIndex === -1) return null
        return { midi: (oct - 4) * 12 + noteIndex + 60, note: n.note, time: n.time, duration: n.duration }
      })
      .filter((n): n is { midi: number; note: string; time: number; duration: number } => n !== null)
      .sort((a, b) => a.midi - b.midi)

    if (midiNotes.length === 0) return { chord: '', chordNotes: [], accompaniment: [] }

    // 마디 내 주요 음표 찾기 (가장 많이 나타나는 음)
    const noteCounts: Record<number, number> = {}
    midiNotes.forEach(n => {
      const pitchClass = n.midi % 12
      noteCounts[pitchClass] = (noteCounts[pitchClass] || 0) + 1
    })

    const dominantPitchClass = Object.entries(noteCounts)
      .sort((a, b) => b[1] - a[1])[0]?.[0]
    
    if (!dominantPitchClass) return { chord: '', chordNotes: [], accompaniment: [] }

    const rootMidi = parseInt(dominantPitchClass)
    const rootNote = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][rootMidi]
    
    // 화음 결정 (C major 스케일 기준)
    // I, IV, V, vi 중 선택
    let chordSymbol = 'I'
    let chordNotes: string[] = []
    
    // 마디의 첫 음표와 마지막 음표를 고려하여 화음 선택
    const firstNote = midiNotes[0].midi % 12
    const lastNote = midiNotes[midiNotes.length - 1].midi % 12
    
    // C major 스케일: C(0), D(2), E(4), F(5), G(7), A(9), B(11)
    if ([0, 4, 7].includes(rootMidi)) {
      // C, E, G -> C major (I)
      chordSymbol = 'I'
      chordNotes = [`C${selectedOctave}`, `E${selectedOctave}`, `G${selectedOctave}`]
    } else if ([5, 9, 0].includes(rootMidi)) {
      // F, A, C -> F major (IV)
      chordSymbol = 'IV'
      chordNotes = [`F${selectedOctave}`, `A${selectedOctave}`, `C${selectedOctave + 1}`]
    } else if ([7, 11, 2].includes(rootMidi)) {
      // G, B, D -> G major (V)
      chordSymbol = 'V'
      chordNotes = [`G${selectedOctave}`, `B${selectedOctave}`, `D${selectedOctave + 1}`]
    } else if ([9, 0, 4].includes(rootMidi)) {
      // A, C, E -> A minor (vi)
      chordSymbol = 'vi'
      chordNotes = [`A${selectedOctave}`, `C${selectedOctave + 1}`, `E${selectedOctave + 1}`]
    } else {
      // 기본값: C major
      chordSymbol = 'I'
      chordNotes = [`C${selectedOctave}`, `E${selectedOctave}`, `G${selectedOctave}`]
    }

    // 반주 생성 (블록 코드 형태, 마디 전체 길이)
    const measureLength = getMeasureLength()
    const accompaniment: AccompanimentNote[] = []
    
    // 마디를 2박자 단위로 나누어 반주 생성
    for (let time = 0; time < measureLength; time += 2) {
      const duration = Math.min(2, measureLength - time)
      chordNotes.forEach(chordNote => {
        accompaniment.push({
          note: chordNote,
          duration: duration,
          time: time
        })
      })
    }

    return {
      chord: chordSymbol === 'I' ? rootNote : `${rootNote}${chordSymbol}`,
      chordNotes,
      accompaniment
    }
  }

  // 계이름으로 음표 추가
  const handleSolfegeClick = (solfege: string) => {
    const noteName = solfegeNotes[solfege]
    if (!noteName) return
    
    const note = `${noteName}${selectedOctave}`
    
    // 마디가 가득 찬 경우 자동으로 다음 마디로 이동
    const measureLength = getMeasureLength()
    const currentMeasure = measures[currentMeasureIndex]
    const remainingTime = measureLength - currentTime
    
    if (remainingTime < selectedNoteDuration) {
      // 현재 마디 완료 처리 및 새 마디로 이동
      const chordAnalysis = analyzeChordAndGenerateAccompaniment(currentMeasure.notes)
      const updatedMeasures = [...measures]
      updatedMeasures[currentMeasureIndex] = {
        ...currentMeasure,
        chord: chordAnalysis.chord,
        chordNotes: chordAnalysis.chordNotes,
        accompaniment: chordAnalysis.accompaniment
      }
      
      // 새 마디 추가
      updatedMeasures.push({ notes: [] })
      const newMeasureIndex = updatedMeasures.length - 1
      
      // 새 마디에 음표 추가
      const newNote: Note = {
        note,
        duration: Math.min(selectedNoteDuration, measureLength),
        time: 0
      }
      
      updatedMeasures[newMeasureIndex] = {
        notes: [newNote],
        chord: '',
        chordNotes: [],
        accompaniment: []
      }
      
      // 화음 분석 및 반주 생성
      const chordAnalysisNew = analyzeChordAndGenerateAccompaniment([newNote])
      updatedMeasures[newMeasureIndex] = {
        ...updatedMeasures[newMeasureIndex],
        chord: chordAnalysisNew.chord,
        chordNotes: chordAnalysisNew.chordNotes,
        accompaniment: chordAnalysisNew.accompaniment
      }
      
      // 상태 업데이트
      setMeasures(updatedMeasures)
      setCurrentMeasureIndex(newMeasureIndex)
      setCurrentTime(newNote.duration)
      
      // 음표 재생
      playNote(note, newNote.duration)
    } else {
      // 일반적인 경우 handleKeyClick 사용
      handleKeyClick(note)
    }
  }

  // 건반 클릭 핸들러
  const handleKeyClick = (note: string) => {
    const measureLength = getMeasureLength()
    let currentMeasure = measures[currentMeasureIndex]
    let remainingTime = measureLength - currentTime
    let newCurrentTime = currentTime
    let newCurrentMeasureIndex = currentMeasureIndex
    let newMeasures = [...measures]

    // 마디가 가득 찬 경우 새 마디로 이동
    if (remainingTime < selectedNoteDuration) {
      // 현재 마디의 화음 분석 및 반주 생성
      const chordAnalysis = analyzeChordAndGenerateAccompaniment(currentMeasure.notes)
      newMeasures[newCurrentMeasureIndex] = {
        ...currentMeasure,
        chord: chordAnalysis.chord,
        chordNotes: chordAnalysis.chordNotes,
        accompaniment: chordAnalysis.accompaniment
      }
      
      // 새 마디 추가
      newMeasures.push({ notes: [] })
      newCurrentMeasureIndex = newMeasures.length - 1
      newCurrentTime = 0
      remainingTime = measureLength
    }

    // 음표 추가
    const noteDuration = Math.min(selectedNoteDuration, remainingTime)
    const newNote: Note = {
      note,
      duration: noteDuration,
      time: newCurrentTime
    }

    currentMeasure = newMeasures[newCurrentMeasureIndex]
    newMeasures[newCurrentMeasureIndex] = {
      ...currentMeasure,
      notes: [...currentMeasure.notes, newNote]
    }

    // 화음 분석 및 반주 생성
    const allNotes = [...currentMeasure.notes, newNote]
    const chordAnalysis = analyzeChordAndGenerateAccompaniment(allNotes)
    
    newMeasures[newCurrentMeasureIndex] = {
      ...newMeasures[newCurrentMeasureIndex],
      chord: chordAnalysis.chord,
      chordNotes: chordAnalysis.chordNotes,
      accompaniment: chordAnalysis.accompaniment
    }

    // 상태 업데이트
    setMeasures(newMeasures)
    setCurrentMeasureIndex(newCurrentMeasureIndex)
    setCurrentTime(newCurrentTime + noteDuration)

    // 음표 재생
    playNote(note, noteDuration)
  }

  // 마디 재생 (멜로디 + 반주)
  const playMeasure = async (measureIndex: number, shouldStopRef: { current: boolean }) => {
    const measure = measures[measureIndex]
    if (!measure || measure.notes.length === 0) return

    // 멜로디와 반주를 동시에 재생하기 위해 시간별로 정렬
    const allEvents: Array<{ note: string; duration: number; time: number; type: 'melody' | 'accompaniment' }> = []
    
    // 멜로디 이벤트 추가
    measure.notes.forEach(note => {
      allEvents.push({ ...note, type: 'melody' })
    })
    
    // 반주 이벤트 추가
    if (measure.accompaniment) {
      measure.accompaniment.forEach(acc => {
        allEvents.push({ ...acc, type: 'accompaniment' })
      })
    }
    
    // 시간순으로 정렬
    allEvents.sort((a, b) => a.time - b.time)
    
    // 재생
    let currentTime = 0
    for (const event of allEvents) {
      if (shouldStopRef.current) break
      
      // 이벤트 시간까지 대기
      if (event.time > currentTime) {
        await new Promise(resolve => setTimeout(resolve, (event.time - currentTime) * 1000 / playbackSpeed))
        currentTime = event.time
      }
      
      // 음표 재생 (반주는 볼륨을 낮춤)
      const volume = event.type === 'accompaniment' ? 0.15 : 0.3
      playNoteWithVolume(event.note, event.duration, volume)
    }
    
    // 마디 끝까지 대기
    const measureLength = getMeasureLength()
    if (currentTime < measureLength) {
      await new Promise(resolve => setTimeout(resolve, (measureLength - currentTime) * 1000 / playbackSpeed))
    }
  }

  // 볼륨 조절 음표 재생
  const playNoteWithVolume = (note: string, duration: number = 0.5, volume: number = 0.3) => {
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
      gainNode.gain.linearRampToValueAtTime(volume, now + 0.01)
      gainNode.gain.exponentialRampToValueAtTime(0.01, now + duration * playbackSpeed)

      oscillator.start(now)
      oscillator.stop(now + duration * playbackSpeed)
    } catch (e) {
      console.warn('음표 재생 실패:', e)
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
              {/* 반주 악보 표시 */}
              {measure.accompaniment && measure.accompaniment.length > 0 && (
                <div className="accompaniment-staff">
                  <div className="accompaniment-label">반주</div>
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
                      {/* 반주 음표 */}
                      {measure.accompaniment.map((acc, accIndex) => {
                        const notePosition = getNotePosition(acc.note)
                        const noteWidth = acc.duration * 50
                        const noteLeft = acc.time * 50
                        
                        return (
                          <div
                            key={accIndex}
                            className="note-element accompaniment-note"
                            style={{
                              left: `${noteLeft}px`,
                              bottom: `${notePosition * 10 + 50}px`,
                              width: `${noteWidth}px`
                            }}
                            title={`${acc.note} (반주)`}
                          >
                            <div className="note-head"></div>
                            {acc.duration >= 2 && <div className="note-stem"></div>}
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>
              )}
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
        <div className="input-section">
          <div className="input-mode-selector">
            <button
              className={`mode-button ${inputMode === 'piano' ? 'active' : ''}`}
              onClick={() => setInputMode('piano')}
            >
              🎹 피아노 건반
            </button>
            <button
              className={`mode-button ${inputMode === 'notes' ? 'active' : ''}`}
              onClick={() => setInputMode('notes')}
            >
              🎵 계이름 입력
            </button>
          </div>

          {inputMode === 'notes' && (
            <div className="solfege-input">
              <div className="octave-selector">
                <label>옥타브:</label>
                <select
                  className="form-control"
                  value={selectedOctave}
                  onChange={(e) => setSelectedOctave(parseInt(e.target.value))}
                >
                  <option value={3}>3옥타브</option>
                  <option value={4}>4옥타브</option>
                  <option value={5}>5옥타브</option>
                </select>
              </div>
              <div className="solfege-buttons">
                {Object.keys(solfegeNotes).map(solfege => (
                  <button
                    key={solfege}
                    className="solfege-button"
                    onClick={() => handleSolfegeClick(solfege)}
                  >
                    {solfege}
                  </button>
                ))}
              </div>
              <div className="solfege-hint">
                <p>💡 마디가 가득 차면 자동으로 다음 마디로 넘어갑니다!</p>
              </div>
            </div>
          )}

          {inputMode === 'piano' && (
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
          )}
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

