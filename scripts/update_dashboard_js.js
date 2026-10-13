const fs = require('fs');
const path = require('path');

const jsPath = path.join(process.cwd(), 'frontend', 'static', 'dashboard.js');
let code = fs.readFileSync(jsPath, 'utf8');

// Add initInspectionPhotos() into DOMContentLoaded
code = code.replace(
  'loadCadenceGaps();',
  'loadCadenceGaps();\r\n  initInspectionPhotos();'
);

const photoModuleCode = `\r\n\r\n// ==========================================
// WEEKLY INSPECTION PHOTOS MODULE (อัพรูป จำนวน ๔ ภาพ)
// ==========================================
const INSPECTION_PHOTO_SLOTS = [
  { id: 1, title: 'ตำแหน่งที่ ๑ (บน-ซ้าย)', desc: 'ชั้นวางอุปกรณ์ / คลัง สป.สาย สพ.' },
  { id: 2, title: 'ตำแหน่งที่ ๒ (บน-ขวา)', desc: 'ตรวจสภาพปืนใหญ่ / โรงเก็บปืนใหญ่' },
  { id: 3, title: 'ตำแหน่งที่ ๓ (ล่าง-ซ้าย)', desc: 'แท่นเครื่องมือ / เครื่องมือประจำปืน' },
  { id: 4, title: 'ตำแหน่งที่ ๔ (ล่าง-ขวา)', desc: 'บอร์ดสถิติ / แผนภูมิการปรนนิบัติ' }
];

let currentInspectionPhotos = [];

async function initInspectionPhotos() {
  const grid = document.getElementById('inspectionPhotosGrid');
  if (!grid) return;

  // 1. Check localStorage first
  try {
    const cached = localStorage.getItem('inspection_photos');
    if (cached) {
      currentInspectionPhotos = JSON.parse(cached);
      if (Array.isArray(currentInspectionPhotos) && currentInspectionPhotos.length >= 4) {
        renderInspectionPhotosGrid(currentInspectionPhotos);
        return;
      }
    }
  } catch (e) {
    console.warn('Could not read cached photos:', e);
  }

  // 2. Try fetching from backend API or static JSON
  try {
    let res = await fetch(\`\${API_BASE}/inspection/photos\`);
    if (!res.ok) {
      res = await fetch('/backend/data/inspection_photos.json');
    }
    if (res.ok) {
      const data = await res.json();
      if (data && Array.isArray(data.photos) && data.photos.length >= 4) {
        currentInspectionPhotos = data.photos;
        localStorage.setItem('inspection_photos', JSON.stringify(currentInspectionPhotos));
        renderInspectionPhotosGrid(currentInspectionPhotos);
        return;
      }
    }
  } catch (err) {
    console.warn('Could not fetch inspection photos from server:', err);
  }

  // Fallback if empty
  renderInspectionPhotosGrid(currentInspectionPhotos);
}

function renderInspectionPhotosGrid(photos) {
  const grid = document.getElementById('inspectionPhotosGrid');
  const badge = document.getElementById('photoUploadStatusBadge');
  if (!grid) return;

  const validCount = (photos || []).filter(p => !!p).length;
  if (badge) {
    badge.innerText = \`พร้อมใช้งาน (\${validCount}/๔ ภาพ)\`;
    badge.className = validCount >= 4 ? 'badge badge-generated' : 'badge badge-pending';
  }

  grid.innerHTML = INSPECTION_PHOTO_SLOTS.map((slot, idx) => {
    const photoSrc = photos && photos[idx] ? photos[idx] : '';
    const hasPhoto = !!photoSrc;

    return \`
      <div class="photo-slot-card" style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.4); transition: all 0.2s;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <span style="font-weight: 600; font-size: 13.5px; color: #fff;">\${slot.title}</span>
            <div style="font-size: 11.5px; color: var(--accent-cyan); margin-top: 1px;">\${slot.desc}</div>
          </div>
          <span class="badge" style="font-size: 11px; padding: 2px 8px; background: \${hasPhoto ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)'}; color: \${hasPhoto ? '#34d399' : '#f87171'}; border: 1px solid \${hasPhoto ? 'rgba(16,185,129,0.35)' : 'rgba(239,68,68,0.35)'};">
            \${hasPhoto ? '✓ มีภาพพร้อม' : 'รออัพโหลด'}
          </span>
        </div>

        <div style="position: relative; height: 160px; border-radius: 8px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.15); background: rgba(0, 0, 0, 0.5); cursor: pointer;"
             onclick="document.getElementById('slotPhotoInput-\${idx}').click()"
             title="คลิกเพื่อเปลี่ยนภาพตำแหน่งที่ \${idx + 1} (\${slot.title})">
          \${hasPhoto ? \`
            <img src="\${photoSrc}" alt="\${slot.title}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.25s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
          \` : \`
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted); gap: 8px;">
              <span style="font-size: 28px;">📷</span>
              <span style="font-size: 12.5px;">คลิกเพื่ออัพโหลดภาพตำแหน่งนี้</span>
            </div>
          \`}
          <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.85)); padding: 6px 10px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 11.5px; color: #38bdf8; font-weight: 500;">🔄 คลิกเปลี่ยนภาพ</span>
            <span style="font-size: 11px; color: #cbd5e1;">ช่องที่ \${idx + 1}</span>
          </div>
        </div>

        <input type="file" id="slotPhotoInput-\${idx}" accept="image/*" style="display: none;" onchange="handleSinglePhotoUpload(\${idx}, event)">
      </div>
    \`;
  }).join('');
}

async function handleBulkPhotoUpload(event) {
  const files = Array.from(event.target.files || []);
  if (!files.length) return;

  const readPromises = files.slice(0, 4).map(file => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  });

  try {
    const base64List = await Promise.all(readPromises);
    if (!Array.isArray(currentInspectionPhotos) || currentInspectionPhotos.length < 4) {
      currentInspectionPhotos = new Array(4).fill('');
    }
    for (let i = 0; i < base64List.length; i++) {
      currentInspectionPhotos[i] = base64List[i];
    }

    // Save to LocalStorage
    localStorage.setItem('inspection_photos', JSON.stringify(currentInspectionPhotos));

    // Try posting to Backend API
    try {
      await fetch(\`\${API_BASE}/inspection/photos\`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photos: currentInspectionPhotos })
      });
    } catch (e) {
      console.warn('Could not sync to backend:', e);
    }

    renderInspectionPhotosGrid(currentInspectionPhotos);
    alert(\`อัพโหลดภาพถ่ายสำเร็จจำนวน \${base64List.length} ภาพ!\\nภาพจะวิ่งตรงไปวางแปะแทนที่เดิมในหน้า ๔ ของแบบรายงาน สด.๑ ทันที ๑๐๐%\`);
  } catch (err) {
    alert('เกิดข้อผิดพลาดในการอ่านไฟล์ภาพ: ' + err.message);
  } finally {
    event.target.value = '';
  }
}

async function handleSinglePhotoUpload(slotIndex, event) {
  const file = event.target.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (e) => {
    const dataUrl = e.target.result;
    if (!Array.isArray(currentInspectionPhotos) || currentInspectionPhotos.length < 4) {
      currentInspectionPhotos = new Array(4).fill('');
    }
    currentInspectionPhotos[slotIndex] = dataUrl;

    // Save to LocalStorage
    localStorage.setItem('inspection_photos', JSON.stringify(currentInspectionPhotos));

    // Try posting to Backend API
    try {
      await fetch(\`\${API_BASE}/inspection/photos\`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photos: currentInspectionPhotos })
      });
    } catch (e) {
      console.warn('Could not sync to backend:', e);
    }

    renderInspectionPhotosGrid(currentInspectionPhotos);
    alert(\`อัพเดตภาพตำแหน่งที่ \${slotIndex + 1} สำเร็จ!\\nภาพถูกนำไปวางแปะแทนที่เดิมในหน้า ๔ เรียบร้อยแล้ว\`);
  };
  reader.readAsDataURL(file);
  event.target.value = '';
}

async function resetInspectionPhotosToDefault() {
  if (!confirm('ต้องการรีเซ็ตภาพถ่ายโรงเก็บปืนใหญ่กลับเป็นภาพถ่ายต้นฉบับเริ่มต้นหรือไม่?')) {
    return;
  }

  try {
    const res = await fetch('/backend/data/inspection_photos.json');
    if (res.ok) {
      const data = await res.json();
      if (data && Array.isArray(data.photos) && data.photos.length >= 4) {
        currentInspectionPhotos = data.photos;
        localStorage.setItem('inspection_photos', JSON.stringify(currentInspectionPhotos));
        
        try {
          await fetch(\`\${API_BASE}/inspection/photos\`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ photos: currentInspectionPhotos })
          });
        } catch (e) {}

        renderInspectionPhotosGrid(currentInspectionPhotos);
        alert('รีเซ็ตภาพถ่ายโรงเก็บปืนใหญ่กลับเป็นภาพตั้งต้นเรียบร้อยแล้ว');
        return;
      }
    }
  } catch (err) {
    console.error('Reset failed:', err);
  }
  alert('ไม่สามารถดึงภาพต้นฉบับได้ กรุณาลองใหม่อีกครั้ง');
}
`;

fs.writeFileSync(jsPath, code + photoModuleCode, 'utf8');
console.log('Successfully updated frontend/static/dashboard.js with inspection photos logic');
