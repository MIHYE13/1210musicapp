// API 클라이언트 유틸리티

// API Base URL 설정
// 개발 환경: http://localhost:8501/api
// 프로덕션: 환경 변수 VITE_API_BASE_URL 사용
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8501/api'

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

class ApiClient {
  private baseUrl: string
  private timeout: number

  constructor(baseUrl: string = API_BASE_URL, timeout: number = 150000) {  // 오디오 처리 시간을 고려하여 150초로 증가
    this.baseUrl = baseUrl
    this.timeout = timeout
  }

  private async fetchWithTimeout(url: string, options: RequestInit): Promise<Response> {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), this.timeout)
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      })
      clearTimeout(timeoutId)
      return response
    } catch (error) {
      clearTimeout(timeoutId)
      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('요청 시간이 초과되었습니다. 서버 응답을 기다리는 중입니다.')
      }
      throw error
    }
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {},
    returnBlob: boolean = false
  ): Promise<ApiResponse<T>> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP error! status: ${response.status}`
        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorData.error || errorMessage
        } catch {
          errorMessage = errorText || errorMessage
        }
        throw new Error(errorMessage)
      }

      let data: any
      if (returnBlob) {
        // Blob 응답 처리 (파일 다운로드)
        const contentType = response.headers.get('content-type') || ''
        if (contentType.includes('application/json')) {
          // JSON 오류 응답인 경우
          data = await response.json()
        } else {
          // 실제 파일 데이터
          data = await response.blob()
        }
      } else {
        // JSON 응답 처리
        data = await response.json()
      }
      return { success: true, data }
    } catch (error) {
      // 네트워크 오류 처리
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return {
          success: false,
          error: `API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요. (${this.baseUrl})`,
        }
      }
      
      // 기타 오류
      return {
        success: false,
        error: error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.',
      }
    }
  }

  async uploadFile<T>(
    endpoint: string,
    file: File,
    additionalData?: Record<string, any>
  ): Promise<ApiResponse<T>> {
    try {
      const formData = new FormData()
      formData.append('file', file)

      if (additionalData) {
        Object.entries(additionalData).forEach(([key, value]) => {
          if (key === 'options' && typeof value === 'object') {
            // 옵션은 JSON 문자열로 변환
            formData.append(key, JSON.stringify(value))
          } else {
            formData.append(key, String(value))
          }
        })
      }

      const response = await this.fetchWithTimeout(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        body: formData,
        // Content-Type 헤더를 설정하지 않음 (브라우저가 자동으로 multipart/form-data 설정)
      })

      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = `HTTP error! status: ${response.status}`
        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorData.error || errorMessage
        } catch {
          errorMessage = errorText || errorMessage
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      
      // API 응답에 success 필드가 있는 경우 확인
      if (data && typeof data === 'object' && 'success' in data && !data.success) {
        return {
          success: false,
          error: data.error || data.detail || 'API 요청이 실패했습니다.',
        }
      }
      
      return { success: true, data }
    } catch (error) {
      // 네트워크 오류 처리
      if (error instanceof TypeError && (error.message.includes('fetch') || error.message.includes('Failed to fetch'))) {
        return {
          success: false,
          error: `API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.\n\n해결 방법:\n1. API 서버 시작: python start_api_simple.py\n2. 서버 주소: ${this.baseUrl}`,
        }
      }
      
      // 기타 오류
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.'
      return {
        success: false,
        error: errorMessage,
      }
    }
  }
}

export const apiClient = new ApiClient()

// API 엔드포인트 함수들
export const audioApi = {
  processAudio: (file: File) =>
    apiClient.uploadFile('/audio/process', file),
}

export const scoreApi = {
  processScore: (file: File, options: {
    addSolfege: boolean
    simplifyRhythm: boolean
    transposeC: boolean
    addChords: boolean
  }) =>
    apiClient.uploadFile('/score/process', file, { options }),
  
  exportMidi: (scoreId: string) =>
    apiClient.request(`/score/${scoreId}/export/midi`, {
      method: 'GET',
    }, true), // blob 응답 처리
  
  exportMp3: (scoreId: string) =>
    apiClient.request(`/score/${scoreId}/export/mp3`, {
      method: 'GET',
    }, true), // blob 응답 처리
  
  exportMusicXML: (scoreId: string) =>
    apiClient.request(`/score/${scoreId}/export/musicxml`, {
      method: 'GET',
    }, true), // blob 응답 처리
}

export const aiApi = {
  chat: (question: string, context?: string) =>
    apiClient.request('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ question, context }),
    }),
  
  clearChat: () =>
    apiClient.request('/ai/chat/clear', {
      method: 'POST',
    }),
  
  explainTheory: (topic: string, age: number) =>
    apiClient.request('/ai/explain-theory', {
      method: 'POST',
      body: JSON.stringify({ topic, age }),
    }),
  
  generateLessonPlan: (songTitle: string, grade: string, duration: number) =>
    apiClient.request('/ai/lesson-plan', {
      method: 'POST',
      body: JSON.stringify({ songTitle, grade, duration }),
    }),
}

export const perplexityApi = {
  search: (query: string, searchType: string) =>
    apiClient.request('/perplexity/search', {
      method: 'POST',
      body: JSON.stringify({ query, searchType }),
    }),
}

export const youtubeApi = {
  search: (query: string, maxResults: number = 5) =>
    apiClient.request('/youtube/search', {
      method: 'POST',
      body: JSON.stringify({ query, maxResults }),
    }),
}

export const chordApi = {
  analyze: (file: File, fileType: 'midi' | 'youtube' | 'pdf' | 'audio' | 'image') =>
    apiClient.uploadFile('/chord/analyze', file, { fileType }),
  
  analyzeYouTube: (youtubeUrl: string) =>
    apiClient.request('/chord/analyze-youtube', {
      method: 'POST',
      body: JSON.stringify({ youtubeUrl }),
    }),
}

