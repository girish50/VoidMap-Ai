import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
ids = ["1780372388831", "1780372529488", "1780451055514", "1780451570442"]

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        # We want to find steps where the source is USER and some image ID is mentioned in the entire json string,
        # but let's look at the fields inside the json object.
        if obj.get("source") == "USER_EXPLICIT" or obj.get("source") == "USER" or obj.get("type") == "USER_INPUT":
            for i in ids:
                if i in line:
                    print(f"=== STEP {obj.get('step_index')} (source={obj.get('source')}) ===")
                    print(json.dumps(obj, indent=2)[:2000])
                    print("="*60)
                    break
