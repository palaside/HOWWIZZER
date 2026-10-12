// vitest.simple.config.ts
import { defineConfig } from 'vitest/config';
import { resolve } from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'happy-dom',
    include: ['src/**/*.test.{ts,tsx}'],
    setupFiles: ['./vitest.setup.ts'],
    root: resolve(__dirname, '.'),
    watch: false,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      'fs': resolve(__dirname, 'src/shims/fs.ts'),
    },
  },
});
