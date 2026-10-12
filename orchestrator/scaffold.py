import os, json, pathlib

def build_tree(root_path):
    tree = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_path = os.path.relpath(dirpath, root_path)
        for d in dirnames:
            tree.append({"type": "dir", "path": os.path.join(rel_path, d).replace('\\', '/')})
        for f in filenames:
            full = os.path.join(dirpath, f)
            size = os.path.getsize(full)
            tree.append({"type": "file", "path": os.path.join(rel_path, f).replace('\\', '/'), "size": size})
    return tree

if __name__ == "__main__":
    root = r"d:/Project/WEPAPP/next-app"
    tree = build_tree(root)
    out_path = r"d:/Project/WEPAPP/orchestrator/state/scaffold.json"
    pathlib.Path(os.path.dirname(out_path)).mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)
    print(f"Scaffold JSON written to {out_path}")
