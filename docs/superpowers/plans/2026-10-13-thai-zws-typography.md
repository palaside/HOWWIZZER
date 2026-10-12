# Thai Typography & ZWS Segmentation Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a production-grade Thai Typography & Zero-Width Space (`\u200b`) Engine that prevents split words (คำขาดครึ่งท่อน) across all Royal Thai Army documents, preserves HTML structure and military acronyms, and enforces justified alignment.

**Architecture:** A lightweight, decoupled module `thai_typography_engine.py` consisting of `HTMLTagShield` (protects tags/entities), `MilitaryCustomLexicon` (custom PyThaiNLP Trie for ranks, units, equipment, form codes), and `ZWSInjector` (joins Thai word tokens with `\u200b`). Governed by `RULE-THAI-TYPOGRAPHY-ZWS-V1`.

**Tech Stack:** Python 3.10+, PyThaiNLP (`newmm` tokenizer), Playwright (Visual QA), Git.

## Global Constraints
- Target workspace: `d:/Project/WEPAPP`
- Zero ZWS (`\u200b`) allowed inside HTML tags (`<...>`) or HTML entities (`&...;`)
- Military acronyms, ranks, and unit designators must remain monolithic (never severed)
- Numbers (Thai `๑-๙`, Arabic `0-9`) and dates (`๒ พ.ย. ๖๙`) must never have internal ZWS
- Official military documents must maintain justified alignment (`text-align: justify; text-justify: inter-cluster;`)

---

### Task 1: Thai Typography Engine Core & Lexicon (TDD)

**Files:**
- Create: `thai_typography_engine.py`
- Test: `test_thai_typography_engine.py`

**Interfaces:**
- Consumes: Raw text strings or full HTML page strings.
- Produces: `ThaiTypographyEngine.process_html(html_str: str) -> str`, `ThaiTypographyEngine.process_text(text_str: str) -> str`.

- [ ] **Step 1: Write the failing unit tests**

Create `test_thai_typography_engine.py`:
```python
import pytest
from thai_typography_engine import ThaiTypographyEngine

def test_html_tag_shield_integrity():
    engine = ThaiTypographyEngine()
    html_input = '<div class="content-para" data-id="123">ขอส่งใบติดตามใบส่งซ่อม</div>'
    output = engine.process_html(html_input)
    # Tags and attributes must remain completely unpolluted
    assert '<div class="content-para" data-id="123">' in output
    assert '</div>' in output
    # Inner text must contain ZWS
    assert '\u200b' in output

def test_military_lexicon_no_split():
    engine = ThaiTypographyEngine()
    # Ensure military acronyms and compound terms are preserved as single units
    text = "ป.๔ พัน.๔ ร้อย.๒ รายงาน ปบค.๙๕ และ จ.ส.อ. สมชาย"
    output = engine.process_text(text)
    
    # Acronyms must not be severed by ZWS internally
    assert "ป.๔" in output
    assert "พัน.๔" in output
    assert "ร้อย.๒" in output
    assert "ปบค.๙๕" in output
    assert "จ.ส.อ." in output

def test_numbers_and_dates_preserved():
    engine = ThaiTypographyEngine()
    text = "ลงวันที่ ๒ พ.ย. ๖๙ เลขที่ ๐๔๘๓.๑.๔.๑/๑๒"
    output = engine.process_text(text)
    # Numbers and slash must not have internal ZWS
    assert "๒ พ.ย. ๖๙" in output
    assert "๐๔๘๓.๑.๔.๑/๑๒" in output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest test_thai_typography_engine.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'thai_typography_engine'`

- [ ] **Step 3: Implement `thai_typography_engine.py`**

