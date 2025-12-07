import { useState } from 'react'
import './PerplexityYouTube.css'
import { perplexityApi, youtubeApi } from '../utils/api'

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
        setResults(data.result || data)
      } else {
        // 시뮬레이션 모드
        await new Promise((resolve) => setTimeout(resolve, 2000))
        setResults(
          `"${query}"에 대한 ${searchType} 결과 (시뮬레이션 모드)\n\n` +
          `검색 결과가 여기에 표시됩니다. 실제 기능을 사용하려면 Perplexity API 키를 설정해주세요.\n\n` +
          `현재는 시뮬레이션 모드로 작동합니다.`
        )
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

    try {
      const apiResponse = await youtubeApi.search(query, maxResults)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        const videos = data.videos || data
        if (Array.isArray(videos)) {
          setResults(
            videos.map((v: any, i: number) => 
              `${i + 1}. ${v.title}\n   채널: ${v.channel}\n   링크: ${v.url}\n`
            ).join('\n')
          )
        } else {
          setResults(JSON.stringify(videos, null, 2))
        }
      } else {
        // 시뮬레이션 모드
        await new Promise((resolve) => setTimeout(resolve, 1500))
        setResults(
          `"${query}"에 대한 YouTube 검색 결과 (시뮬레이션 모드)\n\n` +
          `검색 결과가 여기에 표시됩니다. 실제 기능을 사용하려면 YouTube API 키를 설정해주세요.\n\n` +
          `현재는 시뮬레이션 모드로 작동합니다.`
        )
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="perplexity-youtube">
      <h2>🔍 최신 정보 & 영상 자료</h2>

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
          📺 교육 영상 (YouTube)
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'perplexity' && (
          <div className="section">
            <h3>🌐 최신 음악 교육 정보 조사 (Perplexity)</h3>
            <div className="info-box">
              <p>🔑 <strong>Perplexity API 활성화 방법:</strong></p>
              <ol>
                <li>Perplexity API 키 발급: https://www.perplexity.ai/settings/api</li>
                <li>환경 변수로 설정</li>
                <li>최신 음악 교육 연구, 곡 배경 정보, 교육 자료 등을 실시간으로 조사할 수 있습니다.</li>
              </ol>
            </div>

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
            <h3>📺 음악 교육 영상 찾기 (YouTube)</h3>
            <div className="info-box">
              <p>🔑 <strong>YouTube API 활성화 방법:</strong></p>
              <ol>
                <li>Google Cloud Console에서 프로젝트 생성</li>
                <li>YouTube Data API v3 활성화</li>
                <li>API 키 생성</li>
                <li>환경 변수로 설정</li>
              </ol>
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

            {results && (
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
