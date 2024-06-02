import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  base:"/",
  server: {
    port: 80,
    strictPort: true,
    host: true,
    watch: {
      usePolling: true
    }
  },
  preview: {
    port: 80,
    strictPort: true,
   },
  plugins: [react({
    include: "**/*.jsx",
  })]
});
