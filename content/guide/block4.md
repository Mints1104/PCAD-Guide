# Block 4: Data Analysis and Modeling

Block 4 is 9 items, 18.8% of the exam: hands-on pandas and NumPy (cleaning, merging, reshaping, selecting, grouping), descriptive statistics in code, and the basics of supervised learning. Expect short snippets where you predict the output or pick the line that produces a given table.

All examples here were run with pandas 3 and NumPy 2. Behaviour that differs from pandas 2 is flagged.

## 4.1.1 Organize and clean data using pandas

**Syllabus asks:** filter and sort data, and manage missing or inconsistent values with foundational cleaning techniques.

### Core facts

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "city": ["Oslo", "oslo ", "Rome", "Rome", None],
    "sales": [120, 120, np.nan, 90, 40],
})
df["city"] = df["city"].str.strip().str.title()
print(df.isna().sum().to_dict())
print(df.drop_duplicates().shape, df.dropna().shape, df.dropna(subset=["sales"]).shape)
print(df.fillna({"city": "Unknown", "sales": 0})["sales"].tolist())
print(df.sort_values("sales", ascending=False, na_position="last")["sales"].tolist())
```

```text
{'city': 1, 'sales': 1}
(4, 2) (3, 2) (4, 2)
[120.0, 120.0, 0.0, 90.0, 40.0]
[120.0, 120.0, 90.0, 40.0, nan]
```

| Task | Method |
|---|---|
| Find missing values | `isna()` / `notna()`, `isna().sum()` |
| Drop missing | `dropna()` (any NaN in the row), `how="all"`, `subset=[...]`, `thresh=n` (keep rows with at least n non-NaN), `axis=1` for columns |
| Fill missing | `fillna(value)` or `fillna({"col": value})`; `ffill()` / `bfill()`; `interpolate()` |
| Duplicates | `duplicated(subset, keep="first")`, `drop_duplicates(...)` |
| Inconsistent text | `.str.strip()`, `.str.lower()`, `.replace({"NY": "New York"})`, `.map(...)` |
| Wrong types | `astype()`, `pd.to_numeric(errors="coerce")`, `pd.to_datetime(errors="coerce")` |
| Filter | `df[mask]`, `df.query("sales > 100")`, `isin`, `between`, `.str.contains` |
| Sort | `sort_values(by, ascending)`, `sort_index()`, `nlargest(n, col)` |
| Columns | `rename(columns={...})`, `drop(columns=[...])` |

**Methods give you a new DataFrame.** Methods like `dropna`, `fillna`, `drop_duplicates` and `sort_values` don't change your DataFrame. They return a changed **copy**, and you have to store it, usually back in the same name.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ana", "Ana", "Ben"], "sales": [10, 10, 5]})

df.drop_duplicates()              # the result is thrown away
print(len(df))                    # still 3 rows

df = df.drop_duplicates()         # store the result
print(len(df))
```

```text
3
2
```

**`inplace=True` returns `None`.** With `inplace=True`, the method changes the DataFrame itself and returns `None`. Never combine it with `df = ...`, or you replace your data with `None`.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ana", "Ana", "Ben"], "sales": [10, 10, 5]})

result = df.drop_duplicates(inplace=True)
print(result)                     # None
print(len(df))                    # df itself was changed
```

```text
None
2
```

**`dropna()` drops a row if any value is missing.** With no arguments it removes every row that has a `NaN` in **any** column. `subset=` limits the check to the columns you name.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"city": ["Oslo", None, "Rome"], "sales": [10, 20, np.nan]})

print(len(df.dropna()))                     # rows 1 and 2 both have a gap
print(len(df.dropna(subset=["sales"])))     # only row 2 is missing sales
```

```text
1
2
```

**`drop_duplicates()` compares whole rows.** Two rows count as duplicates only if **every** column matches. `subset=` compares only the columns you name.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ana", "Ana", "Ben"], "city": ["Oslo", "Rome", "Oslo"]})

print(len(df.drop_duplicates()))                    # the Ana rows differ in city
print(len(df.drop_duplicates(subset=["name"])))     # same name counts as a duplicate
```

```text
3
2
```

**Changing values that match a condition.** Use `df.loc[condition, "column"] = value`. The condition picks the rows; the column name picks what to change.

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ana", "Ben", "Cy"], "sales": [10, -5, 7]})

df.loc[df["sales"] < 0, "sales"] = 0        # negative sales become 0
print(df["sales"].tolist())
```

```text
[10, 0, 7]
```

