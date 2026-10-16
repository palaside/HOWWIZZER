import os
import json
from pathlib import Path

appdata = os.environ.get("APPDATA")
updated = []

# 1. Global VS Code settings
if appdata:
    code_user_settings = Path(appdata) / "Code" / "User" / "settings.json"
    if code_user_settings.exists():
        try:
            with open(code_user_settings, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["liveServer.settings.port"] = 8000
            with open(code_user_settings, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            updated.append(str(code_user_settings))
        except Exception as e:
            print("Error updating Code User settings:", e)

# 2. Workspace settings
workspace_settings = Path(__file__).resolve().parent.parent / ".vscode" / "settings.json"
workspace_settings.parent.mkdir(parents=True, exist_ok=True)
try:
    data = {}
    if workspace_settings.exists():
        with open(workspace_settings, "r", encoding="utf-8") as f:
            data = json.load(f)
    data["liveServer.settings.port"] = 8000
    with open(workspace_settings, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    updated.append(str(workspace_settings))
except Exception as e:
    print("Error updating workspace settings:", e)

print("Updated settings in:", updated)
