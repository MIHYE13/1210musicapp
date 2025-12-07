import { useState, useRef } from 'react'
import './ChordAnalysis.css'
import { chordApi } from '../utils/api'

const ChordAnalysis = () => {
  const [activeTab, setActiveTab] = useState<'midi' | 'youtube' | 'pdf'>('midi')
  const [file, setFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (activeTab === 'midi') {
        const validExtensions = ['.mid', '.midi']
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
        if (!validExtensions.includes(fileExtension)) {
          setError('MIDI 파일만 업로드 가능합니다.')
          return
        }
      } else if (activeTab === 'pdf') {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
          setError('PDF 파일만 업로드 가능합니다.')
          return
        }
      }
      setFile(file)
      setError(null)
      setAnalysisResult(null)
    }
  }

  const handleAnalyze = async () => {
    if (activeTab === 'youtube') {
      if (!youtubeUrl.trim()) {
        setError('YouTube URL을 입력해주세요.')
        return
      }
      // YouTube URL 검증
      const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/
      if (!youtubeRegex.test(youtubeUrl)) {
        setError('유효한 YouTube URL을 입력해주세요.')
        return
      }
    } else {
      if (!file) {
        setError('파일을 선택해주세요.')
        return
      }
    }

    setIsProcessing(true)
    setError(null)
    setAnalysisResult(null)

    try {
      if (activeTab === 'youtube') {
        // YouTube 처리 (시뮬레이션)
        await new Promise((resolve) => setTimeout(resolve, 2000))
        setAnalysisResult({
          message: 'YouTube 음원 분석이 완료되었습니다. (시뮬레이션 모드)',
          note: '실제 기능을 사용하려면 백엔드 API가 필요합니다.',
        })
      } else {
        const apiResponse = await chordApi.analyze(file!, activeTab)
        
        if (apiResponse.success && apiResponse.data) {
          setAnalysisResult(apiResponse.data)
        } else {
          // 시뮬레이션 모드
          await new Promise((resolve) => setTimeout(resolve, 2000))
          setAnalysisResult({
            message: `${activeTab.toUpperCase()} 파일 분석이 완료되었습니다. (시뮬레이션 모드)`,
            chords: ['C', 'F', 'G', 'Am'],
            note: '실제 기능을 사용하려면 백엔드 API가 필요합니다.',
          })
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReset = () => {
    setFile(null)
    setYoutubeUrl('')
    setAnalysisResult(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="chord-analysis">
      <h2>🎹 화음 분석 & 피아노 연주</h2>

      <div className="highlight-box">
        <h3>🎯 차별화 기능!</h3>
        <ul>
          <li>MIDI/YouTube/PDF → 화음 자동 분석</li>
          <li>모두 다장조로 변환</li>
          <li>피아노 건반에 화음 표시</li>
          <li>클릭하여 소리 재생</li>
        </ul>
      </div>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'midi' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('midi')
            handleReset()
          }}
        >
          🎵 MIDI 반주 분석
        </button>
        <button
          className={`tab ${activeTab === 'youtube' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('youtube')
            handleReset()
          }}
        >
          📺 YouTube 음원
        </button>
        <button
          className={`tab ${activeTab === 'pdf' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('pdf')
            handleReset()
          }}
        >
          📄 PDF 악보
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'midi' && (
          <div className="section">
            <h3>🎵 MIDI 반주 음원 분석</h3>
            <div className="info-box">
              <p><strong>기능:</strong></p>
              <ol>
                <li>MIDI 파일의 화음을 자동 분석</li>
                <li>다장조(C major)로 자동 변환</li>
                <li>화음 코드를 피아노 건반에 표시</li>
                <li>마디별 화음 진행 확인</li>
                <li>건반을 클릭하여 연주 가능</li>
              </ol>
            </div>

            <div className="upload-area">
              <input
                ref={fileInputRef}
                type="file"
                id="midi-upload"
                accept=".mid,.midi"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="midi-upload" className="upload-button">
                📁 MIDI 파일 업로드
              </label>
              {file && (
                <div className="file-info">
                  <p className="file-name">
                    <strong>선택된 파일:</strong> {file.name}
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

            {file && (
              <button
                className="action-button"
                onClick={handleAnalyze}
                disabled={isProcessing}
              >
                {isProcessing ? (
                  <>
                    <span className="spinner"></span>
                    분석 중...
                  </>
                ) : (
                  '🔍 화음 분석하기'
                )}
              </button>
            )}

            {analysisResult && (
              <div className="results-section">
                <h3>📊 화음 진행 요약</h3>
                <div className="success-message">
                  <p>{analysisResult.message}</p>
                  {analysisResult.note && (
                    <p className="note">ℹ️ {analysisResult.note}</p>
                  )}
                  {analysisResult.chords && (
                    <div className="chords-display">
                      <p><strong>분석된 화음:</strong></p>
                      <div className="chords-list">
                        {analysisResult.chords.map((chord: string, i: number) => (
                          <span key={i} className="chord-badge">{chord}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
                <div className="piano-placeholder">
                  <p>🎹 피아노 건반 표시 영역</p>
                  <p className="note">실제 구현 시 피아노 건반이 여기에 표시됩니다.</p>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'youtube' && (
          <div className="section">
            <h3>📺 YouTube 음원 화음 분석</h3>
            <div className="info-box">
              <p><strong>기능:</strong></p>
              <ol>
                <li>YouTube 링크에서 오디오 추출</li>
                <li>AI로 멜로디 추출 (basic-pitch)</li>
                <li>다장조로 변환</li>
                <li>화음 자동 분석</li>
                <li>피아노 건반에 표시</li>
              </ol>
            </div>

            <div className="form-group">
              <label>YouTube URL</label>
              <input
                type="text"
                className="form-control"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                placeholder="https://www.youtube.com/watch?v=..."
              />
            </div>

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
              </div>
            )}

            <button
              className="action-button"
              onClick={handleAnalyze}
              disabled={isProcessing || !youtubeUrl.trim()}
            >
              {isProcessing ? (
                <>
                  <span className="spinner"></span>
                  오디오 다운로드 및 분석 중... (최대 2분)
                </>
              ) : (
                '🎵 오디오 다운로드 및 분석 시작'
              )}
            </button>

            {analysisResult && (
              <div className="results-section">
                <div className="success-message">
                  <p>{analysisResult.message}</p>
                  {analysisResult.note && (
                    <p className="note">ℹ️ {analysisResult.note}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'pdf' && (
          <div className="section">
            <h3>📄 PDF 악보 화음 분석</h3>
            <div className="info-box">
              <p><strong>기능:</strong></p>
              <ol>
                <li>PDF 악보를 MusicXML로 변환</li>
                <li>다장조로 변환</li>
                <li>화음 자동 분석</li>
                <li>피아노 건반에 표시</li>
              </ol>
            </div>

            <div className="upload-area">
              <input
                ref={fileInputRef}
                type="file"
                id="pdf-upload"
                accept=".pdf"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="pdf-upload" className="upload-button">
                📁 PDF 파일 업로드
              </label>
              {file && (
                <div className="file-info">
                  <p className="file-name">
                    <strong>선택된 파일:</strong> {file.name}
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

            {file && (
              <button
                className="action-button"
                onClick={handleAnalyze}
                disabled={isProcessing}
              >
                {isProcessing ? (
                  <>
                    <span className="spinner"></span>
                    분석 중...
                  </>
                ) : (
                  '🔍 화음 분석하기'
                )}
              </button>
            )}

            <div className="info-box">
              <p><strong>참고:</strong> PDF는 MuseScore 등으로 MusicXML로 변환 후 사용하세요.</p>
            </div>

            {analysisResult && (
              <div className="results-section">
                <div className="success-message">
                  <p>{analysisResult.message}</p>
                  {analysisResult.note && (
                    <p className="note">ℹ️ {analysisResult.note}</p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ChordAnalysis
