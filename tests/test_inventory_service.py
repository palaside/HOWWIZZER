import pytest
from backend.services.inventory_service import (
    request_loan,
    approve_loan,
    return_item,
    replace_damaged_item,
    get_inventory_balance,
    get_item_history
)

def test_loan_workflow_dual_control():
    # 1. Maker/Admin requests loan (Status: PENDING_APPROVAL)
    req = request_loan(
        item_id="GUN-105-01",
        borrower_name="ส.อ. สมเกียรติ สุขใจ",
        purpose="ยิงสนับสนุนการฝึก",
        requested_by="admin_warehouse"
    )
    assert req["status"] == "PENDING_APPROVAL"
    assert "request_id" in req
    
    # 2. Checker/Owner approves loan (Stock deducted, Status: BORROWED)
    approved = approve_loan(
        request_id=req["request_id"],
        approved_by="owner_commander"
    )
    assert approved["status"] == "BORROWED"
    
    # Check inventory balance: Available status updated
    bal = get_inventory_balance()
    item = next(i for i in bal["items"] if i["item_id"] == "GUN-105-01")
    assert item["status"] == "BORROWED"
    assert bal["summary"]["GUN-105"]["issued"] >= 1

def test_return_damaged_and_replacement_audit():
    # 1. Return item with damage notes
    ret = return_item(
        loan_id="loan_test_dam",
        item_id="GUN-105-02",
        is_damaged=True,
        damage_notes="ศูนย์เล็งแตกร้าว",
        receiver="owner_commander"
    )
    assert ret["status"] == "DAMAGED"
    assert ret["damage_notes"] == "ศูนย์เล็งแตกร้าว"
    
    # 2. Replace item with new serial number
    rep = replace_damaged_item(
        item_id="GUN-105-02",
        new_serial_no="SN-NEW-9988",
        replaced_by="owner_commander"
    )
    assert rep["status"] == "AVAILABLE"
    assert rep["serial_no"] == "SN-NEW-9988"
    
    # 3. Verify immutable history contains the damage and replacement audit logs
    hist = get_item_history("GUN-105-02")
    assert any("ศูนย์เล็งแตกร้าว" in h.get("notes", "") for h in hist)
    assert any("SN-NEW-9988" in h.get("notes", "") for h in hist)
