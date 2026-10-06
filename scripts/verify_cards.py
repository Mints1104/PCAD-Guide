"""Run every syntax flashcard's answer against small sample data and check it does what the card asks.

Each card's `back` is a snippet that relies on names such as `df` or `url`. FIXTURES gives each card a
setup (the sample data) and a check (asserts on the result). The value of a snippet's last expression
is available to the check as `_`. SQL cards run against an in-memory SQLite database built by `setup`.

Usage: python scripts/verify_cards.py [card-id ...]
"""

import ast
import contextlib
import io
import json
import os
import sqlite3
import sys
import tempfile
import threading
import traceback
import warnings
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

PRELUDE = """
import json
import sqlite3
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
"""

SHOP_SQL = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, region TEXT);
INSERT INTO customers VALUES (1, 'Ana', 'EU'), (2, 'Ben', 'US'), (3, 'Cara', 'EU'), (4, 'Dev', 'APAC');
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, region TEXT, status TEXT, total REAL);
"""

# card id -> {"setup": python run before the snippet, "check": python run after it,
#             "sql": SQLite script to build the database (SQL cards), "skip": reason}
FIXTURES = {
    "read-csv": {
        "setup": 'open("sales.csv", "w").write("region;amount\\nEU;N/A\\nUS;-999\\nUK;5\\n")',
        "check": 'assert df.shape == (3, 2) and df["amount"].isna().sum() == 2 and df["amount"].iloc[2] == 5',
    },
    "to-csv": {
        "setup": 'df = pd.DataFrame({"a": [1, 2]}, index=[10, 11])',
        "check": 'assert open("clean.csv").read().splitlines() == ["a", "1", "2"]',
    },
    "json-loads": {
        "setup": 'text = \'{"a": 1, "b": [1, 2], "ok": true}\'',
        "check": 'assert json.load(open("out.json", encoding="utf-8")) == {"a": 1, "b": [1, 2], "ok": True}',
    },
    "json-normalize": {
        "setup": 'records = [{"id": 1, "customer": {"name": "Ana", "city": "Oslo"}},'
                 ' {"id": 2, "customer": {"name": "Ben", "city": "Rome"}}]',
        "check": 'assert sorted(df.columns) == ["customer.city", "customer.name", "id"] and len(df) == 2',
    },
    "xml-parse": {
        "setup": "xml = '<library><book id=\"b1\"><title>Dune</title></book>"
                 "<book id=\"b2\"><title>Emma</title></book></library>'",
        "check": 'assert _ == [("b1", "Dune"), ("b2", "Emma")]',
    },
    "requests-get": {
        "setup": 'url = SERVER + "/api"',
        "check": """
assert data == {"page": "1"}, data
bad = requests.get(SERVER + "/missing", timeout=10)
try:
    bad.raise_for_status()
    raise AssertionError("expected HTTPError")
except requests.HTTPError:
    pass
""",
    },
    "bs4-links": {
        "setup": "html = '<a class=\"product\" href=\"/p1\">A</a><a class=\"nav\" href=\"/home\">H</a>"
                 "<a class=\"product sale\" href=\"/p2\">B</a>'",
        "check": 'assert links == ["/p1", "/p2"], links',
    },
    "isna-sum": {
        "setup": 'df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", None]})',
        "check": 'assert _.to_dict() == {"a": 1, "b": 1}',
    },
    "fillna-median": {
        "setup": 'df = pd.DataFrame({"income": [10.0, None, 30.0, 100.0]})',
        "check": 'assert df["income"].tolist() == [10.0, 30.0, 30.0, 100.0]',
    },
    "group-impute": {
        "setup": 'df = pd.DataFrame({"region": ["EU", "EU", "EU", "US", "US"], "age": [20.0, None, 40.0, 50.0, None]})',
        "check": 'assert df["age"].tolist() == [20.0, 30.0, 40.0, 50.0, 50.0], df["age"].tolist()',
    },
    "iqr-outliers": {
        "setup": "s = pd.Series([12, 14, 15, 15, 16, 18, 19, 45])",
        "check": "assert outliers.tolist() == [45]",
    },
    "minmax": {
        "setup": "s = pd.Series([20, 30, 50, 100])",
        "check": "assert _.tolist() == [0.0, 0.125, 0.375, 1.0]",
    },
    "zscore": {
        "setup": "s = pd.Series([2.0, 4.0, 6.0, 8.0])",
        "check": "assert abs(_.mean()) < 1e-12 and abs(_.std() - 1) < 1e-12",
    },
    "get-dummies": {
        "setup": 'df = pd.DataFrame({"id": [1, 2, 3], "color": ["red", "blue", "red"]})',
        "check": """
