"""Compile notebook sources (content/notebooks/src/nb[0-9]*.py) into content/notebooks/nb*.json.

A source file defines NOTEBOOK, built with NB() and T() from nbhelp.py.

Usage: python scripts/compile_notebooks.py
"""

import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "notebooks" / "src"
OUT = ROOT / "content" / "notebooks"

sys.path.insert(0, str(SRC))


def main():
    for old in OUT.glob("nb[0-9]*.json"):
        old.unlink()
    tasks = 0
    paths = sorted(SRC.glob("nb[0-9]*.py"))
    for path in paths:
        nb = runpy.run_path(str(path))["NOTEBOOK"]
        (OUT / f"{path.stem}.json").write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        tasks += len(nb["tasks"])
        print(f"{path.stem}: {nb['title']} ({len(nb['tasks'])} tasks)")
    print(f"total: {len(paths)} notebooks, {tasks} tasks")


if __name__ == "__main__":
    main()
