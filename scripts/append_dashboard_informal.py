"""
Appends Informal Equipment Survey module logic to frontend/static/dashboard.js
"""
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_JS = WORKSPACE_ROOT / "frontend" / "static" / "dashboard.js"

def update_js():
    content = DASHBOARD_JS.read_text(encoding="utf-8")

    # 1. Update DOMContentLoaded
    if "initInformalSurvey();" not in content:
        content = content.replace(
            "  initMasterChecklist();\n});",
            "  initMasterChecklist();\n  initInformalSurvey();\n});"
        )
        print("Updated DOMContentLoaded with initInformalSurvey.")

    # 2. Append Informal Survey Implementation
    informal_code = '''

// =============================================================================
// TAB 5: INFORMAL EQUIPMENT SURVEY & LOAN/DAMAGE MANAGEMENT
// =============================================================================
let informalInventoryData = null;
let currentInformalSection = 'gun_shed'; // 'gun_shed' | 'hq_warehouse' | 'loans_history'
let currentInformalSearch = '';

async function initInformalSurvey() {
  await loadInformalInventoryData();
  renderInformalSurveyUI();
  checkOverdueLoansOnLoad();
}

async function loadInformalInventoryData() {
  try {
    const res = await fetch(`${API_BASE}/informal-equipment`);
    if (res.ok) {
      informalInventoryData = await res.json();
      localStorage.setItem('informal_inventory_db', JSON.stringify(informalInventoryData));
      return;
    }
  } catch (err) {
    console.warn('API /informal-equipment offline, trying static JSON fallback:', err);
  }

  // Fallback 1: LocalStorage
  const cached = localStorage.getItem('informal_inventory_db');
  if (cached) {
    try {
      informalInventoryData = JSON.parse(cached);
      return;
    } catch(e) {}
  }

  // Fallback 2: Static JSON file
  try {
    const resStatic = await fetch('/backend/data/informal_equipment_inventory.json');
    if (resStatic.ok) {
      const data = await resStatic.json();
      // compute stats
      const s1 = data.sections.gun_shed.items;
      const s2 = data.sections.hq_warehouse.items;
      informalInventoryData = {
        metadata: data.metadata,
        stats: {
          gun_shed: {
            total_items: s1.length,
            physical_sum: s1.reduce((acc, i) => acc + (i.physical_amount || 0), 0),
            loan_sum: s1.reduce((acc, i) => acc + (i.loan_amount || 0), 0),
            repair_sum: s1.reduce((acc, i) => acc + (i.repair_amount || 0), 0),
            balance_sum: s1.reduce((acc, i) => acc + (i.balance_amount || 0), 0),
          },
          hq_warehouse: {
            total_items: s2.length,
            physical_sum: s2.reduce((acc, i) => acc + (i.physical_amount || 0), 0),
            loan_sum: s2.reduce((acc, i) => acc + (i.loan_amount || 0), 0),
            repair_sum: s2.reduce((acc, i) => acc + (i.repair_amount || 0), 0),
            balance_sum: s2.reduce((acc, i) => acc + (i.balance_amount || 0), 0),
          },
          active_loans_count: (data.loans || []).filter(l => l.status === 'borrowed').length,
          overdue_loans_count: 0
        },
        sections: data.sections,
        loans: data.loans || []
      };
      localStorage.setItem('informal_inventory_db', JSON.stringify(informalInventoryData));
    }
  } catch (err) {
    console.error('Failed to load informal inventory:', err);
  }
}

function renderInformalSurveyUI() {
  if (!informalInventoryData) return;

  const stats = informalInventoryData.stats || {};
  const s1 = stats.gun_shed || {};
  const s2 = stats.hq_warehouse || {};
  const loans = informalInventoryData.loans || [];

  const totalPhysical = (s1.physical_sum || 0) + (s2.physical_sum || 0);
  const totalLoan = (s1.loan_sum || 0) + (s2.loan_sum || 0);
  const totalRepair = (s1.repair_sum || 0) + (s2.repair_sum || 0);
  const totalBalance = (s1.balance_sum || 0) + (s2.balance_sum || 0);

  // Update quick metrics
  const metricPhysical = document.getElementById('metricPhysicalTotal');
  const metricLoan = document.getElementById('metricLoanTotal');
  const metricRepair = document.getElementById('metricRepairTotal');
  const metricBalance = document.getElementById('metricBalanceTotal');
  const loanBadge = document.getElementById('loanListBadge');

  if (metricPhysical) metricPhysical.innerText = `${toThaiNum(totalPhysical)} รายการ`;
  if (metricLoan) metricLoan.innerText = `${toThaiNum(totalLoan)}`;
  if (metricRepair) metricRepair.innerText = `${toThaiNum(totalRepair)}`;
  if (metricBalance) metricBalance.innerText = `${toThaiNum(totalBalance)} รายการ`;
  if (loanBadge) loanBadge.innerText = toThaiNum(loans.length);

  // Check Overdue count
  const today = new Date().toISOString().split('T')[0];
  const overdueCount = loans.filter(l => l.status === 'borrowed' && l.expected_return_date && l.expected_return_date < today).length;
  const overdueBadge = document.getElementById('overdueCountBadge');
  const overdueBtn = document.getElementById('btnOverdueAlertsBadge');
  if (overdueBadge) overdueBadge.innerText = toThaiNum(overdueCount);
  if (overdueBtn) {
    if (overdueCount > 0) {
      overdueBtn.style.animation = 'pulse 2s infinite alternate';
    } else {
      overdueBtn.style.animation = 'none';
    }
  }

  // Render active section
  if (currentInformalSection === 'loans_history') {
    renderInformalLoansTable();
  } else {
    renderInformalTable();
  }
}

function switchInformalSection(sectionKey) {
  currentInformalSection = sectionKey;
  
  const btnGunShed = document.getElementById('btnSecGunShed');
  const btnHq = document.getElementById('btnSecHqWarehouse');
  const btnLoans = document.getElementById('btnSecLoans');
  const invContainer = document.getElementById('informalInventoryTableContainer');
  const loansContainer = document.getElementById('informalLoansTableContainer');

  [btnGunShed, btnHq, btnLoans].forEach(b => {
    if (b) {
      b.classList.remove('active');
      b.style.background = 'rgba(255,255,255,0.06)';
      b.style.color = '#94a3b8';
      b.style.borderColor = 'rgba(255,255,255,0.15)';
    }
  });

  if (sectionKey === 'gun_shed') {
    if (btnGunShed) {
      btnGunShed.classList.add('active');
      btnGunShed.style.background = 'var(--accent-blue)';
      btnGunShed.style.color = '#fff';
      btnGunShed.style.borderColor = 'var(--accent-blue)';
    }
    if (invContainer) invContainer.style.display = 'block';
    if (loansContainer) loansContainer.style.display = 'none';
    renderInformalTable();
  } else if (sectionKey === 'hq_warehouse') {
    if (btnHq) {
      btnHq.classList.add('active');
      btnHq.style.background = 'var(--accent-blue)';
      btnHq.style.color = '#fff';
      btnHq.style.borderColor = 'var(--accent-blue)';
    }
    if (invContainer) invContainer.style.display = 'block';
    if (loansContainer) loansContainer.style.display = 'none';
    renderInformalTable();
  } else if (sectionKey === 'loans_history') {
    if (btnLoans) {
      btnLoans.classList.add('active');
      btnLoans.style.background = 'var(--accent-blue)';
      btnLoans.style.color = '#fff';
      btnLoans.style.borderColor = 'var(--accent-blue)';
    }
    if (invContainer) invContainer.style.display = 'none';
    if (loansContainer) loansContainer.style.display = 'block';
    renderInformalLoansTable();
  }
}

function onInformalSearchChange(val) {
  currentInformalSearch = (val || '').trim().toLowerCase();
  if (currentInformalSection === 'loans_history') {
    renderInformalLoansTable();
  } else {
    renderInformalTable();
  }
}

function renderInformalTable() {
  const tbody = document.getElementById('informalTableBody');
  if (!tbody || !informalInventoryData) return;

  const sec = informalInventoryData.sections[currentInformalSection];
  if (!sec) return;

  let items = sec.items || [];
  if (currentInformalSearch) {
    items = items.filter(i => 
      i.name.toLowerCase().includes(currentInformalSearch) ||
      (i.parent_name && i.parent_name.toLowerCase().includes(currentInformalSearch)) ||
      (i.remarks && i.remarks.toLowerCase().includes(currentInformalSearch))
    );
  }

  if (items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 24px; color: var(--text-muted);">ไม่พบสิ่งอุปกรณ์ที่ตรงกับคำค้นหา</td></tr>`;
    return;
  }

  tbody.innerHTML = items.map(itm => {
    const isSub = itm.is_sub;
    const canBorrow = (itm.balance_amount || 0) > 0;
    
    return `
      <tr style="background: ${isSub ? 'rgba(255, 255, 255, 0.015)' : 'transparent'}; border-bottom: 1px solid rgba(255,255,255,0.05);">
        <td style="text-align: center; color: var(--text-secondary); font-weight: ${isSub ? '300' : '600'};">
          ${isSub ? '' : toThaiNum(itm.seq)}
        </td>
        <td style="padding-left: ${isSub ? '24px' : '10px'};">
          <div style="display: flex; align-items: center; gap: 6px;">
            ${isSub ? '<span style="color: var(--accent-cyan); font-size: 11px;">↳</span>' : ''}
            <span style="font-weight: ${isSub ? '400' : '600'}; color: ${isSub ? '#cbd5e1' : '#fff'};">
              ${itm.name}
            </span>
            ${itm.remarks ? `<span class="badge" style="font-size: 10px; padding: 0 4px; background: rgba(255,255,255,0.06); color: #94a3b8;">${itm.remarks}</span>` : ''}
          </div>
        </td>
        <td style="text-align: center; color: var(--text-secondary);">${toThaiNum(itm.control_amount || 0)}</td>
        <td style="text-align: center; color: #38bdf8; font-weight: 500;">${toThaiNum(itm.physical_amount || 0)}</td>
        <td style="text-align: center; color: ${itm.deficit_amount ? '#f87171' : 'var(--text-muted)'}; font-weight: ${itm.deficit_amount ? '600' : '300'};">${toThaiNum(itm.deficit_amount || 0)}</td>
        <td style="text-align: center; color: ${itm.surplus_amount ? '#fbbf24' : 'var(--text-muted)'};">${toThaiNum(itm.surplus_amount || 0)}</td>
        <td style="text-align: center; color: ${itm.repair_amount ? '#f87171' : 'var(--text-muted)'}; font-weight: ${itm.repair_amount ? '600' : '300'};">
          ${itm.repair_amount ? `⚠️ ${toThaiNum(itm.repair_amount)}` : '๐'}
        </td>
        <td style="text-align: center; color: ${itm.loan_amount ? '#fbbf24' : 'var(--text-muted)'}; font-weight: ${itm.loan_amount ? '600' : '300'};">
          ${itm.loan_amount ? `⏳ ${toThaiNum(itm.loan_amount)}` : '๐'}
        </td>
        <td style="text-align: center; font-weight: 700; color: ${canBorrow ? '#34d399' : '#f87171'};">
          ${toThaiNum(itm.balance_amount || 0)}
        </td>
        <td style="text-align: center;">
          ${canBorrow ? `
            <button onclick="openBorrowModal('${itm.id}')" class="btn-action btn-html" style="font-size: 11.5px; padding: 3px 8px; cursor: pointer;" title="เบิกยืมสิ่งอุปกรณ์ชิ้นนี้">
              ➕ ยืม
            </button>
          ` : `
            <span style="font-size: 11px; color: var(--text-muted);">หมดสต็อก</span>
          `}
        </td>
      </tr>
    `;
  }).join('');
}

function renderInformalLoansTable() {
  const tbody = document.getElementById('informalLoansBody');
  if (!tbody || !informalInventoryData) return;

  const loans = informalInventoryData.loans || [];
  let filteredLoans = loans;
  if (currentInformalSearch) {
    filteredLoans = filteredLoans.filter(l => 
      l.borrower_fullname.toLowerCase().includes(currentInformalSearch) ||
      l.item_name.toLowerCase().includes(currentInformalSearch) ||
      l.loan_id.toLowerCase().includes(currentInformalSearch)
    );
  }

  if (filteredLoans.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 24px; color: var(--text-muted);">ไม่พบประวัติการเบิกยืมสิ่งอุปกรณ์</td></tr>`;
    return;
  }

  const today = new Date().toISOString().split('T')[0];

  tbody.innerHTML = filteredLoans.map(l => {
    const isBorrowed = l.status === 'borrowed';
    const isDamaged = l.status === 'returned_damaged';
    const isOverdue = isBorrowed && l.expected_return_date && l.expected_return_date < today;

    let statusHtml = '';
    if (isBorrowed) {
      if (isOverdue) {
        statusHtml = `<span class="badge" style="background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4); font-size: 11px;">⚠️ เกินกำหนดคืน!</span>`;
      } else {
        statusHtml = `<span class="badge" style="background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.4); font-size: 11px;">⏳ กำลังเบิกยืม</span>`;
      }
    } else if (isDamaged) {
      statusHtml = `<span class="badge" style="background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4); font-size: 11px;">❌ คืน-ชำรุด (ส่งซ่อม)</span>`;
    } else {
      statusHtml = `<span class="badge" style="background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.4); font-size: 11px;">✓ คืนปกติ</span>`;
    }

    return `
      <tr style="border-bottom: 1px solid rgba(255,255,255,0.05); background: ${isOverdue ? 'rgba(239, 68, 68, 0.05)' : 'transparent'};">
        <td style="text-align: center; font-family: monospace; font-size: 11.5px; color: #94a3b8;">${l.loan_id}</td>
        <td>
          <div style="font-weight: 600; color: #fff;">${l.borrower_fullname}</div>
          <div style="font-size: 11px; color: var(--text-muted);">${l.borrower_position || 'พลปืน'}</div>
        </td>
        <td>
          <div style="font-weight: 600; color: #38bdf8;">${l.item_full_name || l.item_name}</div>
          <div style="font-size: 11px; color: var(--text-secondary);">${l.section_title}</div>
        </td>
        <td style="text-align: center; font-weight: 600; color: #fff;">${toThaiNum(l.quantity)}</td>
        <td style="text-align: center; color: var(--text-secondary); font-size: 12px;">${formatDisplayThaiDate(l.loan_date)}</td>
        <td style="text-align: center; color: ${isOverdue ? '#f87171' : 'var(--text-secondary)'}; font-weight: ${isOverdue ? '700' : '400'}; font-size: 12px;">
          ${formatDisplayThaiDate(l.expected_return_date)}
        </td>
        <td style="text-align: center; color: var(--text-secondary); font-size: 12px;">
          ${l.actual_return_date ? formatDisplayThaiDate(l.actual_return_date) : '-'}
        </td>
        <td style="text-align: center;">${statusHtml}</td>
        <td style="text-align: center;">
          <div style="display: flex; gap: 4px; justify-content: center; flex-wrap: wrap;">
            ${isBorrowed ? `
              <button onclick="openReturnModal('${l.loan_id}')" class="btn-action btn-docx" style="font-size: 11px; padding: 3px 8px; cursor: pointer;">
                📥 บันทึกการคืน
              </button>
            ` : ''}
            ${isDamaged ? `
              <button onclick="openDamageReportModal('${l.loan_id}')" class="btn-action btn-html" style="font-size: 11px; padding: 3px 8px; background: rgba(14, 165, 233, 0.2); color: #38bdf8; border-color: rgba(14, 165, 233, 0.4); cursor: pointer;" title="เปิดบันทึกข้อความรายงานความชำรุดส่ง ผบ.ร้อย">
                📝 เขียนรายงาน
              </button>
            ` : ''}
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function formatDisplayThaiDate(isoDateStr) {
  if (!isoDateStr) return '-';
  const parts = isoDateStr.split('-');
  if (parts.length === 3) {
    const d = parseInt(parts[2], 10);
    const m = parseInt(parts[1], 10);
    const y = parseInt(parts[0], 10) + 543;
    const thMonths = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."];
    return `${toThaiNum(d)} ${thMonths[m]} ${toThaiNum(String(y).slice(-2))}`;
  }
  return toThaiNum(isoDateStr);
}

// ==========================================
// BORROW MODAL FUNCTIONS
// ==========================================
function openBorrowModal(preselectedItemId = '') {
  const selectElem = document.getElementById('borrowItemId');
  if (!selectElem || !informalInventoryData) return;

  const s1Items = informalInventoryData.sections.gun_shed.items || [];
  const s2Items = informalInventoryData.sections.hq_warehouse.items || [];

  let optionsHtml = '<option value="">-- เลือกสิ่งอุปกรณ์ที่ต้องการเบิกยืม --</option>';
  
  optionsHtml += '<optgroup label="🏭 สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ ๑ - ๔๓)">';
  s1Items.forEach(i => {
    const disabled = (i.balance_amount || 0) <= 0 ? 'disabled' : '';
    optionsHtml += `<option value="${i.id}" ${disabled} data-balance="${i.balance_amount || 0}">
      ${i.seq ? i.seq + '. ' : '- '}${i.full_name} (คงเหลือ: ${toThaiNum(i.balance_amount || 0)})
    </option>`;
  });
  optionsHtml += '</optgroup>';

  optionsHtml += '<optgroup label="🏢 สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (ลำดับ ๑ - ๒๙)">';
  s2Items.forEach(i => {
    const disabled = (i.balance_amount || 0) <= 0 ? 'disabled' : '';
    optionsHtml += `<option value="${i.id}" ${disabled} data-balance="${i.balance_amount || 0}">
      ${i.seq ? i.seq + '. ' : '- '}${i.full_name} (คงเหลือ: ${toThaiNum(i.balance_amount || 0)})
    </option>`;
  });
  optionsHtml += '</optgroup>';

  selectElem.innerHTML = optionsHtml;

  if (preselectedItemId) {
    selectElem.value = preselectedItemId;
    onBorrowItemSelectChange(preselectedItemId);
  }

  // Set default dates
  const today = new Date().toISOString().split('T')[0];
  const next3Days = new Date(Date.now() + 3 * 86400000).toISOString().split('T')[0];
  
  document.getElementById('borrowDate').value = today;
  document.getElementById('borrowExpectedReturn').value = next3Days;

  document.getElementById('loanBorrowModal').classList.add('active');
}

function closeBorrowModal() {
  document.getElementById('loanBorrowModal')?.classList.remove('active');
}

function onBorrowItemSelectChange(itemId) {
  const hintElem = document.getElementById('borrowItemStockHint');
  const qtyInput = document.getElementById('borrowQuantity');
  if (!hintElem || !informalInventoryData) return;

  let found = null;
  for (const k of ['gun_shed', 'hq_warehouse']) {
    found = informalInventoryData.sections[k].items.find(i => i.id === itemId);
    if (found) break;
  }

  if (found) {
    const bal = found.balance_amount || 0;
    hintElem.innerText = `คงเหลือพร้อมให้ยืม: ${toThaiNum(bal)} รายการ`;
    hintElem.style.color = bal > 0 ? 'var(--accent-cyan)' : '#f87171';
    if (qtyInput) {
      qtyInput.max = bal;
      qtyInput.value = Math.min(1, bal);
    }
  } else {
    hintElem.innerText = 'คงเหลือพร้อมให้ยืม: - รายการ';
  }
}

async function handleBorrowSubmit(e) {
  e.preventDefault();
  const itemId = document.getElementById('borrowItemId').value;
  const rank = document.getElementById('borrowerRank').value.trim();
  const name = document.getElementById('borrowerName').value.trim();
  const pos = document.getElementById('borrowerPos').value.trim();
  const qty = parseInt(document.getElementById('borrowQuantity').value, 10);
  const loanDate = document.getElementById('borrowDate').value;
  const expDate = document.getElementById('borrowExpectedReturn').value;

  if (!itemId || !rank || !name || qty <= 0) {
    alert('กรุณากรอกข้อมูลการเบิกยืมให้ครบถ้วน');
    return;
  }

  const payload = {
    item_id: itemId,
    borrower_rank: rank,
    borrower_name: name,
    borrower_position: pos,
    quantity: qty,
    loan_date: loanDate,
    expected_return_date: expDate
  };

  try {
    const res = await fetch(`${API_BASE}/informal-equipment/loan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const newLoan = await res.json();
      await loadInformalInventoryData();
      renderInformalSurveyUI();
      closeBorrowModal();
      alert(`บันทึกการเบิกยืมสำเร็จ!\nผู้ยืม: ${rank} ${name}\nรายการ: ${newLoan.item_name} (จำนวน ${toThaiNum(qty)} รายการ)\nระบบได้ตัดยอดยุทโธปกรณ์ออกจากคงเหลือทันที ๑๐๐%`);
      return;
    }
    const errData = await res.json();
    throw new Error(errData.detail || 'เกิดข้อผิดพลาดในการเบิกยืม');
  } catch (err) {
    console.warn('API error, performing client fallback:', err);
    // Client fallback
    executeClientBorrowFallback(payload);
  }
}

function executeClientBorrowFallback(payload) {
  let found = null;
  for (const k of ['gun_shed', 'hq_warehouse']) {
    found = informalInventoryData.sections[k].items.find(i => i.id === payload.item_id);
    if (found) break;
  }
  if (!found) {
    alert('ไม่พบสิ่งอุปกรณ์');
    return;
  }

  found.balance_amount = Math.max(0, (found.balance_amount || 0) - payload.quantity);
  found.loan_amount = (found.loan_amount || 0) + payload.quantity;

  const newLoan = {
    loan_id: `LN-${Date.now().toString().slice(-6)}`,
    item_id: payload.item_id,
    item_name: found.name,
    item_full_name: found.full_name,
    section: found.section,
    section_title: found.section_title,
    borrower_rank: payload.borrower_rank,
    borrower_name: payload.borrower_name,
    borrower_fullname: `${payload.borrower_rank} ${payload.borrower_name}`,
    borrower_position: payload.borrower_position,
    quantity: payload.quantity,
    loan_date: payload.loan_date,
    expected_return_date: payload.expected_return_date,
    actual_return_date: null,
    status: 'borrowed',
    damage_info: null
  };

  informalInventoryData.loans.unshift(newLoan);
  localStorage.setItem('informal_inventory_db', JSON.stringify(informalInventoryData));
  renderInformalSurveyUI();
  closeBorrowModal();
  alert(`บันทึกการเบิกยืมสำเร็จ (โหมด Local)!\nตัดยอดยุทโธปกรณ์ออกจากคงเหลือเรียบร้อย`);
}

// ==========================================
// RETURN & DAMAGE MODAL FUNCTIONS
// ==========================================
function openReturnModal(loanId) {
  if (!informalInventoryData) return;
  const loan = informalInventoryData.loans.find(l => l.loan_id === loanId);
  if (!loan) return;

  document.getElementById('returnLoanId').value = loanId;
  document.getElementById('returnSummaryBorrower').innerText = loan.borrower_fullname;
  document.getElementById('returnSummaryItem').innerText = loan.item_full_name || loan.item_name;
  document.getElementById('returnSummaryQty').innerText = toThaiNum(loan.quantity);
  document.getElementById('returnSummaryLoanDate').innerText = formatDisplayThaiDate(loan.loan_date);
  document.getElementById('returnSummaryExpDate').innerText = formatDisplayThaiDate(loan.expected_return_date);

  document.getElementById('returnActualDate').value = new Date().toISOString().split('T')[0];
  document.getElementById('chkHasDamage').checked = false;
  document.getElementById('damageCause').value = '';
  document.getElementById('damageSymptom').value = '';
  document.getElementById('damageInputGroup').style.display = 'none';

  document.getElementById('loanReturnModal').classList.add('active');
}

function closeReturnModal() {
  document.getElementById('loanReturnModal')?.classList.remove('active');
}

function toggleDamageFields(hasDamage) {
  const grp = document.getElementById('damageInputGroup');
  if (grp) {
    grp.style.display = hasDamage ? 'block' : 'none';
  }
}

async function handleReturnSubmit(e) {
  e.preventDefault();
  const loanId = document.getElementById('returnLoanId').value;
  const actualDate = document.getElementById('returnActualDate').value;
  const hasDamage = document.getElementById('chkHasDamage').checked;
  const cause = document.getElementById('damageCause').value.trim();
  const symptom = document.getElementById('damageSymptom').value.trim();

  if (hasDamage && (!cause || !symptom)) {
    alert('กรณีตรวจพบการชำรุดเสียหาย กรุณาระบุทั้ง "สาเหตุที่เกิด" และ "อาการที่เกิด" ให้ครบถ้วน');
    return;
  }

  const payload = {
    loan_id: loanId,
    actual_return_date: actualDate,
    has_damage: hasDamage,
    cause: cause,
    symptom: symptom
  };

  try {
    const res = await fetch(`${API_BASE}/informal-equipment/return`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      await loadInformalInventoryData();
      renderInformalSurveyUI();
      closeReturnModal();
      if (hasDamage) {
        if (confirm(`บันทึกการรับคืนและตัดยอดเข้า "ส่งซ่อม" เรียบร้อยแล้ว!\n\nคุณต้องการเปิด "บันทึกข้อความ" รายงานการชำรุดเสียหายให้ ผบ.ร้อย ทราบทันทีหรือไม่?`)) {
          openDamageReportModal(loanId);
        }
      } else {
        alert('บันทึกการส่งคืนสิ่งอุปกรณ์สำเร็จ คืนสต็อกคงเหลือพร้อมใช้งานเรียบร้อย!');
      }
      return;
    }
    const errData = await res.json();
    throw new Error(errData.detail || 'เกิดข้อผิดพลาดในการคืน');
  } catch (err) {
    console.warn('API error, client fallback:', err);
    executeClientReturnFallback(payload);
  }
}

function executeClientReturnFallback(payload) {
  const loan = informalInventoryData.loans.find(l => l.loan_id === payload.loan_id);
  if (!loan) return;

  let found = null;
  for (const k of ['gun_shed', 'hq_warehouse']) {
    found = informalInventoryData.sections[k].items.find(i => i.id === loan.item_id);
    if (found) break;
  }

  if (found) {
    found.loan_amount = Math.max(0, (found.loan_amount || 0) - loan.quantity);
    if (payload.has_damage) {
      found.repair_amount = (found.repair_amount || 0) + loan.quantity;
    } else {
      found.balance_amount = (found.balance_amount || 0) + loan.quantity;
    }
  }

  loan.actual_return_date = payload.actual_return_date;
  loan.status = payload.has_damage ? 'returned_damaged' : 'returned_normal';
  loan.damage_info = {
    has_damage: payload.has_damage,
    cause: payload.cause,
    symptom: payload.symptom,
    reported_to_commander: false,
    memo_generated: payload.has_damage
  };

  localStorage.setItem('informal_inventory_db', JSON.stringify(informalInventoryData));
  renderInformalSurveyUI();
  closeReturnModal();
  if (payload.has_damage) {
    if (confirm(`บันทึกการรับคืนและตัดยอดเข้า "ส่งซ่อม" เรียบร้อยแล้ว (โหมด Local)!\n\nต้องการเปิด "บันทึกข้อความ" รายงาน ผบ.ร้อย ทราบหรือไม่?`)) {
      openDamageReportModal(payload.loan_id);
    }
  } else {
    alert('บันทึกการคืนสำเร็จ!');
  }
}

// ==========================================
// OVERDUE ALERTS MODAL
// ==========================================
async function openOverdueModal() {
  const container = document.getElementById('overdueListContainer');
  if (!container || !informalInventoryData) return;

  const today = new Date().toISOString().split('T')[0];
  const overdueLoans = (informalInventoryData.loans || []).filter(l => 
    l.status === 'borrowed' && l.expected_return_date && l.expected_return_date < today
  );

  if (overdueLoans.length === 0) {
    container.innerHTML = `<div style="text-align: center; padding: 24px; color: #34d399;">✓ ยอดเยี่ยม! ไม่พบรายการเบิกยืมที่เกินกำหนดคืนในขณะนี้</div>`;
  } else {
    container.innerHTML = overdueLoans.map(l => {
      const expDate = new Date(l.expected_return_date);
      const diffDays = Math.ceil((new Date() - expDate) / (1000 * 60 * 60 * 24));
      return `
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;">
          <div>
            <div style="font-weight: 600; color: #fff; font-size: 14px;">
              ${l.borrower_fullname} (${l.borrower_position || 'พลปืน'})
            </div>
            <div style="font-size: 12px; color: #38bdf8; margin-top: 2px;">
              ยืม: <strong>${l.item_full_name || l.item_name}</strong> (จำนวน ${toThaiNum(l.quantity)} รายการ)
            </div>
            <div style="font-size: 11.5px; color: #fca5a5; margin-top: 3px;">
              กำหนดคืน: ${formatDisplayThaiDate(l.expected_return_date)} (เกินกำหนดมาแล้ว ${toThaiNum(diffDays)} วัน)
            </div>
          </div>
          <div style="display: flex; gap: 6px;">
            <button onclick="closeOverdueModal(); openReturnModal('${l.loan_id}');" class="btn-primary" style="padding: 6px 12px; font-size: 12px; cursor: pointer;">
              📥 บันทึกรับคืน
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  document.getElementById('overdueLoansModal')?.classList.add('active');
}

function closeOverdueModal() {
  document.getElementById('overdueLoansModal')?.classList.remove('active');
}

function checkOverdueLoansOnLoad() {
  if (!informalInventoryData) return;
  const today = new Date().toISOString().split('T')[0];
  const overdueCount = (informalInventoryData.loans || []).filter(l => 
    l.status === 'borrowed' && l.expected_return_date && l.expected_return_date < today
  ).length;

  if (overdueCount > 0) {
    console.warn(`[ALERT] มีรายการเบิกยืมสิ่งอุปกรณ์เกินกำหนดคืนจำนวน ${overdueCount} รายการ!`);
  }
}

// ==========================================
// DAMAGE MEMO REPORT MODAL & PRINTING
// ==========================================
function openDamageReportModal(loanId) {
  const iframe = document.getElementById('damageMemoIframe');
  const openLink = document.getElementById('btnOpenMemoExternal');
  const memoUrl = `${API_BASE}/informal-equipment/report/${loanId}`;
  const staticFallback = `/บันทึกข้อความ_รายงานการชำรุดเสียหาย_Rebuild_Thai.html`;

  if (iframe) {
    iframe.src = memoUrl;
    // Set fallback on error
    iframe.onerror = () => { iframe.src = staticFallback; };
  }
  if (openLink) {
    openLink.href = memoUrl;
  }

  document.getElementById('damageMemoModal')?.classList.add('active');
}

function closeDamageMemoModal() {
  document.getElementById('damageMemoModal')?.classList.remove('active');
  const iframe = document.getElementById('damageMemoIframe');
  if (iframe) iframe.src = '';
}

function printDamageMemoFrame() {
  const iframe = document.getElementById('damageMemoIframe');
  if (iframe && iframe.contentWindow) {
    iframe.contentWindow.focus();
    iframe.contentWindow.print();
  }
}
'''

    if "initInformalSurvey" not in content or "informalInventoryData" not in content:
        content += informal_code
        print("Appended Informal Survey JavaScript code to dashboard.js.")

    DASHBOARD_JS.write_text(content, encoding="utf-8")
    print("dashboard.js updated successfully.")

if __name__ == '__main__':
    update_js()