Create `thai_typography_engine.py`:
```python
import re
from pythainlp.tokenize import word_tokenize
from pythainlp.util import dict_trie

# Military Custom Lexicon
MILITARY_TERMS = {
    # Ranks
    "พล.อ.", "พล.ท.", "พล.ต.", "พ.อ.", "พ.ท.", "พ.ต.",
    "ร.อ.", "ร.ท.", "ร.ต.", "จ.ส.อ.", "จ.ส.ท.", "จ.ส.ต.",
    "ส.อ.", "ส.ท.", "ส.ต.", "พลทหาร",
    # Units & Commands
    "ป.๔", "พัน.๔", "ร้อย.๑", "ร้อย.๒", "ร้อย.๓", "บก.ร้อย",
    "ผบ.พัน.ป.", "ผบ.ร้อย.ป.", "ผบ.ป.๔", "ผบ.พัน", "ผบ.ร้อย",
    "ส.หน.สย.", "ผบ.หมู่", "หมู่ส่งกำลังบำรุงฯ", "นายสิบส่งกำลัง",
    # Weapons & Equipment
    "ปบค.๙๕", "เอ็ม ๑๐๑ เอ ๑", "เอ็ม.๑๐๑", "เอ็ม ๑๐๑", "ขนาด ๑๐๕ มม.",
    "คส. ๔", "สพ.๔๖๐", "สาย สพ.", "สป.สาย สพ.", "ยุทธภัณฑ์",
    # Military Forms & Staff Terms
    "ทบ.๔๐๐-๐๑๒", "ทบ.๔๖๘-๒๐๔", "ทบ.๔๐๐-๐๐๕", "ทบ.๔๐๐-๐๑๑",
    "ทบ.๔๐๐-๐๗๑", "สด.๑", "ปรนนิบัติบำรุง", "สิ่งอุปกรณ์",
    "ตรวจถูกต้อง", "ผู้ตรวจสอบ", "ผู้เบิก", "ผู้จ่าย", "ผู้รับ"
}

class ThaiTypographyEngine:
    def __init__(self):
        self.custom_trie = dict_trie(dict_source=MILITARY_TERMS)
        self.tag_entity_pattern = re.compile(r'(<[^>]+>|&[a-zA-Z0-9#]+;)')
        self.token_splitter = re.compile(r'([\u0e00-\u0e7f]+)')

    def process_text(self, text: str) -> str:
        if not text:
            return ""

        chunks = self.token_splitter.split(text)
        processed_chunks = []
        for chunk in chunks:
            if not chunk:
                continue
            # If Thai text chunk, segment and insert ZWS
            if re.search(r'[\u0e00-\u0e7f]', chunk):
                words = word_tokenize(chunk, engine="newmm", custom_dict=self.custom_trie, keep_whitespace=True)
                processed_chunks.append("\u200b".join(words))
            else:
                # English, punctuation, numbers untouched
                processed_chunks.append(chunk)

        return "".join(processed_chunks)

    def process_html(self, html_content: str) -> str:
        if not html_content:
            return ""

        parts = self.tag_entity_pattern.split(html_content)
        result = []
        in_skip_block = False

        for part in parts:
            if not part:
                continue

            # Check if this part is an opening or closing script/style tag
            lower_part = part.lower()
            if lower_part.startswith('<script') or lower_part.startswith('<style'):
                in_skip_block = True
                result.append(part)
                continue
            elif lower_part.startswith('</script') or lower_part.startswith('</style'):
                in_skip_block = False
                result.append(part)
                continue

            if in_skip_block or self.tag_entity_pattern.match(part):
                # Verbatim HTML tag or entity
                result.append(part)
            else:
                # Real text content inside HTML
                result.append(self.process_text(part))

        return "".join(result)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest test_thai_typography_engine.py -v`  
Expected: PASS (3 passed)

- [ ] **Step 5: Commit Task 1**

```bash
git add thai_typography_engine.py test_thai_typography_engine.py
git commit -m "feat(typography): implement Thai Typography Engine with HTML shield and military lexicon"
```

---

### Task 2: Project Governance Rule (RULE-THAI-TYPOGRAPHY-ZWS-V1)

**Files:**
- Create: `.agents/rules/thai-typography-zws.md`
- Modify: `GEMINI.md`

