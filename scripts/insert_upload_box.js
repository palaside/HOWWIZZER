const fs = require('fs');
const path = require('path');

const filePath = path.join(process.cwd(), 'frontend', 'templates', 'index.html');
let content = fs.readFileSync(filePath, 'utf8');

const targetMarker = '<div id="operatorsGrid" style="display: grid; grid-template-columns: repeat(9, minmax(0, 1fr)); gap: 6px;">';
if (!content.includes(targetMarker)) {
  console.error('Target marker not found!');
  process.exit(1);
}

// Find closing </div> of operatorsGrid panel
const markerIdx = content.indexOf(targetMarker);
const closeDivIdx = content.indexOf('</div>\r\n    </div>', markerIdx);
const insertPoint = closeDivIdx + '</div>\r\n    </div>'.length;

const cardHtml = `\r\n\r\n    <!-- 📷 Inspection Photos Upload Box (อัพรูป จำนวน ๔ ภาพ) -->
    <div class="glass-panel" style="padding: 22px 20px; margin-bottom: 24px; border-color: rgba(56, 189, 248, 0.35); background: linear-gradient(180deg, rgba(17, 24, 39, 0.8) 0%, rgba(10, 14, 23, 0.95) 100%);">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px; margin-bottom: 18px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 14px;">
        <div>
          <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <h3 style="font-size: 18px; font-weight: 600; color: #fff; margin: 0; display: flex; align-items: center; gap: 8px;">
              📷 ภาพถ่าย​การ​ตรวจ โรง​เก็บ​ปืนใหญ่
            </h3>
            <span class="badge" style="background: rgba(56, 189, 248, 0.18); border: 1px solid rgba(56, 189, 248, 0.45); color: #38bdf8; font-size: 12.5px; padding: 2px 10px;">
              อัพรูป จำนวน ๔ ภาพ
            </span>
            <span class="badge badge-generated" id="photoUploadStatusBadge" style="font-size: 12px;">
              พร้อมใช้งาน (๔/๔ ภาพ)
            </span>
          </div>
          <p style="font-size: 13.5px; color: var(--text-secondary); margin-top: 5px;">
            เมื่อ​อัพโหลด​แล้ว ภาพ​จะ​วิ่ง​ตรง​ไป​วาง​แปะ​แทนที่​เดิม ๔ ตำแหน่ง (หน้า ๔ ของ​แบบ​รายงานผลการตรวจ สด.๑) โดย​อัตโนมัติ ๑๐๐%
          </p>
        </div>

        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
          <input type="file" id="bulkPhotoUploadInput" accept="image/*" multiple style="display: none;" onchange="handleBulkPhotoUpload(event)">
          <button type="button" onclick="document.getElementById('bulkPhotoUploadInput').click()" class="btn-primary" style="padding: 9px 18px; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 16px rgba(56, 189, 248, 0.35);">
            📤 อัพรูป จำนวน ๔ ภาพ
          </button>
          <button type="button" onclick="resetInspectionPhotosToDefault()" class="btn-secondary" style="padding: 8px 14px; font-size: 13px; color: #cbd5e1;" title="รีเซ็ตกลับเป็นภาพถ่ายต้นแบบของโรงเก็บปืนใหญ่">
            🔄 รีเซ็ตภาพตั้งต้น
          </button>
          <a href="/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html" target="_blank" class="btn-secondary" style="padding: 8px 14px; font-size: 13px; color: var(--accent-gold); border-color: rgba(245, 158, 11, 0.4); text-decoration: none;" title="เปิดดูหน้า ๔ ในแบบรายงาน สด.๑">
            👁️ เปิดตรวจหน้า ๔
          </a>
        </div>
      </div>

      <!-- 4 Photo Slots (2x2 Grid Matching Page 4) -->
      <div id="inspectionPhotosGrid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">
        <!-- Hydrated via dashboard.js -->
      </div>

      <div style="margin-top: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; font-size: 12.5px; color: var(--text-muted);">
        <div style="display: flex; align-items: center; gap: 6px;">
          <span>💡 <strong>คำแนะนำ:</strong> สามารถกดปุ่ม <em>"อัพรูป จำนวน ๔ ภาพ"</em> เพื่อเลือก ๔ ไฟล์พร้อมกัน หรือคลิกที่แต่ละช่องเพื่อเปลี่ยนภาพเฉพาะตำแหน่งได้</span>
        </div>
        <div style="color: var(--accent-cyan);">
          ✓ ระบบบันทึกลงคลังถาวรและอัพเดทไปยังเอกสาร สด.๑ ทันที
        </div>
      </div>
    </div>`;

const updatedContent = content.slice(0, insertPoint) + cardHtml + content.slice(insertPoint);
fs.writeFileSync(filePath, updatedContent, 'utf8');
console.log('Successfully inserted Inspection Photos Upload Card into index.html');
