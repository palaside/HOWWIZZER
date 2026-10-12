import pytest
from datetime import date
from pathlib import Path
from backend.services.doc_generation_service import (
    run_scheduled_generation,
    get_generation_checklist,
    inject_inventory_data_into_html,
    HOTFOLDER_OUT
)

def test_generation_checklist_structure():
    checklist = get_generation_checklist("2026-10")
    assert isinstance(checklist, list)
    assert len(checklist) > 0
    item = checklist[0]
    assert "template_id" in item
    assert "title" in item
    assert "status" in item

def test_scheduled_generation_produces_dual_copies_and_300dpi_preview(tmp_path):
    target = date(2026, 10, 16)  # Friday -> adjusted submission date is Thursday Oct 15
    results = run_scheduled_generation(target, output_root=tmp_path)
    assert len(results) > 0
    for res in results:
        assert res["status"] == "GENERATED"
        # Must produce BOTH Original (_ฉบับจริง.html) and File Copy (_สำเนาคู่ฉบับ.html)
        orig_p = Path(res["original_html_path"])
        copy_p = Path(res["copy_html_path"])
        assert orig_p.exists()
        assert copy_p.exists()
        assert orig_p.name.endswith("_ฉบับจริง.html")
        assert copy_p.name.endswith("_สำเนาคู่ฉบับ.html")
        assert "preview_path" in res
        assert Path(res["preview_path"]).exists()
        
        # Check copy text has '(สำเนาคู่ฉบับ)' and staff initials with Thursday date (๑๕ ต.ค. ๖๙)
        copy_text = copy_p.read_text(encoding="utf-8")
        orig_text = orig_p.read_text(encoding="utf-8")
        assert "สำเนาคู่ฉบับ" in copy_text
        assert "สำเนาคู่ฉบับ" not in orig_text
        
        # Rule 6: Submission date is Thursday 15 Oct, NOT Friday 16 Oct
        assert "๑๕" in copy_text
        assert "ต.ค. ๖๙" in copy_text
        # Original hides or strips memo-footer-staff block
        assert "memo-footer-staff" not in orig_text or "display: none" in orig_text

def test_inventory_data_injection():
    mock_html = """
    <table class="inventory-table">
        <tr data-item="GUN-105">
            <td class="col-item">ปบค.๙๕</td>
            <td class="col-recv"></td>
            <td class="col-issue"></td>
            <td class="col-balance"></td>
        </tr>
    </table>
    """
    mock_inventory = {
        "summary": {
            "GUN-105": {
                "received": 12,
                "issued": 2,
                "balance": 10
            }
        }
    }
    injected = inject_inventory_data_into_html(mock_html, mock_inventory)
    assert "๑๐" in injected  # Thai digit for 10
    assert "๑๒" in injected  # Thai digit for 12
    assert "๒" in injected   # Thai digit for 2

