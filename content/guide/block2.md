# Block 2: Programming and Database Skills

Block 2 is the largest block: 16 items, 33.3% of the exam. It covers core Python (syntax, functions, data structures, style), modules and exceptions, object-oriented programming for data records, and SQL both on its own and from Python. Many items show a few lines of code and ask what they print or which line fixes a problem.

## 2.1.1 Apply Python syntax and control structures

**Syllabus asks:** variables, scopes and basic data types; loops and conditionals to control the flow of data.

### Core facts

**Types.** `int`, `float`, `str`, `bool`, `NoneType`. Python is dynamically typed: a name can be rebound to a value of another type. `type(x)` returns the type; `isinstance(x, (int, float))` checks against one or more types. `bool` is a subclass of `int` (`True + True == 2`).

**Operators to know.** `/` always returns a float (`7 / 2 == 3.5`); `//` floors (`7 // 2 == 3`, `-7 // 2 == -4`); `%` is the remainder; `**` is power. Floats are approximate: `0.1 + 0.2 == 0.30000000000000004`.

**Truthiness.** `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None` and `False` are falsy; everything else is truthy.

**`print` options.** By default `print` puts a space between its arguments and starts a new line at the end. `sep=` changes what goes between the arguments, and `end=` changes what goes at the end, so the next `print` can continue on the same line:

```python
print("a", "b")
print("a", "b", sep="-")
print("no newline", end=" | ")
print("same line")
```

```text
a b
a-b
no newline | same line
```

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

**`range`: a sequence of numbers.** `range` produces numbers for a loop to count through. The number you stop at is **never included**. (`list()` below just turns the range into a list so it can be printed.)

```python
print(list(range(4)))         # range(stop): starts at 0
print(list(range(2, 6)))      # range(start, stop)
```

```text
[0, 1, 2, 3]
[2, 3, 4, 5]
```

A third number sets the **step**, the gap between values. A negative step counts down.

```python
print(list(range(1, 10, 3)))     # 1, then +3 each time, stopping before 10
print(list(range(10, 0, -3)))    # count down by 3, stopping before 0
```

```text
[1, 4, 7]
[10, 7, 4, 1]
```

**`break`: leave the loop early.** `break` stops the loop immediately, even if there are items left.

```python
for n in [3, 8, 5]:
    print("checking", n)
    if n > 6:
        print("found", n)
        break
```

```text
checking 3
checking 8
found 8
```

5 is never checked, because the loop stopped at 8.

**`continue`: skip to the next item.** `continue` skips the rest of this pass through the loop and moves straight on to the next item.

```python
for n in [1, 2, 3, 4]:
    if n == 2:
        continue          # skip 2
    print(n)
```

```text
1
3
4
```

**A loop's `else`.** A `for` or `while` loop can have an `else` block. It runs only if the loop finished **without** a `break`. That makes it a natural place for "searched everything, found nothing":

```python
for n in [3, 5]:
    if n > 6:
        print("found", n)
        break
else:
    print("nothing over 6")       # runs: the loop never hit break
```

```text
nothing over 6
```

If the list had contained 8, the loop would have hit `break` and the `else` would have been skipped.

**`enumerate`: a counter alongside each item.** `enumerate(items)` gives you each item together with its position. By default it counts from 0, like list positions:

```python
items = ["tea", "jam", "bread"]
for number, item in enumerate(items):
    print(number, item)
```

```text
0 tea
1 jam
2 bread
```

`start=1` counts from 1 instead, which suits numbered lists for people:

```python
items = ["tea", "jam", "bread"]
for number, item in enumerate(items, start=1):
    print(number, item)
```

```text
1 tea
2 jam
3 bread
```

**`zip`: walk through two lists together.** `zip(a, b)` pairs the first item of `a` with the first of `b`, the second with the second, and so on. If one list is shorter, it stops there and the extra items are dropped without warning.

```python
names = ["Ann", "Bob", "Cy"]
scores = [90, 75]               # only two scores

for name, score in zip(names, scores):
    print(name, score)
```

```text
Ann 90
Bob 75
```

Cy has no score to pair with, so that name is left out.

**Choosing between two values in one line.** `value_if_true if condition else value_if_false` is a compact `if`/`else` that produces a value:

```python
for x in [50, 150]:
    label = "high" if x > 100 else "low"
    print(x, label)
```

```text
50 low
150 high
```

It does the same as this longer version:

```python
x = 150
if x > 100:
    label = "high"
else:
    label = "low"
print(label)
```

```text
high
```

**Chained comparisons.** `0 < x < 10` means "x is between 0 and 10": it is short for `0 < x and x < 10`.

```python
x = 5
print(0 < x < 10)     # both parts true
print(0 < x < 3)      # 5 < 3 is false
```

```text
True
False
```

**List comprehensions: building a list in one line.** A comprehension is a short way to write a loop that builds a list. These two produce the same result:

```python
data = [3, -1, 4, 0]

doubled = []
for x in data:
    doubled.append(x * 2)
print(doubled)

print([x * 2 for x in data])      # the same, as a comprehension
```

```text
[6, -2, 8, 0]
[6, -2, 8, 0]
```

Read `[x * 2 for x in data]` as "x times 2, for each x in data". Adding `if` at the end keeps only the items that pass the test:

```python
data = [3, -1, 4, 0]
print([x * 2 for x in data if x > 0])     # only the positive numbers, doubled
```

```text
[6, 8]
```

**Dict comprehensions.** Curly braces with `key: value` build a dict the same way:

```python
prices = {"tea": 2, "jam": 4}
print({item: price * 10 for item, price in prices.items()})
```

```text
{'tea': 20, 'jam': 40}
```

### Exam traps

> **Trap.** `range(1, 10, 3)` gives 1, 4, 7, never 10. Count the loop body's executions carefully.

> **Trap.** An assignment to a name anywhere inside a function, even inside an `if` that never runs, makes that name local for the whole function; reading it before the assignment raises `UnboundLocalError`.

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

**`lambda`: a one-line function.** `lambda x: x * 2` is a function with no name: the parameters go before the colon, and the single expression after it is the return value. It is mostly used where a short function is passed to another function. (PEP 8 advises using `def` rather than assigning a lambda to a name.)

**Key functions: sorting and choosing by something else.** `sorted`, `list.sort`, `min` and `max` take `key=`, a function that is applied to each item before comparing. A tuple key sorts by several things in turn, and a minus sign reverses a numeric part.

```python
orders = [("tea", 3, 2.5), ("jam", 1, 4.0), ("oat", 3, 5.0), ("fig", 2, 3.0)]

print(sorted(orders, key=lambda o: o[2]))             # by price
print(max(orders, key=lambda o: o[1] * o[2]))         # largest qty × price
print(sorted(orders, key=lambda o: (-o[1], o[0])))    # qty high to low, then name A to Z
```

```text
[('tea', 3, 2.5), ('fig', 2, 3.0), ('jam', 1, 4.0), ('oat', 3, 5.0)]
('oat', 3, 5.0)
[('oat', 3, 5.0), ('tea', 3, 2.5), ('fig', 2, 3.0), ('jam', 1, 4.0)]
```

`oat` and `tea` both have qty 3, so the second part of the key, the name, puts `oat` first.

A key can also be an existing function. Pass the function itself, `key=len`, not the result of calling it, `key=len()`:

```python
words = ["banana", "apple", "Cherry", "fig"]
print(sorted(words))                  # capitals sort before lowercase
print(sorted(words, key=str.lower))   # compare lowercased copies
print(sorted(words, key=len))         # shortest first; ties keep their order
```

```text
['Cherry', 'apple', 'banana', 'fig']
['apple', 'banana', 'Cherry', 'fig']
['fig', 'apple', 'banana', 'Cherry']
```

**`map` and `filter`.** `map(f, items)` applies `f` to each item; `filter(f, items)` keeps the items where `f` returns True. Both give back a lazy object, so wrap them in `list()` to see the values. A list comprehension does the same job and is often clearer:

```python
prices = [2.5, 4.0, 1.0]
print(list(map(lambda p: p * 2, prices)))
print(list(filter(lambda p: p > 2, prices)))
print([p * 2 for p in prices], [p for p in prices if p > 2])
```

```text
[5.0, 8.0, 2.0]
[2.5, 4.0]
[5.0, 8.0, 2.0] [2.5, 4.0]
```

**Clear purpose.** One job per function, a descriptive verb name (`load_orders`, `clean_prices`), a docstring, and return values instead of printing inside the function, so the result can be reused and tested.

### Exam traps

> **Trap.** `def f(a=1, b):` is a `SyntaxError`: a required parameter cannot follow an optional one.

> **Trap.** Mutable default arguments (`[]`, `{}`) keep their contents between calls. Use `None` and create the object inside.

> **Trap.** `key=` takes a function, not a value: `sorted(words, key=len)` works, while `key=len()` raises `TypeError` before sorting starts.

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

**Indexing: one item by position.** Lists, tuples and strings number their items from 0. A negative index counts from the end, so `-1` is the last item.

```python
letters = ["a", "b", "c", "d", "e"]
word = "Python"

print(letters[0], letters[2], letters[-1])
print(word[0], word[-2])
```

```text
a c e
P o
```

An index past the end raises an `IndexError`:

```python
letters = ["a", "b", "c"]
try:
    letters[3]
except IndexError as e:
    print("IndexError:", e)
```

```text
IndexError: list index out of range
```

**Slicing: a run of items.** `seq[start:stop]` takes the items from position `start` up to, but **not** including, `stop`. Leave out `start` to begin at the first item, or `stop` to run to the end. A slice is a new list (or string), and a slice that runs past the end never raises an error: it just stops at the last item.

```python
nums = [10, 20, 30, 40, 50]

print(nums[1:3])      # positions 1 and 2
print(nums[:2])       # the first two
print(nums[3:])       # from position 3 to the end
print(nums[-2:])      # the last two
print(nums[1:99])     # a stop past the end is fine
```

```text
[20, 30]
[10, 20]
[40, 50]
[40, 50]
[20, 30, 40, 50]
```

When both ends are inside the list, `nums[a:b]` holds `b - a` items: `nums[1:3]` has 2.

**A step: `[start:stop:step]`.** A third number jumps that many positions each time. A negative step walks backwards, so `[::-1]` reverses.

