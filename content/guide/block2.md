# Block 2: Programming and Database Skills

Block 2 is the largest block: 16 items, 33.3% of the exam. It covers core Python (syntax, functions, data structures, style), modules and exceptions, object-oriented programming for data records, and SQL both on its own and from Python. Many items show a few lines of code and ask what they print or which line fixes a problem.

## 2.1.1 Apply Python syntax and control structures

**Syllabus asks:** variables, scopes and basic data types; loops and conditionals to control the flow of data.

### Core facts

**Types.** `int`, `float`, `str`, `bool`, `NoneType`. Python is dynamically typed: a name can be rebound to a value of another type. `type(x)` returns the type; `isinstance(x, (int, float))` checks against one or more types. `bool` is a subclass of `int` (`True + True == 2`).

**Operators to know.** `/` always returns a float (`7 / 2 == 3.5`); `//` floors (`7 // 2 == 3`, `-7 // 2 == -4`); `%` is the remainder; `**` is power. Floats are approximate: `0.1 + 0.2 == 0.30000000000000004`.

**Truthiness.** `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None` and `False` are falsy; everything else is truthy.

**Scope (LEGB).** Python looks a name up in the **L**ocal function, then **E**nclosing functions, then **G**lobal (module), then **B**uilt-ins. Assigning to a name anywhere inside a function makes it local to that function for the whole function body, unless declared `global` (module level) or `nonlocal` (enclosing function).

```python
count = 10

def bump():
    global count
    count += 1

def shadow():
    count = 99          # a new local; the global is untouched
    return count

bump()
print(count, shadow(), count)
```

```text
11 99 11
```

Reading a global and then assigning to it in the same function without `global` raises `UnboundLocalError`.

**Control flow.**

```python
total = 0
for i in range(1, 10, 3):        # 1, 4, 7  (stop is excluded)
    if i == 4:
        continue                  # skip the rest of this iteration
    total += i
print(total)

n = 0
while n < 5:
    n += 2
else:
    print("loop ended without break, n =", n)
```

```text
8
loop ended without break, n = 6
```

**`range`.** `range(stop)`, `range(start, stop)` and `range(start, stop, step)`. It starts at `start` (0 if omitted) and `stop` is never included. A negative step counts down.

```python
print(list(range(4)))
print(list(range(2, 6)))
print(list(range(1, 10, 3)))
print(list(range(10, 0, -3)))
```

```text
[0, 1, 2, 3]
[2, 3, 4, 5]
[1, 4, 7]
[10, 7, 4, 1]
```

**`break`, `continue` and a loop's `else`.** `break` leaves the loop at once; `continue` skips the rest of this iteration and moves to the next one (see the first example above). A loop's `else` block runs only if the loop finished without hitting `break`, which makes it a natural "not found" branch.

```python
for n in [3, 8, 5]:
    if n > 6:
        print("found", n)
        break
else:
    print("nothing over 6")

for n in [3, 5]:
    if n > 6:
        print("found", n)
        break
else:
    print("nothing over 6")
```

```text
found 8
nothing over 6
```

The first loop breaks at 8, so its `else` is skipped (and 5 is never checked). The second loop runs to the end, so its `else` runs.

**`enumerate` and `zip`.** `enumerate(items)` gives `(index, item)` pairs, counting from 0 unless you pass `start`. `zip(a, b)` pairs the items of two sequences position by position and stops at the shorter one, silently dropping the extras.

```python
items = ["tea", "jam", "bread"]
for i, item in enumerate(items, start=1):
    print(i, item)

names = ["Ann", "Bob", "Cy"]
scores = [90, 75]
print(list(zip(names, scores)))
```

```text
1 tea
2 jam
3 bread
[('Ann', 90), ('Bob', 75)]
```

**Conditional expressions and chained comparisons.** `a if condition else b` picks one of two values in a single expression. Comparisons chain, so `0 < x < 10` means `0 < x and x < 10`.

```python
for x in [50, 150]:
    label = "high" if x > 100 else "low"
    print(x, label)

x = 5
print(0 < x < 10, 0 < x < 3)
```

```text
50 low
150 high
True False
```

**Comprehensions.** `[expression for item in iterable if condition]` builds a list in one line: the `if` filters, and the expression transforms what passes. Curly braces with `key: value` build a dict the same way.

```python
data = [3, -1, 4, 0]
print([x * 2 for x in data if x > 0])

pairs = [("a", 1), ("b", 2)]
print({k: v for k, v in pairs})
print({k: v * 10 for k, v in pairs})
```

```text
[6, 8]
{'a': 1, 'b': 2}
{'a': 10, 'b': 20}
```

### Exam traps

> **Trap.** `range(1, 10, 3)` gives 1, 4, 7, never 10. Count the loop body's executions carefully.

> **Trap.** An `if` that assigns to a global name inside a function makes that name local everywhere in the function; reading it earlier raises `UnboundLocalError`.

## 2.1.2 Analyze and create Python functions

**Syllabus asks:** design functions with a clear purpose; tell positional (indexed) arguments from keyword arguments; use required vs optional parameters.

### Core facts

**Parameters and arguments.** When you *define* a function, the names in its brackets are its **parameters**. When you *call* it, the values you pass in are the **arguments**. Each argument is stored in one parameter, and the function uses that name to refer to it.

```python
def greet(name, greeting):     # name and greeting are parameters
    print(greeting, name)

greet("Ana", "Hello")          # "Ana" and "Hello" are arguments
```

```text
Hello Ana
```

**Positional and keyword arguments.** Python can match arguments to parameters in two ways:

- **Positional**: by order. The first value goes to the first parameter, the second to the second, and so on.
- **Keyword**: by name. You write `name=value`, so the order no longer matters.

```python
def greet(name, greeting):
    print(greeting, name)

greet("Ana", "Hello")               # positional: "Ana" is first, so it goes to name
greet(greeting="Hi", name="Ben")    # keyword: matched by name, order doesn't matter
greet("Cy", greeting="Hey")         # mixed: positional first, then keyword
```

```text
Hello Ana
Hi Ben
Hey Cy
```

When you mix the two, the positional arguments must come first. `greet(name="Cy", "Hey")` is a `SyntaxError`, so Python refuses to run the file at all.

**Required and optional parameters.** Give a parameter a default value in the definition and the caller is allowed to leave it out. A parameter without a default is required: every call must provide it.

```python
def greet(name, greeting="Hello"):  # greeting has a default, so it is optional
    print(greeting, name)

greet("Ana")             # no greeting given: the default "Hello" is used
greet("Ben", "Hi")       # greeting given: it replaces the default
```

```text
Hello Ana
Hi Ben
```

In the definition, parameters with defaults must come after the ones without. `def greet(greeting="Hello", name):` is a `SyntaxError`.

