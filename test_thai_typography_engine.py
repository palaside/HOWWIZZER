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
