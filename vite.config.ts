import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src/frontend'),
    },
  },
  server: {
    port: 5173,
    host: true,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8501',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  // 환경 변수 보안 설정
  // VITE_ 접두사가 있는 환경 변수만 클라이언트 번들에 포함됩니다.
  // API 키나 비밀 정보는 절대 VITE_ 접두사를 사용하지 마세요!
  envPrefix: 'VITE_',
})