**Calls that go wrong.** Leaving out a required argument, or giving the same parameter a value twice, raises a `TypeError`. The error message says what went wrong. (Below, `try` / `except` catches each error so its message can be printed instead of stopping the program; section 2.2.2 covers it.)

```python
def greet(name, greeting="Hello"):
    print(greeting, name)

try:
    greet()                     # name is required, but nothing was passed
except TypeError as e:
    print(e)

try:
    greet("Ana", name="Ben")    # "Ana" already went to name by position
except TypeError as e:
    print(e)
```

```text
greet() missing 1 required positional argument: 'name'
greet() got multiple values for argument 'name'
```

**`return` versus `print`.** `print` shows a value on the screen. `return` hands a value back to the code that called the function, so it can be stored or used. A function without a `return` hands back `None`.

```python
def add_and_print(a, b):
    print(a + b)            # shows 5 on the screen, hands nothing back

def add_and_return(a, b):
    return a + b            # hands 5 back to the caller

x = add_and_print(2, 3)     # prints 5 while it runs
y = add_and_return(2, 3)    # prints nothing
print(x, y)
```

```text
5
None 5
```

`x` is `None` because `add_and_print` never returned anything. This is why functions should usually return their result instead of printing it.

**Any number of arguments: `*args` and `**kwargs`.** Put `*` before a parameter name and the function accepts any number of positional arguments. They arrive together as one tuple. Put `**` before a name and it accepts any number of keyword arguments, which arrive as a dict. The names `args` and `kwargs` are only a convention; the stars do the work.

```python
def total(*args):
    print(args)             # every value passed in, as a tuple
    return sum(args)

print(total(1, 2, 3))
print(total(10))

def show_settings(**kwargs):
    print(kwargs)           # every name=value pair, as a dict

show_settings(color="red", size=3)
```

```text
(1, 2, 3)
6
(10,)
10
{'color': 'red', 'size': 3}
```

**Forcing one style: the `*` and `/` markers.** These are less common, but the exam can show them.

- A bare `*` in the parameter list means every parameter **after** it must be passed by name (**keyword-only**).
- A `/` means every parameter **before** it must be passed by position (**positional-only**).

```python
def scale(value, *, factor):    # factor is after *, so it must be named
    return value * factor

print(scale(5, factor=2))       # works

try:
    scale(5, 2)                 # factor passed by position: not allowed
except TypeError as e:
    print(e)
```

```text
10
scale() takes 1 positional argument but 2 were given
```

```python
def square(x, /):               # x is before /, so it can't be passed by name
    return x * x

print(square(4))                # works

try:
    square(x=4)                 # passed by name: not allowed
except TypeError as e:
    print(e)
```

```text
16
square() got some positional-only arguments passed as keyword arguments: 'x'
```

**Putting it together.** This function uses a required parameter, an optional one, and a keyword-only one:

```python
def summarize(values, precision=2, *, label="mean"):
    """Return a labeled mean of values, rounded to precision places."""
    avg = sum(values) / len(values)
    return f"{label}: {round(avg, precision)}"

print(summarize([1, 2, 4]))                       # both defaults used
print(summarize([1, 2, 4], 1))                    # precision=1, by position
print(summarize([1, 2, 4], precision=0, label="avg"))
```

```text
mean: 2.33
mean: 2.3
avg: 2.0
```

`values` is required. `precision` is optional and can be passed either way. `label` is optional too, but because it comes after `*`, it can only be passed by name.

**Default values are evaluated once**, when the function is defined. A mutable default is shared between calls:

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add_item("a"), add_item("b"))