Don't write it as two separate selections, `df[df["sales"] < 0]["sales"] = 0`. The first part makes a temporary copy, so the change is made to the copy, not to `df`. Under pandas 3 it never changes `df`.

### Exam traps

> **Trap.** `df = df.dropna(inplace=True)` sets `df` to `None`.

> **Trap.** `fillna(df.mean())` on a whole DataFrame with text columns: use `df.mean(numeric_only=True)`.

## 4.1.2 Merge and reshape datasets using pandas

**Syllabus asks:** merge, join, pivot and reshape DataFrames to structure datasets for an analysis.

### Core facts

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2, 3, 4], "cust": ["a", "b", "b", "z"], "amount": [50, 20, 30, 70]})
custs = pd.DataFrame({"cust": ["a", "b", "c"], "region": ["EU", "US", "EU"]})

print(orders.merge(custs, on="cust").shape)                 # inner: unmatched rows dropped
print(orders.merge(custs, on="cust", how="left").shape)     # all orders kept
print(orders.merge(custs, on="cust", how="outer").shape)    # everything from both
print(pd.concat([custs, custs], ignore_index=True).shape)   # stacked rows
```

```text
(3, 4)
(4, 4)
(5, 4)
(6, 2)
```

| Tool | Combines | Key facts |
|---|---|---|
| `pd.merge(a, b)` / `a.merge(b)` | Columns side by side, matched on key columns | `how="inner"` by default; `on=`, or `left_on=`/`right_on=`; clashing names get `_x`/`_y` suffixes |
| `a.join(b)` | Columns side by side, matched on the **index** | `how="left"` by default |
| `pd.concat([a, b])` | Rows stacked (`axis=0`) or columns side by side (`axis=1`) | Aligns on column names (NaN where missing); `ignore_index=True` renumbers |

If a key appears several times on **both** sides, the merge produces every combination for that key (many-to-many), so the row count can grow a lot.

**Reshaping.**

| Tool | Does |
|---|---|
| `df.pivot(index, columns, values)` | Long → wide; fails if an index/column pair repeats |
| `df.pivot_table(values, index, columns, aggfunc="mean")` | Long → wide with aggregation of repeats; `fill_value=`, `margins=True` for totals |
| `df.melt(id_vars, value_vars, var_name, value_name)` | Wide → long |
| `stack()` / `unstack()` | Move a level between the columns and the index |

```python
import pandas as pd

sales = pd.DataFrame({"region": ["EU", "EU", "US", "US", "EU"],
                      "quarter": ["Q1", "Q2", "Q1", "Q2", "Q1"],
                      "revenue": [10, 12, 8, 9, 4]})
print(sales.pivot_table(values="revenue", index="region", columns="quarter", aggfunc="sum"))
```

```text
quarter  Q1  Q2
region
EU       14  12
US        8   9
```

### Exam traps

> **Trap.** `merge` defaults to an **inner** join; rows without a match disappear silently.

> **Trap.** `pivot_table` defaults to `aggfunc="mean"`, not sum.

## 4.1.3 Understand the relationship between Series and DataFrames

**Syllabus asks:** the conceptual differences and connections between Series and DataFrames; indexing; vectorized functions.

### Core facts

- A **Series** is a one-dimensional labeled array: values of one dtype plus an index.
- A **DataFrame** is a two-dimensional table: a collection of Series (columns) that share one row index. Columns can have different dtypes.
- `df["col"]` returns a **Series**; `df[["col"]]` (a list of names) returns a one-column **DataFrame**. A single row, `df.loc[label]` or `df.iloc[0]`, also comes back as a Series indexed by the column names.

```python
import pandas as pd

s1 = pd.Series([10, 20, 30], index=["a", "b", "c"])
s2 = pd.Series([1, 2, 3], index=["b", "c", "d"])
print((s1 + s2).tolist())                     # aligned on labels, not positions
df = pd.DataFrame({"x": [1, 2], "y": [3.5, 4.5]})
print(type(df["x"]).__name__, type(df[["x"]]).__name__, df.shape, df["x"].shape)
print((df["x"] * 10 + df["y"]).tolist())      # vectorized: no loop
```

```text
[nan, 21.0, 32.0, nan]
Series DataFrame (2, 2) (2,)
[13.5, 24.5]
```

**Arithmetic lines up labels, not positions.** When you add two Series, pandas pairs values with the **same index label**. A label that exists on only one side has nothing to pair with, so the result there is `NaN`. In the example above, `a` and `d` each appear on only one side.

**Vectorized operations.** Writing `s * 2` applies the operation to every value at once, with no loop. These operations run in fast compiled code, so they are much quicker than a Python `for` loop or `.apply()` with a `lambda`.

```python
import pandas as pd

