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
    assert "ผบ.ร้อย" in signer["position"]

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

def test_get_eight_operators():
    from backend.services.personnel_service import get_operators, get_personnel_by_role
    operators = get_operators()
    assert isinstance(operators, list)
    assert len(operators) >= 9
    
    # Check slot 1: พ.ท. พรชัย มากเทพพงษ์ ผบ.พัน.ป.
    op1 = next(o for o in operators if o["slot"] == 1)
    assert op1["rank"] == "พ.ท."
    assert "พรชัย" in op1["name"]
    assert "ผบ.พัน" in op1["position"]
    
    # Check slot 2: ร.อ. กฤติน นราพงษ์ ผบ.ร้อย.ป.
    op2 = next(o for o in operators if o["slot"] == 2)
    assert op2["rank"] == "ร.อ."
    assert "กฤติน" in op2["name"]
    assert "ผบ.ร้อย" in op2["position"]

    # Check slot 3: จ.ส.อ. ณัฐชัย รักษาวงษ์ ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒
    op3 = next(o for o in operators if o["slot"] == 3)
    assert op3["rank"] == "จ.ส.อ."
    assert "ณัฐชัย" in op3["name"]
    assert "ส.หน.สย" in op3["position"]
    
    # Check slot 4: จ.ส.อ. วรนันท์ ศรีวารี ผบ.หมู่ ป.1
    op4 = next(o for o in operators if o["slot"] == 4)
    assert op4["rank"] == "จ.ส.อ."
    assert "วรนันท์" in op4["name"]
    assert "ผบ.หมู่ ป.1" in op4["position"]

    # Check slot 9: ส.อ. อภิวัฒน์ จันทร์ลอย ผบ.หมู่ ป.6
    op9 = next(o for o in operators if o["slot"] == 9)
    assert op9["rank"] == "ส.อ."
    assert "อภิวัฒน์" in op9["name"]
    assert "ผบ.หมู่ ป.6" in op9["position"]
    
    # Check role registry binding
    ops_chief = get_personnel_by_role("chief_operations")
    assert "ณัฐชัย" in ops_chief["name"]
    assert ops_chief["rank"] == "จ.ส.อ."

def test_update_operator():
    from backend.services.personnel_service import update_operator, get_operators
    updated = update_operator(slot=5, rank="จ.ส.ต.", name="ทดสอบ เปลี่ยนชื่อ", position="ผบ.หมู่ ป.2")
    assert updated["name"] == "ทดสอบ เปลี่ยนชื่อ"
    # Revert back
    update_operator(slot=5, rank="จ.ส.ต.", name="จุฑานนท์ คณฑา", position="ผบ.หมู่ ป.2")

