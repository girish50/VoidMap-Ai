import re

file_path = r"e:\VoidMap ai\frontend\src\components\Dashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Look for tabs state or activeTab
print("=== activeTab states and button text ===")
for match in re.finditer(r"activeTab\s*===?\s*['\"][^'\"]+['\"]", content):
    print(match.group())

# Find tab names
print("\n=== Tab elements ===")
for match in re.finditer(r"<button[^>]+onClick[^>]+activeTab[^>]+>([^<]+)</button>", content):
    print(match.group(1).strip())