prices = pd.Series([2.5, 4.0, 3.0])
print((prices * 2).tolist())                 # every value doubled
print((prices > 3).tolist())                 # a True/False for every value

names = pd.Series(["tea", "jam"])
print(names.str.upper().tolist())            # every string uppercased
```

```text
[5.0, 8.0, 6.0]
[False, True, False]
['TEA', 'JAM']
```

**The index labels the rows.** `set_index("id")` turns a column into the index, so you can look rows up by that value. `reset_index()` turns the index back into an ordinary column. A single row comes back as a Series, labelled by the column names.

```python
import pandas as pd

df = pd.DataFrame({"id": [101, 102], "q1": [5, 3], "q2": [7, 1]})

df = df.set_index("id")
print(df.loc[102].to_dict())                 # look up the row whose id is 102

print(df.reset_index().columns.tolist())     # id is a normal column again
```

```text
{'q1': 3, 'q2': 1}
['id', 'q1', 'q2']
```

**`axis=0` and `axis=1`.** `axis=0` works **down** the rows, giving one result per column. `axis=1` works **across** the columns, giving one result per row.

```python
import pandas as pd

df = pd.DataFrame({"q1": [5, 3], "q2": [7, 1]}, index=["Ana", "Ben"])

print(df.sum(axis=0).to_dict())    # total for each column
print(df.sum(axis=1).to_dict())    # total for each row
```

```text
{'q1': 8, 'q2': 8}
{'Ana': 12, 'Ben': 4}
```

**Just the values: `.to_numpy()`.** `.to_numpy()` returns the data as a plain NumPy array, without the row and column labels.

```python
import pandas as pd

df = pd.DataFrame({"q1": [5, 3], "q2": [7, 1]}, index=["Ana", "Ben"])
print(df.to_numpy())
```

```text
[[5 7]
 [3 1]]
```

### Exam traps

> **Trap.** `df["x"]` is a Series and `df[["x"]]` is a DataFrame. Methods such as `.to_frame()` or `.squeeze()` convert between them.

> **Trap.** Adding two Series with different indexes does not add by position; mismatched labels become NaN.

## 4.1.4 Access and manipulate data using locators and slicing

**Syllabus asks:** use `.loc` and `.iloc` to retrieve and modify data; slicing and conditional selection; indexing strategies for efficiency.

### Core facts

| | `.loc` | `.iloc` |
|---|---|---|
| Selects by | Labels (index and column names) or a boolean mask | Integer positions |
| Slice end | **Included** | **Excluded** (like Python) |
| Example | `df.loc["b":"d", "price"]` | `df.iloc[1:4, 0]` |

```python
import pandas as pd

df = pd.DataFrame({"price": [5, 8, 3, 9, 6], "qty": [1, 4, 2, 7, 3]}, index=list("abcde"))
print(df.loc["b":"d", "price"].tolist())          # b, c, d
print(df.iloc[1:3, 0].tolist())                   # positions 1 and 2
print(df.loc[df["qty"] > 2, "price"].tolist())    # boolean mask + column label
print(df.iloc[-1].tolist(), df.at["c", "qty"])
df.loc[df["price"] < 5, "qty"] = 0                # conditional update
print(df["qty"].tolist())
```

```text
[8, 3, 9]
[8, 3]
[8, 9, 6]
[6, 3] 2
[1, 4, 0, 7, 3]
```

**Rows and columns together.** Both `.loc` and `.iloc` take `[rows, columns]`. Each part can be one item, a list, or a slice (`start:end`). `.loc` can also take a True/False condition for the rows.

```python
import pandas as pd

df = pd.DataFrame({"price": [5, 8, 3], "qty": [1, 4, 2]}, index=["a", "b", "c"])

print(df.loc["b", "price"])                   # one row label, one column label
print(df.loc[["a", "c"], "qty"].tolist())     # a list of row labels
print(df.iloc[0, 1])                          # row 0, column 1 (by position)
print(df.loc[df["qty"] > 1, "price"].tolist())   # rows where qty > 1
```

```text
8
[1, 2]
1
[8, 3]
```

**Whole rows and whole columns.** A bare `:` means "all". So `df.iloc[0]` is the first row, `df.iloc[:, 0]` is the first column, and `-1` counts from the end.

```python
import pandas as pd

