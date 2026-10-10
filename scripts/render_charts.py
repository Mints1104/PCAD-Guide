"""Render the guide's chart examples: every ```python block that is directly followed by an
image line ![alt](images/name.png) is run, and the figure it draws is saved to
content/guide/images/name.png. build.mjs inlines those images into the page.

Usage: python scripts/render_charts.py [block5.md ...]
"""

import os
import re
import sys
import tempfile
import traceback
import warnings
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt  # noqa: E402

GUIDE = Path(__file__).resolve().parent.parent / "content" / "guide"
IMAGES = GUIDE / "images"
PAIR = re.compile(r"```python\n((?:(?!```).)*?)```[ \t]*\n\s*!\[[^\]]*\]\(images/([\w.-]+\.png)\)", re.S)


def main():
    files = sys.argv[1:] or sorted(p.name for p in GUIDE.glob("*.md"))
    IMAGES.mkdir(exist_ok=True)
    rendered = failed = 0
    for name in files:
        text = (GUIDE / name).read_text(encoding="utf-8")
        for m in PAIR.finditer(text):
            code, image = m.group(1), m.group(2)
            line = text[: m.start()].count("\n") + 1
            plt.close("all")
            cwd = os.getcwd()
            # Run in a scratch folder so any savefig() inside the example lands there.
            with tempfile.TemporaryDirectory() as scratch:
                os.chdir(scratch)
                try:
                    exec(compile(code, f"{name}:{line}", "exec"), {"__name__": "__main__"})
                    if not plt.get_fignums():
                        raise RuntimeError("the example drew no figure")
                    plt.gcf().savefig(IMAGES / image, dpi=100, bbox_inches="tight")
                    rendered += 1
                    print(f"{name}:{line} -> images/{image}")
                except Exception:  # noqa: BLE001
                    failed += 1
                    print(f"ERROR {name}:{line}\n{traceback.format_exc(limit=3)}")
                finally:
                    os.chdir(cwd)
    print(f"rendered {rendered} chart(s), {failed} problem(s)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
