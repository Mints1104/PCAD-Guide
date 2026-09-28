"""Compile question sources (content/questions/src/block*.py) into content/questions/block*.json.

A source file defines QUESTIONS, built with the Q() helper from qhelp.py. Authoring in Python keeps
code snippets readable (triple-quoted, no JSON escaping); the build and the app only read JSON.

Usage: python scripts/compile_questions.py
"""

import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "questions" / "src"
OUT = ROOT / "content" / "questions"

sys.path.insert(0, str(SRC))


def main():
    total = 0
    for path in sorted(SRC.glob("block*.py")):
        questions = runpy.run_path(str(path))["QUESTIONS"]
        (OUT / f"{path.stem}.json").write_text(json.dumps(questions, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        total += len(questions)
        print(f"{path.stem}: {len(questions)} questions")
    print(f"total: {total}")


if __name__ == "__main__":
    main()