df = pd.DataFrame({"price": [5, 8, 3], "qty": [1, 4, 2]}, index=["a", "b", "c"])

print(df.iloc[0].to_dict())          # first row
print(df.iloc[:, 0].tolist())        # first column, all rows
print(df.iloc[-1].to_dict())         # last row
```

```text
{'price': 5, 'qty': 1}
[5, 8, 3]
{'price': 3, 'qty': 2}
```

**One value, quickly: `.at` and `.iat`.** `.at[row_label, column]` and `.iat[row_position, column_position]` get or set a single cell. They work like `.loc` and `.iloc` but only for one value, and they're faster.

```python
import pandas as pd

df = pd.DataFrame({"price": [5, 8, 3]}, index=["a", "b", "c"])
print(df.at["b", "price"], df.iat[2, 0])
```

```text
8 3
```

**Plain brackets.** Without `.loc` or `.iloc`, square brackets do three different things depending on what you put inside:

```python
import pandas as pd

df = pd.DataFrame({"price": [5, 8, 3, 9], "qty": [1, 4, 2, 7]})

print(df["price"].tolist())          # a column name: that column
print(df[1:3]["price"].tolist())     # a slice: rows by position (1 and 2)
print(df[df["qty"] > 3]["price"].tolist())   # a condition: the matching rows
```

```text
[5, 8, 3, 9]
[8, 3]
[8, 9]
```

**The default-index trap.** With the default index 0, 1, 2…, the labels and positions are the same numbers. But `.loc` includes the end label and `.iloc` doesn't, so the same-looking slice gives a different number of rows:

```python
import pandas as pd

df = pd.DataFrame({"v": [10, 20, 30, 40]})     # index 0, 1, 2, 3

print(df.loc[0:2, "v"].tolist())     # labels 0, 1 and 2: three rows
print(df.iloc[0:2, 0].tolist())      # positions 0 and 1: two rows
```

```text
[10, 20, 30]
[10, 20]
```

**When labels and positions differ.** With a non-default index, `.loc` and `.iloc` can return completely different items for the same number:

```python
import pandas as pd

s = pd.Series(["w", "x", "y", "z"], index=[3, 2, 1, 0])

print(s.loc[1])      # the item labelled 1
print(s.iloc[1])     # the item in position 1 (the second one)
```

```text
y
x
```

**Indexing for speed.** If you often look rows up by an ID or a date, make that column the index (`set_index`) and keep it sorted. Label lookups and date ranges are then fast. Prefer conditions like `df[df["qty"] > 3]` to looping over rows.

### Exam traps

> **Trap.** `.loc` includes the end label; `.iloc` excludes the end position.

> **Trap.** With a non-default index (for example labels 3, 2, 1, 0), `s.loc[1]` looks up the **label** 1 while `s.iloc[1]` takes the **second** item: they return different values.

## 4.1.5 Perform array operations and distinguish data structures

**Syllabus asks:** NumPy arithmetic, broadcasting and aggregations; tell arrays, lists, Series, DataFrames and NDArrays apart and choose between them.

### Core facts

```python
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape, a.ndim, a.dtype, a.size)
print(a * 2)
print(a + np.array([10, 20, 30]))              # (2,3) + (3,) broadcasts across rows
print(a.sum(), a.sum(axis=0), a.mean(axis=1))
print(a[a > 3], [1, 2] * 2, np.array([1, 2]) * 2)
```

```text
(2, 3) 2 int64 6
[[ 2  4  6]
 [ 8 10 12]]
[[11 22 33]
 [14 25 36]]
