#!/usr/bin/env python3
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / 'src'
LOCALE_DIR = SRC_DIR / 'locale'
POT_FILE = LOCALE_DIR / 'helwan_insight.pot'

# تأكد من وجود مجلد locale
LOCALE_DIR.mkdir(parents=True, exist_ok=True)

# Regex لالتقاط النصوص داخل _('...')
TRANSLATION_REGEX = re.compile(r"_\(\s*['\"](.+?)['\"]\s*\)")

entries = []
for py_file in SRC_DIR.rglob("*.py"):
    if py_file.name == "__init__.py":
        continue

    rel_path = py_file.relative_to(PROJECT_ROOT)
    with py_file.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            matches = TRANSLATION_REGEX.findall(line)
            for msg in matches:
                entries.append({
                    "file": rel_path.as_posix(),
                    "line": line_no,
                    "msg": msg
                })

# بناء محتوى ملف POT
with POT_FILE.open("w", encoding="utf-8") as f:
    f.write('# helwan_insight translation template\n')
    f.write('msgid ""\nmsgstr ""\n')
    f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
    f.write('"Language: \\n"\n\n')

    for entry in entries:
        f.write(f'#: {entry["file"]}:{entry["line"]}\n')
        f.write(f'msgid "{entry["msg"]}"\n')
        f.write('msgstr ""\n\n')

print(f"[✓] Translation template generated: {POT_FILE}")
