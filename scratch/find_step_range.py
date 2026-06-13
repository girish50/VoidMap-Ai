import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
out_path = r"e:\VoidMap ai\scratch\steps_1110_1120.txt"

with open(log_path, "r", encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        step = obj.get("step_index")
        source = obj.get("source")
        type_ = obj.get("type")
        content = obj.get("content", "")
        
        if 1110 <= step <= 1120:
            out.write(f"\n=========================================\n=== Step {step} ({source} - {type_}) ===\n")
            out.write(content + "\n")
            out.write("="*60 + "\n")