def add_item_safe(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(add_item_safe("a"), add_item_safe("b"))
```

```text
['a', 'b'] ['a', 'b']
['a'] ['b']
```

**Clear purpose.** One job per function, a descriptive verb name (`load_orders`, `clean_prices`), a docstring, and return values instead of printing inside the function, so the result can be reused and tested.

### Exam traps

> **Trap.** `def f(a=1, b):` is a `SyntaxError`: a required parameter cannot follow an optional one.

> **Trap.** Mutable default arguments (`[]`, `{}`) keep their contents between calls. Use `None` and create the object inside.

## 2.1.3 Evaluate the Python data science ecosystem

**Syllabus asks:** identify the key libraries and tools, and judge which suits a given scenario.

### Core facts

| Tool | Use it for |
|---|---|
| **NumPy** | Fast n-dimensional arrays, vectorized math, linear algebra, random numbers |
| **pandas** | Tabular data: `Series` and `DataFrame`, reading files and SQL, cleaning, grouping, joining, time series |
| **Matplotlib** | The base plotting library; full control over every figure element |
| **Seaborn** | Statistical charts on top of Matplotlib with less code; works directly with DataFrames |
| **SciPy** | Scientific computing; `scipy.stats` for distributions and statistical tests |
| **statsmodels** | Statistical models with detailed summaries (coefficients, p-values, confidence intervals) |
| **scikit-learn** | Machine learning: preprocessing, train/test split, models, metrics |
| **requests** | HTTP calls to APIs and web pages |
| **BeautifulSoup** (`bs4`) | Parsing HTML and XML |
| **sqlite3** | Standard-library interface to SQLite databases |
| **PyMySQL** | Pure-Python client for MySQL / MariaDB |
| **SQLAlchemy** | Database toolkit and ORM; `pandas.read_sql` accepts its engines |
| **openpyxl** | Reading and writing `.xlsx` files (used by `pd.read_excel`) |
| **Jupyter** | Notebooks mixing code, output, charts and text |
| **conda / Anaconda** | Distribution and environment manager with scientific packages pre-built |
| **pip / venv** | Standard package installer / isolated virtual environments |

To judge a resource: does it fit the task and data size, is it maintained and documented, does it have a community, does its licence allow your use, and does it work with the rest of your stack?

### Exam traps

> **Trap.** scikit-learn is for prediction; statsmodels is for statistical inference (p-values, confidence intervals). Both fit regressions.

> **Trap.** Seaborn does not replace Matplotlib; it builds on it. You still use Matplotlib calls (`plt.title`, `plt.savefig`) to finish a Seaborn chart.

## 2.1.4 Organize and manipulate data using core data structures

**Syllabus asks:** use tuples, sets, lists, dictionaries and strings, and pick the right structure for a data-handling task.

### Core facts

| Structure | Literal | Ordered | Mutable | Duplicates | Typical use |
|---|---|---|---|---|---|
| `list` | `[1, 2, 2]` | Yes | Yes | Yes | A sequence you will change |
| `tuple` | `(1, 2)` or `1, 2` | Yes | No | Yes | A fixed record; dict keys; returning several values |
| `set` | `{1, 2}` (`set()` when empty) | No | Yes | No | Unique values; fast membership tests; set algebra |
| `dict` | `{"a": 1}` (`{}` is an empty dict) | Insertion order | Yes | Keys unique | Lookup by key |
| `str` | `"abc"` | Yes | No | Yes | Text |

```python
scores = {"ana": 81, "ben": 67}
scores["cara"] = 92                     # add or overwrite
print(scores.get("dan", 0), len(scores), sorted(scores, key=scores.get))

a, b = {1, 2, 3}, {3, 4}
print(a | b, a & b, a - b)

words = "  Data, Python ,SQL ".split(",")
print([w.strip().lower() for w in words], "-".join(["2025", "07", "15"]))

t = (1, [2, 3])
t[1].append(4)                          # the tuple is immutable; the list inside is not
print(t)
```

```text
0 3 ['ben', 'ana', 'cara']
{1, 2, 3, 4} {3} {1, 2}
['data', 'python', 'sql'] 2025-07-15
(1, [2, 3, 4])
```

- Lists: `append` (one item), `extend` (items of an iterable), `insert`, `pop` (by index, returns it), `remove` (first matching value), `sort()` (in place, returns `None`) vs `sorted()` (new list).

The list methods side by side:

```python
a = [1, 2]
a.append([3, 4])            # adds ONE item: the list itself
b = [1, 2]
b.extend([3, 4])            # adds each item
print(a, b)

c = [5, 3, 5, 1]
c.insert(0, 9)
print(c.pop(), c.pop(0), c)  # pop(): last item; pop(0): first item
c.remove(5)                  # first 5 only
print(c)

nums = [3, 1, 2]
print(sorted(nums), nums)    # sorted() returns a new list; nums is unchanged
print(nums.sort(), nums)     # sort() changes nums in place and returns None
```

```text
[1, 2, [3, 4]] [1, 2, 3, 4]
1 9 [5, 3, 5]
[3, 5]
[1, 2, 3] [3, 1, 2]
None [1, 2, 3]
```

- Dicts: `d[k]` raises `KeyError` if missing; `d.get(k, default)` doesn't. Iterate with `.items()`. Keys must be hashable (str, int, tuple of immutables; not lists).
- Strings are immutable: methods such as `.replace()` and `.upper()` return new strings.
- `(5)` is just `5`; a one-item tuple needs a comma: `(5,)`.

Dict lookups, hashable keys, immutable strings and one-item tuples:

```python
stock = {"tea": 4, "jam": 0}
print(stock.get("milk"), stock.get("milk", 0))
try:
    stock["milk"]
except KeyError as e:
    print("KeyError:", e)

for item, qty in stock.items():
    print(item, qty)

try:
    {["a", "b"]: 1}
except TypeError as e:
    print("TypeError:", e)
print({("a", "b"): 1})       # a tuple of strings is hashable, so it can be a key

s = "data"
print(s.upper(), s)          # upper() returns a new string; s is unchanged

print(type((5)).__name__, type((5,)).__name__)
```

```text
None 0
KeyError: 'milk'
tea 4
jam 0
TypeError: unhashable type: 'list'
{('a', 'b'): 1}
DATA data
int tuple
```

- `collections.Counter` counts items; `collections.defaultdict(list)` groups without checking for missing keys.

Counting and grouping without checking for missing keys:

```python
from collections import Counter, defaultdict

colors = ["red", "blue", "red", "green", "red"]
counts = Counter(colors)
print(counts["red"], counts["pink"], counts.most_common(2))

by_region = defaultdict(list)
for region, amount in [("EU", 10), ("US", 5), ("EU", 7)]:
    by_region[region].append(amount)    # no "if region not in by_region" needed
print(dict(by_region))
```

```text
3 0 [('red', 3), ('blue', 1)]
{'EU': [10, 7], 'US': [5]}
```

A `Counter` returns 0 for an item it has never seen, and a `defaultdict(list)` creates an empty list the first time a key is used.

### Exam traps

> **Trap.** `{}` is an empty **dict**, not an empty set.

> **Trap.** `lst.sort()` returns `None`. `x = lst.sort()` leaves `x` as `None`.

## 2.1.5 Explain and implement Python scripting best practices

**Syllabus asks:** PEP 8 for code style and PEP 257 for docstrings.

### Core facts

**PEP 8 (style).**

| Topic | Rule |
|---|---|
| Indentation | 4 spaces per level; no tabs mixed with spaces |
| Line length | At most 79 characters (72 for comments and docstrings) |
| Names | `snake_case` for functions, variables and modules; `CapWords` for classes; `UPPER_SNAKE` for constants; a leading `_` for internal names |
| Blank lines | Two around top-level functions and classes; one between methods |
| Imports | At the top, one module per line, grouped: standard library, third-party, local, with a blank line between groups; avoid `from x import *` |
| Whitespace | Spaces around assignment and comparison operators and after commas; none just inside brackets; no spaces around `=` for keyword arguments and unannotated defaults (`f(x, y=2)`) |
| Comparisons | `if x is None`, not `== None`; `if not items` for empty sequences; don't compare booleans to `True` with `==` |
| Avoid | Single-letter names `l`, `O`, `I` (they look like 1 and 0) |

**PEP 257 (docstrings).**

- Every public module, function, class and method gets a docstring, written in triple double quotes `"""..."""`.
- One-line docstring: fits on one line, quotes on the same line, a phrase ending in a period, written as a command: `"""Return the median of values."""` (not "Returns…").
- Multi-line docstring: a summary line, a blank line, then details (arguments, return value, exceptions); the closing `"""` on its own line.
- Don't repeat the signature in the docstring. Docstrings are available at run time via `help(f)` and `f.__doc__`; comments are not.

```python
def median(values):
    """Return the median of a non-empty list of numbers.

    Sort a copy of values and return the middle item, or the mean of the
    two middle items when the length is even.
    """
    ordered = sorted(values)
    mid = len(ordered) // 2
    return ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2
```

### Exam traps

> **Trap.** PEP 8 is a style guide, not a rule the interpreter enforces. Code that breaks it still runs; linters such as flake8 or ruff report it.

> **Trap.** Class names use `CapWords` (`SalesRecord`); function and variable names use `snake_case` (`load_sales`).

## 2.2.1 Import modules and manage Python packages

**Syllabus asks:** standard, selective and aliased imports; importing from the standard library, pip-installed packages and your own modules; identifying needed modules; installing, upgrading and removing packages with pip.

### Core facts

```python
import math                          # whole module: math.sqrt(16)
import numpy as np                   # alias (np, pd, plt and sns are the conventions)
from statistics import mean, median  # selective: use mean(...) directly
from datetime import datetime as dt  # selective + alias
```

- `from module import *` pulls every public name into your namespace; it hides where names come from and can overwrite your own names. PEP 8 discourages it.
- **Standard library** modules ship with Python (`math`, `statistics`, `random`, `datetime`, `csv`, `json`, `sqlite3`, `re`, `os`, `pathlib`, `collections`): no install needed.
- **Third-party** packages come from PyPI via pip (`numpy`, `pandas`, `requests`…). Importing one that isn't installed raises `ModuleNotFoundError`.
- **Local modules** are your own `.py` files. `import cleaning` finds `cleaning.py` in the script's folder (or anywhere on `sys.path`). A folder with modules (optionally with `__init__.py`) is a package: `from utils.cleaning import fix_dates`.
- A module's top-level code runs **once**, the first time it is imported; later imports reuse the cached module.
- `if __name__ == "__main__":` guards code that should run only when the file is executed directly, not when it is imported.

**pip.**

| Command | Does |
|---|---|
| `pip install pandas` | Install the latest version |
| `pip install pandas==2.2.3` | Install an exact version |
| `pip install --upgrade pandas` (`-U`) | Upgrade to the latest version |
| `pip uninstall pandas` | Remove it |
| `pip list` / `pip show pandas` | List installed packages / show one package's details |
| `pip freeze > requirements.txt` | Save exact versions |
| `pip install -r requirements.txt` | Install from that file |

Run pip inside a virtual environment (`python -m venv .venv`) so each project keeps its own package versions. `python -m pip ...` guarantees you use the pip that belongs to that Python.

### Exam traps

> **Trap.** `pip update pandas` is not a command. Upgrading is `pip install --upgrade pandas`.

> **Trap.** After `from math import sqrt`, the name `math` is not defined; only `sqrt` is.

## 2.2.2 Apply basic exception handling

**Syllabus asks:** implement exception handling, predict and mitigate common errors, and read error messages to diagnose problems.

### Core facts

```python
def safe_ratio(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("except")
        return None
    except TypeError as e:
        print("bad types:", e)
        return None
    else:
        print("else")          # runs only if no exception was raised
        return result
    finally:
        print("finally")       # always runs, even after return

print(safe_ratio(6, 3))
print(safe_ratio(1, 0))
```

```text
else
finally
2.0
except
finally
None
```

- Clauses are tried top to bottom; the **first** matching `except` wins, so put specific exceptions before general ones.

The same error, with the clauses in the wrong order and then the right one:

```python
try:
    int("12a")
except Exception:
    print("Exception clause caught it")
except ValueError:
    print("never reached")

try:
    int("12a")
except ValueError:
    print("ValueError clause caught it")
except Exception:
    print("only for anything else")
```

```text
Exception clause caught it
ValueError clause caught it
```

- `except (ValueError, TypeError) as e:` catches either; `e` holds the exception object.
- A bare `except:` (or `except Exception:` everywhere) hides bugs. Catch what you expect.
- `raise ValueError("price must be positive")` signals a problem; `raise` alone re-raises inside an `except` block.
- Custom exceptions subclass `Exception`: `class DataQualityError(Exception): pass`.

Raising, re-raising and a custom exception together:

```python
class DataQualityError(Exception):
    pass

def parse_price(text):
    try:
        value = float(text)
    except ValueError:
        print("not a number:", repr(text))
        raise                              # re-raise the same ValueError
    if value < 0:
        raise DataQualityError(f"negative price {value}")
    return value

for text in ["4.5", "-2", "abc"]:
    try:
        print(parse_price(text))
    except (ValueError, DataQualityError) as e:
        print(type(e).__name__, "->", e)
```

```text
4.5
DataQualityError -> negative price -2.0
not a number: 'abc'
ValueError -> could not convert string to float: 'abc'
```

`-2` parses fine but breaks the business rule, so the function raises `DataQualityError`. `abc` fails inside the `try`; the bare `raise` passes the original `ValueError` on to the caller after printing a note.

| Exception | Typical cause |
|---|---|
| `ValueError` | Right type, bad value: `int("12a")`, `float("")` |
| `TypeError` | Wrong type for the operation: `"3" + 4`, calling with the wrong arguments |
| `KeyError` | Missing dict key, or a missing column in `df["col"]` |
| `IndexError` | List or tuple index out of range |
| `ZeroDivisionError` | Division or modulo by zero |
| `AttributeError` | Object has no such attribute: `None.split()` |
| `NameError` | Name not defined (typo, not imported) |
| `FileNotFoundError` | Path does not exist (a subclass of `OSError`) |
| `ModuleNotFoundError` | Package not installed (a subclass of `ImportError`) |

**Reading a traceback.** Read from the **bottom**: the last line names the exception type and message; the lines above it show the call chain, with the most recent call last. The last frame that points at *your* code is usually where to fix.

### Exam traps

> **Trap.** `finally` runs even when the `try` or `except` block returns.

> **Trap.** `except Exception:` placed before `except ValueError:` catches everything first; the `ValueError` clause never runs.

## 2.3.1 Apply basic OOP to structure and model data

**Syllabus asks:** define and instantiate classes for structured data records; constructors and instance variables; encapsulation with `_protected` and `__private` names; getters and setters.

### Core facts

```python
class Customer:
    currency = "EUR"                       # class variable: shared by all instances

    def __init__(self, name, balance=0.0):
        self.name = name                   # instance variables
        self._segment = "retail"           # "protected" by convention
        self.__balance = balance           # "private": name-mangled to _Customer__balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self.__balance = value

c = Customer("Ana", 120.0)
c.set_balance(150.0)
print(c.name, c.get_balance(), c._segment, Customer.currency)
print(hasattr(c, "__balance"), c._Customer__balance)
```

```text
Ana 150.0 retail EUR
False 150.0
```

- `__init__` is the constructor; it runs when you call `Customer(...)`. `self` is the new instance.
- **Instance variables** (`self.name`) belong to one object; **class variables** (`currency`) are shared.
- A single leading underscore (`_segment`) means "internal, don't touch from outside"; Python does not enforce it.
- A double leading underscore (`__balance`) triggers **name mangling**: inside the class it becomes `_Customer__balance`, so `c.__balance` from outside raises `AttributeError`. It prevents accidental clashes; it is not real security.
- **Getters and setters** control access and validate new values. The Pythonic form is a property:

```python
class Product:
    def __init__(self, price):
        self.price = price                 # goes through the setter

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value
```

`__repr__` returns an unambiguous developer string (shown in the console); `__str__` returns the friendly one used by `print()`. `@dataclass` generates `__init__`, `__repr__` and `__eq__` from annotated fields.

Using the property, `__repr__` and `__str__`, and a dataclass:

```python
from dataclasses import dataclass

class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value

    def __repr__(self):
        return f"Product(price={self.price})"

    def __str__(self):
        return f"{self.price:.2f} EUR"

p = Product(4)
p.price = 5                    # looks like a plain attribute, but runs the setter
print(p.price, repr(p), str(p))
print(p)                       # print() uses __str__
try:
    p.price = -1
except ValueError as e:
    print("ValueError:", e)

@dataclass
class Point:
    x: int
    y: int

print(Point(1, 2), Point(1, 2) == Point(1, 2))
```

```text
5 Product(price=5) 5.00 EUR
5.00 EUR
ValueError: price cannot be negative
Point(x=1, y=2) True
```

`p.price = 5` looks like a plain assignment but runs the setter, which is how `-1` gets rejected. The dataclass wrote `__init__`, `__repr__` and `__eq__` from the two fields, so two equal points compare equal.

### Exam traps

> **Trap.** Double-underscore names are mangled, not hidden: `obj._ClassName__attr` still reaches them.

> **Trap.** Assigning `self.total = 0` inside a method creates an instance attribute that shadows a class attribute of the same name for that one object only.

## 2.3.2 Apply OOP patterns for code reuse

**Syllabus asks:** composition to group related data models, inheritance with method overriding, and polymorphism (for example `.process()` or `.export()` across subclasses).

### Core facts

```python
class Exporter:
    def __init__(self, rows):
        self.rows = rows

    def export(self):
        raise NotImplementedError

    def describe(self):
        return f"{type(self).__name__}: {self.export()}"

class CsvExporter(Exporter):
    def export(self):                              # overrides the parent method
        return "\n".join(",".join(map(str, r)) for r in self.rows)

class JsonExporter(Exporter):
    def __init__(self, rows, indent=None):
        super().__init__(rows)                     # reuse the parent's constructor
        self.indent = indent

    def export(self):
        import json
        return json.dumps(self.rows, indent=self.indent)

for exporter in [CsvExporter([[1, 2]]), JsonExporter([[1, 2]])]:
    print(exporter.describe())                     # same call, different behaviour
```

```text
CsvExporter: 1,2
JsonExporter: [[1, 2]]
```

- **Inheritance** ("is-a"): `class CsvExporter(Exporter)` gets every method of `Exporter`. **Overriding** replaces a parent method by defining one with the same name. `super()` calls the parent's version.
- **Polymorphism**: code calls `.export()` without knowing which subclass it has; each object runs its own version. Python also allows *duck typing*: any object with an `export()` method works, related or not.
- **Composition** ("has-a"): a class holds other objects as attributes. An `Order` *has* a `Customer` and a list of `LineItem`s; it is not a kind of customer. Prefer composition when the relationship is "has-a"; it keeps classes small and loosely coupled.

```python
class LineItem:
    def __init__(self, sku, qty, price):
        self.sku, self.qty, self.price = sku, qty, price

class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def total(self):
        return sum(i.qty * i.price for i in self.items)

order = Order("Ana", [LineItem("tea", 2, 3.0), LineItem("jam", 1, 4.5)])
print(order.customer, len(order.items), order.total())
```

```text
Ana 2 10.5
```

`isinstance(obj, Parent)` is `True` for instances of subclasses too; `issubclass(Child, Parent)` checks classes.

`isinstance`, `issubclass`, and what happens when a subclass skips `super().__init__()`:

```python
class Exporter:
    def __init__(self, rows):
        self.rows = rows

class CsvExporter(Exporter):
    pass

class BrokenExporter(Exporter):
    def __init__(self, rows, sep):
        self.sep = sep                     # forgot super().__init__(rows)

e = CsvExporter([[1, 2]])
print(isinstance(e, CsvExporter), isinstance(e, Exporter), isinstance(e, str))
print(issubclass(CsvExporter, Exporter), issubclass(Exporter, CsvExporter))

b = BrokenExporter([[1, 2]], ";")
try:
    b.rows
except AttributeError as err:
    print("AttributeError:", err)
```

```text
True True False
True False
AttributeError: 'BrokenExporter' object has no attribute 'rows'
```

### Exam traps

> **Trap.** If a subclass defines `__init__` and doesn't call `super().__init__(...)`, the parent's attributes are never set, and methods that use them fail with `AttributeError`.

> **Trap.** "Has-a" → composition; "is-a" → inheritance. A `Report` that contains a `Chart` should not inherit from `Chart`.

## 2.3.3 Manage object identity and comparisons

**Syllabus asks:** reference variables and shared vs independent objects; the `==` and `is` operators; a custom `__eq__()`.

### Core facts

Variables are **references** (names) bound to objects. Assignment copies the reference, not the object.

```python
a = [1, 2, 3]
b = a                  # same object, two names
c = a.copy()           # new, independent list (a shallow copy)
b.append(4)
print(a, c, a == c, a is b, a is c)
```

```text
[1, 2, 3, 4] [1, 2, 3] False True False
```

- `==` compares **values** (it calls `__eq__`); `is` compares **identity** (the same object in memory, same `id()`).
- Use `is` only for singletons: `x is None`, `x is True`. Never compare numbers or strings with `is`; small-integer caching makes such code behave inconsistently.
- Copies: `list(a)`, `a[:]`, `a.copy()` and `copy.copy(a)` are **shallow** (nested objects are still shared); `copy.deepcopy(a)` copies nested objects too. In pandas, `df2 = df` shares the object; `df.copy()` makes an independent one.

A shallow copy shares the inner lists; a deep copy doesn't:

```python
import copy

a = [[1, 2], [3]]
shallow = a.copy()
deep = copy.deepcopy(a)
a[0].append(99)            # change a nested list
a.append([4])              # change the outer list
print(a)
print(shallow)             # shares the nested lists, not the outer one
print(deep)                # fully independent
```

```text
[[1, 2, 99], [3], [4]]
[[1, 2, 99], [3]]
[[1, 2], [3]]
```

Appending to `a` itself doesn't affect `shallow` (it has its own outer list), but changing `a[0]` does, because both point at the same inner list.

**Custom equality.** A class without `__eq__` compares by identity, so two separate objects with identical data are not equal.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Point2(Point):
    def __eq__(self, other):
        if not isinstance(other, Point2):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

print(Point(1, 2) == Point(1, 2), Point2(1, 2) == Point2(1, 2), Point2(1, 2) is Point2(1, 2))
```

```text
False True False
```

Defining `__eq__` without `__hash__` makes instances unhashable (they can't go in sets or be dict keys). Define `__hash__` from the same fields if you need that.

### Exam traps

> **Trap.** `b = a` then `b.append(x)` changes `a` too; it is one list with two names.

> **Trap.** Two `Point(1, 2)` objects without `__eq__` are `!=`. Equality needs a custom `__eq__` (or a `@dataclass`).

## 2.4.1 Perform SQL queries to retrieve and manipulate data

**Syllabus asks:** compose queries with SELECT, FROM, JOINs (INNER, LEFT, RIGHT, FULL), WHERE, GROUP BY, HAVING, ORDER BY and LIMIT: the "SFJWGHOL" clause set.

### Core facts

**Written order: S-F-J-W-G-H-O-L.**

```sql
SELECT   c.region, COUNT(*) AS orders, SUM(o.total) AS revenue
FROM     orders AS o
JOIN     customers AS c ON c.id = o.customer_id
WHERE    o.status = 'paid'
GROUP BY c.region
HAVING   SUM(o.total) > 1000
ORDER BY revenue DESC
LIMIT    5;
```

**Logical order** (how the database evaluates it): FROM and JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. That is why WHERE cannot use aggregates (groups don't exist yet) and why, in standard SQL, WHERE cannot use a column alias defined in SELECT, while ORDER BY can.

| Join | Returns |
|---|---|
| `INNER JOIN` (or `JOIN`) | Only rows with a match in both tables |
| `LEFT JOIN` | Every row of the left table; NULLs where the right table has no match |
| `RIGHT JOIN` | Every row of the right table; NULLs where the left has no match |
| `FULL OUTER JOIN` | Every row of both tables, matched where possible |

<div class="dg"><p class="dg-title">Which rows survive a join</p><div class="dg-compare">
<div class="dg-col"><h4>INNER</h4><ul><li>Matches only</li><li>Unmatched rows on either side disappear</li></ul></div>
<div class="dg-col"><h4>LEFT</h4><ul><li>All left rows</li><li>Right columns NULL when no match</li></ul></div>
<div class="dg-col"><h4>RIGHT</h4><ul><li>All right rows</li><li>Left columns NULL when no match</li></ul></div>
<div class="dg-col"><h4>FULL</h4><ul><li>All rows from both</li><li>NULLs on whichever side is missing</li></ul></div>
</div></div>

The same two tables with an inner join and a left join:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER, name TEXT);
CREATE TABLE orders (customer_id INTEGER, total REAL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cy');
INSERT INTO orders VALUES (1, 50), (1, 70), (2, 20), (9, 15);
""")

