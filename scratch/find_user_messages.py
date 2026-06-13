import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        source = obj.get("source")
        type_ = obj.get("type")
        content = obj.get("content", "")
        
        if "USER" in str(source) or type_ == "USER_INPUT":
            print(f"\n=== Step {obj.get('step_index')} User Input ===")
            print(content[:600]) # First 600 chars of user input
            # Check for attachments/media in this user step
            tool_calls = obj.get("tool_calls", [])
            if tool_calls:
                print(f"Tool calls: {tool_calls}")
