"""Check every notebook task with the same runner the site uses (src/runner.py).

For each task (in a chained notebook, after the solutions of the earlier tasks):
  - setup + solution + check must pass, with no error;
  - setup + starter + check must fail (so a check can never pass on untouched starter code).
Then the whole notebook runs top to bottom in one namespace (setup, then each solution and its
check), the way the downloaded .ipynb runs in Jupyter.

Usage: python scripts/verify_notebooks.py
"""

import contextlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from runner import _close_figures, run_cell  # noqa: E402


def sequential(nb):
    """Run the notebook as Jupyter would: one namespace, cells in order."""
    ns = {"__name__": "__main__"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(nb["setup"], ns)
        for t in nb["tasks"]:
            try:
                exec(t["solution"], ns)
                exec(t["check"], ns)
            except Exception as exc:
                return f"{t['id']}: {type(exc).__name__}: {exc}"
            finally:
                _close_figures()
    return None


def main():
    failures = []
    count = 0
    for path in sorted((ROOT / "content" / "notebooks").glob("nb*.json")):
        nb = json.loads(path.read_text(encoding="utf-8"))
        for i, t in enumerate(nb["tasks"]):
            count += 1
            where = f"{nb['id']}/{t['id']}"
            before = [p["solution"] for p in nb["tasks"][:i]] if nb.get("chain") else ()
            good = run_cell(nb["setup"], t["solution"], t["check"], before)
            if good["setup_error"]:
                failures.append(f"{where}: setup failed: {good['setup_error']}")
                continue
            if good["error"]:
                failures.append(f"{where}: solution raised:\n{good['error']}")
            elif not good["check"]["ok"]:
                failures.append(f"{where}: solution fails its check: {good['check']['message']}")
            bad = run_cell(nb["setup"], t["starter"], t["check"], before)
            if bad["check"]["ok"]:
                failures.append(f"{where}: starter code passes the check")
        problem = sequential(nb)
        if problem:
            failures.append(f"{nb['id']} (top to bottom): {problem}")
    if failures:
        print(f"{len(failures)} problem(s):")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print(f"all {count} notebook tasks verified")


if __name__ == "__main__":
    main()
