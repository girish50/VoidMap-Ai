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
            
        for i in ids:
            if i in line:
                print(f"Step {obj.get('step_index')}: source={obj.get('source')}, type={obj.get('type')}")
                content = obj.get("content", "")
                if content:
                    # Print lines that contain the ID
                    for l in content.split("\n"):
                        if i in l:
                            print(f"  CONTENT: {l[:150].strip()}")
                for tc in obj.get("tool_calls", []):
                    if i in str(tc):
                        print(f"  TOOL_CALL: {tc.get('name')} -> {str(tc.get('args'))[:150]}")
