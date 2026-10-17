# 🔄 PROJECT ARCHITECTURAL FLOW & DATA PIPELINE (PROJECT_FLOW.md)
> **Language Mandate:** 100% English Version for Context Window Preservation  
> **System:** Royal Thai Army Production Document & Armament Inventory Suite (WEPAPP / HOWWIZZER)  
> **Last Updated:** 2026-10-17  

---

## 🏗️ High-Level System Interaction Map

```mermaid
graph TD
    User["👤 User / Quartermaster"] -->|HTTP / Local Browser| UI["🌐 Frontend Interface (FastAPI / Jinja2)"]
    UI -->|API Requests| Backend["⚙️ Backend Controller (backend/app.py)"]
    
    subgraph "Core Business Logic & Services"
        Backend --> Service["📦 Equipment Damage Service (informal_equipment_service.py)"]
        Service --> SSOT["📋 SSOT JSON Blueprint (table_layout_damage_memo.json)"]
        Service --> SigEngine["✍️ Universal Signature Engine (signature_engine.py)"]
        Service --> ThaiEngine["🇹🇭 Thai Typography Engine (thai_typography_engine.py)"]
    end

    subgraph "Dual-Copy Document Rendering Pipeline"
        SSOT --> RenderEngine["🖨️ Document Compiler"]
        SigEngine --> RenderEngine
        ThaiEngine --> RenderEngine
        RenderEngine --> Original["📄 Original Copy (Clean Memo)"]
        RenderEngine --> DualCopy["📑 Dual Copy (with Staff Review Footer)"]
    end

    subgraph "Multi-Format Export Targets"
        RenderEngine --> HTML["🌐 HTML (300 DPI Print CSS)"]
        RenderEngine --> DOCX["📝 Word (.docx)"]
        RenderEngine --> XLSX["📊 Excel (.xlsx preserved numbers)"]
    end

    subgraph "Production Cloud Deployment"
        Git["🐙 GitHub (palaside/HOWWIZZER)"] --> Vercel["▲ Vercel Cloud Serverless (api/index.py)"]
        Vercel --> Live["🚀 Live Production (howwizzer-five.vercel.app)"]
    end
```

---

## 🔄 Step-by-Step End-to-End Processing Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as Quartermaster / User
    participant Web as Web Dashboard
    participant API as FastAPI Backend (backend/app.py)
    participant Svc as Equipment Service
    participant Sig as Signature Engine
    participant Vercel as Vercel Edge CDN

    User->>Web: 1. Fill damage report form (upload_form.html)
    Web->>API: 2. Submit form payload (Borrower, Item, Cause, Signer)
    API->>Svc: 3. Resolve Blueprint and Thai Calendar dates
    Svc->>Sig: 4. Construct Universal Red Line Signature block
    Sig-->>Svc: 5. Return strictly aligned signature markup
    Svc-->>API: 6. Compile Dual-Copy Memo (Page 1: Original, Page 2: Copy)
    API-->>Web: 7. Deliver high-fidelity HTML preview
    User->>Web: 8. Trigger Print / PDF export (window.print)
    Note over Web: 9. 300 DPI Print-Grade CSS applied with Zero Overflow
    API->>Vercel: 10. Automated Serverless execution via Cloud
```

---

## ⚖️ Business Logic Constraints & Invariants

1. **Working Day Signature Rule:**
   - Official memorandum submission and signature dates must strictly fall between **Monday and Thursday** (excluding official holidays and never on Fridays).
2. **Universal Red Line Signature Rule:**
   - The end period `.` of the rank MUST align vertically with the opening parenthesis `(` of the name (`right: 100%`).
   - Rank is positioned above the signature line (`bottom: calc(100% + 18px)`).
   - In portrait memos, the signature block is indented **130 mm** from the left page margin and spaced **5 Enters** below the concluding paragraph.
3. **Dual-Copy Package Constraint:**
   - Every memo compile command outputs both the Original copy (no staff footer) and the Staff Copy (with the 4-column dual-axis review footer).
4. **Thai Typography Standard:**
   - Primary font: `TH Sarabun PSK` (Bold 600 for headings, Thin 300 for body texts and inspection results).
   - Zero-Width Space insertion prevents word-breaking halfway through syllables.
5. **Vercel Serverless Bundle Limit:**
   - Lambda package must remain under **225 MB** by excluding dev/testing packages (`pytest`) and heavy static documentation directories from deployment.
