import { useState, useRef } from 'react'
import './ScoreProcessing.css'
import { scoreApi } from '../utils/api'

const ScoreProcessing = () => {
  const [scoreFile, setScoreFile] = useState<File | null>(null)
  const [options, setOptions] = useState({
    addSolfege: true,
    simplifyRhythm: true,
    transposeC: true,
    addChords: true,
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [processed, setProcessed] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [processedScore, setProcessedScore] = useState<any>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // 파일 타입 검증
      const validExtensions = ['.mid', '.midi', '.xml', '.mxl', '.abc', '.musicxml']
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
      
      if (!validExtensions.includes(fileExtension)) {
        setError('지원하지 않는 파일 형식입니다. MIDI, MusicXML, 또는 ABC 파일을 업로드해주세요.')
        return
      }

      setScoreFile(file)
      setError(null)
      setProcessed(false)
    }
  }

  const handleProcess = async () => {
    if (!scoreFile) return

    setIsProcessing(true)
    setError(null)
    setProcessed(false)

    try {
      // 백엔드 API 호출
      const response = await scoreApi.processScore(scoreFile, options)
      
      if (response.success && response.data) {
        setProcessedScore(response.data)
        setProcessed(true)
      } else {
        // API 오류 처리
        const errorMsg = response.error || '악보 처리에 실패했습니다.'
        setError(errorMsg)
        setProcessed(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handlePlay = () => {
    setIsPlaying(true)
    // 실제 재생 로직은 백엔드 API 필요
    setTimeout(() => {
      setIsPlaying(false)
    }, 3000)
  }

  const handlePause = () => {
    setIsPlaying(false)
  }

  const handleStop = () => {
    setIsPlaying(false)
  }

  const handleDownload = async (format: 'mp3' | 'midi' | 'musicxml') => {
    if (!processedScore?.scoreId) {
      alert('처리된 악보가 없습니다.')
      return
    }

    try {
      let response
      let filename = 'processed_score'
      let mimeType = 'application/octet-stream'
      
      if (format === 'mp3') {
        response = await scoreApi.exportMp3(processedScore.scoreId)
        filename = 'processed_score.mp3'
        mimeType = 'audio/mpeg'
      } else if (format === 'midi') {
        response = await scoreApi.exportMidi(processedScore.scoreId)
        filename = 'processed_score.mid'
        mimeType = 'audio/midi'
      } else {
        response = await scoreApi.exportMusicXML(processedScore.scoreId)
        filename = 'processed_score.xml'
        mimeType = 'application/xml'
      }
      
      if (response.success && response.data) {
        const data = response.data as any
        
        // Blob 처리
        let blob: Blob
        if (data instanceof Blob) {
          blob = data
          // Blob의 실제 타입 확인
          if (data.type) {
            mimeType = data.type
          }
        } else if (typeof data === 'string') {
          // Base64 문자열인 경우
          const binaryString = atob(data)
          const bytes = new Uint8Array(binaryString.length)
          for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i)
          }
          blob = new Blob([bytes], { type: mimeType })
        } else {
          // ArrayBuffer나 다른 형식
          blob = new Blob([data], { type: mimeType })
        }
        
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        URL.revokeObjectURL(url)
      } else {
        alert(`파일 다운로드에 실패했습니다: ${response.error || '알 수 없는 오류'}`)
      }
    } catch (err) {
      alert('다운로드 중 오류가 발생했습니다: ' + (err instanceof Error ? err.message : '알 수 없는 오류'))
    }
  }

  const handleReset = () => {
    setScoreFile(null)
    setProcessed(false)
    setProcessedScore(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="score-processing">
      <h2>🎼 악보 → 계이름·반주 추가</h2>

      <div className="section">
        <div className="upload-area">
          <input
            ref={fileInputRef}
            type="file"
            id="score-upload"
            accept=".mid,.midi,.xml,.mxl,.abc,.musicxml"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <label htmlFor="score-upload" className="upload-button">
            📁 악보 파일 업로드 (MIDI, MusicXML, ABC)
          </label>
          {scoreFile && (
            <div className="file-info">
              <p className="file-name">
                <strong>선택된 파일:</strong> {scoreFile.name}
              </p>
              <button className="reset-button" onClick={handleReset}>
                ✕ 파일 제거
              </button>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            <p>❌ {error}</p>
          </div>
        )}

        {scoreFile && (
          <>
            <div className="options-section">
              <h3>⚙️ 처리 옵션</h3>
              <div className="options-grid">
                <label className="option-item">
                  <input
                    type="checkbox"
                    checked={options.addSolfege}
                    onChange={(e) =>
                      setOptions({ ...options, addSolfege: e.target.checked })
                    }
                  />
                  <span>계이름 추가 (도레미)</span>
                </label>
                <label className="option-item">
                  <input
                    type="checkbox"
                    checked={options.simplifyRhythm}
                    onChange={(e) =>
                      setOptions({ ...options, simplifyRhythm: e.target.checked })
                    }
                  />
                  <span>리듬 단순화</span>
                </label>
                <label className="option-item">
                  <input
                    type="checkbox"
                    checked={options.transposeC}
                    onChange={(e) =>
                      setOptions({ ...options, transposeC: e.target.checked })
                    }
                  />
                  <span>다장조 변환</span>
                </label>
                <label className="option-item">
                  <input
                    type="checkbox"
                    checked={options.addChords}
                    onChange={(e) =>
                      setOptions({ ...options, addChords: e.target.checked })
                    }
                  />
                  <span>반주 추가</span>
                </label>
              </div>
            </div>

            <button
              className="action-button"
              onClick={handleProcess}
              disabled={isProcessing}
            >
              {isProcessing ? (
                <>
                  <span className="spinner"></span>
                  처리 중...
                </>
              ) : (
                '🎵 처리하기'
              )}
            </button>
          </>
        )}

        {processed && processedScore && (
          <div className="success-message">
            <h3>✅ 처리가 완료되었습니다!</h3>
            <p>{processedScore.message || '악보 처리가 완료되었습니다.'}</p>
            <div className="score-preview">
              <div className="score-placeholder">
                <p>📄 완성된 악보</p>
                <p className="note">
                  {processedScore.scoreId ? `악보 ID: ${processedScore.scoreId}` : '실제 구현 시 music21을 사용하여 악보 렌더링'}
                </p>
                {processedScore.options && (
                  <div className="applied-options">
                    <p><strong>적용된 옵션:</strong></p>
                    <ul>
                      {processedScore.options.addSolfege && <li>✓ 계이름 추가</li>}
                      {processedScore.options.simplifyRhythm && <li>✓ 리듬 단순화</li>}
                      {processedScore.options.transposeC && <li>✓ 다장조 변환</li>}
                      {processedScore.options.addChords && <li>✓ 반주 추가</li>}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            <div className="playback-controls">
              <h3>🎹 재생</h3>
              <div className="controls">
                <button
                  className={`control-button ${isPlaying ? 'playing' : ''}`}
                  onClick={handlePlay}
                  disabled={isPlaying}
                >
                  ▶️ 재생
                </button>
                <button
                  className="control-button"
                  onClick={handlePause}
                  disabled={!isPlaying}
                >
                  ⏸️ 일시정지
                </button>
                <button
                  className="control-button"
                  onClick={handleStop}
                  disabled={!isPlaying}
                >
                  ⏹️ 정지
                </button>
              </div>
              {isPlaying && (
                <p className="playing-status">재생 중...</p>
              )}
            </div>

            <div className="download-section">
              <h3>💾 다운로드</h3>
              <div className="download-buttons">
                <button
                  className="download-button"
                  onClick={() => handleDownload('mp3')}
                >
                  🎵 MP3 다운로드
                </button>
                <button
                  className="download-button"
                  onClick={() => handleDownload('midi')}
                >
                  🎼 MIDI 다운로드
                </button>
                <button
                  className="download-button"
                  onClick={() => handleDownload('musicxml')}
                >
                  📄 MusicXML 다운로드
                </button>
              </div>
            </div>

            <button className="secondary-button" onClick={handleReset}>
              🔄 새 파일 업로드
            </button>
          </div>
        )}
      </div>

      <div className="info-box">
        <h3>📚 사용 방법</h3>
        <ol>
          <li>MIDI, MusicXML 또는 ABC 파일을 업로드하세요</li>
          <li>원하는 옵션을 선택하세요</li>
          <li>"처리하기" 버튼을 클릭하세요</li>
          <li>완성된 악보를 재생하고 다운로드하세요!</li>
        </ol>
      </div>
    </div>
  )
}

export default ScoreProcessing