assert list(df.columns) == ["id", "color_blue", "color_red"]
assert df["color_red"].tolist() == [1, 0, 1] and str(df["color_red"].dtype).startswith("int")
""",
    },
    "to-numeric": {
        "setup": 'df = pd.DataFrame({"price": ["$1,200", "85", "n/a"]})',
        "check": 'v = df["price"].tolist(); assert v[:2] == [1200.0, 85.0] and pd.isna(v[2])',
    },
    "str-clean": {
        "setup": 'df = pd.DataFrame({"name": ["  ana ", "BEN", "cara lee"]})',
        "check": 'assert df["name"].tolist() == ["Ana", "Ben", "Cara Lee"]',
    },
    "cut": {
        "setup": 'df = pd.DataFrame({"age": [5, 12, 13, 19, 20, 120]})',
        "check": 'assert _.tolist() == ["child", "child", "teen", "teen", "adult", "adult"], _.tolist()',
    },
    "between": {
        "setup": 'df = pd.DataFrame({"age": [-1, 0, 50, 120, 121]})',
        "check": 'assert _["age"].tolist() == [-1, 121]',
    },
    "is-unique": {
        "setup": 'df = pd.DataFrame({"order_id": [1, 2, 2]})',
        "check": "assert _ is False or _ == False  # noqa: E712",
    },
    "melt": {
        "setup": 'df = pd.DataFrame({"store": ["A", "B"], "Jan": [1, 2], "Feb": [3, 4], "Mar": [5, 6]})',
        "check": 'assert _.shape == (6, 3) and list(_.columns) == ["store", "month", "sales"]',
    },
    "split": {
        "setup": "X = list(range(50)); y = [0] * 40 + [1] * 10",
        "check": "assert len(X_test) == 10 and sum(y_test) == 2 and len(X_train) == 40",
    },
    "to-datetime": {
        "setup": 'df = pd.DataFrame({"date": ["2025-07-15", "not a date"]})',
        "check": 'assert df["weekday"].iloc[0] == "Tuesday" and pd.isna(df["date"].iloc[1])',
    },
    "enumerate": {
        "setup": 'items = ["tea", "jam"]',
        "check": 'assert OUT == "1 tea\\n2 jam", OUT',
    },
    "comprehension": {
        "setup": 'words = ["data", "is", "python", "sql"]',
        "check": 'assert _ == {"data": 4, "python": 6}',
    },
    "dict-get": {
        "setup": 'counts = {"a": 2}; key = "b"',
        "check": "assert _ == 0",
    },
    "none-default": {
        "check": "assert add(1) == [1] and add(2) == [2] and add(3, [0]) == [0, 3]",
    },
    "try-except": {
        "setup": 'text = "12a"',
        "check": "assert value is None",
    },
    "pip-upgrade": {"skip": "shell commands; checked against the pip documentation instead"},
    "property": {
        "wrap": "class Product:\n    def __init__(self, price):\n        self.price = price\n\n{body}",
        "check": """
p = Product(5)
p.price = 7
assert p.price == 7
try:
    Product(-1)
    raise AssertionError("expected ValueError")
except ValueError:
    pass
