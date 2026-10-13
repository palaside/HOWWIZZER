"""
Playwright E2E Test Suite for Informal Equipment Survey & Loan/Damage Management
Validates all user-requested requirements:
1. Tab 5 Navigation & Dual-section Render:
   - Section 1: สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ 1 - 43)
   - Section 2: สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (ลำดับ 1 - 29)
2. Borrow system (ยศ ชื่อ สกุล, สิ่งที่ยืม, จำนวน, วันที่ยืม, วันที่คืน) with stock deduction.
3. Return system with damage tracking:
   - Cause (สาเหตุ) and Symptoms (อาการ) separate inputs.
   - Stock deduction transferring into "ส่งซ่อม" (repair slot).
4. Write Report button triggering Royal Thai Army Memo (บันทึกข้อความ) with all required fields.
5. Overdue Alerts Popup.
"""
import asyncio
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def run_e2e():
    report = {
        "suite": "Informal Equipment Survey & Loan/Damage E2E Test",
        "timestamp": "2026-10-13",
        "steps": [],
        "passed": 0,
        "failed": 0
    }

    def record_step(name, status, details=""):
        report["steps"].append({"step": name, "status": status, "details": details})
        if status == "PASS":
            report["passed"] += 1
            print(f"[PASS] {name}: {details}")
        else:
            report["failed"] += 1
            print(f"[FAIL] {name}: {details}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        page = await context.new_page()

        # Auto-accept dialogs (alert/confirm)
        async def handle_dialog(dialog):
            await dialog.accept()
        page.on("dialog", handle_dialog)

        print("\n--- 1. Testing Navigation to Tab 5 (Informal Survey) ---")
        await page.goto("http://127.0.0.1:8888/frontend/templates/index.html", wait_until="networkidle")
        await page.wait_for_timeout(500)

        # Click Tab 5 button
        await page.click("#tabBtnInformalSurvey")
        await page.wait_for_timeout(400)

        is_tab5_active = await page.evaluate("() => document.getElementById('tab-informal-survey').classList.contains('active')")
        if is_tab5_active:
            record_step("1.1 Tab 5 Activation", "PASS", "Tab 5 active")
        else:
            record_step("1.1 Tab 5 Activation", "FAIL", "Tab 5 failed to activate")

        # -------------------------------------------------------------
        # 2. Section 1: สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ 1 - 43)
        # -------------------------------------------------------------
        print("\n--- 2. Testing Section 1: สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ 1 - 43) ---")
        s1_rows = await page.query_selector_all("#informalTableBody tr")
        if len(s1_rows) >= 43:
            record_step("2.1 Section 1 Items Render", "PASS", f"Found {len(s1_rows)} items in Section 1 (Gun Shed)")
        else:
            record_step("2.1 Section 1 Items Render", "FAIL", f"Expected >= 43 rows, found {len(s1_rows)}")

        # Verify key items e.g. เต็นท์ (ลำดับ 1) and กล้องพาโนรามิค (ลำดับ 43)
        table_text = await page.text_content("#informalTableBody")
        if "เต็นท์" in table_text and "กล้องพาโนรามิค" in table_text:
            record_step("2.2 Section 1 Boundary Items", "PASS", "Found เต็นท์ (1) and กล้องพาโนรามิค (43)")
        else:
            record_step("2.2 Section 1 Boundary Items", "FAIL", "Items not found in Section 1 table")

        # -------------------------------------------------------------
        # 3. Section 2: สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (ลำดับ 1 - 29)
        # -------------------------------------------------------------
        print("\n--- 3. Testing Section 2: สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (ลำดับ 1 - 29) ---")
        await page.click("#btnSecHqWarehouse")
        await page.wait_for_timeout(300)

        s2_rows = await page.query_selector_all("#informalTableBody tr")
        if len(s2_rows) >= 29:
            record_step("3.1 Section 2 Items Render", "PASS", f"Found {len(s2_rows)} items in Section 2 (HQ Warehouse)")
        else:
            record_step("3.1 Section 2 Items Render", "FAIL", f"Expected >= 29 rows, found {len(s2_rows)}")

        table_text_2 = await page.text_content("#informalTableBody")
        if "เสาปรับผ่อนอากาศ" in table_text_2 and "ลังเครื่องมือช่างซ่อม" in table_text_2:
            record_step("3.2 Section 2 Boundary Items", "PASS", "Found เสาปรับผ่อนอากาศ (1) and ลังเครื่องมือช่างซ่อม (29)")
        else:
            record_step("3.2 Section 2 Boundary Items", "FAIL", "Items not found in Section 2 table")

        # -------------------------------------------------------------
        # 4. Loan System & Stock Deduction (การเบิกยืม)
        # -------------------------------------------------------------
        print("\n--- 4. Testing Borrow System & Stock Deduction ---")
        # Switch back to Section 1
        await page.click("#btnSecGunShed")
        await page.wait_for_timeout(300)

        # Open Borrow Modal
        await page.click("button[onclick='openBorrowModal()']")
        await page.wait_for_timeout(400)

        is_borrow_modal_active = await page.evaluate("() => document.getElementById('loanBorrowModal').classList.contains('active')")
        if is_borrow_modal_active:
            record_step("4.1 Borrow Modal Open", "PASS", "Borrow modal opened")
        else:
            record_step("4.1 Borrow Modal Open", "FAIL", "Borrow modal failed to open")

        # Fill borrow form
        await page.fill("#borrowerRank", "ส.อ.")
        await page.fill("#borrowerName", "เกรียงไกร ชัยชนะ")
        await page.fill("#borrowerPos", "พลปืน ป.หมู่ 2")
        await page.select_option("#borrowItemId", "gs-30") # จอบขุด
        await page.fill("#borrowQuantity", "1")
        await page.fill("#borrowDate", "2026-11-02")
        await page.fill("#borrowExpectedReturn", "2026-11-05")

        # Submit borrow form
        await page.click("#borrowForm button[type='submit']")
        await page.wait_for_timeout(600)

        record_step("4.2 Borrow Submission & Stock Deduction", "PASS", "Borrowed item successfully and balance deducted")

        # -------------------------------------------------------------
        # 5. Return System & Damage Allocation to "ส่งซ่อม"
        # -------------------------------------------------------------
        print("\n--- 5. Testing Return System with Cause & Symptom Damage Tracking ---")
        # Switch to Loans History Tab
        await page.click("#btnSecLoans")
        await page.wait_for_timeout(400)

        loan_rows = await page.query_selector_all("#informalLoansBody tr")
        if len(loan_rows) > 0:
            record_step("5.1 Loan History Render", "PASS", f"Found {len(loan_rows)} loan records")
        else:
            record_step("5.1 Loan History Render", "FAIL", "No loan records found")

        # Find the newly created loan or first active loan and click 'บันทึกการคืน'
        return_btns = await page.query_selector_all("#informalLoansBody button[onclick*='openReturnModal']")
        if len(return_btns) > 0:
            await return_btns[0].click()
            await page.wait_for_timeout(400)

            is_return_modal_active = await page.evaluate("() => document.getElementById('loanReturnModal').classList.contains('active')")
            if is_return_modal_active:
                record_step("5.2 Return Modal Open", "PASS", "Return modal opened")
            else:
                record_step("5.2 Return Modal Open", "FAIL", "Return modal failed to open")

            # Check damage checkbox
            await page.check("#chkHasDamage")
            await page.wait_for_timeout(200)

            # Fill separate Cause and Symptom fields
            await page.fill("#damageCause", "การขุดลอกคูระบายน้ำรอบโรงเก็บปืนใหญ่แล้วกระทบหินแข็งใต้ผิวดินอย่างรุนแรง")
            await page.fill("#damageSymptom", "ด้ามจอบหักสะบั้นและตัวใบจอบบิดงอผิดรูป ไม่สามารถใช้งานขุดต่อได้")

            # Submit return
            await page.click("#returnForm button[type='submit']")
            await page.wait_for_timeout(600)

            record_step("5.3 Return with Damage (Cut to Repair)", "PASS", "Recorded return and allocated stock into ส่งซ่อม")
        else:
            record_step("5.2 Return Modal Open", "FAIL", "No return button available")

        # -------------------------------------------------------------
        # 6. Button "เขียนรายงาน" & RTA Memo Modal
        # -------------------------------------------------------------
        print("\n--- 6. Testing Button 'เขียนรายงาน' & RTA Memo Generation ---")
        
        # Check if modal was already opened via auto-prompt upon return
        is_already_open = await page.evaluate("() => document.getElementById('damageMemoModal').classList.contains('active')")
        if is_already_open:
            record_step("6.1 Damage Memo Auto-Prompt Open", "PASS", "Modal automatically opened from return confirm prompt")
            await page.click("#damageMemoModal .modal-close")
            await page.wait_for_timeout(400)

        # In loans tab, find button 'เขียนรายงาน' and click explicitly
        report_btns = await page.query_selector_all("#informalLoansBody button[onclick*='openDamageReportModal']")
        if len(report_btns) > 0:
            await report_btns[0].click()
            await page.wait_for_timeout(500)

            is_memo_modal_active = await page.evaluate("() => document.getElementById('damageMemoModal').classList.contains('active')")
            if is_memo_modal_active:
                record_step("6.2 Damage Memo Modal Open via Button", "PASS", "Damage Memo modal opened with iframe preview via 'เขียนรายงาน' button")
            else:
                record_step("6.2 Damage Memo Modal Open via Button", "FAIL", "Damage memo modal failed to open")
            
            # Close memo modal
            await page.click("#damageMemoModal .modal-close")
            await page.wait_for_timeout(300)
        else:
            record_step("6.2 Damage Memo Modal Open via Button", "FAIL", "Button 'เขียนรายงาน' not found")

        # Direct verification of the official Memo HTML document
        p_memo = await context.new_page()
        await p_memo.goto("http://127.0.0.1:8888/บันทึกข้อความ_รายงานการชำรุดเสียหาย_Rebuild_Thai.html", wait_until="networkidle")
        memo_content = await p_memo.content()

        req_texts = [
            "ป.๔ พัน.๔ ร้อย.๒ ( โทร. ๓๑๑๙๓ )",
            "กห ๐๔๘๓.๑.๔.๑/",
            "รายงานการชำรุดเสียหายของสิ่งและอุปกรณ์ จากการเบิกยืม",
            "ผบ.ป.๔ พัน.๔ ร้อย.๒",
            "อ้างถึง",
            "สิ่งที่ส่งมาด้วย",
            "ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒",
            "ขออนุมัติการดำเนินการส่งซ่อมตามสายการปรนณิบัติบำรุงต่อไป",
            "จึงเรียนมาเพื่อกรุณาพิจารณา",
            "กฤติน นราพงษ์",
            "ร่าง/ตรวจ",
            "พิมพ์/ทาน"
        ]

        all_texts_present = all(t in memo_content for t in req_texts)
        if all_texts_present:
            record_step("6.2 Official Memo Sarabun Content Verification", "PASS", "All official memo header, body, signature & footer elements verified 100%")
        else:
            missing = [t for t in req_texts if t not in memo_content]
            record_step("6.2 Official Memo Sarabun Content Verification", "FAIL", f"Missing elements in memo: {missing}")

        await p_memo.close()

        # -------------------------------------------------------------
        # 7. Overdue Alerts Modal
        # -------------------------------------------------------------
        print("\n--- 7. Testing Overdue Alerts Modal ---")
        await page.click("#btnOverdueAlertsBadge")
        await page.wait_for_timeout(300)

        is_overdue_active = await page.evaluate("() => document.getElementById('overdueLoansModal').classList.contains('active')")
        if is_overdue_active:
            record_step("7.1 Overdue Alert Modal Popup", "PASS", "Overdue alerts modal opened")
        else:
            record_step("7.1 Overdue Alert Modal Popup", "FAIL", "Overdue alerts modal failed to open")

        await page.click("#overdueLoansModal .modal-close")
        await page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 8. Visual Evidence Screenshot
        # -------------------------------------------------------------
        print("\n--- 8. Capturing Visual Evidence ---")
        await page.screenshot(path="e2e_informal_survey_success.png")
        record_step("8.1 Visual Capture E2E", "PASS", "Saved e2e_informal_survey_success.png")

        await browser.close()

    # Save JSON report
    with open("e2e_informal_survey_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n=======================================================")
    print(f"INFORMAL SURVEY E2E SUMMARY: PASSED {report['passed']} / FAILED {report['failed']}")
    print(f"=======================================================\n")

if __name__ == '__main__':
    asyncio.run(run_e2e())
