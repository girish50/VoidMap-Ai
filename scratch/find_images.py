import json
import os

def main():
    log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
    if not os.path.exists(log_path):
        print("Transcript log path not found.")
        return
        
    print("Searching transcript for image generation details...")
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            
            # Check if generate_image was called
            tool_calls = obj.get("tool_calls", [])
            for tc in tool_calls:
                if tc.get("name") == "generate_image":
                    args = tc.get("args", {})
                    print(f"--- STEP {obj.get('step_index')} ---")
                    print(f"Image Name: {args.get('ImageName')}")
                    print(f"Prompt: {args.get('Prompt')}")
                    
            # Also check system logs or model logs outputting image details
            if obj.get("source") == "SYSTEM" and "media__" in line:
                # If there are system messages about files created
                pass

if __name__ == "__main__":
    main()
