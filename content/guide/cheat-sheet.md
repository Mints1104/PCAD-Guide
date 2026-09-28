# Cheat sheet

The distinctions the exam leans on most, one table each. Read it the evening before.

## Exam blocks and items

| Block | Items | Weight |
|---|---|---|
| 1 Data Acquisition and Pre-Processing | 14 | 29.2% |
| 2 Programming and Database Skills | 16 | 33.3% |
| 3 Statistical Analysis | 4 | 8.3% |
| 4 Data Analysis and Modeling | 9 | 18.8% |
| 5 Data Communication and Visualization | 5 | 10.4% |
| **Total** | **48 in 60 min, pass at 75%** | |

## MCAR vs MAR vs MNAR

| | Missingness depends on | Example |
|---|---|---|
| MCAR | Nothing | Sensor fails at random |
| MAR | Other observed variables | Younger people skip income; age is recorded |
| MNAR | The missing value itself | High earners hide income because it is high |

## Min-max vs z-score; one-hot vs label

| | Formula / output | Use when |
|---|---|---|
| Min-max | (x − min)/(max − min) → [0, 1] | Bounded range needed; few outliers |
| Z-score | (x − mean)/std → mean 0, std 1 | Centring; unbounded values fine |
| One-hot | One 0/1 column per category | Nominal categories |
| Label | One integer per category | Target labels, trees, ordinal with true order |

## `pd.cut` vs `pd.qcut`

| | Bins by | Result |
|---|---|---|
| `cut` | Edges you give; right-closed `(a, b]` | Unequal counts; out-of-range → NaN |
| `qcut` | Quantiles | About equal counts per bin |

## Validation checks

| Check | Example |
|---|---|
| Type | `qty` is an integer |
| Range | `0 <= age <= 120` |
| Format | Email matches a pattern |
| Cross-field | `end >= start` in the same row |
| Cross-reference | `customer_id` exists in customers table |

## File formats in Python

| Format | Read | Write |
|---|---|---|
| CSV | `pd.read_csv`, `csv.reader` | `df.to_csv(index=False)` |
| JSON (file / string) | `json.load(f)` / `json.loads(s)` | `json.dump(o, f)` / `json.dumps(o)` |
| XML | `ET.parse(p).getroot()`, `findall`, `.text`, `.get()` | `tree.write(p)` |
| HTML | `BeautifulSoup(html, "html.parser")`, `find` / `find_all` | — |

## HTTP status codes

| Code | Meaning |
|---|---|
| 200 | OK |
| 401 / 403 | Not authenticated / not allowed |
| 404 | Not found |
| 429 | Too many requests: slow down |
| 500 | Server error |

## Python operators and truthiness

| Expression | Result |
|---|---|
| `7 / 2`, `7 // 2`, `7 % 2`, `-7 // 2` | `3.5`, `3`, `1`, `-4` |
| `range(1, 10, 3)` | 1, 4, 7 |
| Falsy | `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`, `False` |
| `[1, 2] * 2` vs `np.array([1, 2]) * 2` | `[1, 2, 1, 2]` vs `[2 4]` |

## Data structures

| | Ordered | Mutable | Duplicates | Empty |
|---|---|---|---|---|
| list | Yes | Yes | Yes | `[]` |
| tuple | Yes | No | Yes | `()`; one item `(5,)` |
| set | No | Yes | No | `set()` |
| dict | Insertion | Yes | Unique keys | `{}` |
| str | Yes | No | Yes | `""` |

## Functions

| Rule | Example |
|---|---|
| Positional before keyword in a call | `f(1, b=2)` ✓ `f(a=1, 2)` ✗ SyntaxError |
| Required before optional in a definition | `def f(a, b=2)` ✓ `def f(a=1, b)` ✗ |
| `*args` / `**kwargs` | tuple / dict |
| No `return` | returns `None` |
| Mutable default | shared across calls: use `None` |

## try / except / else / finally

| Block | Runs when |
|---|---|
| `try` | Always first |
| `except X` | X (or a subclass) was raised; first matching clause only |
| `else` | No exception was raised |
| `finally` | Always, even after `return` |

## Which exception?

| Code | Raises |
|---|---|
| `int("12a")` | ValueError |
| `"3" + 4` | TypeError |
| `{"a": 1}["b"]`, `df["missing"]` | KeyError |
| `[1, 2][5]` | IndexError |
| `1 / 0` | ZeroDivisionError |
| `None.upper()` | AttributeError |
| `import nothere` | ModuleNotFoundError |

## OOP essentials

| Concept | Meaning |
|---|---|
| `_x` | Internal by convention (not enforced) |
| `__x` | Name-mangled to `_Class__x` |
| `==` / `is` | Same value / same object |
| No `__eq__` | Instances compare by identity |
| Inheritance / composition | is-a / has-a |
| `super().__init__()` | Run the parent constructor |

## PEP 8 and PEP 257 numbers

| Rule | Value |
|---|---|
| Indent | 4 spaces |
| Line length | 79 (72 for comments and docstrings) |
| Blank lines | 2 around top-level defs, 1 between methods |
| Names | `snake_case` functions/variables, `CapWords` classes, `UPPER_CASE` constants |
| Docstrings | `"""Triple double quotes."""`, imperative summary line |

## pip

| Task | Command |
|---|---|
| Install / exact version | `pip install pkg` / `pip install pkg==1.2.3` |
| Upgrade | `pip install --upgrade pkg` |
| Remove | `pip uninstall pkg` |
| Record / restore | `pip freeze > requirements.txt` / `pip install -r requirements.txt` |

