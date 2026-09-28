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

- `range(stop)`, `range(start, stop)`, `range(start, stop, step)`; `stop` is never included.
- `break` leaves the loop; `continue` jumps to the next iteration; a loop's `else` runs only if the loop ended without `break`.
- `enumerate(items, start=1)` yields `(index, item)`; `zip(a, b)` pairs items and stops at the shorter one.
- Conditional expression: `label = "high" if x > 100 else "low"`; comparisons chain: `0 < x < 10`.
- Comprehensions: `[x * 2 for x in data if x > 0]`, `{k: v for k, v in pairs}`.

### Exam traps

> **Trap.** `range(1, 10, 3)` gives 1, 4, 7, never 10. Count the loop body's executions carefully.

> **Trap.** An `if` that assigns to a global name inside a function makes that name local everywhere in the function; reading it earlier raises `UnboundLocalError`.

## 2.1.2 Analyze and create Python functions

**Syllabus asks:** design functions with a clear purpose; tell positional (indexed) arguments from keyword arguments; use required vs optional parameters.

### Core facts

```python
def summarize(values, precision=2, *, label="mean"):
    """Return a labeled mean of values, rounded to precision places."""
    avg = sum(values) / len(values)
    return f"{label}: {round(avg, precision)}"

print(summarize([1, 2, 4]))                       # defaults used
print(summarize([1, 2, 4], 1))                    # positional
print(summarize([1, 2, 4], precision=0, label="avg"))
```

```text
mean: 2.33
mean: 2.3
avg: 2.0
```

- **Parameters** are the names in the definition; **arguments** are the values in the call.
- **Positional** arguments match parameters by order; **keyword** arguments match by name and can come in any order. In a call, positional arguments must come before keyword arguments (`f(a=1, 2)` is a `SyntaxError`).
- A parameter **without** a default is required; one **with** a default is optional. Parameters with defaults must come after those without in the definition.
- Parameters after a bare `*` are **keyword-only** (`label` above); parameters before a `/` are positional-only.
- `*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dict.
- A function without `return` (or with a bare `return`) returns `None`.
- Missing a required argument, or passing one twice, raises `TypeError`.

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
- Dicts: `d[k]` raises `KeyError` if missing; `d.get(k, default)` doesn't. Iterate with `.items()`. Keys must be hashable (str, int, tuple of immutables; not lists).
- Strings are immutable: methods such as `.replace()` and `.upper()` return new strings.
- `(5)` is just `5`; a one-item tuple needs a comma: `(5,)`.
- `collections.Counter` counts items; `collections.defaultdict(list)` groups without checking for missing keys.

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
- `except (ValueError, TypeError) as e:` catches either; `e` holds the exception object.
- A bare `except:` (or `except Exception:` everywhere) hides bugs. Catch what you expect.
- `raise ValueError("price must be positive")` signals a problem; `raise` alone re-raises inside an `except` block.
- Custom exceptions subclass `Exception`: `class DataQualityError(Exception): pass`.

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
        self.customer = customer          # composition: an Order has a customer
        self.items = items                # and has line items

    def total(self):
        return sum(i.qty * i.price for i in self.items)
```

`isinstance(obj, Parent)` is `True` for instances of subclasses too; `issubclass(Child, Parent)` checks classes.

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

- **Aggregates**: `COUNT(*)` counts rows; `COUNT(col)` counts non-NULL values; `SUM`, `AVG`, `MIN`, `MAX` ignore NULLs.
- **WHERE** filters rows before grouping; **HAVING** filters groups after aggregation.
- Every column in SELECT that isn't aggregated must appear in GROUP BY (SQLite is lenient here; most databases are not).
- Filters: `=`, `<>`/`!=`, `BETWEEN a AND b` (inclusive), `IN (...)`, `LIKE 'A%'` (`%` any run of characters, `_` one character), `IS NULL` / `IS NOT NULL` (never `= NULL`).
- `SELECT DISTINCT` removes duplicate rows; `ORDER BY col DESC`; `LIMIT 10 OFFSET 20` skips 20 rows then returns 10.
- `CASE WHEN total > 100 THEN 'high' ELSE 'low' END` builds conditional columns.

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