```python
nums = [10, 20, 30, 40, 50]
word = "Python"

print(nums[::2])      # every second item
print(nums[::-1])     # reversed
print(word[1:5:2])    # positions 1 and 3
print(word[::-1])
```

```text
[10, 30, 50]
[50, 40, 30, 20, 10]
yh
nohtyP
```

**Changing items.** A list can be changed through an index or a slice. Strings and tuples can't be changed, so you build a new one instead.

```python
nums = [10, 20, 30, 40, 50]
nums[0] = 99
nums[1:3] = [0]           # replace positions 1 and 2 with one item
print(nums)

word = "Python"
try:
    word[0] = "J"
except TypeError as e:
    print("TypeError:", e)
print("J" + word[1:])     # build a new string instead
```

```text
[99, 0, 40, 50]
TypeError: 'str' object does not support item assignment
Jython
```

**Adding to a list: `append` and `extend`.** `append` adds **one** item to the end. `extend` takes a collection and adds **each** of its items.

```python
a = [1, 2]
a.append([3, 4])      # adds the list [3, 4] as a single item
print(a)

b = [1, 2]
b.extend([3, 4])      # adds 3, then 4
print(b)
```

```text
[1, 2, [3, 4]]
[1, 2, 3, 4]
```

`a` now has three items, the last of which is itself a list. `b` has four numbers.

**Removing from a list: `pop` and `remove`.** `pop` removes an item **by position** and gives it back to you; with no position it takes the last item. `remove` deletes the first item **equal to a value** you name.

```python
letters = ["a", "b", "c", "b"]

last = letters.pop()       # removes and returns the last item
print(last, letters)

first = letters.pop(0)     # removes and returns the item at position 0
print(first, letters)

letters.remove("b")        # removes the first "b"
print(letters)
```

```text
b ['a', 'b', 'c']
a ['b', 'c']
['c']
```

`insert(position, item)` does the opposite of `pop`: `letters.insert(0, "z")` puts `"z"` at the front.

**Sorting: `sorted()` versus `.sort()`.** `sorted(nums)` gives you a **new** sorted list and leaves `nums` alone. `nums.sort()` sorts `nums` itself and gives back `None`.

```python
nums = [3, 1, 2]

new_list = sorted(nums)
print(new_list, nums)      # nums is unchanged

result = nums.sort()
print(result, nums)        # nums is now sorted; result is None
```

```text
[1, 2, 3] [3, 1, 2]
None [1, 2, 3]
```

This is why `nums = nums.sort()` is a classic mistake: it replaces your list with `None`.

**Sorting by something else: `key=`.** By default, sorting compares the items themselves. Sorting a dict sorts its keys, so names come out in alphabetical order:

```python
scores = {"ana": 81, "ben": 67, "cara": 92}
print(sorted(scores))
```

```text
['ana', 'ben', 'cara']
```

`key=` gives a function that is applied to each item first, and sorting uses its results instead. With `key=scores.get`, each name is replaced by its score for the comparison, so the names come out from lowest score to highest:

```python
scores = {"ana": 81, "ben": 67, "cara": 92}
print(sorted(scores, key=scores.get))
print(sorted(scores, key=scores.get, reverse=True))   # highest score first
```

```text
['ben', 'ana', 'cara']
['cara', 'ana', 'ben']
```

**Reading from a dict: `[]` versus `.get()`.** Square brackets raise a `KeyError` if the key isn't there. `.get(key, default)` returns the default instead (or `None` if you don't give one).

```python
stock = {"tea": 4, "jam": 0}

print(stock["tea"])
print(stock.get("milk"))         # missing: None
print(stock.get("milk", 0))      # missing: the default, 0

try:
    stock["milk"]
except KeyError as e:
    print("KeyError:", e)
```

```text
4
None
0
KeyError: 'milk'
```

**Looping over a dict.** `.items()` gives you each key and its value together:

```python
stock = {"tea": 4, "jam": 0}
for item, qty in stock.items():
    print(item, qty)
```

```text
tea 4
jam 0
```

`.keys()` gives just the keys and `.values()` just the values. Wrap them in `list()` or `sorted()` to get a list:

```python
stock = {"tea": 4, "jam": 0, "oat": 7}
print(list(stock.keys()))
print(sorted(stock.values()))
print(sum(stock.values()))
```

```text
['tea', 'jam', 'oat']
[0, 4, 7]
11
```

**What can be a dict key.** A key must be **hashable**, which in practice means it can't change. Strings, numbers and tuples work; lists don't, because a list can be changed after it is created.

```python
prices = {("tea", "large"): 3.5}     # a tuple works as a key
print(prices[("tea", "large")])

try:
    {["tea", "large"]: 3.5}          # a list doesn't
except TypeError as e:
    print("TypeError:", e)
```

```text
3.5
TypeError: unhashable type: 'list'
```

**Strings can't be changed.** String methods never change the original string. They return a new one, which you have to store.

```python
word = "data"
word.upper()            # result thrown away
print(word)

word = word.upper()     # store the result
print(word)
```

```text
data
DATA
```

**String methods.** Each of these returns a new value; none changes the original string.

| Method | Example | Result |
|---|---|---|
| `upper()`, `lower()`, `title()` | `"tea bag".title()` | `'Tea Bag'` |
| `strip()`, `lstrip()`, `rstrip()` | `"  x ".strip()` | `'x'` |
| `replace(old, new)` | `"1,200".replace(",", "")` | `'1200'` |
| `split(sep)` | `"a;b;c".split(";")` | `['a', 'b', 'c']` |
| `sep.join(items)` | `"-".join(["a", "b"])` | `'a-b'` |
| `startswith(x)`, `endswith(x)` | `"report.csv".endswith(".csv")` | `True` |
| `find(x)` / `index(x)` | `"data".find("t")` | `2`; for a missing `x`, `find` gives `-1` and `index` raises `ValueError` |
| `count(x)` | `"banana".count("a")` | `3` |
| `isdigit()`, `isalpha()` | `"2025".isdigit()` | `True` |
| `x in s` | `"ana" in "banana"` | `True` |

```python
code = "  INV-2025-0042 "
clean = code.strip()

print(clean.lower(), clean.split("-"))
print(clean.startswith("INV"), clean.find("-"), clean.find("X"))
print(clean.replace("-", "/"), "-".join(["2025", "07", "15"]))
print("2025".isdigit(), "20.5".isdigit(), clean.count("0"))
```

```text
inv-2025-0042 ['INV', '2025', '0042']
True 3 -1
INV/2025/0042 2025-07-15
True False 3
```

`"20.5".isdigit()` is `False` because `.` isn't a digit, so `isdigit` can't check decimal numbers; try `float()` inside `try`/`except` instead (section 2.2.2).

`split()` with no argument splits on any run of whitespace and drops empty pieces. `split(" ")` splits on every single space, so double spaces leave empty strings behind:

```python
text = "tea  jam "
print(text.split())       # any run of spaces; empty pieces dropped
print(text.split(" "))    # exactly one space each time
```

```text
['tea', 'jam']
['tea', '', 'jam', '']
```

**f-strings: putting values into text.** In `f"..."`, each `{expression}` is replaced by its value. A colon after the expression adds a **format spec** that controls how the value looks:

| Spec | Example | Result |
|---|---|---|
| `.2f`: 2 decimal places | `f"{3.14159:.2f}"` | `3.14` |
| `,`: thousands separator | `f"{1234567:,}"` | `1,234,567` |
| `.1%`: percentage | `f"{0.256:.1%}"` | `25.6%` |
| `>6`, `<6`, `^6`: align in a width | `f"{'ab':>6}"` | `'    ab'` |
| `03`: pad with zeros | `f"{7:03}"` | `007` |
| `=`: show the expression too | `f"{x=}"` | `x=5` |

```python
price = 1234.5
share = 0.256
item = "tea"

print(f"{item}: {price:.2f}")
print(f"{price:,.2f} | {share:.1%} | {7:03}")
print(f"[{item:>6}] [{item:<6}] [{item:^7}]")
print(f"{price * 2 = }")
```

```text
tea: 1234.50
1,234.50 | 25.6% | 007
[   tea] [tea   ] [  tea  ]
price * 2 = 2469.0
```

**Rounding.** `round(x, n)` returns a number; a format spec such as `:.2f` returns text. Both round a value exactly halfway to the **even** neighbour, and floats that look like halves often aren't stored exactly, so the results can surprise:

```python
print(round(2.5), round(3.5), round(-2.5))
print(round(2.675, 2), f"{2.675:.2f}")
```

```text
2 4 -2
2.67 2.67
```

2.675 is stored as a float just below 2.675, so it rounds down.

**One-item tuples need a comma.** Brackets alone just group things, like in maths. It's the comma that makes a tuple.

```python
print(type((5)))      # just the number 5
print(type((5,)))     # a tuple holding 5
```

```text
<class 'int'>
<class 'tuple'>
```

**Counting with `Counter`.** `collections.Counter` counts how many times each item appears. Asking for an item it never saw gives 0, not an error.

```python
from collections import Counter

colors = ["red", "blue", "red", "green", "red"]
counts = Counter(colors)

print(counts["red"])
print(counts["pink"])
print(counts.most_common(2))     # the two most common items
```

```text
3
0
[('red', 3), ('blue', 1)]
```

**Grouping with `defaultdict`.** A normal dict raises `KeyError` the first time you add to a key that isn't there yet. `defaultdict(list)` creates an empty list for a new key automatically, so you can append straight away.

```python
from collections import defaultdict

sales = [("EU", 10), ("US", 5), ("EU", 7)]

by_region = defaultdict(list)
for region, amount in sales:
    by_region[region].append(amount)

print(dict(by_region))
```

```text
{'EU': [10, 7], 'US': [5]}
```

**Unpacking.** Assigning a sequence to several names takes it apart, one item per name. A name with a `*` collects whatever is left over into a list. Unpacking also swaps two values without a temporary variable.

```python
point = (3, 7)
x, y = point
first, *rest = [10, 20, 30, 40]
*start, last = "abc"
a, b = 1, 2
a, b = b, a                    # swap
print(x, y, first, rest, start, last, a, b)
```

```text
3 7 10 [20, 30, 40] ['a', 'b'] c 2 1
```

The number of names must match the number of items (unless one name has a `*`), otherwise Python raises a `ValueError`:

```python
try:
    x, y = (1, 2, 3)
except ValueError as e:
    print(type(e).__name__)
```

```text
ValueError
```

