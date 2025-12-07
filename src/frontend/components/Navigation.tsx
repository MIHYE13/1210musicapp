import { useState } from 'react'
import './Navigation.css'

type Page = 
  | 'home' 
  | 'audio-to-score' 
  | 'score-processing' 
  | 'ai-assistant' 
  | 'perplexity-youtube' 
  | 'teacher-dashboard' 
  | 'chord-analysis'

interface NavigationProps {
  currentPage: Page
  setCurrentPage: (page: Page) => void
}

const Navigation = ({ currentPage, setCurrentPage }: NavigationProps) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const menuItems = [
    { id: 'home' as Page, label: '🏠 홈', icon: '🏠' },
    { id: 'audio-to-score' as Page, label: '🎤 오디오→악보', icon: '🎤' },
    { id: 'score-processing' as Page, label: '🎼 악보 처리', icon: '🎼' },
    { id: 'ai-assistant' as Page, label: '🤖 AI 도우미', icon: '🤖' },
    { id: 'perplexity-youtube' as Page, label: '🔍 정보 & 영상', icon: '🔍' },
    { id: 'chord-analysis' as Page, label: '🎹 화음 분석', icon: '🎹' },
    { id: 'teacher-dashboard' as Page, label: '👨‍🏫 교사 대시보드', icon: '👨‍🏫' },
  ]

  return (
    <nav className="navigation">
      <div className="nav-container">
        <button 
          className="mobile-menu-toggle"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="메뉴 토글"
        >
          ☰
        </button>
        <ul className={`nav-menu ${isMobileMenuOpen ? 'open' : ''}`}>
          {menuItems.map((item) => (
            <li key={item.id}>
              <button
                className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
                onClick={() => {
                  setCurrentPage(item.id)
                  setIsMobileMenuOpen(false)
                }}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  )
}

export default Navigation

