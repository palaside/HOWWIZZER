import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_personnel_endpoints():
    res = client.get("/api/v1/personnel")
    assert res.status_code == 200
    data = res.json()
    assert "roles" in data
    
    # Update role
    up_res = client.put("/api/v1/personnel/chief_maintenance", json={
        "rank": "จ.ส.อ.",
        "name": "ทดสอบ นามสมมุติ",
        "position": "จนท.ซ่อมบำรุงอาวุธ"
    })
    assert up_res.status_code == 200
    assert up_res.json()["name"] == "ทดสอบ นามสมมุติ"

def test_docs_checklist_and_generate():
    chk = client.get("/api/v1/docs/checklist")
    assert chk.status_code == 200
    assert isinstance(chk.json(), list)
    
    gen = client.post("/api/v1/docs/generate", json={"target_date": "2026-10-16"})
    assert gen.status_code == 200
    results = gen.json()["results"]
    assert len(results) > 0
    assert "submission_date" in results[0]
    # Synchronized submission date is Thursday Oct 15
    assert results[0]["submission_date"] == "2026-10-15"

def test_inventory_api():
    bal = client.get("/api/v1/inventory/balance")
    assert bal.status_code == 200
    assert "items" in bal.json()

def test_intake_and_gaps_api():
    scan = client.get("/api/v1/intake/scan")
    assert scan.status_code == 200
    
    gaps = client.get("/api/v1/intake/gaps?current_date=2026-10-16")
    assert gaps.status_code == 200
    assert isinstance(gaps.json(), list)