Unpacking is what happens in `for name, score in zip(...)` and `for key, value in d.items()`.

**More dict methods: `update`, `setdefault`, `pop`.** `update` copies another dict in, overwriting keys that already exist. `setdefault(key, default)` returns the key's value, first inserting `default` if the key is missing, which makes grouping into lists a one-liner. `pop(key, default)` removes a key and returns its value, or the default if it isn't there.

```python
prices = {"tea": 2.5, "jam": 4.0}
prices.update({"jam": 4.5, "oat": 1.0})
print(prices)

groups = {}
for region, rep in [("EU", "Ana"), ("US", "Ben"), ("EU", "Cy")]:
    groups.setdefault(region, []).append(rep)
print(groups)

print(prices.pop("oat"), prices.pop("milk", 0), prices)
```

```text
{'tea': 2.5, 'jam': 4.5, 'oat': 1.0}
{'EU': ['Ana', 'Cy'], 'US': ['Ben']}
1.0 0 {'tea': 2.5, 'jam': 4.5}
```

**Nested data: lists of dicts.** Data from APIs and JSON files usually arrives as a list of dicts, with more dicts and lists inside. Read it by chaining lookups from the outside in: `orders[0]["customer"]["city"]` is the first order, then its customer, then the city.

```python
orders = [
    {"id": 1, "customer": {"name": "Ana", "city": "Oslo"},
     "items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]},
    {"id": 2, "customer": {"name": "Ben", "city": "Rome"},
     "items": [{"sku": "A", "qty": 5}]},
]

print(orders[0]["customer"]["city"])
print([o["id"] for o in orders if o["customer"]["city"] == "Rome"])
print(sum(item["qty"] for o in orders for item in o["items"] if item["sku"] == "A"))
```

```text
Oslo
[2]
7
```

The last line has two `for` parts, read in the same order as nested loops: for each order, for each item in that order. It adds up the quantity of SKU A across all orders: 2 + 5. To turn data like this into a table, use `pd.json_normalize` (section 1.4.1).

### Exam traps

> **Trap.** `{}` is an empty **dict**, not an empty set.

> **Trap.** `lst.sort()` returns `None`. `x = lst.sort()` leaves `x` as `None`.

> **Trap.** `nums[5]` on a 3-item list raises `IndexError`, but `nums[5:]` just returns `[]`. Slices never go out of range.

> **Trap.** `s[1:4]` stops **before** position 4, so it has 3 items, not 4.

> **Trap.** `"abc".find("z")` returns `-1`; `"abc".index("z")` raises `ValueError`. And `-1` used as an index means the last item, so an unchecked `find` result can quietly pick the wrong character.

> **Trap.** `round(2.5)` is `2`, not `3`: Python rounds exact halves to the even number.

> **Trap.** In `first, *rest = [10]`, `rest` is an empty list `[]`, not an error; without the `*`, the counts must match exactly.

> **Trap.** `d.setdefault(k, [])` returns the list stored under `k`, inserting it only if `k` was missing; `d.get(k, [])` returns a default without storing anything, so appending to it is lost.

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

**What importing does.** A **module** is a file of Python code that someone has already written, such as `math` for maths functions. `import` loads it so you can use what's inside. There are four ways to write an import, and they differ in what name you use afterwards.

**1. Import the whole module.** You then write the module name, a dot, and the function.

```python
import math

print(math.sqrt(16))     # square root, always a float
print(math.floor(2.7))   # round down to a whole number (an int)
print(math.ceil(2.1))    # round up
print(math.pi)
```

```text
4.0
2
3
3.141592653589793
```

**2. Import with an alias.** `as` gives the module a shorter name. The community uses standard aliases: `np` for NumPy, `pd` for pandas, `plt` for Matplotlib's pyplot and `sns` for Seaborn.

```python
import statistics as st

print(st.mean([2, 4, 9]))
```

```text
5
```

**3. Import only certain names.** `from module import name` brings in just those names, and you use them directly, without the module name in front.

```python
from statistics import mean, median

print(mean([2, 4, 9]), median([2, 4, 9]))
```

```text
5 4
```

With this style, the module name itself is **not** defined, only the names you imported:

```python
from math import sqrt

print(sqrt(25))
try:
    math.sqrt(25)
except NameError as e:
    print("NameError:", e)
```

```text
5.0
NameError: name 'math' is not defined
```

**4. Import a name with an alias.** The two ideas combine: `from datetime import datetime as dt` imports `datetime` and calls it `dt`.

**Avoid `import *`.** `from module import *` pulls in every public name at once. You can no longer tell where a name came from, and it can silently replace names of your own. PEP 8 advises against it.

**Where modules come from.**

- **Standard library**: modules that come with Python, so nothing needs installing. Examples: `math`, `statistics`, `random`, `datetime`, `csv`, `json`, `sqlite3`, `re`, `os`, `pathlib`, `collections`.
- **Third-party packages**: written by others and installed with pip from PyPI, such as `numpy`, `pandas` and `requests`. Importing one that isn't installed raises `ModuleNotFoundError`.
- **Your own modules**: any `.py` file you write. If `cleaning.py` sits next to your script, `import cleaning` loads it. A folder of modules is a **package**: `from utils.cleaning import fix_dates`.

```python
try:
    import not_a_real_package
except ModuleNotFoundError as e:
    print("ModuleNotFoundError:", e)
```

```text
ModuleNotFoundError: No module named 'not_a_real_package'
```

**A module runs once.** The first time a module is imported, Python runs all its top-level code. Importing it again reuses the loaded copy without running it again.

**`if __name__ == "__main__":`.** Every module has a variable `__name__`. When you run a file directly, its `__name__` is `"__main__"`; when it is imported by another file, `__name__` is the module's own name. So code inside `if __name__ == "__main__":` runs when you run the file, but not when another file imports it. It's the usual place for code that tests or demonstrates the module.

```python
def clean(text):
    return text.strip().lower()

if __name__ == "__main__":          # true here, because this code is run directly
    print(clean("  Hello "))
```

```text
hello
```

**Dates and times: `datetime`.** A `date` holds a day, a `datetime` holds a day and a time, and a `timedelta` holds a length of time. `strptime` ("string parse time") reads text into a `datetime` using format codes; `strftime` ("string format time") writes a `datetime` out as text.

| Code | Meaning | Example |
|---|---|---|
| `%Y` | Four-digit year | `2025` |
| `%m` / `%d` | Month / day, two digits | `07` / `15` |
| `%H`, `%M`, `%S` | Hour (24-hour clock), minute, second | `14`, `30`, `00` |
| `%b` / `%B` | Month name, short / full | `Jul` / `July` |
| `%a` / `%A` | Weekday name, short / full | `Tue` / `Tuesday` |

```python
from datetime import datetime, timedelta

placed = datetime.strptime("15/07/2025 14:30", "%d/%m/%Y %H:%M")
print(placed)
print(placed.strftime("%Y-%m-%d"), placed.strftime("%A %d %B"))

due = placed + timedelta(days=30)
print(due.date(), (due - placed).days, due > placed)
print(placed.year, placed.month, placed.weekday())    # weekday(): Monday is 0
```

```text
2025-07-15 14:30:00
2025-07-15 Tuesday 15 July
2025-08-14 30 True
2025 7 1
```

Adding a `timedelta` moves a date; subtracting two dates gives a `timedelta`, whose `.days` is the gap. If the text doesn't match the format exactly, `strptime` raises a `ValueError`:

```python
from datetime import datetime

try:
    datetime.strptime("2025-07-15", "%d/%m/%Y")
except ValueError as e:
    print("ValueError:", e)
```

```text
ValueError: time data '2025-07-15' does not match format '%d/%m/%Y'
```

For ISO text such as `'2025-07-15'`, `date.fromisoformat` needs no format string (section 2.4.5). pandas uses the same format codes: `pd.to_datetime(s, format="%d/%m/%Y")` and `s.dt.strftime("%Y-%m")`.

**Reading and writing files.** `open(path, mode)` opens a file. The mode decides what happens:

| Mode | Does |
|---|---|
| `"r"` (the default) | Read; `FileNotFoundError` if the file doesn't exist |
| `"w"` | Write; creates the file, or **empties** an existing one first |
| `"a"` | Append; adds to the end, creating the file if needed |

`with open(...) as f:` closes the file automatically at the end of the block, even after an error. Give `encoding="utf-8"` for text that might hold non-English characters. `os.path.join` builds a path with the right separator for the operating system, and `os.path.exists` checks that a file is there.

```python
import os
import tempfile

path = os.path.join(tempfile.gettempdir(), "visits.txt")   # folder + file name

with open(path, "w", encoding="utf-8") as f:     # "w": create, or empty and rewrite
    f.write("Oslo,12\n")
    f.write("Rome,7\n")

with open(path, "a", encoding="utf-8") as f:     # "a": add to the end
    f.write("Lima,3\n")

with open(path, encoding="utf-8") as f:          # "r" (read) is the default
    for line in f:
        city, visits = line.strip().split(",")
        print(city, int(visits) * 2)

print(os.path.exists(path), os.path.basename(path))
```

```text
Oslo 24
Rome 14
Lima 6
True visits.txt
```

Looping over a file gives one line at a time, each still ending in `"\n"`, which is why `strip()` comes first. Every value read from a text file is a string, so `int()` converts the counts. `write` doesn't add a newline for you.

`f.read()` returns the whole file as one string, and `f.readlines()` returns a list of lines. Opening with `"w"` a second time wipes what was there:

```python
import os
import tempfile

path = os.path.join(tempfile.gettempdir(), "note.txt")
with open(path, "w", encoding="utf-8") as f:
    f.write("first\nsecond\n")
with open(path, "w", encoding="utf-8") as f:      # "w" again: the old text is gone
    f.write("third\n")

with open(path, encoding="utf-8") as f:
    print(repr(f.read()))                         # the whole file as one string
with open(path, encoding="utf-8") as f:
    print(f.readlines())                          # a list of lines
```

```text
'third\n'
['third\n']
```

**CSV files with the `csv` module.** `csv.writer` writes rows and quotes fields that need it; `csv.DictReader` reads each row as a dict keyed by the header. Every value comes back as a string. Open CSV files with `newline=""` so the module controls the line endings.

```python
import csv
import os
import tempfile

path = os.path.join(tempfile.gettempdir(), "sales.csv")
with open(path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["region", "amount"])
    writer.writerows([["EU", 120], ["US", 80]])

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(rows[0])
print(sum(int(r["amount"]) for r in rows))
```

