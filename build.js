const fs = require('fs');
const path = require('path');

// 1. Ensure minimal dist directory exists for Vercel Static Output check
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// 2. Write lightweight index.html fallback (under 1KB)
fs.writeFileSync(
  path.join(distDir, 'index.html'),
  '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HOWWIZZER</title></head><body><script>window.location.href="/";</script></body></html>'
);

console.log('Build completed: minimal dist output created.');