21 [5 7 9] [2. 5.]
[4 5 6] [1, 2, 1, 2] [2 4]
```

**Broadcasting.** Compare shapes from the right. Two dimensions are compatible if they are equal or one of them is 1; the size-1 dimension is stretched. `(2, 3) + (3,)` works; `(3, 1) + (1, 4)` gives `(3, 4)`; `(2, 3) + (2,)` fails with a `ValueError`.

**Aggregations.** `sum`, `mean`, `min`, `max`, `std` (ddof=0), `argmax`, `cumsum`. `axis=0` collapses rows (one result per column); `axis=1` collapses columns (one result per row). `np.nanmean` and friends skip NaN; plain `np.mean` returns `nan` if any value is NaN.

| Structure | Dimensions | Labels | Types | Choose it for |
|---|---|---|---|---|
| `list` | 1 (nest for more) | Positions | Mixed | General Python collections; `* 2` repeats, `+` concatenates |
| NumPy `ndarray` | Any (`ndim`) | Positions | **One** dtype | Fast numeric computing; element-wise math |
| pandas `Series` | 1 | Index labels | One dtype | One labeled column |
| pandas `DataFrame` | 2 | Row index + column names | One per column | Tables with mixed column types |

Mixing types in one array upcasts: `np.array([1, 2.5])` is float; `np.array([1, "a"])` is all strings. `a * b` on arrays is element-wise; use `a @ b` for matrix multiplication.

### Exam traps

> **Trap.** `[1, 2] * 2` is `[1, 2, 1, 2]`; `np.array([1, 2]) * 2` is `[2, 4]`.

> **Trap.** `axis=0` gives per-**column** results for a 2-D array, not per row.

## 4.1.6 Group, summarize and extract insights

**Syllabus asks:** use `groupby()` and summary tables; pivot and cross-tabulation; descriptive statistics with pandas and NumPy to spot trends.

### Core facts

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "channel": ["web", "shop", "web", "web", "shop"],
                   "amount": [100, 40, 70, 30, 60]})
print(df.groupby("region")["amount"].sum().to_dict())
print(df.groupby("region").agg(total=("amount", "sum"), orders=("amount", "count")))
print(pd.crosstab(df["region"], df["channel"]))
df["share"] = df["amount"] / df.groupby("region")["amount"].transform("sum")
print(df["share"].round(2).tolist())
```

```text
{'EU': 140, 'US': 160}
        total  orders
region
EU        140       2
US        160       3
channel  shop  web
region
EU          1    1
US          1    2
[0.71, 0.29, 0.44, 0.19, 0.38]
```

**How `groupby` works: split, apply, combine.** `groupby("region")` **splits** the rows into one group per region, **applies** a calculation to each group separately, then **combines** the answers into one result.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "amount": [100, 40, 70, 30, 60]})

print(df.groupby("region")["amount"].sum())
```

```text
region
EU    140
US    160
Name: amount, dtype: int64
```

EU's rows (100 and 40) add up to 140; US's rows (70, 30 and 60) add up to 160.

**`agg`: one row per group.** `agg` reduces each group to a single row. Named aggregation, `new_name=("column", "function")`, lets you choose the output column names.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "amount": [100, 40, 70, 30, 60]})

print(df.groupby("region").agg(total=("amount", "sum"), orders=("amount", "count")))
```

```text
        total  orders
region
EU        140       2
US        160       3
```

**`transform`: one value per original row.** `transform` works out the same group result but gives it back to **every row** of the group, so the result is as long as the original table. That makes it easy to compare each row with its group, for example as a share of the group total.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "amount": [100, 40, 70, 30, 60]})

df["region_total"] = df.groupby("region")["amount"].transform("sum")
df["share"] = (df["amount"] / df["region_total"]).round(2)
print(df)
```

```text
  region  amount  region_total  share
0     EU     100           140   0.71
1     EU      40           140   0.29
2     US      70           160   0.44
3     US      30           160   0.19
4     US      60           160   0.38
```

Every EU row gets 140, every US row gets 160, and each share is the row's amount divided by its group total.

**`filter`: keep or drop whole groups.** `filter` runs a test on each group and keeps all its rows if the test is true. Here, only regions with more than 2 rows are kept:

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "amount": [100, 40, 70, 30, 60]})

print(df.groupby("region").filter(lambda group: len(group) > 2))
```

```text
  region  amount
2     US      70
3     US      30
4     US      60
```

(`lambda group: len(group) > 2` is a small unnamed function: it takes a group and returns True or False.)

**`size` versus `count`.** `size()` counts the **rows** in each group. `count()` counts only the values that **aren't missing**.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US"],
                   "amount": [100, np.nan, 70]})

print(df.groupby("region").size().to_dict())
print(df.groupby("region")["amount"].count().to_dict())
```

```text
{'EU': 2, 'US': 1}
{'EU': 1, 'US': 1}
```

EU has 2 rows, but only 1 of them has an amount.

**Grouping by two columns.** Pass a list of columns to group by every combination. The result has a two-level index (a **MultiIndex**); `as_index=False` gives ordinary columns instead, which are easier to work with.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "channel": ["web", "shop", "web", "web", "shop"],
                   "amount": [100, 40, 70, 30, 60]})

print(df.groupby(["region", "channel"], as_index=False)["amount"].sum())
```

