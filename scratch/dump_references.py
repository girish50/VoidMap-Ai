import json
import os

def main():
    log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
    out_path = r"C:\Users\GIRISH\.gemini\antigravity\scratch\image_log.txt"
    if not os.path.exists(log_path):
        print("Transcript log path not found.")
        return
        
    ids = ["1780369962610", "1780372388831", "1780372529488", "1780451055514", "1780451570442"]
    
    print("Dumping transcript matches to scratch...")
    with open(log_path, "r", encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            
            for image_id in ids:
                if image_id in line:
                    out.write(f"=== MATCH for {image_id} in Step {obj.get('step_index')} ({obj.get('type')}) ===\n")
                    content = obj.get("content", "")
                    if content:
                        lines = content.split("\n")
                        for l in lines:
                            if image_id in l:
                                out.write(f"  TEXT: {l.strip()}\n")
                    for tc in obj.get("tool_calls", []):
                        if image_id in str(tc):
                            out.write(f"  TOOL CALL: {tc.get('name')} with args: {tc.get('args')}\n")
                    out.write("\n")
    print(f"Finished. Saved to {out_path}")

if __name__ == "__main__":
    main()
