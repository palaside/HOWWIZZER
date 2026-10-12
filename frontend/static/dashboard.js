// Tactical Military Document & Custody Management Dashboard
const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initDateDefaults();
  loadDocumentChecklist();
  loadOperators();
  loadInventory();
  loadExternalIntake();
  loadCadenceGaps();
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
  if (targetDateInput) {
    const today = new Date();
    targetDateInput.value = today.toISOString().split('T')[0];
  }
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
    const res = await fetch(`${API_BASE}/personnel/operators`);
    const operators = await res.json();
    container.innerHTML = operators.map(op => `
      <div class="operator-slot" onclick="promptEditOperator(${op.slot})" 
           style="background: rgba(0, 0, 0, 0.4); padding: 14px 10px; border-radius: 12px; border: 1px solid var(--border-glass); text-align: center; cursor: pointer; transition: all 0.2s;"
           title="คลิกเพื่อแก้ไขข้อมูลเจ้าหน้าที่ ช่องที่ ${op.slot}">
        <div style="font-size: 12px; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px;">
          ${op.position}
        </div>
        <div style="font-size: 16px; font-weight: 700; color: #ffffff; line-height: 1.2;">
          ${op.rank}
        </div>
        <div style="font-size: 13.5px; font-weight: 500; color: var(--text-primary); margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          ${op.name}
        </div>
        <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
          ${op.gun_serial && op.gun_serial !== '-' 
            ? `<span style="background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; color: var(--text-secondary);">หมายเลข ${op.gun_serial}</span>` 
            : `<span style="color: var(--accent-blue); font-size: 11px;">กองบังคับการ</span>`}
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