```text
  region channel  amount
0     EU    shop      40
1     EU     web     100
2     US    shop      60
3     US     web     100
```

**`crosstab`: counting combinations.** `pd.crosstab(a, b)` counts how many rows have each combination of two columns. `margins=True` adds row and column totals; `normalize="index"` turns each row into shares that add up to 1.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "channel": ["web", "shop", "web", "web", "shop"]})

print(pd.crosstab(df["region"], df["channel"], margins=True))
print(pd.crosstab(df["region"], df["channel"], normalize="index").round(2))
```

```text
channel  shop  web  All
region
EU          1    1    2
US          1    2    3
All         2    3    5
channel  shop   web
region
EU       0.50  0.50
US       0.33  0.67
```

US had 3 orders: 2 web and 1 shop, so its shares are 0.67 and 0.33.

**`pivot_table`: summarizing a value.** `pivot_table` lays out the same kind of grid, but fills it with a calculation on a value column. Its default calculation is the **mean**; pass `aggfunc="sum"` for totals.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "channel": ["web", "shop", "web", "web", "shop"],
                   "amount": [100, 40, 70, 30, 60]})

print(pd.pivot_table(df, index="region", columns="channel", values="amount"))
print(pd.pivot_table(df, index="region", columns="channel", values="amount", aggfunc="sum"))
```

```text
channel  shop    web
region
EU       40.0  100.0
US       60.0   50.0
channel  shop  web
region
EU         40  100
US         60  100
```

The US web cell is 50 in the first table, the average of 70 and 30, and 100 in the second, their sum.

**Shares of one column: `value_counts`.** `value_counts()` counts each value in a column; `normalize=True` gives shares instead.

```python
import pandas as pd

channel = pd.Series(["web", "shop", "web", "web", "shop"])
print(channel.value_counts().to_dict())
print(channel.value_counts(normalize=True).to_dict())
```

```text
{'web': 3, 'shop': 2}
{'web': 0.6, 'shop': 0.4}
```

**Trends over time.** To compare periods, group by part of a date, such as the month (`.dt.to_period("M")`), then use `pct_change()` to get the change from one period to the next. (On a date index, `resample("ME")` does the same monthly grouping.)

```python
import pandas as pd

sales = pd.DataFrame({
    "date": pd.to_datetime(["2025-01-05", "2025-01-20", "2025-02-11", "2025-03-02"]),
    "amount": [100, 50, 180, 135],
})

monthly = sales.groupby(sales["date"].dt.to_period("M"))["amount"].sum()
print(monthly.tolist())                       # January, February, March
print(monthly.pct_change().round(2).tolist())
```

```text
[150, 180, 135]
[nan, 0.2, -0.25]
```

February (180) is 20% up on January (150), and March (135) is 25% down on February. January has no previous month, so its change is `NaN`.

### Exam traps

> **Trap.** `crosstab` counts by default; `pivot_table` averages by default.

> **Trap.** `transform` keeps the original row count; `agg` returns one row per group.

## 4.2.1 Apply Python's descriptive statistics

**Syllabus asks:** calculate and interpret mean, median, mode, variance and standard deviation with pandas and NumPy on real datasets.

### Core facts

```python
import numpy as np
import pandas as pd

s = pd.Series([3, 7, 7, 2, 9, np.nan])
print(s.mean(), s.median(), s.mode().tolist(), s.count())
print(round(s.var(), 2), round(s.std(), 2), round(np.nanstd(s.to_numpy()), 2))
print(np.mean(s.to_numpy()), s.to_numpy().mean() if not s.isna().any() else "nan present")
print(s.describe().round(2).to_dict())
```

```text
5.6 7.0 [7.0] 5
8.8 2.97 2.65
nan nan present
{'count': 5.0, 'mean': 5.6, 'std': 2.97, 'min': 2.0, '25%': 3.0, '50%': 7.0, '75%': 7.0, 'max': 9.0}
```

**Missing values: pandas skips them, NumPy doesn't.** pandas ignores `NaN` when it calculates (`skipna=True` is the default). NumPy doesn't, so a single `NaN` makes the whole result `nan`. NumPy's `nan` versions (`np.nanmean`, `np.nanstd`) skip them.

```python
import numpy as np
import pandas as pd

values = [3, 7, np.nan]

print(pd.Series(values).mean())    # skips the NaN: (3 + 7) / 2
print(np.mean(values))             # the NaN spreads to the result
print(np.nanmean(values))          # skips the NaN
```

```text
5.0
nan
5.0
```

