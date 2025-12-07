import { useState, useEffect } from 'react'
import './App.css'
import Header from './components/Header'
import Navigation from './components/Navigation'
import AudioToScore from './components/AudioToScore'
import ScoreProcessing from './components/ScoreProcessing'
import AIAssistant from './components/AIAssistant'
import PerplexityYouTube from './components/PerplexityYouTube'
import TeacherDashboard from './components/TeacherDashboard'
import ChordAnalysis from './components/ChordAnalysis'

type Page = 
  | 'home' 
  | 'audio-to-score' 
  | 'score-processing' 
  | 'ai-assistant' 
  | 'perplexity-youtube' 
  | 'teacher-dashboard' 
  | 'chord-analysis'

function App() {
  const getPageFromHash = (): Page => {
    const hash = window.location.hash.slice(1)
    const validPages: Page[] = ['home', 'audio-to-score', 'score-processing', 'ai-assistant', 'perplexity-youtube', 'teacher-dashboard', 'chord-analysis']
    return validPages.includes(hash as Page) ? (hash as Page) : 'home'
  }

  const [currentPage, setCurrentPage] = useState<Page>(getPageFromHash())

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentPage(getPageFromHash())
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  const handlePageChange = (page: Page) => {
    setCurrentPage(page)
    window.location.hash = page
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <div className="home-page">
            <h1>🎵 초등 음악 도우미</h1>
            <p className="subtitle">
              오디오나 악보를 업로드하면 초등학생이 배우기 쉬운 형태로 변환해드립니다!
            </p>
            <p className="features">
              <strong>계이름 기재 · 다장조 변환 · 반주 추가 · 자동 재생</strong>
            </p>
            
            <div className="info-box">
              <p>👨‍🏫 <strong>교사이신가요?</strong> 위 메뉴에서 '교사 대시보드'를 선택하여 학급과 학생을 관리하세요!</p>
            </div>

            <div className="feature-grid">
              <div className="feature-card" onClick={() => handlePageChange('audio-to-score')}>
                <h3>🎤 오디오 → 악보</h3>
                <p>MP3, WAV 파일을 업로드하여 악보로 변환</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('score-processing')}>
                <h3>🎼 악보 처리</h3>
                <p>계이름 추가, 다장조 변환, 반주 생성</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('ai-assistant')}>
                <h3>🤖 AI 도우미</h3>
                <p>음악 이론 질문, 수업 계획 생성</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('perplexity-youtube')}>
                <h3>🔍 정보 & 영상</h3>
                <p>최신 정보 조사, 교육 영상 검색</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('chord-analysis')}>
                <h3>🎹 화음 분석</h3>
                <p>화음 자동 분석, 피아노 건반 표시</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('teacher-dashboard')}>
                <h3>👨‍🏫 교사 대시보드</h3>
                <p>학급 관리, 학생 관리, 수업 기록</p>
              </div>
            </div>
          </div>
        )
      case 'audio-to-score':
        return <AudioToScore />
      case 'score-processing':
        return <ScoreProcessing />
      case 'ai-assistant':
        return <AIAssistant />
      case 'perplexity-youtube':
        return <PerplexityYouTube />
      case 'teacher-dashboard':
        return <TeacherDashboard />
      case 'chord-analysis':
        return <ChordAnalysis />
      default:
        return <div>페이지를 찾을 수 없습니다.</div>
    }
  }

  return (
    <div className="App">
      <Header />
      <Navigation currentPage={currentPage} setCurrentPage={handlePageChange} />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  )
}

export default App
