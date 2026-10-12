// d:/Project/WEPAPP/next-app/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  // Added to force ESM mode and avoid CJS fallback
  optimizeDeps: {
    force: true,
  },
  ssr: {
    // Prevent Vite from trying to bundle external CJS modules that cause D:\ lstat errors
    noExternal: ['*'],
  },
   resolve: {
     alias: {
       '@': resolve(__dirname, 'src'),
       'fs': resolve(__dirname, 'src/shims/fs.ts'),
     },
   },
});
