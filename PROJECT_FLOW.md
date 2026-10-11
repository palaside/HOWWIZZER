# 🔄 PROJECT FLOW: WEPAPP
> **Language:** English (AI Context Inheritance Standard)  
> **Architecture Pattern:** Multi-Tier SSOT Compiler & Cross-Platform Forensic Engine  
> **Revision:** 2026-10-12  

---

## 🏛️ System Architecture Diagram

```mermaid
graph TD
    subgraph Data Layer [Single Source of Truth Layer]
        JSON[table_layout_*.json<br>Structured Field Data]
        ASSETS[Image Assets & Logos<br>garuda_tr.png, photos]
    end

    subgraph Core Engine Layer [Compilation & Governance Engines]
        SIG_ENG[signature_engine.py<br>Universal Red Line Standard]
        PAGEFIT[PageFit Tuning Protocol<br>Zero-Overflow 4D Micro-Budget]
        BUILDER[build_superclone_*.py<br>Master Document Compiler]
    end

    subgraph Rendering & Target Layer [Tri-Format Production Targets]
        HTML[HTML Production Page<br>OpenType Font Engine & CSS Print]
        DOCX[Word .docx Document<br>Tab Stop Right-Anchor Axis]
        XLSX[Excel .xlsx Workbook<br>Split-Cell & Thai Numeral Masking]
    end

    subgraph Verification Layer [Visual QA & Automated Verification]
        PW[Playwright Headless Browser<br>2D Pixel-Level Capture]
        QA[Quality Assurance Checks<br>Single-Page Fit & Alignment Pass]
        REF[references/approved_*/<br>Gold Standard Manifest Repository]
    end

    JSON --> BUILDER
    ASSETS --> BUILDER
    SIG_ENG --> BUILDER
    PAGEFIT --> BUILDER

    BUILDER --> HTML
    BUILDER --> DOCX
    BUILDER --> XLSX

    HTML --> PW
    PW --> QA
    QA -->|Passed 100%| REF
```

---

## 🔁 Step-by-Step Execution Workflow

1. **Phase 1: Input Specification Intake**
   - User inputs specific form requirements or structural modification rules.
   - System checks `GEMINI.md` governance rules (`RULE-PROD-DOC-ENGINE-V1`, `RULE-UNIVERSAL-SIGNATURE-BLOCK-V1`, `RULE-PAGEFIT-TUNING-V1`).

2. **Phase 2: Schema Modeling (SSOT)**
   - All variable fields (memo numbers, dates, topics, inspection findings, signer names/ranks) are isolated into `table_layout.json`.
   - Structural parameters remain strictly separated from volatile content.

3. **Phase 3: Multi-Platform Compilation**
   - **HTML Engine:** Renders `@page` responsive stylesheets, sets Thai OpenType numeral feature tags (`locl`, `numr`), and anchors signature elements via `right: 100%`.
   - **DOCX Engine:** Uses `python-docx` to construct native paragraphs, tables, and tab stops at the exact vertical Red Line axis.
   - **XLSX Engine:** Generates typed cells with openpyxl, formatting numbers with Thai localization tags (`[$-th-TH,26]#,##0.00`).

4. **Phase 4: Visual QA & Zero-Overflow Validation**
   - Playwright captures high-resolution screenshots of every page.
   - Computer vision algorithms analyze vertical projection to ensure 100% zero-overflow across standard A4 boundaries.

5. **Phase 5: Governance Cataloging**
   - User reviews and approves the output (`PASS 100%`).
   - Package is archived under `references/approved_<name>/` with a signed `REFERENCE_MANIFEST.md` and indexed in `GEMINI.md`.
