import os
import json
import pathlib
import requests
from datetime import datetime

# Base paths
ROOT = pathlib.Path(r"d:/Project/WEPAPP")
ORCH = ROOT / "orchestrator"
STATE = ORCH / "state"
LOGS = ORCH / "logs"
DOCS = ROOT / "docs"
NEXT_APP = ROOT / "next-app"

def save_state(phase: int, data: dict):
    """Save JSON state for a given phase."""
    STATE.mkdir(parents=True, exist_ok=True)
    out_path = STATE / f"phase_{phase}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[Phase {phase}] state saved to {out_path}")


def phase_1():
    # Scaffold already generated as scaffold.json in previous step
    scaffold_path = STATE / "scaffold.json"
    if not scaffold_path.exists():
        raise FileNotFoundError("scaffold.json not found – run scaffold phase first")
    save_state(1, {"scaffold": str(scaffold_path)})


def phase_2():
    pdf_text_path = STATE / "pdf_text.txt"
    if not pdf_text_path.exists():
        raise FileNotFoundError("pdf_text.txt not found – run extract_pdf phase first")
    # For demo, just store a snippet
    with pdf_text_path.open("r", encoding="utf-8") as f:
        snippet = f.read()[:500]
    save_state(2, {"pdf_snippet": snippet})


def phase_3():
    # Create zone folders and placeholder README.md
    zones = [
        "zone_A_Architecture_and_Inventory",
        "zone_B_Logic_Engine_and_Data",
        "zone_C_Design_and_Layout",
        "zone_D_Validation_Quality_and_Status",
        "zone_E_Operations_Security_and_Lifecycle",
    ]
    for zone in zones:
        zone_path = DOCS / zone
        zone_path.mkdir(parents=True, exist_ok=True)
        readme = zone_path / "README.md"
        if not readme.exists():
            readme.write_text(f"# {zone}\n\nThis folder contains files for {zone.replace('_', ' ')}.\n", encoding="utf-8")
    save_state(3, {"zones_created": zones})


def phase_4():
    # Generate simple architecture and DB schema files using pdf snippet
    pdf_snippet_path = STATE / "pdf_text.txt"
    snippet = ""
    if pdf_snippet_path.exists():
        snippet = pdf_snippet_path.read_text(encoding="utf-8")[:1000]
    arch_path = DOCS / "zone_A_Architecture_and_Inventory" / "architecture.md"
    db_path = DOCS / "zone_A_Architecture_and_Inventory" / "db_schema.sql"
    arch_path.write_text("# Architecture Overview\n\n" + snippet[:800] + "\n... (truncated)\n", encoding="utf-8")
    db_path.write_text("-- Simple DB schema generated for demo\nCREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);\n", encoding="utf-8")
    save_state(4, {"architecture": str(arch_path), "db_schema": str(db_path)})


def phase_5():
    # Create a sample React component stub
    comp_dir = NEXT_APP / "src" / "components"
    comp_dir.mkdir(parents=True, exist_ok=True)
    comp_path = comp_dir / "SampleComponent.jsx"
    comp_path.write_text(
        "import React from 'react';\n\nexport default function SampleComponent() {\n  return <div>Hello from SampleComponent</div>;\n}\n",
        encoding="utf-8",
    )
    save_state(5, {"component": str(comp_path)})


def phase_6():
    # Simple FastAPI endpoint (can be swapped for Express)
    api_path = ORCH / "api.py"
    api_path.write_text(
        "from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\nfrom typing import Dict\n\napp = FastAPI()\n\n# In‑memory store for phase approvals\n_phase_approvals: Dict[int, bool] = {}\n\n@app.get('/hello')\ndef read_root():\n    return {'message': 'Hello from FastAPI'}\n\nclass ApprovalRequest(BaseModel):\n    approve: bool\n\n@app.get('/pause/{phase}')\ndef get_pause(phase: int):\n    \"\"\"Return the current approval status for a given phase. If not set, status is pending.\"\"\"\n    approved = _phase_approvals.get(phase)\n    if approved is None:\n        return {\"phase\": phase, \"status\": \"pending\"}\n    return {\"phase\": phase, \"status\": \"approved\" if approved else \"rejected\"}\n\n@app.post('/pause/{phase}')\ndef set_pause(phase: int, req: ApprovalRequest):\n    \"\"\"Set approval result for a phase. Stores the boolean in memory.\"\"\"\n    _phase_approvals[phase] = req.approve\n    return {\"phase\": phase, \"approved\": req.approve}\n",
        encoding="utf-8",
    )
    save_state(6, {"api_file": str(api_path)})


