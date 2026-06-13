import json
import os

def main():
    log_path = r"C:\Users\GIRISH\.gemini\antigravity\brain\c5698f8d-4ed7-4537-8d5c-e97dbb5b9ab9\.system_generated\logs\transcript.jsonl"
    if not os.path.exists(log_path):
        print("Transcript log path not found.")
        return
        
    ids = ["1780372388831", "1780372529488", "1780451055514", "1780451570442"]
    
    print("Searching transcript for image context...")
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            
            # Check if any ID is in the text of the line
            found_id = None
            for image_id in ids:
                if image_id in line:
                    found_id = image_id
                    break
                    
            if found_id:
                source = obj.get("source")
                type_ = obj.get("type")
                step = obj.get("step_index")
                
                # We only want model responses or planner outputs which explain things
                if source == "MODEL" and type_ == "PLANNER_RESPONSE":
                    print(f"\n=========================================")
                    print(f"STEP {step} - MODEL RESPONSE")
                    print(f"=========================================")
                    print(obj.get("content", ""))
                    print("\n")

if __name__ == "__main__":
    main()
