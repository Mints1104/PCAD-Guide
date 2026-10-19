"""Runs one notebook cell the way the app does: setup, then the learner's code, then (optionally) the
task's check, all in one fresh namespace. Shared by the in-browser runner (Pyodide, in a worker) and
scripts/verify_notebooks.py, so the checks are verified exactly as they run on the site."""

import ast
import base64
import contextlib
import io
import linecache
import os
import sys
import traceback

os.environ.setdefault("MPLBACKEND", "Agg")

CELL = "<cell>"
MAX_TEXT = 20000


def _clip(text):
    return text if len(text) <= MAX_TEXT else text[:MAX_TEXT] + f"\n… ({len(text) - MAX_TEXT} more characters)"


def _cell_traceback(exc):
    """The traceback limited to the learner's own lines, like Jupyter shows it."""
    if isinstance(exc, SyntaxError):
        return "".join(traceback.format_exception_only(type(exc), exc)).replace(f'File "{CELL}", ', "").rstrip()
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == CELL]
    lines = []
    if frames:
        lines.append("Traceback (most recent call last):")
        for f in frames:
            lines.append(f"  line {f.lineno}{'' if f.name == '<module>' else f', in {f.name}'}")
            if f.line:
                lines.append(f"    {f.line.strip()}")
    lines.append("".join(traceback.format_exception_only(type(exc), exc)).rstrip())
    return "\n".join(lines)


def _display(value):
    """A displayable form of the cell's last expression: an HTML table for DataFrames, else repr."""
    mod = type(value).__module__ or ""
    if mod.startswith("pandas") and type(value).__name__ == "DataFrame":
        return {"html": value.to_html(max_rows=30, max_cols=20, border=0)}
    if mod.startswith("pandas") and type(value).__name__ == "Styler":
        return {"html": value.to_html()}
    return {"text": _clip(repr(value))}


def _figures():
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None:
        return []
    out = []
    for num in plt.get_fignums():
        buf = io.BytesIO()
        plt.figure(num).savefig(buf, format="png", dpi=90, bbox_inches="tight")
        out.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    return out


def _close_figures():
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is not None:
        plt.close("all")


def _run_before(before, ns):
    """Earlier tasks of a chained notebook, run silently. Returns an error message or None."""
    for i, code in enumerate(before):
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                exec(compile(code, f"<task {i + 1}>", "exec"), ns)
        except (Exception, SystemExit) as exc:
            return f"Task {i + 1} raised {type(exc).__name__}: {exc}\nThis task builds on the earlier ones, so fix task {i + 1} first."
        finally:
            _close_figures()
    return None


def run_cell(setup, code, check=None, before=()):
    """Returns {stdout, display, figures, error, setup_error, check}. check is None when no check ran,
    else {"ok": bool, "message": str}. before: the code of earlier tasks, for chained notebooks."""
    _close_figures()
    ns = {"__name__": "__main__"}
    out = io.StringIO()
    result = {"stdout": "", "display": None, "figures": [], "error": None, "setup_error": None, "check": None}
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            exec(compile(setup, "<setup>", "exec"), ns)
        except Exception as exc:  # the setup is ours; this means a broken environment
            result["setup_error"] = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        if result["setup_error"] is None and before:
            result["error"] = _run_before(before, ns)
            if result["error"] is not None and check is not None:
                result["check"] = {"ok": False, "message": "An earlier task raised an error, so this one could not be checked."}
        if result["setup_error"] is None and result["error"] is None:
            # Lets tracebacks quote the learner's lines.
            linecache.cache[CELL] = (len(code), None, code.splitlines(True), CELL)
            try:
                tree = ast.parse(code, CELL)
                last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
                exec(compile(tree, CELL, "exec"), ns)
                if last is not None:
                    value = eval(compile(ast.Expression(last.value), CELL, "eval"), ns)
                    if value is not None and not type(value).__module__.startswith("matplotlib"):
                        result["display"] = _display(value)
            except (Exception, SystemExit) as exc:
                result["error"] = _cell_traceback(exc)
            result["figures"] = _figures()
            if check is not None:
                if result["error"] is not None:
                    result["check"] = {"ok": False, "message": "Your code raised an error, so the check did not run. Fix the error first."}
                else:
                    try:
                        exec(compile(check, "<check>", "exec"), ns)
                        result["check"] = {"ok": True, "message": ""}
                    except AssertionError as exc:
                        result["check"] = {"ok": False, "message": str(exc) or "Not quite: the result does not match yet."}
                    except Exception as exc:
                        result["check"] = {"ok": False, "message": f"The check could not use your result ({type(exc).__name__}: {exc})."}
    result["stdout"] = _clip(out.getvalue())
    _close_figures()
    return result
