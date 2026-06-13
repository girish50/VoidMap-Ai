import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
ids = ["1780369962610", "1780372388831", "1780372529488", "1780451055514", "1780451570442"]

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        content = obj.get("content", "")
        source = obj.get("source")
        type_ = obj.get("type")
        step = obj.get("step_index")
        
        # Check if any ID is in the content
        found = [i for i in ids if i in content]
        if found:
            # We want model responses or planner outputs, not tool calls/outputs
            if source == "MODEL":
                print(f"\n=========================================\n=== Step {step} ({source} - {type_}) found={found} ===")
                # Print lines containing the ID or describing it
                lines = content.split("\n")
                for idx, l in enumerate(lines):
                    if any(i in l for i in ids):
                        start = max(0, idx - 3)
                        end = min(len(lines), idx + 4)
                        for i in range(start, end):
                            prefix = ">>> " if i == idx else "    "
                            print(f"{prefix}{lines[i]}")
