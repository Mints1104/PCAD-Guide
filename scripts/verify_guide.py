"""Check the guide's worked examples: every ```python block that is directly followed by a
```text block is run, and its printed output must match the text block exactly.

Usage: python scripts/verify_guide.py [block1.md ...]
"""

import contextlib
import io
import os
import re
import sys
import traceback
import warnings
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

GUIDE = Path(__file__).resolve().parent.parent / "content" / "guide"
PAIR = re.compile(r"```python\n((?:(?!```).)*?)```[ \t]*\n\s*```text\n((?:(?!```).)*?)```", re.S)


def norm(s):
    return "\n".join(line.rstrip() for line in s.strip("\n").split("\n")).strip()


def main():
    files = sys.argv[1:] or sorted(p.name for p in GUIDE.glob("*.md"))
    checked = failed = 0
    for name in files:
        text = (GUIDE / name).read_text(encoding="utf-8")
        for m in PAIR.finditer(text):
            code, expected = m.group(1), m.group(2)
            line = text[: m.start()].count("\n") + 1
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(compile(code, f"{name}:{line}", "exec"), {"__name__": "__main__"})
                got = norm(buf.getvalue())
                if got != norm(expected):
                    failed += 1
                    print(f"MISMATCH {name}:{line}\n--- expected\n{norm(expected)}\n--- got\n{got}\n")
            except Exception:  # noqa: BLE001
                failed += 1
                print(f"ERROR {name}:{line}\n{traceback.format_exc(limit=3)}")
            checked += 1
    print(f"checked {checked} example(s), {failed} problem(s)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