def show(sql):
    print(con.execute(sql).fetchall())

show("""SELECT c.name, o.total FROM customers c
        INNER JOIN orders o ON o.customer_id = c.id""")   # Cy and order 9 drop out
show("""SELECT c.name, o.total FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.id""")    # Cy kept, total is NULL (None)
```

```text
[('Ana', 50.0), ('Ana', 70.0), ('Ben', 20.0)]
[('Ana', 50.0), ('Ana', 70.0), ('Ben', 20.0), ('Cy', None)]
```

Cy has no orders, so the inner join drops him and the left join keeps him with `NULL` (`None` in Python). Order 9 has no customer, so neither join returns it.

- **Aggregates**: `COUNT(*)` counts rows; `COUNT(col)` counts non-NULL values; `SUM`, `AVG`, `MIN`, `MAX` ignore NULLs.
- **WHERE** filters rows before grouping; **HAVING** filters groups after aggregation.
- Every column in SELECT that isn't aggregated must appear in GROUP BY (SQLite is lenient here; most databases are not).

Aggregates, `WHERE` and `HAVING` on one table:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales (region TEXT, rep TEXT, amount REAL);
INSERT INTO sales VALUES ('EU', 'Ana', 100), ('EU', 'Ben', NULL), ('EU', 'Ana', 40),
                         ('US', 'Cy', 30), ('US', 'Dee', 20), ('ASIA', 'Eli', 500);
""")

def show(sql):
    print(con.execute(sql).fetchall())

show("SELECT COUNT(*), COUNT(amount), SUM(amount), AVG(amount) FROM sales WHERE region = 'EU'")
show("SELECT region, SUM(amount) FROM sales WHERE amount > 25 GROUP BY region ORDER BY region")
show("SELECT region, SUM(amount) FROM sales GROUP BY region HAVING SUM(amount) > 100 ORDER BY region")
```