```text
{'region': 'EU', 'amount': '120'}
200
```

The number 120 went in as an integer and came back as the string `'120'`, so it needs `int()` before adding up.

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

> **Trap.** `open(path, "w")` empties an existing file as soon as it opens. Use `"a"` to add to the end.

> **Trap.** `strptime` turns text into a `datetime` (parse); `strftime` turns a `datetime` into text (format). The format must match the text exactly, or `strptime` raises `ValueError`.

> **Trap.** After `from math import sqrt`, the name `math` is not defined; only `sqrt` is.

> **Trap.** Python looks in the script's own folder before the standard library. A file of your own called `statistics.py` or `csv.py` hides the real module, so `import statistics` loads your file and `statistics.mean` raises `AttributeError`.

## 2.2.2 Apply basic exception handling

**Syllabus asks:** implement exception handling, predict and mitigate common errors, and read error messages to diagnose problems.

### Core facts

**What an exception is.** When something goes wrong while code runs, such as dividing by zero or turning `"abc"` into a number, Python **raises an exception**: it stops and prints an error. Exception handling lets your code catch that error and decide what to do instead of crashing.

**`try` and `except`.** Put the code that might fail inside `try:`. If it raises an error, Python jumps straight to the matching `except` block. If nothing goes wrong, the `except` block is skipped.

```python
for text in ["42", "abc"]:
    try:
        number = int(text)
        print("converted:", number)
    except ValueError:
        print("not a number:", text)
```

```text
converted: 42
not a number: abc
```

For `"abc"`, `int()` raised a `ValueError`, so the `print("converted:", ...)` line never ran. Python jumped to `except`.

**`else`: runs only when nothing went wrong.** An `else` block after the `except` blocks runs only if the `try` block finished **without** an error. It keeps the "it worked" code apart from the code being protected.

```python
for text in ["42", "abc"]:
    try:
        number = int(text)
    except ValueError:
        print(text, "-> failed")
    else:
        print(text, "-> worked, doubled:", number * 2)
```

```text
42 -> worked, doubled: 84
abc -> failed
```

**`finally`: always runs.** A `finally` block runs at the end **whatever happened**: success, a caught error, or even a `return`. It is for clean-up that must always happen, such as closing a file or a database connection.

```python
for text in ["42", "abc"]:
    try:
        int(text)
        print(text, "-> converted")
    except ValueError:
        print(text, "-> failed")
    finally:
        print("   finished with", text)
```

```text
42 -> converted
   finished with 42
abc -> failed
   finished with abc
```

**All four together.** This function divides two numbers. Follow the printed words to see which blocks ran for each call:

```python
def safe_ratio(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("except")
        return None
    else:
        print("else")          # only if no error
        return result
    finally:
        print("finally")       # always, even after a return

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

`safe_ratio(6, 3)` worked, so `else` ran, then `finally`, and then the result 2.0 was printed. `safe_ratio(1, 0)` divided by zero, so `except` ran, then `finally`, and the function returned `None`. Notice that `finally` ran **before** each result was printed, even though `return` had already been reached.

**The first matching `except` wins.** Python checks the `except` clauses from top to bottom and runs only the first one that matches. `Exception` matches almost every error, so if it comes first, the more specific clauses below it never get a chance.

```python
try:
    int("12a")
except Exception:
    print("caught by the general clause")
except ValueError:
    print("never reached")
```

```text
caught by the general clause
```

Put the specific error first:

```python
try:
    int("12a")
except ValueError:
    print("caught by the ValueError clause")
except Exception:
    print("only for other errors")
```

```text
caught by the ValueError clause
```

**Catching several errors at once.** Put them in a tuple. `as e` stores the error so you can read its message.

```python
for text in ["12a", None]:
    try:
        int(text)
    except (ValueError, TypeError) as e:
        print(type(e).__name__, "-", e)
```

```text
ValueError - invalid literal for int() with base 10: '12a'
TypeError - int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
```

`int("12a")` is a `ValueError` (right type, bad value); `int(None)` is a `TypeError` (wrong type altogether). One clause handles both.

**Don't catch everything.** A bare `except:`, or `except Exception:` wrapped around everything, also swallows bugs you didn't expect, such as a typo in a variable name. Catch only the errors you know how to handle.

**Raising your own errors.** `raise` stops the function and sends an error to the caller. Use it when the input is wrong in a way the code can't fix.

```python
def set_price(value):
    if value < 0:
        raise ValueError("price cannot be negative")
    return value

print(set_price(5))

try:
    set_price(-1)
except ValueError as e:
    print("ValueError:", e)
```

```text
5
ValueError: price cannot be negative
```

**Re-raising.** Inside an `except` block, `raise` on its own sends the **same** error on to the caller. It is useful when you want to note something (a log message) but still let the error through.

```python
def parse(text):
    try:
        return float(text)
    except ValueError:
        print("could not parse", repr(text))
        raise                    # pass the same ValueError on

try:
    parse("abc")
except ValueError as e:
    print("caller got:", e)
```

```text
could not parse 'abc'
caller got: could not convert string to float: 'abc'
```

**Custom exceptions.** Make your own error type by creating a class that inherits from `Exception`. A clear name tells the caller exactly what went wrong, and they can catch it separately from Python's built-in errors.

```python
class DataQualityError(Exception):
    pass

def check_age(age):
    if age > 120:
        raise DataQualityError(f"age {age} is not plausible")
    return age

try:
    check_age(150)
except DataQualityError as e:
    print("DataQualityError:", e)
```

```text
DataQualityError: age 150 is not plausible
```

**`assert`: checking your own assumptions.** `assert condition, message` does nothing when the condition is true and raises `AssertionError` with the message when it is false. It is a quick guard for things that should never happen if the code is right.

```python
def mean(values):
    assert len(values) > 0, "values must not be empty"
    return sum(values) / len(values)

print(mean([2, 4]))
try:
    mean([])
except AssertionError as e:
    print("AssertionError:", e)
```

```text
3.0
AssertionError: values must not be empty
```

Python skips every `assert` when it runs with the `-O` (optimize) option, so don't use `assert` to check user input or incoming data. Raise a `ValueError` for that instead, so the check always runs.

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

> **Trap.** `assert` statements are skipped when Python runs with `-O`, so they can't be relied on to validate data. Raise an exception for checks that must always run.

## 2.3.1 Apply basic OOP to structure and model data

**Syllabus asks:** define and instantiate classes for structured data records; constructors and instance variables; encapsulation with `_protected` and `__private` names; getters and setters.

### Core facts

**Classes, objects and `__init__`.** A **class** is a blueprint; an **object** (or *instance*) is one thing built from it. Calling the class, `Customer("Ana")`, builds a new object and runs its `__init__` method (the **constructor**) to set it up. Inside the class, `self` means "the object being worked on".

```python
class Customer:
    def __init__(self, name):
        self.name = name          # store the name on this object

ana = Customer("Ana")
ben = Customer("Ben")
print(ana.name, ben.name)
```

```text
Ana Ben
```

`ana` and `ben` are two separate objects from the same blueprint, each with its own `name`.

**Instance variables and class variables.** A variable set on `self` (an **instance variable**) belongs to one object. A variable written directly inside the class (a **class variable**) is shared by every object.

```python
class Customer:
    currency = "EUR"              # class variable: shared

    def __init__(self, name):
        self.name = name          # instance variable: one per object

ana = Customer("Ana")
ben = Customer("Ben")
print(ana.name, ana.currency)
print(ben.name, ben.currency)
print(Customer.currency)          # also readable from the class itself
```

```text
Ana EUR
Ben EUR
EUR
```

**"Keep out" names: one underscore.** Python has no truly private attributes, only conventions. A name starting with one underscore (`self._segment`) means "internal: please don't use this from outside the class". It is only a hint to other programmers; Python doesn't stop you.

```python
class Customer:
    def __init__(self):
        self._segment = "retail"

c = Customer()
print(c._segment)        # works fine: the underscore is only a hint
```

```text
retail
```

**Two underscores: name mangling.** A name starting with **two** underscores (`self.__balance`) gets renamed by Python behind the scenes. Python adds an underscore and the class name to the front, so `__balance` is actually stored as `_Customer__balance`. This is called **name mangling**.

`hasattr(obj, "name")` asks "does this object have an attribute with exactly this name?" and answers `True` or `False`. It shows the renaming clearly:

```python
class Customer:
    def __init__(self, balance):
        self.__balance = balance        # stored as _Customer__balance

c = Customer(100)
print(hasattr(c, "__balance"))            # False: no attribute with that exact name
print(hasattr(c, "_Customer__balance"))   # True: this is the real name
```

```text
False
True
```

So asking for `c.__balance` from outside the class fails:

```python
class Customer:
    def __init__(self, balance):
        self.__balance = balance

c = Customer(100)
try:
    print(c.__balance)
except AttributeError as e:
    print("AttributeError:", e)
```

```text
AttributeError: 'Customer' object has no attribute '__balance'
```

**Inside the class, the short name still works.** Python renames `__balance` inside the class's own code too, so the class's methods can keep writing `self.__balance` and it all lines up:

```python
class Customer:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance           # also renamed, so this finds it

c = Customer(100)
print(c.get_balance())
```

```text
100
```

**It isn't real security.** Anyone who knows the renamed version can still reach the value. Name mangling prevents **accidents**, such as a subclass using the same attribute name by mistake. It doesn't stop someone who is determined.

```python
class Customer:
    def __init__(self, balance):
        self.__balance = balance

c = Customer(100)
print(c._Customer__balance)     # the "private" value, read from outside
```

```text
100
```

**Getters and setters.** Instead of letting outside code change an attribute directly, a class can provide methods that read it (a **getter**) and change it (a **setter**). The setter can check the new value first.

```python
class Customer:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self.__balance = value

c = Customer(100)
c.set_balance(150)
print(c.get_balance())

try:
    c.set_balance(-5)
except ValueError as e:
    print("ValueError:", e)
```

```text
150
ValueError: balance cannot be negative
```

**The Pythonic version: `@property`.** A property gives you the same checks while letting outside code use plain attribute syntax (`p.price = 5`). `@property` marks the getter; `@price.setter` marks the setter. The real value is kept in `_price`.

```python
class Product:
    def __init__(self, price):
        self.price = price            # this line already goes through the setter

    @property
    def price(self):                  # runs when you read p.price
        return self._price

    @price.setter
    def price(self, value):           # runs when you write p.price = ...
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value

