from nbhelp import NB, T

NOTEBOOK = NB(
    "python-challenge", "Python challenge: functions and errors", 3, ["2.1.1", "2.1.2", "2.1.4", "2.2.2"],
    "Edge cases, recursion, functions as arguments, closures, custom exceptions and generators.",
    """
    Each task asks for a small, general-purpose function. The checks try edge cases, so think about empty input and bad arguments.
    """,
    """
    records = [
        {"city": "Leeds", "kind": "cafe", "rating": 4.5},
        {"city": "York", "kind": "pub", "rating": 3.9},
        {"city": "Leeds", "kind": "pub", "rating": 4.1},
        {"city": "Hull", "kind": "cafe", "rating": 4.8},
    ]
    """,
    [
        T("chunk", "Split a list into chunks",
          """
          Write `chunk(items, size)` that returns a list of consecutive lists of at most `size` items:
          `chunk([1, 2, 3, 4, 5], 2)` gives `[[1, 2], [3, 4], [5]]`. Raise `ValueError` when `size` is less than 1.
          """,
          """
          def chunk(items, size):
              pass
          """,
          """
          def chunk(items, size):
              if size < 1:
                  raise ValueError("size must be at least 1")
              return [list(items[i:i + size]) for i in range(0, len(items), size)]
          """,
          """
          assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]], f"chunk([1, 2, 3, 4, 5], 2) gave {chunk([1, 2, 3, 4, 5], 2)}"
          assert chunk([1, 2, 3], 3) == [[1, 2, 3]], "a size equal to the length gives one chunk"
          assert chunk([1, 2], 5) == [[1, 2]], "a size larger than the length gives one chunk"
          assert chunk([], 2) == [], "an empty list gives no chunks"
          for bad in (0, -1):
              try:
                  chunk([1, 2], bad)
              except ValueError:
                  pass
              else:
                  raise AssertionError(f"chunk([1, 2], {bad}) should raise ValueError")
          """,
          ["`range(0, len(items), size)` gives the start of every chunk.",
           "Slicing past the end of a list is safe: `[1, 2][0:5]` is `[1, 2]`."]),

        T("flatten", "Flatten any depth",
          """
          Write `flatten(nested)` that returns a flat list of every non-list, non-tuple value, at any depth:
          `flatten([1, [2, (3, [4])], 5])` gives `[1, 2, 3, 4, 5]`. Strings count as single values.
          """,
          """
          def flatten(nested):
              return [x for x in nested]
          """,
          """
          def flatten(nested):
              out = []
              for x in nested:
                  if isinstance(x, (list, tuple)):
                      out.extend(flatten(x))
                  else:
                      out.append(x)
              return out
          """,
          """
          assert flatten([1, [2, (3, [4])], 5]) == [1, 2, 3, 4, 5], f"got {flatten([1, [2, (3, [4])], 5])}"
          assert flatten([]) == [] and flatten([[], [[]]]) == [], "empty lists contribute nothing"
          assert flatten(["ab", ["cd"]]) == ["ab", "cd"], "strings are values, not sequences to split"
          assert flatten([[[[[7]]]]]) == [7], "handle any depth (recursion)"
          """,
          ["A recursive function calls itself on each nested list or tuple.",
           "`isinstance(x, (list, tuple))` tests for either type."]),

        T("group-by", "Group with a key name or a function",
          """
          Write `group_by(items, key)` that returns a dict mapping each key to the list of items with that key, in their original order.
          `key` is either a dictionary key name (a string) or a function applied to each item.

          `group_by(records, "city")["Leeds"]` is the two Leeds records; `group_by([1, 2, 3, 4], lambda n: n % 2)` is `{1: [1, 3], 0: [2, 4]}`.
          """,
          """
          def group_by(items, key):
              groups = {}
              return groups
          """,
          """
          def group_by(items, key):
              get = key if callable(key) else (lambda item: item[key])
              groups = {}
              for item in items:
                  groups.setdefault(get(item), []).append(item)
              return groups
          """,
          """
          by_city = group_by(records, "city")
          assert sorted(by_city) == ["Hull", "Leeds", "York"], f"keys are {sorted(by_city)}"
          assert [r["kind"] for r in by_city["Leeds"]] == ["cafe", "pub"], "keep each group's items in their original order"
          assert group_by([1, 2, 3, 4], lambda n: n % 2) == {1: [1, 3], 0: [2, 4]}, "key can also be a function"
          high = group_by(records, lambda r: r["rating"] >= 4.5)
          assert [r["city"] for r in high[True]] == ["Leeds", "Hull"], "a function key can return any hashable value"
          assert group_by([], "city") == {}, "no items give an empty dict"
          """,
          ["`callable(key)` tells a function from a string.",
           "`d.setdefault(k, []).append(x)` creates the list the first time a key appears."]),

        T("counter", "A closure that remembers",
          """
          Write `make_counter(start=0)` that returns a function. Each call of that function returns the next number:
          `c = make_counter(); c(), c()` gives `1, 2`. Separate counters must count separately. Do not use a global variable.
          """,
          """
          count = 0

          def make_counter(start=0):
              def step():
                  global count
                  count += 1
                  return count
              return step
          """,
          """
          def make_counter(start=0):
              count = start

              def step():
                  nonlocal count
                  count += 1
                  return count

              return step
          """,
          """
          a = make_counter()
          b = make_counter(10)
          assert callable(a), "make_counter should return a function"
          assert [a(), a(), a()] == [1, 2, 3], "each call should return the next number"
          assert [b(), b()] == [11, 12], "make_counter(10) should continue from 10, and not share a's count"
          assert a() == 4, "a should keep its own count"
          """,
          ["An inner function can read the outer function's variables; to **rebind** one it needs `nonlocal`.",
           "Each call of `make_counter` creates a new `count`, so counters are independent."]),

        T("exceptions", "A custom exception",
          """
          Define `class RecordError(ValueError)` and write:

          - `parse_line(line)` that turns `"name,age"` into `(name, int(age))`, with the name stripped. It raises `RecordError`
            when the line does not have exactly two fields, or when the age is not a whole number (chain the original error with `from`).
          - `parse_all(lines)` that returns `(good, bad)`: the parsed tuples, and the **1-based line numbers** that failed.
          """,
          """
          class RecordError(ValueError):
              pass


          def parse_line(line):
              name, age = line.split(",")
              return name, int(age)


          def parse_all(lines):
              return [parse_line(l) for l in lines], []
          """,
          """
          class RecordError(ValueError):
              pass


          def parse_line(line):
              parts = line.split(",")
              if len(parts) != 2:
                  raise RecordError(f"expected 2 fields, got {len(parts)}")
              name, age = parts
              try:
                  return name.strip(), int(age)
              except ValueError as exc:
                  raise RecordError(f"bad age {age!r}") from exc


          def parse_all(lines):
              good, bad = [], []
              for number, line in enumerate(lines, start=1):
                  try:
                      good.append(parse_line(line))
                  except RecordError:
                      bad.append(number)
              return good, bad
          """,
          """
          assert issubclass(RecordError, ValueError), "RecordError should subclass ValueError"
          assert parse_line(" Ana ,34") == ("Ana", 34), f"parse_line(' Ana ,34') gave {parse_line(' Ana ,34')!r}"
          for bad_line in ("Ben", "Ben,30,x", "Ben,thirty"):
              try:
                  parse_line(bad_line)
              except RecordError:
                  pass
              except Exception as exc:
                  raise AssertionError(f"parse_line({bad_line!r}) raised {type(exc).__name__}; it should raise RecordError")
              else:
                  raise AssertionError(f"parse_line({bad_line!r}) should raise RecordError")
          try:
              parse_line("Ben,thirty")
          except RecordError as exc:
              assert isinstance(exc.__cause__, ValueError), "chain the int() error: raise RecordError(...) from exc"
          good, bad = parse_all(["Ana,34", "oops", "Cara, 29", "Dev,x"])
          assert good == [("Ana", 34), ("Cara", 29)], f"good is {good}"
          assert bad == [2, 4], f"bad is {bad}; use 1-based line numbers (enumerate(lines, start=1))"
          """,
          ["`int(' 29')` ignores surrounding spaces, so only the name needs stripping.",
           "`raise NewError(...) from exc` keeps the original error as `__cause__`.",
           "Catch `RecordError` (not every exception) in `parse_all`, so real bugs still surface."]),

        T("generator", "A running mean generator",
          """
          Write a **generator function** `running_mean(values)` that yields the mean of the values seen so far:
          `list(running_mean([2, 4, 9]))` gives `[2.0, 3.0, 5.0]`. It should work on any iterable, including another generator,
          without building a list of the values.
          """,
          """
          def running_mean(values):
              values = list(values)
              return [sum(values[:i + 1]) / (i + 1) for i in range(len(values))]
          """,
          """
          def running_mean(values):
              total = 0
              for n, value in enumerate(values, start=1):
                  total += value
                  yield total / n
          """,
          """
          import inspect
          import itertools
          assert inspect.isgeneratorfunction(running_mean), "running_mean should be a generator function (use yield)"
          assert list(running_mean([2, 4, 9])) == [2.0, 3.0, 5.0], f"got {list(running_mean([2, 4, 9]))}"
          assert list(running_mean([])) == [], "no values give no means"
          assert list(itertools.islice(running_mean(itertools.count(1)), 3)) == [1.0, 1.5, 2.0], "it should work on an endless iterator, one value at a time"
          """,
          ["`yield` hands back one value and pauses the function until the next value is requested.",
           "Keep a running total and count instead of storing every value."]),
    ],
)
