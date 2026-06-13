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
        source = obj.get("source")
        type_ = obj.get("type")
        content = obj.get("content", "")
        
        if 440 <= step <= 800:
            if "USER" in str(source) or type_ == "USER_INPUT":
                print(f"\n=========================================\n=== Step {step} (USER) ===")
                print(content.strip().encode('ascii', errors='replace').decode('ascii'))
                print("="*60)
