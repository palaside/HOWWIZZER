# Design Specification: Thai Typography & ZWS Segmentation Engine

**Document ID:** `SPEC-THAI-ZWS-TYPOGRAPHY-V1`  
**Date:** 2026-10-13  
**Status:** Approved by User (Pending Plan & Execution)  
**Target:** RTA Military Document & HotFolder Engine (WEPAPP)

---

## 1. Executive Summary & Objective

In Royal Thai Army (RTA) official documents, line-breaking without word boundaries causes browsers and rendering engines to arbitrarily sever Thai words in the middle of syllables (e.g., breaking `กรุงเทพมหานคร` into `กรุงเทพม` on line 1 and `หานคร` on line 2, or splitting ranks like `ผู้บัง|คับบัญชา` and acronyms like `ปบค.|๙๕`).

This specification establishes a permanent, production-grade **Thai Typography & Zero-Width Space (ZWS, `\u200b`) Engine** that:
1. Injects invisible Zero-Width Space (`\u200b`) between natural Thai word boundaries using PyThaiNLP dictionary-based segmentation (`newmm`) enriched with a dedicated **Military Custom Lexicon**.
2. Protects HTML tags, attributes, entities, and numeric/date literals from ZWS pollution via an **HTML Tag & Entity Shield**.
3. Enforces official Thai military document justification (`text-align: justify; text-justify: inter-cluster;`) preventing jagged right margins while maintaining zero word splitting.
4. Formalizes project governance by registering **`RULE-THAI-TYPOGRAPHY-ZWS-V1`** in `.agents/rules/` and `GEMINI.md`.

---

## 2. Architecture & Component Design

The system is encapsulated in `thai_typography_engine.py` with three decoupled components:

```
+--------------------------------------------------------------+
|                    Input: Text or HTML Page                  |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| 1. HTMLTagShield                                             |
|    - Parses HTML into sequential tokens (Tag vs Text Node)   |
|    - Ignores <script>, <style>, HTML tags, attributes,       |
|      and entities (&nbsp;, &amp;, etc.)                      |
+--------------------------------------------------------------+
                               |
                               v (Only Text Nodes)
+--------------------------------------------------------------+
| 2. MilitaryCustomLexicon & Tokenizer                         |
|    - Preloads Thai military terms, ranks, units, form IDs    |
|    - Combines PyThaiNLP newmm engine with custom Trie        |
|    - Protects numbers (๑-๙, 0-9), dates, and abbreviations   |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| 3. ZWSInjector & Reassembler                                 |
|    - Inserts \u200b between segmented words                  |
|    - Reconstructs the sanitized HTML output                  |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|              Output: Flawless Typography HTML                |
+--------------------------------------------------------------+
```

### Component 1: `HTMLTagShield`
- **Responsibility:** Ensure zero ZWS characters penetrate HTML tags (e.g., `<div class="content-para">` must never become `<div class="con\u200btent-para">`).
- **Mechanism:**
  - Tokenizes string using regex `(<[^>]+>|&[a-zA-Z0-9#]+;)`.
  - Content matching tag or entity pattern is emitted verbatim without modification.
  - Raw text blocks outside tags are routed to the segmentation pipeline.

### Component 2: `MilitaryCustomLexicon`
- **Responsibility:** Prevent splitting of specialized military terms, ranks, unit designators, equipment names, and standard form codes.
- **Lexicon Registry:**
  - **Ranks:** `พล.อ.`, `พล.ท.`, `พล.ต.`, `พ.อ.`, `พ.ท.`, `พ.ต.`, `ร.อ.`, `ร.ท.`, `ร.ต.`, `จ.ส.อ.`, `จ.ส.ท.`, `จ.ส.ต.`, `ส.อ.`, `ส.ท.`, `ส.ต.`
  - **Units & Appointments:** `ป.๔`, `พัน.๔`, `ร้อย.๒`, `บก.ร้อย`, `ผบ.พัน`, `ผบ.ร้อย`, `ส.หน.สย.`, `ผบ.หมู่`, `หมู่ส่งกำลังบำรุงฯ`
  - **Equipment & Weapons:** `ปบค.๙๕`, `เอ็ม ๑๐๑ เอ ๑`, `ขนาด ๑๐๕ มม.`, `คส. ๔`, `สพ.๔๖๐`
  - **Forms & Terms:** `ทบ.๔๐๐-๐๑๒`, `ทบ.๔๖๘-๒๐๔`, `ทบ.๔๐๐-๐๐๕`, `สด.๑`, `ปรนนิบัติบำรุง`, `ยุทธภัณฑ์`, `สิ่งอุปกรณ์`, `ตรวจถูกต้อง`
- **Numeric Preservation:** Patterns matching Thai/Arabic numbers and punctuation sequences (e.g., `๐๔๘๓.๑.๔.๑/`, `๒ พ.ย. ๖๙`, `๑๐๕ มม.`) remain monolithic without internal ZWS.

### Component 3: `ZWSInjector`
- **Method Signature:** `ThaiTypographyEngine.process_html(html_content: str) -> str`
- **Behavior:** Segments text nodes using the lexicon-backed engine, joins word tokens with `\u200b` (U+200B), and preserves existing whitespaces.

---

## 3. Governance Rule: `RULE-THAI-TYPOGRAPHY-ZWS-V1`

A new permanent rule will be established in `.agents/rules/thai-typography-zws.md` and referenced in `GEMINI.md`:

1. **Zero Split Words Mandate:** All generated or updated Thai text paragraphs in military documents must be processed with ZWS word boundaries before final export.
2. **Strict Official Justification:**
   - Formal military documents (Memos, Inspection Reports, Survey Cards, Form 400 series) must always specify:
     ```css
     text-align: justify;
     text-justify: inter-cluster;
     word-break: keep-all;
     overflow-wrap: break-word;
     ```
   - Web application dashboard cards and UI controls may use `text-align: left`.
3. **Dual-Copy Engine Compatibility:** Both the "Original" (ฉบับจริง) and "Parallel Copy" (สำเนาคู่ฉบับ) must inherit identical typography treatment.

---

## 4. Verification & Testing Strategy

1. **Automated Unit Tests (`test_thai_typography_engine.py`):**
   - Verify HTML tag integrity (no ZWS injected inside `<...>` or `&...;`).
   - Verify military terms are treated as single tokens (`ป.๔ พัน.๔ ร้อย.๒`, `ปบค.๙๕`, `จ.ส.อ.`).
   - Verify numeric dates (`๒ พ.ย. ๖๙`) and official reference codes are not severed.
2. **Visual QA (Playwright 300 DPI):**
   - Render `บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html` before and after processing.
   - Inspect line break edges at right margin under 300 DPI (`device_scale_factor: 2.5`).
   - Confirm zero broken words and clean justified alignment.

---

## 5. Scope & Rollout Plan

- **In Scope:**
  - Module `thai_typography_engine.py`.
  - Rule `.agents/rules/thai-typography-zws.md` and `GEMINI.md` update.
  - Integration into document rebuilding and hotfolder generation scripts.
  - Test suite `test_thai_typography_engine.py`.
- **Out of Scope:**
  - Modifying non-Thai text strings or foreign language documents.
  - Modifying numerical data cells in raw `.xlsx` Excel spreadsheets.
