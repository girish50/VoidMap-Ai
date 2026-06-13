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
            
        content = obj.get("content", "")
        # Look for model responses that are planning or explaining
        if obj.get("source") == "MODEL" and obj.get("type") == "PLANNER_RESPONSE":
            for image_id in ids:
                if image_id in content:
                    print(f"\n=== Step {obj.get('step_index')} Model Explanation for {image_id} ===")
                    # print lines around the matching line in content
                    lines = content.split("\n")
                    for idx, l in enumerate(lines):
                        if image_id in l:
                            start = max(0, idx - 4)
                            end = min(len(lines), idx + 5)
                            for i in range(start, end):
                                prefix = ">>> " if i == idx else "    "
                                print(f"{prefix}{lines[i]}")
