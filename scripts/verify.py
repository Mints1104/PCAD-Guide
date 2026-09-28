"""Run every code question and check its keyed answer.

Each question may carry a "verify" field (stripped from the published build):
  "stdout"            run `code`; its printed output must equal the correct option
  "raises:Name"       run `code`; it must raise the named exception
  "runs"              run `code`; it must finish without an exception
  {"py": "..."}       run a check snippet; helpers below are in scope, asserts must pass
SQL questions set lang "sql" plus a "setup" script; checks use run_sql(setup, query).

Usage: python scripts/verify.py [question-id ...]
"""

import contextlib
import io
import json
import os
import sqlite3
import sys
import traceback
import warnings
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def strip_ticks(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        t = t.rsplit("```", 1)[0]
    elif t.startswith("`") and t.endswith("`") and t.count("`") == 2:
        t = t[1:-1]
    return "\n".join(line.rstrip() for line in t.strip("\n").split("\n")).strip()


def run_py(code):
    buf = io.StringIO()
    ns = {"__name__": "__main__"}
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<question>", "exec"), ns)
    return "\n".join(line.rstrip() for line in buf.getvalue().rstrip("\n").split("\n")).strip()


def run_py_ns(code):
    ns = {"__name__": "__main__"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, "<question>", "exec"), ns)
    return ns


def run_sql(setup, query, params=()):
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(setup)
        rows = con.execute(query, params).fetchall()
        return rows
    finally:
        con.close()


def run_sql_script(setup, script):
    """Run a multi-statement script, then return the connection for inspection."""
    con = sqlite3.connect(":memory:")
    con.executescript(setup)
    con.executescript(script)
    return con


def check(q):
    v = q.get("verify")
    options = q["options"]
    answers = [strip_ticks(options[i]) for i in q["answer"]]
    helpers = {
        "q": q,
        "run_py": run_py,
        "run_py_ns": run_py_ns,
        "run_sql": run_sql,
        "run_sql_script": run_sql_script,
        "opt": lambda i: strip_ticks(options[i]),
        "ans": answers,
        "code": q.get("code", ""),
        "setup": q.get("setup", ""),
    }
    if v == "stdout":
        out = run_py(q["code"])
        assert q["type"] == "single", "stdout check needs a single-select question"
        assert out == answers[0], f"printed:\n{out}\nkeyed answer:\n{answers[0]}"
        others = [strip_ticks(o) for i, o in enumerate(options) if i not in q["answer"]]
        assert out not in others, "a wrong option matches the output too"
    elif isinstance(v, str) and v.startswith("raises:"):
        name = v.split(":", 1)[1]
        try:
            run_py(q["code"])
        except Exception as e:  # noqa: BLE001
            assert type(e).__name__ == name, f"raised {type(e).__name__}, expected {name}"
        else:
            raise AssertionError(f"expected {name}, but the code ran")
    elif v == "runs":
        run_py(q["code"])
    elif isinstance(v, dict) and "py" in v:
        exec(compile(v["py"], f"<verify {q['id']}>", "exec"), dict(helpers))
    else:
        raise AssertionError(f"unknown verify spec {v!r}")


def main():
    only = set(sys.argv[1:])
    questions = []
    for f in sorted((ROOT / "content" / "questions").glob("*.json")):
        questions += json.loads(f.read_text(encoding="utf-8"))
    failed, passed, unverified = [], 0, []
    for q in questions:
        if only and q["id"] not in only:
            continue
        if "verify" not in q:
            if q.get("code") and q.get("lang", "python") != "text":
                unverified.append(q["id"])
            continue
        try:
            check(q)
            passed += 1
        except Exception as e:  # noqa: BLE001
            detail = str(e) if isinstance(e, AssertionError) else traceback.format_exc(limit=2)
            failed.append((q["id"], detail))
    for qid, detail in failed:
        print(f"FAIL {qid}\n  " + detail.replace("\n", "\n  "))
    print(f"\nverified {passed} question(s), {len(failed)} failed")
    if unverified:
        print(f"code questions without a check: {', '.join(unverified)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
