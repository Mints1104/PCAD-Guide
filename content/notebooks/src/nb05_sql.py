from nbhelp import NB, T

NOTEBOOK = NB(
    "sql", "SQL from Python with sqlite3", 2, ["2.4.1", "2.4.2", "2.4.3", "2.4.4", "2.4.6"],
    "SELECT, JOIN and GROUP BY, parameterized queries, INSERT, UPDATE and DELETE, and read_sql_query.",
    """
    An in-memory SQLite database with two tables; `con` is the open connection. The `products` table:

    | id | name | category | price |
    |---|---|---|---|
    | 1 | Notebook | stationery | 3.5 |
    | 2 | Pen | stationery | 1.2 |
    | 3 | Desk lamp | office | 24.0 |
    | 4 | Chair | office | 89.0 |
    | 5 | Mug | kitchen | 6.0 |
    | 6 | Ruler | stationery | 2.0 |

    `sales(id, product_id, qty, day)` has six sales; the Ruler has never sold.
    """,
    '''
    import sqlite3

    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT, price REAL);
    INSERT INTO products VALUES
      (1, 'Notebook', 'stationery', 3.5),
      (2, 'Pen', 'stationery', 1.2),
      (3, 'Desk lamp', 'office', 24.0),
      (4, 'Chair', 'office', 89.0),
      (5, 'Mug', 'kitchen', 6.0),
      (6, 'Ruler', 'stationery', 2.0);
    CREATE TABLE sales (id INTEGER PRIMARY KEY, product_id INTEGER REFERENCES products(id), qty INTEGER, day TEXT);
    INSERT INTO sales VALUES
      (1, 1, 10, '2024-05-01'), (2, 2, 25, '2024-05-01'), (3, 3, 2, '2024-05-02'),
      (4, 1, 4, '2024-05-02'), (5, 5, 6, '2024-05-03'), (6, 4, 1, '2024-05-03');
    """)
    ''',
    [
        T("where-order", "Filter and sort",
          """
          Store the `(name, price)` rows of products cheaper than 5.00, cheapest first, in `cheap` (a list of tuples from `fetchall()`).
          """,
          """
          query = "SELECT name, price FROM products"
          cheap = con.execute(query).fetchall()
          """,
          """
          query = "SELECT name, price FROM products WHERE price < 5 ORDER BY price"
          cheap = con.execute(query).fetchall()
          """,
          """
          assert isinstance(cheap, list), "cheap should be the list that fetchall() returns"
          assert cheap == [("Pen", 1.2), ("Ruler", 2.0), ("Notebook", 3.5)], f"got {cheap}"
          """,
          ["`WHERE price < 5` filters; `ORDER BY price` sorts ascending (add `DESC` for descending)."]),

        T("join-group", "JOIN and GROUP BY",
          """
          Store the total quantity sold per category, as `(category, total_qty)` rows sorted by category, in `by_category`.
          Categories with no sales may be left out.
          """,
          """
          by_category = con.execute("SELECT category FROM products").fetchall()
          """,
          """
          by_category = con.execute(\"\"\"
              SELECT p.category, SUM(s.qty) AS total_qty
              FROM sales AS s
              JOIN products AS p ON p.id = s.product_id
              GROUP BY p.category
              ORDER BY p.category
          \"\"\").fetchall()
          """,
          """
          assert isinstance(by_category, list), "by_category should be a list of rows"
          assert by_category == [("kitchen", 6), ("office", 3), ("stationery", 39)], f"got {by_category}"
          """,
          ["Join `sales` to `products` on `products.id = sales.product_id`, then `GROUP BY category`.",
           "Every selected column must be grouped or aggregated: `SELECT category, SUM(qty)`."]),

        T("params", "A parameterized query",
          """
          Write `find_by_category(con, category)` that returns the product **names** in that category, sorted by name.
          Pass `category` with a `?` placeholder; never build the SQL with string formatting.
          """,
          """
          def find_by_category(con, category):
              sql = f"SELECT name FROM products WHERE category = '{category}' ORDER BY name"
              return [row[0] for row in con.execute(sql)]
          """,
          """
          def find_by_category(con, category):
              sql = "SELECT name FROM products WHERE category = ? ORDER BY name"
              return [row[0] for row in con.execute(sql, (category,))]
          """,
          """
          assert find_by_category(con, "office") == ["Chair", "Desk lamp"], f"office gave {find_by_category(con, 'office')}"
          assert find_by_category(con, "kitchen") == ["Mug"], "kitchen should give ['Mug']"
          try:
              attack = find_by_category(con, "x' OR '1'='1")
          except Exception as exc:
              raise AssertionError(f"a category containing a quote broke the query ({type(exc).__name__}); use a ? placeholder")
          assert attack == [], f"the input x' OR '1'='1 returned {attack}: the SQL was built from the text (SQL injection). Use a ? placeholder"
          """,
          ["`con.execute(sql, (value,))`: the parameters go in a tuple; note the comma in a one-item tuple.",
           "The driver sends the value separately from the SQL, so quotes in it cannot change the query."]),

        T("read-sql", "Query results as a DataFrame",
          """
          Use `pd.read_sql_query` to make `revenue`: a DataFrame with the columns `day` and `revenue` (sum of `qty * price`), one row per day, sorted by day.
          """,
          """
          import pandas as pd

          revenue = pd.read_sql_query("SELECT day FROM sales", con)
          """,
          """
          import pandas as pd

          revenue = pd.read_sql_query(\"\"\"
              SELECT s.day, SUM(s.qty * p.price) AS revenue
              FROM sales AS s
              JOIN products AS p ON p.id = s.product_id
              GROUP BY s.day
              ORDER BY s.day
          \"\"\", con)
          """,
          """
          assert isinstance(revenue, pd.DataFrame), "revenue should be a DataFrame"
          assert list(revenue.columns) == ["day", "revenue"], f"columns should be day and revenue, got {list(revenue.columns)} (alias the sum: AS revenue)"
          assert revenue["day"].tolist() == ["2024-05-01", "2024-05-02", "2024-05-03"], f"days: {revenue['day'].tolist()}"
          assert [round(v, 2) for v in revenue["revenue"]] == [65.0, 62.0, 125.0], f"revenue: {revenue['revenue'].tolist()}"
          """,
          ["`pd.read_sql_query(sql, con)` runs the query and builds a DataFrame from the rows and column names."]),
        T("insert", "INSERT and commit",
          """
          Write `add_product(con, name, category, price)` that inserts a product with a parameterized `INSERT`,
          commits, and returns the new row's `id`. Leave out `id` so SQLite assigns the next one.
          """,
          """
          def add_product(con, name, category, price):
              pass
          """,
          """
          def add_product(con, name, category, price):
              cur = con.execute(
                  "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                  (name, category, price),
              )
              con.commit()
              return cur.lastrowid
          """,
          """
          new_id = add_product(con, "Stapler", "stationery", 7.5)
          assert new_id == 7, f"add_product should return the new id (7), got {new_id!r}; the cursor's lastrowid holds it"
          row = con.execute("SELECT name, category, price FROM products WHERE id = ?", (new_id,)).fetchone()
          assert row == ("Stapler", "stationery", 7.5), f"the inserted row is {row}"
          assert not con.in_transaction, "commit after the insert"
          """,
          ["`cur = con.execute(...)` returns a cursor; `cur.lastrowid` is the id SQLite assigned.",
           "`con.commit()` makes the change permanent."]),

        T("update-delete", "UPDATE and DELETE",
          """
          Raise every `office` price by 10%, then delete products that have never been sold. Commit at the end.
          """,
          """
          # your UPDATE and DELETE statements
          """,
          """
          con.execute("UPDATE products SET price = price * 1.1 WHERE category = ?", ("office",))
          con.execute("DELETE FROM products WHERE id NOT IN (SELECT product_id FROM sales)")
          con.commit()
          """,
          """
          office = [round(p, 2) for (p,) in con.execute("SELECT price FROM products WHERE category = 'office' ORDER BY price")]
          assert office == [26.4, 97.9], f"office prices are {office}, expected [26.4, 97.9]"
          others = con.execute("SELECT price FROM products WHERE category = 'stationery' ORDER BY price").fetchall()
          assert others == [(1.2,), (3.5,)], f"only office prices should change (and the Ruler should be gone); stationery prices are {others}"
          names = [n for (n,) in con.execute("SELECT name FROM products")]
          assert "Ruler" not in names, "the Ruler has no sales, so it should be deleted"
          assert len(names) == 5, f"5 products should remain, found {len(names)}"
          assert not con.in_transaction, "commit at the end"
          """,
          ["`UPDATE products SET price = price * 1.1 WHERE ...`: without WHERE, every row changes.",
           "`DELETE FROM products WHERE id NOT IN (SELECT product_id FROM sales)`."]),

    ],
)