## SQL: written vs logical order

| Order | Sequence |
|---|---|
| Written (SFJWGHOL) | SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT |
| Logical (evaluated) | FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT |

## Joins

| Join | Keeps |
|---|---|
| INNER | Matches only |
| LEFT | All left + matches |
| RIGHT | All right + matches |
| FULL OUTER | Everything from both |

## WHERE vs HAVING; NULLs

| | |
|---|---|
| WHERE | Filters rows, before grouping, no aggregates |
| HAVING | Filters groups, after grouping, aggregates allowed |
| `COUNT(*)` vs `COUNT(col)` | All rows vs non-NULL values |
| NULL test | `IS NULL`, never `= NULL` |
| `BETWEEN a AND b` | Inclusive |

## sqlite3 vs pymysql

| | sqlite3 | pymysql |
|---|---|---|
| Connect | `sqlite3.connect("file.db")` | `pymysql.connect(host=, user=, password=, database=)` |
| Placeholder | `?` or `:name` | `%s` or `%(name)s` |
| Save changes | `con.commit()` | `con.commit()` |
| One param | `(value,)` | `(value,)` |

## SQL ↔ Python types

| SQLite | Python |
|---|---|
| NULL | None |
| INTEGER | int (bool stored as 0/1) |
| REAL | float |
| TEXT | str (dates stored as ISO text) |
| BLOB | bytes |
| MySQL DECIMAL / DATE | `decimal.Decimal` / `datetime.date` |

## pandas selection

| Code | Returns |
|---|---|
| `df["a"]` / `df[["a"]]` | Series / DataFrame |
| `df.loc["b":"d"]` | Labels b to d **inclusive** |
| `df.iloc[1:3]` | Positions 1 and 2 (end **excluded**) |
| `df.loc[0:2]` vs `df.iloc[0:2]` (default index) | 3 rows vs 2 rows |
| `df.loc[mask, "col"] = v` | Conditional update |

## Combining and reshaping

| Tool | Does | Default |
|---|---|---|
| `merge` | Join on key columns | `how="inner"` |
| `join` | Join on index | `how="left"` |
| `concat` | Stack rows or columns | `axis=0` |
| `pivot` | Long → wide, no duplicates allowed | — |
| `pivot_table` | Long → wide with aggregation | `aggfunc="mean"` |
| `melt` | Wide → long | — |
| `crosstab` | Count combinations | counts |

## groupby

| | |
|---|---|
| `agg` | One row per group |
| `transform` | Same length as original |
| `size()` / `count()` | Rows incl. NaN / non-null values |
| Flatten keys | `as_index=False` or `.reset_index()` |

## pandas vs NumPy defaults

| | pandas | NumPy |
|---|---|---|
| NaN in `mean` | Skipped | Returns nan (use `nanmean`) |
| `std` / `var` ddof | 1 (sample) | 0 (population) |
| `mode` | Series (can be several) | `scipy.stats.mode` |

## Broadcasting

| Shapes | Result |
|---|---|
| (2, 3) + (3,) | (2, 3) |
| (3, 1) + (1, 4) | (3, 4) |
| (2, 3) + (2,) | ValueError |
| `sum(axis=0)` on 2-D | One value per column |

## Centre and spread

| Data | Best centre |
|---|---|
| Symmetric numeric | Mean |
| Skewed or with outliers | Median |
| Categories | Mode |
| Right skew | Mean > median |

## Pearson's r

| r | Reading |
|---|---|
| ±1 | Perfect linear |
| ≳ ±0.7 | Strong |
| ±0.3 to ±0.7 | Moderate |
| ≈ 0 | No **linear** link (curves possible) |

## Bootstrapping

| Setting | Value |
|---|---|
| Resample size | Same as original n |
| Replacement | **With** |
| 95% interval | 2.5th and 97.5th percentiles |
| Can't fix | Biased or tiny samples |

## Linear vs logistic regression

| | Linear | Logistic |
|---|---|---|
| Target | Continuous | Binary |
| Output | Any number | Probability 0–1 |
| Fit | Least squares | Maximum likelihood |
| `.score()` in scikit-learn | R² | Accuracy |

## Model fit

| Train | Test | Diagnosis | Fix |
|---|---|---|---|
| Low | Low | Underfitting (high bias) | More features / flexible model |
| High | High | Good fit | — |
| Very high | Much lower | Overfitting (high variance) | More data, simpler model, regularization |

## Chart chooser

| Question | Chart |
|---|---|
| Trend over time | Line |
| Compare categories | Bar (sorted, axis from 0) |
| One variable's distribution | Histogram / box plot |
| Distribution by group | Side-by-side box plots |
| Two numeric variables | Scatter |
| Many correlations | Heatmap |
| Part of a whole (≤ 5 parts) | Pie or stacked bar |

## Palettes

| Data | Palette |
|---|---|
| Unordered groups | Qualitative (`"colorblind"`, `"tab10"`) |
| Low → high | Sequential (`"viridis"`) |
| Around a midpoint | Diverging (`"coolwarm"`, centre 0) |

## Chart calls

| Task | Call |
|---|---|
| Title / labels | `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel` |
| Legend | `label=` on series, `ax.legend(loc=, fontsize=, facecolor=)` |
| Arrow to a point | `ax.annotate(text, xy=, xytext=, arrowprops=)` |
| Save | `fig.savefig("f.png", dpi=150)` before `plt.show()` |
