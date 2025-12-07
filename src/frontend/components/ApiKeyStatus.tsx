import { useState, useEffect } from 'react'
import './ApiKeyStatus.css'

interface ApiStatus {
  name: string
  status: 'checking' | 'valid' | 'invalid' | 'not_set'
  message: string
}

const ApiKeyStatus = () => {
  const [apiStatuses, setApiStatuses] = useState<ApiStatus[]>([
    { name: 'OpenAI', status: 'checking', message: '확인 중...' },
    { name: 'Perplexity', status: 'checking', message: '확인 중...' },
    { name: 'YouTube', status: 'checking', message: '확인 중...' },
  ])
  const [isChecking, setIsChecking] = useState(false)

  const checkApiKeys = async () => {
    setIsChecking(true)
    
    // 백엔드 API를 통해 API 키 상태 확인
    try {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8501/api'
      const response = await fetch(`${apiBaseUrl}/keys/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (response.ok) {
        const data = await response.json()
        setApiStatuses(data.statuses || [])
      } else {
        // 백엔드가 없을 경우 로컬에서 확인
        checkLocalApiKeys()
      }
    } catch (error) {
      // 네트워크 오류 처리
      if (error instanceof TypeError && error.message.includes('fetch')) {
        setApiStatuses([
          { 
            name: 'API 서버', 
            status: 'not_set', 
            message: `서버에 연결할 수 없습니다. (${apiBaseUrl})` 
          },
        ])
      } else {
        // 백엔드가 없을 경우 로컬에서 확인
        checkLocalApiKeys()
      }
    } finally {
      setIsChecking(false)
    }
  }

  const checkLocalApiKeys = () => {
    // 로컬 스토리지나 환경 변수에서 확인 (프론트엔드에서는 직접 확인 불가)
    // 실제로는 백엔드 API를 통해 확인해야 함
    setApiStatuses([
      { 
        name: 'OpenAI', 
        status: 'not_set', 
        message: '백엔드 API를 통해 확인하세요' 
      },
      { 
        name: 'Perplexity', 
        status: 'not_set', 
        message: '백엔드 API를 통해 확인하세요' 
      },
      { 
        name: 'YouTube', 
        status: 'not_set', 
        message: '백엔드 API를 통해 확인하세요' 
      },
    ])
  }

  useEffect(() => {
    checkApiKeys()
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'valid':
        return '✅'
      case 'invalid':
        return '❌'
      case 'not_set':
        return '⚠️'
      default:
        return '🔄'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'valid':
        return 'status-valid'
      case 'invalid':
        return 'status-invalid'
      case 'not_set':
        return 'status-not-set'
      default:
        return 'status-checking'
    }
  }

  return (
    <div className="api-key-status">
      <div className="status-header">
        <h3>🔐 API 키 상태</h3>
        <button 
          className="refresh-button"
          onClick={checkApiKeys}
          disabled={isChecking}
        >
          {isChecking ? '🔄 확인 중...' : '🔄 새로고침'}
        </button>
      </div>

      <div className="status-list">
        {apiStatuses.map((api, index) => (
          <div key={index} className={`status-item ${getStatusColor(api.status)}`}>
            <div className="status-icon">{getStatusIcon(api.status)}</div>
            <div className="status-info">
              <div className="status-name">{api.name}</div>
              <div className="status-message">{api.message}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="status-footer">
        <p>💡 <strong>API 키 설정 방법:</strong></p>
        <ol>
          <li>프로젝트 루트에 <code>.env</code> 파일 생성</li>
          <li><code>.env.example</code> 파일을 참고하여 API 키 입력</li>
          <li>Python 스크립트로 확인: <code>python check_api_keys.py</code></li>
        </ol>
      </div>
    </div>
  )
}

export default ApiKeyStatus