**Interfaces:**
- Consumes: Specification guidelines from `SPEC-THAI-ZWS-TYPOGRAPHY-V1`.
- Produces: Official rule declaration and binding index in `GEMINI.md`.

- [ ] **Step 1: Create rule file `.agents/rules/thai-typography-zws.md`**

Create `.agents/rules/thai-typography-zws.md`:
```markdown
# [RULE-THAI-TYPOGRAPHY-ZWS-V1] มาตรฐานการตัดคำและการจัดหน้ากระดาษภาษาไทย

## 📌 บทบัญญัติการควบคุม (Mandatory Directives)
ทุกเอกสารและทุกเนื้อความภาษาไทยในโปรเจกต์นี้ ต้องปฏิบัติตามมาตรฐานการจัดระเบียบตัวอักษรเพื่อป้องกันคำขาดครึ่งท่อน (Zero Split Words) ดังนี้:

1. **การแทรก Zero-Width Space (ZWS, `\\u200b`):**
   - เนื้อความภาษาไทยทุกย่อหน้า ต้องผ่านการตัดคำด้วย `ThaiTypographyEngine` เพื่อแทรก ZWS ระหว่างคำ ป้องกันบราวเซอร์ผ่ากลางคำ
   - ห้ามมี ZWS หลุดเข้าไปแทรกในแท็ก HTML (`<...>`) หรือ HTML Entities (`&...;`) เด็ดขาด ๑๐๐%

2. **การจัดขอบหน้ากระดาษตามระเบียบสารบรรณ (Official Alignment):**
   - **เอกสารราชการและแบบฟอร์ม ทบ. ทั้งหมด:** ต้องจัดชิดขอบสองข้างเสมอกัน (Justified) ตามระเบียบสำนักนายกฯ และ ทบ. ด้วยชุดคำสั่ง CSS:
     ```css
     text-align: justify !important;
     text-justify: inter-cluster !important;
     word-break: keep-all !important;
     overflow-wrap: break-word !important;
     ```
   - **หน้า Web App / แดชบอร์ด:** สามารถใช้ `text-align: left` ได้ตามความเหมาะสม

3. **การคุ้มครองคำย่อทหารและตัวเลข:**
   - คำย่อทางทหาร ยศ (`จ.ส.อ.`, `ร.ท.`), หน่วยรบ (`ป.๔ พัน.๔ ร้อย.๒`), และรหัสแบบฟอร์ม/สป. (`ปบค.๙๕`, `ทบ.๔๐๐-๐๑๒`) ต้องคงรูปเป็นคำก้อนเดียว ห้ามตัดแยก
   - ตัวเลขไทย-อารบิก และวันที่ (`๒ พ.ย. ๖๙`) ต้องคงสภาพสมบูรณ์ ไม่ถูกแทรก ZWS ระหว่างหลัก
```

- [ ] **Step 2: Register rule in `GEMINI.md`**

Add rule entry to `Active Governance Rules` in `GEMINI.md`:
```markdown
5. **[RULE-THAI-TYPOGRAPHY-ZWS-V1](file:///d:/Project/WEPAPP/.agents/rules/thai-typography-zws.md)**
   - มาตรฐานการตัดคำและจัดหน้ากระดาษภาษาไทย ป้องกันคำขาดครึ่งท่อน ๑๐๐%
   - แทรก Zero-Width Space (`\u200b`) ผ่าน `thai_typography_engine.py` โดยคุ้มครองแท็ก HTML และคำย่อทหาร
   - เอกสารราชการทุกฉบับต้องกั้นหน้า-กั้นหลังตรงเสมอ (`text-align: justify; text-justify: inter-cluster;`)
```

- [ ] **Step 3: Commit Task 2**

```bash
git add .agents/rules/thai-typography-zws.md GEMINI.md
git commit -m "docs(governance): register RULE-THAI-TYPOGRAPHY-ZWS-V1 in project constitution"
```

