import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path(__file__).parent.parent / "data" / "personnel_registry.json"

def load_registry() -> dict:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_registry(data: dict) -> None:
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_personnel_by_role(role_id: str) -> dict:
    data = load_registry()
    if role_id not in data.get("roles", {}):
        raise KeyError(f"Role {role_id} not found in personnel registry")
    return data["roles"][role_id]

def update_personnel_role(role_id: str, rank: str, name: str, position: str) -> dict:
    data = load_registry()
    if role_id not in data.get("roles", {}):
        raise KeyError(f"Role {role_id} not found")
    data["roles"][role_id].update({
        "rank": rank.strip(),
        "name": name.strip(),
        "position": position.strip(),
        "updated_at": datetime.now().isoformat()
    })
    save_registry(data)
    return data["roles"][role_id]

def inject_signers_into_template(template_data: dict) -> dict:
    data = load_registry()
    hydrated = json.loads(json.dumps(template_data))
    if "signature_blocks" in hydrated and isinstance(hydrated["signature_blocks"], list):
        for block in hydrated["signature_blocks"]:
            binding = block.get("role_binding")
            if binding and binding in data.get("roles", {}):
                role_info = data["roles"][binding]
                block["rank"] = role_info["rank"]
                block["name"] = role_info["name"]
                block["position"] = role_info["position"]
    return hydrated
