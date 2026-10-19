from qhelp import Q

SHOP = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, region TEXT);
INSERT INTO customers VALUES (1, 'Ana', 'EU'), (2, 'Ben', 'US'), (3, 'Cara', 'EU'), (4, 'Dev', 'APAC');
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL, status TEXT);
INSERT INTO orders VALUES (10, 1, 120, 'paid'), (11, 1, 80, 'paid'), (12, 2, 200, 'refunded'),
                          (13, 3, 50, 'paid'), (14, 5, 70, 'paid');
"""


QUESTIONS = [
    # ---------- 2.1.1 Syntax, scope, control flow ----------
    Q("b2-001", "2.1.1", 2,
      "What does this code print?",
      ["`3 -4 1 2.0`", "`3 -3 1 2.0`", "`3.5 -3.5 1 2`", "`3 -4 1 2`"],
      0,
      {1: "`//` floors toward negative infinity, so −7 // 2 is −4, not −3.",
       2: "`//` returns a whole number for integers; `/` is the operator that gives 3.5.",
       3: "`/` always returns a float, so 8 / 4 is 2.0."},
      "7 // 2 = 3; −7 // 2 floors −3.5 down to −4; 7 % 3 = 1; 2 ** 3 / 4 = 8 / 4 = 2.0 (true division gives a float).",
      "Syllabus 2.1.1 · Python docs: numeric types", ["operators", "division"],
      code="""
      print(7 // 2, -7 // 2, 7 % 3, 2 ** 3 / 4)
      """, verify="stdout"),

    Q("b2-002", "2.1.1", 2,
      "What does this loop print?",
      ["`16`", "`26`", "`10`", "`5`"],
      0,
      {1: "26 adds every value from range (2 + 5 + 8 + 11); `continue` skips the even ones.",
       2: "10 is the sum of the even values, which are the ones skipped.",
       3: "The loop continues after 5; 11 is also odd."},
      "`range(2, 12, 3)` yields 2, 5, 8, 11. Even values are skipped, so total = 5 + 11 = 16.",
      "Syllabus 2.1.1", ["loops", "range"],
      code="""
      total = 0
      for i in range(2, 12, 3):
          if i % 2 == 0:
              continue
          total += i
      print(total)
      """, verify="stdout"),

    Q("b2-003", "2.1.1", 3,
      "What does this code print?",
      ["`120.0 0.1 130.0 0.3`", "`120.0 0.2 130.0 0.3`", "`120.0 0.1 130.0 0.1`", "`110.0 0.1 130.0 0.3`"],
      0,
      {1: "The assignment inside `apply` creates a local `rate`; the global stays 0.1.",
       2: "`global rate` makes `apply_global` rebind the module-level name, so it becomes 0.3.",
       3: "`apply` uses its local rate of 0.2, giving 120.0, not 110.0."},
      "`apply` shadows `rate` with a local 0.2 (global untouched). `apply_global` declares `global rate` and sets it to 0.3. Arguments are evaluated left to right, so the second value printed is still 0.1 and the last is 0.3.",
      "Syllabus 2.1.1 · Python docs: scopes and namespaces", ["scope", "global"],
      code="""
      rate = 0.1

      def apply(price):
          rate = 0.2
          return price * (1 + rate)

      def apply_global(price):
          global rate
          rate = 0.3
          return price * (1 + rate)

      print(round(apply(100), 1), rate, round(apply_global(100), 1), rate)
      """, verify="stdout"),

    Q("b2-004", "2.1.1", 3,
      "What happens when this code runs?",
      ["An UnboundLocalError is raised", "It prints `6`", "It prints `1`", "A SyntaxError is raised"],
      0,
      {1: "Because `count` is assigned inside the function, it is local there, and the read on the right-hand side happens before it has a value.",
       2: "There's no local value of 0 to add 1 to; the read fails first.",
       3: "The code is syntactically valid; the problem appears only when the function runs."},
      "Assigning to `count` inside `increment` makes it a local name for the whole function, so reading it on the right side raises UnboundLocalError. `global count` would fix it.",
      "Syllabus 2.1.1 · Python docs: UnboundLocalError", ["scope", "errors"],
      code="""
      count = 5

      def increment():
          count = count + 1
          return count

      print(increment())
      """, verify="raises:UnboundLocalError"),

    Q("b2-005", "2.1.1", 2,
      "What does this code print?",
      ["`27`",
       "no break\n27",
       "`81`",
       "no break\n81"],
      0,
      {1: "The loop ends with `break`, so its `else` block does not run.",
       2: "The loop stops at 27 because of `break`, before multiplying again.",
       3: "The loop breaks at 27, so neither \"no break\" nor 81 appears."},
      "n goes 3, 9, 27, then `break` exits. A loop's `else` runs only if the loop finishes without `break`, so only 27 is printed.",
      "Syllabus 2.1.1", ["while", "break"],
      code="""
      n = 1
      while n < 100:
          n *= 3
          if n == 27:
              break
      else:
          print("no break")
      print(n)
      """, optlang="text", verify="stdout"),

    Q("b2-006", "2.1.1", 1,
      "Which value is truthy in an `if` statement?",
      ["`[0]`", "`0`", "`\"\"`", "`None`"],
      0,
      {1: "Zero is falsy.",
       2: "An empty string is falsy.",
       3: "None is falsy."},
      "A list containing one element (even 0) is non-empty, so it is truthy. 0, \"\" and None are all falsy.",
      "Syllabus 2.1.1", ["truthiness", "types"]),

    Q("b2-007", "2.1.1", 1,
      "What does this list comprehension produce?",
      ["`[9, 16, 81]`", "`[9, 1, 16, 0, 25, 81]`", "`[3, 4, 9]`", "`[9, 16, 0, 81]`"],
      0,
      {1: "The `if x > 0` filter removes −1, 0 and −5 before squaring.",
       2: "The expression squares each kept value.",
       3: "0 is not greater than 0, so it's filtered out."},
      "Only positive values (3, 4, 9) pass the filter, and each is squared.",
      "Syllabus 2.1.1", ["comprehensions", "filtering"],
      code="""
      data = [3, -1, 4, 0, -5, 9]
      print([x ** 2 for x in data if x > 0])
      """, verify="stdout"),

    Q("b2-008", "2.1.1", 3,
      "What does this code print?",
      ["`1-Ann-90; 2-Bob-75; done`",
       "`0-Ann-90; 1-Bob-75; done`",
       "`1-Ann-90; 2-Bob-75; 3-Cy-None; done`",
       "1 Ann 90\n2 Bob 75\ndone"],
      0,
      {1: "`start=1` makes `enumerate` count from 1.",
       2: "`zip` stops at the shorter list, so Cy (who has no score) is dropped without any error.",
       3: "`sep=\"-\"` joins the values with dashes, and `end=\"; \"` keeps everything on one line."},
      "`zip` pairs the names with the two scores and stops there; `enumerate(..., start=1)` numbers the pairs from 1; `sep` goes between the printed values and `end` replaces the newline, so the final `print` continues the same line.",
      "Syllabus 2.1.1 · Python docs", ["zip", "enumerate", "print"], optlang="text",
      code="""
      names = ["Ann", "Bob", "Cy"]
      scores = [90, 75]
      for i, (name, score) in enumerate(zip(names, scores), start=1):
          print(i, name, score, sep="-", end="; ")
      print("done")
      """, verify="stdout"),

    Q("b2-009", "2.1.1", 3,
      "What does this code print?",
      ["`2 4 0.12 4`", "`3 4 0.13 5`", "`2 4 0.13 4`", "`3 4 0.13 4.5`"],
      0,
      {1: "Python doesn't round halves up: exact halves go to the even neighbour, so 2.5 becomes 2 and 4.5 becomes 4.",
       2: "0.125 is stored exactly in binary, so it is a true half and rounds to the even 0.12.",
       3: "`round(2.5)` is 2, and `:.0f` shows no decimal places, so 4.5 prints as 4."},
      "Exact halves round to the even neighbour (\"banker's rounding\"): 2.5 → 2, 3.5 → 4, 0.125 → 0.12 and, with the `.0f` format spec, 4.5 → 4.",
      "Syllabus 2.1.1 · Python docs (round)", ["round", "floats"],
      code="""
      print(round(2.5), round(3.5), round(0.125, 2), f"{4.5:.0f}")
      """, verify="stdout"),

    # ---------- 2.1.2 Functions ----------
    Q("b2-010", "2.1.2", 2,
      "What does this code print?",
      ["`120.0 110.0 115.0 50.0`", "`120.0 110.0 100.0 50.0`", "`120.0 105.0 115.0 50.0`", "`120.0 110.0 115.0 60.0`"],
      0,
      {1: "`discount=5` is passed by keyword and subtracted: 120 − 5 = 115.",
       2: "The positional 0.1 fills `vat`, the second parameter, giving 110.",
       3: "`vat=0.0` means no tax on 50."},
      "Defaults fill any parameter not given: 100 × 1.2 = 120; the positional 0.1 sets vat → 110; the keyword discount subtracts 5 → 115; net=50 with vat=0.0 → 50.0.",
      "Syllabus 2.1.2", ["arguments", "defaults"],
      code="""
      def price(net, vat=0.2, discount=0):
          return round(net * (1 + vat) - discount, 2)

      print(price(100), price(100, 0.1), price(100, discount=5), price(net=50, vat=0.0))
      """, verify="stdout"),

    Q("b2-011", "2.1.2", 2,
      "Given `def report(title, rows, sep=\",\"):`, which call is invalid?",
      ["`report(title=\"Q1\", data)`",
       "`report(\"Q1\", data, sep=\";\")`",
       "`report(rows=data, title=\"Q1\")`",
       "`report(\"Q1\", sep=\";\", rows=data)`"],
      0,
      {1: "Two positional arguments, then a keyword: valid.",
       2: "Keyword arguments can be in any order: valid.",
       3: "A positional first argument followed by keywords: valid."},
      "A positional argument cannot follow a keyword argument in a call; `report(title=\"Q1\", data)` is a SyntaxError.",
      "Syllabus 2.1.2", ["arguments", "keyword"],
      verify={"py": """
      data = [1]
      def report(title, rows, sep=","):
          return title
      try:
          compile('report(title="Q1", data)', "<q>", "eval")
          raise AssertionError("expected SyntaxError")
      except SyntaxError:
          pass
      assert report("Q1", data, sep=";") == "Q1"
      assert report(rows=data, title="Q1") == "Q1"
      assert report("Q1", sep=";", rows=data) == "Q1"
      """}),

    Q("b2-012", "2.1.2", 3,
      "What does this code print?",
      ["`1 2 1 3`", "`1 1 1 1`", "`1 2 3 4`", "`1 2 1 1`"],
      0,
      {1: "The default list is created once and shared, so it keeps growing between calls that use it.",
       2: "The third call passes its own new list, so it starts from empty.",
       3: "The fourth call uses the shared default list again, which already holds \"a\" and \"b\"."},
      "The default `[]` is evaluated once, at definition time. Calls without `history` share it (1, 2, then 3); the call with `[]` uses a fresh list (1).",
      "Syllabus 2.1.2 · Python docs: default argument values", ["defaults", "mutability"],
      code="""
      def log(event, history=[]):
          history.append(event)
          return len(history)

      print(log("a"), log("b"), log("c", []), log("d"))
      """, verify="stdout"),

    Q("b2-013", "2.1.2", 2,
      "What does this code print?",
      ["`('tuple', 3, ['source', 'unit'])`", "`('list', 3, ['unit', 'source'])`", "`('tuple', 5, ['source', 'unit'])`", "`('dict', 3, ['source', 'unit'])`"],
      0,
      {1: "`*args` is always a tuple, and `sorted` orders the keyword names alphabetically.",
       2: "Keyword arguments go into `kwargs`, not `args`.",
       3: "`args` holds the positional values; `kwargs` is the dict."},
      "`*args` collects the three positional values into a tuple; `**kwargs` collects `unit` and `source` into a dict, whose sorted keys are ['source', 'unit'].",
      "Syllabus 2.1.2", ["args", "kwargs"],
      code="""
      def describe(*args, **kwargs):
          return type(args).__name__, len(args), sorted(kwargs)

      print(describe(1, 2, 3, unit="kg", source="lab"))
      """, verify="stdout"),

    Q("b2-014", "2.1.2", 2,
      "What does this code print?",
      ["6\nNone", "6\n6", "None\n6", "`6`"],
      0,
      {1: "`total` prints the sum but returns nothing, so `result` is None.",
       2: "The function body runs first, printing 6, before `result` is printed.",
       3: "`print(result)` also prints something: None."},
      "A function with no `return` returns None. The call prints 6, then `print(result)` prints None.",
      "Syllabus 2.1.2", ["return", "none"],
      code="""
      def total(values):
          s = sum(values)
          print(s)

      result = total([1, 2, 3])
      print(result)
      """, optlang="text", verify="stdout"),

    Q("b2-015", "2.1.2", 1,
      "Which function definition is valid Python?",
      ["`def f(a, b=2):`", "`def f(a=1, b):`", "`def f(a, b=2, c):`", "`def f(a b):`"],
      0,
      {1: "A parameter without a default can't follow one with a default.",
       2: "`c` has no default but follows `b=2`.",
       3: "Parameters must be separated by commas."},
      "Required parameters come first, then optional ones with defaults.",
      "Syllabus 2.1.2", ["parameters", "syntax"],
      verify={"py": """
      ok = []
      for i in range(4):
          try:
              compile(opt(i) + "\\n    pass", "<q>", "exec")
              ok.append(i)
          except SyntaxError:
              pass
      assert ok == q["answer"], ok
      """}),

    Q("b2-016", "2.1.2", 2,
      "What happens when this code runs?",
      ["A TypeError is raised", "It prints `2 rows as json`", "It prints `2 rows as csv`", "A SyntaxError is raised"],
      0,
      {1: "Parameters after `*` are keyword-only, so \"json\" can't be passed by position.",
       2: "The call fails before the function body runs.",
       3: "The definition and call are both valid syntax; the error happens at call time."},
      "`fmt` follows a bare `*`, so it is keyword-only. Passing a second positional argument raises TypeError: export() takes 1 positional argument but 2 were given.",
      "Syllabus 2.1.2", ["keyword-only", "errors"],
      code="""
      def export(data, *, fmt="csv"):
          return f"{len(data)} rows as {fmt}"

      print(export([1, 2], "json"))
      """, verify="raises:TypeError"),

    Q("b2-017", "2.1.2", 3,
      "Given `def scale(x, /, factor=2, *, offset=0):`, which call raises a TypeError?",
      ["`scale(x=3)`", "`scale(3, 4)`", "`scale(3, offset=1)`", "`scale(3, factor=4, offset=1)`"],
      0,
      {1: "`factor` sits between `/` and `*`, so it can be passed by position.",
       2: "`offset` is keyword-only and is passed by name, which is what it requires.",
       3: "`factor` can also be passed by name, and `offset` is passed by name as required."},
      "Parameters before `/` are positional-only, so `x` can't be passed as `x=3`. Parameters after `*` are keyword-only. Those in between, here `factor`, can be passed either way.",
      "Syllabus 2.1.2 · Python docs", ["positional-only", "keyword-only"],
      verify={"py": """
      def scale(x, /, factor=2, *, offset=0):
          return x * factor + offset
      results = []
      for i in range(4):
          try:
              eval(opt(i))
              results.append(False)
          except TypeError:
              results.append(True)
      assert results == [True, False, False, False], results
      """}),

    Q("b2-018", "2.1.2", 3,
      "What does this code print?",
      ["['Ben', 'Cy', 'Ana', 'Dee']\nDee Ana",
       "['Dee', 'Ana', 'Ben', 'Cy']\nDee Ana",
       "['Cy', 'Ben', 'Ana', 'Dee']\nDee Ana",
       "['Ben', 'Cy', 'Ana', 'Dee']\nDee Dee"],
      0,
      {1: "The minus sign sorts the scores from high to low.",
       2: "Ties on score are broken by the second part of the key, the name, A to Z: Ben before Cy.",
       3: "`max` returns the first of several equal maximums: Ana, Ben and Dee all have 3-letter names, and Ana comes first."},
      "The key `(-score, name)` sorts by score from high to low, then by name: Ben (61), Cy (61), Ana (52), Dee (47). `min` by score picks Dee (47). `max` by name length finds a tie at 3 letters and returns the first, Ana.",
      "Syllabus 2.1.2, 2.1.4 · Python docs (sorting)", ["lambda", "key-function", "sorted"], optlang="text",
      code="""
      staff = [("Ana", "EU", 52), ("Ben", "US", 61), ("Cy", "EU", 61), ("Dee", "US", 47)]
      print([s[0] for s in sorted(staff, key=lambda s: (-s[2], s[0]))])
      print(min(staff, key=lambda s: s[2])[0], max(staff, key=lambda s: len(s[0]))[0])
      """, verify="stdout"),

    Q("b2-019", "2.1.2", 2,
      "Which call sorts the list `words` from the shortest word to the longest?",
      ["`sorted(words, key=len)`", "`sorted(words, key=len())`", "`sorted(words, len)`", "`sorted(len(words))`"],
      0,
      {1: "`len()` is called immediately, with no argument, and raises TypeError; pass the function itself.",
       2: "`sorted` takes only one positional argument; `key` must be passed by name.",
       3: "`len(words)` is a single number, and a number can't be sorted."},
      "`key=` takes a function. `sorted` calls `len` on each word and orders the words by those lengths.",
      "Syllabus 2.1.2 · Python docs (sorted)", ["key-function", "sorted"],
      verify={"py": """
      words = ["banana", "fig", "kiwi"]
      assert eval(opt(0)) == ["fig", "kiwi", "banana"]
      for i in (1, 2, 3):
          try:
              eval(opt(i))
              raise AssertionError(f"option {i} ran")
          except TypeError:
              pass
      """}),

    # ---------- 2.1.3 Ecosystem ----------
    Q("b2-020", "2.1.3", 1,
      "Which library is designed for reading, cleaning, joining and grouping labeled tabular data?",
      ["pandas", "Matplotlib", "BeautifulSoup", "requests"],
      0,
      {1: "Matplotlib draws charts.",
       2: "BeautifulSoup parses HTML.",
       3: "requests makes HTTP calls."},
      "pandas provides Series and DataFrame for labeled tables, with I/O, cleaning, merging and groupby.",
      "Syllabus 2.1.3", ["ecosystem", "pandas"]),

    Q("b2-021", "2.1.3", 2,
      "An analyst must report which predictors of house prices are statistically significant, with p-values and confidence intervals for each coefficient. Which library fits best?",
      ["statsmodels", "scikit-learn", "Seaborn", "BeautifulSoup"],
      0,
      {1: "scikit-learn focuses on prediction and doesn't report p-values for coefficients.",
       2: "Seaborn visualizes; it doesn't produce inference tables.",
       3: "BeautifulSoup parses HTML."},
      "statsmodels fits regressions with full inference output: coefficients, standard errors, p-values and confidence intervals.",
      "Syllabus 2.1.3", ["ecosystem", "statsmodels"]),

    Q("b2-022", "2.1.3", 1,
      "Which two libraries are needed to download a web page and extract the product names from its HTML? Select two.",
      ["requests", "BeautifulSoup", "NumPy", "Matplotlib", "sqlite3"],
      [0, 1],
      {2: "NumPy is for numerical arrays.",
       3: "Matplotlib is for charts.",
       4: "sqlite3 talks to SQLite databases."},
      "requests fetches the page over HTTP; BeautifulSoup parses the HTML and finds the elements.",
      "Syllabus 2.1.3, 1.4.3", ["ecosystem", "web-scraping"]),

    Q("b2-023", "2.1.3", 2,
      "Which statement about Seaborn is correct?",
      ["It is built on Matplotlib and draws statistical charts directly from DataFrames",
       "It replaces Matplotlib, so Matplotlib calls no longer work on its charts",
       "It is a machine learning library",
       "It can only draw charts from NumPy arrays"],
      0,
      {1: "Seaborn charts are Matplotlib figures; you still use Matplotlib to adjust and save them.",
       2: "Machine learning is scikit-learn's job.",
       3: "Seaborn works best with pandas DataFrames and column names."},
      "Seaborn is a high-level layer over Matplotlib for statistical graphics, designed around DataFrames.",
      "Syllabus 2.1.3", ["ecosystem", "seaborn"]),

    Q("b2-024", "2.1.3", 1,
      "Which of these is part of Python's standard library, so it needs no installation?",
      ["sqlite3", "pandas", "requests", "PyMySQL"],
      0,
      {1: "pandas is a third-party package installed with pip or conda.",
       2: "requests is third-party.",
       3: "PyMySQL is third-party."},
      "sqlite3 ships with Python; the others come from PyPI.",
      "Syllabus 2.1.3, 2.2.1", ["ecosystem", "standard-library"]),

    Q("b2-025", "2.1.3", 1,
      "When choosing between two libraries for a long-running project, which two factors matter most? Select two.",
      ["Active maintenance and good documentation",
       "A licence compatible with how the project will be used",
       "Whether the library's name is short",
       "Whether it was the first search result",
       "Whether its logo matches the company's colours"],
      [0, 1],
      {2: "A name says nothing about quality or fit.",
       3: "Search ranking isn't a measure of suitability.",
       4: "Branding is irrelevant to technical suitability."},
      "Suitability means fitting the task, being maintained and documented, having a community, and a licence that allows your use.",
      "Syllabus 2.1.3", ["ecosystem", "evaluation"]),

    Q("b2-026", "2.1.3", 3,
      "An analyst must (1) read 30 Excel workbooks into one table, (2) predict which customers will churn and estimate accuracy with cross-validation, and (3) give a regulator a p-value for each predictor. Which set of tools fits?",
      ["pandas (with openpyxl) for the workbooks, scikit-learn for the churn model and cross-validation, statsmodels for the p-values",
       "NumPy for the workbooks, Seaborn for the model, SciPy for the p-values",
       "pandas for the workbooks, then statsmodels for everything else, because it also provides cross-validation and pipelines",
       "BeautifulSoup for the workbooks, then scikit-learn for the model and its p-values"],
      0,
      {1: "NumPy doesn't read Excel files, and Seaborn draws charts; it doesn't fit predictive models.",
       2: "statsmodels reports inference statistics, but cross-validation, pipelines and predictive evaluation are scikit-learn's job.",
       3: "BeautifulSoup parses HTML, not Excel, and scikit-learn's models don't report p-values."},
      "`pd.read_excel` (which uses openpyxl) and `pd.concat` combine the workbooks; scikit-learn handles prediction and `cross_val_score`; statsmodels reports coefficients with p-values and confidence intervals.",
      "Syllabus 2.1.3", ["ecosystem", "library-choice"]),

    Q("b2-027", "2.1.3", 2,
      "Which two statements about scikit-learn are correct? Select two.",
      ["It provides `train_test_split` and cross-validation tools",
       "Its models share the same `fit` / `predict` interface",
       "It reports p-values for regression coefficients by default",
       "It is a plotting library built on Matplotlib",
       "It is the standard tool for reading Excel files"],
      [0, 1],
      {2: "Inference output such as p-values comes from statsmodels.",
       3: "That describes Seaborn.",
       4: "pandas reads Excel files (`pd.read_excel`)."},
      "scikit-learn is the machine-learning library: preprocessing, splitting, models with a common `fit`/`predict` API, and evaluation metrics.",
      "Syllabus 2.1.3 · scikit-learn docs", ["ecosystem", "scikit-learn"]),

    # ---------- 2.1.4 Data structures ----------
    Q("b2-030", "2.1.4", 2,
      "What does this code print?",
      ["`3 None 3`", "`2 None 3`", "`3 0 3`", "A KeyError is raised"],
      0,
      {1: "\"milk\" is added as a new key, so there are three keys.",
       2: "`get` without a default returns None for a missing key.",
       3: "`get` never raises; only `stock[\"sugar\"]` would."},
      "`get(\"milk\", 0)` returns 0, so milk becomes 2 (a third key); tea drops to 3; `get(\"sugar\")` returns None.",
      "Syllabus 2.1.4", ["dict", "get"],
      code="""
      stock = {"tea": 4, "coffee": 0}
      stock["milk"] = stock.get("milk", 0) + 2
      stock["tea"] -= 1
      print(len(stock), stock.get("sugar"), stock["tea"])
      """, verify="stdout"),

    Q("b2-031", "2.1.4", 2,
      "What does this code print?",
      ["`['apac', 'eu', 'latam', 'us'] ['us'] ['apac', 'eu']`",
       "`['apac', 'eu', 'latam', 'us', 'us'] ['us'] ['apac', 'eu']`",
       "`['apac', 'eu', 'latam', 'us'] ['us'] ['latam']`",
       "`['us'] ['apac', 'eu', 'latam', 'us'] ['apac', 'eu']`"],
      0,
      {1: "Sets hold unique items, so \"us\" appears once in the union.",
       2: "`a - b` keeps items of `a` not in `b`; \"latam\" is only in `b`.",
       3: "`|` is union and `&` is intersection, not the other way round."},
      "`|` is the union, `&` the intersection and `-` the difference (in a but not b).",
      "Syllabus 2.1.4", ["set", "set-operations"],
      code="""
      a = {"eu", "us", "apac"}
      b = {"us", "latam"}
      print(sorted(a | b), sorted(a & b), sorted(a - b))
      """, verify="stdout"),

    Q("b2-032", "2.1.4", 2,
      "What does this code print?",
      ["`None [95, 82, 70]`", "`[95, 82, 70] [70, 95, 82]`", "`[95, 82, 70] [95, 82, 70]`", "`None [70, 95, 82]`"],
      0,
      {1: "`list.sort()` returns None and sorts the list itself.",
       2: "`ranked` is None, not a list.",
       3: "`scores` was sorted in place, so it changed."},
      "`sort()` sorts in place and returns None. Use `sorted(scores, reverse=True)` for a new list.",
      "Syllabus 2.1.4", ["list", "sort"],
      code="""
      scores = [70, 95, 82]
      ranked = scores.sort(reverse=True)
      print(ranked, scores)
      """, verify="stdout"),

    Q("b2-033", "2.1.4", 1,
      "What does this code print?",
      ["`3 4`", "`4 4`", "`3 3`", "`4 3`"],
      0,
      {1: "`append` adds the list [3, 4] as a single item.",
       2: "`extend` adds each item separately.",
       3: "The lengths are the other way round."},
      "`append([3, 4])` adds one element (a nested list), giving length 3; `extend([3, 4])` adds two elements, giving length 4.",
      "Syllabus 2.1.4", ["list", "append"],
      code="""
      a = [1, 2]
      b = [1, 2]
      a.append([3, 4])
      b.extend([3, 4])
      print(len(a), len(b))
      """, verify="stdout"),

    Q("b2-034", "2.1.4", 1,
      "What happens when this code runs?",
      ["A TypeError is raised", "`point` becomes `(5, 4)`", "A ValueError is raised", "A new tuple is created and assigned to `point`"],
      0,
      {1: "Tuples are immutable; item assignment isn't allowed.",
       2: "The error is about the operation on the type (TypeError), not a bad value.",
       3: "Item assignment never builds a new tuple."},
      "Tuples don't support item assignment: TypeError: 'tuple' object does not support item assignment.",
      "Syllabus 2.1.4", ["tuple", "immutability"],
      code="""
      point = (3, 4)
      point[0] = 5
      """, verify="raises:TypeError"),

    Q("b2-035", "2.1.4", 2,
      "A script checks whether each of 2 million transaction IDs appears in a blocklist of 50,000 IDs. Which structure for the blocklist makes each check fastest?",
      ["A set", "A list", "A tuple", "One long comma-separated string"],
      0,
      {1: "`in` on a list scans items one by one.",
       2: "Tuples also scan linearly.",
       3: "Substring search is slow and can give false matches (\"12\" inside \"123\")."},
      "Sets use hashing, so `id in blocklist` takes about the same time regardless of the blocklist's size.",
      "Syllabus 2.1.4", ["set", "performance"]),

    Q("b2-036", "2.1.4", 3,
      "What does this code print?",
      ["`1042 paid 39.8`", "`Order 1042 paid 39.8`", "`1042 PAID 39.8`", "`1042 paid 19.9019.90`"],
      0,
      {1: "`split(\"-\")[1]` keeps only the part after the dash.",
       2: "`.lower()` converts \"PAID\" to lowercase.",
       3: "`float()` converts the text first, so `* 2` multiplies the number."},
      "Splitting on \";\" and stripping gives ['Order-1042', 'PAID', '19.90']; then the ID after the dash, the lowercased status, and 19.9 × 2 = 39.8.",
      "Syllabus 2.1.4", ["strings", "split"],
      code="""
      raw = "  Order-1042 ; PAID ; 19.90 "
      parts = [p.strip() for p in raw.split(";")]
      print(parts[0].split("-")[1], parts[1].lower(), float(parts[2]) * 2)
      """, verify="stdout"),

    Q("b2-037", "2.1.4", 2,
      "Which two can be used as dictionary keys? Select two.",
      ["`(\"EU\", 2025)`", "`\"region\"`", "`[\"EU\", 2025]`", "`{\"EU\"}`", "`{\"id\": 1}`"],
      [0, 1],
      {2: "Lists are mutable and unhashable.",
       3: "Sets are mutable and unhashable.",
       4: "Dicts are mutable and unhashable."},
      "Keys must be hashable: strings and tuples of immutable values qualify; lists, sets and dicts don't.",
      "Syllabus 2.1.4", ["dict", "hashable"],
      verify={"py": """
      import ast
      ok = []
      for i in range(5):
          try:
              {ast.literal_eval(opt(i)): 1}
              ok.append(i)
          except TypeError:
              pass
      assert ok == q["answer"], ok
      """}),

    Q("b2-038", "2.1.4", 2,
      "What does this code print?",
      ["`south 95`", "`south 340`", "`east 95`", "`north 120`"],
      0,
      {1: "`sorted(...)[0]` is the smallest value, not the largest.",
       2: "`max` with `key=sales.get` returns the key with the largest value.",
       3: "north has neither the largest value nor is it the first when sorted."},
      "`max(sales, key=sales.get)` returns the key whose value is largest (south, 340); the sorted values start with 95.",
      "Syllabus 2.1.4", ["dict", "max"],
      code="""
      sales = {"north": 120, "south": 340, "east": 95}
      top = max(sales, key=sales.get)
      print(top, sorted(sales.values())[0])
      """, verify="stdout"),

    Q("b2-039", "2.1.4", 3,
      "What does this code print?",
      ["`2 0 2 0 3`", "`2 0 2 0 2`", "`3 0 2 0 2`", "A KeyError is raised for \"APAC\""],
      0,
      {1: "Reading `by_region[\"APAC\"]` creates that key with an empty set, so the dict has 3 keys by the time `len(by_region)` runs.",
       2: "EU's items go into a set, so the repeated \"tea\" is stored once: EU has 2 distinct items.",
       3: "A `defaultdict` never raises KeyError for a missing key; it creates the key with a default value."},
      "EU's set holds {tea, jam} (2). Looking up \"APAC\" creates an empty set (0) and adds the key. The Counter has tea twice and returns 0 for the unseen \"milk\". The arguments are evaluated left to right, so `len(by_region)` sees EU, US and APAC: 3.",
      "Syllabus 2.1.4 · Python docs (collections)", ["defaultdict", "counter", "set"],
      code="""
      from collections import Counter, defaultdict

      orders = [("EU", "tea"), ("US", "jam"), ("EU", "jam"), ("EU", "tea")]
      by_region = defaultdict(set)
      for region, item in orders:
          by_region[region].add(item)
      counts = Counter(item for _, item in orders)
      print(len(by_region["EU"]), len(by_region["APAC"]), counts["tea"], counts["milk"], len(by_region))
      """, verify="stdout"),

    Q("b2-170", "2.1.4", 2,
      "What does this code print?",
      ["`[20, 30, 40] [50, 60] [10, 30, 50] 4`",
       "`[20, 30, 40, 50] [50, 60] [10, 30, 50] 4`",
       "`[20, 30, 40] [60] [10, 30, 50] 4`",
       "`[20, 30, 40] [50, 60] [20, 40, 60] 4`"],
      0,
      {1: "A slice stops before the stop position, so `nums[1:4]` is positions 1, 2 and 3.",
       2: "`nums[-2:]` starts two from the end and runs to the end: the last two items.",
       3: "With no start, a step slice begins at position 0: 10, 30, 50."},
      "`nums[1:4]` takes positions 1 to 3; `nums[-2:]` the last two; `nums[::2]` every second item from the start; and `nums[2:99]` stops quietly at the end, leaving 4 items.",
      "Syllabus 2.1.4 · Python docs", ["slicing", "list"],
      code="""
      nums = [10, 20, 30, 40, 50, 60]
      print(nums[1:4], nums[-2:], nums[::2], len(nums[2:99]))
      """, verify="stdout"),

    Q("b2-171", "2.1.4", 3,
      "What does this code print?",
      ["`analyst 12 5202 True`", "`analyst_ 12 2025 True`", "`-analys 12 5202 True`", "`analyst 13 5202 True`"],
      0,
      {1: "`s[5:12]` stops before position 12, the underscore, and `[::-1]` reverses \"2025\".",
       2: "Position 5 is \"A\" (the hyphen is position 4), so the slice is \"Analyst\".",
       3: "`find` counts from 0: the underscore is at position 12."},
      "Counting from 0, \"Analyst\" fills positions 5 to 11, so `s[5:12]` lowercased is \"analyst\". The underscore is at 12. Splitting on \"_\" gives \"2025\", reversed to \"5202\". The last four characters, \"2025\", are all digits.",
      "Syllabus 2.1.4 · Python docs (str)", ["strings", "slicing", "string-methods"],
      code="""
      s = "Data-Analyst_2025"
      print(s[5:12].lower(), s.find("_"), s.split("_")[1][::-1], s[-4:].isdigit())
      """, verify="stdout"),

    Q("b2-172", "2.1.4", 2,
      "What does this code print?",
      ["`1,234.6|40%|  ab|005`", "`1234.6|0.4%|ab  |005`", "`1,234.57|40%|  ab|5`", "`1,234.6|40.0%|ab  |005`"],
      0,
      {1: "`,` adds a thousands separator, `%` multiplies by 100, and `>` aligns to the right.",
       2: "`.1f` keeps one decimal place, and `03` pads 5 with zeros to three digits.",
       3: "`.0%` shows no decimal places, and `>4` pads on the left."},
      "`,.1f` gives a thousands separator and one decimal place; `.0%` multiplies by 100 and shows no decimals; `>4` right-aligns in a width of 4; `03` pads with zeros to 3 digits.",
      "Syllabus 2.1.4 · Python docs (format spec)", ["f-string", "formatting"],
      code="""
      print(f"{1234.567:,.1f}|{0.4:.0%}|{'ab':>4}|{5:03}")
      """, verify="stdout"),

    Q("b2-173", "2.1.4", 2,
      "What does this code print?",
      ["`['tea', 'jam', '', 'oat'] 3 ['tea', 'jam']`",
       "`['tea', 'jam', 'oat'] 3 ['tea', 'jam']`",
       "`['tea', 'jam', '', 'oat'] 2 ['tea', 'jam']`",
       "`['tea', 'jam', '', 'oat'] 3 ['tea', '', 'jam']`"],
      0,
      {1: "`split(\",\")` keeps the empty piece between the two commas.",
       2: "Splitting \"tea  jam\" on each single space gives 'tea', '' and 'jam': 3 pieces.",
       3: "`split()` with no argument treats any run of whitespace as one separator and drops empty pieces."},
      "A given separator splits at every occurrence, so neighbouring separators leave empty strings. `split()` with no argument splits on runs of whitespace and never returns empty pieces.",
      "Syllabus 2.1.4 · Python docs (str.split)", ["strings", "split"],
      code="""
      line = "tea,jam,,oat"
      print(line.split(","), len("tea  jam".split(" ")), "tea  jam".split())
      """, verify="stdout"),

    Q("b2-174", "2.1.4", 3,
      "What happens when this code runs?",
      ["It prints `[] ['a', 'b', 'c']`, then raises IndexError",
       "It raises IndexError at the first `print`",
       "It prints `[] ['a', 'b', 'c']`, then prints `None`",
       "It prints `[] []`, then raises IndexError"],
      0,
      {1: "Slices never raise for out-of-range positions; they return whatever exists.",
       2: "A list doesn't return None for a missing position; indexing past the end raises IndexError.",
       3: "A slice start before the beginning is treated as position 0, so `letters[-5:]` is the whole list."},
      "Slicing clamps out-of-range positions: `letters[5:]` is empty and `letters[-5:]` is everything. Indexing doesn't: `letters[5]` raises IndexError: list index out of range.",
      "Syllabus 2.1.4 · Python docs", ["indexing", "slicing", "indexerror"],
      code="""
      letters = ["a", "b", "c"]
      print(letters[5:], letters[-5:])
      print(letters[5])
      """,
      verify={"py": """
      import contextlib, io
      buf = io.StringIO()
      try:
          with contextlib.redirect_stdout(buf):
              exec(code, {})
          raise AssertionError("no IndexError")
      except IndexError:
          pass
      assert buf.getvalue().strip() == "[] ['a', 'b', 'c']", buf.getvalue()
      """}),

    Q("b2-176", "2.1.4", 3,
      "What does this code print?",
      ["`EU [120, 80] 95 1`", "`EU (120, 80) 95 1`", "`EU [120, 80] US 1`", "A ValueError is raised, because the tuples have different lengths"],
      0,
      {1: "A starred name always collects the leftovers into a list, even when unpacking a tuple.",
       2: "`*_, last` puts everything except the final item into `_`, so `last` is 95.",
       3: "A starred name absorbs any number of items, so different lengths are fine."},
      "`head` is the first tuple and `tail` the list of the rest. Unpacking `head` gives \"EU\" and the list [120, 80]. `*_, last` on (\"US\", 95) keeps the final item, 95. `tail` holds one tuple.",
      "Syllabus 2.1.4 · Python docs", ["unpacking", "tuples"],
      code="""
      data = [("EU", 120, 80), ("US", 95)]
      head, *tail = data
      region, *values = head
      *_, last = tail[0]
      print(region, values, last, len(tail))
      """, verify="stdout"),

    Q("b2-177", "2.1.4", 3,
      "What does this code print?",
      ["`{'t': ['tea', 'tea'], 'j': ['jam']} {}`",
       "`{'t': ['tea', 'tea'], 'j': ['jam']} {'t': ['tea', 'tea'], 'j': ['jam']}`",
       "`{'t': ['tea'], 'j': ['jam']} {}`",
       "A KeyError is raised"],
      0,
      {1: "`get` returns a new empty list without storing it in the dict, so the appends to it are lost.",
       2: "`setdefault` returns the list already stored under \"t\" on the second \"tea\", so both are kept.",
       3: "Neither method raises for a missing key; both fall back to the default."},
      "`setdefault(k, [])` inserts the empty list the first time and returns the stored list every time, so appending groups the words. `get(k, [])` hands back a temporary list that is never put into `b`, so `b` stays empty.",
      "Syllabus 2.1.4 · Python docs (dict)", ["dict", "setdefault", "get"],
      code="""
      a, b = {}, {}
      for word in ["tea", "jam", "tea"]:
          a.setdefault(word[0], []).append(word)
          b.get(word[0], []).append(word)
      print(a, b)
      """, verify="stdout"),

    Q("b2-178", "2.1.4", 3,
      "What does this code print?",
      ["`{'Oslo': 3, 'Rome': 4} [3]`",
       "`{'Oslo': 3, 'Rome': 4} []`",
       "`{'Oslo': 2, 'Rome': 4} [3]`",
       "A KeyError is raised for the order with no items"],
      0,
      {1: "Order 3's `items` list is empty, and an empty list is falsy, so `not o[\"items\"]` is True for it.",
       2: "Order 1 has two items (2 + 1 = 3), and both are added.",
       3: "`sum` over an empty list is 0, and `units.get(city, 0)` handles the first visit to each city."},
      "For each order, the city comes from the nested customer dict and the quantities from the nested list of items. Oslo gets 3 from order 1 and 0 from order 3; Rome gets 4. Only order 3 has no items.",
      "Syllabus 2.1.4", ["nested-data", "dict", "comprehension"],
      code="""
      orders = [
          {"id": 1, "customer": {"city": "Oslo"}, "items": [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}]},
          {"id": 2, "customer": {"city": "Rome"}, "items": [{"sku": "B", "qty": 4}]},
          {"id": 3, "customer": {"city": "Oslo"}, "items": []},
      ]
      units = {}
      for o in orders:
          city = o["customer"]["city"]
          units[city] = units.get(city, 0) + sum(i["qty"] for i in o["items"])
      print(units, [o["id"] for o in orders if not o["items"]])
      """, verify="stdout"),

    # ---------- 2.1.5 PEP 8 and PEP 257 ----------
    Q("b2-040", "2.1.5", 1,
      "Which pair of names follows PEP 8?",
      ["Class `SalesReport`, function `load_sales_data`",
       "Class `sales_report`, function `LoadSalesData`",
       "Class `SALES_REPORT`, function `loadSalesData`",
       "Class `Sales_Report`, function `Load_sales_data`"],
      0,
      {1: "This reverses the conventions.",
       2: "UPPER_CASE is for constants, and camelCase isn't PEP 8 for functions.",
       3: "Class names use CapWords without underscores; functions are lowercase."},
      "PEP 8: CapWords for classes, snake_case for functions and variables, UPPER_CASE for constants.",
      "Syllabus 2.1.5 · PEP 8", ["pep8", "naming"]),

    Q("b2-041", "2.1.5", 1,
      "What is PEP 8's maximum line length for code?",
      ["79 characters", "72 characters", "100 characters", "120 characters"],
      0,
      {1: "72 is the limit for comments and docstrings.",
       2: "PEP 8 lets a team agree on up to 99 characters, but its standard limit is 79.",
       3: "120 is a common editor setting, not PEP 8."},
      "PEP 8 limits code lines to 79 characters (72 for docstrings and comments).",
      "Syllabus 2.1.5 · PEP 8", ["pep8", "line-length"]),

    Q("b2-042", "2.1.5", 2,
      "Which one-line docstring follows PEP 257?",
      ["`\"\"\"Return the median of values.\"\"\"`",
       "`\"\"\"Returns the median of values\"\"\"`",
       "`'''median(values) -> float'''`",
       "`# Return the median of values.`"],
      0,
      {1: "PEP 257 asks for the imperative mood (\"Return\") and a closing period.",
       2: "Don't repeat the signature; describe what the function does, using triple double quotes.",
       3: "A comment isn't a docstring; it isn't available through `help()`."},
      "PEP 257: triple double quotes, a phrase in the imperative mood ending in a period, on one line.",
      "Syllabus 2.1.5 · PEP 257", ["pep257", "docstrings"]),

    Q("b2-043", "2.1.5", 2,
      "Which two lines follow PEP 8? Select two.",
      ["`if value is None:`", "`def area(width, height=1):`", "`if flag == True:`", "`total=df [ \"amount\" ].sum()`", "`import os, sys`"],
      [0, 1],
      {2: "Don't compare booleans to True with `==`; write `if flag:`.",
       3: "Put spaces around `=` in assignments and none before brackets.",
       4: "Import one module per line."},
      "Compare with None using `is`, and write default parameters with no spaces around `=`.",
      "Syllabus 2.1.5 · PEP 8", ["pep8", "style"]),

    Q("b2-044", "2.1.5", 2,
      "Which import block follows PEP 8?",
      ["import json\nimport os\n\nimport pandas as pd\n\nfrom cleaning import fix_dates",
       "import pandas as pd, json, os\nfrom cleaning import fix_dates",
       "from cleaning import fix_dates\nimport pandas as pd\nimport json\nimport os",
       "from pandas import *\nfrom json import *\nfrom cleaning import *"],
      0,
      {1: "PEP 8 wants one module per import line.",
       2: "Groups should run standard library, third-party, then local, separated by blank lines.",
       3: "Wildcard imports hide where names come from."},
      "Standard library first, then third-party, then local modules, each group separated by a blank line, one import per line.",
      "Syllabus 2.1.5 · PEP 8", ["pep8", "imports"]),

    Q("b2-045", "2.1.5", 3,
      "This script runs correctly. Which three things in it break PEP 8? Select three.",
      ["`import os, sys` on one line",
       "Only one blank line between `MAX_ROWS = 500` and `def load_rows`",
       "`if limit == None:`",
       "`MAX_ROWS` written in upper case",
       "No spaces around `=` in `limit=MAX_ROWS`",
       "`load_rows` written in snake_case"],
      [0, 1, 2],
      {3: "Module-level constants are written in UPPER_CASE_WITH_UNDERSCORES.",
       4: "PEP 8 asks for no spaces around `=` in an unannotated default value.",
       5: "Function names are lowercase with underscores."},
      "PEP 8 wants one import per line, two blank lines around top-level function and class definitions, and `is None` rather than `== None`. The constant's case, the default-value spacing and the function name are all correct.",
      "Syllabus 2.1.5 · PEP 8", ["pep8", "style"],
      code="""
      import os, sys

      MAX_ROWS = 500

      def load_rows(path, limit=MAX_ROWS):
          if limit == None:
              limit = MAX_ROWS
          with open(path) as f:
              return f.read().splitlines()[:limit]
      """, verify="runs"),

    Q("b2-046", "2.1.5", 3,
      "Which two docstrings follow PEP 257? Select two.",
      ['"""Return the share of orders that were refunded."""',
       '"""Summarize sales by region.\n\nGroup the rows by region and return a DataFrame with the\ntotal and the order count for each.\n"""',
       '"""returns the share of orders that were refunded"""',
       "'''Summarize sales by region.'''",
       '"""share_refunded(orders) -> float"""'],
      [0, 1],
      {2: "The summary should be a command (\"Return\", not \"returns\"), start with a capital and end with a period.",
       3: "PEP 257 asks for triple double quotes, `\"\"\"`.",
       4: "A docstring shouldn't just repeat the signature; say what the function does."},
      "A one-line docstring is a command ending in a period, on one line. A multi-line docstring has a summary line, a blank line, the details, and the closing quotes on a line of their own.",
      "Syllabus 2.1.5 · PEP 257", ["pep257", "docstring"], optlang="text"),

    Q("b2-047", "2.1.5", 2,
      "Which two lines follow PEP 8's whitespace rules? Select two.",
      ["`total = price * qty`",
       "`items = [1, 2, 3]`",
       "`x=compute( a,b )`",
       "`print (total)`",
       "`def f(a, b = 2):`"],
      [0, 1],
      {2: "PEP 8 wants spaces around `=` and after commas, and none just inside brackets.",
       3: "No space goes between a function name and its opening bracket.",
       4: "A default value in a definition takes no spaces around `=`: `b=2`."},
      "Put single spaces around assignment and binary operators and after commas; put none just inside brackets, before a call's bracket, or around `=` in default values and keyword arguments.",
      "Syllabus 2.1.5 · PEP 8", ["pep8", "whitespace"]),

    # ---------- 2.2.1 Modules and pip ----------
    Q("b2-050", "2.2.1", 1,
      "After `from statistics import mean`, which line works?",
      ["`mean([1, 2, 3])`", "`statistics.mean([1, 2, 3])`", "`math.mean([1, 2, 3])`", "`stats.mean([1, 2, 3])`"],
      0,
      {1: "Only the name `mean` was imported; `statistics` itself isn't defined.",
       2: "`math` isn't imported and has no `mean`.",
       3: "No alias `stats` was created."},
      "A selective import binds only the imported name, so `mean` is used directly.",
      "Syllabus 2.2.1", ["imports", "selective-import"]),

    Q("b2-051", "2.2.1", 1,
      "Which command upgrades pandas to the latest version?",
      ["`pip install --upgrade pandas`", "`pip update pandas`", "`pip upgrade pandas`", "`pip install pandas --latest`"],
      0,
      {1: "pip has no `update` command.",
       2: "pip has no `upgrade` command either; it's an option of `install`.",
       3: "There is no `--latest` option."},
      "Upgrading is `pip install --upgrade pandas` (or `-U`).",
      "Syllabus 2.2.1 · pip docs", ["pip", "packages"]),

    Q("b2-052", "2.2.1", 2,
      "A project has `analysis.py` and a folder `helpers/` containing `cleaning.py`, which defines `fix_dates`. Which line in `analysis.py` imports the function?",
      ["`from helpers.cleaning import fix_dates`", "`import fix_dates from helpers.cleaning`", "`from cleaning.helpers import fix_dates`", "`import helpers/cleaning`"],
      0,
      {1: "That's JavaScript syntax, not Python.",
       2: "The package (`helpers`) comes before the module (`cleaning`).",
       3: "Imports use dots, not slashes."},
      "Packages and modules are separated by dots: `from package.module import name`.",
      "Syllabus 2.2.1", ["imports", "local-modules"]),

    Q("b2-053", "2.2.1", 2,
      "`utils.py` ends with `if __name__ == \"__main__\": run_tests()`. What happens when another script runs `import utils`?",
      ["`run_tests()` is not called", "`run_tests()` is called once", "An ImportError is raised", "`run_tests()` is called every time a function from utils is used"],
      0,
      {1: "When imported, the module's `__name__` is \"utils\", so the guarded block is skipped.",
       2: "The guard is valid Python; importing works.",
       3: "Module code runs once, at import; the guarded block not at all."},
      "`__name__` equals \"__main__\" only when the file is run directly. On import it is the module's name, so the guarded code doesn't run.",
      "Syllabus 2.2.1 · Python docs: __main__", ["modules", "main-guard"]),

    Q("b2-054", "2.2.1", 1,
      "Which two modules ship with Python and need no pip install? Select two.",
      ["`json`", "`sqlite3`", "`numpy`", "`requests`", "`seaborn`"],
      [0, 1],
      {2: "NumPy is a third-party package.",
       3: "requests is a third-party package.",
       4: "Seaborn is a third-party package."},
      "json and sqlite3 are part of the standard library.",
      "Syllabus 2.2.1", ["standard-library", "modules"]),

    Q("b2-055", "2.2.1", 2,
      "In a newly created virtual environment, `import pymysql` raises ModuleNotFoundError. What fixes it?",
      ["Run `pip install pymysql` with that environment active",
       "Rename the script to `pymysql.py`",
       "Change the line to `import PyMySQL`",
       "Change the line to `from pymysql import *`"],
      0,
      {1: "Naming your file after a package shadows the real package: it causes errors rather than fixing them.",
       2: "The import name is lowercase `pymysql`; the problem is that it isn't installed.",
       3: "A wildcard import still needs the package installed."},
      "Each virtual environment has its own packages; install the driver into the active environment.",
      "Syllabus 2.2.1", ["pip", "virtual-environments"]),

    Q("b2-056", "2.2.1", 2,
      "What does this code print?",
      ["`6.0`", "`6`", "`5.0`", "A NameError is raised"],
      0,
      {1: "`sqrt` returns a float, so the sum is a float.",
       2: "`floor(2.7)` is 2 and `sqrt(16)` is 4.0.",
       3: "Both aliases `m` and `root` are defined by the imports."},
      "`m` is an alias for math and `root` for `math.sqrt`: 2 + 4.0 = 6.0.",
      "Syllabus 2.2.1", ["imports", "aliasing"],
      code="""
      import math as m
      from math import sqrt as root

      print(m.floor(2.7) + root(16))
      """, verify="stdout"),

    Q("b2-057", "2.2.1", 3,
      "A project folder holds the two files below. What happens when `python analysis.py` is run?",
      ["An AttributeError is raised: `import statistics` loads the local statistics.py, which has no `mean`",
       "It prints `3`, because the standard library always takes priority",
       "An ImportError is raised, because two modules share a name",
       "Python combines both modules, so it prints `3`"],
      0,
      {1: "The script's own folder comes first on `sys.path`, so the local file wins over the standard library.",
       2: "There is no name-clash error: Python simply imports the first `statistics` it finds.",
       3: "Python imports one module per name; it never combines files."},
      "Python searches the script's folder before the standard library, so a local file named after a standard module hides it. Don't name your own files `statistics.py`, `random.py`, `csv.py` and so on.",
      "Syllabus 2.2.1 · Python docs (sys.path)", ["imports", "sys-path"],
      code="""
      # statistics.py (written by the analyst)
      def summarize(values):
          return min(values), max(values)

      # analysis.py
      import statistics
      print(statistics.mean([2, 4]))
      """,
      verify={"py": """
      import os, subprocess, sys, tempfile
      folder = tempfile.mkdtemp()
      with open(os.path.join(folder, "statistics.py"), "w") as f:
          f.write("def summarize(values):\\n    return min(values), max(values)\\n")
      with open(os.path.join(folder, "analysis.py"), "w") as f:
          f.write("import statistics\\nprint(statistics.mean([2, 4]))\\n")
      env = {k: v for k, v in os.environ.items() if k != "PYTHONSAFEPATH"}
      r = subprocess.run([sys.executable, "analysis.py"], cwd=folder, capture_output=True, text=True, env=env)
      assert "AttributeError" in r.stderr and "mean" in r.stderr, r.stderr
      """}),

    Q("b2-058", "2.2.1", 3,
      "What does this code print?",
      ["`2025-02-03 05 Mar 0`", "`2025-03-02 01 Apr 6`", "`2025-02-03 05 Mar 1`", "`2025-02-03 5 March 0`"],
      0,
      {1: "`%d/%m/%Y` reads the first number as the day, so the date is 3 February, not 2 March.",
       2: "`weekday()` counts Monday as 0; `isoweekday()` is the one that counts Monday as 1.",
       3: "`%d` pads the day to two digits and `%b` is the short month name."},
      "`strptime` with `%d/%m/%Y` parses 3 February 2025, a Monday (`weekday()` 0). `strftime(\"%Y-%m-%d\")` writes it in ISO form, and 30 days later is 5 March, written as \"05 Mar\".",
      "Syllabus 2.2.1 · Python docs (datetime)", ["datetime", "strptime", "strftime"],
      code="""
      from datetime import datetime, timedelta

      d = datetime.strptime("03/02/2025", "%d/%m/%Y")
      print(d.strftime("%Y-%m-%d"), (d + timedelta(days=30)).strftime("%d %b"), d.weekday())
      """, verify="stdout"),

    Q("b2-059", "2.2.1", 2,
      "What does this code print?",
      ["`['c', 'd']`", "`['a', 'b', 'c', 'd']`", "`['d']`", "`['c']`"],
      0,
      {1: "The second `\"w\"` open empties the file, wiping a and b.",
       2: "`\"a\"` adds to what is already there, so c stays.",
       3: "The last `\"a\"` open adds d after c."},
      "\"w\" creates the file or empties it before writing; \"a\" appends. The second \"w\" erases a and b, leaving c, and the final append adds d.",
      "Syllabus 2.2.1, 1.4.1 · Python docs (open)", ["files", "open", "file-modes"],
      code="""
      import os
      import tempfile

      path = os.path.join(tempfile.gettempdir(), "log.txt")
      with open(path, "w") as f:
          f.write("a\\n")
      with open(path, "a") as f:
          f.write("b\\n")
      with open(path, "w") as f:
          f.write("c\\n")
      with open(path, "a") as f:
          f.write("d\\n")
      with open(path) as f:
          print(f.read().split())
      """, verify="stdout"),

    Q("b2-175", "2.2.1", 1,
      "Which line turns the text \"2025-07-15\" into a `datetime` object? (`datetime` was imported with `from datetime import datetime`.)",
      ["`datetime.strptime(\"2025-07-15\", \"%Y-%m-%d\")`",
       "`datetime.strftime(\"2025-07-15\", \"%Y-%m-%d\")`",
       "`datetime.strptime(\"2025-07-15\", \"%d-%m-%Y\")`",
       "`\"2025-07-15\".date()`"],
      0,
      {1: "`strftime` formats an existing datetime as text; it can't parse a string.",
       2: "The codes must follow the text's order; \"2025\" isn't a valid day, so this raises ValueError.",
       3: "Strings have no `.date()` method."},
      "`strptime` (\"parse\") reads text using format codes that match it exactly; `strftime` (\"format\") goes the other way.",
      "Syllabus 2.2.1 · Python docs (datetime)", ["datetime", "strptime"],
      verify={"py": """
      from datetime import datetime
      assert eval(opt(0)) == datetime(2025, 7, 15)
      for i in (1, 2, 3):
          try:
              eval(opt(i))
              raise AssertionError(f"option {i} ran")
          except (TypeError, ValueError, AttributeError):
              pass
      """}),

    # ---------- 2.2.2 Exceptions ----------
    Q("b2-060", "2.2.2", 3,
      "What does this code print?",
      ["`ok done bad done 12 None`", "`ok done 12 bad done None`", "`ok bad done 12 None`", "`ok done bad 12 None`"],
      0,
      {1: "Both `parse` calls run before `print` shows their return values.",
       2: "`finally` runs on every call, including the first.",
       3: "`finally` runs after the `except` branch returns too."},
      "Arguments are evaluated first: parse(\"12\") prints \"ok done\", parse(\"x\") prints \"bad done\"; then print shows 12 and None. `finally` runs even when a `return` happens in `else` or `except`.",
      "Syllabus 2.2.2 · Python docs: try statement", ["exceptions", "finally"],
      code="""
      def parse(text):
          try:
              value = int(text)
          except ValueError:
              print("bad", end=" ")
              return None
          else:
              print("ok", end=" ")
              return value
          finally:
              print("done", end=" ")

      print(parse("12"), parse("x"))
      """, verify="stdout"),

    Q("b2-061", "2.2.2", 1,
      "Which exception does this code raise?",
      ["KeyError", "IndexError", "ValueError", "NameError"],
      0,
      {1: "IndexError is for sequence positions.",
       2: "ValueError is for a bad value of the right type.",
       3: "`prices` is defined; the missing thing is the key."},
      "Looking up a missing dict key with square brackets raises KeyError.",
      "Syllabus 2.2.2", ["exceptions", "keyerror"],
      code="""
      prices = {"tea": 2.5}
      print(prices["coffee"])
      """, verify="raises:KeyError"),

    Q("b2-062", "2.2.2", 2,
      "What does this code print?",
      ["`general`", "`index`", "general\nindex", "Nothing; an IndexError escapes"],
      0,
      {1: "The first matching clause wins, and `Exception` matches first.",
       2: "Only one `except` clause runs.",
       3: "The exception is handled by the first clause."},
      "`except` clauses are checked in order; IndexError is a subclass of Exception, so the general clause catches it and the specific clause never runs.",
      "Syllabus 2.2.2", ["exceptions", "order"],
      code="""
      try:
          [1, 2, 3][5]
      except Exception:
          print("general")
      except IndexError:
          print("index")
      """, optlang="text", verify="stdout"),

    Q("b2-063", "2.2.2", 1,
      "Which exception does this line raise?",
      ["TypeError", "ValueError", "SyntaxError", "AttributeError"],
      0,
      {1: "The values are fine; the operation isn't defined for this pair of types.",
       2: "The line is syntactically valid.",
       3: "No attribute is being accessed."},
      "`+` can't combine str and int: TypeError: can only concatenate str (not \"int\") to str.",
      "Syllabus 2.2.2", ["exceptions", "typeerror"],
      code="""
      total = "3" + 4
      """, verify="raises:TypeError"),

    Q("b2-064", "2.2.2", 3,
      "What does this code print?",
      ["`141`", "`41`", "`40`", "A TypeError is raised"],
      0,
      {1: "`int(None)` raises TypeError, handled by the second clause (+100).",
       2: "\"x\" isn't skipped; its ValueError adds 1.",
       3: "The TypeError from None is caught by the second `except`."},
      "10 and 30 convert; \"x\" raises ValueError (+1); None raises TypeError (+100). 10 + 1 + 30 + 100 = 141.",
      "Syllabus 2.2.2", ["exceptions", "valueerror"],
      code="""
      values = ["10", "x", "30", None]
      total = 0
      for v in values:
          try:
              total += int(v)
          except ValueError:
              total += 1
          except TypeError:
              total += 100
      print(total)
      """, verify="stdout"),

    Q("b2-065", "2.2.2", 2,
      "A report script stops with this traceback. What should be fixed?",
      ["`df` has no column named 'orders'; fix the column name used on line 7 of report.py (or the data)",
       "pandas has a bug on line 4102 of frame.py",
       "The code divides by zero",
       "Line 12 of report.py has a syntax error"],
      0,
      {1: "The frame inside pandas is where the lookup failed, not the cause; the bad key came from your code.",
       2: "The exception is a KeyError, not ZeroDivisionError.",
       3: "A syntax error would stop the script before anything runs, with a SyntaxError."},
      "Read from the bottom: KeyError: 'orders' means the column is missing. The last frame in your own code, report.py line 7, is where to fix it.",
      "Syllabus 2.2.2", ["tracebacks", "debugging"],
      code="""
      Traceback (most recent call last):
        File "report.py", line 12, in <module>
          summary = build_summary(df)
        File "report.py", line 7, in build_summary
          return df["revenue"].sum() / df["orders"].sum()
        File ".../pandas/core/frame.py", line 4102, in __getitem__
          indexer = self.columns.get_loc(key)
      KeyError: 'orders'
      """, lang="text"),

    Q("b2-066", "2.2.2", 2,
      "Which two statements about `finally` are true? Select two.",
      ["It runs even when the `try` block executes a `return`",
       "It runs even when an exception is not caught by any `except` clause",
       "It runs only when no exception occurred",
       "It replaces the need for `except` clauses",
       "It runs before the `try` block"],
      [0, 1],
      {2: "That describes `else`.",
       3: "`finally` doesn't handle exceptions; an uncaught one still propagates afterwards.",
       4: "It runs last, after try/except/else."},
      "`finally` always runs on the way out of the try statement, making it the place for cleanup such as closing files or connections.",
      "Syllabus 2.2.2", ["exceptions", "finally"]),

    Q("b2-067", "2.2.2", 3,
      "What does this code print?",
      ["`40 log ValueError DataQualityError type`",
       "`40 log ValueError DataQualityError ValueError`",
       "`40 ValueError DataQualityError type`",
       "`40 log ValueError 150 type`"],
      0,
      {1: "`int(None)` raises TypeError, which the inner `except ValueError` doesn't catch; the caller's `except TypeError` prints \"type\".",
       2: "The inner handler prints \"log\" before the bare `raise` passes the same ValueError on to the caller.",
       3: "150 passes `int()` but fails the `age > 120` check, which raises DataQualityError."},
      "\"40\" parses. \"abc\" raises ValueError: the inner handler logs it and re-raises it, and the caller prints its name. \"150\" raises the custom DataQualityError, caught by the tuple. `int(None)` raises TypeError, which skips the inner handler and the tuple and lands in `except TypeError`.",
      "Syllabus 2.2.2 · Python docs", ["exceptions", "re-raise", "custom-exception"],
      code="""
      class DataQualityError(Exception):
          pass

      def parse_age(text):
          try:
              age = int(text)
          except ValueError:
              print("log", end=" ")
              raise
          if age > 120:
              raise DataQualityError(age)
          return age

      for t in ["40", "abc", "150", None]:
          try:
              print(parse_age(t), end=" ")
          except (ValueError, DataQualityError) as e:
              print(type(e).__name__, end=" ")
          except TypeError:
              print("type", end=" ")
      print()
      """, verify="stdout"),

    Q("b2-068", "2.2.2", 2,
      "What does this code print?",
      ["`[0.25, 'whole must be positive']`", "`[0.25, 'zero']`", "`[0.25]`", "An AssertionError escapes and nothing is printed"],
      0,
      {1: "The assert runs before the division, so the division by zero is never reached.",
       2: "The second call's error is caught and its message appended, so the list has two items.",
       3: "The `except AssertionError as e` clause catches it."},
      "For (2, 0) the `assert whole > 0` fails first and raises AssertionError with its message, which the second `except` clause catches and stores.",
      "Syllabus 2.2.2 · Python docs (assert)", ["assert", "exceptions"],
      code="""
      def share(part, whole):
          assert whole > 0, "whole must be positive"
          return round(part / whole, 2)

      results = []
      for p, w in [(1, 4), (2, 0)]:
          try:
              results.append(share(p, w))
          except ZeroDivisionError:
              results.append("zero")
          except AssertionError as e:
              results.append(str(e))
      print(results)
      """, verify="stdout"),

    # ---------- 2.3.1 Classes ----------
    Q("b2-070", "2.3.1", 2,
      "What does this code print?",
      ["`5 0 2`", "`5 5 2`", "`5 0 1`", "`5 0 0`"],
      0,
      {1: "`count` is an instance variable, so each object has its own.",
       2: "The constructor ran twice, once per object.",
       3: "`Counter.total += 1` updates the shared class variable in each constructor call."},
      "Each instance has its own `count`; `total` is a class variable incremented by both constructors.",
      "Syllabus 2.3.1", ["classes", "class-variables"],
      code="""
      class Counter:
          total = 0

          def __init__(self):
              self.count = 0
              Counter.total += 1

      a = Counter()
      b = Counter()
      a.count += 5
      print(a.count, b.count, Counter.total)
      """, verify="stdout"),

    Q("b2-071", "2.3.1", 2,
      "What happens when this code runs?",
      ["An AttributeError is raised", "It prints `100`", "It prints `None`", "A SyntaxError is raised"],
      0,
      {1: "The attribute was stored under the mangled name `_Account__balance`.",
       2: "Python raises an error for a missing attribute rather than returning None.",
       3: "The syntax is valid; the error happens at run time."},
      "Inside the class, `__balance` is name-mangled to `_Account__balance`, so `acct.__balance` from outside doesn't exist: AttributeError.",
      "Syllabus 2.3.1 · Python docs: private variables", ["classes", "name-mangling"],
      code="""
      class Account:
          def __init__(self, balance):
              self.__balance = balance

      acct = Account(100)
      print(acct.__balance)
      """, verify="raises:AttributeError"),

    Q("b2-072", "2.3.1", 2,
      "What does this code print?",
      ["`Ana 100`", "An AttributeError is raised for `_owner`", "An AttributeError is raised for `_Account__balance`", "`None 100`"],
      0,
      {1: "A single underscore is only a convention; the attribute is fully accessible.",
       2: "`_Account__balance` is exactly the mangled name, so it works.",
       3: "`_owner` holds \"Ana\"."},
      "`_owner` is \"protected\" by convention only; `__balance` is stored as `_Account__balance`, which can still be reached by that name.",
      "Syllabus 2.3.1", ["classes", "encapsulation"],
      code="""
      class Account:
          def __init__(self, balance):
              self._owner = "Ana"
              self.__balance = balance

      acct = Account(100)
      print(acct._owner, acct._Account__balance)
      """, verify="stdout"),

    Q("b2-073", "2.3.1", 3,
      "What does this code print?",
      ["`10.0`", "`-1`", "`9.999`", "A ValueError is raised"],
      0,
      {1: "The setter raises before storing −1, so the old value remains.",
       2: "The setter rounds to two decimals when storing: 9.999 → 10.0.",
       3: "The ValueError is caught by the try/except."},
      "The constructor's `self.price = price` goes through the setter, storing round(9.999, 2) = 10.0. Setting −1 raises ValueError before assignment, which is caught, so 10.0 stays.",
      "Syllabus 2.3.1 · Python docs: property", ["classes", "property"],
      code="""
      class Product:
          def __init__(self, price):
              self.price = price

          @property
          def price(self):
              return self._price

          @price.setter
          def price(self, value):
              if value < 0:
                  raise ValueError("negative")
              self._price = round(value, 2)

      p = Product(9.999)
      try:
          p.price = -1
      except ValueError:
          pass
      print(p.price)
      """, verify="stdout"),

    Q("b2-074", "2.3.1", 1,
      "What does a class's `__init__` method do?",
      ["It runs when a new object is created and sets up its initial attributes",
       "It deletes the object when it's no longer used",
       "It defines how two objects are compared with ==",
       "It returns a string shown by print()"],
      0,
      {1: "Cleanup at deletion is `__del__`, rarely used.",
       2: "Equality is `__eq__`.",
       3: "The print string comes from `__str__`."},
      "`__init__` is the constructor: calling `ClassName(...)` creates the object and runs `__init__` with it as `self`.",
      "Syllabus 2.3.1", ["classes", "constructor"]),

    Q("b2-075", "2.3.1", 3,
      "What does this code print?",
      ["`USD GBP`", "`GBP GBP`", "`USD EUR`", "`USD USD`"],
      0,
      {1: "`a.currency = \"USD\"` created an instance attribute on `a`, which shadows the class attribute.",
       2: "`b` has no instance attribute, so it sees the updated class value.",
       3: "Assigning on `a` doesn't touch `b` or the class."},
      "`a` has its own `currency` (USD). `b` has none, so it reads the class attribute, now GBP.",
      "Syllabus 2.3.1", ["classes", "attributes"],
      code="""
      class Config:
          currency = "EUR"

      a = Config()
      b = Config()
      a.currency = "USD"
      Config.currency = "GBP"
      print(a.currency, b.currency)
      """, verify="stdout"),

    Q("b2-076", "2.3.1", 2,
      "Why route changes to an account's balance through a `set_balance()` method instead of assigning the attribute directly?",
      ["The method can validate new values (e.g. reject negatives) before the object's state changes",
       "Methods run faster than attribute assignment",
       "It makes the attribute impossible to read",
       "Python forbids assigning attributes from outside a class"],
      0,
      {1: "Speed isn't the point; a method call is slightly slower.",
       2: "A setter controls writes; reading is usually through a getter.",
       3: "Python allows it; encapsulation is a design choice."},
      "Setters (or properties) encapsulate state: every change passes through one place that enforces the rules.",
      "Syllabus 2.3.1", ["encapsulation", "setters"]),

    Q("b2-077", "2.3.1", 3,
      "What does this code print?",
      ["`A1 @ 2.50 [Sku(code='A1', price=2.5)] True False`",
       "`A1 @ 2.50 [A1 @ 2.50] True False`",
       "`Sku(code='A1', price=2.5) [Sku(code='A1', price=2.5)] True False`",
       "`A1 @ 2.50 [Sku(code='A1', price=2.5)] False False`"],
      0,
      {1: "A list shows its items with `__repr__`, not `__str__`.",
       2: "`print(a)` uses the class's own `__str__`.",
       3: "`@dataclass` writes an `__eq__` that compares the fields, so two objects with the same code and price are equal."},
      "`print` uses `__str__` (written by hand here); a list displays its items with `__repr__`, which `@dataclass` generated. The generated `__eq__` compares fields, so `==` is True, while `is` asks whether they are the same object: False.",
      "Syllabus 2.3.1, 2.3.3 · Python docs (dataclasses)", ["dataclass", "repr", "str"],
      code="""
      from dataclasses import dataclass

      @dataclass
      class Sku:
          code: str
          price: float

          def __str__(self):
              return f"{self.code} @ {self.price:.2f}"

      a = Sku("A1", 2.5)
      print(a, [a], a == Sku("A1", 2.5), a is Sku("A1", 2.5))
      """, verify="stdout"),

    # ---------- 2.3.2 Inheritance, composition, polymorphism ----------
    Q("b2-080", "2.3.2", 2,
      "What does this code print?",
      ["Report\nSales Report", "Report\nSales", "Report\nReport", "Sales Report\nSales Report"],
      0,
      {1: "`super().title()` returns \"Report\", which is appended.",
       2: "`SalesReport` overrides `title`, so its version runs for that object.",
       3: "The first object is a plain `Report`."},
      "Each object runs its own `title`; the override extends the parent's result via `super()`.",
      "Syllabus 2.3.2", ["inheritance", "super"],
      code="""
      class Report:
          def title(self):
              return "Report"

      class SalesReport(Report):
          def title(self):
              return "Sales " + super().title()

      for r in [Report(), SalesReport()]:
          print(r.title())
      """, optlang="text", verify="stdout"),

    Q("b2-081", "2.3.2", 3,
      "What happens when this code runs?",
      ["An AttributeError is raised", "It prints `3`", "It prints `0`", "A TypeError is raised"],
      0,
      {1: "`self.rows` was never set, because the parent constructor never ran.",
       2: "Nothing sets rows to an empty value.",
       3: "The constructor call matches the subclass signature, so no TypeError."},
      "The subclass overrides `__init__` without calling `super().__init__(rows)`, so `self.rows` doesn't exist and `size()` fails: 'LabeledDataset' object has no attribute 'rows'.",
      "Syllabus 2.3.2", ["inheritance", "super"],
      code="""
      class Dataset:
          def __init__(self, rows):
              self.rows = rows

          def size(self):
              return len(self.rows)

      class LabeledDataset(Dataset):
          def __init__(self, rows, label):
              self.label = label

      d = LabeledDataset([1, 2, 3], "train")
      print(d.size())
      """, verify="raises:AttributeError"),

    Q("b2-082", "2.3.2", 2,
      "What does this code print?",
      ["`'OK'`", "`'  OK '`", "`'ok'`", "`'  ok '`"],
      0,
      {1: "Strip runs first, removing the spaces.",
       2: "Upper runs second, and the base Cleaner returns its input unchanged.",
       3: "Both Strip and Upper change the value."},
      "Polymorphism: each object's `process` runs in turn. Strip → \"ok\", Upper → \"OK\", and the base Cleaner passes it through.",
      "Syllabus 2.3.2", ["polymorphism", "overriding"],
      code="""
      class Cleaner:
          def process(self, x):
              return x

      class Upper(Cleaner):
          def process(self, x):
              return x.upper()

      class Strip(Cleaner):
          def process(self, x):
              return x.strip()

      value = "  ok "
      for step in [Strip(), Upper(), Cleaner()]:
          value = step.process(value)
      print(repr(value))
      """, verify="stdout"),

    Q("b2-083", "2.3.2", 2,
      "An `Invoice` needs a customer and a list of line items. Which design fits best?",
      ["`Invoice` stores a `Customer` object and a list of `LineItem` objects as attributes (composition)",
       "`Invoice` inherits from `Customer`",
       "`LineItem` inherits from `Invoice`",
       "`Invoice` inherits from both `list` and `Customer`"],
      0,
      {1: "An invoice is not a kind of customer; it has one.",
       2: "A line item is not a kind of invoice; it's a part of one.",
       3: "Multiple inheritance here would model \"is-a\" relationships that don't exist."},
      "\"Has-a\" relationships are modeled with composition: the invoice holds its parts as attributes.",
      "Syllabus 2.3.2", ["composition", "design"]),

    Q("b2-084", "2.3.2", 2,
      "What does this code print?",
      ["`True False True`", "`True True True`", "`False False True`", "`True False False`"],
      0,
      {1: "A plain Exporter is not a CsvExporter.",
       2: "An instance of a subclass is also an instance of its parent.",
       3: "CsvExporter is declared as a subclass of Exporter."},
      "A CsvExporter is an Exporter (True); a base Exporter isn't a CsvExporter (False); `issubclass` confirms the relationship (True).",
      "Syllabus 2.3.2", ["inheritance", "isinstance"],
      code="""
      class Exporter:
          pass

      class CsvExporter(Exporter):
          pass

      e = CsvExporter()
      print(isinstance(e, Exporter), isinstance(Exporter(), CsvExporter), issubclass(CsvExporter, Exporter))
      """, verify="stdout"),

    Q("b2-085", "2.3.2", 2,
      "Which two statements describe polymorphism? Select two.",
      ["Different classes implement a method with the same name",
       "Code can call `obj.export()` without knowing the object's concrete class",
       "A class may have only one parent class",
       "Attributes starting with `__` are private",
       "A subclass copies its parent's source code"],
      [0, 1],
      {2: "Python allows multiple inheritance; this is unrelated anyway.",
       3: "That's name mangling, an encapsulation topic.",
       4: "Subclasses inherit behaviour; nothing is copied."},
      "Polymorphism means one interface, many implementations: callers use the shared method name and each class supplies its own behaviour.",
      "Syllabus 2.3.2", ["polymorphism", "definitions"]),

    Q("b2-086", "2.3.2", 3,
      "What does this code print?",
      ["saved q1.txt\nsaved q1.csv\nsaved q1.csv.gz",
       "saved q1.txt\nsaved q1.txt\nsaved q1.txt.gz",
       "saved q1.txt\nsaved q1.csv\nsaved q1.csv",
       "saved q1.txt\nsaved q1.csv\nsaved q1.txt.gz"],
      0,
      {1: "`self.ext` is looked up on the object's own class first, and CsvExporter overrides it with \"csv\".",
       2: "GzipCsvExporter overrides `filename`, so its version runs and adds \".gz\".",
       3: "`super().filename(name)` runs the inherited method, but `self` is still the GzipCsvExporter, so `self.ext` is \"csv\"."},
      "`export` is written once in the base class and calls `self.filename`, which dispatches to each object's own version. CsvExporter only overrides the class attribute `ext`; GzipCsvExporter overrides `filename` and extends the inherited result with `super()`.",
      "Syllabus 2.3.2 · Python docs", ["inheritance", "super", "polymorphism"], optlang="text",
      code="""
      class Exporter:
          ext = "txt"

          def filename(self, name):
              return f"{name}.{self.ext}"

          def export(self, name):
              return "saved " + self.filename(name)

      class CsvExporter(Exporter):
          ext = "csv"

      class GzipCsvExporter(CsvExporter):
          def filename(self, name):
              return super().filename(name) + ".gz"

      for e in [Exporter(), CsvExporter(), GzipCsvExporter()]:
          print(e.export("q1"))
      """, verify="stdout"),

    Q("b2-087", "2.3.2", 2,
      "Which two relationships are better modeled with composition than with inheritance? Select two.",
      ["A `Report` that contains several `Chart` objects",
       "A survey `Response` that holds the `Respondent` who gave it",
       "A `CsvExporter` that is a kind of `Exporter`",
       "A `SalesReport` that is a specialized `Report`",
       "A `MonthlyForecast` that is a kind of `Forecast`"],
      [0, 1],
      {2: "\"Is a kind of\" is the test for inheritance.",
       3: "A specialized report is a report: inheritance.",
       4: "A monthly forecast is a forecast: inheritance."},
      "Use composition for \"has-a\" relationships, where one object holds others as attributes, and inheritance for \"is-a\" relationships.",
      "Syllabus 2.3.2", ["composition", "inheritance"]),

    # ---------- 2.3.3 Identity and comparison ----------
    Q("b2-090", "2.3.3", 2,
      "What does this code print?",
      ["`2 1 True False`", "`1 1 True True`", "`2 2 True True`", "`2 1 False False`"],
      0,
      {1: "`b` is the same dict as `a`, so adding \"y\" through `b` changes `a`.",
       2: "`c` is an independent copy made before the change.",
       3: "`a is b` is True: one object, two names."},
      "`b = a` aliases the dict; `dict(a)` copies it. After `b[\"y\"] = 2`, `a` has 2 keys, `c` still 1, so they're no longer equal.",
      "Syllabus 2.3.3", ["identity", "aliasing"],
      code="""
      a = {"x": 1}
      b = a
      c = dict(a)
      b["y"] = 2
      print(len(a), len(c), a is b, a == c)
      """, verify="stdout"),

    Q("b2-091", "2.3.3", 3,
      "What does this code print?",
      ["`[1, 2, 99] [1, 2]`", "`[1, 2] [1, 2]`", "`[1, 2, 99] [1, 2, 99]`", "`[1, 2] [1, 2, 99]`"],
      0,
      {1: "A shallow copy shares the inner lists, so the append shows up in `shallow`.",
       2: "`deepcopy` copied the inner lists too, so `deep` is unaffected.",
       3: "This reverses shallow and deep."},
      "`orig.copy()` makes a new outer list whose items are the same inner lists; `deepcopy` duplicates the inner lists as well.",
      "Syllabus 2.3.3 · Python docs: copy", ["copy", "deepcopy"],
      code="""
      import copy

      orig = [[1, 2], [3]]
      shallow = orig.copy()
      deep = copy.deepcopy(orig)
      orig[0].append(99)
      print(shallow[0], deep[0])
      """, verify="stdout"),

    Q("b2-092", "2.3.3", 2,
      "What does this code print?",
      ["`False True False`", "`True True False`", "`False True True`", "`True True True`"],
      0,
      {1: "Without `__eq__`, two separate Sku objects compare by identity, so they're not equal.",
       2: "Two separately created objects are never the same object.",
       3: "Only Sku2 compares by content."},
      "The base class compares by identity (False); Sku2's `__eq__` compares codes (True); `is` checks identity, and they are two objects (False).",
      "Syllabus 2.3.3", ["equality", "eq"],
      code="""
      class Sku:
          def __init__(self, code):
              self.code = code

      class Sku2(Sku):
          def __eq__(self, other):
              return isinstance(other, Sku2) and self.code == other.code

      print(Sku("A1") == Sku("A1"), Sku2("A1") == Sku2("A1"), Sku2("A1") is Sku2("A1"))
      """, verify="stdout"),

    Q("b2-093", "2.3.3", 1,
      "Which is the recommended way to test whether `result` holds no value?",
      ["`if result is None:`", "`if result == None:`", "`if result is \"None\":`", "`if type(result) == None:`"],
      0,
      {1: "It usually works, but PEP 8 says to compare singletons with `is`, and a custom `__eq__` can make it misbehave.",
       2: "That compares with the string \"None\", which is a different object.",
       3: "`type(result)` is a class, never None."},
      "None is a singleton, so identity (`is`) is the correct and idiomatic test.",
      "Syllabus 2.3.3, 2.1.5", ["identity", "none"]),

    Q("b2-094", "2.3.3", 2,
      "What does this code print?",
      ["`[10, 20] [1, 2]`", "`[1, 2] [1, 2]`", "`[10, 20] [10, 20]`", "`[1, 2] [10, 20]`"],
      0,
      {1: "`view = df` binds a second name to the same DataFrame, so the change is visible through `df`.",
       2: "`safe` is an independent copy made before the change.",
       3: "This reverses which object changed."},
      "Assignment doesn't copy a DataFrame; `view` and `df` are the same object. `df.copy()` creates an independent one.",
      "Syllabus 2.3.3 · pandas: DataFrame.copy", ["identity", "pandas-copy"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"a": [1, 2]})
      view = df
      safe = df.copy()
      view["a"] = view["a"] * 10
      print(df["a"].tolist(), safe["a"].tolist())
      """, verify="stdout"),

    Q("b2-095", "2.3.3", 3,
      "What does this code print?",
      ["[[0, 5, 0], [0, 5, 0]]\n[[0, 5, 0], [0, 0, 0]]",
       "[[0, 5, 0], [0, 0, 0]]\n[[0, 5, 0], [0, 0, 0]]",
       "[[0, 5, 0], [0, 5, 0]]\n[[0, 5, 0], [0, 5, 0]]",
       "[[0, 5, 0], [0, 0, 0]]\n[[0, 5, 0], [0, 5, 0]]"],
      0,
      {1: "`[row] * 2` repeats a reference to the same inner list, so both rows change together.",
       2: "The comprehension runs `[0] * 3` once per row, creating two separate lists.",
       3: "It's the other way round: the multiplied version shares one list."},
      "`[[0] * 3] * 2` builds one inner list and puts two references to it in the outer list, so changing `grid[0]` also changes `grid[1]`. The comprehension creates a new inner list on each pass, so the rows are independent.",
      "Syllabus 2.3.3 · Python docs", ["references", "aliasing", "lists"], optlang="text",
      code="""
      grid = [[0] * 3] * 2
      grid[0][1] = 5
      print(grid)

      rows = [[0] * 3 for _ in range(2)]
      rows[0][1] = 5
      print(rows)
      """, verify="stdout"),

    Q("b2-096", "2.3.3", 3,
      "What does this code print?",
      ["`['tea', 'jam'] ['tea'] True False`",
       "`['tea'] ['tea'] False True`",
       "`['tea', 'jam'] ['tea', 'jam'] True True`",
       "`['tea', 'jam'] ['tea'] False False`"],
      0,
      {1: "`a` and `b` were both given the same list object, so the append through `a` shows in `b`.",
       2: "`list(shared)` made `c` its own copy before the append.",
       3: "`a.items` and `b.items` are the very same list, so `is` is True."},
      "Storing an argument in `self.items` stores a reference, not a copy. `a` and `b` share one list; `c` got an independent copy, so it still has only \"tea\" and is no longer equal to `a.items`.",
      "Syllabus 2.3.3", ["references", "objects", "copy"],
      code="""
      class Basket:
          def __init__(self, items):
              self.items = items

      shared = ["tea"]
      a = Basket(shared)
      b = Basket(shared)
      c = Basket(list(shared))
      a.items.append("jam")
      print(b.items, c.items, a.items is b.items, a.items == c.items)
      """, verify="stdout"),

    Q("b2-097", "2.3.3", 2,
      "After `a = [1, 2]`, `b = [1, 2]` and `c = a`, which two expressions are True? Select two.",
      ["`a == b`", "`a is c`", "`a is b`", "`a != c`", "`b is c`"],
      [0, 1],
      {2: "`a` and `b` are two separate lists that happen to hold the same values.",
       3: "`c` is the same list as `a`, so they are equal.",
       4: "`c` refers to `a`'s list, not to `b`'s."},
      "`==` compares values, so the two lists holding [1, 2] are equal. `is` compares identity: only `a` and `c` name the same object.",
      "Syllabus 2.3.3", ["identity", "equality"],
      verify={"py": """
      a = [1, 2]
      b = [1, 2]
      c = a
      truths = [i for i in range(5) if eval(opt(i))]
      assert truths == q["answer"], truths
      """}),

    # ---------- 2.4.1 SQL queries ----------
    Q("b2-100", "2.4.1", 2,
      "How many rows does this query return?",
      ["5", "4", "6", "3"],
      0,
      {1: "Dev has no orders but still appears once, with NULL totals.",
       2: "Order 14 belongs to customer 5, who doesn't exist, so a LEFT JOIN from customers never shows it.",
       3: "Ana has two orders, so she appears twice."},
      "A LEFT JOIN keeps every customer: Ana ×2, Ben ×1, Cara ×1 and Dev ×1 (with NULL), so 5 rows.",
      "Syllabus 2.4.1", ["sql", "left-join"],
      code="""
      SELECT c.name, o.total
      FROM customers AS c
      LEFT JOIN orders AS o ON o.customer_id = c.id;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": "assert len(run_sql(setup, code)) == 5"}),

    Q("b2-101", "2.4.1", 2,
      "How many rows does this query return?",
      ["4", "5", "3", "6"],
      0,
      {1: "Order 14 references customer 5, who doesn't exist, so the inner join drops it.",
       2: "Orders 10 to 13 all have matching customers.",
       3: "An inner join never adds rows for unmatched customers such as Dev."},
      "An INNER JOIN keeps only orders with a matching customer: 10, 11, 12 and 13.",
      "Syllabus 2.4.1", ["sql", "inner-join"],
      code="""
      SELECT o.id, c.name
      FROM orders AS o
      JOIN customers AS c ON c.id = o.customer_id;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": "assert len(run_sql(setup, code)) == 4"}),

    Q("b2-102", "2.4.1", 3,
      "What does this query return?",
      ["One row: `('EU', 250.0)`", "Two rows: `('EU', 250.0)` and `('US', 200.0)`", "One row: `('EU', 200.0)`", "No rows"],
      0,
      {1: "Ben's order is refunded, so WHERE removes it before grouping.",
       2: "Cara's paid order (50) also belongs to EU: 120 + 80 + 50.",
       3: "EU's paid total of 250 is above 100."},
      "WHERE keeps paid orders with a customer (Ana 120, Ana 80, Cara 50; order 14 has no customer). Grouped by region: EU = 250. HAVING keeps groups above 100.",
      "Syllabus 2.4.1", ["sql", "having"],
      code="""
      SELECT c.region, SUM(o.total) AS revenue
      FROM orders AS o
      JOIN customers AS c ON c.id = o.customer_id
      WHERE o.status = 'paid'
      GROUP BY c.region
      HAVING SUM(o.total) > 100;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": "assert run_sql(setup, code) == [('EU', 250.0)]"}),

    Q("b2-103", "2.4.1", 2,
      "Which query is invalid?",
      ["`SELECT region, COUNT(*) FROM customers WHERE COUNT(*) > 1 GROUP BY region;`",
       "`SELECT region, COUNT(*) FROM customers GROUP BY region HAVING COUNT(*) > 1;`",
       "`SELECT region, COUNT(*) AS n FROM customers GROUP BY region ORDER BY n DESC;`",
       "`SELECT DISTINCT region FROM customers WHERE name LIKE 'A%';`"],
      0,
      {1: "Conditions on aggregates belong in HAVING: valid.",
       2: "ORDER BY can use a SELECT alias: valid.",
       3: "DISTINCT with a LIKE filter is valid."},
      "WHERE runs before grouping, so it can't use an aggregate such as COUNT(*). Move the condition to HAVING.",
      "Syllabus 2.4.1", ["sql", "where-vs-having"], lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": """
      bad = []
      for i in range(4):
          try:
              run_sql(setup, opt(i))
          except Exception:
              bad.append(i)
      assert bad == q["answer"], bad
      """}),

    Q("b2-104", "2.4.1", 1,
      "Which clause order is valid SQL?",
      ["`SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT …`",
       "`SELECT … FROM … GROUP BY … WHERE … ORDER BY … HAVING …`",
       "`FROM … SELECT … WHERE … LIMIT … ORDER BY …`",
       "`SELECT … WHERE … FROM … HAVING … GROUP BY …`"],
      0,
      {1: "WHERE must come before GROUP BY, and HAVING before ORDER BY.",
       2: "Queries start with SELECT, and ORDER BY comes before LIMIT.",
       3: "FROM comes right after SELECT, and GROUP BY before HAVING."},
      "The written order is SELECT, FROM, (JOIN), WHERE, GROUP BY, HAVING, ORDER BY, LIMIT: \"SFJWGHOL\".",
      "Syllabus 2.4.1", ["sql", "clause-order"]),

    Q("b2-105", "2.4.1", 2,
      "Table `t` has one column `x` holding 1, NULL, 3, NULL. What does this query return?",
      ["`(4, 2, 2.0)`", "`(4, 4, 1.0)`", "`(2, 2, 2.0)`", "`(4, 2, 1.0)`"],
      0,
      {1: "COUNT(x) skips NULLs, and AVG ignores them too.",
       2: "COUNT(*) counts rows, NULL or not: 4.",
       3: "AVG divides by the number of non-NULL values (2), not by 4."},
      "COUNT(*) = 4 rows; COUNT(x) = 2 non-NULL values; AVG(x) = (1 + 3) / 2 = 2.0.",
      "Syllabus 2.4.1", ["sql", "null", "aggregates"],
      code="""
      SELECT COUNT(*), COUNT(x), AVG(x) FROM t;
      """, lang="sql",
      setup="CREATE TABLE t (x INTEGER); INSERT INTO t VALUES (1), (NULL), (3), (NULL);",
      verify={"py": "assert run_sql(setup, code) == [(4, 2, 2.0)]"}),

    Q("b2-106", "2.4.1", 2,
      "Table `t` has one column `x` holding 1, NULL, 3, NULL. What count does this query return?",
      ["0", "2", "4", "An error"],
      0,
      {1: "Comparing with NULL using = is never true; `IS NULL` would give 2.",
       2: "Only rows where the condition is true are counted.",
       3: "The query is valid; it just matches nothing."},
      "Any comparison with NULL yields unknown, which WHERE treats as false. Use `WHERE x IS NULL`.",
      "Syllabus 2.4.1", ["sql", "null"],
      code="""
      SELECT COUNT(*) FROM t WHERE x = NULL;
      """, lang="sql",
      setup="CREATE TABLE t (x INTEGER); INSERT INTO t VALUES (1), (NULL), (3), (NULL);",
      verify={"py": "assert run_sql(setup, code) == [(0,)]"}),

    Q("b2-107", "2.4.1", 3,
      "Which query lists customers who have never placed an order?",
      ["SELECT c.name\nFROM customers AS c\nLEFT JOIN orders AS o ON o.customer_id = c.id\nWHERE o.id IS NULL;",
       "SELECT c.name\nFROM customers AS c\nJOIN orders AS o ON o.customer_id = c.id\nWHERE o.id IS NULL;",
       "SELECT c.name\nFROM customers AS c\nLEFT JOIN orders AS o ON o.customer_id = c.id\nWHERE o.id = NULL;",
       "SELECT c.name\nFROM orders AS o\nLEFT JOIN customers AS c ON c.id = o.customer_id\nWHERE c.id IS NULL;"],
      0,
      {1: "An inner join keeps only customers with orders, so nothing is left with a NULL order id.",
       2: "`= NULL` is never true; use `IS NULL`.",
       3: "This finds orders without a customer (order 14), and returns a NULL name."},
      "A LEFT JOIN keeps customers without orders, whose order columns are NULL; `WHERE o.id IS NULL` keeps just those (Dev).",
      "Syllabus 2.4.1", ["sql", "anti-join"], lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": """
      results = [run_sql(setup, opt(i)) for i in range(4)]
      assert results[0] == [('Dev',)], results[0]
      assert all(r != [('Dev',)] for i, r in enumerate(results) if i != 0), results
      """}),

    Q("b2-108", "2.4.1", 2,
      "Which names does this query return, in order?",
      ["Cara, Ben", "Dev, Cara", "Ben, Ana", "Ana, Ben"],
      0,
      {1: "OFFSET 1 skips the first row (Dev).",
       2: "Descending order starts with Dev; Ben and Ana are positions 3 and 4.",
       3: "That's ascending order without the offset."},
      "Sorted descending: Dev, Cara, Ben, Ana. OFFSET 1 skips Dev and LIMIT 2 returns Cara and Ben.",
      "Syllabus 2.4.1", ["sql", "limit"],
      code="""
      SELECT name FROM customers ORDER BY name DESC LIMIT 2 OFFSET 1;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": "assert run_sql(setup, code) == [('Cara',), ('Ben',)]"}),

    Q("b2-109", "2.4.1", 2,
      "How many rows does this query return?",
      ["6", "5", "4", "9"],
      0,
      {1: "A LEFT or RIGHT JOIN would give 5; a FULL OUTER JOIN keeps both Dev and order 14.",
       2: "4 is the INNER JOIN: matching pairs only.",
       3: "Rows aren't created for every customer-order combination; only matching pairs join, and each unmatched row appears once."},
      "The 4 matching pairs (Ana ×2, Ben, Cara), plus Dev with no orders (order columns NULL), plus order 14 whose customer 5 doesn't exist (customer columns NULL): 6 rows.",
      "Syllabus 2.4.1 · SQLite: FULL OUTER JOIN", ["sql", "full-outer-join"],
      code="""
      SELECT c.name, o.id
      FROM customers AS c
      FULL OUTER JOIN orders AS o ON o.customer_id = c.id;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": "assert len(run_sql(setup, code)) == 6"}),

    Q("b2-160", "2.4.1", 2,
      "What does the last row of this query's result contain?",
      ["`('Dev', 0)`", "`('Dev', None)`", "`('Cara', 50.0)`", "`('Ana', 200.0)`"],
      0,
      {1: "`SUM` over Dev's NULL order totals is NULL, but `COALESCE` replaces it with 0.",
       2: "The LEFT JOIN keeps Dev, who has no orders, so Cara isn't last.",
       3: "Ana ties with Ben at 200 and the tie is broken by name, A to Z, so Ana comes first."},
      "The LEFT JOIN keeps Dev with NULL order columns. `SUM` of nothing but NULLs is NULL, and `COALESCE(x, 0)` returns its first non-NULL argument, 0. Sorted by `spent` from highest to lowest, Dev (0) comes last.",
      "Syllabus 2.4.1 · SQLite docs", ["sql", "coalesce", "left-join"],
      code="""
      SELECT c.name, COALESCE(SUM(o.total), 0) AS spent
      FROM customers AS c
      LEFT JOIN orders AS o ON o.customer_id = c.id
      GROUP BY c.name
      ORDER BY spent DESC, c.name;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": """
      rows = run_sql(setup, code)
      assert rows[-1] == ('Dev', 0) and rows[0] == ('Ana', 200.0), rows
      """}),

    Q("b2-161", "2.4.1", 3,
      "How many rows does this query return?",
      ["4", "5", "3", "6"],
      0,
      {1: "Bread and Bagel both give ('bakery', 'mid'), and `DISTINCT` keeps that row once.",
       2: "Milk's NULL price makes `BETWEEN` unknown, so `CASE` falls through to `ELSE`: dairy still appears, as 'other'.",
       3: "Cake is left out: its name doesn't start with B and bakery isn't in the `IN` list."},
      "The WHERE keeps Apple, Avocado, Bread, Bagel and Milk. `BETWEEN 1.5 AND 3` includes both ends, so Bread (3.0) and Bagel (1.5) are 'mid', Avocado is 'mid', Apple is 'other', and Milk (NULL) goes to ELSE. `DISTINCT` collapses the two bakery rows: (bakery, mid), (dairy, other), (fruit, mid), (fruit, other).",
      "Syllabus 2.4.1 · SQLite docs", ["sql", "case", "between", "distinct"],
      code="""
      SELECT DISTINCT category,
             CASE WHEN price BETWEEN 1.5 AND 3 THEN 'mid' ELSE 'other' END AS band
      FROM products
      WHERE name LIKE 'B%' OR category IN ('dairy', 'fruit')
      ORDER BY category, band;
      """, lang="sql", tables=["products"],
      setup="""
      CREATE TABLE products (name TEXT, category TEXT, price REAL);
      INSERT INTO products VALUES ('Apple', 'fruit', 1.2), ('Avocado', 'fruit', 2.5),
        ('Bread', 'bakery', 3.0), ('Bagel', 'bakery', 1.5), ('Cake', 'bakery', 12.0), ('Milk', 'dairy', NULL);
      """,
      verify={"py": """
      rows = run_sql(setup, code)
      assert rows == [('bakery', 'mid'), ('dairy', 'other'), ('fruit', 'mid'), ('fruit', 'other')], rows
      """}),

    Q("b2-162", "2.4.1", 2,
      "What is the last row of this query's result?",
      ["`(14, None)`", "`(None, 'Dev')`", "`(13, 'Cara')`", "`(14, 'Dev')`"],
      0,
      {1: "A RIGHT JOIN keeps every row of the right table (orders); Dev has no orders, so Dev doesn't appear.",
       2: "Order 14 has no matching customer but is still kept, and it sorts after 13.",
       3: "Order 14 belongs to customer 5, who doesn't exist, so its customer columns are NULL."},
      "A RIGHT JOIN keeps every order and fills in the customer where one matches. Order 14 points at customer 5, who doesn't exist, so its `name` is NULL (None in Python). It is the mirror image of `orders LEFT JOIN customers`.",
      "Syllabus 2.4.1 · SQLite docs", ["sql", "right-join"],
      code="""
      SELECT o.id, c.name
      FROM customers AS c
      RIGHT JOIN orders AS o ON o.customer_id = c.id
      ORDER BY o.id;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": """
      rows = run_sql(setup, code)
      assert len(rows) == 5 and rows[-1] == (14, None), rows
      """}),

    Q("b2-163", "2.4.1", 3,
      "Which names does this query return?",
      ["Ben, Dev", "Dev", "Ana, Cara", "Ben, Dev and a row for customer 5"],
      0,
      {1: "Ben's only order (12) is refunded, so Ben has no paid order either.",
       2: "Ana and Cara are exactly the customers who do have paid orders.",
       3: "The outer query reads only the customers table; customer 5 isn't in it."},
      "The subquery lists the customer IDs with a paid order: 1, 1, 3 and 5. `NOT IN` keeps the customers whose ID isn't in that list: Ben (2) and Dev (4).",
      "Syllabus 2.4.1 · SQLite docs", ["sql", "subquery", "not-in"],
      code="""
      SELECT c.name
      FROM customers AS c
      WHERE c.id NOT IN (SELECT customer_id FROM orders WHERE status = 'paid')
      ORDER BY c.name;
      """, lang="sql", setup=SHOP, tables=["customers", "orders"],
      verify={"py": """
      rows = run_sql(setup, code)
      assert rows == [('Ben',), ('Dev',)], rows
      """}),

    Q("b2-164", "2.4.1", 3,
      "What does this query return?",
      ["`[('Ana', 2, 19.0), ('Ben', 1, 2.5)]`",
       "`[('Ana', 3, 19.0), ('Ben', 1, 2.5)]`",
       "`[('Ana', 2, 7.0), ('Ben', 1, 1.0)]`",
       "`[('Ana', 2, 19.0)]`"],
      0,
      {1: "Order 11 has two item rows; `COUNT(DISTINCT o.id)` counts the order once.",
       2: "7 and 1 are the quantities; the query sums quantity × price.",
       3: "Ben's order 12 has an item, so Ben appears too."},
      "Each item row is joined to its order and each order to its customer. Ana has orders 10 and 11 with items worth 2×3.0 + 1×3.0 + 4×2.5 = 19.0; Ben has order 12 worth 2.5. Joining items repeats order rows, which is why `DISTINCT` is needed to count orders.",
      "Syllabus 2.4.1 · SQLite docs", ["sql", "joins", "count-distinct"],
      code="""
      SELECT c.name, COUNT(DISTINCT o.id) AS orders, SUM(i.qty * i.price) AS spent
      FROM customers AS c
      JOIN orders AS o ON o.customer_id = c.id
      JOIN items AS i ON i.order_id = o.id
      GROUP BY c.name
      ORDER BY c.name;
      """, lang="sql", tables=["customers", "orders", "items"],
      setup="""
      CREATE TABLE customers (id INTEGER, name TEXT);
      CREATE TABLE orders (id INTEGER, customer_id INTEGER);
      CREATE TABLE items (order_id INTEGER, sku TEXT, qty INTEGER, price REAL);
      INSERT INTO customers VALUES (1, 'Ana'), (2, 'Ben');
      INSERT INTO orders VALUES (10, 1), (11, 1), (12, 2);
      INSERT INTO items VALUES (10, 'tea', 2, 3.0), (11, 'tea', 1, 3.0), (11, 'jam', 4, 2.5), (12, 'jam', 1, 2.5);
      """,
      verify={"py": """
      rows = run_sql(setup, code)
      assert rows == [('Ana', 2, 19.0), ('Ben', 1, 2.5)], rows
      """}),

    # ---------- 2.4.2 CRUD ----------
    Q("b2-110", "2.4.2", 1,
      "Which SQL statement performs the \"Update\" in CRUD?",
      ["UPDATE", "INSERT", "ALTER TABLE", "SELECT"],
      0,
      {1: "INSERT is Create.",
       2: "ALTER TABLE changes a table's structure, not its rows.",
       3: "SELECT is Read."},
      "CRUD maps to INSERT (create), SELECT (read), UPDATE (update) and DELETE (delete).",
      "Syllabus 2.4.2", ["sql", "crud"]),

    Q("b2-111", "2.4.2", 2,
      "Table `products` has three rows. How many rows have a price of 0 after this statement runs?",
      ["3", "1", "0", "It fails without a WHERE clause"],
      0,
      {1: "There is no WHERE clause restricting it to one row.",
       2: "The statement is valid and changes rows.",
       3: "SQL allows UPDATE without WHERE; it updates every row."},
      "UPDATE without WHERE changes every row in the table.",
      "Syllabus 2.4.2", ["sql", "update"],
      code="""
      UPDATE products SET price = 0;
      """, lang="sql",
      setup="CREATE TABLE products (name TEXT, price REAL); INSERT INTO products VALUES ('Tea', 2.5), ('Cocoa', 3.0), ('Milk', 1.2);",
      verify={"py": """
      con = run_sql_script(setup, code)
      assert con.execute("SELECT COUNT(*) FROM products WHERE price = 0").fetchone()[0] == 3
      """}),

    Q("b2-112", "2.4.2", 1,
      "Which statement removes all rows from `logs` but keeps the table for new data?",
      ["`DELETE FROM logs;`", "`DROP TABLE logs;`", "`REMOVE logs;`", "`SELECT * FROM logs LIMIT 0;`"],
      0,
      {1: "DROP TABLE deletes the table itself, structure included.",
       2: "REMOVE is not a SQL command.",
       3: "SELECT only reads; it changes nothing."},
      "DELETE without WHERE empties the table; DROP removes it completely.",
      "Syllabus 2.4.2", ["sql", "delete"]),

    Q("b2-113", "2.4.2", 3,
      "What does this code print?",
      ["`0`", "`1`", "An OperationalError is raised", "A ProgrammingError is raised"],
      0,
      {1: "The INSERT was never committed, so closing the connection rolled it back.",
       2: "The table exists; it was committed before the INSERT.",
       3: "Both connections are valid; the data simply wasn't saved."},
      "sqlite3 opens a transaction for the INSERT; closing without `commit()` discards it, so the reopened database has an empty table.",
      "Syllabus 2.4.2, 2.4.3 · Python docs: sqlite3 transaction control", ["sql", "commit"],
      code="""
      import os
      import sqlite3
      import tempfile

      path = os.path.join(tempfile.mkdtemp(), "shop.db")
      con = sqlite3.connect(path)
      con.execute("CREATE TABLE items (name TEXT)")
      con.commit()
      con.execute("INSERT INTO items VALUES ('tea')")
      con.close()                      # no commit after the INSERT

      con = sqlite3.connect(path)
      print(con.execute("SELECT COUNT(*) FROM items").fetchone()[0])
      """, verify="stdout"),

    Q("b2-114", "2.4.2", 2,
      "Table `products` starts with three rows. How many rows does it hold after this statement?",
      ["5", "4", "3", "It fails: only one row can be inserted per statement"],
      0,
      {1: "The VALUES list contains two rows.",
       2: "INSERT adds rows; it doesn't replace them.",
       3: "A single INSERT can list several rows."},
      "One INSERT with two VALUES tuples adds two rows: 3 + 2 = 5.",
      "Syllabus 2.4.2", ["sql", "insert"],
      code="""
      INSERT INTO products (name, price) VALUES ('Tea', 2.5), ('Cocoa', 3.0);
      """, lang="sql",
      setup="CREATE TABLE products (name TEXT, price REAL); INSERT INTO products VALUES ('A', 1), ('B', 2), ('C', 3);",
      verify={"py": """
      con = run_sql_script(setup, code)
      assert con.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 5
      """}),

    Q("b2-115", "2.4.2", 2,
      "Which two statements change the data in a table rather than its structure? Select two.",
      ["INSERT", "DELETE", "CREATE TABLE", "DROP TABLE", "ALTER TABLE"],
      [0, 1],
      {2: "CREATE TABLE defines structure.",
       3: "DROP TABLE removes structure.",
       4: "ALTER TABLE changes structure."},
      "INSERT, UPDATE and DELETE manipulate rows (DML); CREATE, DROP and ALTER define structure (DDL).",
      "Syllabus 2.4.2", ["sql", "dml"]),

    Q("b2-116", "2.4.2", 3,
      "These three statements run in order. Which names does `SELECT name FROM products ORDER BY name` return afterwards?",
      ["Chai, Green, Mint, Oats", "Chai, Green, Oats", "Chai, Green, Jam, Mint, Oats", "Green, Mint, Oats"],
      0,
      {1: "The UPDATE runs first and lifts Mint from 1.9 to about 2.09, so the DELETE no longer removes it.",
       2: "Jam (1.8) isn't tea, so its price isn't raised, and the DELETE removes it.",
       3: "The INSERT adds Chai after the DELETE has run, so Chai stays."},
      "The UPDATE raises tea prices by 10% (Green 2.2, Mint 2.09); the DELETE then removes only Jam (1.8); the INSERT adds Chai. Statements run in order, so each one sees the previous one's changes.",
      "Syllabus 2.4.2", ["sql", "crud", "update", "delete"],
      code="""
      UPDATE products SET price = price * 1.1 WHERE category = 'tea';
      DELETE FROM products WHERE price < 2;
      INSERT INTO products (name, category, price) VALUES ('Chai', 'tea', 3.0);
      """, lang="sql", tables=["products"],
      setup="""
      CREATE TABLE products (name TEXT, category TEXT, price REAL);
      INSERT INTO products VALUES ('Green', 'tea', 2.0), ('Mint', 'tea', 1.9),
                                  ('Jam', 'food', 1.8), ('Oats', 'food', 4.0);
      """,
      verify={"py": """
      con = run_sql_script(setup, code)
      names = [r[0] for r in con.execute("SELECT name FROM products ORDER BY name")]
      assert names == ["Chai", "Green", "Mint", "Oats"], names
      """}),

    Q("b2-117", "2.4.2", 2,
      "Which two statements delete rows from `logs` but keep the table itself? Select two.",
      ["`DELETE FROM logs WHERE created < '2025-01-01';`",
       "`DELETE FROM logs;`",
       "`DROP TABLE logs;`",
       "`SELECT * FROM logs LIMIT 0;`",
       "`ALTER TABLE logs RENAME TO old_logs;`"],
      [0, 1],
      {2: "DROP removes the whole table, structure included.",
       3: "SELECT only reads; it never changes the data.",
       4: "Renaming changes the table's name, not its rows."},
      "DELETE removes rows: those matching the WHERE, or every row when there is no WHERE. The empty table stays, ready for new data.",
      "Syllabus 2.4.2", ["sql", "delete", "drop"]),

    # ---------- 2.4.3 Connections ----------
    Q("b2-120", "2.4.3", 2,
      "What does this code print?",
      ["`(1,) [(2,), (3,)] None`", "`1 [2, 3] None`", "`(1,) [(1,), (2,), (3,)] (1,)`", "`[(1,)] [(2,), (3,)] []`"],
      0,
      {1: "Rows come back as tuples, even with one column.",
       2: "The cursor advances; `fetchall` returns only the remaining rows.",
       3: "`fetchone` returns a single tuple (or None), not a list."},
      "`fetchone` returns the next row as a tuple; `fetchall` returns the remaining rows as a list; with no rows left, `fetchone` returns None.",
      "Syllabus 2.4.3 · Python docs: sqlite3 Cursor", ["sqlite3", "fetch"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE t (n INTEGER)")
      con.executemany("INSERT INTO t VALUES (?)", [(1,), (2,), (3,)])
      cur = con.execute("SELECT n FROM t ORDER BY n")
      print(cur.fetchone(), cur.fetchall(), cur.fetchone())
      """, verify="stdout"),

    Q("b2-121", "2.4.3", 2,
      "A script runs `sqlite3.connect(\"sales.db\")` and then fails with `no such table: orders`, although a colleague's copy of sales.db contains that table. What is the most likely cause?",
      ["The script ran from a different folder, so `connect` created a new, empty sales.db there",
       "The table name is a reserved word",
       "sqlite3 needs a password",
       "The database server is down"],
      0,
      {1: "`orders` is not a reserved word.",
       2: "SQLite files have no users or passwords.",
       3: "SQLite is a file, not a server."},
      "`connect` creates the file if it doesn't exist, so a wrong relative path silently opens an empty database. Use an absolute path or check the working directory.",
      "Syllabus 2.4.3", ["sqlite3", "troubleshooting"]),

    Q("b2-122", "2.4.3", 2,
      "What does `with sqlite3.connect(path) as con:` do when the block ends without an error?",
      ["It commits the transaction but leaves the connection open",
       "It commits and closes the connection",
       "It rolls back the transaction",
       "It closes the connection without committing"],
      0,
      {1: "The connection's context manager handles the transaction only; call `con.close()` (or use `contextlib.closing`).",
       2: "It rolls back only when an exception occurs.",
       3: "It commits on success."},
      "The sqlite3 connection context manager commits on success and rolls back on an exception; it does not close the connection.",
      "Syllabus 2.4.3 · Python docs: sqlite3 connection context manager", ["sqlite3", "transactions"],
      verify={"py": """
      import sqlite3
      with sqlite3.connect(":memory:") as con:
          con.execute("CREATE TABLE t (x)")
          con.execute("INSERT INTO t VALUES (1)")
      assert not con.in_transaction
      assert con.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1   # still open
      """}),

    Q("b2-123", "2.4.3", 2,
      "`pymysql.connect(...)` fails with \"Access denied for user 'analyst'@'10.0.0.5'\". What is the likely cause?",
      ["Wrong user name or password, or no privileges for that user from that host",
       "The PyMySQL package isn't installed",
       "The server's hostname can't be resolved",
       "The query has a syntax error"],
      0,
      {1: "A missing package fails at `import pymysql`, before connecting.",
       2: "Name-resolution problems give a \"can't connect\" error, not \"access denied\".",
       3: "No query has run yet."},
      "\"Access denied\" means the server was reached but rejected the credentials or permissions.",
      "Syllabus 2.4.3", ["pymysql", "troubleshooting"]),

    Q("b2-124", "2.4.3", 1,
      "In Python's DB-API, which object executes SQL statements and fetches their results?",
      ["The cursor", "The connection string", "The DataFrame", "The transaction log"],
      0,
      {1: "A connection string only describes where to connect.",
       2: "pandas can read results into a DataFrame, but the DB-API object is the cursor.",
       3: "The transaction log is internal to the database."},
      "`con.cursor()` returns a cursor with `execute()`, `fetchone()`, `fetchall()` and `fetchmany()`.",
      "Syllabus 2.4.3", ["db-api", "cursor"]),

    Q("b2-125", "2.4.3", 2,
      "What does this code print?",
      ["`tea 2.5 ['name', 'price']`", "`tea 2.5 ('name', 'price')`", "A TypeError is raised", "`None 2.5 []`"],
      0,
      {1: "`Row.keys()` returns a list of column names.",
       2: "With `sqlite3.Row`, rows support both name and index access.",
       3: "The row has data; nothing is None."},
      "`row_factory = sqlite3.Row` makes each row accessible by column name or position, and `keys()` lists the column names.",
      "Syllabus 2.4.3 · Python docs: sqlite3.Row", ["sqlite3", "row-factory"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.row_factory = sqlite3.Row
      con.execute("CREATE TABLE p (name TEXT, price REAL)")
      con.execute("INSERT INTO p VALUES ('tea', 2.5)")
      row = con.execute("SELECT * FROM p").fetchone()
      print(row["name"], row[1], row.keys())
      """, verify="stdout"),

    Q("b2-126", "2.4.3", 3,
      "What does this code print?",
      ["`0`", "`1`", "`2`", "A ProgrammingError is raised, because the `with` block closed the connection"],
      0,
      {1: "Leaving the `with` block with an exception rolls back the whole transaction, including the first INSERT.",
       2: "The second INSERT fails (two values for a one-column table), so it never adds a row.",
       3: "`with con:` commits or rolls back, but it doesn't close the connection, so the last query works."},
      "The second INSERT raises OperationalError. Because it leaves the `with` block, the open transaction is rolled back and the first INSERT is undone too. The CREATE TABLE ran before that transaction began, so the table still exists, empty, and the connection is still open.",
      "Syllabus 2.4.3 · Python sqlite3 docs", ["sqlite3", "transactions", "context-manager"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE t (n INTEGER)")
      try:
          with con:
              con.execute("INSERT INTO t VALUES (1)")
              con.execute("INSERT INTO t VALUES ('x', 2)")
      except sqlite3.OperationalError:
          pass
      print(con.execute("SELECT COUNT(*) FROM t").fetchone()[0])
      """, verify="stdout"),

    Q("b2-127", "2.4.3", 2,
      "Which two error messages point to a connection problem rather than a mistake in the SQL? Select two.",
      ["`Access denied for user 'analyst'@'10.0.0.5'`",
       "`Can't connect to MySQL server on 'db.example.com' (timed out)`",
       "`near \"FORM\": syntax error`",
       "`no such column: totl`",
       "`UNIQUE constraint failed: users.email`"],
      [0, 1],
      {2: "A misspelled keyword (FORM for FROM) is an SQL syntax error; the connection worked.",
       3: "A misspelled column name is a mistake in the query.",
       4: "A constraint error means the query ran and the data broke a rule."},
      "\"Access denied\" means the server was reached but rejected the login or permissions; \"can't connect / timed out\" means the server wasn't reached (wrong host or port, server down, firewall). The other messages come from a connection that works.",
      "Syllabus 2.4.3", ["connections", "errors", "pymysql"]),

    # ---------- 2.4.4 Parameterized queries ----------
    Q("b2-130", "2.4.4", 1,
      "`email` holds text typed by a user. Which sqlite3 call is correctly parameterized?",
      ["`cur.execute(\"SELECT * FROM users WHERE email = ?\", (email,))`",
       "`cur.execute(f\"SELECT * FROM users WHERE email = '{email}'\")`",
       "`cur.execute(\"SELECT * FROM users WHERE email = '%s'\" % email)`",
       "`cur.execute(\"SELECT * FROM users WHERE email = \" + email)`"],
      0,
      {1: "An f-string pastes the input into the SQL text: injectable.",
       2: "The `%` operator formats the string in Python before sqlite3 sees it: injectable.",
       3: "Concatenation is injectable and also produces invalid SQL for text."},
      "The `?` placeholder with a one-item tuple sends the value separately from the SQL text.",
      "Syllabus 2.4.4", ["sql", "parameters"]),

    Q("b2-131", "2.4.4", 3,
      "What happens when the last line runs?",
      ["A `sqlite3.ProgrammingError` is raised, because `(5)` is the integer 5, not a tuple",
       "It returns no rows",
       "It returns the row with id 5",
       "A SyntaxError is raised"],
      0,
      {1: "The call fails before any query runs.",
       2: "The parameters argument must be a sequence or dict; a bare int is rejected.",
       3: "The line is valid Python syntax; the problem is the argument's type."},
      "Parentheses alone don't make a tuple. Write `(5,)` or `[5]` for a single parameter.",
      "Syllabus 2.4.4 · Python docs: sqlite3 placeholders", ["sql", "parameters", "tuples"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE t (id INTEGER)")
      con.execute("SELECT * FROM t WHERE id = ?", (5))
      """, verify="raises:ProgrammingError"),

    Q("b2-132", "2.4.4", 3,
      "What does this code print?",
      ["`3 0`", "`0 0`", "`3 3`", "`1 0`"],
      0,
      {1: "The f-string query is altered by the input: `OR '1'='1'` is always true.",
       2: "The parameterized query treats the whole input as one name, which matches nobody.",
       3: "The injected condition matches every row, not one."},
      "String formatting lets the input rewrite the WHERE clause and return all 3 users; the placeholder version searches for a user literally named \"nobody' OR '1'='1\" and finds none.",
      "Syllabus 2.4.4, 2.4.6", ["sql-injection", "parameters"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE users (name TEXT, secret TEXT)")
      con.executemany("INSERT INTO users VALUES (?, ?)",
                      [("ana", "a1"), ("ben", "b2"), ("cara", "c3")])
      name = "nobody' OR '1'='1"
      unsafe = con.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()
      safe = con.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
      print(len(unsafe), len(safe))
      """, verify="stdout"),

    Q("b2-133", "2.4.4", 2,
      "What does this code print?",
      ["`[('a', 5.0), ('b', 2.0)]`", "`[('a', 1.5), ('b', 2.0)]`", "`[('a', 3.5), ('b', 2.0)]`", "`[('a', 5.0), ('a', 5.0), ('b', 2.0)]`"],
      0,
      {1: "Both rows for sensor a are summed.",
       2: "SUM adds 1.5 and 3.5.",
       3: "GROUP BY returns one row per sensor."},
      "`executemany` inserts all three rows; grouping by sensor sums a = 1.5 + 3.5 = 5.0 and b = 2.0.",
      "Syllabus 2.4.4 · Python docs: executemany", ["executemany", "sql"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE readings (sensor TEXT, value REAL)")
      rows = [("a", 1.5), ("b", 2.0), ("a", 3.5)]
      con.executemany("INSERT INTO readings VALUES (?, ?)", rows)
      print(con.execute("SELECT sensor, SUM(value) FROM readings "
                        "GROUP BY sensor ORDER BY sensor").fetchall())
      """, verify="stdout"),

    Q("b2-134", "2.4.4", 2,
      "Which sqlite3 call correctly uses named placeholders?",
      ["`con.execute(\"SELECT * FROM t WHERE region = :r AND total > :m\", {\"r\": \"EU\", \"m\": 100})`",
       "`con.execute(\"SELECT * FROM t WHERE region = {r} AND total > {m}\", {\"r\": \"EU\", \"m\": 100})`",
       "`con.execute(\"SELECT * FROM t WHERE region = :r AND total > :m\", (\"EU\", 100))`",
       "`con.execute(\"SELECT * FROM t WHERE region = $r AND total > $m\", r=\"EU\", m=100)`"],
      0,
      {1: "Braces are Python format fields, not SQL placeholders; the query has no parameters.",
       2: "Named placeholders take a dict. A tuple is matched by position and the names are ignored: Python 3.12 and 3.13 warn that this is deprecated, and Python 3.14 raises a ProgrammingError.",
       3: "`execute` doesn't take keyword arguments for parameters."},
      "sqlite3's named style uses `:name` in the SQL and a dict of values.",
      "Syllabus 2.4.4 · Python docs: sqlite3 placeholders", ["sql", "named-parameters"],
      verify={"py": """
      import sqlite3
      import sys
      import warnings

      def run(i):
          con = sqlite3.connect(":memory:")
          con.execute("CREATE TABLE t (region TEXT, total REAL)")
          con.execute("INSERT INTO t VALUES ('EU', 150)")
          with warnings.catch_warnings():
              warnings.simplefilter("error")          # a deprecation counts as incorrect use
              return eval(opt(i), {"con": con}).fetchall()

      assert run(0) == [('EU', 150.0)]
      for i in (1, 3):
          try:
              run(i)
              raise AssertionError(f"option {i} should fail")
          except (sqlite3.Error, TypeError):
              pass
      if sys.version_info >= (3, 12):                # earlier versions accept a tuple silently
          try:
              run(2)
              raise AssertionError("option 2 should warn or fail")
          except (DeprecationWarning, sqlite3.ProgrammingError):
              pass
      """}),

    Q("b2-135", "2.4.4", 3,
      "A report lets users choose the column to sort by. How should the query be built safely?",
      ["Check the chosen name against a fixed allow-list of column names, then insert it into the SQL",
       "Pass the column name as a `?` parameter",
       "Insert the name with an f-string after removing quote characters",
       "Lowercase the name before inserting it"],
      0,
      {1: "Placeholders bind values, not identifiers; `ORDER BY ?` sorts by a constant string.",
       2: "Stripping quotes is fragile; other characters can still inject SQL.",
       3: "Lowercasing doesn't make input safe."},
      "Identifiers can't be parameterized, so only accept names from a known list; still use placeholders for any values.",
      "Syllabus 2.4.4, 2.4.6", ["sql", "identifiers", "security"]),

    Q("b2-136", "2.4.4", 3,
      "What does this code print?",
      ["`2 ('ana',)`",
       "An OperationalError is raised, because the quotes break the INSERT",
       "`1 None`",
       "An OperationalError is raised: no such table: notes"],
      0,
      {1: "Values passed through placeholders are never pasted into the SQL text, so quotes inside them are harmless.",
       2: "Both rows are inserted, and the second body contains \"DROP\" as plain text.",
       3: "The DROP TABLE text was stored as data; it never ran as SQL."},
      "`executemany` with named placeholders inserts both rows, apostrophes and all. The attempted injection is just text in the `body` column, which the `LIKE ?` query finds.",
      "Syllabus 2.4.4 · Python sqlite3 docs", ["executemany", "named-placeholders", "sql-injection"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE notes (author TEXT, body TEXT)")
      rows = [{"a": "o'brien", "b": "it's fine"},
              {"a": "ana", "b": "x'); DROP TABLE notes; --"}]
      con.executemany("INSERT INTO notes VALUES (:a, :b)", rows)
      print(con.execute("SELECT COUNT(*) FROM notes").fetchone()[0],
            con.execute("SELECT author FROM notes WHERE body LIKE ?", ("%DROP%",)).fetchone())
      """, verify="stdout"),

    Q("b2-137", "2.4.4", 2,
      "`region` and `minimum` come from user input. Which PyMySQL call passes both values safely?",
      ["`cur.execute(\"SELECT * FROM t WHERE region = %s AND total > %s\", (region, minimum))`",
       "`cur.execute(\"SELECT * FROM t WHERE region = %s AND total > %s\" % (region, minimum))`",
       "`cur.execute(\"SELECT * FROM t WHERE region = ? AND total > ?\", (region, minimum))`",
       "`cur.execute(f\"SELECT * FROM t WHERE region = '{region}' AND total > {minimum}\")`"],
      0,
      {1: "The `%` operator builds the SQL string in Python before the driver sees it, so it is injectable.",
       2: "`?` is sqlite3's placeholder; PyMySQL uses `%s`.",
       3: "An f-string pastes the input into the SQL text."},
      "PyMySQL's placeholder is `%s`, with the values passed as the second argument to `execute`. The driver then sends them as data, separately from the SQL.",
      "Syllabus 2.4.4 · PyMySQL docs", ["pymysql", "placeholders"]),

    # ---------- 2.4.5 Types ----------
    Q("b2-140", "2.4.5", 2,
      "What does this code print?",
      ["`['int', 'float', 'str', 'str', 'int']`",
       "`['int', 'float', 'str', 'date', 'bool']`",
       "`['int', 'float', 'str', 'datetime', 'int']`",
       "`['int', 'float', 'str', 'str', 'bool']`"],
      0,
      {1: "SQLite has no date or boolean types: the date comes back as text and True as 1.",
       2: "A TEXT column returns str unless you add a converter.",
       3: "Booleans are stored as integers and read back as int."},
      "INTEGER → int, REAL → float, TEXT → str; the ISO date is just text, and True was stored as the integer 1.",
      "Syllabus 2.4.5 · Python docs: sqlite3 type mapping", ["sql-types", "sqlite3"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE t (n INTEGER, x REAL, s TEXT, d TEXT, flag INTEGER)")
      con.execute("INSERT INTO t VALUES (?, ?, ?, ?, ?)", (3, 2.5, "a", "2025-07-15", True))
      print([type(v).__name__ for v in con.execute("SELECT * FROM t").fetchone()])
      """, verify="stdout"),

    Q("b2-141", "2.4.5", 2,
      "What does this code print?",
      ["`float64`", "`int64`", "`object`", "`Int64`"],
      0,
      {1: "The NULL becomes NaN, which is a float, so the column can't stay int64.",
       2: "The values are numeric, so pandas uses a numeric dtype.",
       3: "The nullable `Int64` dtype is only used if you ask for it."},
      "An integer column containing NULL is read as float64, because NaN is a floating-point value.",
      "Syllabus 2.4.5 · pandas: read_sql_query", ["sql-types", "pandas"],
      code="""
      import sqlite3
      import pandas as pd

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE t (qty INTEGER)")
      con.executemany("INSERT INTO t VALUES (?)", [(1,), (None,), (3,)])
      df = pd.read_sql_query("SELECT qty FROM t", con)
      print(df["qty"].dtype)
      """, verify="stdout"),

    Q("b2-142", "2.4.5", 2,
      "A MySQL column is declared `DECIMAL(10,2)`. Which Python type does PyMySQL return for its values?",
      ["`decimal.Decimal`", "`float`", "`str`", "`int`"],
      0,
      {1: "Converting to float would lose DECIMAL's exactness.",
       2: "Numbers are converted to a numeric type, not text.",
       3: "DECIMAL(10,2) has two decimal places, so int can't hold it."},
      "DECIMAL maps to `decimal.Decimal`, which keeps exact decimal values (important for money).",
      "Syllabus 2.4.5 · PyMySQL converters", ["sql-types", "decimal"]),

    Q("b2-143", "2.4.5", 2,
      "How should order dates be stored in SQLite so they sort and compare correctly?",
      ["As ISO 8601 text, such as '2025-07-15'",
       "As text in day/month/year form, such as '15/07/2025'",
       "In a DATE column, which SQLite converts to Python `date` objects automatically",
       "As the number of days in the month"],
      0,
      {1: "Day-first text sorts wrongly: '02/01/2026' comes before '15/07/2025'.",
       2: "SQLite has no real DATE type; values come back as whatever was stored, usually text.",
       3: "That loses the year and month."},
      "ISO 8601 text sorts chronologically as plain text and converts easily with `date.fromisoformat` or `pd.to_datetime`.",
      "Syllabus 2.4.5", ["sql-types", "dates"]),

    Q("b2-144", "2.4.5", 3,
      "What does this code print?",
      ["`14`", "A TypeError is raised", "`2025-07-01`", "`0`"],
      0,
      {1: "The text is converted with `date.fromisoformat` before subtracting.",
       2: "The printed value is the number of days between the dates.",
       3: "The dates are two weeks apart."},
      "SQLite returns the stored text; `date.fromisoformat` converts it to a date, and subtracting dates gives a timedelta of 14 days.",
      "Syllabus 2.4.5", ["sql-types", "dates"],
      code="""
      import sqlite3
      from datetime import date

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE o (placed TEXT)")
      con.execute("INSERT INTO o VALUES (?)", ("2025-07-01",))
      placed = con.execute("SELECT placed FROM o").fetchone()[0]
      print((date(2025, 7, 15) - date.fromisoformat(placed)).days)
      """, verify="stdout"),

    Q("b2-145", "2.4.5", 3,
      "What does this code print?",
      ["`[('integer',), ('text',)]`", "`[('integer',), ('integer',)]`", "`[('text',), ('text',)]`", "An IntegrityError is raised"],
      0,
      {1: "\"abc\" can't be converted to an integer, so it is stored as text.",
       2: "The INTEGER affinity converts the numeric text '12' to an integer.",
       3: "SQLite's type affinity doesn't reject values of other types."},
      "SQLite applies type affinity: numeric-looking text becomes an integer, and anything else is stored as it is. Validate types in Python before inserting.",
      "Syllabus 2.4.5 · SQLite docs: type affinity", ["sql-types", "affinity"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE t (qty INTEGER)")
      con.execute("INSERT INTO t VALUES ('12'), ('abc')")
      print(con.execute("SELECT typeof(qty) FROM t").fetchall())
      """, verify="stdout"),

    Q("b2-146", "2.4.5", 3,
      "A DataFrame is written to SQLite with pandas. What does this code print?",
      ["`('text', 'integer', 'integer')`",
       "`('date', 'boolean', 'integer')`",
       "`('text', 'text', 'integer')`",
       "`('real', 'integer', 'integer')`"],
      0,
      {1: "SQLite has no date or boolean storage types.",
       2: "A Python or pandas boolean is stored as the integer 0 or 1.",
       3: "pandas writes datetimes to SQLite as ISO-style text, not as numbers."},
      "SQLite stores only NULL, INTEGER, REAL, TEXT and BLOB. pandas writes the datetime as text (\"2025-07-15 00:00:00\") and the boolean as 1, so both need converting back when read (`parse_dates=`, `astype(bool)`).",
      "Syllabus 2.4.5 · pandas docs · SQLite docs", ["to_sql", "type-conversion", "sqlite"],
      code="""
      import sqlite3
      import pandas as pd

      con = sqlite3.connect(":memory:")
      df = pd.DataFrame({"day": pd.to_datetime(["2025-07-15"]), "paid": [True], "qty": [3]})
      df.to_sql("t", con, index=False)
      print(con.execute("SELECT typeof(day), typeof(paid), typeof(qty) FROM t").fetchone())
      """, verify="stdout"),

    Q("b2-147", "2.4.5", 2,
      "What does this code print?",
      ["`20.00 False 0.3`", "`20.0 True 0.3`", "`20.00 False 0.30000000000000004`", "`20 False 0.3`"],
      0,
      {1: "Decimals keep their two decimal places, and `0.1 + 0.2 == 0.3` is False for floats.",
       2: "Decimal arithmetic is exact: `Decimal(\"0.1\") * 3` is exactly 0.3.",
       3: "Adding 19.99 and 0.01 as Decimals keeps two decimal places: 20.00."},
      "`Decimal` (what MySQL's DECIMAL columns become in Python) stores decimal values exactly and keeps their precision, which is why it suits money. Binary floats can't store 0.1 or 0.2 exactly, so their sum isn't exactly 0.3.",
      "Syllabus 2.4.5 · Python docs (decimal)", ["decimal", "float", "money"],
      code="""
      from decimal import Decimal

      prices = [Decimal("19.99"), Decimal("0.01")]
      print(sum(prices), 0.1 + 0.2 == 0.3, Decimal("0.1") * 3)
      """, verify="stdout"),

    # ---------- 2.4.6 Security ----------
    Q("b2-150", "2.4.6", 2,
      "`user_id` comes from a web form. Which PyMySQL call is vulnerable to SQL injection?",
      ["`cur.execute(\"SELECT * FROM t WHERE id = %s\" % user_id)`",
       "`cur.execute(\"SELECT * FROM t WHERE id = %s\", (user_id,))`",
       "`cur.execute(\"SELECT * FROM t WHERE id = %(id)s\", {\"id\": user_id})`",
       "`cur.executemany(\"INSERT INTO t (id) VALUES (%s)\", [(user_id,)])`"],
      0,
      {1: "The value is passed as a separate argument: parameterized.",
       2: "Named parameters in a dict are also safe.",
       3: "`executemany` with parameter tuples is parameterized."},
      "The `%` operator formats the SQL string in Python before the driver sees it, so the input becomes part of the SQL. Pass values as the second argument instead.",
      "Syllabus 2.4.6", ["sql-injection", "pymysql"]),

    Q("b2-151", "2.4.6", 1,
      "What is the primary defence against SQL injection in Python code?",
      ["Parameterized queries with placeholders", "Escaping quotes by hand", "Blocking words like DROP in user input", "Converting input to uppercase"],
      0,
      {1: "Manual escaping is easy to get wrong and misses edge cases.",
       2: "Blocklists miss countless variations.",
       3: "Changing case changes nothing about safety."},
      "Placeholders keep data separate from SQL code, so input can never change the query's structure.",
      "Syllabus 2.4.6", ["sql-injection", "parameters"]),

    Q("b2-152", "2.4.6", 2,
      "A dashboard only reads sales figures. Which database account should it use?",
      ["A dedicated account with read-only access to the tables it needs",
       "The database administrator account",
       "An account with full rights on every table so it never fails",
       "An anonymous account with no password"],
      0,
      {1: "An admin account turns any bug or injection into full control of the database.",
       2: "Broad rights maximize the damage of a leak.",
       3: "Anyone could connect."},
      "Least privilege: give each account only what it needs, which limits the damage if its credentials leak or its code is exploited.",
      "Syllabus 2.4.6", ["least-privilege", "security"]),

    Q("b2-153", "2.4.6", 2,
      "A shared notebook in version control contains `password=\"S3cret!\"` in its `pymysql.connect(...)` call. What is the best fix?",
      ["Read the password from an environment variable or secrets manager, and rotate the exposed one",
       "Base64-encode the password in the notebook",
       "Move the password into a code comment",
       "Rename the variable to `pwd`"],
      0,
      {1: "Base64 is an encoding, not encryption; anyone can decode it.",
       2: "Comments are still in the file and its history.",
       3: "Renaming hides nothing."},
      "Keep credentials out of code, and treat any password that reached version control as compromised.",
      "Syllabus 2.4.6", ["credentials", "security"]),

    Q("b2-154", "2.4.6", 2,
      "Which two measures reduce the likelihood or the damage of SQL injection? Select two.",
      ["Using parameterized queries for all external input",
       "Running the application with a least-privilege database account",
       "Showing full database error messages to end users",
       "Building queries with f-strings after lowercasing the input",
       "Storing the database password in the source code"],
      [0, 1],
      {2: "Detailed errors help attackers map the database.",
       3: "Lowercasing doesn't stop injection.",
       4: "Hard-coded passwords are a separate security risk."},
      "Parameterization prevents injection; least privilege limits what an attacker could do if something slips through.",
      "Syllabus 2.4.6", ["sql-injection", "defence-in-depth"]),

    Q("b2-155", "2.4.6", 3,
      "Users type a `region` and pick a column to sort by (`sort_col`). Which sqlite3 code is safe from SQL injection and sorts by the chosen column?",
      ["col = sort_col if sort_col in {\"name\", \"total\"} else \"name\"\ncon.execute(f\"SELECT * FROM sales WHERE region = ? ORDER BY {col}\", (region,))",
       "`con.execute(\"SELECT * FROM sales WHERE region = ? ORDER BY ?\", (region, sort_col))`",
       "`con.execute(f\"SELECT * FROM sales WHERE region = ? ORDER BY {sort_col}\", (region,))`",
       "col = sort_col if sort_col in {\"name\", \"total\"} else \"name\"\ncon.execute(f\"SELECT * FROM sales WHERE region = '{region}' ORDER BY {col}\")"],
      0,
      {1: "A placeholder can only stand for a value: `ORDER BY ?` sorts by a constant string, so the rows come back unsorted.",
       2: "`sort_col` goes into the SQL text unchecked, so a crafted value can change the query.",
       3: "The column is checked, but `region` is pasted into the SQL text, so it is injectable."},
      "Values go in placeholders. Identifiers such as column names can't be parameterized, so they are checked against a fixed allow-list before being placed in the SQL.",
      "Syllabus 2.4.6, 2.4.4", ["sql-injection", "allow-list", "placeholders"], optlang="python",
      verify={"py": """
      import sqlite3
      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE sales (name TEXT, region TEXT, total REAL)")
      con.executemany("INSERT INTO sales VALUES (?, ?, ?)", [("b", "EU", 1), ("a", "EU", 3), ("c", "EU", 2)])
      ns = {"con": con, "region": "EU", "sort_col": "total"}
      setup_line, call = opt(0).splitlines()
      exec(setup_line, ns)
      assert [r[2] for r in eval(call, ns).fetchall()] == [1, 2, 3]
      assert [r[2] for r in eval(opt(1), ns).fetchall()] == [1, 3, 2]
      """}),

    Q("b2-156", "2.4.6", 3,
      "A login check builds `f\"SELECT * FROM users WHERE name = '{name}' AND pw_hash = '{h}'\"`. An attacker types `admin' --` as the name and anything as the password. What happens?",
      ["The query returns the admin row: `--` turns the rest of the line, including the password check, into a comment",
       "The query fails with a syntax error, because of the stray quote",
       "It looks for a user literally named \"admin' --\" and finds nobody",
       "Nothing changes, because comments are only allowed at the end of a script"],
      0,
      {1: "The typed quote closes the name string neatly, so the remaining SQL is valid.",
       2: "That is what a parameterized query would do; an f-string makes the input part of the SQL.",
       3: "`--` starts a comment anywhere on a line in SQL."},
      "The SQL becomes `... WHERE name = 'admin' --' AND pw_hash = '...'`. Everything after `--` is a comment, so only the name is checked. Placeholders stop this, because the input can never close the string or start a comment.",
      "Syllabus 2.4.6", ["sql-injection", "comments", "authentication"],
      verify={"py": """
      import sqlite3
      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE users (name TEXT, pw_hash TEXT)")
      con.execute("INSERT INTO users VALUES ('admin', 'secret'), ('ben', 'other')")
      name, h = "admin' --", "wrong"
      rows = con.execute(f"SELECT * FROM users WHERE name = '{name}' AND pw_hash = '{h}'").fetchall()
      assert rows == [('admin', 'secret')], rows
      safe = con.execute("SELECT * FROM users WHERE name = ? AND pw_hash = ?", (name, h)).fetchall()
      assert safe == [], safe
      """}),

    Q("b2-157", "2.4.6", 2,
      "Which two measures are not reliable defences against SQL injection on their own? Select two.",
      ["Replacing each `'` in the input with `''` by hand before building the SQL",
       "Rejecting input that contains words such as DROP or DELETE",
       "Passing every value through placeholders",
       "Checking user-chosen column names against a fixed allow-list",
       "Giving the application's account read-only access to the tables it needs"],
      [0, 1],
      {2: "Placeholders are the primary defence: values can never change the query.",
       3: "Allow-lists are the right defence for identifiers, which placeholders can't cover.",
       4: "Least privilege limits the damage if anything gets through."},
      "Hand-escaping misses edge cases (other quote styles, encodings, numeric contexts), and word blacklists are easy to bypass and block legitimate text. Use placeholders for values, allow-lists for identifiers, and least privilege to limit damage.",
      "Syllabus 2.4.6", ["sql-injection", "defences"]),
]
