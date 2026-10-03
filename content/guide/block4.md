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

- Methods return a **new** object; the original is unchanged unless you assign the result back. With `inplace=True` they modify in place and return **`None`**.
- `dropna()` with no arguments drops a row if **any** column is missing.
- `drop_duplicates()` compares whole rows; pass `subset=` to compare only some columns.
- To change values that match a condition, use `df.loc[mask, "col"] = value`. Chained assignment such as `df[df["a"] > 0]["b"] = 1` modifies a temporary copy; under pandas 3's copy-on-write it never changes `df`.

Assigning back, `inplace=True`, `subset=` and a `.loc` update:

```python
import pandas as pd

df = pd.DataFrame({"name": ["Ana", "Ana", "Ben"], "city": ["Oslo", "Rome", "Oslo"],
                   "sales": [10, 20, -5]})

df.drop_duplicates(subset=["name"])         # result not assigned: df is unchanged
print(len(df))
result = df.drop_duplicates(subset=["name"], inplace=True)
print(result, len(df))                      # inplace=True changed df and returned None

df.loc[df["sales"] < 0, "sales"] = 0        # conditional update with .loc
print(df["sales"].tolist())
```

```text
3
None 2
[10, 0]
```

The first `drop_duplicates` returned a new DataFrame that was thrown away, so `df` still had 3 rows. With `inplace=True` the method changed `df` and returned `None`.

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

- Arithmetic between Series (or DataFrames) **aligns on the index**: labels present in only one side give `NaN`.
- **Vectorized** operations (`s * 2`, `s.str.upper()`, `np.log(s)`) run in optimized C code and are much faster than Python loops or `apply` with a lambda.
- The index labels rows: `set_index("id")` makes a column the index; `reset_index()` turns the index back into a column (`drop=True` discards it).
- `axis=0` means "along the rows" (an aggregation per column); `axis=1` means "along the columns" (one result per row).
- `.to_numpy()` returns the underlying values as a NumPy array, without the labels.

An index, a row as a Series, the two axes, and the raw values:

```python
import pandas as pd

df = pd.DataFrame({"id": [101, 102], "q1": [5, 3], "q2": [7, 1]})
df = df.set_index("id")
print(df.loc[102].to_dict())                # one row comes back as a Series
print(df.sum(axis=0).to_dict())             # down the rows: one total per column
print(df.sum(axis=1).to_dict())             # across the columns: one total per row
print(df.reset_index().columns.tolist())    # id is a column again
print(df.to_numpy())
```

```text
{'q1': 3, 'q2': 1}
{'q1': 8, 'q2': 8}
{101: 12, 102: 4}
['id', 'q1', 'q2']
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

- `df.loc[rows, cols]` and `df.iloc[rows, cols]`: each part can be a single item, a list, a slice or (for `.loc`) a boolean mask.
- `df.iloc[0]` is the first row as a Series; `df.iloc[:, 0]` is the first column; `df.iloc[-1]` is the last row.
- `df.at[label, col]` and `df.iat[i, j]` get or set a single value quickly.
- Plain brackets: `df["col"]` selects a column; `df[1:3]` slices **rows by position**; `df[mask]` filters rows.
- With a default integer index (0, 1, 2…), `.loc[0:2]` returns **three** rows (labels 0, 1, 2) while `.iloc[0:2]` returns two.

Inclusive `.loc`, exclusive `.iloc`, plain-bracket row slices, and a non-default index:

```python
import pandas as pd

df = pd.DataFrame({"v": [10, 20, 30, 40]})          # default index 0, 1, 2, 3
print(df.loc[0:2, "v"].tolist())                    # labels 0 to 2: end included
print(df.iloc[0:2, 0].tolist())                     # positions 0 and 1: end excluded
print(df[1:3]["v"].tolist())                        # plain brackets with a slice: rows by position
print(df.iat[3, 0], df.iloc[:, 0].tolist())

s = pd.Series(["w", "x", "y", "z"], index=[3, 2, 1, 0])
print(s.loc[1], s.iloc[1])                          # label 1 vs second position
```

```text
[10, 20, 30]
[10, 20]
[20, 30]
40 [10, 20, 30, 40]
y x
```

On the last line, `s.loc[1]` finds the label 1 (`"y"`), while `s.iloc[1]` takes the second item (`"x"`).

- Efficient indexing: set a meaningful index (for example an ID or a date) for fast label lookups and time slicing, keep it sorted, and use vectorized masks instead of loops.

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

- **Split-apply-combine**: `groupby` splits rows by key, applies a function to each group, and combines the results.
- `agg` **reduces** each group to one row; `transform` returns a result the **same length** as the original (useful for group shares or group-mean imputation); `filter` keeps or drops whole groups.
- Named aggregation: `agg(total=("amount", "sum"))` names the output columns.
- Grouping by several keys gives a MultiIndex; `as_index=False` or `.reset_index()` flattens it.
- `size()` counts rows per group (including NaN); `count()` counts non-null values per column.

`size` versus `count`, `filter`, and grouping by two keys:

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "channel": ["web", "shop", "web", "web", "shop"],
                   "amount": [100, np.nan, 70, 30, 60]})

print(df.groupby("region").size().to_dict())                 # rows per group
print(df.groupby("region")["amount"].count().to_dict())      # non-null values per group
print(df.groupby("region").filter(lambda g: len(g) > 2)["region"].tolist())   # keep whole groups
print(df.groupby(["region", "channel"], as_index=False)["amount"].sum())   # EU/shop is all NaN: sum 0
```

