"""
Updates frontend/templates/index.html to add:
1. Tab 5: Informal Equipment Survey & Loan/Damage Management
2. Complete Section UI with tables for Section 1 (1-43) and Section 2 (1-29)
3. Modals for Borrowing, Returning (with Cause/Symptom damage tracking), Overdue Alerts, and Damage Memo Preview.
"""
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = WORKSPACE_ROOT / "frontend" / "templates" / "index.html"

def update_html():
    content = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Add 5th Tab Button if not present
    tab_needle = 'id="tabBtn17Docs">'
    new_tab_btn = '''
    <button class="tab-btn" data-tab="tab-informal-survey" id="tabBtnInformalSurvey">
      📋 สำรวจ​สิ่งอุปกรณ์ & เบิกยืม-ส่งซ่อม (ไม่เป็นทางการ)
    </button>'''

    if 'id="tabBtnInformalSurvey"' not in content:
        # Find where the tabBtn17Docs button tag closes </button>
        idx = content.find(tab_needle)
        if idx != -1:
            close_btn_idx = content.find('</button>', idx)
            if close_btn_idx != -1:
                insert_pos = close_btn_idx + len('</button>')
                content = content[:insert_pos] + new_tab_btn + content[insert_pos:]
                print("Added tabBtnInformalSurvey button.")

    # 2. Add Section 5 HTML
    section_needle = '</section>'  # end of tab-all-17-docs
    # Find last </section> before previewModal
    modal_idx = content.find('id="previewModal"')
    if modal_idx != -1:
        last_sec_close = content.rfind('</section>', 0, modal_idx)
    else:
        last_sec_close = content.rfind('</section>')

    section_5_html = '''

  <!-- ==================================================== -->
  <!-- TAB 5: INFORMAL EQUIPMENT SURVEY & LOAN/DAMAGE MGMT  -->
  <!-- ==================================================== -->
  <section id="tab-informal-survey" class="tab-content">
    
    <!-- Header Banner -->
    <div class="glass-panel" style="padding: 22px 24px; margin-bottom: 22px; border-color: rgba(56, 189, 248, 0.35); background: linear-gradient(180deg, rgba(15, 23, 42, 0.85) 0%, rgba(10, 15, 26, 0.95) 100%);">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
        <div>
          <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 6px;">
            <span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); font-size: 11.5px; font-weight: 600;">
              📌 สำรวจแบบไม่เป็นทางการ เพื่อรายงาน ผบ.ร้อย
            </span>
            <span class="badge badge-generated" style="font-size: 11.5px;">
              🛡️ แยกอิสระ ไม่นับรวมบัญชีทางการเดิม
            </span>
            <span class="badge" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35); font-size: 11.5px;">
              🔄 ตัดยอดส่งซ่อม & บันทึกข้อความอัตโนมัติ
            </span>
          </div>
          <h2 style="font-size: 21px; font-weight: 600; color: #fff; margin: 0; display: flex; align-items: center; gap: 10px;">
            📋 บัญชี​สำรวจ​รายการ​และ​สิ่งอุปกรณ์ & ระบบ​เบิกยืม-ส่ง​ซ่อม
          </h2>
          <p style="font-size: 13.5px; color: var(--text-secondary); margin: 6px 0 0 0; line-height: 1.4;">
            โคลน​จาก <em>บัญชีรายการและสิ่งอุปกรณ์.xlsx</em> แบ่งออกเป็น: 
            <strong>๑. สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ ๑ - ๔๓)</strong> และ 
            <strong>๒. สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (ลำดับ ๑ - ๒๙)</strong>
          </p>
        </div>

        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
          <button onclick="openBorrowModal()" class="btn-primary" style="padding: 9px 18px; font-size: 13.5px; cursor: pointer;">
            ➕ เบิกยืม​สิ่งอุปกรณ์
          </button>
          <button onclick="openOverdueModal()" id="btnOverdueAlertsBadge" class="btn-danger" style="padding: 9px 16px; font-size: 13.5px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
            ⚠️ แจ้งเตือน​เกินกำหนด (<span id="overdueCountBadge">0</span>)
          </button>
          <a href="/บันทึกข้อความ_รายงานการชำรุดเสียหาย_Rebuild_Thai.html" target="_blank" class="btn-secondary" style="padding: 8px 14px; font-size: 13px;" title="เปิดดูต้นแบบบันทึกข้อความรายงานความชำรุดจากการยืม">
            📄 ตัวอย่าง​บันทึกข้อความ
          </a>
        </div>
      </div>

      <!-- Quick Metrics Grid -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-top: 20px; padding-top: 18px; border-top: 1px solid rgba(255, 255, 255, 0.08);">
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 12px 14px;">
          <div style="font-size: 12px; color: var(--text-muted);">รายการ​สำรวจ​ทั้งหมด</div>
          <div style="font-size: 20px; font-weight: 700; color: #fff; margin-top: 4px;" id="metricTotalItems">๑๐๑ รายการ</div>
          <div style="font-size: 11px; color: #38bdf8; margin-top: 2px;">โรงเก็บ ๕๘ • คลัง บก. ๔๓</div>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 12px 14px;">
          <div style="font-size: 12px; color: var(--text-muted);">ยอดที่​มี​จริง (Physical)</div>
          <div style="font-size: 20px; font-weight: 700; color: #38bdf8; margin-top: 4px;" id="metricPhysicalTotal">-</div>
          <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">ตรวจนับ​หน้า​คลัง</div>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 10px; padding: 12px 14px;">
          <div style="font-size: 12px; color: #fbbf24;">กำลัง​ถูก​เบิกยืม</div>
          <div style="font-size: 20px; font-weight: 700; color: #fbbf24; margin-top: 4px;" id="metricLoanTotal">0</div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">ตัดยอด​จาก​คงเหลือ</div>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 10px; padding: 12px 14px;">
          <div style="font-size: 12px; color: #f87171;">ชำรุด / ส่ง​ซ่อม (ตัดยอด)</div>
          <div style="font-size: 20px; font-weight: 700; color: #f87171; margin-top: 4px;" id="metricRepairTotal">0</div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">ย้าย​เข้า​ช่องส่งซ่อม</div>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 12px 14px;">
          <div style="font-size: 12px; color: #34d399;">คงเหลือ​พร้อม​ใช้งาน</div>
          <div style="font-size: 20px; font-weight: 700; color: #34d399; margin-top: 4px;" id="metricBalanceTotal">-</div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">พร้อม​เบิกยืม​ทันที</div>
        </div>
      </div>
    </div>

    <!-- Section Filter Segment Navigation -->
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; margin-bottom: 16px;">
      <div style="display: flex; gap: 8px; flex-wrap: wrap;" id="informalSectionTabs">
        <button onclick="switchInformalSection('gun_shed')" id="btnSecGunShed" class="btn-filter active" style="padding: 9px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; cursor: pointer;">
          🏭 สิ่งอุปกรณ์​ใน​โรงเก็บ​ปืนใหญ่ (ลำดับ ๑ - ๔๓)
        </button>
        <button onclick="switchInformalSection('hq_warehouse')" id="btnSecHqWarehouse" class="btn-filter" style="padding: 9px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; cursor: pointer;">
          🏢 สิ่งอุปกรณ์​ใน​คลัง บก.โรงเก็บ​ปืนใหญ่ (ลำดับ ๑ - ๒๙)
        </button>
        <button onclick="switchInformalSection('loans_history')" id="btnSecLoans" class="btn-filter" style="padding: 9px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; cursor: pointer;">
          📑 ประวัติ​การ​เบิกยืม & บันทึก​ส่ง​ซ่อม (<span id="loanListBadge">0</span>)
        </button>
      </div>

      <!-- Live Search Box -->
      <div style="position: relative; width: 280px; max-width: 100%;">
        <input type="text" id="informalSearchInput" oninput="onInformalSearchChange(this.value)" placeholder="🔍 ค้นหาชื่อสิ่งอุปกรณ์..." style="width: 100%; padding: 8px 14px; border-radius: 8px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.15); color: #fff; font-size: 13px;">
      </div>
    </div>

    <!-- Section 1 & 2 Equipment Inventory Table -->
    <div id="informalInventoryTableContainer" class="glass-panel table-container" style="padding: 0; margin-bottom: 24px; overflow-x: auto;">
      <table class="data-table" style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <thead>
          <tr>
            <th style="width: 55px; text-align: center;">ลำดับ</th>
            <th style="text-align: left; min-width: 220px;">รายการ</th>
            <th style="width: 85px; text-align: center;">ยอดบัญชีคุม</th>
            <th style="width: 80px; text-align: center;">ยอดที่มี</th>
            <th style="width: 65px; text-align: center;">ขาด</th>
            <th style="width: 65px; text-align: center;">เกิน</th>
            <th style="width: 75px; text-align: center; color: #f87171;">ส่งซ่อม</th>
            <th style="width: 75px; text-align: center; color: #fbbf24;">เบิกยืม</th>
            <th style="width: 85px; text-align: center; color: #34d399; font-weight: 600;">คงเหลือ</th>
            <th style="width: 105px; text-align: center;">การดำเนินการ</th>
          </tr>
        </thead>
        <tbody id="informalTableBody">
          <!-- Hydrated by dashboard.js -->
        </tbody>
      </table>
    </div>

    <!-- Loans and Returns History Table (Hidden by default, shown when loan tab selected) -->
    <div id="informalLoansTableContainer" class="glass-panel table-container" style="padding: 0; margin-bottom: 24px; display: none; overflow-x: auto;">
      <table class="data-table" style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <thead>
          <tr>
            <th style="width: 110px; text-align: center;">รหัสการยืม</th>
            <th style="text-align: left; min-width: 140px;">ผู้เบิกยืม (ยศ ชื่อ สกุล)</th>
            <th style="text-align: left; min-width: 180px;">สิ่งอุปกรณ์ที่ยืม</th>
            <th style="width: 65px; text-align: center;">จำนวน</th>
            <th style="width: 95px; text-align: center;">วันที่ยืม</th>
            <th style="width: 100px; text-align: center;">กำหนดคืน</th>
            <th style="width: 100px; text-align: center;">วันที่คืนจริง</th>
            <th style="width: 120px; text-align: center;">สถานะ</th>
            <th style="width: 160px; text-align: center;">การดำเนินการ</th>
          </tr>
        </thead>
        <tbody id="informalLoansBody">
          <!-- Hydrated by dashboard.js -->
        </tbody>
      </table>
    </div>

  </section>

  <!-- ==================================================== -->
  <!-- MODAL: เบิกยืมสิ่งอุปกรณ์ (BORROW MODAL)                  -->
  <!-- ==================================================== -->
  <div id="loanBorrowModal" class="modal-overlay" onclick="closeBorrowModal()">
    <div class="glass-panel modal-content" onclick="event.stopPropagation()" style="max-width: 540px; padding: 22px;">
      <div class="modal-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 17px; font-weight: 600; color: #fff; margin: 0; display: flex; align-items: center; gap: 8px;">
          ➕ บันทึก​การ​เบิกยืม​สิ่งอุปกรณ์ (ตัดยอด​คงคลัง)
        </h3>
        <button class="modal-close" onclick="closeBorrowModal()">&times;</button>
      </div>

      <form id="borrowForm" onsubmit="handleBorrowSubmit(event)">
        <div style="display: grid; grid-template-columns: 120px 1fr; gap: 12px; margin-bottom: 12px;">
          <div>
            <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">ยศ:</label>
            <input type="text" id="borrowerRank" required placeholder="เช่น ส.อ., จ.ส.อ." style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #fff; font-size: 13px;">
          </div>
          <div>
            <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">ชื่อ - สกุล:</label>
            <input type="text" id="borrowerName" required placeholder="ระบุชื่อและนามสกุลผู้ยืม" style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #fff; font-size: 13px;">
          </div>
        </div>

        <div style="margin-bottom: 12px;">
          <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">ตำแหน่ง / หน้าที่:</label>
          <input type="text" id="borrowerPos" placeholder="เช่น พลปืน ป.หมู่ 1, ผบ.หมู่" value="พลปืน" style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #fff; font-size: 13px;">
        </div>

        <div style="margin-bottom: 12px;">
          <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">สิ่งอุปกรณ์ที่ยืม:</label>
          <select id="borrowItemId" required onchange="onBorrowItemSelectChange(this.value)" style="width: 100%; padding: 8px 10px; border-radius: 6px; background: #0f172a; border: 1px solid rgba(56, 189, 248, 0.4); color: #fff; font-size: 13px;">
            <!-- Populated via JS -->
          </select>
          <div id="borrowItemStockHint" style="font-size: 11.5px; color: var(--accent-cyan); margin-top: 4px;">
            คงเหลือพร้อมให้ยืม: - รายการ
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
          <div>
            <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">จำนวนที่ยืม:</label>
            <input type="number" id="borrowQuantity" required min="1" value="1" style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #fff; font-size: 13px;">
          </div>
          <div>
            <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">วันที่ยืม:</label>
            <input type="date" id="borrowDate" required style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #fff; font-size: 13px;">
          </div>
        </div>

        <div style="margin-bottom: 18px;">
          <label style="display: block; font-size: 12.5px; color: #fbbf24; margin-bottom: 4px;">วันที่ (จะ) คืน:</label>
          <input type="date" id="borrowExpectedReturn" required style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(245, 158, 11, 0.4); color: #fff; font-size: 13px;">
          <span style="font-size: 11px; color: var(--text-muted); margin-top: 3px; display: block;">
            ⚠️ หากพ้นกำหนดวันดังกล่าว ระบบจะมีป๊อปอัปแจ้งเตือนเพื่อติดตามทวงถามอัตโนมัติ
          </span>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px;">
          <button type="button" onclick="closeBorrowModal()" class="btn-secondary" style="padding: 8px 16px;">ยกเลิก</button>
          <button type="submit" class="btn-primary" style="padding: 8px 20px;">ยืนยันการเบิกยืม</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ==================================================== -->
  <!-- MODAL: คืนสิ่งอุปกรณ์ & บันทึกชำรุดเสียหาย (RETURN MODAL)    -->
  <!-- ==================================================== -->
  <div id="loanReturnModal" class="modal-overlay" onclick="closeReturnModal()">
    <div class="glass-panel modal-content" onclick="event.stopPropagation()" style="max-width: 560px; padding: 22px;">
      <div class="modal-header" style="margin-bottom: 16px;">
        <h3 style="font-size: 17px; font-weight: 600; color: #fff; margin: 0; display: flex; align-items: center; gap: 8px;">
          📥 บันทึก​การ​คืน​สิ่งอุปกรณ์ & ตรวจสอบ​ความชำรุด
        </h3>
        <button class="modal-close" onclick="closeReturnModal()">&times;</button>
      </div>

      <form id="returnForm" onsubmit="handleReturnSubmit(event)">
        <input type="hidden" id="returnLoanId">

        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; margin-bottom: 14px; font-size: 13px; line-height: 1.45;">
          <div>ผู้ยืม: <strong id="returnSummaryBorrower" style="color: #fff;">-</strong></div>
          <div>สิ่งอุปกรณ์: <strong id="returnSummaryItem" style="color: #38bdf8;">-</strong></div>
          <div>จำนวน: <strong id="returnSummaryQty" style="color: #fff;">-</strong> รายการ | วันที่ยืม: <span id="returnSummaryLoanDate">-</span></div>
          <div>กำหนดคืนเดิม: <span id="returnSummaryExpDate" style="color: #fbbf24;">-</span></div>
        </div>

        <div style="margin-bottom: 14px;">
          <label style="display: block; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 4px;">วันที่คืนจริง:</label>
          <input type="date" id="returnActualDate" required style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #fff; font-size: 13px;">
        </div>

        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 12px; margin-bottom: 14px;">
          <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13.5px; font-weight: 600; color: #f87171;">
            <input type="checkbox" id="chkHasDamage" onchange="toggleDamageFields(this.checked)" style="width: 17px; height: 17px; accent-color: #ef4444;">
            พบการชำรุดเสียหายจากการใช้งาน (ตัดยอดไปอยู่ช่องส่งซ่อม)
          </label>
          <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 4px; padding-left: 25px;">
            หากติ๊กเลือก ระบบจะตัดยอดยุทโธปกรณ์เข้าช่อง "ส่งซ่อม" และเปิดสิทธิ์สร้าง "บันทึกข้อความ" รายงาน ผบ.ร้อย ทราบทันที
          </div>
        </div>

        <!-- Separate Cause and Symptom Fields -->
        <div id="damageInputGroup" style="display: none; border-left: 2px solid #ef4444; padding-left: 12px; margin-bottom: 16px;">
          <div style="margin-bottom: 12px;">
            <label style="display: block; font-size: 12.5px; color: #f87171; font-weight: 600; margin-bottom: 4px;">
              ⚡ สาเหตุที่เกิด (Cause):
            </label>
            <textarea id="damageCause" rows="2" placeholder="ระบุสาเหตุที่เกิดความชำรุดเสียหาย (เช่น กระทบหินแข็งใต้ผิวดิน, พลัดตกกระแทก)" style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(239, 68, 68, 0.4); color: #fff; font-size: 13px; font-family: inherit; resize: vertical;"></textarea>
          </div>

          <div>
            <label style="display: block; font-size: 12.5px; color: #f87171; font-weight: 600; margin-bottom: 4px;">
              🔧 อาการที่เกิด (Symptoms & Condition):
            </label>
            <textarea id="damageSymptom" rows="2" placeholder="ระบุอาการชำรุดเสียหายที่ตรวจพบ (เช่น ด้ามหักสะบั้น, ใบจอบบิดงอผิดรูป, ลั่นไกขัดข้อง)" style="width: 100%; padding: 8px 10px; border-radius: 6px; background: rgba(0,0,0,0.5); border: 1px solid rgba(239, 68, 68, 0.4); color: #fff; font-size: 13px; font-family: inherit; resize: vertical;"></textarea>
          </div>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px;">
          <button type="button" onclick="closeReturnModal()" class="btn-secondary" style="padding: 8px 16px;">ยกเลิก</button>
          <button type="submit" class="btn-primary" style="padding: 8px 20px;">บันทึกการคืน</button>
        </div>
      </form>
    </div>
  </div>

  <!-- ==================================================== -->
  <!-- MODAL: รายการเกินกำหนดคืน (OVERDUE ALERTS MODAL)         -->
  <!-- ==================================================== -->
  <div id="overdueLoansModal" class="modal-overlay" onclick="closeOverdueModal()">
    <div class="glass-panel modal-content" onclick="event.stopPropagation()" style="max-width: 640px; padding: 22px;">
      <div class="modal-header" style="margin-bottom: 14px;">
        <h3 style="font-size: 17px; font-weight: 600; color: #f87171; margin: 0; display: flex; align-items: center; gap: 8px;">
          ⚠️ แจ้งเตือน​รายการ​เบิกยืม​เกินกำหนด​คืน (ติดตาม​ทวงถาม)
        </h3>
        <button class="modal-close" onclick="closeOverdueModal()">&times;</button>
      </div>

      <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 14px;">
        รายการต่อไปนี้พ้นกำหนดวันที่ (จะ) คืนแล้ว กรุณาประสานเจ้าหน้าที่ผู้เบิกยืมเพื่อส่งคืนสิ่งอุปกรณ์หรือตรวจสอบความชำรุดเสียหาย:
      </div>

      <div id="overdueListContainer" style="max-height: 340px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;">
        <!-- Hydrated by JS -->
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 18px;">
        <button onclick="closeOverdueModal()" class="btn-secondary" style="padding: 8px 18px;">ปิดหน้าต่าง</button>
      </div>
    </div>
  </div>

  <!-- ==================================================== -->
  <!-- MODAL: พรีวิวบันทึกข้อความรายงานความชำรุด (MEMO PREVIEW)    -->
  <!-- ==================================================== -->
  <div id="damageMemoModal" class="modal-overlay" onclick="closeDamageMemoModal()">
    <div class="glass-panel modal-content" onclick="event.stopPropagation()" style="width: 95%; max-width: 920px; height: 90vh; padding: 18px; display: flex; flex-direction: column;">
      <div class="modal-header" style="margin-bottom: 10px;">
        <div>
          <h3 style="font-size: 17px; font-weight: 600; color: #fff; margin: 0; display: flex; align-items: center; gap: 8px;">
            📄 บันทึก​ข้อความ: รายงาน​การ​ชำรุด​เสียหาย​ของ​สิ่งและ​อุปกรณ์ จาก​การ​เบิกยืม
          </h3>
          <p style="font-size: 12px; color: var(--accent-cyan); margin: 2px 0 0 0;">
            ระเบียบ​สารบรรณ ทบ. • Red Line Standard ๑๓๐ มม. • พิมพ์​คู่ขนาน ๒ ชุด (ฉบับ​ตัวจริง & สำเนา​คู่ฉบับ)
          </p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button onclick="printDamageMemoFrame()" class="btn-primary" style="padding: 6px 14px; font-size: 12.5px;">
            🖨️ สั่งพิมพ์ (Print 300 DPI)
          </button>
          <a id="btnOpenMemoExternal" href="#" target="_blank" class="btn-secondary" style="padding: 6px 12px; font-size: 12.5px;">
            🌐 เปิดแท็บใหม่
          </a>
          <button class="modal-close" onclick="closeDamageMemoModal()">&times;</button>
        </div>
      </div>

      <div style="flex: 1; border-radius: 8px; overflow: hidden; border: 1px solid rgba(255,255,255,0.15); background: #525659;">
        <iframe id="damageMemoIframe" src="" style="width: 100%; height: 100%; border: none;"></iframe>
      </div>
    </div>
  </div>
'''

    if 'id="tab-informal-survey"' not in content:
        if last_sec_close != -1:
            insert_pos = last_sec_close + len('</section>')
            content = content[:insert_pos] + section_5_html + content[insert_pos:]
            print("Added section tab-informal-survey and modals.")

    INDEX_HTML.write_text(content, encoding="utf-8")
    print("Updated index.html successfully.")

if __name__ == '__main__':
    update_html()