p = Product(4)
p.price = 5                           # looks like a plain assignment, but runs the setter
print(p.price)

try:
    p.price = -1
except ValueError as e:
    print("ValueError:", e)
```

```text
5
ValueError: price cannot be negative
```

**How an object prints: `__repr__` and `__str__`.** `__str__` returns a friendly description and is what `print()` uses. `__repr__` returns an exact, developer-facing one, used by `repr()` and when an object is shown inside a list.

```python
class Product:
    def __init__(self, price):
        self.price = price

    def __repr__(self):
        return f"Product(price={self.price})"

    def __str__(self):
        return f"{self.price:.2f} EUR"

p = Product(5)
print(p)              # uses __str__
print(repr(p))        # uses __repr__
print([p])            # objects inside a list use __repr__
```

```text
5.00 EUR
Product(price=5)
[Product(price=5)]
```

**`@dataclass` writes the boilerplate.** For a class that mainly holds data, `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the fields you list.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p)                       # a readable __repr__ for free
print(p == Point(1, 2))        # __eq__ compares the fields
```

```text
Point(x=1, y=2)
True
```

**Putting it together.** Here is one class that uses everything above. Each comment points back to the step that explains it.

```python
class Customer:
    currency = "EUR"                       # class variable: shared by every customer

    def __init__(self, name, balance=0.0): # the constructor
        self.name = name                   # instance variable: one per customer
        self._segment = "retail"           # one underscore: "internal", only a hint
        self.__balance = balance           # two underscores: stored as _Customer__balance

    def get_balance(self):                 # getter
        return self.__balance

    def set_balance(self, value):          # setter, which checks the value first
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

The first line shows the name, the balance (changed by the setter), the "internal" segment and the shared currency. The second shows name mangling: there is no attribute called `__balance`, but the value is still there under `_Customer__balance`.

### Exam traps

> **Trap.** Double-underscore names are mangled, not hidden: `obj._ClassName__attr` still reaches them.

> **Trap.** Assigning `self.total = 0` inside a method creates an instance attribute that shadows a class attribute of the same name for that one object only.

## 2.3.2 Apply OOP patterns for code reuse

**Syllabus asks:** composition to group related data models, inheritance with method overriding, and polymorphism (for example `.process()` or `.export()` across subclasses).

### Core facts

**Inheritance ("is-a").** Writing `class Child(Parent)` makes `Child` a specialised kind of `Parent`. It gets every method the parent has without you writing them again.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is an animal"

class Dog(Animal):          # Dog inherits from Animal
    pass                    # nothing new yet

d = Dog("Rex")
print(d.describe())         # describe() came from Animal
```

```text
Rex is an animal
```

**Overriding.** If the child defines a method with the same name as one in the parent, the child's version replaces it for child objects.

```python
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):        # overrides Animal.sound
        return "Woof"

print(Animal().sound(), Dog().sound())
```

```text
... Woof
```

**`super()`: reuse the parent's version.** Often the child wants to add to the parent's method rather than replace it completely. `super().method()` runs the parent's version. It is most common in `__init__`, so the parent can set up its attributes before the child adds its own.

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)      # let Animal set self.name
        self.breed = breed          # then add what's new

d = Dog("Rex", "collie")
print(d.name, d.breed)
```

```text
Rex collie
```

If a child's `__init__` forgets `super().__init__(...)`, the parent's setup never runs and its attributes don't exist:

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Cat(Animal):
    def __init__(self, name, indoor):
        self.indoor = indoor        # forgot super().__init__(name)

c = Cat("Tom", True)
try:
    print(c.name)
except AttributeError as e:
    print("AttributeError:", e)
```

```text
AttributeError: 'Cat' object has no attribute 'name'
```

**Polymorphism: one call, different behaviour.** Code can call the same method on different objects without checking what type each one is. Each object runs its own version. The example at the end of this section does the same with data exporters; here it is in its simplest form:

```python
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "Woof"

class Cat(Animal):
    def sound(self):
        return "Meow"

for pet in [Dog(), Cat(), Dog()]:
    print(pet.sound())              # the same line works for every kind of animal
```

```text
Woof
Meow
Woof
```

Python also allows **duck typing**: any object with a `sound()` method would work in that loop, even if it isn't an `Animal` at all.

**Composition ("has-a").** Instead of inheriting, a class can hold other objects as attributes. An order *has* a customer and *has* line items; it is not a kind of customer, so inheritance would be wrong.

```python
class LineItem:
    def __init__(self, product, qty, price):
        self.product = product
        self.qty = qty
        self.price = price

class Order:
    def __init__(self, customer, items):
        self.customer = customer    # an Order has a customer...
        self.items = items          # ...and has a list of LineItems

    def total(self):
        return sum(item.qty * item.price for item in self.items)

order = Order("Ana", [LineItem("tea", 2, 3.0), LineItem("jam", 1, 4.5)])
print(order.customer, order.total())
```

```text
Ana 10.5
```

A quick test: if "X is a Y" sounds right, use inheritance. If "X has a Y" sounds right, use composition.

**Checking types: `isinstance` and `issubclass`.** `isinstance(obj, Class)` asks "is this object one of these?", and it counts children too: a dog **is** an animal. `issubclass(Child, Parent)` asks the same question about two classes.

```python
class Animal:
    pass

class Dog(Animal):
    pass

d = Dog()
print(isinstance(d, Dog), isinstance(d, Animal), isinstance(d, str))
print(issubclass(Dog, Animal), issubclass(Animal, Dog))
```

```text
True True False
True False
```

**Putting it together.** A realistic use of all of this: one parent class, `Exporter`, and two subclasses that turn the same rows into different text formats.

- `Exporter.export()` only raises `NotImplementedError`: the parent says "every exporter has an `export` method" but leaves the details to each subclass.
- `describe()` is written **once**, in the parent. It calls `self.export()`, so it automatically uses whichever subclass's version belongs to the object.
- `CsvExporter` **overrides** `export()` to produce comma-separated text.
- `JsonExporter` adds its own `indent` setting, so its `__init__` calls `super().__init__(rows)` first to let the parent store the rows.

```python
import json

class Exporter:
    def __init__(self, rows):
        self.rows = rows

    def export(self):
        raise NotImplementedError          # each subclass must supply its own

    def describe(self):
        return f"{type(self).__name__}: {self.export()}"

class CsvExporter(Exporter):
    def export(self):                      # overrides the parent method
        lines = []
        for row in self.rows:
            lines.append(",".join(str(value) for value in row))
        return "\n".join(lines)

class JsonExporter(Exporter):
    def __init__(self, rows, indent=None):
        super().__init__(rows)             # let Exporter store the rows
        self.indent = indent

    def export(self):
        return json.dumps(self.rows, indent=self.indent)

for exporter in [CsvExporter([[1, 2]]), JsonExporter([[1, 2]])]:
    print(exporter.describe())             # same call, different behaviour
```

```text
CsvExporter: 1,2
JsonExporter: [[1, 2]]
```

`type(self).__name__` is the name of the object's class, which is how `describe()` prints `CsvExporter` or `JsonExporter`. The loop calls the same method on both objects and gets a different format from each: that is polymorphism.

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

**`==` versus `is`.** `==` asks "do these hold the **same value**?" `is` asks "are these the **same object**?" Two separate lists can be equal without being the same list.

```python
a = [1, 2]
b = [1, 2]        # a separate list with the same values
c = a             # another name for the list a

print(a == b, a is b)    # equal values, different objects
print(a == c, a is c)    # same object, so also equal
```

```text
True False
True True
```

Use `is` to check for `None` (`if x is None:`), not to compare values. PEP 8 also advises against `x is True` and `x == True`: write `if x:`. For numbers and strings always use `==`: Python sometimes reuses the same object for small numbers and short strings, so `is` can seem to work in one case and fail in another.

**Copying a list.** Since `b = a` only adds a second name, you need an explicit copy to get an independent list. `a.copy()`, `list(a)` and `a[:]` all make one.

```python
a = [1, 2, 3]
same = a           # same list, two names
copy = a.copy()    # a new list

a.append(4)
print(same)        # sees the change
print(copy)        # doesn't
```

```text
[1, 2, 3, 4]
[1, 2, 3]
```

**Shallow and deep copies.** Those copies are **shallow**: they copy the outer list, but any lists *inside* it are still shared. `copy.deepcopy` copies everything, all the way down.

```python
import copy

a = [[1, 2], [3]]
shallow = a.copy()
deep = copy.deepcopy(a)

a[0].append(99)        # change a list inside a
print(shallow)         # the inner list is shared, so the change shows
print(deep)            # fully separate, so it doesn't
```

```text
[[1, 2, 99], [3]]
[[1, 2], [3]]
```

The same applies in pandas: `df2 = df` is just a second name, and `df.copy()` makes an independent DataFrame.

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

**Aggregates: WHERE fails, HAVING works.** WHERE runs before GROUP BY, so there are no groups to sum yet:

```sql
-- Fails: aggregate functions are not allowed in WHERE
SELECT   customer_id, SUM(total) AS spent
FROM     orders
WHERE    SUM(total) > 100
GROUP BY customer_id;

-- Works: HAVING runs after GROUP BY, once each group's SUM exists
SELECT   customer_id, SUM(total) AS spent
FROM     orders
GROUP BY customer_id
HAVING   SUM(total) > 100;
```

**Aliases: WHERE fails, ORDER BY works.** The alias `gross` is created in SELECT, which runs after WHERE but before ORDER BY:

```sql
-- Fails in standard SQL: column "gross" does not exist
SELECT total * 1.2 AS gross
FROM   orders
WHERE  gross > 50;

-- Works: repeat the expression in WHERE
SELECT total * 1.2 AS gross
FROM   orders
WHERE  total * 1.2 > 50;

