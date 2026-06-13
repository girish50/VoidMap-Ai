import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        step = obj.get("step_index")
        if 1121 <= step <= 1125:
            print(f"=== Step {step} (source={obj.get('source')}, type={obj.get('type')}) ===")
            print(obj.get("content", ""))
            print("="*60)
