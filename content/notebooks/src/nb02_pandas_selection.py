from nbhelp import NB, T

NOTEBOOK = NB(
    "pandas-selection", "Selecting with loc and iloc", 1, ["4.1.3", "4.1.4"],
    "Columns, label and position slicing, boolean masks and new columns.",
    """
    A small sales table with a text index (`r1` to `r6`), so label-based `.loc` and position-based `.iloc` give different answers.
    """,
    """
    import pandas as pd

    sales = pd.DataFrame(
        {
            "region": ["North", "South", "East", "West", "North", "East"],
            "product": ["A", "B", "A", "C", "B", "C"],
            "units": [12, 7, 3, 15, 9, 4],
            "price": [2.5, 4.0, 2.5, 6.0, 4.0, 6.0],
        },
        index=["r1", "r2", "r3", "r4", "r5", "r6"],
    )
    """,
    [
        T("column", "One column as a Series",
          """
          Store the `units` column in `units`, as a **Series** (not a one-column DataFrame).
          """,
          """
          units = None
          """,
          """
          units = sales["units"]
          """,
          """
          assert isinstance(units, pd.Series), f"units should be a Series, got {type(units).__name__} (single brackets give a Series, double brackets a DataFrame)"
          assert units.tolist() == [12, 7, 3, 15, 9, 4], "units should hold the units column"
          assert list(units.index) == ["r1", "r2", "r3", "r4", "r5", "r6"], "keep the original index"
          """,
          ["`df['col']` gives a Series; `df[['col']]` gives a DataFrame."]),

        T("first-three", "The first three rows by position",
          """
          Store the first three rows (all columns) in `first_three`, selecting **by position** with `.iloc`.
          """,
          """
          first_three = sales
          """,
          """
          first_three = sales.iloc[:3]
          """,
          """
          assert isinstance(first_three, pd.DataFrame), "first_three should be a DataFrame"
          assert list(first_three.index) == ["r1", "r2", "r3"], f"expected rows r1, r2, r3, got {list(first_three.index)}"
          assert list(first_three.columns) == list(sales.columns), "keep all four columns"
          """,
          ["`.iloc` slices exclude the stop position, like Python lists: `[:3]` is positions 0, 1, 2."]),

        T("label-slice", "A label slice with two columns",
          """
          Store rows `r2` **through** `r4` (inclusive), with only the `region` and `units` columns, in `middle`. Use `.loc`.
          """,
          """
          middle = sales.loc[:, :]
          """,
          """
          middle = sales.loc["r2":"r4", ["region", "units"]]
          """,
          """
          assert isinstance(middle, pd.DataFrame), "middle should be a DataFrame"
          assert list(middle.index) == ["r2", "r3", "r4"], f"expected rows r2, r3, r4, got {list(middle.index)} (a .loc slice includes its end label)"
          assert list(middle.columns) == ["region", "units"], f"expected columns ['region', 'units'], got {list(middle.columns)}"
          """,
          ["`.loc[rows, columns]`: rows can be a label slice `'r2':'r4'`, columns a list of names.",
           "Unlike `.iloc`, a `.loc` slice **includes** the end label."]),

        T("mask", "Filter with a boolean mask",
          """
          Store the rows where `units` is greater than 8 in `big`.
          """,
          """
          big = sales
          """,
          """
          big = sales[sales["units"] > 8]
          """,
          """
          assert isinstance(big, pd.DataFrame), "big should be a DataFrame"
          assert list(big.index) == ["r1", "r4", "r5"], f"expected rows r1, r4, r5, got {list(big.index)}"
          """,
          ["`sales['units'] > 8` is a Series of True/False; indexing with it keeps the True rows."]),

        T("two-conditions", "Combine two conditions",
          """
          Store the rows where `region` is `"North"` **and** `product` is `"B"` in `north_b`.
          """,
          """
          north_b = sales[sales["region"] == "North"]
          """,
          """
          north_b = sales[(sales["region"] == "North") & (sales["product"] == "B")]
          """,
          """
          assert isinstance(north_b, pd.DataFrame), "north_b should be a DataFrame"
          assert list(north_b.index) == ["r5"], f"expected only row r5, got {list(north_b.index)}"
          """,
          ["pandas uses `&` (and), `|` (or) and `~` (not), not the Python keywords.",
           "Wrap each condition in parentheses: `&` binds more tightly than `==`."]),

        T("new-column", "Add a column without changing the original",
          """
          Make `with_revenue`: a **copy** of `sales` with an extra column `revenue` = `units * price`.
          `sales` itself must stay unchanged.
          """,
          """
          with_revenue = sales
          with_revenue["revenue"] = 0
          """,
          """
          with_revenue = sales.copy()
          with_revenue["revenue"] = with_revenue["units"] * with_revenue["price"]
          """,
          """
          assert "revenue" not in sales.columns, "sales gained a revenue column: plain assignment (with_revenue = sales) names the same object, so make a copy first"
          assert isinstance(with_revenue, pd.DataFrame), "with_revenue should be a DataFrame"
          assert "revenue" in with_revenue.columns, "with_revenue needs a revenue column"
          assert with_revenue["revenue"].tolist() == [30.0, 28.0, 7.5, 90.0, 36.0, 24.0], "revenue should be units * price for each row"
          """,
          ["`df.copy()` makes an independent DataFrame; `b = a` only gives the same object a second name.",
           "`df.assign(revenue=...)` also returns a new DataFrame."]),

        T("idxmax", "The label of the largest value",
          """
          Store the **index label** of the row with the most units in `best` (it should be a label such as `"r1"`, not a position).
          """,
          """
          best = sales["units"].max()
          """,
          """
          best = sales["units"].idxmax()
          """,
          """
          assert best == "r4", f"best should be 'r4', got {best!r}" + (" (that is the largest value itself; idxmax gives its label)" if best == 15 else "")
          """,
          ["`.max()` gives the value; `.idxmax()` gives the index label where it occurs."]),
    ],
)
