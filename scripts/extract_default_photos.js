const fs = require('fs');
const path = require('path');

const srcFile = path.join(process.cwd(), 'แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html');
const content = fs.readFileSync(srcFile, 'utf8');

// Match <div class="photo-card">\s*<img src="(data:image/jpeg;base64,[^"]+)"
const regex = /<div class="photo-card">\s*<img[^>]+src="(data:image\/jpeg;base64,[^"]+)"/g;
const photos = [];
let m;
while ((m = regex.exec(content)) !== null) {
  photos.push(m[1]);
}

console.log('Extracted photos count:', photos.length);
if (photos.length >= 4) {
  const outDir = path.join(process.cwd(), 'backend', 'data');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'inspection_photos.json'), JSON.stringify({ photos: photos.slice(0, 4) }, null, 2));
  console.log('Successfully saved to backend/data/inspection_photos.json');
} else {
  console.error('Error: Less than 4 photos found!');
}
