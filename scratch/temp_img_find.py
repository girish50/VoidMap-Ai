import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
        
        # Check if the step has tool_calls
        tool_calls = obj.get("tool_calls", [])
        for tc in tool_calls:
            if tc.get("name") == "generate_image":
                print(f"Step {obj.get('step_index')}: generate_image -> {tc.get('args')}")
            elif "media__" in str(tc):
                print(f"Step {obj.get('step_index')}: tool {tc.get('name')} -> {tc.get('args')}")
        
        # Check if there is output from generate_image in the status or content
        content = obj.get("content", "")
        if "media__" in content and obj.get("source") == "SYSTEM":
            print(f"Step {obj.get('step_index')} (SYSTEM): {content[:300]}")
