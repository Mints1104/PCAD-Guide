from nbhelp import NB, T

NOTEBOOK = NB(
    "acquisition", "Reading CSV, JSON and HTML", 2, ["1.1.2", "1.4.1", "1.4.3"],
    "European-style CSV, nested JSON from an API, scraping a table with BeautifulSoup, and combining sources.",
    """
    Three raw inputs held as text, as they would arrive from a file, an API and a web page,
    plus two shop exports that name their columns differently.
    """,
    '''
    import io
    import json
    import pandas as pd

    csv_text = """date;city;temp_c
    01/03/2024;Leeds;7,5
    02/03/2024;Leeds;8,1
    01/03/2024;York;6,9
    02/03/2024;York;
    """

    json_text = """{"meta": {"source": "api", "page": 1},
     "results": [
      {"id": 1, "user": {"name": "Ana", "country": "PT"}, "score": 9.5},
      {"id": 2, "user": {"name": "Ben", "country": "UK"}, "score": 7.0},
      {"id": 3, "user": {"name": "Cara", "country": "ES"}, "score": null}
     ]}"""

    html_text = """<html><body>
    <h1>Price list</h1>
    <table id="prices">
      <tr><th>Item</th><th>Price</th></tr>
      <tr><td>Tea</td><td>£2.50</td></tr>
      <tr><td>Coffee</td><td>£3.10</td></tr>
      <tr><td>Cake</td><td>£4.00</td></tr>
    </table>
    <table id="hours"><tr><td>Mon</td><td>9-5</td></tr></table>
    </body></html>"""

    shop_a = pd.DataFrame({"sku": ["A1", "B2"], "qty": [3, 5]})
    shop_b = pd.DataFrame({"SKU": ["C3", "A1"], "quantity": [2, 1]})
    ''',
    [
        T("csv", "A European-style CSV",
          """
          Read `csv_text` into the DataFrame `weather`. Fields are separated by `;`, decimals use a comma,
          and dates are day first (`02/03/2024` is 2 March). Make `date` a datetime column and `temp_c` a float column.
          """,
          """
          weather = pd.read_csv(io.StringIO(csv_text))
          """,
          """
          weather = pd.read_csv(io.StringIO(csv_text), sep=";", decimal=",")
          weather["date"] = pd.to_datetime(weather["date"], format="%d/%m/%Y")
          """,
          """
          assert isinstance(weather, pd.DataFrame), "weather should be a DataFrame"
          assert list(weather.columns) == ["date", "city", "temp_c"], f"columns are {list(weather.columns)}: set sep=';'"
          assert pd.api.types.is_float_dtype(weather["temp_c"]), f"temp_c has dtype {weather['temp_c'].dtype}: set decimal=','"
          assert [None if pd.isna(t) else t for t in weather["temp_c"]] == [7.5, 8.1, 6.9, None], f"temp_c is {weather['temp_c'].tolist()}"
          assert pd.api.types.is_datetime64_any_dtype(weather["date"]), "date should be a datetime column"
          assert weather["date"].iloc[1] == pd.Timestamp("2024-03-02"), f"02/03/2024 should be 2 March 2024, got {weather['date'].iloc[1]}"
          """,
          ["`io.StringIO(text)` lets `read_csv` read a string as if it were a file.",
           "`read_csv(..., sep=';', decimal=',')`; for the dates use `pd.to_datetime(..., format='%d/%m/%Y')` or `dayfirst=True`."]),

        T("json", "Parse JSON",
          """
          Parse `json_text` into `data` with the `json` module, then store the list of user names in `names`.
          """,
          """
          data = json_text
          names = []
          """,
          """
          data = json.loads(json_text)
          names = [r["user"]["name"] for r in data["results"]]
          """,
          """
          assert isinstance(data, dict), "data should be the parsed dictionary (json.loads)"
          assert names == ["Ana", "Ben", "Cara"], f"names is {names}"
          assert data["results"][2]["score"] is None, "JSON null becomes Python None"
          """,
          ["`json.loads` parses a string; `json.load` reads from a file object.",
           "Nested JSON becomes nested dicts and lists: `record['user']['name']`."]),

        T("normalize", "Flatten nested records",
          """
          Turn `data["results"]` into a flat DataFrame `flat` with one column per field, including `user.name` and `user.country`.
          Parse `json_text` again inside this cell.
          """,
          """
          data = json.loads(json_text)
          flat = pd.DataFrame(data["results"])
          """,
          """
          data = json.loads(json_text)
          flat = pd.json_normalize(data["results"])
          """,
          """
          assert isinstance(flat, pd.DataFrame), "flat should be a DataFrame"
          assert {"id", "score", "user.name", "user.country"} <= set(flat.columns), f"columns are {list(flat.columns)}; the nested user dict should become user.name and user.country"
          assert len(flat) == 3, "one row per result"
          assert flat["user.country"].tolist() == ["PT", "UK", "ES"], f"user.country is {flat['user.country'].tolist()}"
          assert flat["score"].isna().sum() == 1, "Cara's null score should be missing"
          """,
          ["`pd.DataFrame(records)` keeps the nested dict in one column; `pd.json_normalize(records)` spreads it into dotted columns."]),

        T("html", "Scrape a table",
          """
          Parse `html_text` with BeautifulSoup and build the dict `prices` mapping each item in the **prices** table to its price
          as a float, e.g. `{"Tea": 2.5, ...}`. Ignore the header row and the other table.
          """,
          """
          from bs4 import BeautifulSoup

          soup = BeautifulSoup(html_text, "html.parser")
          prices = {}
          """,
          """
          from bs4 import BeautifulSoup

          soup = BeautifulSoup(html_text, "html.parser")
          prices = {}
          for row in soup.select("#prices tr")[1:]:
              item, price = [td.get_text(strip=True) for td in row.find_all("td")]
              prices[item] = float(price.lstrip("£"))
          """,
          """
          assert isinstance(prices, dict), "prices should be a dict"
          assert prices == {"Tea": 2.5, "Coffee": 3.1, "Cake": 4.0}, f"prices is {prices}"
          """,
          ["`soup.select('#prices tr')` finds the rows of the table with `id=\"prices\"`; `[1:]` skips the header row.",
           "`td.get_text(strip=True)` gives the cell text; remove the `£` before `float()`."]),

        T("combine", "Combine two sources",
          """
          Rename `shop_b`'s columns to match `shop_a`, add a `source` column (`"a"` or `"b"`) to each, and stack them into `combined`
          with a fresh index. Then store the total `qty` per `sku` in the Series `totals`.
          """,
          """
          combined = pd.concat([shop_a, shop_b])
          totals = combined
          """,
          """
          a = shop_a.assign(source="a")
          b = shop_b.rename(columns={"SKU": "sku", "quantity": "qty"}).assign(source="b")
          combined = pd.concat([a, b], ignore_index=True)
          totals = combined.groupby("sku")["qty"].sum()
          """,
          """
          assert isinstance(combined, pd.DataFrame), "combined should be a DataFrame"
          assert sorted(combined.columns) == ["qty", "sku", "source"], f"columns are {list(combined.columns)}: rename SKU and quantity before concatenating"
          assert list(combined.index) == [0, 1, 2, 3], "use ignore_index=True for a fresh index"
          assert sorted(zip(combined["sku"], combined["source"])) == [("A1", "a"), ("A1", "b"), ("B2", "a"), ("C3", "b")], "each row should record which shop it came from"
          assert isinstance(totals, pd.Series) and totals.to_dict() == {"A1": 4, "B2": 5, "C3": 2}, f"totals should be A1: 4, B2: 5, C3: 2, got {totals.to_dict() if isinstance(totals, pd.Series) else totals}"
          """,
          ["`pd.concat` lines columns up by name, so mismatched names give extra columns full of NaN.",
           "`df.rename(columns={...})` and `df.assign(source='a')` each return a new DataFrame."]),
    ],
)
