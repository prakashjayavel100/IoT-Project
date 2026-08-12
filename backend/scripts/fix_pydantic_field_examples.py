import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "app" / "schemas" / "device_schema.py"
text = path.read_text(encoding="utf-8")

pattern = re.compile(r",\s*example=(.+?)\)\s*$")

new_lines = []
changed = False
for line in text.splitlines(keepends=True):
    new_line = pattern.sub(r', json_schema_extra={"example":\1})', line)
    if new_line != line:
        changed = True
    new_lines.append(new_line)

if changed:
    path.write_text("".join(new_lines), encoding="utf-8")
    print(f"Updated {path}")
else:
    print("No changes made")
