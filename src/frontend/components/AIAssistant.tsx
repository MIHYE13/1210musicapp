import { useState } from 'react'
import './AIAssistant.css'
import { aiApi } from '../utils/api'

const AIAssistant = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'theory' | 'lesson'>('chat')
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Theory tab
  const [theoryTopic, setTheoryTopic] = useState('계이름')
  const [studentAge, setStudentAge] = useState(10)
  const [customTopic, setCustomTopic] = useState('')
  
  // Lesson plan tab
  const [songTitle, setSongTitle] = useState('')
  const [gradeLevel, setGradeLevel] = useState('3-4학년')
  const [lessonDuration, setLessonDuration] = useState(40)
  const [lessonPlan, setLessonPlan] = useState('')
  const [contextOption, setContextOption] = useState('일반 질문')

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      setError('질문을 입력해주세요.')
      return
    }

    setIsLoading(true)
    setError(null)
    setResponse('')

    try {
      const context = contextOption === '현재 악보에 대해' ? '현재 악보 컨텍스트' : undefined
      const apiResponse = await aiApi.chat(question, context)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        setResponse(data.response || data)
      } else {
        // 시뮬레이션 모드
        await new Promise((resolve) => setTimeout(resolve, 1500))
        setResponse(
          `질문: "${question}"\n\n` +
          `AI 답변 (시뮬레이션 모드):\n` +
          `이 질문에 대한 답변입니다. 실제 기능을 사용하려면 OpenAI API 키를 설정하고 백엔드 API를 연결해주세요.\n\n` +
          `현재는 시뮬레이션 모드로 작동하며, 실제 AI 답변을 받으려면:\n` +
          `1. OpenAI API 키 발급\n` +
          `2. 백엔드 API 설정\n` +
          `3. 환경 변수 설정이 필요합니다.`
        )
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleExplainTheory = async () => {
    const topic = theoryTopic === '직접 입력' ? customTopic : theoryTopic
    if (!topic.trim()) {
      setError('주제를 입력해주세요.')
      return
    }

    setIsLoading(true)
    setError(null)
    setResponse('')

    try {
      const apiResponse = await aiApi.explainTheory(topic, studentAge)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        setResponse(data.explanation || data)
      } else {
        // 시뮬레이션 모드
        await new Promise((resolve) => setTimeout(resolve, 1500))
        setResponse(
          `"${topic}"에 대한 설명 (${studentAge}세용)\n\n` +
          `이 주제에 대한 초등학생 수준의 설명입니다. 실제 기능을 사용하려면 OpenAI API 키를 설정해주세요.\n\n` +
          `현재는 시뮬레이션 모드로 작동합니다.`
        )
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateLessonPlan = async () => {
    if (!songTitle.trim()) {
      setError('곡 제목을 입력해주세요.')
      return
    }

    setIsLoading(true)
    setError(null)
    setLessonPlan('')

    try {
      const apiResponse = await aiApi.generateLessonPlan(songTitle, gradeLevel, lessonDuration)
      
      if (apiResponse.success && apiResponse.data) {
        const data = apiResponse.data as any
        setLessonPlan(data.plan || data)
      } else {
        // 시뮬레이션 모드
        await new Promise((resolve) => setTimeout(resolve, 2000))
        setLessonPlan(
          `"${songTitle}" 수업 계획 (${gradeLevel}, ${lessonDuration}분)\n\n` +
          `1. 도입 (5분)\n` +
          `   - 곡 소개 및 학습 목표 제시\n\n` +
          `2. 전개 (30분)\n` +
          `   - 계이름 익히기\n` +
          `   - 리듬 연습\n` +
          `   - 악보 읽기\n\n` +
          `3. 정리 (5분)\n` +
          `   - 복습 및 평가\n\n` +
          `실제 기능을 사용하려면 OpenAI API 키를 설정해주세요.`
        )
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownloadLessonPlan = () => {
    if (!lessonPlan) return
    
    const blob = new Blob([lessonPlan], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `lesson_plan_${songTitle || '수업계획'}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleClearChat = () => {
    setQuestion('')
    setResponse('')
    setError(null)
  }

  return (
    <div className="ai-assistant">
      <h2>🤖 AI 음악 도우미</h2>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 질문하기
        </button>
        <button
          className={`tab ${activeTab === 'theory' ? 'active' : ''}`}
          onClick={() => setActiveTab('theory')}
        >
          📖 음악 이론
        </button>
        <button
          className={`tab ${activeTab === 'lesson' ? 'active' : ''}`}
          onClick={() => setActiveTab('lesson')}
        >
          📝 수업 계획
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'chat' && (
          <div className="section">
            <h3>💬 AI 선생님께 질문하기</h3>
            <div className="info-box">
              <p>🔑 <strong>AI 기능 활성화 방법:</strong></p>
              <ol>
                <li>OpenAI API 키 발급: https://platform.openai.com/api-keys</li>
                <li>환경 변수로 설정</li>
                <li>API 키 없이도 기본 기능은 사용 가능합니다.</li>
              </ol>
            </div>

            <div className="form-group">
              <label>질문 맥락</label>
              <select
                className="form-control"
                value={contextOption}
                onChange={(e) => setContextOption(e.target.value)}
              >
                <option>일반 질문</option>
                <option>현재 악보에 대해</option>
                <option>연습 방법</option>
                <option>수업 준비</option>
              </select>
            </div>

            <div className="form-group">
              <label>질문을 입력하세요</label>
              <textarea
                className="form-control"
                rows={4}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="예: 이 곡을 초등학교 3학년이 배우기에 적절한가요?"
              />
            </div>

            <div className="button-group">
              <button
                className="action-button"
                onClick={handleAskQuestion}
                disabled={isLoading || !question.trim()}
              >
                {isLoading ? (
                  <>
                    <span className="spinner"></span>
                    AI가 답변을 생성하는 중...
                  </>
                ) : (
                  '💬 질문하기'
                )}
              </button>
              {response && (
                <button className="secondary-button" onClick={handleClearChat}>
                  🗑️ 대화 초기화
                </button>
              )}
            </div>

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
              </div>
            )}

            {response && (
              <div className="response-box">
                <h4>🎵 AI 답변</h4>
                <div className="response-content">{response}</div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'theory' && (
          <div className="section">
            <h3>📖 음악 이론 설명</h3>
            <div className="form-row">
              <div className="form-group">
                <label>알고 싶은 음악 이론</label>
                <select
                  className="form-control"
                  value={theoryTopic}
                  onChange={(e) => setTheoryTopic(e.target.value)}
                >
                  <option>계이름</option>
                  <option>박자</option>
                  <option>화음</option>
                  <option>장조와 단조</option>
                  <option>음표와 쉼표</option>
                  <option>셈여림</option>
                  <option>빠르기말</option>
                  <option>음정</option>
                  <option>리듬</option>
                  <option>직접 입력</option>
                </select>
              </div>
              <div className="form-group">
                <label>학생 나이</label>
                <input
                  type="number"
                  className="form-control"
                  min={6}
                  max={13}
                  value={studentAge}
                  onChange={(e) => setStudentAge(Number(e.target.value))}
                />
              </div>
            </div>

            {theoryTopic === '직접 입력' && (
              <div className="form-group">
                <label>설명받고 싶은 주제를 입력하세요</label>
                <input
                  type="text"
                  className="form-control"
                  value={customTopic}
                  onChange={(e) => setCustomTopic(e.target.value)}
                  placeholder="예: 3화음"
                />
              </div>
            )}

            <button
              className="action-button"
              onClick={handleExplainTheory}
              disabled={isLoading || (theoryTopic === '직접 입력' && !customTopic.trim())}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  AI가 설명을 준비하는 중...
                </>
              ) : (
                '📖 설명 듣기'
              )}
            </button>

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
              </div>
            )}

            {response && (
              <div className="response-box">
                <h4>🎵 '{theoryTopic === '직접 입력' ? customTopic : theoryTopic}' 설명</h4>
                <div className="response-content">{response}</div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'lesson' && (
          <div className="section">
            <h3>📝 수업 계획 생성</h3>
            <div className="form-row">
              <div className="form-group">
                <label>곡 제목 *</label>
                <input
                  type="text"
                  className="form-control"
                  value={songTitle}
                  onChange={(e) => setSongTitle(e.target.value)}
                  placeholder="예: 학교종"
                />
              </div>
              <div className="form-group">
                <label>학년</label>
                <select
                  className="form-control"
                  value={gradeLevel}
                  onChange={(e) => setGradeLevel(e.target.value)}
                >
                  <option>1-2학년</option>
                  <option>3-4학년</option>
                  <option>5-6학년</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>수업 시간 (분): {lessonDuration}분</label>
              <input
                type="range"
                min={20}
                max={60}
                step={5}
                value={lessonDuration}
                onChange={(e) => setLessonDuration(Number(e.target.value))}
                className="form-control"
              />
            </div>

            <button
              className="action-button"
              onClick={handleGenerateLessonPlan}
              disabled={isLoading || !songTitle.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  AI가 수업 계획을 작성하는 중...
                </>
              ) : (
                '📝 수업 계획 생성'
              )}
            </button>

            {error && (
              <div className="error-message">
                <p>❌ {error}</p>
              </div>
            )}

            {lessonPlan && (
              <div className="response-box">
                <h4>📋 생성된 수업 계획</h4>
                <div className="response-content">{lessonPlan}</div>
                <button className="download-button" onClick={handleDownloadLessonPlan}>
                  💾 수업 계획 다운로드
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default AIAssistant
