import { useState } from 'react'
import { HiPlay, HiExternalLink, HiMusicNote } from 'react-icons/hi'
import './PerplexityYouTube.css'
import { perplexityApi, youtubeApi, chordApi } from '../utils/api'

interface YouTubeVideo {
  videoId: string
  title: string
  channel: string
  thumbnail?: string
  url: string
  description?: string
  viewCount?: number
  publishedAt?: string
  hasScore?: boolean
  hasAudio?: boolean
  contentScore?: number
}

const PerplexityYouTube = () => {
  const [activeTab, setActiveTab] = useState<'perplexity' | 'youtube'>('perplexity')
  const [searchType, setSearchType] = useState('음악 이론 조사')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // YouTube specific
  const [videoSearchType, setVideoSearchType] = useState('일반 검색')
  const [maxResults, setMaxResults] = useState(5)
  const [youtubeVideos, setYoutubeVideos] = useState<YouTubeVideo[]>([])
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null)
  
  // 오디오 분석 관련
  const [analyzingVideoId, setAnalyzingVideoId] = useState<string | null>(null)
  const [analysisResult, setAnalysisResult] = useState<any>(null)

  const extractVideoId = (url: string): string | null => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
      /^([a-zA-Z0-9_-]{11})$/,
    ]
    for (const pattern of patterns) {
      const match = url.match(pattern)
      if (match) return match[1]
    }
    return null
  }

  const handlePerplexitySearch = async () => {
    if (!query.trim()) {
      setError('검색어를 입력해주세요.')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults('')

    try {
      const apiResponse = await perplexityApi.search(query, searchType)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        if (data.result) {
          setResults(data.result)
        } else if (data.error) {
          setError(data.error)
          setResults('')
        } else {
          setResults(JSON.stringify(data))
        }
      } else {
        const errorMsg = apiResponse.error || 'API 호출에 실패했습니다.'
        setError(errorMsg)
        setResults('')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleYouTubeSearch = async () => {
    if (!query.trim()) {
      setError('검색어를 입력해주세요.')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults('')
    setYoutubeVideos([])
    setSelectedVideo(null)
    setAnalysisResult(null)

    try {
      const apiResponse = await youtubeApi.search(query, maxResults)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        const videos = data.videos || data
        
        if (Array.isArray(videos) && videos.length > 0) {
          // 비디오 데이터를 구조화
          const formattedVideos: YouTubeVideo[] = videos.map((v: any) => {
            const videoId = v.video_id || v.id?.videoId || v.id || extractVideoId(v.url || '') || ''
            const url = v.url || `https://www.youtube.com/watch?v=${videoId}`
            const thumbnail = v.thumbnail || (videoId ? `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg` : undefined)
            const viewCount = v.view_count || v.viewCount || v.statistics?.viewCount || 0
            
            return {
              videoId,
              title: v.title || v.snippet?.title || '제목 없음',
              channel: v.channel || v.snippet?.channelTitle || '채널 없음',
              thumbnail,
              url,
              description: v.description || v.snippet?.description || '',
              viewCount: typeof viewCount === 'string' ? parseInt(viewCount) : viewCount,
              publishedAt: v.published_at || v.publishedAt || v.snippet?.publishedAt,
              hasScore: v.has_score || false,
              hasAudio: v.has_audio || false,
              contentScore: v.content_score || 0
            }
          }).filter((video) => {
            // 10만 뷰 이상인 영상만 표시 (뷰 카운트가 없는 경우도 포함)
            return !video.viewCount || video.viewCount >= 100000
          })
          
          setYoutubeVideos(formattedVideos)
          
          // 텍스트 결과도 유지 (호환성)
          setResults(
            formattedVideos.map((v, i) => 
              `${i + 1}. ${v.title}\n   채널: ${v.channel}\n   링크: ${v.url}\n`
            ).join('\n')
          )
        } else if (data.error) {
          setError(data.error)
          setResults('')
        } else {
          setResults('검색 결과가 없습니다.')
        }
      } else {
        const errorMsg = apiResponse.error || 'API 호출에 실패했습니다.'
        setError(errorMsg)
        setResults('')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleVideoClick = (videoId: string) => {
    setSelectedVideo(selectedVideo === videoId ? null : videoId)
  }

  const handleAnalyzeAudio = async (video: YouTubeVideo) => {
    if (!video.url) {
      setError('영상 URL을 찾을 수 없습니다.')
      return
    }

    setAnalyzingVideoId(video.videoId)
    setError(null)
    setAnalysisResult(null)

    try {
      const apiResponse = await chordApi.analyzeYouTube(video.url)
      
      if (apiResponse.success && apiResponse.data) {
        setAnalysisResult({
          video: video,
          ...apiResponse.data
        })
      } else {
        const errorMsg = apiResponse.error || '오디오 분석에 실패했습니다.'
        setError(errorMsg)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '오디오 분석 중 오류가 발생했습니다.')
    } finally {
      setAnalyzingVideoId(null)
    }
  }

  return (
    <div className="perplexity-youtube">
      <h2>최신 정보 & 영상 자료</h2>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'perplexity' ? 'active' : ''}`}
          onClick={() => setActiveTab('perplexity')}
        >
          🌐 웹 조사 (Perplexity)
        </button>
        <button
          className={`tab ${activeTab === 'youtube' ? 'active' : ''}`}
          onClick={() => setActiveTab('youtube')}
        >
          📺 유튜브 검색어로 찾기
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'perplexity' && (
          <div className="section">
            <h3>🌐 최신 음악 교육 정보 조사 (Perplexity)</h3>

            <div className="form-group">
              <label>조사 유형</label>
              <select
                className="form-control"
                value={searchType}
                onChange={(e) => setSearchType(e.target.value)}
              >
                <option>음악 이론 조사</option>
                <option>곡 배경 정보</option>
                <option>교육 자료 찾기</option>
                <option>최신 트렌드</option>
                <option>교수법 비교</option>
              </select>
            </div>

            <div className="form-group">
              <label>검색어</label>
              <input
                type="text"
                className="form-control"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="예: 3화음의 구성과 활용"
                onKeyPress={(e) => e.key === 'Enter' && handlePerplexitySearch()}
              />
            </div>

            <button
              className="action-button"
              onClick={handlePerplexitySearch}
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  최신 정보를 조사하는 중...
                </>
              ) : (
                '🔍 조사하기'
              )}
            </button>

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
              </div>
            )}

            {results && (
              <div className="response-box">
                <h4>📚 조사 결과</h4>
                <div className="response-content">{results}</div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'youtube' && (
          <div className="section">
            <h3>📺 유튜브 검색어로 찾기</h3>

            <div className="workflow-steps">
              <div className="step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>검색어로 영상 찾기</h4>
                  <p>YouTube에서 음악 교육 영상을 검색합니다</p>
                  <p className="step-note">✓ 10만 뷰 이상 신뢰성 있는 영상만 추천</p>
                </div>
              </div>
              <div className="step-arrow">→</div>
              <div className="step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>링크 추출</h4>
                  <p>검색 결과에서 영상 링크를 자동으로 추출합니다</p>
                </div>
              </div>
              <div className="step-arrow">→</div>
              <div className="step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>오디오 분석</h4>
                  <p>추출한 링크로 오디오를 다운로드하고 분석합니다</p>
                </div>
              </div>
            </div>

            <div className="form-group">
              <label>영상 유형</label>
              <select
                className="form-control"
                value={videoSearchType}
                onChange={(e) => setVideoSearchType(e.target.value)}
              >
                <option>일반 검색</option>
                <option>악기 튜토리얼</option>
                <option>음악 이론 영상</option>
                <option>연습용 반주</option>
                <option>추천 채널</option>
              </select>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>검색어</label>
                <input
                  type="text"
                  className="form-control"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="예: 계이름 배우기"
                  onKeyPress={(e) => e.key === 'Enter' && handleYouTubeSearch()}
                />
              </div>
              <div className="form-group">
                <label>결과 개수: {maxResults}개</label>
                <input
                  type="range"
                  min={3}
                  max={10}
                  value={maxResults}
                  onChange={(e) => setMaxResults(Number(e.target.value))}
                  className="form-control"
                />
              </div>
            </div>

            <button
              className="action-button"
              onClick={handleYouTubeSearch}
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  교육 영상을 검색하는 중...
                </>
              ) : (
                '🔍 영상 검색'
              )}
            </button>

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
              </div>
            )}

            {youtubeVideos.length > 0 && (
              <div className="youtube-results">
                <div className="results-header">
                  <h4>📺 검색 결과 ({youtubeVideos.length}개)</h4>
                  <div className="reliability-badge">
                    <span className="badge-icon">✓</span>
                    <span>10만 뷰 이상 신뢰성 있는 영상만 추천</span>
                  </div>
                </div>
                <div className="video-grid">
                  {youtubeVideos.map((video, index) => (
                    <div key={video.videoId || index} className="video-card">
                      {/* YouTube 링크 표시 */}
                      <div className="video-url-display">
                        <label>YouTube 링크:</label>
                        <div className="url-input-group">
                          <input
                            type="text"
                            className="url-input"
                            value={video.url}
                            readOnly
                            onClick={(e) => e.currentTarget.select()}
                          />
                          <button
                            className="copy-url-button"
                            onClick={(e) => {
                              e.stopPropagation()
                              navigator.clipboard.writeText(video.url)
                              const button = e.currentTarget
                              const originalText = button.textContent
                              button.textContent = '복사됨!'
                              setTimeout(() => {
                                button.textContent = originalText
                              }, 2000)
                            }}
                            title="링크 복사"
                          >
                            복사
                          </button>
                        </div>
                      </div>

                      {/* 미리보기 영상 (기본 표시) */}
                      {video.videoId && (
                        <div className="video-embed">
                          <iframe
                            src={`https://www.youtube.com/embed/${video.videoId}`}
                            title={video.title}
                            frameBorder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="youtube-iframe"
                          ></iframe>
                        </div>
                      )}
                      
                      <div className="video-info">
                        <h5 className="video-title" title={video.title}>
                          {video.title}
                        </h5>
                        {(video.hasScore || video.hasAudio) && (
                          <div className="content-badges">
                            {video.hasScore && (
                              <span className="content-badge score-badge">
                                📄 악보 포함
                              </span>
                            )}
                            {video.hasAudio && (
                              <span className="content-badge audio-badge">
                                🎵 음원 포함
                              </span>
                            )}
                          </div>
                        )}
                        <div className="video-meta">
                          <p className="video-channel">{video.channel}</p>
                          {video.viewCount && (
                            <p className="video-views">
                              👁️ {video.viewCount.toLocaleString()}회
                            </p>
                          )}
                          {video.publishedAt && (
                            <p className="video-date">
                              📅 {video.publishedAt}
                            </p>
                          )}
                        </div>
                        
                        <div className="video-actions">
                          <a
                            href={video.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="video-link"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <HiExternalLink />
                            YouTube에서 보기
                          </a>
                          <button
                            className="analyze-button"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAnalyzeAudio(video)
                            }}
                            disabled={analyzingVideoId === video.videoId}
                          >
                            {analyzingVideoId === video.videoId ? (
                              <>
                                <span className="spinner"></span>
                                분석 중...
                              </>
                            ) : (
                              <>
                                <HiMusicNote />
                                오디오 분석하기
                              </>
                            )}
                          </button>
                        </div>
                      </div>

                      {analysisResult && analysisResult.video?.videoId === video.videoId && (
                        <div className="analysis-result">
                          <h5>🎵 분석 결과</h5>
                          {analysisResult.message && (
                            <p className="analysis-message">{analysisResult.message}</p>
                          )}
                          {analysisResult.chords && (
                            <div className="chords-display">
                              <p><strong>화음:</strong> {analysisResult.chords.join(', ')}</p>
                            </div>
                          )}
                          {analysisResult.note && (
                            <p className="analysis-note">ℹ️ {analysisResult.note}</p>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {results && youtubeVideos.length === 0 && (
              <div className="response-box">
                <h4>📺 검색 결과</h4>
                <div className="response-content">{results}</div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default PerplexityYouTube
