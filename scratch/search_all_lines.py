import json
import os

def main():
    log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
    out_path = r"e:\VoidMap ai\scratch\image_log_detail.txt"
    if not os.path.exists(log_path):
        print("Transcript log path not found.")
        return
        
    ids = ["1780372388831", "1780372529488", "1780451055514", "1780451570442"]
    
    print("Dumping detailed matches to scratch...")
    with open(log_path, "r", encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
        for line_num, line in enumerate(f, 1):
            for image_id in ids:
                if image_id in line:
                    try:
                        obj = json.loads(line)
                    except Exception:
                        out.write(f"Line {line_num} contains raw {image_id} (json invalid)\n\n")
                        continue
                    
                    # If this step is a user message, system message, or model response,
                    # print details
                    out.write(f"=== STEP {obj.get('step_index')} ({obj.get('source')} - {obj.get('type')}) ===\n")
                    content = obj.get("content", "")
                    if content:
                        # Print surrounding text (10 lines before/after matching line)
                        lines = content.split("\n")
                        for idx, l in enumerate(lines):
                            if image_id in l:
                                start = max(0, idx - 5)
                                end = min(len(lines), idx + 6)
                                out.write(f"--- Context for {image_id} ---\n")
                                for i in range(start, end):
                                    prefix = ">>> " if i == idx else "    "
                                    out.write(f"{prefix}{lines[i]}\n")
                                out.write("-------------------------\n")
                    
                    # Check in tool_calls
                    for tc in obj.get("tool_calls", []):
                        if image_id in str(tc):
                            out.write(f"  TOOL CALL: {tc.get('name')}\n")
                            out.write(f"  ARGS: {json.dumps(tc.get('args'))}\n")
                    out.write("\n")
    print(f"Finished. Saved to {out_path}")

if __name__ == "__main__":
    main()
