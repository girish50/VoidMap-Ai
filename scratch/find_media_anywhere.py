import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        if "media__" in line:
            try:
                obj = json.loads(line)
            except Exception:
                continue
                
            print(f"Step {obj.get('step_index')}: source={obj.get('source')}, type={obj.get('type')}")
            # If it has content, print first line
            content = obj.get("content", "")
            if content:
                print(f"  CONTENT first line: {content.splitlines()[0][:120]}")
            # If it has tool_calls, print them
            for tc in obj.get("tool_calls", []):
                print(f"  TOOL_CALL: {tc.get('name')} -> {str(tc.get('args'))[:120]}")
