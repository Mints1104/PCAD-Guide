from nbhelp import NB, T

NOTEBOOK = NB(
    "group-merge", "Group, merge and reshape", 2, ["4.1.2", "4.1.6"],
    "groupby with named aggregation, inner, left and anti joins, pivot_table and melt.",
    """
    Orders and customers that do not line up perfectly: customer 13 placed an order but is not in `customers`,
    and customer 14 (Eli) never ordered. `wide` is a small table in wide format for the reshaping task.
    """,
    """
    import pandas as pd

    orders = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6, 7],
        "customer_id": [10, 11, 10, 12, 13, 11, 10],
        "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Mar", "Mar"],
        "amount": [50.0, 20.0, 35.0, 80.0, 15.0, 40.0, 25.0],
    })
    customers = pd.DataFrame({
        "customer_id": [10, 11, 12, 14],
        "name": ["Ana", "Ben", "Cara", "Eli"],
        "segment": ["retail", "business", "retail", "business"],
    })
    wide = pd.DataFrame({"store": ["A", "B"], "Q1": [100, 80], "Q2": [120, 90]})
    """,
    [
        T("per-customer", "Total per customer",
          """
          Store the total `amount` per `customer_id` in `per_customer`, as a Series indexed by `customer_id`.
          """,
          """
          per_customer = orders["amount"]
          """,
          """
          per_customer = orders.groupby("customer_id")["amount"].sum()
          """,
          """
          assert isinstance(per_customer, pd.Series), f"per_customer should be a Series, got {type(per_customer).__name__} (select one column after groupby)"
          assert per_customer.to_dict() == {10: 110.0, 11: 60.0, 12: 80.0, 13: 15.0}, f"got {per_customer.to_dict()}"
          """,
          ["`df.groupby(key)[column].sum()` gives one total per key."]),

        T("inner", "An inner join",
          """
          Store `orders` merged with `customers` on `customer_id` in `joined`, keeping **only** orders whose customer is known.
          """,
          """
          joined = orders
          """,
          """
          joined = orders.merge(customers, on="customer_id", how="inner")
          """,
          """
          assert isinstance(joined, pd.DataFrame), "joined should be a DataFrame"
          assert {"name", "segment"} <= set(joined.columns), "joined should include the customer columns"
          assert len(joined) == 6, f"joined should have 6 rows (order 5 has no matching customer), got {len(joined)}"
          assert 13 not in joined["customer_id"].tolist(), "customer 13 is not in customers, so an inner join drops that order"
          """,
          ["`orders.merge(customers, on='customer_id', how='inner')`; inner is the default `how`."]),

        T("left", "A left join keeps every order",
          """
          Store a merge that keeps **every** order in `all_orders`. The order from customer 13 should have a missing `name`.
          """,
          """
          all_orders = orders.merge(customers, on="customer_id")
          """,
          """
          all_orders = orders.merge(customers, on="customer_id", how="left")
          """,
          """
          assert isinstance(all_orders, pd.DataFrame), "all_orders should be a DataFrame"
          assert len(all_orders) == 7, f"all_orders should keep all 7 orders, got {len(all_orders)}"
          row = all_orders[all_orders["customer_id"] == 13]
          assert len(row) == 1 and pd.isna(row["name"].iloc[0]), "the order from customer 13 should have a missing name"
          assert "Eli" not in all_orders["name"].tolist(), "a left join on orders does not add customers without orders"
          """,
          ["`how='left'` keeps every row of the left table and fills unmatched right-hand columns with NaN."]),

        T("anti", "Customers who never ordered",
          """
          Store the **names** of customers with no orders in the list `no_orders`.
          """,
          """
          no_orders = []
          """,
          """
          no_orders = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
          """,
          """
          assert isinstance(no_orders, list), "no_orders should be a list (Series have .tolist())"
          assert no_orders == ["Eli"], f"expected ['Eli'], got {no_orders}"
          """,
          ["`isin` tests membership; `~` negates the mask.",
           "Alternatively, merge with `how='left', indicator=True` and keep the rows marked `left_only`."]),

        T("named-agg", "Several summaries per group",
          """
          From the inner join of `orders` and `customers`, make `by_segment`: one row per `segment` with two columns,
          `total` (sum of `amount`) and `orders` (number of orders).
          """,
          """
          joined = orders.merge(customers, on="customer_id")
          by_segment = joined
          """,
          """
          joined = orders.merge(customers, on="customer_id")
          by_segment = joined.groupby("segment").agg(total=("amount", "sum"), orders=("order_id", "count"))
          """,
          """
          assert isinstance(by_segment, pd.DataFrame), "by_segment should be a DataFrame"
          assert sorted(by_segment.columns) == ["orders", "total"], f"columns should be total and orders, got {list(by_segment.columns)}"
          assert sorted(by_segment.index) == ["business", "retail"], "the index should be the two segments"
          assert by_segment.loc["retail", "total"] == 190.0, f"retail total should be 190.0, got {by_segment.loc['retail', 'total']}"
          assert by_segment.loc["business", "orders"] == 2, f"business should have 2 orders, got {by_segment.loc['business', 'orders']}"
          """,
          ["Named aggregation: `.agg(new_name=(column, function), ...)`."]),

        T("pivot", "A pivot table",
          """
          Store a pivot table of `orders` in `pivot`: one row per `customer_id`, one column per month **in the order Jan, Feb, Mar**,
          values the summed `amount`, and `0` where a customer had no orders that month.
          """,
          """
          pivot = orders.pivot_table(index="customer_id", columns="month", values="amount", aggfunc="sum")
          """,
          """
          pivot = orders.pivot_table(index="customer_id", columns="month", values="amount", aggfunc="sum", fill_value=0)
          pivot = pivot[["Jan", "Feb", "Mar"]]
          """,
          """
          assert isinstance(pivot, pd.DataFrame), "pivot should be a DataFrame"
          assert list(pivot.columns) == ["Jan", "Feb", "Mar"], f"columns should be Jan, Feb, Mar in that order, got {list(pivot.columns)} (pivot_table sorts them alphabetically)"
          assert not pivot.isna().any().any(), "fill the gaps with 0 (fill_value=0)"
          assert pivot.loc[10].tolist() == [50, 35, 25], f"customer 10 should be [50, 35, 25], got {pivot.loc[10].tolist()}"
          assert pivot.loc[11, "Feb"] == 0, "customer 11 had no orders in February"
          """,
          ["`pivot_table(..., fill_value=0)` replaces empty cells.",
           "Select the columns in the order you want: `pivot[['Jan', 'Feb', 'Mar']]`."]),

        T("melt", "Wide to long",
          """
          Reshape `wide` into `long`, with one row per store and quarter and the columns `store`, `quarter` and `sales`.
          """,
          """
          long = wide
          """,
          """
          long = wide.melt(id_vars="store", var_name="quarter", value_name="sales")
          """,
          """
          assert isinstance(long, pd.DataFrame), "long should be a DataFrame"
          assert list(long.columns) == ["store", "quarter", "sales"], f"columns should be store, quarter, sales, got {list(long.columns)}"
          assert len(long) == 4, f"2 stores x 2 quarters = 4 rows, got {len(long)}"
          got = sorted(zip(long["store"], long["quarter"], long["sales"]))
          assert got == [("A", "Q1", 100), ("A", "Q2", 120), ("B", "Q1", 80), ("B", "Q2", 90)], f"got {got}"
          """,
          ["`melt` is the reverse of pivot: `id_vars` stay as columns, every other column becomes rows.",
           "`var_name` and `value_name` name the two new columns."]),
    ],
)
