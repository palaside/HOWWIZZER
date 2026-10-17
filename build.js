const fs = require('fs');
const path = require('path');

// 1. Ensure dist directory exists
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// 2. Copy static files into dist if static exists
const staticDir = path.join(__dirname, 'static');
if (fs.existsSync(staticDir)) {
  fs.cpSync(staticDir, distDir, { recursive: true });
}

// 3. Ensure an index.html fallback exists
const indexPath = path.join(distDir, 'index.html');
if (!fs.existsSync(indexPath)) {
  fs.writeFileSync(
    indexPath,
    '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HOWWIZZER</title></head><body><script>window.location.href="/";</script></body></html>'
  );
}

console.log('Build completed: dist output created successfully.');