-- Works: ORDER BY runs after SELECT, so the alias exists by then
SELECT   total * 1.2 AS gross
FROM     orders
ORDER BY gross DESC;
```

SQLite (and MySQL) relax the alias rule and accept `WHERE gross > 50`; PostgreSQL, SQL Server and Oracle reject it. Rely on the standard rule.

**Both rules together.** Filter rows with WHERE, filter groups with HAVING, sort by the alias:

```sql
SELECT   customer_id, SUM(total) AS spent
FROM     orders
WHERE    total > 10          -- row filter: runs first, no aggregates
GROUP BY customer_id
HAVING   SUM(total) > 50     -- group filter: aggregates allowed
ORDER BY spent DESC;         -- alias allowed: SELECT has already run
```

**Joins.** A join combines rows from two tables wherever a condition matches, usually an ID in one table equal to an ID in the other. The join type decides what happens to rows that **don't** match:

| Join | Returns |
|---|---|
| `INNER JOIN` (or `JOIN`) | Only rows with a match in both tables |
| `LEFT JOIN` | Every row of the left table; NULLs where the right table has no match |
| `RIGHT JOIN` | Every row of the right table; NULLs where the left has no match |
| `FULL OUTER JOIN` | Every row of both tables, matched where possible |

<div class="dg jd">
<p class="dg-title">The same two tables, four joins</p>
<p class="jd-intro">Each join below uses <code>ON orders.customer_id = customers.id</code>. Ana appears twice in every result because Ana has two orders.</p>
<div class="jd-sources"><table class="jt"><caption>customers (left table)</caption><thead><tr><th>id</th><th>name</th></tr></thead><tbody><tr><td>1</td><td>Ana</td></tr><tr><td>2</td><td>Ben</td></tr><tr class="jd-l"><td>3</td><td>Cy</td></tr></tbody></table><table class="jt"><caption>orders (right table)</caption><thead><tr><th>customer_id</th><th>total</th></tr></thead><tbody><tr><td>1</td><td>50</td></tr><tr><td>1</td><td>70</td></tr><tr><td>2</td><td>20</td></tr><tr class="jd-r"><td>9</td><td>15</td></tr></tbody></table></div>
<p class="jd-legend"><span class="jd-key jd-key-l">Cy: a customer with no orders</span> <span class="jd-key jd-key-r">Order 9: an order with no customer</span></p>
<div class="jd-grid">
<div class="jd-card"><table class="jt"><thead><tr><th>id</th><th>name</th><th>customer_id</th><th>total</th></tr></thead><tbody><tr><td>1</td><td>Ana</td><td>1</td><td>50</td></tr><tr><td>1</td><td>Ana</td><td>1</td><td>70</td></tr><tr><td>2</td><td>Ben</td><td>2</td><td>20</td></tr></tbody></table><p class="jd-name">INNER JOIN</p><p class="jd-why">Only pairs where <code>customer_id</code> equals <code>id</code>. Cy has no orders and order 9's customer doesn't exist, so both disappear. <b>3 rows.</b></p></div>
<div class="jd-card"><table class="jt"><thead><tr><th>id</th><th>name</th><th>customer_id</th><th>total</th></tr></thead><tbody><tr><td>1</td><td>Ana</td><td>1</td><td>50</td></tr><tr><td>1</td><td>Ana</td><td>1</td><td>70</td></tr><tr><td>2</td><td>Ben</td><td>2</td><td>20</td></tr><tr class="jd-l"><td>3</td><td>Cy</td><td class="jd-null">NULL</td><td class="jd-null">NULL</td></tr></tbody></table><p class="jd-name">LEFT JOIN</p><p class="jd-why">Every row of the left table (customers) is kept. Cy matches no order, so Cy's order columns are NULL. Order 9 is still dropped: it is on the right and matches no one. <b>4 rows.</b></p></div>
<div class="jd-card"><table class="jt"><thead><tr><th>id</th><th>name</th><th>customer_id</th><th>total</th></tr></thead><tbody><tr><td>1</td><td>Ana</td><td>1</td><td>50</td></tr><tr><td>1</td><td>Ana</td><td>1</td><td>70</td></tr><tr><td>2</td><td>Ben</td><td>2</td><td>20</td></tr><tr class="jd-r"><td class="jd-null">NULL</td><td class="jd-null">NULL</td><td>9</td><td>15</td></tr></tbody></table><p class="jd-name">RIGHT JOIN</p><p class="jd-why">The mirror image: every row of the right table (orders) is kept. Order 9 matches no customer, so its customer columns are NULL. Cy is dropped. <b>4 rows.</b></p></div>
<div class="jd-card"><table class="jt"><thead><tr><th>id</th><th>name</th><th>customer_id</th><th>total</th></tr></thead><tbody><tr><td>1</td><td>Ana</td><td>1</td><td>50</td></tr><tr><td>1</td><td>Ana</td><td>1</td><td>70</td></tr><tr><td>2</td><td>Ben</td><td>2</td><td>20</td></tr><tr class="jd-l"><td>3</td><td>Cy</td><td class="jd-null">NULL</td><td class="jd-null">NULL</td></tr><tr class="jd-r"><td class="jd-null">NULL</td><td class="jd-null">NULL</td><td>9</td><td>15</td></tr></tbody></table><p class="jd-name">FULL OUTER JOIN</p><p class="jd-why">Everything from both sides: the three matches, plus Cy and order 9, each with NULLs on the side it's missing. <b>5 rows.</b></p></div>
</div>
</div>

The examples below run SQL from Python with the built-in `sqlite3` module (section 2.4.3 explains it). Each one creates a tiny table, runs one query, and prints the rows it returns; each row prints as a tuple, and `NULL` prints as `None`.

Three customers, and four orders. Cy has no orders, and the last order belongs to customer 9, who doesn't exist:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER, name TEXT);
CREATE TABLE orders (customer_id INTEGER, total REAL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cy');
INSERT INTO orders VALUES (1, 50), (1, 70), (2, 20), (9, 15);
""")

inner = con.execute("""
    SELECT c.name, o.total
    FROM customers c
    INNER JOIN orders o ON o.customer_id = c.id
""").fetchall()
print(inner)
```

```text
[('Ana', 50.0), ('Ana', 70.0), ('Ben', 20.0)]
```

Only matching pairs: Ana's two orders and Ben's one. Cy (no orders) and order 9 (no customer) both disappear. Now the same query as a `LEFT JOIN`:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER, name TEXT);
CREATE TABLE orders (customer_id INTEGER, total REAL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cy');
INSERT INTO orders VALUES (1, 50), (1, 70), (2, 20), (9, 15);
""")

left = con.execute("""
    SELECT c.name, o.total
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.id
""").fetchall()
print(left)
```

```text
[('Ana', 50.0), ('Ana', 70.0), ('Ben', 20.0), ('Cy', None)]
```

Every customer from the left table (`customers`) is kept. Cy has no order, so Cy's `total` is `NULL`. Order 9 is still missing, because it is on the right side and has no match.

**Counting and adding up: aggregates.** `COUNT`, `SUM`, `AVG`, `MIN` and `MAX` turn many rows into one value. `COUNT(*)` counts rows; `COUNT(column)` counts only the rows where that column isn't `NULL`. The others skip `NULL`s too.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales (rep TEXT, amount REAL);
INSERT INTO sales VALUES ('Ana', 100), ('Ben', NULL), ('Cy', 40);
""")

print(con.execute("SELECT COUNT(*), COUNT(amount), SUM(amount), AVG(amount) FROM sales").fetchall())
```

```text
[(3, 2, 140.0, 70.0)]
```

3 rows, but only 2 amounts. The average is (100 + 40) / 2 = 70: Ben's `NULL` is ignored, not counted as 0.

**`GROUP BY`: one result per group.** `GROUP BY region` splits the rows into one group per region, and the aggregate is worked out separately for each group.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales (region TEXT, amount REAL);
INSERT INTO sales VALUES ('EU', 100), ('EU', 40), ('US', 30), ('US', 20);
""")

print(con.execute("SELECT region, SUM(amount) FROM sales GROUP BY region").fetchall())
```

```text
[('EU', 140.0), ('US', 50.0)]
```

Every column in the `SELECT` that isn't inside an aggregate (here `region`) must also be in `GROUP BY`. SQLite lets you break this rule; most databases don't.

**`WHERE` versus `HAVING`.** Both filter, but at different moments. `WHERE` removes **rows before** they are grouped. `HAVING` removes **groups after** the totals are worked out, so it is the one that can use `SUM(...)` or `COUNT(...)`.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales (region TEXT, amount REAL);
INSERT INTO sales VALUES ('EU', 100), ('EU', 40), ('US', 30), ('US', 20);
""")

# WHERE: drop small sales first, then total what's left
print(con.execute("""
    SELECT region, SUM(amount) FROM sales
    WHERE amount > 25
    GROUP BY region
""").fetchall())

# HAVING: total everything, then drop small groups
print(con.execute("""
    SELECT region, SUM(amount) FROM sales
    GROUP BY region
    HAVING SUM(amount) > 100
""").fetchall())
```

```text
[('EU', 140.0), ('US', 30.0)]
[('EU', 140.0)]
```

In the first query the US sale of 20 is removed before grouping, so the US total is 30. In the second, all sales are totalled (EU 140, US 50), then the US group is dropped because 50 is not over 100.

**Filtering rows.** The everyday `WHERE` conditions, on one small table:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 1.2), ('Avocado', 2.5), ('Bread', 3.0),
                            ('Cake', 12.0), ('Milk', NULL);
""")

def names(sql):
    return [row[0] for row in con.execute(sql)]

print(names("SELECT name FROM products WHERE price BETWEEN 1.2 AND 3"))
print(names("SELECT name FROM products WHERE name LIKE 'A%'"))
print(names("SELECT name FROM products WHERE name IN ('Cake', 'Milk')"))
print(names("SELECT name FROM products WHERE price <> 3"))
```

```text
['Apple', 'Avocado', 'Bread']
['Apple', 'Avocado']
['Cake', 'Milk']
['Apple', 'Avocado', 'Cake']
```

- `BETWEEN 1.2 AND 3` includes both ends, so Apple (1.2) and Bread (3.0) are in.
- `LIKE 'A%'`: `%` stands for any run of characters, so this means "starts with A". `_` stands for exactly one character.
- `IN (...)` matches any value in the list.
- `<>` (or `!=`) means "not equal". Milk isn't in that result even though its price isn't 3, which leads to the next point.

**`NULL` needs `IS NULL`.** `NULL` means "unknown", and comparing anything with an unknown value gives "unknown", which `WHERE` treats as false. So `= NULL` never matches, and neither does `<>` on a `NULL` row. Use `IS NULL` and `IS NOT NULL`.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 1.2), ('Milk', NULL);
""")

print(con.execute("SELECT name FROM products WHERE price = NULL").fetchall())
print(con.execute("SELECT name FROM products WHERE price IS NULL").fetchall())
```

