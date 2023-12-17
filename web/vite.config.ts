import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  build:{
    assetsDir: "9bb29bc2dcb6d6e9",
    outDir: "../dist",
  },
  plugins: [react()],
  server: {
    proxy: {
      "/9bb29bc2dcb6d6e9": {
        target: 'http://localhost:5000/',
        changeOrigin: true,
      }
    }
  }

})