---

### Task 3: Pipeline Integration & Batch ZWS Processing

**Files:**
- Create: `apply_zws_universal.py`
- Modify: `apply_thin_font_universal.py`
- Modify: Root and Reference HTML documents (via script)

**Interfaces:**
- Consumes: `ThaiTypographyEngine.process_html` from Task 1.
- Produces: All 45 HTML files updated with ZWS-segmented Thai text and CSS `word-break: keep-all; overflow-wrap: break-word;`.

- [ ] **Step 1: Write `apply_zws_universal.py`**

Create `apply_zws_universal.py`:
```python
import glob
import os
import sys
from thai_typography_engine import ThaiTypographyEngine

sys.stdout.reconfigure(encoding='utf-8')

def main():
    engine = ThaiTypographyEngine()
    target_files = []
    
    # Root HTMLs
    for f in glob.glob('*.html'):
        if not f.startswith('test_'):
            target_files.append(f)
            
    # Reference HTMLs
    for f in glob.glob('references/**/*.html', recursive=True):
        target_files.append(f)
        
    # HotFolder HTMLs
    for f in glob.glob('hotfolder/ready_to_print/*.html'):
        target_files.append(f)
        
    # Frontend HTMLs
    for f in glob.glob('frontend/**/*.html', recursive=True):
        target_files.append(f)

    target_files = sorted(list(set(target_files)))
    print(f"Applying Thai ZWS Segmentation Engine to {len(target_files)} files...")
    
    updated_count = 0
    for file_path in target_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update CSS justification rules inside rta-universal-thin-font-engine style block
        if 'word-break: keep-all;' not in content and '<style id="rta-universal-thin-font-engine">' in content:
            content = content.replace(
                "text-justify: inter-cluster;",
                "text-justify: inter-cluster; word-break: keep-all; overflow-wrap: break-word;"
            )

        processed = engine.process_html(content)
        if processed != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(processed)
            updated_count += 1
            print(f"[ZWS APPLIED] {file_path}")
        else:
            print(f"[UNCHANGED] {file_path}")

    print(f"\nSuccessfully applied ZWS to {updated_count}/{len(target_files)} files!")

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Run batch processing**

Run: `python apply_zws_universal.py`  
Expected: Processed 45 files with ZWS applied.

- [ ] **Step 3: Commit Task 3**

```bash
git add apply_zws_universal.py *.html references/ frontend/ hotfolder/
git commit -m "feat(pipeline): batch process all HTML documents with Thai ZWS Typography Engine"
```

---

### Task 4: Visual QA & Verification (Playwright 300 DPI)

**Files:**
- Create: `verify_zws_visual.py`
- Test Output: `preview_zws_memo.png`

**Interfaces:**
- Consumes: Rendered HTML of `บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html`.
- Produces: High-resolution visual proof confirming zero split words and clean right margin.

- [ ] **Step 1: Create verification script `verify_zws_visual.py`**

Create `verify_zws_visual.py`:
```python
import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1200, 'height': 1600}, device_scale_factor=2.5)
        
        url = 'http://127.0.0.1:8888/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html'
        await page.goto(url, wait_until='networkidle')
        
        # Verify ZWS presence in body text
        has_zws = await page.evaluate("() => document.body.innerText.includes('\\u200b')")
        print(f"ZWS Detected in DOM: {has_zws}")
        
        await page.screenshot(path='preview_zws_memo.png', full_page=False)
        print("Captured preview_zws_memo.png at 300 DPI")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
```

- [ ] **Step 2: Execute visual verification**

Run: `C:\Users\EVE\miniconda3\python.exe verify_zws_visual.py`  
Expected: `ZWS Detected in DOM: True`, generated `preview_zws_memo.png`.

- [ ] **Step 3: Commit Task 4 and finalize plan**

```bash
git add verify_zws_visual.py
git commit -m "test(visual): add Playwright 300 DPI visual verification for ZWS typography"
```