""",
    },
    "super-init": {
        "setup": "class Exporter:\n    def __init__(self, rows):\n        self.rows = rows",
        "check": "e = JsonExporter([[1, 2]]); assert e.rows == [[1, 2]] and e.indent == 2",
    },
    "eq": {
        "wrap": "class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\n{body}",
        "check": "assert Point(1, 2) == Point(1, 2) and Point(1, 2) != Point(2, 1) and Point(1, 2) != (1, 2)",
    },
    "sql-having": {
        "sql": SHOP_SQL + "".join(
            f"INSERT INTO orders (customer_id, region, status, total) VALUES (1, '{r}', '{s}', 10);\n"
            for r, s, n in [("EU", "paid", 12), ("US", "paid", 15), ("APAC", "paid", 5), ("US", "refunded", 9)]
            for _ in range(n)),
        "check": 'assert ROWS == [("US", 15), ("EU", 12)], ROWS',
    },
    "sql-left-null": {
        "sql": SHOP_SQL + "INSERT INTO orders (customer_id, region, status, total) VALUES "
                          "(1, 'EU', 'paid', 10), (2, 'US', 'paid', 5), (3, 'EU', 'paid', 7), (9, 'EU', 'paid', 1);",
        "check": 'assert ROWS == [("Dev",)], ROWS',
    },
    "sql-update": {
        "sql": "CREATE TABLE products (id INTEGER PRIMARY KEY, price REAL);"
               "INSERT INTO products VALUES (6, 10.0), (7, 10.0), (8, 10.0);",
        "check": 'p = dict(CON.execute("SELECT id, price FROM products").fetchall()); '
                 "assert abs(p[7] - 11.0) < 1e-9 and p[6] == 10.0 and p[8] == 10.0, p",
    },
    "sqlite-connect": {
        "setup": 'c = sqlite3.connect("shop.db"); c.execute("CREATE TABLE orders (id INTEGER, total REAL)"); '
                 'c.execute("INSERT INTO orders VALUES (1, 9.5)"); c.commit(); c.close()',
        "check": "assert rows == [(1, 9.5)]",
    },
    "sqlite-param": {
        "setup": 'con = sqlite3.connect(":memory:"); con.execute("CREATE TABLE users (name TEXT, role TEXT)"); '
                 "con.execute(\"INSERT INTO users VALUES ('ana', 'admin'), ('ben', 'viewer')\"); "
                 'cur = con.cursor(); name = "ben"',
        "check": 'assert cur.fetchall() == [("ben", "viewer")]\n'
                 'cur.execute("SELECT * FROM users WHERE name = ?", ("x\' OR \'1\'=\'1",)); assert cur.fetchall() == []',
    },
    "pymysql-param": {"skip": "needs a MySQL server; %s is PyMySQL's documented placeholder (paramstyle 'pyformat')"},
    "executemany": {
        "setup": 'con = sqlite3.connect("shop.db"); con.execute("CREATE TABLE products (name TEXT, price REAL)"); '
                 'rows = [("tea", 2.5), ("jam", 4.0)]',
        "check": 'other = sqlite3.connect("shop.db"); '
                 'assert other.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 2  # committed',
    },
    "read-sql": {
        "setup": 'con = sqlite3.connect(":memory:"); con.execute("CREATE TABLE orders (id INTEGER, order_date TEXT)"); '
                 "con.execute(\"INSERT INTO orders VALUES (1, '2025-07-15')\")",
        "check": 'assert df["order_date"].dtype.kind == "M" and df["order_date"].iloc[0].day == 15',
    },
    "np-std": {
        "setup": "x = [2, 4, 6]",
        "check": "assert _ == 2.0",
    },
    "corr": {
        "setup": 'df = pd.DataFrame({"ads": [1, 2, 3, 4], "sales": [10, 20, 30, 40]})',
        "check": "assert abs(_ - 1.0) < 1e-12",
    },
    "bootstrap": {
        "setup": "x = np.array([12, 15, 11, 30, 14, 13, 16, 12, 15, 14])",
        "check": "assert len(_) == 2 and _[0] <= np.median(x) <= _[1] and _[0] < _[1]",
    },
    "linreg": {
        "setup": "X = np.array([[1], [2], [3], [4]]); y = np.array([3, 5, 7, 9])",
        "check": "coef, intercept, r2 = _; assert abs(coef[0] - 2) < 1e-9 and abs(intercept - 1) < 1e-9 and abs(r2 - 1) < 1e-9",
    },
    "logreg": {
        "setup": "X_train = np.array([[1], [2], [3], [7], [8], [9]]); y_train = np.array([0, 0, 0, 1, 1, 1]); "
                 "X_test = np.array([[1], [9]])",
        "check": "assert _.shape == (2,) and _[0] < 0.5 < _[1]",
    },
    "dropna-subset": {
        "setup": 'df = pd.DataFrame({"email": ["a@x", None, "c@x"], "phone": [None, "1", "2"]})',
        "check": 'assert df["email"].tolist() == ["a@x", "c@x"]',
    },
    "drop-dups": {
        "setup": 'df = pd.DataFrame({"email": ["a@x", "b@x", "a@x"], "visit": [1, 2, 3]})',
        "check": 'assert df["visit"].tolist() == [2, 3]',
    },
    "loc-update": {
        "setup": 'df = pd.DataFrame({"qty": [1, 12, 5], "discount": [0.0, 0.0, 0.0]})',
        "check": 'assert df["discount"].tolist() == [0.0, 0.1, 0.0]',
    },
    "iloc-last": {
        "setup": 'df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})',
        "check": 'assert _.shape == (2, 2) and list(_.columns) == ["a", "b"] and df.iloc[-1].tolist() == [2, 4, 6]',
    },
    "merge-left": {
        "setup": 'orders = pd.DataFrame({"order": [1, 2, 3], "customer_id": [10, 11, 99]}); '
                 'customers = pd.DataFrame({"customer_id": [10, 11], "name": ["Ana", "Ben"]})',
        "check": 'assert len(_) == 3 and pd.isna(_.loc[_["customer_id"] == 99, "name"].iloc[0])',
    },
    "pivot-table": {
        "setup": 'df = pd.DataFrame({"region": ["EU", "EU", "US"], "quarter": ["Q1", "Q1", "Q2"], "revenue": [10, 5, 7]})',
        "check": 'assert _.loc["EU", "Q1"] == 15 and _.loc["EU", "Q2"] == 0 and _.loc["US", "Q2"] == 7',
    },
    "named-agg": {
        "setup": 'df = pd.DataFrame({"region": ["EU", "EU", "US"], "amount": [10, 30, 5], "order_id": [1, 2, 3]})',
        "check": 'assert list(_.columns) == ["total", "orders"] and _.loc["EU"].tolist() == [40, 2]',
    },
    "crosstab": {
        "setup": 'df = pd.DataFrame({"region": ["EU", "EU", "US", "US", "US"], "channel": ["web", "shop", "web", "web", "shop"]})',
        "check": "assert all(abs(t - 1) < 1e-12 for t in _.sum(axis=1)) and abs(_.loc['US', 'web'] - 2 / 3) < 1e-12",
    },
    "np-axis": {
        "setup": "a = np.array([[1, 2], [3, 4]])",
        "check": "assert _.tolist() == [3, 7] and a.mean(axis=0).tolist() == [2.0, 3.0]",
    },
    "np-reshape": {
        "check": "assert _.shape == (2, 3) and _[1].tolist() == [3, 4, 5]",
    },
    "describe": {
        "setup": 'df = pd.DataFrame({"x": [1, 2, 3], "name": ["a", "b", "c"]})',
        "check": 'assert list(_.columns) == ["x"] and _.loc["mean", "x"] == 2 and "50%" in _.index',
    },
    "cross-val": {
        "setup": "from sklearn.datasets import make_classification\n"
                 "X, y = make_classification(n_samples=100, random_state=0); model = LogisticRegression()",
        "check": "assert len(_) == 5 and all(0 <= s <= 1 for s in _)",
    },
    "tree-depth": {
        "setup": "from sklearn.datasets import make_classification\nX, y = make_classification(n_samples=200, random_state=0)",
        "check": "assert _.max_depth == 4 and _.fit(X, y).get_depth() <= 4",
    },
    "subplots": {
        "setup": 'df = pd.DataFrame({"sales": np.arange(100)})',
        "check": "assert axes.shape == (2,) and len(axes[0].patches) == 20",
    },
    "heatmap": {
        "setup": 'df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 5, 9], "label": list("wxyz")})',
        "check": "assert len(_.collections) == 1 and len(_.texts) == 4  # 2 x 2 numeric matrix, 4 annotations",
    },
    "boxplot": {
        "setup": 'df = pd.DataFrame({"department": ["A", "A", "B", "B"], "salary": [30, 40, 50, 70]})',
        "check": '_.figure.canvas.draw(); assert [t.get_text() for t in _.get_xticklabels()] == ["A", "B"]',
    },
    "legend": {
        "setup": 'fig, ax = plt.subplots(); ax.plot([1, 2], [1, 2], label="Sales")',
        "check": "import matplotlib.colors as mc\n"
                 "assert _._loc == 2 and _.get_texts()[0].get_fontsize() == 8 "
                 "and mc.to_hex(_.get_frame().get_facecolor()) == '#ffffff'",
    },
    "annotate": {
        "setup": "fig, ax = plt.subplots(); x_peak, y_peak = 5, 100",
        "check": "assert _.xy == (5, 100) and _.arrow_patch is not None and _.get_text() == 'Peak'",
    },
    "scatter-cmap": {
        "setup": 'fig, ax = plt.subplots(); df = pd.DataFrame({"x": [1, 2, 3], "y": [3, 1, 2], "z": [0.1, 0.5, 0.9]})',
        "check": "assert len(fig.axes) == 2  # the colour bar adds an Axes",
    },
    "savefig": {
        "setup": "fig, ax = plt.subplots(); ax.plot([1, 2], [3, 4])",
        "check": 'assert os.path.getsize("chart.png") > 0',
    },
}


class _Api(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path.startswith("/api"):
            from urllib.parse import parse_qs, urlparse
            body = json.dumps({k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        else:
            body = b"not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def run_snippet(code, ns):
    """Exec code; return (stdout, value of the last expression or None)."""
    tree = ast.parse(code)
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = ast.Expression(tree.body.pop().value)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(tree, "<card>", "exec"), ns)
        value = eval(compile(last, "<card>", "eval"), ns) if last else None
    return buf.getvalue().rstrip("\n"), value


def main():
    only = set(sys.argv[1:])
    cards = json.loads((ROOT / "content" / "cards" / "syntax.json").read_text(encoding="utf-8"))
    missing = [c["id"] for c in cards if c["id"] not in FIXTURES]
    server = HTTPServer(("127.0.0.1", 0), _Api)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    passed, skipped, failed = 0, [], []
    home = os.getcwd()
    for card in cards:
        if only and card["id"] not in only:
            continue
        fx = FIXTURES.get(card["id"])
        if fx is None:
            continue
        if "skip" in fx:
            skipped.append(f"{card['id']} ({fx['skip']})")
            continue
        work = tempfile.mkdtemp()
        os.chdir(work)
        try:
            ns = {"__name__": "__main__", "os": os, "SERVER": f"http://127.0.0.1:{server.server_port}"}
            exec(PRELUDE, ns)
            if "sql" in fx:
                con = sqlite3.connect(":memory:")
                con.executescript(fx["sql"])
                con.executescript(card["back"]) if card["back"].lstrip().upper().startswith("UPDATE") else None
                ns["ROWS"] = [] if card["back"].lstrip().upper().startswith("UPDATE") else con.execute(card["back"]).fetchall()
                ns["CON"] = con
            else:
                exec(fx.get("setup", ""), ns)
                body = card["back"]
                if "wrap" in fx:
                    body = fx["wrap"].format(body="\n".join("    " + line if line else line for line in body.split("\n")))
                ns["OUT"], ns["_"] = run_snippet(body, ns)
            exec(fx["check"], ns)
            passed += 1
        except Exception:  # noqa: BLE001
            failed.append((card["id"], traceback.format_exc(limit=3)))
        finally:
            os.chdir(home)
            import matplotlib.pyplot as plt
            plt.close("all")
    server.shutdown()
    for cid, detail in failed:
        print(f"FAIL {cid}\n  " + detail.replace("\n", "\n  "))
    print(f"\nverified {passed} card(s), {len(failed)} failed, {len(skipped)} skipped")
    for s in skipped:
        print(f"  skipped: {s}")
    if missing:
        print(f"cards without a fixture: {', '.join(missing)}")
    sys.exit(1 if failed or missing else 0)


if __name__ == "__main__":
    main()
