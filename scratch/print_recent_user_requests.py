import re

file_path = r"e:\VoidMap ai\scratch\user_messages_parsed.txt"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Split by "=== Step"
steps = re.split(r"=== Step ", content)
for step_block in steps:
    if not step_block.strip():
        continue
    
    first_line = step_block.split("\n")[0]
    step_num = int(re.search(r"^\d+", first_line).group())
    
    if step_num >= 400:
        print(f"\n=== Step {step_num} ===")
        # print the block using repr for safety, or print lines safely
        for line in step_block.split("\n")[1:25]:
            # print line safely
            print(line.encode('ascii', errors='replace').decode('ascii'))