```text
[]
[('Milk',)]
```

**Sorting: `ORDER BY`.** `ORDER BY col` sorts the result from smallest to largest (or A to Z). That is the default, also written `ASC`:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 'fruit', 1.2), ('Avocado', 'fruit', 2.5),
                            ('Bread', 'bakery', 3.0), ('Cake', 'bakery', 12.0);
""")

print(con.execute("SELECT name FROM products ORDER BY price").fetchall())
```

```text
[('Apple',), ('Avocado',), ('Bread',), ('Cake',)]
```

Add `DESC` for largest first:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 'fruit', 1.2), ('Avocado', 'fruit', 2.5),
                            ('Bread', 'bakery', 3.0), ('Cake', 'bakery', 12.0);
""")

print(con.execute("SELECT name FROM products ORDER BY price DESC").fetchall())
```

```text
[('Cake',), ('Bread',), ('Avocado',), ('Apple',)]
```

**Paging: `LIMIT` and `OFFSET`.** `LIMIT n` keeps only the first n rows, and `OFFSET m` skips m rows before that:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 'fruit', 1.2), ('Avocado', 'fruit', 2.5),
                            ('Bread', 'bakery', 3.0), ('Cake', 'bakery', 12.0);
""")

print(con.execute("SELECT name FROM products ORDER BY price DESC LIMIT 2").fetchall())
print(con.execute("SELECT name FROM products ORDER BY price DESC LIMIT 2 OFFSET 1").fetchall())
```

```text
[('Cake',), ('Bread',)]
[('Bread',), ('Avocado',)]
```

`LIMIT 2` gives the two most expensive items. Adding `OFFSET 1` skips Cake first, then keeps the next two.

**Removing duplicates: `DISTINCT`.** A plain `SELECT` returns one row per row in the table, repeats included:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, category TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 'fruit', 1.2), ('Avocado', 'fruit', 2.5),
                            ('Bread', 'bakery', 3.0), ('Cake', 'bakery', 12.0);
""")

print(con.execute("SELECT category FROM products").fetchall())
print(con.execute("SELECT DISTINCT category FROM products").fetchall())
```

```text
[('fruit',), ('fruit',), ('bakery',), ('bakery',)]
[('fruit',), ('bakery',)]
```

`SELECT DISTINCT` keeps each different row once, so the four rows collapse to two categories.

**`CASE`: a column built from conditions.** `CASE WHEN condition THEN value ELSE other END` works like an if/else for each row.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, price REAL);
INSERT INTO products VALUES ('Apple', 1.2), ('Bread', 3.0), ('Cake', 12.0);
""")

print(con.execute("""
    SELECT name, CASE WHEN price > 10 THEN 'high' ELSE 'low' END
    FROM products
""").fetchall())
```

```text
[('Apple', 'low'), ('Bread', 'low'), ('Cake', 'high')]
```

**Functions on single values.** Besides aggregates, SQL has functions that work on one value in each row: `UPPER` and `LOWER` change the case, `LENGTH` counts characters, `ROUND(x, n)` rounds to n decimal places, and `COALESCE(a, b, …)` returns the first argument that isn't `NULL`, which turns a missing value into a default. `AS` names the result column.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products (name TEXT, price REAL, discount REAL);
INSERT INTO products VALUES ('apple', 1.234, 0.1), ('bread', 3.0, NULL);
""")

print(con.execute("""
    SELECT UPPER(name) AS item, LENGTH(name) AS letters,
           ROUND(price, 1) AS price, COALESCE(discount, 0) AS discount
    FROM products
""").fetchall())
```

```text
[('APPLE', 5, 1.2, 0.1), ('BREAD', 5, 3.0, 0)]
```

Bread's discount is `NULL`, so `COALESCE` returns 0 instead. The same function fixes totals after a `LEFT JOIN`: for a customer with no orders, `SUM(o.total)` is `NULL`, while `COALESCE(SUM(o.total), 0)` is 0.

**Subqueries and joining three tables.** A **subquery** is a `SELECT` inside another query, in brackets. In `WHERE ... IN (SELECT ...)` it supplies a list of values; compared with `>` or `=` it must return a single value, such as an average. To combine more than two tables, add one `JOIN ... ON` per extra table; each `ON` links the new table to one already in the query.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER, name TEXT);
CREATE TABLE orders (id INTEGER, customer_id INTEGER, total REAL);
CREATE TABLE items (order_id INTEGER, sku TEXT, qty INTEGER);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben'), (3, 'Cy');
INSERT INTO orders VALUES (10, 1, 50), (11, 1, 200), (12, 2, 80);
INSERT INTO items VALUES (10, 'tea', 2), (11, 'jam', 1), (11, 'tea', 5), (12, 'oat', 3);
""")

# customers with at least one order over 100
print(con.execute("""
    SELECT name FROM customers
    WHERE id IN (SELECT customer_id FROM orders WHERE total > 100)
""").fetchall())

# orders above the average order total
print(con.execute("""
    SELECT id, total FROM orders
    WHERE total > (SELECT AVG(total) FROM orders)
""").fetchall())

# tea units bought by each customer: customers -> orders -> items
print(con.execute("""
    SELECT c.name, SUM(i.qty) AS tea_units
    FROM customers AS c
    JOIN orders AS o ON o.customer_id = c.id
    JOIN items AS i ON i.order_id = o.id
    WHERE i.sku = 'tea'
    GROUP BY c.name
