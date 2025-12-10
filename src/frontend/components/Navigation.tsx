import { useState } from 'react'
import { 
  HiHome, 
  HiSparkles,
  HiSearch,
  HiPuzzle,
  HiAcademicCap
} from 'react-icons/hi'
import { HiBars3, HiXMark } from 'react-icons/hi2'
import { FaMusic } from 'react-icons/fa'
import './Navigation.css'

type Page = 
  | 'home' 
  | 'chord-builder' 
  | 'rhythm-composer'
  | 'classic-music' 
  | 'ai-assistant' 
  | 'perplexity-youtube' 
  | 'teacher-dashboard'

interface NavigationProps {
  currentPage: Page
  setCurrentPage: (page: Page) => void
}

const Navigation = ({ currentPage, setCurrentPage }: NavigationProps) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const menuItems = [
    { id: 'home' as Page, label: '홈', icon: HiHome },
    { id: 'rhythm-composer' as Page, label: '리듬 작곡', icon: HiPuzzle },
    { id: 'chord-builder' as Page, label: '화음 구성', icon: HiPuzzle },
    { id: 'classic-music' as Page, label: '클래식 감상', icon: FaMusic },
    { id: 'ai-assistant' as Page, label: 'AI 도우미', icon: HiSparkles },
    { id: 'perplexity-youtube' as Page, label: '정보 & 영상', icon: HiSearch },
    { id: 'teacher-dashboard' as Page, label: '교사 대시보드', icon: HiAcademicCap },
  ]

  return (
    <nav className="navigation">
      <div className="nav-container">
        <button 
          className="mobile-menu-toggle"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="메뉴 토글"
        >
          {isMobileMenuOpen ? <HiXMark /> : <HiBars3 />}
        </button>
        <ul className={`nav-menu ${isMobileMenuOpen ? 'open' : ''}`}>
          {menuItems.map((item) => {
            const IconComponent = item.icon
            return (
              <li key={item.id}>
                <button
                  className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
                  onClick={() => {
                    setCurrentPage(item.id)
                    setIsMobileMenuOpen(false)
                  }}
                >
                  <IconComponent className="nav-icon" />
                  <span className="nav-label">{item.label}</span>
                </button>
              </li>
            )
          })}
        </ul>
      </div>
    </nav>
  )
}

export default Navigation
