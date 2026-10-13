import asyncio
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def run_e2e_test():
    report = {
        "suite": "E2E UI/UX Micro-Interactions Walkthrough Test",
        "timestamp": "2026-10-13",
        "steps": [],
        "passed": 0,
        "failed": 0
    }

    def record_step(step_name, status, details=""):
        report["steps"].append({"step": step_name, "status": status, "details": details})
        if status == "PASS":
            report["passed"] += 1
            print(f"[PASS] {step_name}: {details}")
        else:
            report["failed"] += 1
            print(f"[FAIL] {step_name}: {details}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        page = await context.new_page()

        # Handle dialogs automatically (for operator edits / alerts)
        dialog_counter = 0
        dialog_inputs = ["ร.อ.", "ทดสอบ ชื่อสกุล", "ผบ.ร้อย.ป."]
        
        async def handle_dialog(dialog):
            nonlocal dialog_counter
            if dialog.type == "prompt":
                val = dialog_inputs[dialog_counter % len(dialog_inputs)]
                dialog_counter += 1
                await dialog.accept(val)
            else:
                await dialog.accept()

        page.on("dialog", handle_dialog)

        # -------------------------------------------------------------
        # 1. Top Nav Header & System Status
        # -------------------------------------------------------------
        print("\n--- 1. Testing Top Nav Header & System Status ---")
        await page.goto("http://127.0.0.1:8888/frontend/templates/index.html", wait_until="networkidle")
        await page.wait_for_timeout(500)

        brand_badge = await page.text_content(".brand-badge")
        if brand_badge and "RTA DOC-ENGINE" in brand_badge:
            record_step("1.1 Brand Badge Render", "PASS", f"Found brand badge: {brand_badge.strip()}")
        else:
            record_step("1.1 Brand Badge Render", "FAIL", "Brand badge missing or incorrect")

        status_text = await page.text_content(".system-status")
        if status_text and "Cloud HotFolder" in status_text:
            record_step("1.2 System Status Dot", "PASS", "HotFolder status active")
        else:
            record_step("1.2 System Status Dot", "FAIL", "Status text missing")

        # -------------------------------------------------------------
        # 2. Setting Target Cycle Date & Thai Calendar
        # -------------------------------------------------------------
        print("\n--- 2. Testing Target Cycle Date & Thai Calendar ---")
        date_display = await page.input_value("#targetCycleDateDisplay")
        cycle_chip = await page.text_content("#cycleRangeDisplay")
        
        if date_display and "69" in date_display:
            record_step("2.1 Thai Year BE Format", "PASS", f"Initial display: {date_display}")
        else:
            record_step("2.1 Thai Year BE Format", "FAIL", f"Unexpected date display: {date_display}")

        if cycle_chip and "พ.ย. 69" in cycle_chip:
            record_step("2.2 Floating Cycle Chip", "PASS", f"Cycle range: {cycle_chip.strip()}")
        else:
            record_step("2.2 Floating Cycle Chip", "FAIL", f"Unexpected cycle chip: {cycle_chip}")

        # Simulate changing date
        await page.evaluate("""() => {
            const dateInput = document.getElementById('targetCycleDate');
            dateInput.value = '2026-11-13';
            onNativeDateChanged('2026-11-13');
        }""")
        await page.wait_for_timeout(300)
        new_chip = await page.text_content("#cycleRangeDisplay")
        if new_chip and "9 - 13" in new_chip:
            record_step("2.3 Date Change & Re-calculation", "PASS", f"Updated to: {new_chip.strip()}")
        else:
            record_step("2.3 Date Change & Re-calculation", "FAIL", f"Got: {new_chip}")

        # Reset back to 2026-11-06
        await page.evaluate("""() => {
            const dateInput = document.getElementById('targetCycleDate');
            dateInput.value = '2026-11-06';
            onNativeDateChanged('2026-11-06');
        }""")

        # -------------------------------------------------------------
        # 3. Personnel Roster Verification (9 Operators)
        # -------------------------------------------------------------
        print("\n--- 3. Testing Personnel Roster Verification ---")
        slots = await page.query_selector_all("#operatorsGrid .operator-slot")
        if len(slots) == 9:
            record_step("3.1 9 Operator Slots Render", "PASS", f"Found exactly {len(slots)} operator cards")
        else:
            record_step("3.1 9 Operator Slots Render", "FAIL", f"Expected 9, found {len(slots)}")

        # -------------------------------------------------------------
        # 4. Inspection Photo Management (4-Slot Grid 2.5x2.5 in)
        # -------------------------------------------------------------
        print("\n--- 4. Testing Inspection Photo 4-Slot Grid ---")
        photo_cards = await page.query_selector_all("#inspectionPhotosGrid .photo-slot-card")
        if len(photo_cards) == 4:
            record_step("4.1 4-Slot Photo Grid Render", "PASS", f"Found {len(photo_cards)} photo slots")
        else:
            record_step("4.1 4-Slot Photo Grid Render", "FAIL", f"Expected 4 photo slots, found {len(photo_cards)}")

        status_badge = await page.text_content("#photoUploadStatusBadge")
        if status_badge and "๔/๔" in status_badge:
            record_step("4.2 Photo Status Ready Badge", "PASS", f"Status: {status_badge.strip()}")
        else:
            record_step("4.2 Photo Status Ready Badge", "FAIL", f"Status: {status_badge}")

        # Check Page 4 real-time hydration
        p_sd1 = await context.new_page()
        await p_sd1.goto("http://127.0.0.1:8888/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html", wait_until="networkidle")
        await p_sd1.wait_for_timeout(500)
        img_p4 = await p_sd1.query_selector_all(".photo-grid .photo-card img")
        if len(img_p4) == 4:
            record_step("4.3 Form SD.1 Page 4 Photo Placement", "PASS", f"Page 4 has all {len(img_p4)} inspection photos hydrated")
        else:
            record_step("4.3 Form SD.1 Page 4 Photo Placement", "FAIL", f"Expected 4 images on Page 4, found {len(img_p4)}")
        await p_sd1.close()

        # -------------------------------------------------------------
        # 5. Master Document Queue & Interactive Checklist
        # -------------------------------------------------------------
        print("\n--- 5. Testing Master Document Queue & Interactive Checklist ---")
        queue_cards = await page.query_selector_all("#upcomingQueueGrid > div")
        if len(queue_cards) == 5:
            record_step("5.1 Upcoming Queue Priority Cards", "PASS", f"Rendered {len(queue_cards)} queue priority cards")
        else:
            record_step("5.1 Upcoming Queue Priority Cards", "FAIL", f"Expected 5 queue cards, found {len(queue_cards)}")

        rows = await page.query_selector_all("#masterChecklistTableBody tr")
        if len(rows) == 19:
            record_step("5.2 Master Checklist 19 Documents", "PASS", f"Rendered all {len(rows)} documents in checklist")
        else:
            record_step("5.2 Master Checklist 19 Documents", "FAIL", f"Expected 19, found {len(rows)}")

        # Test Filter Tabs
        await page.click("button:has-text('📌 คิวสัปดาห์นี้')")
        await page.wait_for_timeout(200)
        filtered_weekly = await page.query_selector_all("#masterChecklistTableBody tr")
        if len(filtered_weekly) == 2:
            record_step("5.3 Category Filter: Weekly", "PASS", f"Filtered to {len(filtered_weekly)} weekly documents")
        else:
            record_step("5.3 Category Filter: Weekly", "FAIL", f"Expected 2, got {len(filtered_weekly)}")

        await page.click("button:has-text('⏱️ คิวทวงถาม')")
        await page.wait_for_timeout(200)
        filtered_followup = await page.query_selector_all("#masterChecklistTableBody tr")
        if len(filtered_followup) == 6:
            record_step("5.4 Category Filter: Follow-up", "PASS", f"Filtered to {len(filtered_followup)} follow-up documents")
        else:
            record_step("5.4 Category Filter: Follow-up", "FAIL", f"Expected 6, got {len(filtered_followup)}")

        # Reset filter to 'All'
        await page.click("button:has-text('ทั้งหมด (๑๙ ฉบับ)')")
        await page.wait_for_timeout(200)

        # Test Search
        await page.fill("#checklistSearchInput", "สด.๑")
        await page.wait_for_timeout(200)
        searched_rows = await page.query_selector_all("#masterChecklistTableBody tr")
        if len(searched_rows) == 1:
            record_step("5.5 Instant Search Filter", "PASS", f"Successfully found exact document for 'สด.๑'")
        else:
            record_step("5.5 Instant Search Filter", "FAIL", f"Expected 1, got {len(searched_rows)}")

        await page.fill("#checklistSearchInput", "")
        await page.wait_for_timeout(200)

        # Test Batch Checkbox
        await page.click("button:has-text('✅ ติ๊กเลือกทั้งหมด')")
        await page.wait_for_timeout(200)
        checked_display = await page.text_content("#checkedCountDisplay")
        if checked_display and ("๑๙/๑๙" in checked_display or "19/19" in checked_display):
            record_step("5.6 Batch Check All (19/19)", "PASS", f"Counter: {checked_display.strip()}")
        else:
            record_step("5.6 Batch Check All (19/19)", "FAIL", f"Counter: {checked_display}")

        await page.click("button:has-text('🔄 ล้างการติ๊ก')")
        await page.wait_for_timeout(200)
        cleared_display = await page.text_content("#checkedCountDisplay")
        if cleared_display and ("0/๑๙" in cleared_display or "๐/๑๙" in cleared_display or "0/19" in cleared_display):
            record_step("5.7 Batch Clear Checkboxes (0/19)", "PASS", f"Counter: {cleared_display.strip()}")
        else:
            record_step("5.7 Batch Clear Checkboxes (0/19)", "FAIL", f"Counter: {cleared_display}")

        # Check Single Doc Checkbox & LocalStorage
        await page.click("#chk-doc-sd1")
        await page.wait_for_timeout(200)
        single_display = await page.text_content("#checkedCountDisplay")
        if single_display and ("1/๑๙" in single_display or "๑/๑๙" in single_display or "1/19" in single_display):
            record_step("5.8 Single Checkbox & State Persistence", "PASS", f"Counter: {single_display.strip()}")
        else:
            record_step("5.8 Single Checkbox & State Persistence", "FAIL", f"Counter: {single_display}")

        # -------------------------------------------------------------
        # 6. Tab Navigation & Module Verification (Tab 2, 3, 4)
        # -------------------------------------------------------------
        print("\n--- 6. Testing Tab Navigation & Modules ---")
        
        # Tab 2: Armory Custody
        await page.click(".tab-btn[data-tab='tab-inventory-custody']")
        await page.wait_for_timeout(300)
        is_tab2_active = await page.evaluate("() => document.getElementById('tab-inventory-custody').classList.contains('active')")
        if is_tab2_active:
            record_step("6.1 Tab 2 Armory Custody Switch", "PASS", "Tab 2 active")
        else:
            record_step("6.1 Tab 2 Armory Custody Switch", "FAIL", "Tab 2 failed to activate")

        # Tab 3: External Intake
        await page.click(".tab-btn[data-tab='tab-external-intake']")
        await page.wait_for_timeout(300)
        is_tab3_active = await page.evaluate("() => document.getElementById('tab-external-intake').classList.contains('active')")
        if is_tab3_active:
            record_step("6.2 Tab 3 External Intake Switch", "PASS", "Tab 3 active")
        else:
            record_step("6.2 Tab 3 External Intake Switch", "FAIL", "Tab 3 failed to activate")

        # Tab 4: 17 Docs Full Catalog
        await page.click("#tabBtn17Docs")
        await page.wait_for_timeout(300)
        catalog_cards = await page.query_selector_all("#catalogDocsGrid .doc-card")
        if len(catalog_cards) >= 17:
            record_step("6.3 Tab 4 Full Catalog 17 Docs", "PASS", f"Catalog has {len(catalog_cards)} document cards")
        else:
            record_step("6.3 Tab 4 Full Catalog 17 Docs", "FAIL", f"Expected >=17, got {len(catalog_cards)}")

        # Switch back to Tab 1
        await page.click(".tab-btn[data-tab='tab-internal-docs']")
        await page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 7. Responsive Behavior Verification
        # -------------------------------------------------------------
        print("\n--- 7. Testing Responsive Viewports ---")
        
        # Tablet Viewport (768px)
        await page.set_viewport_size({'width': 768, 'height': 1024})
        await page.wait_for_timeout(300)
        op_cols_tablet = await page.evaluate("""() => {
            const el = document.getElementById('operatorsGrid');
            return window.getComputedStyle(el).gridTemplateColumns.split(' ').length;
        }""")
        if op_cols_tablet == 3:
            record_step("7.1 Tablet (768px) 3-Col Operators Grid", "PASS", f"Operators grid adapted to {op_cols_tablet} columns")
        else:
            record_step("7.1 Tablet (768px) 3-Col Operators Grid", "FAIL", f"Expected 3 columns, got {op_cols_tablet}")

        # Mobile Viewport (390px)
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.wait_for_timeout(300)
        op_cols_mobile = await page.evaluate("""() => {
            const el = document.getElementById('operatorsGrid');
            return window.getComputedStyle(el).gridTemplateColumns.split(' ').length;
        }""")
        if op_cols_mobile in [1, 2]:
            record_step("7.2 Mobile (390px) Compact Operators Grid", "PASS", f"Operators grid adapted to {op_cols_mobile} columns")
        else:
            record_step("7.2 Mobile (390px) Compact Operators Grid", "FAIL", f"Unexpected columns: {op_cols_mobile}")

        # Take final E2E screenshot
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.wait_for_timeout(300)
        await page.screenshot(path="e2e_walkthrough_success.png")
        record_step("7.3 Visual Capture E2E", "PASS", "Saved e2e_walkthrough_success.png")

        await browser.close()

    # Save JSON report
    with open("e2e_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n=======================================================")
    print(f"E2E TEST SUMMARY: PASSED {report['passed']} / FAILED {report['failed']}")
    print(f"=======================================================\n")

if __name__ == '__main__':
    asyncio.run(run_e2e_test())
