import { FaMusic } from 'react-icons/fa'
import { HiSparkles } from 'react-icons/hi'
import './Header.css'

const Header = () => {
  return (
    <header className="app-header">
      <div className="header-content">
        <div className="header-icon-wrapper">
          <FaMusic className="header-icon" />
          <HiSparkles className="sparkle-icon sparkle-1" />
          <HiSparkles className="sparkle-icon sparkle-2" />
          <HiSparkles className="sparkle-icon sparkle-3" />
        </div>
        <div className="header-text">
          <h1>초등 음악 도우미</h1>
          <p>AI 기반 음악 학습 지원 웹 애플리케이션</p>
        </div>
      </div>
      <div className="header-wave">
        <svg viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,60 C300,100 600,20 900,60 C1050,80 1150,40 1200,60 L1200,120 L0,120 Z" fill="currentColor" opacity="0.1"></path>
        </svg>
      </div>
    </header>
  )
}

export default Header
