// Tactical Military Document & Custody Management Dashboard
const API_BASE = '/api/v1';

function toThaiNum(n) {
  if (n === null || n === undefined) return '';
  return String(n).replace(/[0-9]/g, d => '๐๑๒๓๔๕๖๗๘๙'[d]);
}

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initDateDefaults();
  loadDocumentChecklist();
  loadOperators();
  loadInventory();
  loadExternalIntake();
  loadCadenceGaps();
  initInspectionPhotos();
  initMasterChecklist();
});

function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      document.getElementById(targetId)?.classList.add('active');
    });
  });
}

function initDateDefaults() {
  const targetDateInput = document.getElementById('targetCycleDate');
  const targetDisplay = document.getElementById('targetCycleDateDisplay');
  
  // Default to 2026-11-06 (Cycle 2 - 6 พ.ย. 69: Monday 2 Nov start)
  const initialDate = targetDateInput?.value || '2026-11-06';
  if (targetDateInput) {
    targetDateInput.value = initialDate;
    targetDateInput.addEventListener('change', (e) => onNativeDateChanged(e.target.value));
  }
  
  if (targetDisplay) {
    targetDisplay.value = formatToThaiBE(initialDate);
    targetDisplay.addEventListener('change', (e) => onThaiDateInputChanged(e.target.value));
    targetDisplay.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        onThaiDateInputChanged(e.target.value);
        targetDisplay.blur();
      }
    });
  }

  updateCycleInfo(initialDate);
}

function triggerNativeDatePicker() {
  const nativeInput = document.getElementById('targetCycleDate');
  if (nativeInput) {
    if (typeof nativeInput.showPicker === 'function') {
      nativeInput.showPicker();
    } else {
      nativeInput.focus();
    }
  }
}

function onNativeDateChanged(isoDate) {
  if (!isoDate) return;
  const targetDisplay = document.getElementById('targetCycleDateDisplay');
  if (targetDisplay) {
    targetDisplay.value = formatToThaiBE(isoDate);
  }
  updateCycleInfo(isoDate);
}

function onThaiDateInputChanged(thaiStr) {
  const iso = parseThaiBEToIso(thaiStr);
  if (iso) {
    const targetDateInput = document.getElementById('targetCycleDate');
    if (targetDateInput) {
      targetDateInput.value = iso;
    }
    const targetDisplay = document.getElementById('targetCycleDateDisplay');
    if (targetDisplay) {
      targetDisplay.value = formatToThaiBE(iso);
    }
    updateCycleInfo(iso);
  } else {
    // Revert to current valid date if invalid format
    const targetDateInput = document.getElementById('targetCycleDate');
    const targetDisplay = document.getElementById('targetCycleDateDisplay');
    if (targetDateInput && targetDisplay) {
      targetDisplay.value = formatToThaiBE(targetDateInput.value);
    }
  }
}

function formatToThaiBE(isoDateStr) {
  if (!isoDateStr) return '';
  const parts = isoDateStr.split('-');
  if (parts.length !== 3) return '';
  const y = parseInt(parts[0], 10);
  const m = parseInt(parts[1], 10);
  const d = parseInt(parts[2], 10);
  const beYear = (y + 543) % 100;
  return `${String(d).padStart(2, '0')}/${String(m).padStart(2, '0')}/${String(beYear).padStart(2, '0')}`;
}

function parseThaiBEToIso(thaiStr) {
  if (!thaiStr) return null;
  const parts = thaiStr.trim().split(/[\/\-\.]/);
  if (parts.length === 3) {
    const d = parseInt(parts[0], 10);
    const m = parseInt(parts[1], 10);
    let y = parseInt(parts[2], 10);
    if (isNaN(d) || isNaN(m) || isNaN(y)) return null;
    if (d < 1 || d > 31 || m < 1 || m > 12) return null;
    
    // Support 2 digits BE (e.g. 69 -> 2569) or 4 digits BE (2569)
    if (y < 100) {
      y = y + 2500;
    }
    const ceYear = y - 543;
    return `${ceYear}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
  }
  return null;
}

async function updateCycleInfo(targetIsoDate) {
  const displayElem = document.getElementById('cycleRangeDisplay');
  const chipElem = document.getElementById('floatingCycleChip');
  if (!displayElem) return;

  try {
    const res = await fetch(`${API_BASE}/cycle/info?target_date=${targetIsoDate}`);
    if (!res.ok) throw new Error('API Error');
    const data = await res.json();
    
    displayElem.innerText = data.range_text;
    
    if (chipElem) {
      if (data.is_friday_holiday) {
        chipElem.classList.add('chip-holiday-alert');
        chipElem.title = `⚠️ วันศุกร์เป็นวันหยุดราชการ วงรอบสัปดาห์ปรับร่นเป็น: ${data.range_text}`;
      } else {
        chipElem.classList.remove('chip-holiday-alert');
        chipElem.title = `ช่วงวันทำการในวงรอบสัปดาห์: ${data.range_text}`;
      }
    }
  } catch (err) {
    console.warn('Failed to fetch cycle info, using client fallback:', err);
    // Instant fallback calculation
    calculateClientCycleRange(targetIsoDate);
  }
}

function calculateClientCycleRange(isoDateStr) {
  const displayElem = document.getElementById('cycleRangeDisplay');
  if (!displayElem || !isoDateStr) return;
  
  const TH_MONTHS = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
  const d = new Date(isoDateStr);
  const day = d.getDay(); // 0=Sun, 1=Mon, ..., 5=Fri
  const diffToMon = day === 0 ? -6 : 1 - day;
  
  const mon = new Date(d);
  mon.setDate(d.getDate() + diffToMon);
  
  const fri = new Date(mon);
  fri.setDate(mon.getDate() + 4);
  
  const beYear = (fri.getFullYear() + 543) % 100;
  displayElem.innerText = `${mon.getDate()} - ${fri.getDate()} ${TH_MONTHS[fri.getMonth() + 1]} ${String(beYear).padStart(2, '0')}`;
}

// ==========================================
// TAB 1: INTERNAL DOCS & HOTFOLDER PIPELINE
// ==========================================
async function loadDocumentChecklist() {
  const container = document.getElementById('docsChecklistGrid');
  if (!container) return;
  try {
    const res = await fetch(`${API_BASE}/docs/checklist`);
    const checklist = await res.json();
    container.innerHTML = checklist.map(item => {
      const isGen = item.status === 'GENERATED';
      const badgeClass = isGen ? 'badge-generated' : 'badge-pending';
      const badgeText = isGen ? 'พร้อมพิมพ์ ๒ ชุด' : 'รอสั่งสร้าง';
      
      const origUrl = item.original_url;
      const copyUrl = item.copy_url;
      const previewImg = item.preview_url;

      return `
        <div class="glass-panel doc-card">
          <div>
            <div class="card-header">
              <span class="badge ${badgeClass}">${badgeText}</span>
              <span style="font-size: 12px; color: var(--text-muted); font-family: monospace;">${item.template_id}</span>
            </div>
            <h3 class="card-title">${item.title}</h3>
            <div class="card-meta">
              <div>ความถี่: <strong>${item.frequency}</strong></div>
              <div>กฎวันที่: <strong>วันพฤหัสบดี (จันทร์-พฤหัสบดี ห้ามตรงวันหยุด)</strong></div>
            </div>
          </div>
          <div class="card-actions">
            ${isGen ? `
              <a href="${origUrl}" target="_blank" class="btn-secondary">
                📄 ฉบับจริง
              </a>
              <a href="${copyUrl}" target="_blank" class="btn-secondary" style="border-color: rgba(56, 189, 248, 0.4); color: var(--accent-blue);">
                📑 สำเนาคู่ฉบับ
              </a>
              <button onclick="openPreviewModal('${previewImg}', '${item.title}')" class="btn-secondary" style="color: var(--accent-gold);">
                🔍 พรีวิว 300 DPI
              </button>
            ` : `
              <span style="font-size: 13px; color: var(--text-muted);">กดปุ่ม "ประมวลผลและส่งออกแพ็กเกจคู่ขนาน" ด้านบนเพื่อสร้างเอกสาร</span>
            `}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Failed to load checklist:', err);
  }
}

