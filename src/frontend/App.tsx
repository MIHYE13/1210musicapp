import { useState, useEffect } from 'react'
import { 
  HiSparkles,
  HiSearch,
  HiPuzzle,
  HiAcademicCap
} from 'react-icons/hi'
import { FaMusic } from 'react-icons/fa'
import './App.css'
import Header from './components/Header'
import Navigation from './components/Navigation'
import AIAssistant from './components/AIAssistant'
import PerplexityYouTube from './components/PerplexityYouTube'
import TeacherDashboard from './components/TeacherDashboard'
import ChordAnalysis from './components/ChordAnalysis'
import ClassicMusicEducation from './components/ClassicMusicEducation'
import RhythmComposer from './components/RhythmComposer'

type Page = 
  | 'home' 
  | 'chord-builder' 
  | 'rhythm-composer'
  | 'classic-music' 
  | 'ai-assistant' 
  | 'perplexity-youtube' 
  | 'teacher-dashboard'

function App() {
  const getPageFromHash = (): Page => {
    const hash = window.location.hash.slice(1)
    const validPages: Page[] = ['home', 'chord-builder', 'rhythm-composer', 'classic-music', 'ai-assistant', 'perplexity-youtube', 'teacher-dashboard']
    return validPages.includes(hash as Page) ? (hash as Page) : 'home'
  }

  const [currentPage, setCurrentPage] = useState<Page>(() => {
    const page = getPageFromHash()
    // 초기 로드 시 hash가 없으면 'home'으로 설정
    if (!window.location.hash) {
      window.location.hash = 'home'
    }
    return page
  })

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentPage(getPageFromHash())
    }

    // 초기 로드 시 hash가 없으면 'home'으로 설정
    if (!window.location.hash) {
      window.location.hash = 'home'
      setCurrentPage('home')
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
          <div className="home-page" style={{ minHeight: '60vh', display: 'flex', flexDirection: 'column' }}>
            <h1>초등 음악 도우미</h1>
            <p className="subtitle">
              피아노 건반을 클릭하여 화음을 만들고, 음악 이론을 배워보세요!
            </p>
            <p className="features">
              <strong>화음 구성</strong> · <strong>화음 분석</strong> · <strong>음악 이론 학습</strong> · <strong>교육 자료 검색</strong>
            </p>
            
            <div className="info-box">
              <p>
                <HiAcademicCap style={{ display: 'inline', marginRight: '0.5rem', fontSize: '1.2rem' }} />
                <strong>교사이신가요?</strong> 위 메뉴에서 '교사 대시보드'를 선택하여 학급과 학생을 관리하세요!
              </p>
            </div>

            <div className="feature-grid">
              <div className="feature-card main-feature" onClick={() => handlePageChange('rhythm-composer')}>
                <div className="icon-wrapper">
                  <HiPuzzle />
                </div>
                <h3>🎼 리듬 작곡기</h3>
                <p>박자에 맞춰 건반을 클릭하면 자동으로 화음 반주 악보가 그려집니다!</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('chord-builder')}>
                <div className="icon-wrapper">
                  <HiPuzzle />
                </div>
                <h3>🎹 화음 구성하기</h3>
                <p>피아노 건반을 클릭하여 화음을 만들고 분석해보세요!</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('classic-music')}>
                <div className="icon-wrapper">
                  <FaMusic />
                </div>
                <h3>🎼 클래식 음악 감상</h3>
                <p>유명 작곡가의 곡을 감상하고 멜로디와 화음을 배워보세요!</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('ai-assistant')}>
                <div className="icon-wrapper">
                  <HiSparkles />
                </div>
                <h3>AI 도우미</h3>
                <p>음악 이론 질문, 수업 계획 생성</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('perplexity-youtube')}>
                <div className="icon-wrapper">
                  <HiSearch />
                </div>
                <h3>정보 & 영상</h3>
                <p>최신 정보 조사, 교육 영상 검색</p>
              </div>
              <div className="feature-card" onClick={() => handlePageChange('teacher-dashboard')}>
                <div className="icon-wrapper">
                  <HiAcademicCap />
                </div>
                <h3>교사 대시보드</h3>
                <p>학급 관리, 학생 관리, 수업 기록</p>
              </div>
            </div>
          </div>
        )
      case 'chord-builder':
        return <ChordAnalysis />
      case 'rhythm-composer':
        return <RhythmComposer />
      case 'classic-music':
        return <ClassicMusicEducation />
      case 'ai-assistant':
        return <AIAssistant />
      case 'perplexity-youtube':
        return <PerplexityYouTube />
      case 'teacher-dashboard':
        return <TeacherDashboard />
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
