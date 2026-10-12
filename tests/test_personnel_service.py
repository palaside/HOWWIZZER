import pytest
from backend.services.personnel_service import (
    get_personnel_by_role,
    update_personnel_role,
    inject_signers_into_template
)

def test_get_battery_commander():
    signer = get_personnel_by_role("commander_battery")
    assert "rank" in signer
    assert "name" in signer
    assert "position" in signer
    assert signer["position"] == "ผบ.ร้อย.พล.รพศ.๑"

def test_update_and_persist_signer():
    original = get_personnel_by_role("commander_battery")
    updated = update_personnel_role("commander_battery", "ร.อ.", "สมชาย รักสงบ", "ผบ.ร้อย.พล.รพศ.๑")
    assert updated["name"] == "สมชาย รักสงบ"
    # Restore original for cleanliness
    update_personnel_role("commander_battery", original["rank"], original["name"], original["position"])

def test_inject_signers_into_template_payload():
    payload = {
        "title": "รายงานประจำสัปดาห์",
        "signature_blocks": [
            {"role_binding": "commander_battery"}
        ]
    }
    hydrated = inject_signers_into_template(payload)
    assert hydrated["signature_blocks"][0]["name"] != ""
    assert hydrated["signature_blocks"][0]["rank"] != ""
