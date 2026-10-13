# 🔄 PROJECT FLOW: WEPAPP
> **Language:** English (AI Context Inheritance Standard)  
> **Architecture Pattern:** Multi-Tier SSOT Compiler & Royal Thai Army Production Engine  
> **Revision:** 2026-10-14  

---

## 🏛️ System Architecture Diagram

```mermaid
graph TD
    subgraph Data Layer [Single Source of Truth Layer]
        INV_DB[informal_equipment_inventory.json<br>Real-time Inventory & Loans]
        MEMO_BP[table_layout_damage_memo.json<br>RTA Sarabun Page 29 Blueprint]
        TABLE_BP[table_layout_*.json<br>Approved Document Blueprints]
        ASSETS[garuda_vector_official.png<br>High-Res Military Emblems]
    end

    subgraph Service & Engine Layer [Core Processing Engines]
        INV_SRV[informal_equipment_service.py<br>Loan Tracking & Stock Management]
        MEMO_ENG[Damage Memo HTML Compiler<br>Dual-Copy & Staff Review Footer]
        TYPO_ENG[thai_typography_engine.py<br>Zero-Width Space ZWS Injection]
        SIG_ENG[signature_engine.py<br>Universal Red Line Standard]
        BIZ_ENG[business_day_engine.py<br>Official Mon-Thu Signing Cadence]
    end

    subgraph Presentation & Target Layer [Tri-Format & Web Presentation]
        FASTAPI[backend/app.py<br>FastAPI Application Server]
        WEB_UI[Frontend Web Dashboard<br>Inventory Tables & Live Previews]
        A4_PAGE1[Original Memo A4<br>Print-Grade 300 DPI Clean Copy]
        A4_PAGE2[Dual-Copy Memo A4<br>Copy Banner + 4-Col Staff Footer]
    end

    subgraph Verification & Mirror Layer [Quality Assurance & Archival]
        PLAYWRIGHT[Playwright Headless Engine<br>device_scale_factor=2.5 Validation]
        STATE_MIRROR[state/ Redundant Mirror<br>LATEST_CHECKPOINT.md & Behavior]
    end

    INV_DB --> INV_SRV
    MEMO_BP --> MEMO_ENG
    ASSETS --> MEMO_ENG

    INV_SRV --> MEMO_ENG
    BIZ_ENG --> MEMO_ENG
    SIG_ENG --> MEMO_ENG
    MEMO_ENG --> TYPO_ENG

    INV_SRV --> FASTAPI
    FASTAPI --> WEB_UI

    TYPO_ENG --> A4_PAGE1
    TYPO_ENG --> A4_PAGE2

    A4_PAGE1 --> PLAYWRIGHT
    A4_PAGE2 --> PLAYWRIGHT
    PLAYWRIGHT --> STATE_MIRROR
```

---

## 🔁 Step-by-Step Execution Workflow

1. **Step 1: Inventory Intake & Loan Tracking**
   - User or operator creates a loan record for equipment in Section 1 (Gun Shed) or Section 2 (HQ Warehouse).
   - System validates available stock balance and reserves quantities atomically in `informal_equipment_inventory.json`.

2. **Step 2: Return & Damage Assessment**
   - On item return, operator records condition:
     - **Normal Return:** Stock balance is restored to the primary storage location.
     - **Damaged Return:** Stock is moved to the repair track (`repair_amount`), recording `cause` and `symptom` separately.

3. **Step 3: Automated RTA Memo Generation**
   - Service loads `table_layout_damage_memo.json` based on *RTA Sarabun 2563 Appendix A Sub-Appendix 1 (Page 29)*.
   - Computes official signing date conforming to the Monday-Thursday business day rule.
   - Interpolates the 3-tier paragraph content (`paragraph_1_reason`, `paragraph_2_intention`, `paragraph_3_summary`).
   - Compiles dual-copy package (Original Copy + Dual Copy with staff review footer).

4. **Step 4: Typography & Micro-Layout Optimization**
   - `thai_typography_engine.py` inserts Zero-Width Space (`\u200b`) between Thai syllables, protecting military abbreviations and HTML tags.
   - Signature block positions the rank end dot exactly collinear with the open parenthesis of the signatory name (Universal Red Line Standard).

5. **Step 5: Visual QA Verification & Archival**
   - Headless browser renders output at 300 DPI (`device_scale_factor = 2.5`).
   - Ensures strict single-page boundary enforcement without overflow.
