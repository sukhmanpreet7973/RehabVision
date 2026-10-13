import json
from datetime import datetime, timezone

input_file = "rehabvision_25_exercises.json"
output_file = "rehabvision_25_exercises_fixed.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

now = datetime.now(timezone.utc).isoformat()

for item in data:
    item["fields"]["created_at"] = now
    item["fields"]["updated_at"] = now

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Fixed JSON created successfully!")
print(f"Total exercises: {len(data)}")