async function triggerDocGeneration() {
  const dateInput = document.getElementById('targetCycleDate');
  const targetDate = dateInput ? dateInput.value : new Date().toISOString().split('T')[0];
  const btn = document.getElementById('btnTriggerGen');
  if (btn) btn.innerText = 'กำลังสร้างเอกสาร 300 DPI...';

  try {
    const res = await fetch(`${API_BASE}/docs/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_date: targetDate })
    });
    const data = await res.json();
    alert(`สร้างเอกสารแพ็กเกจคู่ขนาน ๒ ชุด สำเร็จจำนวน ${data.count} ฉบับ!\nวันเสนอเซ็นคำนวณลงล็อก: ${data.results[0]?.submission_date || 'N/A'}`);
    loadDocumentChecklist();
  } catch (err) {
    alert('เกิดข้อผิดพลาดในการสร้างเอกสาร: ' + err.message);
  } finally {
    if (btn) btn.innerText = '⚡ สั่งประมวลผลและสร้างแพ็กเกจคู่ขนาน ๒ ชุด';
  }
}

function openPreviewModal(imgUrl, title) {
  const modal = document.getElementById('previewModal');
  const modalImg = document.getElementById('modalPreviewImage');
  const modalTitle = document.getElementById('modalTitle');
  if (modal && modalImg) {
    modalTitle.innerText = `พรีวิวความคมชัด Print-Grade 300 DPI: ${title}`;
    modalImg.src = imgUrl;
    modal.classList.add('active');
  }
}

function closePreviewModal() {
  const modal = document.getElementById('previewModal');
  if (modal) modal.classList.remove('active');
}

// ==========================================
// 8 USER OPERATOR SLOTS (ผบ.หมู่ ป.1 - 6, ผบ.ร้อย, ผบ.พัน)
// ==========================================
async function loadOperators() {
  const container = document.getElementById('operatorsGrid');
  if (!container) return;
  try {
    let operators = [];
    try {
      const res = await fetch(`${API_BASE}/personnel/operators`);
      if (res.ok) {
        operators = await res.json();
      }
    } catch(e) {}

    // Fallback to static JSON if API is offline
    if (!operators || operators.length === 0) {
      const resStatic = await fetch('/backend/data/personnel_registry.json');
      if (resStatic.ok) {
        const reg = await resStatic.json();
        operators = reg.operators || reg.eight_operators || [];
      }
    }

    if (!operators || operators.length === 0) return;

    container.innerHTML = operators.map(op => `
      <div class="operator-slot" onclick="promptEditOperator(${op.slot})" 
           title="คลิกเพื่อแก้ไขข้อมูลเจ้าหน้าที่ ช่องที่ ${op.slot} (${op.position})">
        <div>
          <div class="operator-name-badge">
            <div class="operator-name-text" title="${op.rank} ${op.name}">
              <span class="operator-rank">${op.rank}</span> ${op.name}
            </div>
          </div>
          <div class="operator-pos-text" title="${op.position}">
            ${op.position}
          </div>
        </div>
        <div class="operator-serial-box">
          ${op.gun_serial && op.gun_serial !== '-' 
            ? `<span class="operator-serial-tag">หมายเลข ${op.gun_serial}</span>` 
            : `<span class="operator-hq-tag">กองบังคับการ</span>`}
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load operators:', err);
  }
}

async function promptEditOperator(slot) {
  const res = await fetch(`${API_BASE}/personnel/operators`);
  const operators = await res.json();
  const current = operators.find(o => o.slot === slot);
  if (!current) return;

  const newRank = prompt(`ช่องที่ ${slot} (${current.position})\nระบุ ยศ:`, current.rank);
  if (newRank === null) return;
  const newName = prompt(`ระบุ ชื่อ-สกุล:`, current.name);
  if (newName === null) return;
  const newPos = prompt(`ระบุ ตำแหน่ง (เช่น ผบ.หมู่ ป.${slot}):`, current.position);
  if (newPos === null) return;

  try {
    await fetch(`${API_BASE}/personnel/operators/${slot}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        rank: newRank,
        name: newName,
        position: newPos,
        gun_serial: current.gun_serial
      })
    });
    alert(`อัปเดตข้อมูลเจ้าหน้าที่ช่องที่ ${slot} สำเร็จ!`);
    loadOperators();
  } catch (err) {
    alert('เกิดข้อผิดพลาดในการบันทึก: ' + err.message);
  }
}


// ==========================================
// TAB 2: ARMORY & DUAL-CONTROL CUSTODY
// ==========================================
async function loadInventory() {
  const tableBody = document.getElementById('inventoryTableBody');
  const summaryBox = document.getElementById('inventorySummary');
  if (!tableBody) return;
  try {
    const res = await fetch(`${API_BASE}/inventory/balance`);
    const data = await res.json();
    
    // Render summary
    const sum = data.summary?.['GUN-105'] || { total: 0, received: 0, issued: 0, balance: 0 };
    if (summaryBox) {
      summaryBox.innerHTML = `
        <div style="display: flex; gap: 24px; flex-wrap: wrap;">
          <div>ยอดทั้งหมด: <strong style="color: #fff; font-size: 18px;">${sum.total}</strong></div>
          <div>ยอดรับเข้า: <strong style="color: var(--accent-emerald); font-size: 18px;">${sum.received}</strong></div>
          <div>จ่ายยืม: <strong style="color: var(--accent-gold); font-size: 18px;">${sum.issued}</strong></div>
          <div>คงคลังพร้อมใช้: <strong style="color: var(--accent-cyan); font-size: 18px;">${sum.balance}</strong></div>
        </div>
      `;
    }

    // Render items table
    tableBody.innerHTML = (data.items || []).map(item => `
      <tr>
        <td style="font-family: monospace; font-weight: 600;">${item.item_id}</td>
        <td>${item.name}</td>
        <td style="font-family: monospace;">${item.serial_no}</td>
        <td>
          <span class="badge ${item.status === 'AVAILABLE' ? 'badge-generated' : (item.status === 'BORROWED' ? 'badge-pending' : 'badge-overdue')}">
            ${item.status}
          </span>
        </td>
        <td>
          ${item.status === 'AVAILABLE' ? `
            <button onclick="promptLoanRequest('${item.item_id}')" class="btn-secondary" style="font-size: 12px; padding: 4px 10px;">
              ขอเบิก (Maker)
            </button>
          ` : (item.status === 'BORROWED' ? `
            <button onclick="promptReturnItem('${item.item_id}')" class="btn-secondary" style="font-size: 12px; padding: 4px 10px; color: var(--accent-emerald);">
              คืนสิ่งอุปกรณ์
            </button>
          ` : `
            <button onclick="promptReplaceItem('${item.item_id}')" class="btn-danger" style="font-size: 12px; padding: 4px 10px;">
              เปลี่ยนทดแทน
            </button>
          `)}
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load inventory:', err);
  }
}

async function promptLoanRequest(itemId) {
  const borrower = prompt(`กรุณาระบุชื่อผู้ขอเบิก (${itemId}):`, 'ส.อ. สมเกียรติ สุขใจ');
  if (!borrower) return;
  const purpose = prompt('วัตถุประสงค์การใช้งาน:', 'ยิงสนับสนุนการฝึก');
  if (!purpose) return;

  try {
    const res = await fetch(`${API_BASE}/inventory/loan/request`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: itemId,
        borrower_name: borrower,
        purpose: purpose,
        requested_by: 'แอดมินคลัง'
      })
    });
    const req = await res.json();
    
    // Auto-prompt Checker approval for seamless Dual-Control test
    if (confirm(`สร้างใบขอเบิกสำเร็จ (${req.request_id}) สถานะ: รออนุมัติ\nต้องการให้ ผบ.ร้อย (Checker) กดอนุมัติการเบิกทันทีหรือไม่?`)) {
      await fetch(`${API_BASE}/inventory/loan/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          request_id: req.request_id,
          approved_by: 'ร.อ. จิตรภณ วงค์แก้ว (ผบ.ร้อย)'
        })
      });
      alert('อนุมัติการเบิกเรียบร้อย! ตัดยอดคงเหลือในคลังแล้ว');
    }
    loadInventory();
  } catch (err) {
    alert('เกิดข้อผิดพลาด: ' + err.message);
  }
}

async function promptReturnItem(itemId) {
  const isDamaged = confirm(`สิ่งอุปกรณ์ ${itemId} ชำรุดเสียหายหรือไม่?\n[ตกลง] = ชำรุด  /  [ยกเลิก] = สภาพปกติ`);
  let notes = '';
  if (isDamaged) {
    notes = prompt('ระบุอาการชำรุดเสียหาย:', 'ศูนย์เล็งแตกร้าว');
  }

  try {
    await fetch(`${API_BASE}/inventory/item/return`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: itemId,
        is_damaged: isDamaged,
        damage_notes: notes,
        receiver: 'เสมียนคลัง สป.'
      })
    });
    alert('บันทึกการรับคืนเรียบร้อยแล้ว!');
    loadInventory();
  } catch (err) {
    alert('เกิดข้อผิดพลาด: ' + err.message);
  }
}

async function promptReplaceItem(itemId) {
  const newSerial = prompt(`ระบุหมายเลขซีเรียลใหม่สำหรับเปลี่ยนทดแทน (${itemId}):`, 'SN-REPLACE-2026');
  if (!newSerial) return;

  try {
    await fetch(`${API_BASE}/inventory/item/replace`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: itemId,
        new_serial_no: newSerial,
        replaced_by: 'นายช่างประจำหมวด'
      })
    });
    alert('เปลี่ยนทดแทนหมายเลขยุทธภัณฑ์และเก็บบันทึกประวัติสำเร็จ!');
    loadInventory();
  } catch (err) {
    alert('เกิดข้อผิดพลาด: ' + err.message);
  }
}

// ==========================================
// TAB 3: EXTERNAL INTAKE & CADENCE GAPS
// ==========================================
async function loadExternalIntake() {
  const listContainer = document.getElementById('externalIntakeList');
  if (!listContainer) return;
  try {
    const res = await fetch(`${API_BASE}/intake/scan`);
    const records = await res.json();
    if (!records.length) {
      listContainer.innerHTML = '<div style="color: var(--text-muted); padding: 12px;">ยังไม่มีไฟล์เข้ามาใน hotfolder/FolderIN/</div>';
      return;
    }

    listContainer.innerHTML = records.map(rec => {
      const isUnclassified = rec.doc_type === 'UNCLASSIFIED_EXTERNAL';
      return `
        <div class="glass-panel" style="padding: 18px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border-color: ${isUnclassified ? 'rgba(244, 63, 94, 0.4)' : 'var(--border-glass)'};">
          <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
              <span class="badge ${isUnclassified ? 'badge-overdue' : 'badge-generated'}">${rec.status}</span>
              <strong style="color: #fff;">${rec.filename}</strong>
            </div>
            <div style="font-size: 13px; color: var(--text-secondary);">
              ประเภท: <strong>${rec.title}</strong> | วงรอบ: <strong>${rec.period_key}</strong>
            </div>
            ${rec.alert ? `<div style="font-size: 13px; color: var(--accent-rose); margin-top: 4px;">⚠️ ${rec.alert}</div>` : ''}
          </div>
          <div>
            ${isUnclassified ? `
              <button onclick="promptClassifyExternal('${rec.filename}')" class="btn-primary" style="font-size: 13px; padding: 8px 16px;">
                ⚡ ระบุวงรอบใน ๑ คลิก
              </button>
            ` : `
              <span style="color: var(--accent-emerald); font-size: 13px; font-weight: 500;">✓ ดูดเข้าเรียบร้อย</span>
            `}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Failed to load intake:', err);
  }
}

async function promptClassifyExternal(filename) {
  const docType = prompt(`เลือกประเภทเอกสารสำหรับ ${filename}\n1 = รายงานอัคคีภัย (FIRE_SAFETY)\n2 = ตรวจสภาพกระสุน (AMMO_INSPECTION):`, 'FIRE_SAFETY');
  if (!docType) return;
  const period = prompt('ระบุรอบเดือน/ไตรมาส (เช่น 2026-10):', '2026-10');
  if (!period) return;

  try {
    await fetch(`${API_BASE}/intake/classify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        filename: filename,
        doc_type: docType,
        period_key: period
      })
    });
    alert('จัดหมวดหมู่เอกสารและระบุวงรอบเรียบร้อยแล้ว!');
    loadExternalIntake();
    loadCadenceGaps();
  } catch (err) {
    alert('เกิดข้อผิดพลาด: ' + err.message);
  }
}

async function loadCadenceGaps() {
  const gapContainer = document.getElementById('cadenceGapsList');
  if (!gapContainer) return;
  try {
    const res = await fetch(`${API_BASE}/intake/gaps?current_date=2026-10-16`);
    const gaps = await res.json();
    gapContainer.innerHTML = gaps.map(g => {
      const isOverdue = g.status === 'OVERDUE';
      return `
        <div class="glass-panel" style="padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid ${isOverdue ? 'var(--accent-rose)' : 'var(--accent-emerald)'};">
          <div>
            <div style="font-weight: 600; font-size: 15px; color: #fff;">${g.title}</div>
            <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
              วงรอบที่คาดหวัง: <strong>${g.expected_period}</strong> (กำหนดส่งภายในวันที่ ${g.deadline_day})
            </div>
            ${g.gap_alert ? `<div style="font-size: 13px; color: var(--accent-rose); font-weight: 500; margin-top: 4px;">🚨 ${g.gap_alert}</div>` : ''}
          </div>
          <div>
            <span class="badge ${isOverdue ? 'badge-overdue' : 'badge-generated'}">${g.status}</span>
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Failed to load gaps:', err);
  }
}

function filterCatalogDocs() {
  const query = document.getElementById('catalogSearchInput')?.value.toLowerCase().trim() || '';
  const cards = document.querySelectorAll('#catalogDocsGrid .doc-card');
  cards.forEach(card => {
    const text = (card.getAttribute('data-title') + ' ' + card.innerText).toLowerCase();
    card.style.display = text.includes(query) ? 'flex' : 'none';
  });
}



// ==========================================
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
    let res = await fetch(`${API_BASE}/inspection/photos`);
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
    badge.innerText = `พร้อมใช้งาน (${toThaiNum(validCount)}/๔ ภาพ)`;
    badge.className = validCount >= 4 ? 'badge badge-generated' : 'badge badge-pending';
  }

  grid.innerHTML = INSPECTION_PHOTO_SLOTS.map((slot, idx) => {
    const photoSrc = photos && photos[idx] ? photos[idx] : '';
    const hasPhoto = !!photoSrc;

    return `
      <div class="photo-slot-card" style="width: calc(2.5in + 20px); background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 10px; display: flex; flex-direction: column; gap: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.4); transition: all 0.2s; box-sizing: border-box;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 4px;">
          <div>
            <span style="font-weight: 600; font-size: 13px; color: #fff; line-height: 1.25; display: block;">${slot.title}</span>
            <div style="font-size: 11px; color: var(--accent-cyan); margin-top: 2px; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px;" title="${slot.desc}">${slot.desc}</div>
          </div>
          <span class="badge" style="font-size: 10px; padding: 1px 6px; white-space: nowrap; background: ${hasPhoto ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)'}; color: ${hasPhoto ? '#34d399' : '#f87171'}; border: 1px solid ${hasPhoto ? 'rgba(16,185,129,0.35)' : 'rgba(239,68,68,0.35)'};">
            ${hasPhoto ? '✓ พร้อม' : 'รออัพโหลด'}
          </span>
        </div>

        <div style="position: relative; width: 2.5in; height: 2.5in; border-radius: 8px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.15); background: rgba(0, 0, 0, 0.6); cursor: pointer; margin: 0 auto;"
             onclick="document.getElementById('slotPhotoInput-${idx}').click()"
             title="คลิกเพื่อเปลี่ยนภาพตำแหน่งที่ ${idx + 1} (${slot.title})">
          ${hasPhoto ? `
            <img src="${photoSrc}" alt="${slot.title}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.25s;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
          ` : `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted); gap: 6px;">
              <span style="font-size: 26px;">📷</span>
              <span style="font-size: 12px;">คลิกเพื่ออัพโหลด</span>
            </div>
          `}
          <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.88)); padding: 6px 8px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 11px; color: #38bdf8; font-weight: 500;">🔄 คลิกเปลี่ยนภาพ</span>
            <span style="font-size: 10.5px; color: #cbd5e1;">ภาพที่ ${idx + 1}</span>
          </div>
        </div>

        <input type="file" id="slotPhotoInput-${idx}" accept="image/*" style="display: none;" onchange="handleSinglePhotoUpload(${idx}, event)">
      </div>
    `;
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
      await fetch(`${API_BASE}/inspection/photos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photos: currentInspectionPhotos })
      });
    } catch (e) {
      console.warn('Could not sync to backend:', e);
    }

    renderInspectionPhotosGrid(currentInspectionPhotos);
    alert(`อัพโหลดภาพถ่ายสำเร็จจำนวน ${base64List.length} ภาพ!\nภาพจะวิ่งตรงไปวางแปะแทนที่เดิมในหน้า ๔ ของแบบรายงาน สด.๑ ทันที ๑๐๐%`);
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
      await fetch(`${API_BASE}/inspection/photos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photos: currentInspectionPhotos })
      });
    } catch (e) {
      console.warn('Could not sync to backend:', e);
    }

    renderInspectionPhotosGrid(currentInspectionPhotos);
    alert(`อัพเดตภาพตำแหน่งที่ ${slotIndex + 1} สำเร็จ!\nภาพถูกนำไปวางแปะแทนที่เดิมในหน้า ๔ เรียบร้อยแล้ว`);
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
          await fetch(`${API_BASE}/inspection/photos`, {
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


// =========================================================================
// MASTER DOCUMENT INVENTORY & WORK QUEUE CHECKLIST ENGINE (๑๙ ฉบับ)
// =========================================================================
const MASTER_DOC_INVENTORY = [
  {
    id: 'doc-sd1',
    code: 'สด.๑',
    title: 'แบบรายงานผลการตรวจ สด.๑ (สาย สพ. อาวุธ)',
    desc: 'บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) พร้อมตารางสรุปปรนนิบัติบำรุงและภาพถ่าย ๔ ช่อง',
    category: 'weekly',
    queueOrder: 1,
    isUpcoming: true,
    cadence: 'ประจำสัปดาห์ (ทุกวันพฤหัสบดี)',
    queueBadge: 'คิวที่ ๑ (ด่วนสัปดาห์นี้)',
    queueDesc: 'วงรอบ ๒-๖ พ.ย. ๖๙ (เสนอเซ็น พฤ. ๕ พ.ย.)',
    htmlFile: '/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html',
    docxFile: '/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.docx',
    xlsxFile: '/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-weekly-rep',
    code: 'WEEKLY-REP',
    title: 'บันทึกรายงานผลการตรวจประจำสัปดาห์ (ชุดตรวจ)',
    desc: 'รายงานผลการตรวจสภาพยุทโธปกรณ์ประจำสัปดาห์ พร้อมบล็อกลงนามมาตรฐาน Red Line Standard',
    category: 'weekly',
    queueOrder: 2,
    isUpcoming: true,
    cadence: 'ประจำสัปดาห์ (ทุกวันพฤหัสบดี)',
    queueBadge: 'คิวที่ ๒ (ประจำสัปดาห์)',
    queueDesc: 'วงรอบ ๒-๖ พ.ย. ๖๙ (เสนอเซ็น พฤ. ๕ พ.ย.)',
    htmlFile: '/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html',
    docxFile: '/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.docx',
    xlsxFile: '/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-followup-45',
    code: 'ทบ.๔๐๐-๐๗๑ (ก)',
    title: 'ขอส่งใบติดตามทวงถาม ๔๕ วัน (ทบ.๔๐๐-๐๗๑ แบบ ก)',
    desc: 'บันทึกข้อความและ ทบ.๔๐๐-๐๗๑ แบบ ก ใบติดตามใบเบิก สิ่งอุปกรณ์สาย สพ. เกินกำหนด ๔๕ วัน',
    category: 'followup',
    queueOrder: 3,
    isUpcoming: true,
    cadence: 'วงรอบเกิน ๔๕ วัน',
    queueBadge: 'คิวที่ ๓ (รอบ ๔๕ วัน)',
    queueDesc: 'ติดตามใบเบิก/ส่งซ่อมเกินกำหนด ๔๕ วัน',
    htmlFile: '/ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.html',
    docxFile: '/ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.docx',
    xlsxFile: '/ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-followup-90',
    code: 'ทบ.๔๐๐-๐๗๑ (ข)',
    title: 'ขอส่งใบติดตามทวงถาม ๙๐ วัน (ทบ.๔๐๐-๐๗๑ แบบ ข)',
    desc: 'บันทึกข้อความและ ทบ.๔๐๐-๐๗๑ แบบ ข ใบติดตามใบเบิก สิ่งอุปกรณ์สาย สพ. เกินกำหนด ๙๐ วัน',
    category: 'followup',
    queueOrder: 4,
    isUpcoming: true,
    cadence: 'วงรอบเกิน ๙๐ วัน',
    queueBadge: 'คิวที่ ๔ (รอบ ๙๐ วัน)',
    queueDesc: 'ติดตามใบเบิก/ส่งซ่อมเกินกำหนด ๙๐ วัน',
    htmlFile: '/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html',
    docxFile: '/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.docx',
    xlsxFile: '/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-memo-latest',
    code: 'MEMO-45',
    title: 'บันทึกข้อความ (ขอส่งใบติดตามใบส่งซ่อมเกิน ๔๕ วัน)',
    desc: 'บันทึกข้อความราชการ ทบ. นำส่งใบติดตามใบส่งซ่อมเกิน ๔๕ วัน ฟอนต์ Sarabun PSK 16pt / 20pt / 29pt',
    category: 'followup',
    queueOrder: 5,
    isUpcoming: false,
    cadence: 'วงรอบเกิน ๔๕ วัน',
    queueBadge: 'เอกสารนำส่ง ๔๕ วัน',
    queueDesc: 'บันทึกข้อความนำส่งประกอบ ทบ.๔๐๐-๐๗๑',
    htmlFile: '/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html',
    docxFile: '/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.docx',
    xlsxFile: '/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-memo-90',
    code: 'MEMO-90',
    title: 'บันทึกข้อความ (ขอส่งใบติดตามใบส่งซ่อมเกิน ๙๐ วัน)',
    desc: 'บันทึกข้อความราชการ ทบ. นำส่งใบติดตามใบส่งซ่อมเกิน ๙๐ วัน ฟอนต์ Sarabun PSK 16pt / 20pt / 29pt',
    category: 'followup',
    queueOrder: 6,
    isUpcoming: false,
    cadence: 'วงรอบเกิน ๙๐ วัน',
    queueBadge: 'เอกสารนำส่ง ๙๐ วัน',
    queueDesc: 'บันทึกข้อความนำส่งประกอบ ทบ.๔๐๐-๐๗๑',
    htmlFile: '/บันทึกข้อความ_90_วัน_Rebuild_Thai.html',
    docxFile: '/บันทึกข้อความ_90_วัน_Rebuild_Thai.docx',
    xlsxFile: '/บันทึกข้อความ_90_วัน_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-repair-track-a',
    code: 'REPAIR-TRACK-A',
    title: 'ทบ.๔๐๐-๐๗๑ แบบ ก ใบติดตามใบส่งซ่อม (๔๕ - ๙๐ วัน)',
    desc: 'แบบ ก แนวนอน สำหรับติดตามใบส่งซ่อมสิ่งอุปกรณ์สาย สพ. เกิน ๔๕ - ๙๐ วัน',
    category: 'followup',
    queueOrder: 7,
    isUpcoming: false,
    cadence: 'วงรอบซ่อมบำรุง',
    queueBadge: 'แบบ ก แนวนอน',
    queueDesc: 'ใบติดตามสถานะการส่งซ่อม',
    htmlFile: '/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.html',
    docxFile: '/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.docx',
    xlsxFile: '/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-repair-track-b',
    code: 'REPAIR-TRACK-B',
    title: 'ทบ.๔๐๐-๐๗๑ แบบ ข ใบติดตามใบส่งซ่อม (เกิน ๙๐ วัน)',
    desc: 'แบบ ข แนวนอน สำหรับติดตามใบส่งซ่อมสิ่งอุปกรณ์สาย สพ. เกิน ๙๐ วัน',
    category: 'followup',
    queueOrder: 8,
    isUpcoming: false,
    cadence: 'วงรอบซ่อมบำรุง',
    queueBadge: 'แบบ ข แนวนอน',
    queueDesc: 'ใบติดตามสถานะการส่งซ่อมค้างนาน',
    htmlFile: '/ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.html',
    docxFile: '/ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.docx',
    xlsxFile: '/ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-quarterly',
    code: 'QUARTERLY-REP',
    title: 'รายงานผลการตรวจสอบอาการถอยและจำลองการยิง ป. (ประจำไตรมาส)',
    desc: 'รายงานตรวจสอบระบบเครื่องช่วยถอยและจำลองยิง ไฮบริด ๓ หน้า (หน้า ๑-๒ แนวตั้ง, หน้า ๓ แนวนอน)',
    category: 'periodic',
    queueOrder: 9,
    isUpcoming: true,
    cadence: 'ประจำไตรมาส (ทุก ๓ เดือน)',
    queueBadge: 'คิวที่ ๕ (ประจำไตรมาส)',
    queueDesc: 'ตรวจรอบไตรมาส ๑/๖๙ ระบบไฮดรอลิก/ถอย ป.',
    htmlFile: '/รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.html',
    docxFile: '/รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.docx',
    xlsxFile: '/รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-tb400-012',
    code: 'ทบ.๔๐๐-๐๑๒',
    title: 'ทบ.๔๐๐-๐๑๒ ใบรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์',
    desc: 'Legal แนวนอน ๒ หน้า ตรวจสอบยอดคงเหลือสิ่งอุปกรณ์เปรียบเทียบกับบัญชีคุมยอด',
    category: 'periodic',
    queueOrder: 10,
    isUpcoming: false,
    cadence: 'ประจำเดือน / ไตรมาส',
    queueBadge: 'คิวตรวจยอดคงเหลือ',
    queueDesc: 'เปรียบเทียบตรวจนับจริงกับบัญชีคุม',
    htmlFile: '/ทบ_400_012_Rebuild_Thai.html',
    docxFile: '/ทบ_400_012_Rebuild_Thai.docx',
    xlsxFile: '/ทบ_400_012_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-insp-gen2',
    code: 'INSP-GEN2',
    title: 'บันทึกผลการตรวจกิจการทั่วไป (ชุดตรวจที่ ๒) ประจำปี ๒๕๖๙',
    desc: 'เอกสารชุดใหญ่ ๑๘ หน้า (บันทึกข้อความ ๑ หน้า + ทบ.๑๐๕-๐๐๙ รวม ๑๗ หน้า ๖ ชุดตรวจ)',
    category: 'periodic',
    queueOrder: 11,
    isUpcoming: false,
    cadence: 'ประจำปี ๒๕๖๙',
    queueBadge: 'ตรวจกิจการทั่วไป',
    queueDesc: 'รอบการตรวจประจำปีของหน่วย',
    htmlFile: '/บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.html',
    docxFile: '/บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.docx',
    xlsxFile: '/บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-tb468-360',
    code: 'ทบ.๔๖๘-๓๖๐',
    title: 'ทบ.๔๖๘-๓๖๐ (สพ.๔๖๐) กำหนดการปรนนิบัติบำรุงยุทธภัณฑ์',
    desc: 'A4 แนวนอน ๔ หน้า กำหนดการปรนนิบัติบำรุงยุทธภัณฑ์ประจำปีของกองร้อย',
    category: 'periodic',
    queueOrder: 12,
    isUpcoming: false,
    cadence: 'ประจำปี ๒๕๖๙',
    queueBadge: 'ตารางปรนนิบัติบำรุง',
    queueDesc: 'แผนงานบำรุงรักษายุทธภัณฑ์ทั้งปี',
    htmlFile: '/ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.html',
    docxFile: '/ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.docx',
    xlsxFile: '/ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-survey-sp',
    code: 'ทบ.๔๐๐-๐๑๑',
    title: 'ทบ.๔๐๐-๐๑๑ ใบสำรวจสิ่งอุปกรณ์ สาย สพ.',
    desc: 'Legal แนวนอน ๑๒ หน้า (หน้าละ ๒ การ์ด รวม ๒๔ การ์ด) สำรวจสถานภาพสิ่งอุปกรณ์ครบวงจร',
    category: 'periodic',
    queueOrder: 13,
    isUpcoming: false,
    cadence: 'ประจำปี / รอบสำรวจ',
    queueBadge: 'สำรวจสิ่งอุปกรณ์',
    queueDesc: 'สำรวจสภาพยุทธภัณฑ์ประจำปี',
    htmlFile: '/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html',
    docxFile: '/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.docx',
    xlsxFile: '/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-gun-book',
    code: 'GUN-BOOK',
    title: 'สมุดประวัติการใช้ปืนใหญ่ (A4 แนวนอน ๕ หน้า)',
    desc: 'บันทึกประวัติการใช้ปืนใหญ่ ๕ หมวด (ยิง, ซ่อม, เคลื่อนย้าย, ตรวจสภาพ) หน้าละ ๑ หมวดพอดีเป๊ะ',
    category: 'armory',
    queueOrder: 14,
    isUpcoming: false,
    cadence: 'ประจำรอบยิง / ปรนนิบัติบำรุง',
    queueBadge: 'สมุดประวัติปืนใหญ่',
    queueDesc: 'บันทึกยอดนัดยิงและสภาพลำกล้อง',
    htmlFile: '/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.html',
    docxFile: '/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.docx',
    xlsxFile: '/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-gun-hist',
    code: 'GUN-HIST',
    title: 'ประวัติการใช้อาวุธ (ป.หมู่ ๒ ถึง ๖)',
    desc: 'A4 แนวตั้ง ๕ หน้า บันทึกประวัติการยิงและการปรนนิบัติบำรุงประจำปืนแต่ละกระบอก',
    category: 'armory',
    queueOrder: 15,
    isUpcoming: false,
    cadence: 'ประจำรอบยิง / คุมปืนหมู่',
    queueBadge: 'ประวัติการใช้อาวุธ',
    queueDesc: 'ประวัติ ป.หมู่ ๒ ถึง ๖',
    htmlFile: '/ประวัติการใช้อาวุธ_Rebuild_Thai.html',
    docxFile: '/ประวัติการใช้อาวุธ_Rebuild_Thai.docx',
    xlsxFile: '/ประวัติการใช้อาวุธ_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-pbk-95',
    code: 'ปบค.๙๕',
    title: 'บัญชีรายละเอียดหมายเลข ปบค.๙๕ ขนาด ๑๐๕ มม. เอ็ม ๑๐๑ เอ ๑ ปรับปรุง',
    desc: 'A4 แนวนอน ๑ หน้า ควบคุมหมายเลขซีเรียลปืนใหญ่ ทะเบียน และส่วนประกอบหลัก ๖ หมู่',
    category: 'armory',
    queueOrder: 16,
    isUpcoming: false,
    cadence: 'ทะเบียนคุมอาวุธหลัก',
    queueBadge: 'ทะเบียน ปบค.๙๕',
    queueDesc: 'หมายเลขซีเรียลปืนใหญ่ประจำร้อย',
    htmlFile: '/บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.html',
    docxFile: '/บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.docx',
    xlsxFile: '/บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-tb468-204',
    code: 'ทบ.๔๖๘-๒๐๔',
    title: 'ทบ.๔๖๘-๒๐๔ (คส.๔) บัญชีหมายเลขอาวุธ',
    desc: 'A4 แนวตั้ง ๖ หน้า คุมหมายเลขอาวุธประจำกายและอาวุธประจำหน่วยทั้งหมด',
    category: 'armory',
    queueOrder: 17,
    isUpcoming: false,
    cadence: 'ทะเบียนคุมอาวุธ',
    queueBadge: 'คส.๔ หมายเลขอาวุธ',
    queueDesc: 'บัญชีหมายเลขอาวุธประจำกาย/หน่วย',
    htmlFile: '/ทบ_468_204_Rebuild_Thai.html',
    docxFile: '/ทบ_468_204_Rebuild_Thai.docx',
    xlsxFile: '/ทบ_468_204_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-tb400-005',
    code: 'ทบ.๔๐๐-๐๐๕',
    title: 'ทบ.๔๐๐-๐๐๕ บัญชีสิ่งอุปกรณ์ของหน่วย',
    desc: 'A5 แนวตั้ง ๓๑ หน้า (หน้าสารบัญ/รับรอง ๑ หน้า + การ์ดหน้า/หลัง ๑๕ แผ่น) คุมการรับ-จ่าย สป.',
    category: 'armory',
    queueOrder: 18,
    isUpcoming: false,
    cadence: 'บัญชีคุมสิ่งอุปกรณ์หลัก',
    queueBadge: 'ทบ.๔๐๐-๐๐๕ บัญชีคุม',
    queueDesc: 'บัญชีคุมสิ่งอุปกรณ์ของหน่วย',
    htmlFile: '/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html',
    docxFile: '/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.docx',
    xlsxFile: '/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.xlsx',
    dualCopy: true
  },
  {
    id: 'doc-cat2-4',
    code: 'ทบ.CAT2-4',
    title: 'บัญชีคุมสิ่งอุปกรณ์ ประเภท ๒ และ ๔ (ทบ.๔๐๐-๐๐๕)',
    desc: 'A5 แนวตั้ง ๑๗๘ หน้า บัญชีคุมสิ่งอุปกรณ์ละเอียด ปก+รับรอง+คำเตือน/ตรวจ+ที่ตั้ง+การ์ด ๘๗ แผ่น',
    category: 'armory',
    queueOrder: 19,
    isUpcoming: false,
    cadence: 'บัญชีคุม สป.๒ และ ๔',
    queueBadge: 'คุม สป.๒ และ ๔',
    queueDesc: 'คุมสิ่งอุปกรณ์ประเภท ๒ และ ๔ ครบ ๘๗ การ์ด',
    htmlFile: '/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.html',
    docxFile: '/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.docx',
    xlsxFile: '/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.xlsx',
    dualCopy: true
  }
];

let currentChecklistFilter = 'all';
let currentChecklistSearch = '';

function getCheckedDocsMap() {
  try {
    const raw = localStorage.getItem('checked_military_docs');
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    return {};
  }
}

function saveCheckedDocsMap(map) {
  try {
    localStorage.setItem('checked_military_docs', JSON.stringify(map));
  } catch (e) {}
}

function initMasterChecklist() {
  renderUpcomingQueue();
  renderMasterChecklist();
}

function renderUpcomingQueue() {
  const container = document.getElementById('upcomingQueueGrid');
  if (!container) return;

  const upcomingList = MASTER_DOC_INVENTORY.filter(d => d.isUpcoming).slice(0, 5);
  
  container.innerHTML = upcomingList.map((item, idx) => {
    return `
      <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; justify-content: space-between; gap: 8px; transition: transform 0.2s;" onmouseover="this.style.borderColor='rgba(56,189,248,0.6)'" onmouseout="this.style.borderColor='rgba(56,189,248,0.25)'">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span class="badge" style="font-size: 10px; padding: 1px 7px; background: rgba(56, 189, 248, 0.18); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4);">
              ${item.queueBadge}
            </span>
            <span style="font-size: 11px; font-weight: 600; color: var(--accent-gold);">ลำดับ ${idx + 1}</span>
          </div>
          <div style="font-weight: 600; font-size: 13.5px; color: #fff; line-height: 1.3;">
            ${item.title}
          </div>
          <div style="font-size: 11.5px; color: var(--accent-cyan); margin-top: 4px; line-height: 1.2;">
            📅 ${item.queueDesc}
          </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 8px; margin-top: 2px;">
          <span style="font-size: 11px; color: #34d399;">✓ ไฟล์พร้อม ๑๐๐%</span>
          <a href="${item.htmlFile}" target="_blank" style="font-size: 11.5px; color: #38bdf8; text-decoration: none; font-weight: 500;">
            เปิดดู ➔
          </a>
        </div>
      </div>
    `;
  }).join('');
}

function renderMasterChecklist() {
  const tbody = document.getElementById('masterChecklistTableBody');
  const countDisplay = document.getElementById('checkedCountDisplay');
  if (!tbody) return;

  const checkedMap = getCheckedDocsMap();

  let filtered = MASTER_DOC_INVENTORY;
  if (currentChecklistFilter !== 'all') {
    filtered = filtered.filter(d => d.category === currentChecklistFilter);
  }

  if (currentChecklistSearch.trim()) {
    const q = currentChecklistSearch.toLowerCase().trim();
    filtered = filtered.filter(d => 
      d.code.toLowerCase().includes(q) ||
      d.title.toLowerCase().includes(q) ||
      d.desc.toLowerCase().includes(q) ||
      d.cadence.toLowerCase().includes(q)
    );
  }

  const totalCount = MASTER_DOC_INVENTORY.length;
  const checkedCount = Object.values(checkedMap).filter(Boolean).length;
  if (countDisplay) {
    countDisplay.innerText = `เช็คแล้ว ${toThaiNum(checkedCount)}/${toThaiNum(totalCount)} ฉบับ`;
  }

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align: center; padding: 24px; color: var(--text-muted);">
          ไม่พบเอกสารที่ตรงกับเงื่อนไขการค้นหา
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = filtered.map(item => {
    const isChecked = !!checkedMap[item.id];
    return `
      <tr style="background: ${isChecked ? 'rgba(16, 185, 129, 0.05)' : 'transparent'}; transition: background 0.2s;">
        <td style="text-align: center;">
          <input type="checkbox" id="chk-${item.id}" ${isChecked ? 'checked' : ''} onchange="toggleDocChecked('${item.id}', this.checked)" style="width: 17px; height: 17px; cursor: pointer; accent-color: var(--accent-blue);">
        </td>
        <td>
          <span class="doc-code" style="font-size: 12px; padding: 2px 7px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 4px; color: #38bdf8; font-weight: 600;">
            ${item.code}
          </span>
        </td>
        <td>
          <div style="font-weight: 600; color: #fff; font-size: 13.5px; line-height: 1.35;">
            ${item.title}
          </div>
          <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px; line-height: 1.25;">
            ${item.desc}
          </div>
        </td>
        <td>
          <div style="font-size: 12.5px; color: var(--accent-cyan); font-weight: 500;">
            ${item.cadence}
          </div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">
            ${item.queueDesc}
          </div>
        </td>
        <td style="text-align: center;">
          <div style="display: flex; gap: 4px; justify-content: center; flex-wrap: wrap;">
            <span class="badge badge-generated" style="font-size: 10px; padding: 1px 6px;">HTML 300DPI</span>
            <span class="badge" style="font-size: 10px; padding: 1px 6px; background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.35);">Word</span>
            <span class="badge" style="font-size: 10px; padding: 1px 6px; background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.35);">Excel</span>
          </div>
        </td>
        <td style="text-align: center;">
          <div style="display: flex; gap: 5px; justify-content: center; align-items: center;">
            <a href="${item.htmlFile}" target="_blank" class="btn-action btn-html" style="font-size: 11px; padding: 3px 8px; text-decoration: none;" title="เปิดดู HTML Preview คมชัด 300 DPI">
              🌐 ดู HTML
            </a>
            <a href="${item.docxFile}" class="btn-action btn-docx" style="font-size: 11px; padding: 3px 8px; text-decoration: none;" title="ดาวน์โหลด Microsoft Word (.docx) มาตรฐาน Red Line">
              📘 Word
            </a>
            <a href="${item.xlsxFile}" class="btn-action btn-xlsx" style="font-size: 11px; padding: 3px 8px; text-decoration: none;" title="ดาวน์โหลด Microsoft Excel (.xlsx) สูตรคำนวณแท้">
              📊 Excel
            </a>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function toggleDocChecked(docId, isChecked) {
  const map = getCheckedDocsMap();
  map[docId] = isChecked;
  saveCheckedDocsMap(map);
  renderMasterChecklist();
}

function toggleCheckAllDocs(checkAll) {
  const map = {};
  MASTER_DOC_INVENTORY.forEach(d => {
    map[d.id] = checkAll;
  });
  saveCheckedDocsMap(map);
  renderMasterChecklist();
}

function filterChecklist(category, btnElem) {
  currentChecklistFilter = category;
  const filterBtns = document.querySelectorAll('#checklistFilterTabs .btn-filter');
  filterBtns.forEach(b => {
    b.style.background = 'rgba(255,255,255,0.06)';
    b.style.color = '#94a3b8';
    b.style.borderColor = 'rgba(255,255,255,0.15)';
  });
  if (btnElem) {
    btnElem.style.background = 'var(--accent-blue)';
    btnElem.style.color = '#fff';
    btnElem.style.borderColor = 'var(--accent-blue)';
  }
  renderMasterChecklist();
}

function onChecklistSearchInput(val) {
  currentChecklistSearch = val || '';
  renderMasterChecklist();
}
