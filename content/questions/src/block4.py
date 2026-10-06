from qhelp import Q

QUESTIONS = [
    # ---------- 4.1.1 Cleaning with pandas ----------
    Q("b4-001", "4.1.1", 3,
      "What does this code print?",
      ["`1 4 2 3`", "`1 0 2 3`", "`2 4 2 2`", "`1 4 1 3`"],
      0,
      {1: "`how=\"all\"` only drops rows where every value is missing; column c is never missing.",
       2: "Only row 2 has no missing values at all.",
       3: "Rows 0 and 2 both have a value in column a."},
      "dropna() keeps only the complete row 2 (1); how=\"all\" drops nothing (4); subset=[\"a\"] keeps rows 0 and 2 (2); thresh=2 keeps rows with at least two values: 0, 2 and 3 (3).",
      "Syllabus 4.1.1 · pandas: DataFrame.dropna", ["dropna", "missing-data"],
      code="""
      import numpy as np
      import pandas as pd

      df = pd.DataFrame({"a": [1, np.nan, 3, np.nan],
                         "b": [np.nan, np.nan, 6, 8],
                         "c": [1, 2, 3, 4]})
      print(len(df.dropna()), len(df.dropna(how="all")),
            len(df.dropna(subset=["a"])), len(df.dropna(thresh=2)))
      """, verify="stdout"),

    Q("b4-002", "4.1.1", 2,
      "What does this code print?",
      ["`None [1, 2, 3]`", "`None [3, 1, 2]`", "`[1, 2, 3] [1, 2, 3]`", "`[1, 2, 3] [3, 1, 2]`"],
      0,
      {1: "`inplace=True` does sort `df` itself.",
       2: "With `inplace=True` the method returns None.",
       3: "The result is None, and `df` was changed."},
      "`inplace=True` modifies the DataFrame and returns None, so `result` is None while `df` is sorted.",
      "Syllabus 4.1.1 · pandas: sort_values", ["inplace", "sorting"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"x": [3, 1, 2]})
      result = df.sort_values("x", inplace=True)
      print(result, df["x"].tolist())
      """, verify="stdout"),

    Q("b4-003", "4.1.1", 2,
      "What does this code print?",
      ["`[3, 4, 5]`", "`[1, 2, 4]`", "`[4]`", "`[5, 4, 3]`"],
      0,
      {1: "`keep=\"last\"` keeps the last occurrence of each email, not the first.",
       2: "That is what `keep=False` gives: it drops every row whose email appears more than once, leaving only c@x.",
       3: "Kept rows stay in their original order."},
      "For each email the last row is kept: a@x → visit 3, c@x → 4, b@x → 5, in original row order.",
      "Syllabus 4.1.1 · pandas: drop_duplicates", ["duplicates", "cleaning"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"email": ["a@x", "b@x", "a@x", "c@x", "b@x"],
                         "visit": [1, 2, 3, 4, 5]})
      print(df.drop_duplicates(subset="email", keep="last")["visit"].tolist())
      """, verify="stdout"),

    Q("b4-004", "4.1.1", 2,
      "What does this code print?",
      ["`5 2`", "`2 2`", "`5 5`", "`3 2`"],
      0,
      {1: "Before cleaning, case and spaces make every spelling distinct.",
       2: "After stripping and title-casing, only Oslo and Rome remain.",
       3: "\" oslo\" and \"OSLO \" differ from \"Oslo\" until they're cleaned."},
      "The raw column has 5 distinct strings. `.str.strip().str.title()` turns them into Oslo ×3 and Rome ×2: 2 unique values.",
      "Syllabus 4.1.1, 1.2.4 · pandas: string methods", ["string-cleaning", "nunique"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"city": ["Oslo", " oslo", "OSLO ", "Rome", "rome"]})
      print(df["city"].nunique(), df["city"].str.strip().str.title().nunique())
      """, verify="stdout"),

    Q("b4-005", "4.1.1", 2,
      "What does this code print?",
      ["`[10.0, 10.0, 10.0, 13.0] 23.0 [10.0, 11.0, 12.0, 13.0]`",
       "`[10.0, 13.0, 13.0, 13.0] 23.0 [10.0, 11.5, 11.5, 13.0]`",
       "`[10.0, 10.0, 10.0, 13.0] 23.0 [10.0, 10.0, 10.0, 13.0]`",
       "`[10.0, nan, nan, 13.0] 23.0 [10.0, 11.0, 12.0, 13.0]`"],
      0,
      {1: "`ffill` copies the previous value forward; filling backward is `bfill`.",
       2: "`interpolate` draws a straight line between 10 and 13.",
       3: "`ffill` does fill the gaps."},
      "`ffill` repeats 10 into the gaps; `fillna(0)` makes the sum 23.0; linear `interpolate` fills 11 and 12.",
      "Syllabus 4.1.1 · pandas: ffill, interpolate", ["missing-data", "ffill"],
      code="""
      import numpy as np
      import pandas as pd

      s = pd.Series([10, np.nan, np.nan, 13])
      print(s.ffill().tolist(), s.fillna(0).sum(), s.interpolate().tolist())
      """, verify="stdout"),

    Q("b4-006", "4.1.1", 3,
      "Which line reliably sets `discount` to 0.1 for rows where `qty` is above 10, changing `df` itself in every recent pandas version (2.x and 3.x)?",
      ["`df.loc[df[\"qty\"] > 10, \"discount\"] = 0.1`",
       "`df[df[\"qty\"] > 10][\"discount\"] = 0.1`",
       "`df[\"discount\"][df[\"qty\"] > 10] = 0.1`",
       "`df.query(\"qty > 10\")[\"discount\"] = 0.1`"],
      0,
      {1: "Chained indexing: `df[mask]` makes a temporary copy, and the assignment changes that copy, not `df`.",
       2: "Also chained assignment. In pandas 2 it happens to change `df` (with a warning), but under copy-on-write, the default from pandas 3, it changes nothing.",
       3: "`query` returns a new DataFrame; assigning into it leaves `df` alone."},
      "`.loc[row_mask, column] = value` selects and assigns in one step on the original DataFrame, so it works the same in every version.",
      "Syllabus 4.1.1, 4.1.4 · pandas: copy-on-write", ["loc", "chained-assignment"],
      verify={"py": """
      import warnings
      import pandas as pd

      # pandas 2 can run with copy-on-write off (its default) or on; pandas 3 always uses it.
      modes = [False, True] if int(pd.__version__.split(".")[0]) < 3 else [None]
      works_everywhere = None
      for mode in modes:
          changed = set()
          for i in range(4):
              df = pd.DataFrame({"qty": [1, 12, 5], "discount": [0.0, 0.0, 0.0]})
              with warnings.catch_warnings():
                  warnings.simplefilter("ignore")
                  if mode is None:
                      exec(opt(i), {"df": df})
                  else:
                      with pd.option_context("mode.copy_on_write", mode):
                          exec(opt(i), {"df": df})
              if df["discount"].tolist() == [0.0, 0.1, 0.0]:
                  changed.add(i)
          works_everywhere = changed if works_everywhere is None else works_everywhere & changed
      assert sorted(works_everywhere) == q["answer"], works_everywhere
      """}),

    # ---------- 4.1.2 Merge and reshape ----------
    Q("b4-010", "4.1.2", 2,
      "What does this code print?",
      ["`2 3 4`", "`2 3 3`", "`3 3 4`", "`2 2 4`"],
      0,
      {1: "An outer merge keeps keys from both sides: 1, 2, 3 and 4.",
       2: "The default inner merge keeps only keys 2 and 3.",
       3: "A left merge keeps all three left rows."},
      "inner → keys {2, 3}; left → all left keys {1, 2, 3}; outer → the union {1, 2, 3, 4}.",
      "Syllabus 4.1.2 · pandas: merge", ["merge", "joins"],
      code="""
      import pandas as pd

      left = pd.DataFrame({"k": [1, 2, 3], "a": ["x", "y", "z"]})
      right = pd.DataFrame({"k": [2, 3, 4], "b": [True, False, True]})
      print(len(left.merge(right, on="k")),
            len(left.merge(right, on="k", how="left")),
            len(left.merge(right, on="k", how="outer")))
      """, verify="stdout"),

    Q("b4-011", "4.1.2", 2,
      "What does this code print?",
      ["`['id', 'amount_x', 'amount_y']`", "`['id', 'amount', 'amount']`", "`['id', 'amount']`", "`['id', 'amount_left', 'amount_right']`"],
      0,
      {1: "pandas never creates duplicate column names in a merge; it adds suffixes.",
       2: "Both `amount` columns are kept, since neither is the key.",
       3: "The default suffixes are `_x` and `_y`."},
      "Non-key columns with the same name get the suffixes `_x` (left) and `_y` (right); change them with `suffixes=`.",
      "Syllabus 4.1.2 · pandas: merge suffixes", ["merge", "suffixes"],
      code="""
      import pandas as pd

      a = pd.DataFrame({"id": [1, 2], "amount": [10, 20]})
      b = pd.DataFrame({"id": [1, 2], "amount": [7, 9]})
      print(list(a.merge(b, on="id").columns))
      """, verify="stdout"),

    Q("b4-012", "4.1.2", 2,
      "What does this code print?",
      ["`(4, 3) 2`", "`(4, 2) 0`", "`(2, 5) 0`", "`(4, 3) 0`"],
      0,
      {1: "concat keeps the union of the columns, so `promo` is added.",
       2: "`concat` stacks rows by default (axis=0).",
       3: "January's rows have no promo value, so they get NaN."},
      "Stacking aligns on column names: 4 rows, columns sku, units and promo; January's two rows have NaN for promo.",
      "Syllabus 4.1.2 · pandas: concat", ["concat", "alignment"],
      code="""
      import pandas as pd

      jan = pd.DataFrame({"sku": ["A", "B"], "units": [5, 3]})
      feb = pd.DataFrame({"sku": ["A", "C"], "units": [4, 6], "promo": [True, False]})
      both = pd.concat([jan, feb], ignore_index=True)
      print(both.shape, both["promo"].isna().sum())
      """, verify="stdout"),

    Q("b4-013", "4.1.2", 3,
      "What does this code print?",
      ["`20.0`", "`40`", "`10`", "A ValueError is raised because of duplicate entries"],
      0,
      {1: "`pivot_table` averages by default; summing needs `aggfunc=\"sum\"`.",
       2: "It doesn't keep just the first duplicate.",
       3: "`pivot` would raise on duplicates; `pivot_table` aggregates them."},
      "EU/Q1 has two rows (10 and 30); `pivot_table`'s default `aggfunc=\"mean\"` gives 20.0.",
      "Syllabus 4.1.2 · pandas: pivot_table", ["pivot-table", "aggregation"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"region": ["EU", "EU", "US"], "q": ["Q1", "Q1", "Q1"], "rev": [10, 30, 5]})
      print(df.pivot_table(values="rev", index="region", columns="q").loc["EU", "Q1"])
      """, verify="stdout"),

    Q("b4-014", "4.1.2", 2,
      "`sales` and `targets` are both indexed by store ID. What does `sales.join(targets)` do by default?",
      ["A left join on the index: every store in `sales`, with NaN where `targets` has no row",
       "An inner join on a column named `id`",
       "Stacks the rows of `targets` under `sales`",
       "An outer join on the index"],
      0,
      {1: "`join` matches on the index, and defaults to a left join.",
       2: "Stacking rows is `pd.concat`.",
       3: "Outer must be requested with `how=\"outer\"`."},
      "`DataFrame.join` aligns on the index with `how=\"left\"` by default; `merge` joins on columns with `how=\"inner\"`.",
      "Syllabus 4.1.2 · pandas: DataFrame.join", ["join", "index"]),

    Q("b4-015", "4.1.2", 2,
      "What does this code print?",
      ["`[70, 90] (4, 3)`", "`[80, 65] (4, 3)`", "`[70, 90] (2, 4)`", "`[70] (4, 3)`"],
      0,
      {1: "Those are the math scores.",
       2: "Melting two subject columns for two students gives 4 rows.",
       3: "Both students have an art score."},
      "`melt` makes one row per student-subject pair (4 rows × id, subject, score); the art rows hold 70 and 90.",
      "Syllabus 4.1.2 · pandas: melt", ["melt", "reshaping"],
      code="""
      import pandas as pd

      wide = pd.DataFrame({"id": [1, 2], "math": [80, 65], "art": [70, 90]})
      long = wide.melt(id_vars="id", var_name="subject", value_name="score")
      print(long.loc[long["subject"] == "art", "score"].tolist(), long.shape)
      """, verify="stdout"),

    # ---------- 4.1.3 Series and DataFrames ----------
    Q("b4-020", "4.1.3", 3,
      "What does this code print?",
      ["`[21.0, nan, 13.0]`", "`[11, 22, 3]`", "`[11.0, 22.0, nan]`", "`[21, 2, 13]`"],
      0,
      {1: "Series arithmetic aligns on index labels, not positions.",
       2: "Label x pairs with 20 and z with 10.",
       3: "A label present in only one Series gives NaN, not its own value."},
      "Alignment by label: x = 1 + 20 = 21, y has no partner (NaN), z = 3 + 10 = 13. NaN forces float.",
      "Syllabus 4.1.3 · pandas: alignment", ["series", "alignment"],
      code="""
      import pandas as pd

      a = pd.Series([1, 2, 3], index=["x", "y", "z"])
      b = pd.Series([10, 20], index=["z", "x"])
      print((a + b).tolist())
      """, verify="stdout"),

    Q("b4-021", "4.1.3", 1,
      "What does this code print?",
      ["`Series DataFrame (2, 1)`", "`DataFrame DataFrame (2, 1)`", "`Series Series (2,)`", "`list DataFrame (1, 2)`"],
      0,
      {1: "A single column name returns a Series.",
       2: "A list of names returns a DataFrame, even with one name.",
       3: "`df[[\"a\"]]` has 2 rows and 1 column."},
      "`df[\"a\"]` returns a Series; `df[[\"a\"]]` returns a one-column DataFrame with shape (2, 1).",
      "Syllabus 4.1.3", ["series", "dataframe"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
      print(type(df["a"]).__name__, type(df[["a"]]).__name__, df[["a"]].shape)
      """, verify="stdout"),

    Q("b4-022", "4.1.3", 2,
      "What does this code print?",
      ["`{'north': 16, 'south': 27} {'q1': 30, 'q2': 3, 'q3': 10}`",
       "`{'q1': 30, 'q2': 3, 'q3': 10} {'north': 16, 'south': 27}`",
       "`{'north': 43} {'q1': 30, 'q2': 3, 'q3': 10}`",
       "`{'north': 16, 'south': 27} {'total': 43}`"],
      0,
      {1: "`axis=1` sums across columns, giving one value per row.",
       2: "`axis=1` still keeps one total per row.",
       3: "The default `axis=0` gives one total per column."},
      "`sum(axis=1)` collapses the columns (one result per row); the default `axis=0` collapses the rows (one result per column).",
      "Syllabus 4.1.3 · pandas: DataFrame.sum", ["axis", "aggregation"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"q1": [10, 20], "q2": [1, 2], "q3": [5, 5]}, index=["north", "south"])
      print(df.sum(axis=1).to_dict(), df.sum().to_dict())
      """, verify="stdout"),

    Q("b4-023", "4.1.3", 2,
      "What is the fastest way to add 10% tax to a `price` column with 5 million rows?",
      ["`df[\"price\"] * 1.1`", "A `for` loop over `df.index` using `df.loc`", "`df[\"price\"].apply(lambda p: p * 1.1)`", "Looping with `df.iterrows()`"],
      0,
      {1: "Row-by-row Python loops are orders of magnitude slower.",
       2: "`apply` calls a Python function per value: still a loop.",
       3: "`iterrows` builds a Series per row; the slowest option."},
      "Vectorized arithmetic on the whole column runs in optimized compiled code.",
      "Syllabus 4.1.3", ["vectorization", "performance"]),

    Q("b4-024", "4.1.3", 2,
      "What does this code print?",
      ["`['units'] ['sku', 'units']`", "`['sku', 'units'] ['sku', 'units']`", "`['units'] ['index', 'units']`", "`['units'] ['units']`"],
      0,
      {1: "`set_index` moves `sku` out of the columns into the index.",
       2: "`reset_index` restores the column using the index's name, `sku`.",
       3: "`reset_index()` without `drop=True` turns the index back into a column."},
      "`set_index(\"sku\")` makes sku the row labels; `reset_index()` moves it back into a regular column.",
      "Syllabus 4.1.3 · pandas: set_index, reset_index", ["index", "reset-index"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"sku": ["A", "B"], "units": [5, 3]}).set_index("sku")
      print(list(df.columns), list(df.reset_index().columns))
      """, verify="stdout"),

    # ---------- 4.1.4 Locators and slicing ----------
    Q("b4-030", "4.1.4", 2,
      "What does this code print?",
      ["`3 2`", "`2 2`", "`3 3`", "`2 3`"],
      0,
      {1: "`.loc` includes the end label 3.",
       2: "`.iloc` excludes the end position 3.",
       3: "This reverses the two."},
      "With the default index, `.loc[1:3]` returns labels 1, 2 and 3 (inclusive); `.iloc[1:3]` returns positions 1 and 2.",
      "Syllabus 4.1.4 · pandas: indexing", ["loc", "iloc"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"v": [10, 20, 30, 40, 50]})
      print(len(df.loc[1:3]), len(df.iloc[1:3]))
      """, verify="stdout"),

    Q("b4-031", "4.1.4", 2,
      "What does this code print?",
      ["`11 11 9`", "`11 8 9`", "`20 11 9`", "`11 11 5`"],
      0,
      {1: "`iloc[1:3]` covers positions 1 and 2: 8 and 3.",
       2: "The label slice \"b\":\"c\" covers only b and c.",
       3: "`iloc[-1, 0]` is the last row's first column: 9."},
      "The label slice b:c (inclusive) and the position slice 1:3 (exclusive) select the same two rows here (8 + 3 = 11); `iloc[-1, 0]` is 9.",
      "Syllabus 4.1.4", ["loc", "iloc"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"price": [5, 8, 3, 9]}, index=["a", "b", "c", "d"])
      print(df.loc["b":"c", "price"].sum(), df.iloc[1:3]["price"].sum(), df.iloc[-1, 0])
      """, verify="stdout"),

    Q("b4-032", "4.1.4", 3,
      "What does this code print?",
      ["`c b ['a', 'b', 'c']`", "`b b ['b', 'c']`", "`b c ['a', 'b', 'c']`", "`c b ['a', 'b']`"],
      0,
      {1: "`.loc[1]` looks up the label 1, which is the third item.",
       2: "This swaps label and position.",
       3: "A `.loc` slice includes its end label, 1."},
      "The index is 3, 2, 1, 0. `s.loc[1]` is the item labeled 1 (\"c\"); `s.iloc[1]` is the second item (\"b\"); `s.loc[3:1]` runs from label 3 to label 1 inclusive.",
      "Syllabus 4.1.4", ["loc", "iloc", "labels"],
      code="""
      import pandas as pd

      s = pd.Series(["a", "b", "c", "d"], index=[3, 2, 1, 0])
      print(s.loc[1], s.iloc[1], s.loc[3:1].tolist())
      """, verify="stdout"),

    Q("b4-033", "4.1.4", 2,
      "What does this code print?",
      ["`4.833333333333333`", "`5.875`", "`3.75`", "`4.5`"],
      0,
      {1: "That averages all four prices, ignoring the mask.",
       2: "Three rows have qty above 4, not two.",
       3: "4.5 is a single price, not the mean."},
      "The mask keeps qty 12, 5 and 20, whose prices are 4.5, 7.0 and 3.0: mean 14.5 / 3 ≈ 4.83.",
      "Syllabus 4.1.4 · pandas: boolean indexing", ["loc", "boolean-mask"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"qty": [1, 12, 5, 20], "price": [9.0, 4.5, 7.0, 3.0]})
      print(df.loc[df["qty"] > 4, "price"].mean())
      """, verify="stdout"),

    Q("b4-034", "4.1.4", 2,
      "What does this code print?",
      ["`16 5`", "`18 5`", "`16 12`", "`18 12`"],
      0,
      {1: "`df.at[\"b\", \"qty\"] = 10` replaced 12 with 10.",
       2: "`iat[2, 0]` is row position 2, column position 0: 5.",
       3: "The update changed the sum, and position 2 holds 5."},
      "`at` sets one cell by label (b → 10), so the sum is 1 + 10 + 5 = 16; `iat` reads one cell by position.",
      "Syllabus 4.1.4 · pandas: at, iat", ["at", "iat"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"qty": [1, 12, 5]}, index=["a", "b", "c"])
      df.at["b", "qty"] = 10
      print(df["qty"].sum(), df.iat[2, 0])
      """, verify="stdout"),

    # ---------- 4.1.5 NumPy ----------
    Q("b4-040", "4.1.5", 2,
      "What does this code print?",
      ["`(3, 4)`", "`(3, 1)`", "`(4, 3)`", "A ValueError is raised"],
      0,
      {1: "The size-1 dimension is stretched to 4.",
       2: "Shapes combine as (3, 1) and (1, 4), giving 3 rows and 4 columns.",
       3: "Compared from the right, 1 and 4 are compatible, and so are 3 and (missing) 1."},
      "Broadcasting treats `b` as shape (1, 4); (3, 1) + (1, 4) stretches both size-1 dimensions to (3, 4).",
      "Syllabus 4.1.5 · NumPy: broadcasting", ["broadcasting", "numpy"],
      code="""
      import numpy as np

      a = np.ones((3, 1))
      b = np.arange(4)
      print((a + b).shape)
      """, verify="stdout"),

    Q("b4-041", "4.1.5", 2,
      "What happens when the last line runs?",
      ["A ValueError is raised: shapes (2, 3) and (2,) can't be broadcast",
       "`b` is added to each row",
       "`b` is added to each column",
       "The result has shape (2, 2)"],
      0,
      {1: "Compared from the right, 3 and 2 differ and neither is 1.",
       2: "Adding to each column needs `b` shaped (2, 1).",
       3: "No valid broadcast exists, so there's no result."},
      "Broadcasting compares trailing dimensions: 3 vs 2 are incompatible. Reshape `b` to (2, 1) to add it per row.",
      "Syllabus 4.1.5 · NumPy: broadcasting", ["broadcasting", "errors"],
      code="""
      import numpy as np

      a = np.ones((2, 3))
      b = np.array([1, 2])
      a + b
      """, verify="raises:ValueError"),

    Q("b4-042", "4.1.5", 2,
      "What does this code print?",
      ["`[5 7 9] [3 6] 3.5`", "`[6 15] [3 6] 3.5`", "`[5 7 9] [4 5 6] 3.5`", "`[5 7 9] [3 6] 21`"],
      0,
      {1: "`axis=0` collapses the rows: one sum per column.",
       2: "`max(axis=1)` gives one maximum per row.",
       3: "`mean()` without an axis averages all six values: 21 / 6."},
      "axis=0 → per column [1+4, 2+5, 3+6]; axis=1 → per row maxima [3, 6]; no axis → overall mean 3.5.",
      "Syllabus 4.1.5 · NumPy: aggregations", ["axis", "numpy"],
      code="""
      import numpy as np

      m = np.array([[1, 2, 3], [4, 5, 6]])
      print(m.sum(axis=0), m.max(axis=1), m.mean())
      """, verify="stdout"),

    Q("b4-043", "4.1.5", 1,
      "What does this code print?",
      ["`[1, 2, 3, 1, 2, 3] [2 4 6]`", "`[2, 4, 6] [2 4 6]`", "`[1, 2, 3, 1, 2, 3] [1 2 3 1 2 3]`", "`[2, 4, 6] [1 2 3 1 2 3]`"],
      0,
      {1: "`+` concatenates lists.",
       2: "`+` adds arrays element-wise.",
       3: "This swaps list and array behaviour."},
      "List + list concatenates; array + array adds element by element.",
      "Syllabus 4.1.5", ["numpy", "lists"],
      code="""
      import numpy as np

      lst = [1, 2, 3]
      arr = np.array(lst)
      print(lst + lst, arr + arr)
      """, verify="stdout"),

    Q("b4-044", "4.1.5", 2,
      "What does this code print?",
      ["`float64 U`", "`int64 U`", "`float64 i`", "`object O`"],
      0,
      {1: "One float value upcasts the whole array to float.",
       2: "Mixing a number with a string makes every element a string (kind 'U').",
       3: "NumPy chooses a Unicode string dtype, not object, for this mix."},
      "An ndarray has one dtype: [1, 2, 3.5] becomes float64, and [1, \"2\"] becomes a Unicode string array.",
      "Syllabus 4.1.5 · NumPy: dtypes", ["dtype", "numpy"],
      code="""
      import numpy as np

      print(np.array([1, 2, 3.5]).dtype, np.array([1, "2"]).dtype.kind)
      """, verify="stdout"),

    Q("b4-045", "4.1.5", 2,
      "What does this code print?",
      ["`nan 3.0`", "`3.0 3.0`", "`2.0 3.0`", "`nan nan`"],
      0,
      {1: "`np.mean` doesn't skip NaN; any NaN makes the result NaN.",
       2: "NaN isn't treated as 0.",
       3: "`np.nanmean` ignores NaN and averages 2.0 and 4.0."},
      "NumPy propagates NaN through `mean`; `nanmean` skips missing values.",
      "Syllabus 4.1.5, 4.2.1 · NumPy: nanmean", ["nan", "numpy"],
      code="""
      import numpy as np

      x = np.array([2.0, np.nan, 4.0])
      print(np.mean(x), np.nanmean(x))
      """, verify="stdout"),

    Q("b4-046", "4.1.5", 2,
      "A table of customers holds a name (text), a signup date and a lifetime value (float), with labeled columns. Which structure fits it best?",
      ["A pandas DataFrame", "A 2-D NumPy array", "A single pandas Series", "A tuple of tuples"],
      0,
      {1: "An ndarray has one dtype, so text, dates and floats would all be coerced.",
       2: "A Series holds one column.",
       3: "Tuples have no column labels or vectorized operations."},
      "DataFrames hold labeled columns that can each have their own dtype.",
      "Syllabus 4.1.5", ["data-structures", "dataframe"]),

    # ---------- 4.1.6 Grouping ----------
    Q("b4-050", "4.1.6", 2,
      "What does this code print?",
      ["`{'a': 9, 'b': 6} {'a': 3.0, 'b': 3.0}`", "`{'a': 3, 'b': 2} {'a': 3.0, 'b': 3.0}`", "`{'a': 9, 'b': 6} {'a': 4.5, 'b': 3.0}`", "`{'a': 15} {'a': 3.0}`"],
      0,
      {1: "`sum` adds points; counting rows would be `size()` or `count()`.",
       2: "Team a has three games: 9 / 3 = 3.0.",
       3: "Grouping gives one entry per team."},
      "Team a: 3 + 2 + 4 = 9 over 3 games (mean 3.0); team b: 5 + 1 = 6 over 2 games (mean 3.0).",
      "Syllabus 4.1.6 · pandas: groupby", ["groupby", "aggregation"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"team": ["a", "b", "a", "b", "a"], "pts": [3, 5, 2, 1, 4]})
      print(df.groupby("team")["pts"].sum().to_dict(),
            df.groupby("team")["pts"].mean().round(2).to_dict())
      """, verify="stdout"),

    Q("b4-051", "4.1.6", 2,
      "What does this code print?",
      ["`[2, 1] [1, 1]`", "`[2, 1] [2, 1]`", "`[1, 1] [1, 1]`", "`[1, 1] [2, 1]`"],
      0,
      {1: "`count` skips the NaN in group x.",
       2: "`size` counts every row, including the one with NaN.",
       3: "This swaps size and count."},
      "`size()` counts rows per group (x has 2); `count()` counts non-null values (x has 1).",
      "Syllabus 4.1.6 · pandas: GroupBy.size, count", ["groupby", "size-vs-count"],
      code="""
      import numpy as np
      import pandas as pd

      df = pd.DataFrame({"g": ["x", "x", "y"], "v": [1, np.nan, 3]})
      print(df.groupby("g").size().tolist(), df.groupby("g")["v"].count().tolist())
      """, verify="stdout"),

    Q("b4-052", "4.1.6", 3,
      "What does this code print?",
      ["`[0.75, 0.25, 1.0] 2`", "`[0.75, 0.25, 1.0] 3`", "`[0.33, 0.11, 0.56] 2`", "`[1.0, 1.0, 1.0] 2`"],
      0,
      {1: "`agg` reduces to one row per store: 2 rows.",
       2: "Shares are within each store, not of the grand total 90.",
       3: "Each row's sales is divided by its store's total, not by itself."},
      "`transform(\"sum\")` returns each row's store total (40, 40, 50), so the shares are 30/40, 10/40 and 50/50; `agg` gives one row per store.",
      "Syllabus 4.1.6 · pandas: GroupBy.transform", ["groupby", "transform"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"store": ["A", "A", "B"], "sales": [30, 10, 50]})
      df["share"] = df["sales"] / df.groupby("store")["sales"].transform("sum")
      print(df["share"].tolist(), len(df.groupby("store")["sales"].agg("sum")))
      """, verify="stdout"),

    Q("b4-053", "4.1.6", 2,
      "What does this code print?",
      ["`2`", "`1`", "`3`", "`0`"],
      0,
      {1: "Two free-plan customers churned: rows 0 and 3.",
       2: "Three customers are on the free plan, but only two of them churned.",
       3: "`crosstab` counts combinations; free & True occurs twice."},
      "`pd.crosstab` counts each (plan, churned) combination: free & True appears twice.",
      "Syllabus 4.1.6 · pandas: crosstab", ["crosstab", "frequency"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"plan": ["free", "pro", "free", "free", "pro"],
                         "churned": [True, False, False, True, False]})
      print(pd.crosstab(df["plan"], df["churned"]).loc["free", True])
      """, verify="stdout"),

    Q("b4-054", "4.1.6", 2,
      "What does this code print?",
      ["`['region', 'total', 'n'] 40`", "`['total', 'n'] 40`", "`['region', 'amount', 'order'] 40`", "`['region', 'total', 'n'] 45`"],
      0,
      {1: "`as_index=False` keeps `region` as a column.",
       2: "Named aggregation names the output columns `total` and `n`.",
       3: "Row 0 is EU: 10 + 30 = 40."},
      "Named aggregation creates the columns total and n; `as_index=False` keeps region as a regular column.",
      "Syllabus 4.1.6 · pandas: named aggregation", ["groupby", "agg"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"region": ["EU", "EU", "US"], "amount": [10, 30, 5], "order": [1, 2, 3]})
      out = df.groupby("region", as_index=False).agg(total=("amount", "sum"), n=("order", "count"))
      print(out.columns.tolist(), out.loc[0, "total"])
      """, verify="stdout"),

    Q("b4-055", "4.1.6", 2,
      "`df` has columns `region` and `amount`. Which two expressions produce one row per region holding the total amount? Select two.",
      ["`df.groupby(\"region\")[\"amount\"].sum()`",
       "`df.pivot_table(values=\"amount\", index=\"region\", aggfunc=\"sum\")`",
       "`df.groupby(\"region\")[\"amount\"].transform(\"sum\")`",
       "`pd.crosstab(df[\"region\"], df[\"amount\"])`",
       "`df.sort_values(\"region\")`"],
      [0, 1],
      {2: "`transform` returns one value per original row, not per region.",
       3: "`crosstab` counts combinations of region and each distinct amount.",
       4: "Sorting only reorders rows."},
      "Both `groupby(...).sum()` and a `pivot_table` with `aggfunc=\"sum\"` reduce to one total per region.",
      "Syllabus 4.1.6", ["groupby", "pivot-table"],
      verify={"py": """
      import pandas as pd
      df = pd.DataFrame({"region": ["EU", "EU", "US"], "amount": [10, 30, 5]})
      good = []
      for i in range(5):
          out = eval(opt(i), {"df": df, "pd": pd})
          vals = out.squeeze() if isinstance(out, pd.DataFrame) and out.shape[1] == 1 else out
          if len(out) == 2 and isinstance(vals, pd.Series) and vals.to_dict() == {"EU": 40, "US": 5}:
              good.append(i)
      assert good == q["answer"], good
      """}),

    # ---------- 4.2.1 Descriptive statistics in code ----------
    Q("b4-060", "4.2.1", 2,
      "What does this code print?",
      ["`6.0 nan`", "`4.0 4.0`", "`6.0 6.0`", "`nan nan`"],
      0,
      {1: "Neither function treats NaN as 0.",
       2: "NumPy's `mean` doesn't skip NaN.",
       3: "pandas skips NaN by default."},
      "pandas' `mean` skips missing values (skipna=True); NumPy's `mean` returns nan when any value is NaN.",
      "Syllabus 4.2.1", ["mean", "nan"],
      code="""
      import numpy as np
      import pandas as pd

      s = pd.Series([4, np.nan, 8])
      print(s.mean(), np.mean(s.to_numpy()))
      """, verify="stdout"),

    Q("b4-061", "4.2.1", 2,
      "What does this code print?",
      ["`[2, 3]`", "`[2]`", "`[3]`", "`2.5`"],
      0,
      {1: "2 and 3 both appear twice, so both are modes.",
       2: "3 is as frequent as 2.",
       3: "The mode is a most-frequent value, never an average."},
      "`mode()` returns a Series with every value that ties for most frequent.",
      "Syllabus 4.2.1 · pandas: Series.mode", ["mode", "descriptive-statistics"],
      code="""
      import pandas as pd

      s = pd.Series([1, 2, 2, 3, 3])
      print(s.mode().tolist())
      """, verify="stdout"),

    Q("b4-062", "4.2.1", 2,
      "What does this code print?",
      ["`4.0 5.0 5`", "`5.0 5.0 5`", "`4.0 3.0 5`", "`4.0 5.0 4`"],
      0,
      {1: "`count` excludes the missing value.",
       2: "The median of 1, 3, 7, 9 is (3 + 7) / 2 = 5.0.",
       3: "`len` counts every element, including NaN."},
      "`describe()` counts 4 non-null values and reports the median (50%) of 1, 3, 7, 9 as 5.0; `len` counts all 5 elements.",
      "Syllabus 4.2.1 · pandas: describe", ["describe", "descriptive-statistics"],
      code="""
      import numpy as np
      import pandas as pd

      s = pd.Series([1, 3, np.nan, 7, 9])
      d = s.describe()
      print(d["count"], d["50%"], len(s))
      """, verify="stdout"),

    Q("b4-063", "4.2.1", 2,
      "What does this code print?",
      ["`1.633 2.0 2.0`", "`2.0 1.633 2.0`", "`1.633 1.633 2.0`", "`2.0 2.0 1.633`"],
      0,
      {1: "NumPy's default is the population formula (ddof=0), which is smaller.",
       2: "pandas uses ddof=1 by default.",
       3: "`ddof=1` in NumPy matches pandas' default."},
      "Squared deviations from 4 sum to 8. Population: √(8/3) ≈ 1.633; sample: √(8/2) = 2.0.",
      "Syllabus 4.2.1, 3.1.1", ["standard-deviation", "ddof"],
      code="""
      import numpy as np
      import pandas as pd

      x = [2, 4, 6]
      print(round(np.std(x), 3), round(pd.Series(x).std(), 3), round(np.std(x, ddof=1), 3))
      """, verify="stdout"),

    Q("b4-064", "4.2.1", 2,
      "`df[\"order_value\"].describe()` shows mean 820 and 50% of 310. What does this suggest?",
      ["The distribution is right-skewed: a few very large orders pull the mean up",
       "Most orders are worth about 820",
       "The data has no outliers",
       "Half of all orders are worth more than 820"],
      0,
      {1: "The typical (median) order is 310.",
       2: "A mean far above the median signals large extreme values.",
       3: "Half the orders exceed the median, 310, not the mean."},
      "When the mean is much larger than the median, large values in the right tail are dragging the mean upward.",
      "Syllabus 4.2.1, 3.1.1", ["skew", "describe"]),

    # ---------- 4.2.2 Test datasets ----------
    Q("b4-070", "4.2.2", 1,
      "What is the main purpose of a held-out test set?",
      ["To estimate how the model will perform on new, unseen data",
       "To give the model more data to learn from",
       "To choose the model's hyperparameters",
       "To make training faster"],
      0,
      {1: "Test data must never be used for training.",
       2: "Tuning uses a validation set or cross-validation; the test set is for the final check.",
       3: "Holding data out has nothing to do with speed."},
      "A test set the model has never seen gives an unbiased estimate of generalization.",
      "Syllabus 4.2.2", ["test-set", "generalization"]),

    Q("b4-071", "4.2.2", 2,
      "A churn model scores 99% accuracy. One of its features is `cancellation_date`, which is filled in only for customers who churned. What is wrong?",
      ["Target leakage: the feature reveals the answer, so the score won't hold for new customers",
       "Nothing; the model is excellent",
       "The model is underfitting",
       "The test set is too large"],
      0,
      {1: "At prediction time, future churners don't yet have a cancellation date.",
       2: "Underfitting would give low scores.",
       3: "Test size doesn't explain a suspiciously perfect score."},
      "A feature that is only known after the outcome leaks the target into training and inflates evaluation scores.",
      "Syllabus 4.2.2", ["data-leakage", "target-leakage"]),

    Q("b4-072", "4.2.2", 2,
      "With only 400 labeled rows, which technique gives the most reliable performance estimate for choosing between models?",
      ["k-fold cross-validation", "Evaluating on the training data", "A single 95/5 train/test split", "Removing the test set entirely"],
      0,
      {1: "Training scores reward memorization.",
       2: "A 20-row test set gives a very noisy estimate.",
       3: "Without held-out data there's no honest estimate at all."},
      "Cross-validation rotates the held-out fold so every row is used for testing once, averaging out the noise of a single small split.",
      "Syllabus 4.2.2 · scikit-learn: cross-validation", ["cross-validation", "evaluation"]),

    Q("b4-073", "4.2.2", 2,
      "What does this code print?",
      ["`5`", "`1`", "`200`", "`40`"],
      0,
      {1: "One score per fold is returned, not a single average.",
       2: "Scores are per fold, not per sample.",
       3: "40 is the size of each fold, not the number of scores."},
      "`cross_val_score` with cv=5 trains and scores the model 5 times, returning an array of 5 scores.",
      "Syllabus 4.2.2 · scikit-learn: cross_val_score", ["cross-validation", "sklearn"],
      code="""
      from sklearn.datasets import make_classification
      from sklearn.linear_model import LogisticRegression
      from sklearn.model_selection import cross_val_score

      X, y = make_classification(n_samples=200, random_state=0)
      scores = cross_val_score(LogisticRegression(), X, y, cv=5)
      print(len(scores))
      """, verify="stdout"),

    Q("b4-074", "4.2.2", 2,
      "A team tries 50 model settings and picks the one with the best score on the test set, then reports that score. Why is the reported score too optimistic?",
      ["The test set was used for model selection, so it no longer measures performance on unseen data",
       "50 settings is too few",
       "Test scores are always lower than training scores",
       "The model was trained on the test set"],
      0,
      {1: "The number of settings isn't the issue; where they were evaluated is.",
       2: "Test scores are usually lower, but that doesn't explain the bias here.",
       3: "It wasn't trained on it, but choosing by it leaks information just the same."},
      "Selecting the best of many models on one test set fits to its noise; use a validation set or cross-validation, and keep the test set for one final check.",
      "Syllabus 4.2.2", ["test-set", "selection-bias"]),

    Q("b4-075", "4.2.2", 3,
      "Which two are forms of data leakage? Select two.",
      ["Fitting the scaler on all rows before splitting into training and test sets",
       "The same customers' duplicate records ending up in both training and test sets",
       "Setting `random_state=42` in the split",
       "Using `stratify=y` for an imbalanced target",
       "Using a 70/30 split instead of 80/20"],
      [0, 1],
      {2: "A fixed random state only makes the split reproducible.",
       3: "Stratifying keeps class proportions; it doesn't leak.",
       4: "The split ratio doesn't create leakage."},
      "Leakage lets test information reach training: via preprocessing statistics, or via duplicate records the model has effectively seen.",
      "Syllabus 4.2.2", ["data-leakage", "evaluation"]),

    # ---------- 4.2.3 Supervised learning ----------
    Q("b4-080", "4.2.3", 1,
      "A model scores 0.99 accuracy on training data and 0.71 on test data. What is the diagnosis?",
      ["Overfitting (high variance)", "Underfitting (high bias)", "A perfect fit", "Data leakage from test to train"],
      0,
      {1: "Underfitting shows low scores on both sets.",
       2: "A large gap between training and test scores is not a good fit.",
       3: "Leakage would inflate the test score, not leave it far below training."},
      "Near-perfect training and much weaker test performance means the model memorized noise.",
      "Syllabus 4.2.3", ["overfitting", "diagnosis"]),

    Q("b4-081", "4.2.3", 1,
      "A model scores 0.62 on training data and 0.60 on test data, well below what the problem allows. What is the diagnosis?",
      ["Underfitting (high bias)", "Overfitting (high variance)", "Data leakage", "A perfect fit"],
      0,
      {1: "Overfitting shows a big gap between training and test.",
       2: "Leakage produces suspiciously high scores.",
       3: "Both scores are poor."},
      "Low scores on both sets mean the model is too simple to capture the pattern.",
      "Syllabus 4.2.3", ["underfitting", "diagnosis"]),

    Q("b4-082", "4.2.3", 2,
      "An unrestricted decision tree overfits. Which change is most likely to help?",
      ["Limit its depth (for example `max_depth=4`)", "Remove the test set", "Add more features of random noise", "Train on the test data too"],
      0,
      {1: "Removing the test set only hides the problem.",
       2: "Noise features give the tree more to memorize.",
       3: "Training on test data destroys the evaluation."},
      "Restricting depth (or other pruning) lowers variance at the cost of a little bias.",
      "Syllabus 4.2.3", ["overfitting", "regularization"]),

    Q("b4-083", "4.2.3", 3,
      "The code prints the training and test accuracy (shown as comments) for three tree depths. Which reading is correct?",
      ["Depth 1 underfits, depth 3 generalizes best, and the unlimited tree overfits",
       "The unlimited tree is best because its training accuracy is 1.0",
       "Depth 1 is best because its train and test scores are closest",
       "All three models overfit"],
      0,
      {1: "Perfect training accuracy with a lower test score is overfitting.",
       2: "Scores that are close but low mean the model is too simple.",
       3: "Depth 1 and depth 3 don't show a large train-test gap."},
      "Judge by test performance and the train-test gap: depth 3 has the best test score; depth 1 is low on both; the unlimited tree memorizes training data (1.0) but drops 10 points on test.",
      "Syllabus 4.2.3 · scikit-learn: DecisionTreeClassifier", ["bias-variance", "model-complexity"],
      code="""
      from sklearn.datasets import make_classification
      from sklearn.model_selection import train_test_split
      from sklearn.tree import DecisionTreeClassifier

      X, y = make_classification(n_samples=300, n_features=8, n_informative=3,
                                 flip_y=0.3, random_state=31)
      X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
      for depth in [1, 3, None]:
          tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_tr, y_tr)
          print(depth, round(tree.score(X_tr, y_tr), 2), round(tree.score(X_te, y_te), 2))
      # 1 0.61 0.57
      # 3 0.79 0.76
      # None 1.0 0.66
      """, verify={"py": "assert run_py(code) == '1 0.61 0.57\\n3 0.79 0.76\\nNone 1.0 0.66'"}),

    Q("b4-084", "4.2.3", 2,
      "As a model is made more complex (deeper trees, more features), what usually happens?",
      ["Bias decreases and variance increases", "Bias increases and variance decreases", "Both bias and variance decrease", "Neither changes"],
      0,
      {1: "That describes making a model simpler.",
       2: "The two move in opposite directions: that's the trade-off.",
       3: "Complexity is exactly what shifts the balance."},
      "Flexible models fit training data more closely (less bias) but react more to its noise (more variance).",
      "Syllabus 4.2.3", ["bias-variance", "trade-off"]),

    Q("b4-085", "4.2.3", 2,
      "A fraud model reports 98% accuracy on data where 2% of transactions are fraud. Why should the team be cautious?",
      ["A model that labels every transaction \"not fraud\" also scores 98%; check recall and precision on the fraud class",
       "98% accuracy always means the model overfits",
       "Accuracy can't be computed for binary problems",
       "The model must be using the test set for training"],
      0,
      {1: "High accuracy alone doesn't indicate overfitting.",
       2: "Accuracy is defined for binary problems; it's just misleading here.",
       3: "Nothing indicates leakage; the class balance explains the number."},
      "With imbalanced classes, accuracy rewards predicting the majority class; recall, precision and F1 reveal whether fraud is actually caught.",
      "Syllabus 4.2.3", ["imbalanced-classes", "metrics"]),

    Q("b4-086", "4.2.3", 1,
      "Which task is supervised learning?",
      ["Predicting house prices from past sales where the sale price is known",
       "Grouping customers into segments without any labels",
       "Finding unusual transactions with no examples of fraud",
       "Compressing 50 features into 5 components"],
      0,
      {1: "Grouping without labels is clustering, an unsupervised task.",
       2: "Anomaly detection without labeled examples is unsupervised.",
       3: "Dimensionality reduction doesn't learn from a target."},
      "Supervised learning learns from examples that include the correct answer (the label).",
      "Syllabus 4.2.3", ["supervised-learning", "definitions"]),

    Q("b4-087", "4.2.3", 2,
      "In scikit-learn's `LogisticRegression`, what does lowering `C` from 1.0 to 0.01 do?",
      ["Strengthens regularization, which can reduce overfitting",
       "Weakens regularization",
       "Changes the model into linear regression",
       "Raises the classification threshold"],
      0,
      {1: "C is the inverse of the regularization strength: smaller C means stronger regularization.",
       2: "The model type is unchanged.",
       3: "The threshold is separate from C."},
      "Smaller C penalizes large coefficients more, trading a little bias for less variance.",
      "Syllabus 4.2.3 · scikit-learn: LogisticRegression", ["regularization", "logistic-regression"]),

    Q("b4-088", "4.2.3", 2,
      "Compared with an unrestricted decision tree, what is the typical tendency of linear and logistic regression?",
      ["Higher bias and lower variance: stable, but they can underfit curved relationships",
       "Lower bias and higher variance: they memorize the training data",
       "They can't overfit under any circumstances",
       "They have no bias, because their coefficients are calculated exactly"],
      0,
      {1: "That describes very flexible models such as deep, unpruned trees.",
       2: "With many features compared with rows they can overfit, which is why regularization (such as a smaller `C`) exists.",
       3: "Assuming a straight-line relationship is itself a source of bias, however exactly the line is fitted."},
      "A straight-line model can't bend to follow complex patterns (bias) but changes little between training samples (low variance). Add features if it underfits; regularize if many features make it overfit.",
      "Syllabus 4.2.3", ["bias-variance", "linear-regression"]),
]
