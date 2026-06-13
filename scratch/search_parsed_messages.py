import re

file_path = r"e:\VoidMap ai\scratch\user_messages_parsed.txt"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all blocks starting with === Step
steps = re.split(r"=== Step ", content)
ids = ["1780369962610", "1780372388831", "1780372529488", "1780451055514", "1780451570442"]

for step_block in steps:
    if not step_block.strip():
        continue
    
    # Check if any ID is in this block
    found = [i for i in ids if i in step_block]
    if found:
        # print first few lines of the block
        lines = step_block.split("\n")
        print(f"\n=========================================\n=== Step {lines[0]}")
        # print the rest of the block
        for line in lines[1:30]:
            print(line)