**Sample or population standard deviation.** pandas' `.std()` and `.var()` treat the data as a **sample** and divide by n − 1 (`ddof=1`). NumPy's `np.std` treats it as the whole **population** and divides by n (`ddof=0`). Same data, different answer, unless you pass `ddof` yourself.

```python
import numpy as np
import pandas as pd

x = [2, 4, 4, 4, 5, 5, 7, 9]

print(round(pd.Series(x).std(), 3))     # divides by n - 1
print(round(np.std(x), 3))              # divides by n
print(round(np.std(x, ddof=1), 3))      # now matches pandas
```

```text
2.138
2.0
2.138
```

**`mode()` returns a Series.** A column can have more than one most common value, so `mode()` always returns a Series. Take `[0]` if you want just the first.

```python
import pandas as pd

s = pd.Series([1, 1, 2, 2, 3])
print(s.mode().tolist())      # 1 and 2 both appear twice
print(s.mode()[0])
```

```text
[1, 2]
1
```

**`describe()` summarizes a column.** For numbers it gives count, mean, std, min, the quartiles (25%, 50% = the median, 75%) and max. For text it gives count, number of unique values, the most common value (`top`) and how often it appears (`freq`).

```python
import pandas as pd

print(pd.Series([3, 7, 7, 2, 9]).describe().round(2).to_dict())
print(pd.Series(["tea", "jam", "tea", "milk"]).describe().to_dict())
```

```text
{'count': 5.0, 'mean': 5.6, 'std': 2.97, 'min': 2.0, '25%': 3.0, '50%': 7.0, '75%': 7.0, 'max': 9.0}
{'count': 4, 'unique': 3, 'top': 'tea', 'freq': 2}
```

**More tools.** `quantile(0.9)` gives the value 90% of the data falls below. `idxmax()` gives the **label** of the largest value. `cumsum()` gives a running total. `rolling(3).mean()` gives the average of each window of 3 consecutive values.

```python
import pandas as pd

s = pd.Series([3, 8, 1, 9, 4], index=["mon", "tue", "wed", "thu", "fri"])

print(s.quantile(0.5))                          # the median
print(s.idxmax())                               # the day with the largest value
print(s.cumsum().tolist())                      # 3, 3+8, 3+8+1, ...
print(s.rolling(3).mean().round(2).tolist())
```

```text
4.0
thu
[3, 11, 12, 21, 25]
[nan, nan, 4.0, 6.0, 4.67]
```

The rolling mean needs 3 values, so the first two are `NaN`. The third is (3 + 8 + 1) / 3 = 4.

**Reading the numbers.** A mean well above the median signals right skew (a few very large values). A standard deviation that is large compared with the mean signals widely spread data.

### Exam traps

> **Trap.** `describe()`'s `count` excludes missing values, so it can be smaller than `len(df)`.

## 4.2.2 Recognize the importance of test datasets in model evaluation

**Syllabus asks:** the role of a test dataset in validating a machine learning model, and how to choose one for an unbiased evaluation.

### Core facts

A model is only useful if it **generalizes** to new data. Scoring it on the data it learned from rewards memorization; a held-out **test set** estimates real-world performance.

| Split | Used for |
|---|---|
| Training set | Fitting the model's parameters |
| Validation set (or cross-validation) | Choosing features, models and hyperparameters |
| Test set | One final, unbiased estimate, used once at the end |

**Splitting the data.** `train_test_split` shuffles the rows and sets some aside as the test set. `test_size=0.2` keeps 20% for testing (80/20 and 70/30 are typical). `random_state` fixes the shuffle so you get the same split every time.

```python
from sklearn.model_selection import train_test_split

X = list(range(10))                       # 10 rows of data
y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]        # their labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(len(X_train), len(X_test))
```

```text
8 2
```

**A representative test set.** The test set should look like the data the model will meet in real life.

- **Imbalanced classes:** pass `stratify=y` so the test set keeps the same class proportions. Without it, a rare class might barely appear, or not appear at all.
- **Independent rows:** a random shuffle is fine.
- **Time series:** don't shuffle. Train on the past and test on the later period, or the model gets to "see the future".

```python
from sklearn.model_selection import train_test_split

X = list(range(50))
y = [0] * 40 + [1] * 10                   # 20% of rows are class 1

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
print(len(y_test), sum(y_test))           # test rows, and how many are class 1
```

```text
10 2
```

The 10 test rows keep the 20% share: 2 of them are class 1.