def phase_7():
    # ORM model stub (SQLModel for demo)
    models_path = ORCH / "models.py"
    models_path.write_text(
        "from sqlmodel import SQLModel, Field\n\nclass User(SQLModel, table=True):\n    id: int = Field(default=None, primary_key=True)\n    name: str\n",
        encoding="utf-8",
    )
    save_state(7, {"models_file": str(models_path)})


def phase_8():
    # PyTest stub
    tests_dir = ORCH / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    test_path = tests_dir / "test_api.py"
    test_path.write_text(
        "import sys\nsys.path.append('..')\nfrom api import app\nfrom fastapi.testclient import TestClient\n\nclient = TestClient(app)\n\ndef test_hello():\n    response = client.get('/hello')\n    assert response.status_code == 200\n    assert response.json() == {'message': 'Hello from FastAPI'}\n",
        encoding="utf-8",
    )
    save_state(8, {"test_file": str(test_path)})


def phase_9():
    # GitHub Actions CI workflow (basic lint + test)
    workflow_dir = ROOT / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    ci_path = workflow_dir / "ci.yml"
    ci_path.write_text(
        "name: CI\n\non: [push, pull_request]\n\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Set up Python\n        uses: actions/setup-python@v4\n        with:\n          python-version: '3.13'\n      - name: Install deps\n        run: pip install fastapi sqlmodel pytest\n      - name: Run tests\n        run: pytest orchestrator/tests\n",
        encoding="utf-8",
    )
    save_state(9, {"ci_workflow": str(ci_path)})


def phase_10():
    # Final report linking artefacts
    report_path = DOCS / "final_report.md"
    links = []
    # collect key artefacts
    artefacts = [
        ("Scaffold JSON", STATE / "scaffold.json"),
        ("PDF Text", STATE / "pdf_text.txt"),
        ("Architecture MD", DOCS / "zone_A_Architecture_and_Inventory" / "architecture.md"),
        ("DB Schema", DOCS / "zone_A_Architecture_and_Inventory" / "db_schema.sql"),
        ("Sample Component", NEXT_APP / "src" / "components" / "SampleComponent.jsx"),
        ("API File", ORCH / "api.py"),
        ("ORM Models", ORCH / "models.py"),
        ("Test File", ORCH / "tests" / "test_api.py"),
        ("CI Workflow", ROOT / ".github" / "workflows" / "ci.yml"),
    ]
    for name, path in artefacts:
        if path.exists():
            rel = path.relative_to(ROOT).as_posix()
            links.append(f"- [{name}]({{file:///" + str(path).replace('\\', '/') + "}})")
    report_content = "# Final Report – Automated Orchestrator\n\nGenerated artefacts for the 10‑phase pipeline:\n\n" + "\n".join(links) + "\n\n*All files are located under the project root `d:/Project/WEPAPP`.\n"
    report_path.write_text(report_content, encoding="utf-8")
    save_state(10, {"final_report": str(report_path)})


def request_approval(phase: int):
    """Poll the FastAPI pause endpoint until approval is granted or rejected."""
    import time
    while True:
        try:
            resp = requests.get(f'http://127.0.0.1:8000/pause/{phase}')
            data = resp.json()
            status = data.get('status')
            if status == 'approved':
                print(f"[Phase {phase}] approved by human.")
                return True
            if status == 'rejected':
                print(f"[Phase {phase}] rejected by human. Stopping.")
                return False
            print(f"[Phase {phase}] awaiting human approval...")
            time.sleep(5)
        except Exception as e:
            print(f"Error checking approval for phase {phase}: {e}")
            time.sleep(5)


def main():
    start = datetime.now()
    print(f"🚀 Starting Automated Orchestrator – {start.isoformat()}")
    phases = [phase_1, phase_2, phase_3, phase_4, phase_5, phase_6, phase_7, phase_8, phase_9, phase_10]
    for i, fn in enumerate(phases, start=1):
        print(f"\n--- Phase {i} ---")
        try:
            fn()
            approved = request_approval(i)
            if not approved:
                print(f"[Phase {i}] stopped due to rejection.")
                break
        except Exception as e:
            print(f"[Phase {i}] ERROR: {e}")
            break
    end = datetime.now()
    print(f"\n✅ Finished at {end.isoformat()} (elapsed {end-start})")

if __name__ == "__main__":
    main()
