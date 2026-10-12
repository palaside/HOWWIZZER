import pytest
from pathlib import Path
from datetime import date
from backend.services.external_intake_service import (
    scan_and_ingest_hotfolder,
    classify_external_doc,
    check_external_cadence_gaps
)

def test_external_ingest_regex_match(tmp_path):
    # Setup test file that matches regex
    folder_in = tmp_path / "FolderIN"
    folder_in.mkdir(parents=True, exist_ok=True)
    valid_file = folder_in / "รายงานอัคคีภัย_ประจำเดือน_2026-10.pdf"
    valid_file.write_text("DUMMY PDF CONTENT", encoding="utf-8")
    
    results = scan_and_ingest_hotfolder(folder_in=folder_in)
    assert len(results) == 1
    res = results[0]
    assert res["status"] == "INGESTED"
    assert res["doc_type"] == "FIRE_SAFETY"
    assert res["period_key"] == "2026-10"

def test_external_ingest_fallback_unclassified_and_one_click_classification(tmp_path):
    # Setup file that does NOT match standard regex (Requirement 4)
    folder_in = tmp_path / "FolderIN"
    folder_in.mkdir(parents=True, exist_ok=True)
    odd_file = folder_in / "รายงานดับเพลิง_กองร้อยพิเศษ_ฉบับด่วน.pdf"
    odd_file.write_text("DUMMY ODD PDF", encoding="utf-8")
    
    results = scan_and_ingest_hotfolder(folder_in=folder_in)
    assert len(results) == 1
    res = results[0]
    # Fallback to UNCLASSIFIED_EXTERNAL with alert for 1-click dashboard action
    assert res["doc_type"] == "UNCLASSIFIED_EXTERNAL"
    assert res["status"] == "ACTION_REQUIRED"
    assert "alert" in res
    
    # Test 1-click manual classification by admin
    classified = classify_external_doc(
        filename=odd_file.name,
        doc_type="FIRE_SAFETY",
        period_key="2026-10"
    )
    assert classified["doc_type"] == "FIRE_SAFETY"
    assert classified["period_key"] == "2026-10"
    assert classified["status"] == "CLASSIFIED"

def test_cadence_gap_detection():
    # Detect overdue external reports
    gaps = check_external_cadence_gaps(current_date=date(2026, 10, 15))
    assert isinstance(gaps, list)
    assert len(gaps) > 0
    # Every gap record should have doc_type, expected_cadence, and status
    first_gap = gaps[0]
    assert "doc_type" in first_gap
    assert "expected_period" in first_gap
    assert first_gap["status"] in ["RECEIVED", "OVERDUE"]
