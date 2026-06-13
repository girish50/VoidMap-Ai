import json
import os

log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
out_path = r"e:\VoidMap ai\scratch\user_messages_parsed.txt"
ids = ["1780369962610", "1780372388831", "1780372529488", "1780451055514", "1780451570442"]

with open(log_path, "r", encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
    for line in f:
        try:
            obj = json.loads(line)
        except Exception:
            continue
            
        source = obj.get("source")
        type_ = obj.get("type")
        content = obj.get("content", "")
        step = obj.get("step_index")
        
        has_id = any(image_id in line for image_id in ids)
        
        if (source == "USER" or type_ == "USER_INPUT") or has_id:
            out.write(f"\n=== Step {step} : source={source}, type={type_} ===\n")
            out.write(content[:2000] + "\n")
            tool_calls = obj.get("tool_calls", [])
            for tc in tool_calls:
                out.write(f"  Tool: {tc.get('name')} -> {json.dumps(tc.get('args'))}\n")