""").fetchall())
```

```text
[('Ana',)]
[(11, 200.0)]
[('Ana', 7)]
```

The average order total is (50 + 200 + 80) / 3 = 110, so only order 11 is above it. In the three-table join, each item row is linked to its order and each order to its customer: Ana's tea items are 2 (order 10) and 5 (order 11). `NOT IN (SELECT ...)` gives the opposite list, for example customers who never placed an order.

### Exam traps

> **Trap.** `WHERE COUNT(*) > 5` is an error; conditions on aggregates go in `HAVING`.

> **Trap.** `WHERE col = NULL` matches nothing, because any comparison with NULL is unknown. Use `IS NULL`.

> **Trap.** A LEFT JOIN followed by `WHERE right_table.col = 'x'` removes the unmatched (NULL) rows, turning it into an inner join. Put that condition in the `ON` clause to keep them.

> **Trap.** A subquery compared with `=` or `>` must return one value. Use `IN (SELECT ...)` when it returns a list.

## 2.4.2 Execute fundamental SQL commands

**Syllabus asks:** CRUD operations (Create, Read, Update, Delete): inserting, retrieving, updating and deleting data.

### Core facts

| CRUD | SQL | Example |
|---|---|---|
| Create | `INSERT` | `INSERT INTO products (name, price) VALUES ('Tea', 2.5);` |
| Read | `SELECT` | `SELECT name, price FROM products WHERE price < 3;` |
| Update | `UPDATE` | `UPDATE products SET price = 2.75 WHERE name = 'Tea';` |
| Delete | `DELETE` | `DELETE FROM products WHERE price IS NULL;` |

Here are the four operations one at a time, on a small `products` table. The examples run the SQL from Python with `sqlite3` (see 2.4.3), and `fetchall()` returns the rows as a list of tuples.

**Create: `INSERT`.** Adds new rows. You can add several in one statement by separating them with commas.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products (name, price) VALUES ('Tea', 2.5), ('Jam', 4.0)")
print(con.execute("SELECT * FROM products").fetchall())
```

```text
[('Tea', 2.5), ('Jam', 4.0)]
```

**Read: `SELECT`.** Returns rows, optionally filtered with `WHERE`. It never changes the data.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products VALUES ('Tea', 2.5), ('Jam', 4.0)")
print(con.execute("SELECT name FROM products WHERE price < 3").fetchall())
```

```text
[('Tea',)]
```

**Update: `UPDATE ... SET ... WHERE`.** Changes values in the rows that match the `WHERE`.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products VALUES ('Tea', 2.5), ('Jam', 4.0)")

con.execute("UPDATE products SET price = 2.75 WHERE name = 'Tea'")
print(con.execute("SELECT * FROM products").fetchall())
```

```text
[('Tea', 2.75), ('Jam', 4.0)]
```

**Forgetting `WHERE` changes every row.** With no `WHERE`, `UPDATE` and `DELETE` apply to the whole table. A safe habit: run a `SELECT` with the same `WHERE` first to see which rows will be affected.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products VALUES ('Tea', 2.5), ('Jam', 4.0)")

con.execute("UPDATE products SET price = 0")      # no WHERE
print(con.execute("SELECT * FROM products").fetchall())
```

```text
[('Tea', 0.0), ('Jam', 0.0)]
```

**Delete: `DELETE FROM ... WHERE`.** Removes the matching rows. `DELETE FROM products` with no `WHERE` removes every row but keeps the (now empty) table.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products VALUES ('Tea', 2.5), ('Jam', 4.0)")

con.execute("DELETE FROM products WHERE name = 'Jam'")
print(con.execute("SELECT * FROM products").fetchall())

con.execute("DELETE FROM products")               # every row
print(con.execute("SELECT * FROM products").fetchall())
```

```text
[('Tea', 2.5)]
[]
```

**`DELETE` versus `DROP`.** `DELETE` removes rows; the table is still there. `DROP TABLE` removes the table itself, structure and all, so any later query on it fails.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("DROP TABLE products")

try:
    con.execute("SELECT * FROM products")
except sqlite3.OperationalError as e:
    print("OperationalError:", e)
```

```text
OperationalError: no such table: products
```

`CREATE TABLE`, `ALTER TABLE` and `DROP TABLE` change the table's structure (they are called DDL, data definition language). The "Create" in CRUD means adding **rows** with `INSERT`, not creating tables.

**Saving changes: `commit()`.** In Python's `sqlite3`, `INSERT`, `UPDATE` and `DELETE` are held in a pending **transaction** until you call `con.commit()`. Until then, `con.rollback()` undoes them, and closing the connection without committing throws them away.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE products (name TEXT, price REAL)")
con.execute("INSERT INTO products VALUES ('Tea', 2.5)")
con.commit()                                      # the insert is now saved

con.execute("UPDATE products SET price = 0")      # oops: no WHERE
con.rollback()                                    # undo everything since the last commit
print(con.execute("SELECT * FROM products").fetchall())
```

```text
[('Tea', 2.5)]
```

To insert many rows from Python, use `executemany` with placeholders (section 2.4.4).

### Exam traps

> **Trap.** `DELETE` removes rows; `DROP` removes the table. "Remove all rows but keep the table" is `DELETE FROM t;`.

## 2.4.3 Establish database connections using Python

**Syllabus asks:** connect with `sqlite3` and `pymysql`, and resolve common connection issues.

### Core facts

Here is a complete round trip with Python's built-in `sqlite3` module: connect to a database, create a table, insert three rows, run a query, and close the connection. The steps after it go through each part.

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

**1. Connect.** `sqlite3.connect()` opens a database file and returns a **connection**. `":memory:"` makes a temporary database that exists only while the program runs, which is handy for examples. A real file path creates the file if it doesn't exist yet.

**2. Run SQL with `execute`.** `execute` runs one SQL statement. Calling it on the connection is a shortcut that creates a **cursor** for you; a cursor is the object that runs queries and holds their results.

**3. Fetch the results.** After a `SELECT`, the cursor holds the result rows. Each row comes back as a tuple.

- `fetchone()` gives the next row, or `None` when there are no rows left.
- `fetchall()` gives all remaining rows as a list.
- `fetchmany(n)` gives up to n rows.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales (region TEXT, amount REAL)")
con.execute("INSERT INTO sales VALUES ('EU', 120.0), ('US', 80.0)")

cur = con.execute("SELECT region, amount FROM sales ORDER BY region")
print(cur.fetchone())      # first row
print(cur.fetchone())      # second row
print(cur.fetchone())      # nothing left
```

```text
('EU', 120.0)
('US', 80.0)
None
```

**4. Commit, then close.** `con.commit()` saves inserts, updates and deletes (see 2.4.2); `con.close()` closes the connection when you're done.

**`with` commits, but doesn't close.** `with sqlite3.connect(path) as con:` commits automatically if the block succeeds, and rolls back if it raises an error. It does **not** close the connection, so you still call `con.close()` afterwards.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales (region TEXT, amount REAL)")

with con:                                              # commits at the end of the block
    con.execute("INSERT INTO sales VALUES ('EU', 120.0)")

print(con.execute("SELECT COUNT(*) FROM sales").fetchone())   # still open: this works
con.close()
```

```text
(1,)
```

**Reading columns by name.** Set `con.row_factory = sqlite3.Row` and each row can be read like a dict, by column name. Reading by position still works too, and `.keys()` lists the column names.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
con.execute("CREATE TABLE sales (region TEXT, amount REAL)")
con.execute("INSERT INTO sales VALUES ('EU', 120.0)")

row = con.execute("SELECT region, amount FROM sales").fetchone()
print(row["region"], row["amount"])
print(row[0], row.keys())
```

```text
EU 120.0
EU ['region', 'amount']
```

**Straight into pandas.** `pd.read_sql_query(sql, con)` runs a query and returns the result as a DataFrame. Going the other way, `df.to_sql("table", con, if_exists="append", index=False)` writes a DataFrame into a table.

```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE sales (region TEXT, amount REAL)")
con.execute("INSERT INTO sales VALUES ('EU', 120.0), ('US', 80.0)")

df = pd.read_sql_query("SELECT region, amount FROM sales", con)
print(df)
```

```text
  region  amount
0     EU   120.0
1     US    80.0
```

**MySQL with `pymysql`.** Connecting to a MySQL server works the same way, but you give the server's address and your login instead of a file path. Keep the password out of the code, for example in an environment variable. pymysql uses `%s` as its placeholder where sqlite3 uses `?`. (This example needs a running MySQL server, so its output isn't shown.)

```python
import os
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

**The problem: building SQL from user input.** Programs often put a value typed by a user into a query, for example looking up a name. The tempting way is to paste the value into the SQL text with an f-string. That lets the **user's text become part of the SQL**, which is called **SQL injection**.

Here is a normal lookup done the unsafe way. It works fine with an ordinary name:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, role TEXT)")
con.execute("INSERT INTO users VALUES ('ana', 'admin'), ('ben', 'viewer')")

name = "ben"                                                    # typed by a user
print(con.execute(f"SELECT role FROM users WHERE name = '{name}'").fetchall())
```

```text
[('viewer',)]
```

But a user can type something that changes the query itself:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, role TEXT)")
con.execute("INSERT INTO users VALUES ('ana', 'admin'), ('ben', 'viewer')")

name = "x' OR '1'='1"                                           # a malicious "name"
sql = f"SELECT role FROM users WHERE name = '{name}'"
print(sql)
print(con.execute(sql).fetchall())
```

```text
SELECT role FROM users WHERE name = 'x' OR '1'='1'
[('admin',), ('viewer',)]
```

The quote in the "name" closed the string early, and `OR '1'='1'` (always true) was added to the condition, so the query returned **every** row.

**The fix: placeholders.** Write `?` in the SQL where the value goes, and pass the value separately as a tuple. The database driver sends the SQL and the value **separately**, so the value is always treated as plain data, never as SQL.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, role TEXT)")
con.execute("INSERT INTO users VALUES ('ana', 'admin'), ('ben', 'viewer')")

for name in ["ben", "x' OR '1'='1"]:
    print(con.execute("SELECT role FROM users WHERE name = ?", (name,)).fetchall())
```

```text
[('viewer',)]
[]
```

The normal name still works. The attack now just looks for a user literally called `x' OR '1'='1`, finds nobody, and returns nothing.

**The one-item tuple.** The values go in a tuple, even when there is only one. `(name,)` with a comma is a tuple; `(name)` without one is just `name`, and the call raises `sqlite3.ProgrammingError`. A list, `[name]`, also works.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (id INTEGER)")
print(con.execute("SELECT * FROM t WHERE id = ?", (5,)).fetchall())
try:
    con.execute("SELECT * FROM t WHERE id = ?", (5))     # (5) is just the integer 5
except sqlite3.ProgrammingError as e:
    print("ProgrammingError:", e)
```

```text
[]
ProgrammingError: parameters are of unsupported type
```

**Named placeholders.** Instead of `?`, you can write `:name` in the SQL and pass a dict. This is easier to read when there are several values.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, role TEXT)")
con.execute("INSERT INTO users VALUES ('ana', 'admin'), ('ben', 'viewer')")

print(con.execute("SELECT name FROM users WHERE role = :r", {"r": "admin"}).fetchall())
```

```text
[('ana',)]
```

pymysql (for MySQL) uses `%s` and `%(name)s` instead of `?` and `:name`, but the idea is the same.

**Many rows at once: `executemany`.** `executemany` runs the same statement once for each item in a list:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users (name TEXT, role TEXT)")

new_users = [("cy", "viewer"), ("dee", "editor"), ("o'brien", "viewer")]
con.executemany("INSERT INTO users VALUES (?, ?)", new_users)
print(con.execute("SELECT * FROM users").fetchall())
```

```text
[('cy', 'viewer'), ('dee', 'editor'), ("o'brien", 'viewer')]
```

`o'brien` went in without any trouble: placeholders also take care of quotes inside values, which would break an f-string query.

**Values only.** Placeholders can stand in for **values**, not for table or column names. If a user picks which column to sort by, check their choice against a fixed list of allowed names before putting it in the SQL.

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

**What comes back from SQLite.** Each value you read back arrives as the matching Python type from the first table. Two surprises: SQLite has no date type and no true/false type.

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (qty INTEGER, price REAL, day TEXT, paid INTEGER, note TEXT)")
con.execute("INSERT INTO t VALUES (?, ?, ?, ?, ?)", (3, 2.5, "2025-07-15", True, None))

row = con.execute("SELECT * FROM t").fetchone()
print(row)
print([type(value).__name__ for value in row])
```

```text
(3, 2.5, '2025-07-15', 1, None)
['int', 'float', 'str', 'int', 'NoneType']
```

The date came back as a plain string, `True` came back as `1`, and `NULL` came back as `None`.

**Dates are stored as text.** Store dates as ISO 8601 text (`'2025-07-15'`): year first, so sorting the text also sorts the dates. To do date arithmetic, convert the string back to a real date first.

```python
import datetime

day = "2025-07-15"                            # what SQLite gave back
real_date = datetime.date.fromisoformat(day)
print(real_date + datetime.timedelta(days=1))

try:
    day + datetime.timedelta(days=1)          # can't add days to a string
except TypeError as e:
    print("TypeError:", e)
```

```text
2025-07-16
TypeError: can only concatenate str (not "datetime.timedelta") to str
```

Subtracting one date from another gives a `timedelta`, and its `.days` attribute is the gap as a whole number:

```python
import datetime

placed = datetime.date.fromisoformat("2025-07-01")
gap = datetime.date(2025, 7, 15) - placed
print(gap.days)
```

```text
14
```

In pandas, `pd.read_sql_query(..., parse_dates=["day"])` or `pd.to_datetime` does the conversion.

**Missing values turn integer columns into floats.** pandas' standard integer type has no way to store "missing", so an integer column containing a `NULL` becomes `float64`, and `3` shows as `3.0`. The nullable `"Int64"` type (capital I) keeps whole numbers and shows the gap as `<NA>`.

```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (qty INTEGER)")
con.execute("INSERT INTO t VALUES (3), (NULL)")

df = pd.read_sql_query("SELECT qty FROM t", con)
print(df["qty"].dtype, df["qty"].tolist())
print(df["qty"].astype("Int64").tolist())
```

```text
float64 [3.0, nan]
[3, <NA>]
```

**SQLite doesn't enforce column types.** A column declared `INTEGER` will still accept text (this is called **type affinity**). Check your values in Python before inserting them. `typeof()` shows what was actually stored:

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (qty INTEGER)")
con.execute("INSERT INTO t VALUES (3)")
con.execute("INSERT INTO t VALUES ('three')")     # accepted, no error
print(con.execute("SELECT qty, typeof(qty) FROM t").fetchall())
```

```text
[(3, 'integer'), ('three', 'text')]
```

**Money: avoid floats.** Floats can't store most decimals exactly, so sums drift (`0.1 + 0.2` is `0.30000000000000004`). For money, use `decimal.Decimal`, which MySQL's `DECIMAL` type maps to, or store whole cents as integers.

```python
from decimal import Decimal

print(0.1 + 0.2)
print(Decimal("0.1") + Decimal("0.2"))
```

```text
0.30000000000000004
0.3
```

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
