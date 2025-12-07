import { useState, useRef } from 'react'
import './ChordAnalysis.css'
import { chordApi } from '../utils/api'
import PianoKeyboard from './PianoKeyboard'

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
        const validExtensions = ['.mid', '.midi', '.mp3', '.wav', '.mpeg']
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
        if (!validExtensions.includes(fileExtension)) {
          setError('MIDI 또는 오디오 파일(MP3, WAV)만 업로드 가능합니다.')
          return
        }
      } else if (activeTab === 'pdf') {
        const validExtensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp']
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
        if (!validExtensions.includes(fileExtension)) {
          setError('PDF 또는 이미지 파일(JPG, PNG 등)만 업로드 가능합니다.')
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
        // YouTube URL을 백엔드로 전송
        const apiResponse = await chordApi.analyzeYouTube(youtubeUrl)
        
        if (apiResponse.success && apiResponse.data) {
          setAnalysisResult(apiResponse.data)
        } else {
          setError(apiResponse.error || 'YouTube 음원 분석에 실패했습니다.')
        }
      } else {
        // 파일 타입 결정
        const fileExtension = '.' + file!.name.split('.').pop()?.toLowerCase()
        let fileType: 'midi' | 'youtube' | 'pdf' | 'audio' | 'image' = activeTab
        
        if (activeTab === 'midi' && ['.mp3', '.wav', '.mpeg'].includes(fileExtension)) {
          fileType = 'audio'
        } else if (activeTab === 'pdf') {
          // 이미지 파일은 'image' 타입으로, PDF는 'pdf' 타입으로
          if (['.jpg', '.jpeg', '.png', '.gif', '.bmp'].includes(fileExtension)) {
            fileType = 'image'
          } else {
            fileType = 'pdf'
          }
        }
        
        const apiResponse = await chordApi.analyze(file!, fileType)
        
        if (apiResponse.success && apiResponse.data) {
          setAnalysisResult(apiResponse.data)
        } else {
          setError(apiResponse.error || '화음 분석에 실패했습니다.')
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
            <h3>MIDI 반주 음원 분석</h3>
            <div className="info-box">
              <p><strong>기능:</strong></p>
              <ol>
                <li>MIDI 또는 오디오 파일(MP3, WAV)의 화음을 자동 분석</li>
                <li>오디오 파일은 자동으로 MIDI로 변환 후 분석</li>
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
                accept=".mid,.midi,.mp3,.wav,.mpeg"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="midi-upload" className="upload-button">
                📁 MIDI/오디오 파일 업로드 (MIDI, MP3, WAV)
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

                {/* 화음 정보가 있을 때 피아노 건반 표시 */}
                {analysisResult.chordsInfo && analysisResult.chordsInfo.length > 0 && (
                  <div className="piano-section">
                    <h3>🎹 마디별 화음 반주 (처음 8마디)</h3>
                    {analysisResult.chordsInfo.map((chordInfo: any, index: number) => (
                      <PianoKeyboard
                        key={index}
                        chordNotes={chordInfo.notes || []}
                        chordName={`마디 ${chordInfo.measure || index + 1}: ${chordInfo.chord_name || ''}`}
                        interactive={true}
                        octaves={[4, 5]}
                      />
                    ))}
                  </div>
                )}

                {/* 단순 화음 리스트만 있을 때 첫 번째 화음 표시 */}
                {analysisResult.chords && analysisResult.chords.length > 0 && !analysisResult.chordsInfo && (
                  <div className="piano-section">
                    <h3>🎹 화음 반주</h3>
                    <PianoKeyboard
                      chordNotes={[]}
                      chordName={analysisResult.chords[0] || '화음'}
                      interactive={true}
                      octaves={[4, 5]}
                    />
                    <p className="note">💡 전체 화음 정보를 보려면 MIDI 파일을 업로드하세요.</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'youtube' && (
          <div className="section">
            <h3>YouTube 음원 화음 분석</h3>
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
            <h3>PDF/이미지 악보 화음 분석</h3>
            <div className="info-box">
              <p><strong>기능:</strong></p>
              <ol>
                <li>PDF 또는 이미지 파일(JPG, PNG)의 악보를 스캔하여 분석</li>
                <li>OMR(Optical Music Recognition) 기술로 악보 인식</li>
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
                accept=".pdf,.jpg,.jpeg,.png,.gif,.bmp,image/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <label htmlFor="pdf-upload" className="upload-button">
                📁 PDF/이미지 파일 업로드 (PDF, JPG, PNG)
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
              <p><strong>참고:</strong></p>
              <ul>
                <li>PDF와 이미지 파일은 OMR(Optical Music Recognition) 기술로 악보를 인식합니다.</li>
                <li>인식 품질을 높이려면 깨끗한 스캔 이미지(300 DPI 이상)를 사용하세요.</li>
                <li>인식이 어려운 경우 MuseScore 등으로 MusicXML로 변환 후 '악보 처리' 메뉴에서 사용하세요.</li>
              </ul>
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