**Cross-validation.** With little data, a single split can be lucky or unlucky. **k-fold cross-validation** splits the data into k parts (folds), then trains k times, each time testing on a different fold. The average of the k scores is a steadier estimate. It is used to compare and tune models; if you can, still keep a final test set aside.

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

X, y = load_iris(return_X_y=True)          # a small built-in dataset of flowers
scores = cross_val_score(LogisticRegression(max_iter=1000), X, y, cv=5)

print(scores.round(2))                     # one accuracy per fold
print(round(scores.mean(), 2))             # the overall estimate
```

```text
[0.97 1.   0.93 0.97 1.  ]
0.97
```

**Data leakage.** Leakage is when information from the test data sneaks into training, so the test score looks better than the model really is. Common causes:

- Fitting a scaler or imputer on **all** the data before splitting (see 1.2.3).
- The same record appearing in both the training and test sets.
- A feature that already contains the answer, such as a "cancellation date" when predicting whether a customer will cancel.
- Future information in time-series data.

**Pipelines prevent preprocessing leakage.** A `Pipeline` chains preprocessing and the model into one object. Inside cross-validation, the whole pipeline is refitted on each fold's training part, so the scaler never sees that fold's test part.

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression())   # scale, then classify

print(cross_val_score(model, X, y, cv=5).mean().round(2))
```

```text
0.96
```

**Use the test set once.** If you keep adjusting the model until the test score looks good, you are tuning to the test set. It then becomes a validation set, and its score is no longer an honest estimate.

### Exam traps

> **Trap.** High training accuracy says nothing about generalization. Compare training and test scores.

> **Trap.** Shuffling time-series data before splitting lets the model see the future.

## 4.2.3 Analyze and evaluate supervised learning algorithms

**Syllabus asks:** the characteristics and uses of supervised learning algorithms; overfitting and underfitting; the bias-variance trade-off; the tendencies of linear and logistic regression; preventing model accuracy problems.

### Core facts

**Supervised learning** learns a mapping from features (X) to a known label (y). **Regression** predicts a number; **classification** predicts a category.

| Algorithm | Task | Character |
|---|---|---|
| Linear regression | Regression | Simple, interpretable; high bias if the relationship is not linear |
| Logistic regression | Classification | Linear decision boundary; outputs probabilities; interpretable |
| Decision tree | Both | Captures non-linear rules; overfits when deep (high variance) |
| Random forest | Both | Many trees averaged; lower variance than one tree; less interpretable |
| k-nearest neighbours | Both | Predicts from the closest training points; needs scaling; slow on big data |

**Underfitting vs overfitting.**

| | Underfitting | Good fit | Overfitting |
|---|---|---|---|
| Training score | Low | High | Very high |
| Test score | Low | High, close to training | Much lower than training |
| Cause | Model too simple (**high bias**) | | Model too complex, learns noise (**high variance**) |
| Fix | More or better features, a more flexible model, less regularization | | More data, a simpler model, regularization, fewer features, pruning or `max_depth`, cross-validation |

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=300, n_features=8, n_informative=3, flip_y=0.3, random_state=31)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
for depth in [1, 3, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_tr, y_tr)
    print(depth, round(tree.score(X_tr, y_tr), 2), round(tree.score(X_te, y_te), 2))
```

```text
1 0.61 0.57
3 0.79 0.76
None 1.0 0.66
```

A one-level tree is too simple and scores poorly on both sets (underfitting). The unlimited tree scores 100% on training data but 10 points lower on test data than the depth-3 tree: it memorized the noise (overfitting).

**Bias-variance trade-off.** Expected error = bias² + variance + irreducible noise. **Bias** is error from overly simple assumptions; **variance** is sensitivity to the particular training sample. Making a model more complex lowers bias but raises variance; the best model balances the two.

**Linear and logistic regression tendencies.** Both are low-variance, higher-bias models: stable and interpretable, but they underfit curved relationships unless you add features such as polynomial terms or interactions. With many features and few rows they can overfit too; regularization (Ridge, Lasso; `C` in `LogisticRegression`, where a smaller `C` means stronger regularization) reins that in.

**Preventing accuracy problems.** Split before preprocessing; use cross-validation; scale inside a pipeline; check class balance (with 95% negatives, a model that always says "negative" is 95% accurate, so look at precision, recall and F1); compare training and test scores.

### Exam traps

> **Trap.** High training score + low test score = overfitting (high variance). Low on both = underfitting (high bias).

> **Trap.** More training data helps overfitting; it does little for a model that is too simple.
