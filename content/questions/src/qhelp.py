"""Helper for authoring questions. Q(...) returns a dict in the published question schema."""

import textwrap


def _clean(code):
    return textwrap.dedent(code).strip("\n") if code else code


def Q(id, obj, d, stem, options, answer, wrong, exp, src, tags, code=None, lang=None, verify=None, setup=None, optlang=None):
    """Build one question.

    answer: an option index, or a list of indexes for multiple-select.
    wrong:  {option index: why that option is wrong} for every wrong option.
    verify: see scripts/verify.py ("stdout", "raises:Name", "runs" or {"py": "..."}).
    optlang: how multi-line options are shown ("text" for printed output; defaults to the code language).
    """
    answers = sorted(answer) if isinstance(answer, (list, tuple)) else [answer]
    options = [_clean(o) if "\n" in o else o for o in options]
    missing = [i for i in range(len(options)) if i not in answers and i not in wrong]
    extra = [i for i in wrong if i in answers or i >= len(options)]
    if missing or extra:
        raise ValueError(f"{id}: why_wrong missing for {missing}, or given for correct/unknown {extra}")
    q = {
        "id": id,
        "objective": obj,
        "type": "multi" if len(answers) > 1 else "single",
        "stem": stem,
        "options": options,
        "answer": answers,
        "explanation": exp,
        "why_wrong": ["" if i in answers else wrong[i] for i in range(len(options))],
        "source": src,
        "difficulty": d,
        "tags": tags,
    }
    if code:
        q["code"] = _clean(code)
    if lang and lang != "python":
        q["lang"] = lang
    if optlang:
        q["optlang"] = optlang
    if setup:
        q["setup"] = _clean(setup)
    if verify:
        q["verify"] = {"py": _clean(verify["py"])} if isinstance(verify, dict) else verify
    return q