```text
[(3, 2, 140.0, 70.0)]
[('ASIA', 500.0), ('EU', 140.0), ('US', 30.0)]
[('ASIA', 500.0), ('EU', 140.0)]
```

`COUNT(*)` counts all 3 EU rows; `COUNT(amount)`, `SUM` and `AVG` skip Ben's `NULL`, so the average is 140 / 2 = 70. `WHERE amount > 25` removes Dee's 20 before grouping, so the US total is 30. In the last query, `HAVING` runs after grouping and drops the US group, whose total of 50 is not over 100.

- Filters: `=`, `<>`/`!=`, `BETWEEN a AND b` (inclusive), `IN (...)`, `LIKE 'A%'` (`%` any run of characters, `_` one character), `IS NULL` / `IS NOT NULL` (never `= NULL`).
- `SELECT DISTINCT` removes duplicate rows; `ORDER BY col DESC`; `LIMIT 10 OFFSET 20` skips 20 rows then returns 10.
- `CASE WHEN total > 100 THEN 'high' ELSE 'low' END` builds conditional columns.

The filters, `NULL` checks, paging and `CASE` in action:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 1.2), ('Avocado', 2.5), ('Bread', 3.0),
                            ('Cake', 12.0), ('Milk', NULL);
""")

def show(sql):
    print(con.execute(sql).fetchall())

show("SELECT name FROM products WHERE price BETWEEN 1.2 AND 3")     # both ends included
show("SELECT name FROM products WHERE name LIKE 'A%'")
show("SELECT name FROM products WHERE name IN ('Cake', 'Milk')")
show("SELECT name FROM products WHERE price = NULL")                # matches nothing
show("SELECT name FROM products WHERE price IS NULL")
show("SELECT name FROM products ORDER BY price DESC LIMIT 2 OFFSET 1")
show("""SELECT name, CASE WHEN price > 10 THEN 'high' ELSE 'low' END
        FROM products WHERE price IS NOT NULL""")
```

```text
[('Apple',), ('Avocado',), ('Bread',)]
[('Apple',), ('Avocado',)]
[('Cake',), ('Milk',)]
[]
[('Milk',)]
[('Bread',), ('Avocado',)]
[('Apple', 'low'), ('Avocado', 'low'), ('Bread', 'low'), ('Cake', 'high')]
```

`ORDER BY price DESC` puts Cake first and Milk (`NULL`) last; `OFFSET 1` skips Cake and `LIMIT 2` keeps the next two.

### Exam traps

> **Trap.** `WHERE COUNT(*) > 5` is an error; conditions on aggregates go in `HAVING`.

> **Trap.** `WHERE col = NULL` matches nothing, because any comparison with NULL is unknown. Use `IS NULL`.

> **Trap.** A LEFT JOIN followed by `WHERE right_table.col = 'x'` removes the unmatched (NULL) rows, turning it into an inner join. Put that condition in the `ON` clause to keep them.

## 2.4.2 Execute fundamental SQL commands

**Syllabus asks:** CRUD operations (Create, Read, Update, Delete): inserting, retrieving, updating and deleting data.

### Core facts

| CRUD | SQL | Example |
|---|---|---|
| Create | `INSERT` | `INSERT INTO products (name, price) VALUES ('Tea', 2.5);` |
| Read | `SELECT` | `SELECT name, price FROM products WHERE price < 3;` |
| Update | `UPDATE` | `UPDATE products SET price = 2.75 WHERE name = 'Tea';` |
| Delete | `DELETE` | `DELETE FROM products WHERE price IS NULL;` |

- `UPDATE` or `DELETE` **without** `WHERE` changes or removes **every** row. Run the matching `SELECT` first to see what will be affected.
- `DELETE FROM t` empties a table but keeps it; `DROP TABLE t` removes the table itself (structure and data).
- `CREATE TABLE`, `ALTER TABLE` and `DROP TABLE` are data *definition* statements (DDL); CRUD's "Create" is about rows (`INSERT`).
- Inserting several rows: `INSERT INTO t (a, b) VALUES (1, 'x'), (2, 'y');` or, from Python, `executemany`.
- In Python's `sqlite3`, `INSERT`, `UPDATE` and `DELETE` run inside a transaction that you must `commit()`; closing without committing discards them.

All four operations, an `UPDATE` without `WHERE`, and `DELETE` versus `DROP`:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products (name, price) VALUES ('Tea', 2.5), ('Jam', 4.0)")   # Create
con.commit()
print(con.execute("SELECT * FROM products").fetchall())                               # Read

con.execute("UPDATE products SET price = 2.75 WHERE name = 'Tea'")                    # Update one row
print(con.execute("SELECT * FROM products").fetchall())

con.execute("UPDATE products SET price = 0")                                          # no WHERE: every row
print(con.execute("SELECT * FROM products").fetchall())
con.rollback()                                                                        # undo since last commit
print(con.execute("SELECT * FROM products").fetchall())

con.execute("DELETE FROM products WHERE name = 'Jam'")                                # Delete
con.execute("DELETE FROM products")                                                   # all rows; table stays
print(con.execute("SELECT COUNT(*) FROM products").fetchone())
con.execute("DROP TABLE products")                                                    # table gone
try:
    con.execute("SELECT * FROM products")
except sqlite3.OperationalError as e:
    print("OperationalError:", e)
```

```text
[('Tea', 2.5), ('Jam', 4.0)]
[('Tea', 2.75), ('Jam', 4.0)]
[('Tea', 0.0), ('Jam', 0.0)]
[('Tea', 2.5), ('Jam', 4.0)]
(0,)
OperationalError: no such table: products
```

The unfiltered `UPDATE` set every price to 0; `rollback()` undid it because nothing had been committed since the insert.

### Exam traps

> **Trap.** `DELETE` removes rows; `DROP` removes the table. "Remove all rows but keep the table" is `DELETE FROM t;`.

## 2.4.3 Establish database connections using Python

**Syllabus asks:** connect with `sqlite3` and `pymysql`, and resolve common connection issues.

### Core facts

```python
import sqlite3

con = sqlite3.connect(":memory:")            # or a file path; the file is created if missing
cur = con.cursor()
cur.execute("CREATE TABLE sales (region TEXT, amount REAL)")
cur.executemany("INSERT INTO sales VALUES (?, ?)", [("EU", 120.0), ("US", 80.0), ("EU", 30.0)])
con.commit()

cur.execute("SELECT region, SUM(amount) FROM sales GROUP BY region ORDER BY region")
print(cur.fetchall())
print(cur.execute("SELECT COUNT(*) FROM sales").fetchone())
con.close()
```

```text
[('EU', 150.0), ('US', 80.0)]
(3,)
```

- `connect()` → `cursor()` → `execute()` → `fetchone()` / `fetchall()` / `fetchmany(n)` → `commit()` → `close()`.
- `fetchone()` returns one tuple (or `None` when no rows are left); `fetchall()` returns a list of tuples.
- `with sqlite3.connect(path) as con:` commits on success and rolls back on an exception, but it does **not** close the connection.
- `con.row_factory = sqlite3.Row` lets you read columns by name (`row["region"]`).
- pandas: `pd.read_sql_query("SELECT ...", con)` returns a DataFrame; `df.to_sql("table", con, if_exists="append", index=False)` writes one.

Fetching rows one at a time, reading columns by name, and pandas:

```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales (region TEXT, amount REAL)")
con.executemany("INSERT INTO sales VALUES (?, ?)", [("EU", 120.0), ("US", 80.0)])

cur = con.execute("SELECT region, amount FROM sales ORDER BY region")
print(cur.fetchone())         # first row
print(cur.fetchone())         # next row
print(cur.fetchone())         # no rows left -> None

con.row_factory = sqlite3.Row
row = con.execute("SELECT region, amount FROM sales").fetchone()
print(row["region"], row["amount"])

print(pd.read_sql_query("SELECT region, amount FROM sales", con))

with con:                     # commits this block (or rolls back on error)...
    con.execute("INSERT INTO sales VALUES ('ASIA', 50.0)")
print(con.execute("SELECT COUNT(*) FROM sales").fetchone()[0])   # ...but the connection is still open
con.close()
```

```text
('EU', 120.0)
('US', 80.0)
None
EU 120.0
  region  amount
0     EU   120.0
1     US    80.0
3
```

```python
import pymysql

con = pymysql.connect(host="db.example.com", port=3306, user="analyst",
                      password=os.environ["DB_PASSWORD"], database="shop")
with con.cursor() as cur:
    cur.execute("SELECT id, total FROM orders WHERE total > %s", (100,))
    rows = cur.fetchall()
con.close()
```

**Common connection problems.**

| Symptom | Likely cause |
|---|---|
| `ModuleNotFoundError: No module named 'pymysql'` | Driver not installed (`pip install pymysql`) |
| Access denied for user | Wrong user name or password, or no privileges on that database |
| Can't connect / timed out | Wrong host or port, server not running, firewall |
| Unknown database | Database name misspelled or not created |
| SQLite `no such table` | Wrong file path: `connect()` silently created a new, empty database |
| SQLite `database is locked` | Another connection holds a write lock; commit or close it |
| Inserted rows disappear | `commit()` was never called |

### Exam traps

> **Trap.** `sqlite3.connect("wrong_name.db")` does not fail; it creates an empty file. The error appears later as "no such table".

> **Trap.** pymysql uses `%s` placeholders; sqlite3 uses `?` (or `:name`). Neither is Python string formatting.

## 2.4.4 Execute parameterized SQL queries through Python

**Syllabus asks:** write and run parameterized queries, and explain how they prevent SQL injection and protect data integrity.

### Core facts

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, role TEXT)")
con.executemany("INSERT INTO users VALUES (?, ?)", [("ana", "admin"), ("ben", "viewer")])

name = "ben"
print(con.execute("SELECT role FROM users WHERE name = ?", (name,)).fetchall())
print(con.execute("SELECT role FROM users WHERE name = :n", {"n": "ana"}).fetchall())

attack = "x' OR '1'='1"
print(con.execute("SELECT role FROM users WHERE name = ?", (attack,)).fetchall())
print(con.execute(f"SELECT role FROM users WHERE name = '{attack}'").fetchall())
```

```text
[('viewer',)]
[('admin',)]
[]
[('admin',), ('viewer',)]
```

- Placeholders: `?` with a tuple or list (`(name,)`: note the comma in a one-item tuple), or `:name` with a dict. pymysql uses `%s` / `%(name)s`.
- The driver sends the values **separately** from the SQL text, so a value can never change the query's structure. The last line above shows what string formatting allows: the injected `OR '1'='1'` returned every row.
- Parameters also handle quoting (names like `O'Brien`), types and dates for you, and let the database reuse the query plan.
- `executemany(sql, rows)` runs one parameterized statement for many rows.
- Placeholders work for **values only**, not table or column names. If a user chooses a column, check it against a fixed allow-list.

### Exam traps

> **Trap.** `cur.execute("... WHERE id = ?", (5))` fails: `(5)` is an integer, not a tuple. Write `(5,)` or `[5]`.

> **Trap.** An f-string with quotes around the value is still injectable. Only real placeholders are safe.

## 2.4.5 Understand and convert SQL data types

**Syllabus asks:** identify SQL data types and their Python counterparts, and convert types correctly when moving data between them.

### Core facts

| SQL (SQLite storage class) | Python (`sqlite3`) | pandas after `read_sql` |
|---|---|---|
| `NULL` | `None` | `NaN` / `None` / `NaT` |
| `INTEGER` | `int` | `int64` (becomes `float64` if the column has NULLs) |
| `REAL` | `float` | `float64` |
| `TEXT` | `str` | text column (`object` or `str` dtype) |
| `BLOB` | `bytes` | `object` |

| MySQL type | Python (`pymysql`) |
|---|---|
| `INT`, `BIGINT` | `int` |
| `DECIMAL(10,2)` | `decimal.Decimal` (exact, good for money) |
| `FLOAT`, `DOUBLE` | `float` |
| `VARCHAR`, `TEXT` | `str` |
| `DATE` / `DATETIME` | `datetime.date` / `datetime.datetime` |
| `BOOLEAN` (`TINYINT(1)`) | `int` (0 or 1) |

- SQLite has no dedicated date or boolean type. Store dates as ISO 8601 `TEXT` (`'2025-07-15'`), which sorts correctly as text, and convert when reading (`datetime.date.fromisoformat`, `pd.to_datetime`, or `parse_dates=` in `read_sql_query`). Python `True`/`False` are stored as 1/0.
- SQLite uses *type affinity*: a column declared `INTEGER` can still hold text. Validate types in Python before inserting.
- A DataFrame integer column with a missing value becomes `float64`; use the nullable `"Int64"` dtype to keep integers.
- Use `Decimal` (or integer cents) for money to avoid float rounding (`0.1 + 0.2`).

What comes back from SQLite, and how to convert it:

```python
import sqlite3
import datetime
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (qty INTEGER, price REAL, day TEXT, paid INTEGER, note TEXT)")
con.execute("INSERT INTO t VALUES (?, ?, ?, ?, ?)", (3, 2.5, "2025-07-15", True, None))
con.execute("INSERT INTO t VALUES (?, ?, ?, ?, ?)", (None, 4.0, "2025-07-16", False, "late"))

row = con.execute("SELECT * FROM t").fetchone()
print(row)
print([type(v).__name__ for v in row])          # the date comes back as str, True as 1
print(datetime.date.fromisoformat(row[2]) + datetime.timedelta(days=1))

df = pd.read_sql_query("SELECT qty, day FROM t", con, parse_dates=["day"])
print(df["qty"].dtype, df["day"].dt.day_name().tolist())   # NULL turns qty into float64; day is a real date
print(df["qty"].astype("Int64").tolist())       # nullable integers keep whole numbers

con.execute("INSERT INTO t (qty) VALUES ('three')")   # INTEGER column happily stores text
print(con.execute("SELECT qty, typeof(qty) FROM t").fetchall())
```

```text
(3, 2.5, '2025-07-15', 1, None)
['int', 'float', 'str', 'int', 'NoneType']
2025-07-16
float64 ['Tuesday', 'Wednesday']
[3, <NA>]
[(3, 'integer'), (None, 'null'), ('three', 'text')]
```

The date comes back as text and `True` as `1`, so convert before doing arithmetic. The last query shows type affinity: the `INTEGER` column accepted the text `'three'`.

### Exam traps

> **Trap.** Reading a SQLite date column gives Python `str`, not `datetime`. Convert it before doing date arithmetic.

## 2.4.6 Understand essential database security concepts

**Syllabus asks:** strategies to prevent SQL injection and write secure SQL from Python.

### Core facts

**SQL injection** happens when user input is pasted into SQL text, so the input can change the query. `name = "x' OR '1'='1"` turns a lookup into "return every row"; `"x'; DROP TABLE users; --"` tries to run a second statement.

Defences, most important first:

1. **Parameterized queries** for every value that comes from outside (users, files, APIs).
2. **Allow-lists** for identifiers (table, column, sort direction) that can't be parameterized.
3. **Least privilege**: the account a reporting script uses should only read the tables it needs.
4. **Keep credentials out of code**: environment variables or a secrets manager, never a hard-coded password in a script or notebook in version control.
5. **Validate input** (type, length, format) and **don't show raw database errors** to end users.
6. Encrypted connections (TLS) to remote databases; backups; audit logs.

Escaping quotes by hand, or blocking a few "dangerous" words, is not a reliable defence. ORMs such as SQLAlchemy are safe because they parameterize under the hood, until you pass them raw formatted SQL.

### Exam traps

> **Trap.** Input validation alone does not prevent injection; parameterization does. Validation is an extra layer.

> **Trap.** `cursor.execute("SELECT * FROM t WHERE id = %s" % user_id)` uses Python's `%` operator (string formatting), not a driver placeholder. It is injectable.
