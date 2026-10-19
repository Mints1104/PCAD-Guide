from nbhelp import NB, T

NOTEBOOK = NB(
    "cleaning", "Cleaning a messy customer table", 2, ["1.2.2", "1.2.4", "1.3.1", "4.1.1"],
    "Strings, inconsistent categories, numbers stored as text, impossible dates, duplicates and validation rules.",
    """
    `raw` is a customer export with the usual problems: stray spaces and mixed case in names, three spellings of one country,
    ages stored as text (one of them negative), an impossible date, a duplicated row and a missing name.
    Each task fixes one problem and stores the result in a new variable, so `raw` itself never changes.
    """,
    """
    import numpy as np
    import pandas as pd

    raw = pd.DataFrame({
        "customer": [" Ana Silva", "ben ong", "Cara  Diaz", "ben ong", "Dev Rao ", None],
        "country": ["UK", "uk", "U.K.", "uk", "India", "France"],
        "age": ["34", "29", "n/a", "29", "-5", "41"],
        "spend": [120.5, 80.0, np.nan, 80.0, 310.0, 55.25],
        "signup": ["2024-01-15", "2024-02-03", "2024-02-30", "2024-02-03", "2024-03-12", "2024-04-01"],
    })
    """,
    [
        T("names", "Standardize the names",
          """
          Make a Series `names` from `raw["customer"]` with surrounding spaces removed, runs of internal spaces
          collapsed to one, and title case (`"Cara  Diaz"` → `"Cara Diaz"`, `"ben ong"` → `"Ben Ong"`). The missing name stays missing.
          """,
          """
          names = raw["customer"]
          """,
          """
          names = raw["customer"].str.strip().str.replace(r"\\s+", " ", regex=True).str.title()
          """,
          """
          assert isinstance(names, pd.Series), "names should be a Series"
          assert len(names) == 6, "keep all six rows"
          assert names.iloc[:5].tolist() == ["Ana Silva", "Ben Ong", "Cara Diaz", "Ben Ong", "Dev Rao"], f"got {names.iloc[:5].tolist()}"
          assert pd.isna(names.iloc[5]), "the missing name should still be missing (the .str methods pass missing values through)"
          """,
          ["The `.str` accessor applies string methods to every value: `.str.strip()`, `.str.title()`.",
           "`.str.replace(r'\\s+', ' ', regex=True)` turns any run of whitespace into one space."]),

        T("country", "One spelling per country",
          """
          Make a Series `country` where every spelling of the United Kingdom becomes `"UK"`. Other countries stay as they are.
          """,
          """
          country = raw["country"]
          """,
          """
          country = raw["country"].replace({"uk": "UK", "U.K.": "UK"})
          """,
          """
          assert isinstance(country, pd.Series), "country should be a Series"
          assert country.tolist() == ["UK", "UK", "UK", "UK", "India", "France"], f"got {country.tolist()}"
          """,
          ["`Series.replace({old: new, ...})` swaps whole values using a dictionary.",
           "Upper-casing everything would also change `India` to `INDIA`, which the task does not want."]),

        T("age", "Ages as numbers, invalid ones missing",
          """
          Make a numeric Series `age` from `raw["age"]`. Text that is not a number becomes missing (`NaN`),
          and so does any negative age, since it cannot be right.
          """,
          """
          age = raw["age"].astype(int)
          """,
          """
          age = pd.to_numeric(raw["age"], errors="coerce")
          age = age.where(age >= 0)
          """,
          """
          assert isinstance(age, pd.Series), "age should be a Series"
          assert pd.api.types.is_numeric_dtype(age), f"age should be numeric, got dtype {age.dtype}"
          got = [None if pd.isna(a) else a for a in age]
          assert got[2] is None, "'n/a' should become missing"
          assert got[4] is None, "the negative age (-5) should become missing"
          assert got == [34, 29, None, 29, None, 41], f"got {got}"
          """,
          ["`pd.to_numeric(s, errors='coerce')` turns unparseable text into NaN instead of raising.",
           "`s.where(condition)` keeps values where the condition is True and puts NaN elsewhere."]),

        T("dates", "Parse dates, flag impossible ones",
          """
          Make a datetime Series `signup` from `raw["signup"]`. 30 February does not exist, so that value should become `NaT`.
          """,
          """
          signup = raw["signup"]
          """,
          """
          signup = pd.to_datetime(raw["signup"], errors="coerce")
          """,
          """
          assert isinstance(signup, pd.Series), "signup should be a Series"
          assert pd.api.types.is_datetime64_any_dtype(signup), f"signup should have a datetime dtype, got {signup.dtype}"
          assert signup.isna().tolist() == [False, False, True, False, False, False], "only 2024-02-30 should be missing"
          assert signup.iloc[0] == pd.Timestamp("2024-01-15"), "the first date should be 15 January 2024"
          """,
          ["`pd.to_datetime` takes `errors='coerce'` too, giving NaT (not a time) for impossible dates."]),

        T("dedupe", "Drop duplicates and nameless rows",
          """
          Make `clean`: `raw` without exact duplicate rows and without rows where `customer` is missing, with a fresh
          index `0, 1, 2, ...`. Do not fix the strings here; this task is only about which rows survive.
          """,
          """
          clean = raw.copy()
          """,
          """
          clean = raw.drop_duplicates().dropna(subset=["customer"]).reset_index(drop=True)
          """,
          """
          assert isinstance(clean, pd.DataFrame), "clean should be a DataFrame"
          assert len(clean) == 4, f"clean should have 4 rows, got {len(clean)}"
          assert list(clean.index) == [0, 1, 2, 3], f"reset the index (drop=True), got {list(clean.index)}"
          assert clean["customer"].tolist() == [" Ana Silva", "ben ong", "Cara  Diaz", "Dev Rao "], f"got {clean['customer'].tolist()}"
          assert list(clean.columns) == list(raw.columns), "keep every column (reset_index(drop=True) does not add an index column)"
          """,
          ["`drop_duplicates()` compares whole rows; `dropna(subset=[...])` looks only at the columns you name.",
           "`reset_index(drop=True)` renumbers the rows without keeping the old index as a column."]),

        T("validate", "A reusable validation rule",
          """
          Write `validate(df)` that returns a **list of index labels** for rows that break a rule:

          - `spend` is missing or negative, or
          - `age` (converted as in task 3) is missing or outside 0 to 120.

          `validate(raw)` should return `[2, 4]`.
          """,
          """
          def validate(df):
              return []
          """,
          """
          def validate(df):
              age = pd.to_numeric(df["age"], errors="coerce")
              bad_age = age.isna() | (age < 0) | (age > 120)
              bad_spend = df["spend"].isna() | (df["spend"] < 0)
              return df.index[bad_age | bad_spend].tolist()
          """,
          """
          got = validate(raw)
          assert isinstance(got, list), f"validate should return a list, got {type(got).__name__} (an Index has .tolist())"
          assert got == [2, 4], f"validate(raw) returned {got}, expected [2, 4]"
          test = pd.DataFrame({"age": ["10", "200", "x", "50"], "spend": [5.0, 1.0, 3.0, -2.0]}, index=[7, 8, 9, 10])
          assert validate(test) == [8, 9, 10], f"on another table validate returned {validate(test)}, expected [8, 9, 10]: return labels, not positions, and check age > 120 and negative spend"
          """,
          ["Build one boolean Series per rule, then combine them with `|`.",
           "`df.index[mask]` picks the labels where the mask is True."]),
    ],
)
