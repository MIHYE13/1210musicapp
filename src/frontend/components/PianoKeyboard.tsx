import { useState, useEffect, useRef } from 'react'
import './PianoKeyboard.css'

interface PianoKeyboardProps {
  chordNotes?: string[]
  chordName?: string
  interactive?: boolean
  octaves?: number[]
}

const PianoKeyboard = ({ 
  chordNotes = [], 
  chordName = '',
  interactive = true,
  octaves = [4, 5]
}: PianoKeyboardProps) => {
  const [pressedKeys, setPressedKeys] = useState<Set<string>>(new Set())
  const audioContextRef = useRef<AudioContext | null>(null)

  useEffect(() => {
    // Web Audio API 초기화
    if (interactive && typeof window !== 'undefined') {
      try {
        audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)()
      } catch (e) {
        console.warn('Web Audio API를 사용할 수 없습니다:', e)
      }
    }
  }, [interactive])

  // 음표 주파수 매핑 (A4 = 440Hz)
  const noteFrequencies: Record<string, number> = {
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
    'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
    'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
    'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
  }

  const WHITE_KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
  const BLACK_KEY_POSITIONS: Record<string, number> = {
    'C': 0.6, 'D': 0.4, 'F': 0.6, 'G': 0.4, 'A': 0.4
  }

  const playNote = (note: string) => {
    if (!interactive || !audioContextRef.current) return

    const frequency = noteFrequencies[note]
    if (!frequency) return

    try {
      const oscillator = audioContextRef.current.createOscillator()
      const gainNode = audioContextRef.current.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(audioContextRef.current.destination)

      oscillator.frequency.value = frequency
      oscillator.type = 'sine'

      // Envelope
      const now = audioContextRef.current.currentTime
      gainNode.gain.setValueAtTime(0, now)
      gainNode.gain.linearRampToValueAtTime(0.3, now + 0.01)
      gainNode.gain.exponentialRampToValueAtTime(0.01, now + 1)

      oscillator.start(now)
      oscillator.stop(now + 1)

      // 시각적 피드백
      setPressedKeys(prev => new Set([...prev, note]))
      setTimeout(() => {
        setPressedKeys(prev => {
          const next = new Set(prev)
          next.delete(note)
          return next
        })
      }, 100)
    } catch (e) {
      console.warn('음표 재생 실패:', e)
    }
  }

  const isNoteHighlighted = (noteName: string, octave: number): boolean => {
    if (chordNotes.length === 0) return false
    const noteFull = `${noteName}${octave}`
    const normalizedNotes = chordNotes.map(n => n.replace('♯', '#').replace('♭', 'b'))
    return normalizedNotes.includes(noteName) || normalizedNotes.includes(noteFull) ||
           normalizedNotes.some(n => n.startsWith(noteName) && n.includes(String(octave)))
  }

  const isNotePressed = (noteName: string, octave: number): boolean => {
    const noteFull = `${noteName}${octave}`
    return pressedKeys.has(noteFull)
  }

  const whiteKeyWidth = 50
  const whiteKeyHeight = 150
  const blackKeyWidth = 30
  const blackKeyHeight = 100

  let xPos = 0
  const whiteKeys: JSX.Element[] = []
  const blackKeys: JSX.Element[] = []

  octaves.forEach(octave => {
    WHITE_KEYS.forEach((noteName, index) => {
      const noteFull = `${noteName}${octave}`
      const isHighlighted = isNoteHighlighted(noteName, octave)
      const isPressed = isNotePressed(noteName, octave)

      // 흰 건반
      let fillColor = '#FFFFFF'
      if (isPressed) {
        fillColor = '#FF6B6B'
      } else if (isHighlighted) {
        fillColor = '#FFD700'
      }

      whiteKeys.push(
        <g key={`white-${noteFull}`}>
          <rect
            x={xPos}
            y={0}
            width={whiteKeyWidth}
            height={whiteKeyHeight}
            fill={fillColor}
            stroke="#000000"
            strokeWidth="2"
            className={`piano-key white-key ${interactive ? 'interactive' : ''}`}
            data-note={noteFull}
            onClick={() => interactive && playNote(noteFull)}
            style={{ cursor: interactive ? 'pointer' : 'default' }}
          />
          <text
            x={xPos + whiteKeyWidth / 2}
            y={whiteKeyHeight + 20}
            textAnchor="middle"
            fontSize="12"
            fill="#333"
          >
            {noteName}
          </text>
        </g>
      )

      // 검은 건반 (E와 B는 없음)
      if (noteName !== 'E' && noteName !== 'B') {
        const blackNote = `${noteName}#${octave}`
        const isBlackHighlighted = isNoteHighlighted(`${noteName}#`, octave) || 
                                   chordNotes.some(n => n.includes(`${noteName}#`))
        const isBlackPressed = pressedKeys.has(blackNote)

        let blackFill = '#000000'
        if (isBlackPressed) {
          blackFill = '#FF6B6B'
        } else if (isBlackHighlighted) {
          blackFill = '#FFD700'
        }

        blackKeys.push(
          <rect
            key={`black-${blackNote}`}
            x={xPos + whiteKeyWidth - blackKeyWidth / 2}
            y={0}
            width={blackKeyWidth}
            height={blackKeyHeight}
            fill={blackFill}
            stroke="#000"
            strokeWidth="1"
            className={`piano-key black-key ${interactive ? 'interactive' : ''}`}
            data-note={blackNote}
            onClick={() => interactive && playNote(blackNote)}
            style={{ cursor: interactive ? 'pointer' : 'default' }}
          />
        )
      }

      xPos += whiteKeyWidth
    })
  })

  return (
    <div className="piano-keyboard-container">
      {chordName && (
        <div className="piano-header">
          <h3>🎹 {chordName} 코드</h3>
          {chordNotes.length > 0 && (
            <p className="chord-notes">구성음: {chordNotes.join(', ')}</p>
          )}
        </div>
      )}
      
      <div className="piano-wrapper">
        <svg 
          width="100%" 
          height="200" 
          viewBox={`0 0 ${xPos} 200`}
          xmlns="http://www.w3.org/2000/svg"
          className="piano-svg"
        >
          {whiteKeys}
          {blackKeys}
        </svg>
      </div>

      {interactive && (
        <p className="piano-hint">💡 건반을 클릭하여 소리를 들어보세요!</p>
      )}
    </div>
  )
}

export default PianoKeyboard