```text
{'EU': 2, 'US': 3}
{'EU': 1, 'US': 3}
['US', 'US', 'US']
  region channel  amount
0     EU    shop     0.0
1     EU     web   100.0
2     US    shop    60.0
3     US     web   100.0
```

EU has 2 rows but only 1 non-null amount. `filter` keeps the US rows because only that group has more than 2. `as_index=False` returns the keys as ordinary columns.

- `pd.crosstab(a, b)` counts combinations (a frequency table); `normalize=True` gives proportions; `margins=True` adds totals. `pivot_table` summarizes a value column with any aggregation.
- `value_counts(normalize=True)` gives the share of each category.

Totals, row shares, a pivot table and category shares:

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"],
                   "channel": ["web", "shop", "web", "web", "shop"],
                   "amount": [100, 40, 70, 30, 60]})

print(pd.crosstab(df["region"], df["channel"], margins=True))
print(pd.crosstab(df["region"], df["channel"], normalize="index").round(2))   # shares within each row
print(pd.pivot_table(df, index="region", columns="channel", values="amount"))  # mean by default
print(df["channel"].value_counts(normalize=True).to_dict())
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
channel  shop    web
region
EU       40.0  100.0
US       60.0   50.0
{'web': 0.6, 'shop': 0.4}
```

`normalize="index"` makes each row add up to 1. The pivot table shows the US web cell as 50.0, the **mean** of 70 and 30, not their sum.

- Trends over time: group by a date part (`df.groupby(df["date"].dt.to_period("M"))`) or `resample("ME")` on a datetime index, then compare periods with `pct_change()`.

Monthly totals and the change from one month to the next:

```python
import pandas as pd

sales = pd.DataFrame({"date": pd.to_datetime(["2025-01-05", "2025-01-20", "2025-02-11", "2025-03-02"]),
                      "amount": [100, 50, 180, 135]})
monthly = sales.groupby(sales["date"].dt.to_period("M"))["amount"].sum()
print(monthly.tolist())                          # Jan, Feb, Mar
print(monthly.pct_change().round(2).tolist())     # change vs the previous month
```

```text
[150, 180, 135]
[nan, 0.2, -0.25]
```

February is 20% up on January (180 vs 150) and March 25% down on February. The first month has nothing to compare with, so it is `NaN`.

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

- pandas skips NaN by default (`skipna=True`); NumPy does not, so `np.mean` of data with NaN is `nan` (use `np.nanmean`, `np.nanstd`).
- pandas `var()` and `std()` use ddof=1 (sample); NumPy uses ddof=0 (population) unless you pass `ddof=1`.
- `mode()` returns a **Series**, because there can be several modes; take `[0]` for the first.
- `describe()` gives count, mean, std, min, the quartiles (25%, 50% = median, 75%) and max for numeric columns; for text columns it gives count, unique, top and freq.
- `quantile(0.9)`, `skew()`, `idxmax()`, `cumsum()`, `rolling(7).mean()` and `corr()` round out the toolkit.

Sample versus population spread, several modes, text columns and the rest of the toolkit:

```python
import numpy as np
import pandas as pd

x = [2, 4, 4, 4, 5, 5, 7, 9]
print(round(pd.Series(x).std(), 3), round(np.std(x), 3), round(np.std(x, ddof=1), 3))

print(pd.Series([1, 1, 2, 2, 3]).mode().tolist())    # two modes

names = pd.Series(["tea", "jam", "tea", "milk"])
print(names.describe().to_dict())                    # text: count, unique, top, freq

s = pd.Series([3, 8, 1, 9, 4], index=list("abcde"))
print(s.quantile(0.5), s.idxmax(), s.cumsum().tolist())
print(s.rolling(3).mean().round(2).tolist())                   # mean of each 3-value window
```

```text
2.138 2.0 2.138
[1, 2]
{'count': 4, 'unique': 3, 'top': 'tea', 'freq': 2}
4.0 d [3, 11, 12, 21, 25]
[nan, nan, 4.0, 6.0, 4.67]
```

The rolling mean needs three values, so the first two are `NaN`; the third is (3 + 8 + 1) / 3 = 4.

- Interpret in context: a mean far above the median signals right skew; a large standard deviation relative to the mean signals high variability.

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

- Typical splits: 80/20 or 70/30. `train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)`.
- **Representative**: `stratify=y` keeps class proportions (vital with imbalanced classes); random shuffling for independent rows; a time-based split for time series (train on the past, test on the future).
- **k-fold cross-validation** (`cross_val_score(model, X, y, cv=5)`) rotates which part is held out, giving a more stable estimate when data are limited. It is used for model selection; keep a final test set apart if you can.
- **Data leakage** makes test scores look better than reality: fitting scalers or imputers on all the data before splitting, duplicate records landing in both sets, features that contain the answer (a "cancellation date" when predicting churn), or future information in time series. Put preprocessing inside a scikit-learn `Pipeline` so it is fitted on training folds only.

Five-fold cross-validation with the scaler inside a pipeline, so each fold's scaler sees only that fold's training data:

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression())   # scaler is refit inside each fold
scores = cross_val_score(model, X, y, cv=5)
print(scores.round(2), round(scores.mean(), 2))
```

```text
[0.97 1.   0.93 0.9  1.  ] 0.96
```

Each number is the accuracy on one held-out fold; their mean is the estimate.

- If you tune repeatedly against the test set, it quietly becomes a validation set and its score is no longer unbiased.

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
