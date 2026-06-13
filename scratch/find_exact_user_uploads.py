import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
ids = ["1780369962610", "1780372388831", "1780372529488", "1780451055514", "1780451570442"]

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        source = obj.get("source", "")
        type_ = obj.get("type", "")
        content = obj.get("content", "")
        
        # Check if user message or if has image ID and is from USER
        if "USER" in str(source) or type_ == "USER_INPUT":
            found_ids = [i for i in ids if i in line or i in content]
            if found_ids:
                print(f"Step {obj.get('step_index')}: User uploaded {found_ids}")
                print(f"Text content: {content.strip()}")
                print("-" * 50)
