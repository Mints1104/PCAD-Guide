from nbhelp import NB, T

NOTEBOOK = NB(
    "python-warmup", "Python warm-up", 1, ["2.1.1", "2.1.2", "2.1.4", "2.2.2"],
    "Comprehensions, functions with defaults, dictionaries and try/except.",
    """
    Plain Python on small lists and dictionaries: the building blocks every later notebook uses.
    """,
    """
    temps = [21.5, 19.0, None, 23.4, 18.2, None, 25.1]
    scores = {"ana": 82, "ben": 67, "cara": 91, "dev": 74}
    words = ["data", "Python", "pandas", "data", "SQL", "python", "NumPy"]
    """,
    [
        T("drop-none", "Drop the missing readings",
          """
          `temps` has gaps recorded as `None`. Make a list `clean` with every reading that is not `None`,
          in the original order.
          """,
          """
          clean = []
          """,
          """
          clean = [t for t in temps if t is not None]
          """,
          """
          assert isinstance(clean, list), "clean should be a list"
          assert None not in clean, "clean still contains None"
          assert clean == [21.5, 19.0, 23.4, 18.2, 25.1], "clean should hold the five readings in their original order"
          """,
          ["A list comprehension with a condition: `[x for x in items if ...]`.",
           "Test with `is not None` rather than truthiness: a reading of `0.0` would be falsy but is not missing."]),

        T("passed", "A function with a default argument",
          """
          Write `passed(scores, mark=70)` that returns the **sorted** list of names whose score is at least `mark`.

          `passed(scores)` should give `['ana', 'cara', 'dev']`.
          """,
          """
          def passed(scores, mark=70):
              pass
          """,
          """
          def passed(scores, mark=70):
              return sorted(name for name, score in scores.items() if score >= mark)
          """,
          """
          assert passed(scores) == ["ana", "cara", "dev"], f"passed(scores) returned {passed(scores)!r}, expected ['ana', 'cara', 'dev']"
          assert passed(scores, 80) == ["ana", "cara"], "passed(scores, 80) should use the mark you pass in"
          assert passed(scores, mark=74) == ["ana", "cara", "dev"], "a score equal to the mark counts as passed (use >=)"
          assert passed({}) == [], "an empty dict should give an empty list"
          """,
          ["`scores.items()` gives `(name, score)` pairs.", "`sorted(...)` accepts any iterable and returns a new list."]),

        T("count-words", "Count words, ignoring case",
          """
          Build a dictionary `counts` that maps each word in `words`, **lower-cased**, to how many times it appears.
          For example `counts["python"]` is `2`.
          """,
          """
          counts = {}
          for w in words:
              pass
          """,
          """
          counts = {}
          for w in words:
              key = w.lower()
              counts[key] = counts.get(key, 0) + 1
          """,
          """
          assert isinstance(counts, dict), "counts should be a dict (or a Counter)"
          expected = {"data": 2, "python": 2, "pandas": 1, "sql": 1, "numpy": 1}
          assert set(counts) == set(expected), f"the keys should be {sorted(expected)}, got {sorted(counts)}"
          assert dict(counts) == expected, "some counts are off: 'Python' and 'python' should count as the same word"
          """,
          ["`d.get(key, 0)` returns 0 for a key that is not in the dictionary yet.",
           "`collections.Counter` does the counting in one call."]),

        T("label-temps", "Label each reading",
          """
          For every reading in `temps` that is not `None`, add a label to the list `labels`:

          - `"cold"` below 20
          - `"mild"` from 20 up to (not including) 24
          - `"warm"` from 24 upwards
          """,
          """
          labels = []
          """,
          """
          labels = []
          for t in temps:
              if t is None:
                  continue
              if t < 20:
                  labels.append("cold")
              elif t < 24:
                  labels.append("mild")
              else:
                  labels.append("warm")
          """,
          """
          assert isinstance(labels, list), "labels should be a list"
          assert len(labels) == 5, f"there are 5 readings that are not None; labels has {len(labels)} items"
          assert labels == ["mild", "cold", "mild", "cold", "warm"], f"got {labels!r}; check the boundaries (20 is mild, 24 is warm)"
          """,
          ["`continue` skips to the next reading.", "With `if / elif / else`, only the first true branch runs, so `elif t < 24` already knows `t >= 20`."]),

        T("to-float", "Convert safely with try/except",
          """
          Write `to_float(value)` that returns `float(value)`, or `None` when the value cannot be converted.
          It must handle text such as `"n/a"` (a `ValueError`) and `None` (a `TypeError`).
          Catch only those two exceptions, not every exception.
          """,
          """
          def to_float(value):
              return float(value)
          """,
          """
          def to_float(value):
              try:
                  return float(value)
              except (ValueError, TypeError):
                  return None
          """,
          """
          assert to_float("3.5") == 3.5, "to_float('3.5') should be 3.5"
          assert to_float(" 7 ") == 7.0, "float() ignores surrounding spaces, so ' 7 ' gives 7.0"
          assert to_float("n/a") is None, "to_float('n/a') should return None"
          assert to_float(None) is None, "to_float(None) should return None (float(None) raises TypeError)"
          class Weird:
              def __float__(self):
                  raise KeyError("not a conversion problem")
          try:
              to_float(Weird())
          except KeyError:
              pass
          else:
              raise AssertionError("catch only ValueError and TypeError: other errors should still be raised")
          """,
          ["Several exceptions can share one handler: `except (ValueError, TypeError):`.",
           "A bare `except:` would also hide bugs you did not expect, which is why the check rejects it."]),
    ],
)
