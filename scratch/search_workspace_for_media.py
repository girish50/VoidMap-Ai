import os

ids = ["1780369962610", "1780372388831", "1780372529488", "1780451055514", "1780451570442"]
workspace_dir = r"e:\VoidMap ai"

for root, dirs, files in os.walk(workspace_dir):
    # Skip backend/node_modules, frontend/node_modules, .git
    if "node_modules" in root or ".git" in root:
        continue
        
    for file in files:
        if file.endswith((".py", ".md", ".json", ".js", ".jsx", ".html", ".css", ".txt")):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                found = [i for i in ids if i in content]
                if found:
                    print(f"Found {found} in file: {file_path}")
            except Exception as e:
                pass
