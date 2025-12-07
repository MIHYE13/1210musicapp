import { useState, useRef } from 'react'
import './AudioToScore.css'
import { audioApi } from '../utils/api'

const AudioToScore = () => {
  const [audioFile, setAudioFile] = useState<File | null>(null)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [scoreGenerated, setScoreGenerated] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [scoreData, setScoreData] = useState<any>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // 파일 타입 검증
      const validTypes = ['audio/mp3', 'audio/wav', 'audio/mpeg', 'audio/x-wav']
      const validExtensions = ['.mp3', '.wav', '.mpeg']
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
      
      if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
        setError('지원하지 않는 파일 형식입니다. MP3 또는 WAV 파일을 업로드해주세요.')
        return
      }

      // 파일 크기 검증 (10MB 제한)
      const maxSize = 10 * 1024 * 1024 // 10MB
      if (file.size > maxSize) {
        setError('파일 크기가 너무 큽니다. 10MB 이하의 파일을 업로드해주세요.')
        return
      }

      setAudioFile(file)
      setError(null)
      const url = URL.createObjectURL(file)
      setAudioUrl(url)
      setScoreGenerated(false)
    }
  }

  const handleGenerateScore = async () => {
    if (!audioFile) return

    setIsProcessing(true)
    setError(null)
    setScoreGenerated(false)

    try {
      // 백엔드 API 호출 시도
      const response = await audioApi.processAudio(audioFile)
      
      if (response.success && response.data) {
        setScoreData(response.data)
        setScoreGenerated(true)
      } else {
        // 백엔드가 없을 경우 시뮬레이션
        // 실제 환경에서는 백엔드 API를 사용해야 합니다
        await new Promise((resolve) => setTimeout(resolve, 2000))
        
        // 시뮬레이션 데이터
        setScoreData({
          scoreId: `score_${Date.now()}`,
          message: '악보 생성이 완료되었습니다. (시뮬레이션 모드)',
          note: '실제 기능을 사용하려면 백엔드 API를 설정해주세요.',
        })
        setScoreGenerated(true)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReset = () => {
    setAudioFile(null)
    setAudioUrl(null)
    setScoreGenerated(false)
    setScoreData(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="audio-to-score">
      <h2>🎤 오디오 → 악보 변환</h2>
      
      <div className="section">
        <div className="upload-area">
          <input
            ref={fileInputRef}
            type="file"
            id="audio-upload"
            accept="audio/mp3,audio/wav,audio/mpeg,.mp3,.wav"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <label htmlFor="audio-upload" className="upload-button">
            📁 오디오 파일 업로드 (MP3, WAV)
          </label>
          {audioFile && (
            <div className="file-info">
              <p className="file-name">
                <strong>선택된 파일:</strong> {audioFile.name}
              </p>
              <p className="file-size">
                크기: {(audioFile.size / 1024 / 1024).toFixed(2)} MB
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

        {audioUrl && (
          <div className="audio-preview">
            <h3>오디오 미리보기</h3>
            <audio controls src={audioUrl} style={{ width: '100%' }} />
          </div>
        )}

        {audioFile && !scoreGenerated && (
          <button
            className="action-button"
            onClick={handleGenerateScore}
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <span className="spinner"></span>
                처리 중... (최대 2분 소요)
              </>
            ) : (
              '🎼 악보 생성하기'
            )}
          </button>
        )}

        {scoreGenerated && scoreData && (
          <div className="success-message">
            <h3>✅ 악보가 생성되었습니다!</h3>
            <p>{scoreData.message || '악보 생성이 완료되었습니다.'}</p>
            {scoreData.note && (
              <p className="note">ℹ️ {scoreData.note}</p>
            )}
            <div className="score-preview">
              <div className="score-placeholder">
                <p>📄 악보 이미지</p>
                <p className="note">
                  {scoreData.scoreId ? `악보 ID: ${scoreData.scoreId}` : '실제 구현 시 music21을 사용하여 악보 렌더링'}
                </p>
              </div>
            </div>
            <div className="action-buttons">
              <button
                className="secondary-button"
                onClick={() => {
                  window.location.hash = 'score-processing'
                }}
              >
                ➡️ 악보 처리 페이지로 이동
              </button>
              <button className="secondary-button" onClick={handleReset}>
                🔄 새 파일 업로드
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="info-box">
        <h3>📚 사용 방법</h3>
        <ol>
          <li>MP3 또는 WAV 파일을 업로드하세요 (최대 10MB)</li>
          <li>"악보 생성하기" 버튼을 클릭하세요</li>
          <li>AI가 멜로디를 추출하여 악보를 만듭니다 (최대 2분 소요)</li>
          <li>"악보 처리" 메뉴에서 계속 진행하세요</li>
        </ol>
        <div className="warning-box">
          <p>⚠️ <strong>참고:</strong> 실제 오디오 처리를 위해서는 백엔드 API가 필요합니다.</p>
          <p>현재는 시뮬레이션 모드로 작동합니다.</p>
        </div>
      </div>
    </div>
  )
}

export default AudioToScore
