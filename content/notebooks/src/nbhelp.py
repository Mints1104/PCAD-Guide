"""Helpers for authoring notebooks. NB(...) returns a dict in the published notebook schema.

A notebook is a setup cell (data and imports) followed by tasks. Each task is checked on its own:
the app runs setup, then the learner's code, then the task's check in one fresh namespace. A check
is plain Python that raises AssertionError (with a message the learner sees) when the answer is wrong.
"""

import textwrap


def _clean(code):
    return textwrap.dedent(code).strip("\n") if code else ""


def T(id, title, prompt, starter, solution, check, hints=()):
    """One task.

    prompt:   Markdown shown above the code cell.
    starter:  code the cell starts with (must fail the check).
    solution: a model answer (must pass the check).
    check:    asserts run after the learner's code in the same namespace.
    hints:    revealed one at a time.
    """
    return {
        "id": id,
        "title": title,
        "prompt": _clean(prompt),
        "starter": _clean(starter),
        "solution": _clean(solution),
        "check": _clean(check),
        "hints": list(hints),
    }


def NB(id, title, level, objectives, summary, intro, setup, tasks, chain=False):
    """One notebook. level: 1 warm-up, 2 core, 3 challenge.

    chain: later tasks build on earlier ones, so running task N first runs the learner's code for
    tasks 1 to N-1 (as running a Jupyter notebook top to bottom would)."""
    ids = [t["id"] for t in tasks]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{id}: duplicate task ids")
    nb = {
        "id": id,
        "title": title,
        "level": level,
        "objectives": objectives,
        "summary": summary,
        "intro": _clean(intro),
        "setup": _clean(setup),
        "tasks": tasks,
    }
    if chain:
        nb["chain"] = True
    return nb
