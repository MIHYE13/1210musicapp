// API 클라이언트 유틸리티

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8501/api'

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
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
          formData.append(key, JSON.stringify(value))
        })
      }

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
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
    apiClient.request(`/score/${scoreId}/export/midi`),
  
  exportMusicXML: (scoreId: string) =>
    apiClient.request(`/score/${scoreId}/export/musicxml`),
}

export const aiApi = {
  chat: (question: string, context?: string) =>
    apiClient.request('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ question, context }),
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
  analyze: (file: File, fileType: 'midi' | 'youtube' | 'pdf') =>
    apiClient.uploadFile('/chord/analyze', file, { fileType }),
}

