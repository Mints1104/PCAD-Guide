from nbhelp import NB, T

NOTEBOOK = NB(
    "capstone", "Capstone: from raw export to finding", 3, ["1.2.4", "1.3.2", "4.1.2", "4.1.6", "5.2.2"],
    "Clean a messy transactions file, aggregate by month and store, normalize by store size and state the finding.",
    """
    A shop chain's transaction export and a table of its stores. The export has a repeated transaction, inconsistent store
    and product spellings, a missing quantity and a refund recorded as a negative quantity.

    The tasks build on each other: running a task first runs your code for the tasks before it.
    """,
    '''
    import io
    import numpy as np
    import pandas as pd

    transactions_csv = """txn_id,store,date,product,qty,unit_price
    1001,S1,2024-01-05,Widget,2,9.99
    1002,S2,2024-01-05,Gadget,1,24.50
    1003,s1 ,2024-01-06,widget ,3,9.99
    1004,S3,2024-01-07,Gizmo,,14.00
    1005,S2,2024-01-07,Gadget,2,24.50
    1005,S2,2024-01-07,Gadget,2,24.50
    1006,S1,2024-02-02,Gizmo,1,14.00
    1007,S3,2024-02-03,Widget,5,9.99
    1008,S2,2024-02-10,Widget,-1,9.99
    1009,S1,2024-02-11,Gadget,1,24.50
    1010,S3,2024-02-15,Gadget,2,24.50
    """

    stores = pd.DataFrame({"store": ["S1", "S2", "S3"], "city": ["Leeds", "York", "Hull"], "sq_m": [120, 80, 150]})
    ''',
    [
        T("clean", "Clean the export",
          """
          Read `transactions_csv` into `tx` and clean it:

          - `store` codes upper-case without spaces, `product` names stripped and in title case;
          - one row per `txn_id` (drop the repeat);
          - drop rows with a missing or non-positive `qty`, then make `qty` an integer column;
          - `date` as datetime; a fresh index.
          """,
          """
          tx = pd.read_csv(io.StringIO(transactions_csv))
          """,
          """
          tx = pd.read_csv(io.StringIO(transactions_csv))
          tx["store"] = tx["store"].str.strip().str.upper()
          tx["product"] = tx["product"].str.strip().str.title()
          tx = tx.drop_duplicates(subset="txn_id")
          tx = tx[tx["qty"] > 0].copy()
          tx["qty"] = tx["qty"].astype(int)
          tx["date"] = pd.to_datetime(tx["date"])
          tx = tx.reset_index(drop=True)
          """,
          """
          assert isinstance(tx, pd.DataFrame), "tx should be a DataFrame"
          assert sorted(tx["txn_id"]) == [1001, 1002, 1003, 1005, 1006, 1007, 1009, 1010], f"txn_ids left: {sorted(tx['txn_id'])} (drop the repeated 1005, the missing quantity and the refund)"
          assert tx["txn_id"].is_unique, "each txn_id should appear once"
          assert sorted(set(tx["store"])) == ["S1", "S2", "S3"], f"stores are {sorted(set(tx['store']))}"
          assert sorted(set(tx["product"])) == ["Gadget", "Gizmo", "Widget"], f"products are {sorted(set(tx['product']))}"
          assert pd.api.types.is_integer_dtype(tx["qty"]), f"qty should be integers, got {tx['qty'].dtype}"
          assert pd.api.types.is_datetime64_any_dtype(tx["date"]), "date should be a datetime column"
          assert list(tx.index) == list(range(len(tx))), "reset the index"
          """,
          ["A missing `qty` makes the column float with NaN; `tx[tx['qty'] > 0]` drops NaN as well as negatives, because NaN > 0 is False.",
           "Convert `qty` to `int` only after the missing value is gone.",
           "`drop_duplicates(subset='txn_id')` keeps the first row of each id."]),

        T("monthly", "Revenue by month",
          """
          Add a `revenue` column (`qty * unit_price`) to `tx`, then store total revenue per month in the Series `monthly`,
          indexed by month labels such as `"2024-01"`.
          """,
          """
          monthly = None
          """,
          """
          tx["revenue"] = tx["qty"] * tx["unit_price"]
          monthly = tx.groupby(tx["date"].dt.strftime("%Y-%m"))["revenue"].sum()
          """,
          """
          assert "revenue" in tx.columns, "add a revenue column to tx"
          assert np.allclose(tx["revenue"], tx["qty"] * tx["unit_price"]), "revenue should be qty * unit_price"
          assert isinstance(monthly, pd.Series), "monthly should be a Series"
          assert [str(m) for m in monthly.index] == ["2024-01", "2024-02"], f"index is {[str(m) for m in monthly.index]}"
          assert [round(v, 2) for v in monthly] == [123.45, 137.45], f"monthly revenue is {[round(v, 2) for v in monthly]}"
          """,
          ["`tx['date'].dt.strftime('%Y-%m')` or `.dt.to_period('M')` gives a month key to group by."]),

        T("stores", "Performance per store",
          """
          Join `tx` with `stores` and build `store_perf`, indexed by `city`, with the columns `revenue` (total), `orders`
          (number of transactions) and `revenue_per_sqm` (revenue ÷ `sq_m`), sorted by `revenue_per_sqm`, highest first.
          """,
          """
          store_perf = stores
          """,
          """
          merged = tx.merge(stores, on="store", how="left")
          store_perf = merged.groupby("city").agg(revenue=("revenue", "sum"), orders=("txn_id", "count"), sq_m=("sq_m", "first"))
          store_perf["revenue_per_sqm"] = store_perf["revenue"] / store_perf["sq_m"]
          store_perf = store_perf.drop(columns="sq_m").sort_values("revenue_per_sqm", ascending=False)
          """,
          """
          assert isinstance(store_perf, pd.DataFrame), "store_perf should be a DataFrame"
          assert {"revenue", "orders", "revenue_per_sqm"} <= set(store_perf.columns), f"columns are {list(store_perf.columns)}"
          assert list(store_perf.index) == ["York", "Leeds", "Hull"], f"order is {list(store_perf.index)}; index by city and sort by revenue_per_sqm, highest first"
          assert [round(v, 2) for v in store_perf["revenue"]] == [73.5, 88.45, 98.95], f"revenue is {store_perf['revenue'].round(2).tolist()}"
          assert store_perf["orders"].tolist() == [2, 4, 2], f"orders is {store_perf['orders'].tolist()}"
          assert np.allclose(store_perf["revenue_per_sqm"], [73.5 / 80, 88.45 / 120, 98.95 / 150]), f"revenue_per_sqm is {store_perf['revenue_per_sqm'].round(4).tolist()}; divide revenue by sq_m"
          """,
          ["Merge on `store`, group by `city`, and use named aggregation for revenue and orders.",
           "`sq_m` is one value per store: take it with `('sq_m', 'first')`, or merge `stores` in again after grouping."]),

        T("mix", "Product mix per store",
          """
          Store in `share` a cross-tabulation of `store` (rows) by `product` (columns) giving the **share of each store's units**
          per product, so every row sums to 1.
          """,
          """
          share = pd.crosstab(tx["store"], tx["product"])
          """,
          """
          share = pd.crosstab(tx["store"], tx["product"], values=tx["qty"], aggfunc="sum", normalize="index").fillna(0)
          """,
          """
          assert isinstance(share, pd.DataFrame), "share should be a DataFrame"
          assert sorted(share.index) == ["S1", "S2", "S3"] and sorted(share.columns) == ["Gadget", "Gizmo", "Widget"], "rows should be stores and columns products"
          assert np.allclose(share.sum(axis=1), 1), "each row should sum to 1 (normalize='index')"
          assert np.isclose(share.loc["S1", "Widget"], 5 / 7), f"S1 sold 5 of its 7 units as Widgets, so the share is {5 / 7:.3f}; got {share.loc['S1', 'Widget']:.3f}. Weight by qty, not by number of transactions"
          """,
          ["`pd.crosstab(rows, cols)` counts transactions; pass `values=tx['qty'], aggfunc='sum'` to add up units instead.",
           "`normalize='index'` divides each row by its total."]),

        T("finding", "State the finding",
          """
          Set `best_city` to the city with the highest revenue per square metre, taken from `store_perf` rather than typed in,
          and write a one-sentence `summary` that names the city and gives its revenue per m² to 2 decimal places.
          """,
          """
          best_city = ""
          summary = ""
          """,
          """
          best_city = store_perf["revenue_per_sqm"].idxmax()
          value = store_perf.loc[best_city, "revenue_per_sqm"]
          summary = f"{best_city} earns {value:.2f} per square metre, the most of the three stores."
          """,
          """
          assert best_city == "York", f"best_city is {best_city!r}"
          assert isinstance(summary, str) and "York" in summary, "the summary should name the city"
          assert "0.92" in summary, f"the summary should give the figure to 2 decimal places (0.92): {summary!r}"
          assert summary.count(".") >= 1 and len(summary.split()) >= 6, "write a full sentence"
          """,
          ["`idxmax()` returns the index label of the largest value.",
           "Format with `f\"{value:.2f}\"`. Lead with the finding and the number that supports it."]),
    ],
    chain=True,
)
