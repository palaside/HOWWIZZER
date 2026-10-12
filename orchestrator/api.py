from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In‑memory store for phase approvals
_phase_approvals: Dict[int, bool] = {}

@app.get('/hello')
def read_root():
    return {'message': 'Hello from FastAPI'}

class ApprovalRequest(BaseModel):
    approve: bool

@app.get('/pause/{phase}')
def get_pause(phase: int):
    """Return the current approval status for a given phase. If not set, status is pending."""
    approved = _phase_approvals.get(phase)
    if approved is None:
        return {"phase": phase, "status": "pending"}
    return {"phase": phase, "status": "approved" if approved else "rejected"}

@app.post('/pause/{phase}')
def set_pause(phase: int, req: ApprovalRequest):
    """Set approval result for a phase. Stores the boolean in memory."""
    _phase_approvals[phase] = req.approve
    return {"phase": phase, "approved": req.approve}

