# Block 1: Data Acquisition and Pre-Processing

Block 1 is 14 items, 29.2% of the exam: how data is collected and stored, how to spot and fix what is wrong with it, how to validate it, and how to read it in from files, databases, APIs and web pages. Expect scenario questions ("a retailer has survey data where…") and short pandas snippets.

## 1.1.1 Compare data collection methods

**Syllabus asks:** compare surveys, interviews and web scraping; representative sampling; qualitative vs quantitative research; legal and ethical considerations; anonymizing PII; how collection choices feed business strategy, market research, risk assessment and policy-making; survey design and structured interviews.

### Core facts

| Method | Gives you | Strengths | Weaknesses |
|---|---|---|---|
| Survey (questionnaire) | Mostly quantitative answers from many people | Cheap per response, scales, easy to analyze when questions are closed | Shallow; wording and non-response bias |
| Interview | Qualitative depth from few people | Explains *why*; follow-up questions | Slow, expensive, small samples, interviewer bias |
| Observation / experiment | Behaviour as it happens; A/B tests give causal evidence | Not self-reported | Costly; the observer can change behaviour |
| Web scraping | Data published on websites | Large volumes, automated | Legal limits (terms of service, copyright, personal data); fragile when pages change |
| API | Structured data a provider chooses to share | Stable, documented, usually JSON | Rate limits, keys, only what the provider exposes |
| Existing (secondary) data | Data someone else collected | Fast and cheap | May not fit your question; unknown quality |

**Primary data** is collected by you for your question; **secondary data** was collected by someone else for another purpose.

**Qualitative vs quantitative research.** Quantitative research measures (how many, how much, how often) and supports statistics. Qualitative research explores meaning (why, how) through words, themes and observations. Interviews and open-ended survey questions are qualitative; closed questions, rating scales and transaction logs are quantitative.

**Representative sampling.** A sample is representative when it mirrors the population on the traits that matter.

| Sampling method | How it works | Note |
|---|---|---|
| Simple random | Every member has an equal chance | Baseline for unbiased samples |
| Stratified | Split the population into groups (strata), sample from each in proportion | Guarantees small groups are included |
| Systematic | Every k-th member from a list | Watch for periodic patterns in the list |
| Cluster | Randomly pick whole groups (schools, stores) | Cheaper; less precise |
| Convenience | Whoever is easy to reach | Fast but usually biased |

Common biases: **selection bias** (the way people enter the sample skews it), **non-response bias** (people who answer differ from those who don't), **survivorship bias** (only the "survivors" are visible), **leading questions** (wording pushes an answer).

**Survey design.** Use clear, neutral, single-topic questions. Avoid double-barreled questions ("Is the app fast and easy to use?") and leading ones ("How much do you love…"). Offer balanced scales (Likert, 1 to 5). Define the target audience and sampling frame first, and pilot the survey on a small group. **Structured interviews** ask every person the same questions in the same order, so answers are comparable; semi-structured interviews keep a core list but allow follow-ups.

**Legal and ethical considerations.** Get informed consent; collect only what you need (data minimization); use data only for the stated purpose; store it securely; respect laws such as the GDPR (EU) and CCPA (California) and sector rules such as HIPAA for health data; respect website terms of service and copyright when scraping.

**PII and anonymization.** Personally identifiable information identifies a person directly (name, email, national ID, phone) or indirectly when combined (postcode + birth date + gender are *quasi-identifiers*).

| Technique | Example | Reversible? |
|---|---|---|
| Suppression (removal) | Drop the `email` column | No |
| Masking | `****-****-****-1234` | No |
| Generalization | Age 37 → "35–44"; full postcode → district | No |
| Aggregation | Report counts per region, not per person | No |
| Pseudonymization | Replace names with consistent tokens or keyed hashes | Yes, with the key: still personal data under the GDPR |

**Anonymization** is irreversible: nobody can re-identify the person, even by combining fields. Pseudonymized data is not anonymous.

**Where collection choices matter.** Market research (surveys, focus groups, social media), risk assessment (historical transactions, claims), policy-making (census and national surveys, which rely on representative samples), and business strategy (combining sales data with customer interviews to explain *why* numbers move).

### Exam traps

> **Trap.** Pseudonymization is not anonymization. If a lookup table or key can reverse it, the data is still personal data.

> **Trap.** A large sample is not the same as a representative one. 50,000 responses from an opt-in web poll can be more biased than 1,000 random ones.

> **Trap.** Interviews answer *why*; surveys answer *how many*. Match the method to the question in the scenario.

## 1.1.2 Aggregate data from diverse sources

**Syllabus asks:** combine data from databases, APIs and file-based storage into one dataset; deal with differences in format; keep the result consistent and accurate.

### Core facts

Aggregation has three steps: **extract** from each source, **standardize** so the pieces match, then **integrate** and check.

| Mismatch | Example | Fix |
|---|---|---|
| Column names | `cust_id` vs `CustomerID` | `rename()` to one convention |
| Key types | `"00042"` (string) vs `42` (int) | Cast both sides to the same type before merging |
| Units and currency | kg vs lb; EUR vs USD | Convert to one unit; keep the unit in the column name |
| Dates and time zones | `03/04/2025` vs `2025-04-03`; local vs UTC | `pd.to_datetime(..., format=...)`; convert to UTC |
| Granularity | Daily sales vs monthly targets | Aggregate the finer source up (`resample`, `groupby`) |
| Encoding | UTF-8 vs Latin-1 | Pass `encoding=` when reading |
| Duplicates and conflicts | Same customer in CRM and web shop with different emails | De-duplicate; decide which source wins |

```python
import pandas as pd

crm = pd.DataFrame({"CustomerID": ["001", "002"], "Country": ["DE", "FR"]})
web = pd.DataFrame({"cust_id": [1, 2, 3], "spend_eur": [120.0, 80.5, 42.0]})

crm = crm.rename(columns={"CustomerID": "cust_id"})
crm["cust_id"] = crm["cust_id"].astype(int)          # align key types first

combined = web.merge(crm, on="cust_id", how="left", validate="one_to_one", indicator=True)
print(combined)
```

```text
   cust_id  spend_eur Country     _merge
0        1      120.0      DE       both
1        2       80.5      FR       both
2        3       42.0     NaN  left_only
```

- `pd.concat([a, b])` **stacks** datasets with the same columns (rows from several monthly files).
- `merge()` **joins** datasets side by side on a key (orders + customers).
- `validate="one_to_one"` (or `"one_to_many"`, `"many_to_one"`) raises an error if the keys are not what you expect. `indicator=True` adds a `_merge` column that shows unmatched rows.
- After integrating, check row counts, key uniqueness and new nulls. A merge on a key with duplicates silently multiplies rows.

Stacking, joining, and what `validate` and duplicate keys do:

```python
import pandas as pd

jan = pd.DataFrame({"order": [1, 2], "amount": [50, 20]})
feb = pd.DataFrame({"order": [3], "amount": [35]})
print(pd.concat([jan, feb], ignore_index=True))       # stack: same columns, more rows

customers = pd.DataFrame({"cust": ["a", "b"], "city": ["Oslo", "Rome"]})
orders = pd.DataFrame({"cust": ["a", "a", "b"], "amount": [10, 20, 30]})
print(orders.merge(customers, on="cust", validate="many_to_one"))   # join: match on a key

dupes = pd.DataFrame({"cust": ["a", "a"], "city": ["Oslo", "Bergen"]})
try:
    orders.merge(dupes, on="cust", validate="many_to_one")
except pd.errors.MergeError as e:
    print("MergeError:", e)
print(len(orders), "->", len(orders.merge(dupes, on="cust")))   # 2 orders x 2 rows for "a", plus 0 for "b"
```

```text
   order  amount
0      1      50
1      2      20
2      3      35
  cust  amount  city
0    a      10  Oslo
1    a      20  Oslo
2    b      30  Rome
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
3 -> 4
```

The second merge fails fast because customer `a` appears twice on the right. Without `validate`, the merge runs and quietly turns 3 orders into 4 rows: each of `a`'s two orders matches both of `a`'s rows, and `b` has no match at all.

**ETL vs ELT.** ETL transforms data before loading it into the target (typical for warehouses); ELT loads raw data first and transforms inside the target (typical for lakes and modern cloud warehouses).

### Exam traps

> **Trap.** Merging a string key with an integer key finds no matches (pandas raises an error for some type pairs). Align dtypes first.

> **Trap.** `concat` for same-shaped pieces, `merge` for matching on keys. Stacking two tables that should be joined leaves NaNs everywhere.

## 1.1.3 Explain data storage solutions

**Syllabus asks:** data warehouses, data lakes and file-based storage (CSV, Excel); cloud storage and its role in modern data management.

### Core facts

| | Data warehouse | Data lake | Files (CSV / Excel) |
|---|---|---|---|
| Holds | Cleaned, structured, integrated data | Raw data of any kind: tables, JSON, logs, images, audio | One table (CSV) or a workbook of sheets (Excel) |
| Schema | **Schema-on-write**: defined before loading | **Schema-on-read**: applied when the data is used | CSV has none; Excel has cell formats only |
| Users | Business analysts, BI dashboards (SQL) | Data scientists, ML engineers, big-data jobs | Individuals, small teams |
| Strength | Fast, consistent reporting across the business | Cheap, flexible, keeps everything | Simple, portable, universal |
| Risk | Rigid; costly to change | Becomes a "data swamp" without governance | No types, no concurrency control, size limits |

- A **data mart** is a subject-focused slice of a warehouse (for example, only sales).
- A **lakehouse** combines lake storage with warehouse-style tables and SQL.
- **OLTP** databases run day-to-day transactions (many small writes); **OLAP** systems such as warehouses serve analytical queries (large reads and aggregations).
- **CSV** stores plain text: no data types, no formulas, one table, and any delimiter or encoding. **Excel** (`.xlsx`) stores several sheets, formulas and formatting, with a limit of 1,048,576 rows per sheet.
- **Cloud storage** (object stores such as Amazon S3, Azure Blob Storage, Google Cloud Storage) offers elastic capacity, pay-as-you-go pricing, high durability, access control and easy sharing. Warehouses and lakes in the cloud separate storage from compute, so each scales independently.

### Exam traps

> **Trap.** Raw, unprocessed, mixed-format data → data lake. Cleaned, modeled data for dashboards → warehouse. The scenario's word "raw" or "unstructured" usually decides it.

> **Trap.** Saving a workbook as CSV keeps only the values of the active sheet. Formulas, formatting and other sheets are lost.

## 1.2.1 Distinguish structured and unstructured data

**Syllabus asks:** the characteristics of structured data (databases, spreadsheets) and unstructured data (text, images, video), and how each affects storage, retrieval and analysis.

### Core facts

| | Structured | Semi-structured | Unstructured |
|---|---|---|---|
| Shape | Fixed schema of rows and typed columns | Self-describing keys or tags, flexible schema | No predefined model |
| Examples | SQL tables, spreadsheets, CSV | JSON, XML, log files, emails' headers | Free text, PDFs, images, audio, video, social media posts |
| Storage | Relational databases, warehouses | Document databases, lakes | Object storage, data lakes |
| Retrieval | SQL queries, filters, joins | Key paths, JSON queries | Search indexes, metadata, specialized tools |
| Analysis | Statistics, aggregation, BI | Flatten first (`json_normalize`), then as structured | NLP, computer vision, audio processing; features must be extracted first |

Most organizations hold far more unstructured than structured data, but structured data is what most analysis runs on. Turning unstructured data into structured features (word counts, sentiment scores, image labels, transcripts) is a preprocessing step with its own cost and error.

### Exam traps

> **Trap.** JSON and XML are **semi-structured**, not unstructured: they carry keys or tags but no fixed table schema.

> **Trap.** A CSV of customer reviews has a structured *container* but the review text inside it is unstructured. Analysis of that column still needs text processing.

## 1.2.2 Identify and rectify erroneous data

**Syllabus asks:** diagnose errors and inconsistencies; handle missing, inaccurate and misleading values, duplicates and invalid entries; the MCAR / MAR / MNAR types of missingness; imputation; the effect of correcting or removing data on integrity; outlier detection; how numeric and categorical data change the approach.

### Core facts

**Kinds of error.** Missing values (`NaN`, `None`, empty strings, sentinels such as `-999` or `"N/A"`), inaccurate values (typos, wrong units), misleading values (defaults that look real, such as a birth date of 1900-01-01), inconsistent categories (`"NY"`, `"New York"`, `"new york "`), duplicates, invalid entries (age −3, 30 February), and outliers.

**Diagnosis in pandas.**

```python
df.info()                    # dtypes and non-null counts
df.isna().sum()              # missing values per column
df.describe()                # min/max reveal impossible values
df["city"].value_counts()    # inconsistent spellings of categories
df.duplicated().sum()        # exact duplicate rows
```

**Missingness types.**

| Type | Missingness depends on | Example | What works |
|---|---|---|---|
| **MCAR** (missing completely at random) | Nothing: not other variables, not the value itself | A lab tube is dropped; a sensor fails at random | Deleting rows is unbiased (only loses power); simple imputation is OK |
| **MAR** (missing at random) | Other *observed* variables | Younger respondents skip the income question more often, and age is recorded | Impute using the related variables (group means, regression, multiple imputation) |
| **MNAR** (missing not at random) | The *missing value itself* | High earners skip the income question *because* their income is high | Hardest: deletion and simple imputation are biased; needs domain knowledge, modeling or more data collection |

**Imputation.** Mean (numeric, no strong outliers), median (numeric, skewed or with outliers), mode (categorical), a constant or "Unknown" category, forward/backward fill (ordered time series), interpolation, group-wise statistics, or model-based methods (k-nearest neighbours, regression). Adding a "was missing" flag column preserves the fact that a value was imputed.

```python
df["income"] = df["income"].fillna(df["income"].median())
df["segment"] = df["segment"].fillna(df["segment"].mode()[0])
df["age"] = df["age"].fillna(df.groupby("region")["age"].transform("mean"))
```

**Correction or removal changes the data.** Dropping rows shrinks the sample and can bias it if the dropped rows differ. Mean imputation keeps the mean but shrinks the variance and weakens correlations. Record every change so results can be reproduced.

**Outliers.** Detect with a box plot, the **IQR rule** (below Q1 − 1.5·IQR or above Q3 + 1.5·IQR) or **z-scores** (|z| > 3). Then decide: a data-entry error (fix or remove) or a genuine extreme value (keep, cap, or transform, for example with a log). Never delete outliers only because they are inconvenient.

**Numeric vs categorical.** Numeric columns: ranges, summary statistics, IQR and z-scores. Categorical columns: `value_counts()`, allowed-value lists, case and whitespace differences, rare categories and typos. Statistics such as z-scores make no sense for categories.

### Exam traps

> **Trap.** MAR depends on *other observed* variables; MNAR depends on the *missing value itself*. "People with high incomes don't report income" is MNAR.

> **Trap.** Mean imputation is a poor choice when a column has strong outliers or skew; the median is robust.

> **Trap.** `df.isna()` does not catch sentinel values such as `-999` or the string `"N/A"`. Convert them to `NaN` first (for example `na_values=` in `read_csv`).

## 1.2.3 Understand normalization, scaling and encoding

**Syllabus asks:** min-max scaling and z-score normalization; one-hot and label encoding; the trade-off between data reduction and explainability; outlier treatment; standard date-time and number formats.

### Core facts

| Method | Formula | Result | Outliers |
|---|---|---|---|
| **Min-max scaling** | (x − min) / (max − min) | Values in [0, 1] | Very sensitive: one extreme value squeezes the rest together |
| **Z-score standardization** | (x − mean) / std | Mean 0, standard deviation 1, unbounded | Less sensitive, but mean and std are still pulled |
| Robust scaling | (x − median) / IQR | Centered on the median | Resistant |

```python
import pandas as pd

s = pd.Series([10, 20, 30, 40, 50])
print(((s - s.min()) / (s.max() - s.min())).tolist())
print(((s - s.mean()) / s.std(ddof=0)).round(2).tolist())
```

```text
[0.0, 0.25, 0.5, 0.75, 1.0]
[-1.41, -0.71, 0.0, 0.71, 1.41]
```

- Scaling matters for distance- and gradient-based methods (k-nearest neighbours, k-means, regularized regression). Tree-based models do not need it.
- Fit the scaler on the **training** data only, then apply the same parameters to the test data. Fitting on all data leaks information from the test set.
- scikit-learn's `MinMaxScaler` and `StandardScaler` do this; `StandardScaler` uses the population standard deviation (`ddof=0`).

Fit on the training data, then reuse the same parameters on the test data:

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler

train = np.array([[10], [20], [30]])
test = np.array([[25], [40]])

scaler = MinMaxScaler().fit(train)        # learns min = 10, max = 30 from training data only
print(scaler.transform(train).ravel())
print(scaler.transform(test).ravel())     # same parameters; 40 is past the training max
```

```text
[0.  0.5 1. ]
[0.75 1.5 ]
```

The test value 40 scales to 1.5 because the scaler only knows the training range (10 to 30). That is expected: the test set must not influence the parameters.

**Encoding categories.**

| Encoding | What it produces | Use for |
|---|---|---|
| **One-hot** | One 0/1 column per category (`pd.get_dummies`, `OneHotEncoder`) | Nominal categories with no order (colour, city) |
| **Label encoding** | One integer per category (0, 1, 2…) | Target labels, tree models, or ordinal categories when the integers follow the real order |
| Ordinal mapping | Explicit order, e.g. `{"low": 0, "medium": 1, "high": 2}` | Ordered categories |

Label-encoding a nominal feature invents an order ("red" = 0 < "green" = 1 < "blue" = 2) that linear and distance-based models will treat as real. One-hot encoding avoids this but adds a column per category, which is a problem for high-cardinality columns such as ZIP codes.

**Data reduction trade-off.** Dropping features, aggregating, or compressing with PCA makes data smaller, faster and less noisy, but loses information, and derived components are harder to explain to stakeholders. Selecting a subset of original features keeps explainability; PCA components do not map to one business variable.

**Standard formats.** Dates in ISO 8601 (`2025-07-15`, `2025-07-15T14:30:00Z`) in one time zone (usually UTC); numbers with one decimal separator, no thousands separators or currency symbols in the stored value, and one unit per column.

### Exam traps

> **Trap.** "Normalization" is used loosely. In this syllabus, min-max scaling gives [0, 1]; z-score normalization (standardization) gives mean 0 and standard deviation 1.

> **Trap.** Z-scores are not bounded to [−1, 1] or [0, 1]; a value three standard deviations above the mean has z = 3.

## 1.2.4 Apply data cleaning and standardization techniques

**Syllabus asks:** imputation, string manipulation, format standardization, boolean and case normalization, string-to-number conversion, imputation vs exclusion, one-hot encoding for machine learning, and bucketization.

### Core facts

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["  Ana ", "BEN", "cara"],
    "active": ["Yes", "n", "TRUE"],
    "price": ["$1,200", "85", "n/a"],
    "age": [23, 41, 67],
})

df["name"] = df["name"].str.strip().str.title()                 # 'Ana', 'Ben', 'Cara'
df["active"] = df["active"].str.lower().map({"yes": True, "y": True, "true": True,
                                              "no": False, "n": False, "false": False})
df["price"] = pd.to_numeric(df["price"].str.replace(r"[$,]", "", regex=True), errors="coerce")
df["age_band"] = pd.cut(df["age"], bins=[0, 30, 60, 120], labels=["young", "middle", "senior"])
print(df)
```

```text
   name  active   price  age age_band
0   Ana    True  1200.0   23    young
1   Ben   False    85.0   41   middle
2  Cara    True     NaN   67   senior
```

- **String cleanup**: `.str.strip()`, `.str.lower()` / `.str.upper()` / `.str.title()`, `.str.replace()`; normalize case *before* comparing or grouping.
- **Boolean normalization**: map every spelling (`"Y"`, `"yes"`, `"1"`, `"True"`) to real `True`/`False`.
- **String to number**: `pd.to_numeric(s, errors="coerce")` turns unparseable values into `NaN`; `s.astype(float)` raises a `ValueError` instead. Remove currency symbols and thousands separators first.

`to_numeric` versus `astype` on the same messy column:

```python
import pandas as pd

prices = pd.Series(["12.5", "7", "n/a"])
print(pd.to_numeric(prices, errors="coerce").tolist())
try:
    prices.astype(float)
except ValueError as e:
    print("ValueError:", e)
```

```text
[12.5, 7.0, nan]
ValueError: could not convert string to float: 'n/a'
```

- **Imputation vs exclusion**: impute when rows are valuable and missingness is limited and explainable; exclude when a value cannot be estimated sensibly, the column is mostly empty, or the target itself is missing.
- **One-hot encoding**: `pd.get_dummies(df, columns=["color"])` replaces the column with `color_blue`, `color_red`… (boolean in pandas 2 and later; pass `dtype=int` for 0/1). `drop_first=True` drops one column to avoid perfectly redundant columns in linear models.

One column per category, and what `drop_first` removes:

```python
import pandas as pd

df = pd.DataFrame({"color": ["red", "blue", "red"], "qty": [1, 2, 3]})
print(pd.get_dummies(df, columns=["color"], dtype=int))
print(pd.get_dummies(df, columns=["color"], dtype=int, drop_first=True).columns.tolist())
```

```text
   qty  color_blue  color_red
0    1           0          1
1    2           1          0
2    3           0          1
['qty', 'color_red']
```

With `drop_first=True` only `color_red` is left: a 0 there already means blue.

- **Bucketization** turns a continuous variable into categories. `pd.cut` uses bin **edges** you choose (intervals are right-closed by default, so `(30, 60]` includes 60); `pd.qcut` uses **quantiles**, giving roughly equal counts per bin.

`cut` with your own edges versus `qcut` with equal-sized groups:

```python
import pandas as pd

ages = pd.Series([5, 18, 30, 31, 45, 70])
print(pd.cut(ages, bins=[0, 30, 60, 120]).astype(str).tolist())     # your edges
print(pd.qcut(ages, q=3, labels=["low", "mid", "high"]).tolist())   # equal-sized groups
```

```text
['(0, 30]', '(0, 30]', '(0, 30]', '(30, 60]', '(30, 60]', '(60, 120]']
['low', 'low', 'mid', 'mid', 'high', 'high']
```

30 lands in `(0, 30]` because intervals include their right edge. `qcut` puts two of the six values in each group, whatever their spacing.

### Exam traps

> **Trap.** `pd.cut(ages, bins=[0, 30, 60])` puts 30 in the first bin `(0, 30]`, and a value of 0 or anything above 60 becomes `NaN`.

> **Trap.** `astype(int)` on a column with `NaN` raises an error; fill or drop missing values first, or use the nullable `"Int64"` dtype.

## 1.3.1 Execute basic data validation methods

**Syllabus asks:** type, range and cross-field validation; implementing them with Python logic and schema checks; type, range and cross-reference checks; why early type checks in ingestion scripts help.

### Core facts

| Check | Question it answers | Example |
|---|---|---|
| **Type** | Is the value the right kind? | `quantity` is an integer, `signup` parses as a date |
| **Range** | Is it within allowed limits? | `0 <= age <= 120`, `discount` between 0 and 1 |
| **Format** | Does it match a pattern? | Email, postcode, ISO date (regular expressions) |
| **Presence** | Is a required value there? | `order_id` is never empty |
| **Uniqueness** | Are keys unique? | `df["order_id"].is_unique` |
| **Allowed values** | Is it one of a fixed set? | `status in {"new", "paid", "shipped"}` |
| **Cross-field** | Do fields in the same record agree? | `end_date >= start_date`; `total == price * qty` |
| **Cross-reference** | Does the value exist in another dataset? | Every `customer_id` in orders exists in the customers table |

```python
import pandas as pd

orders = pd.DataFrame({"qty": [2, -1, 5], "start": pd.to_datetime(["2025-01-02"] * 3),
                       "end": pd.to_datetime(["2025-01-05", "2025-01-04", "2025-01-01"])})

problems = {
    "qty out of range": ~orders["qty"].between(1, 1000),
    "end before start": orders["end"] < orders["start"],
}
for name, mask in problems.items():
    print(name, orders.index[mask].tolist())
```

```text
qty out of range [1]
end before start [2]
```

In plain Python, validate with `isinstance()`, comparisons and `raise ValueError(...)`. Schema tools (pandera, pydantic, Great Expectations) declare the expected columns, types and rules once and check every batch.

**Validate early.** A type check at the start of an ingestion script catches a bad file before its errors spread into joins, aggregations and reports, where they are much harder to trace (fail fast).

### Exam traps

> **Trap.** Cross-field checks compare fields **within one record**; cross-reference checks look a value up **in another table or list**.

> **Trap.** A value can pass a type check and still be invalid: an integer age of 250 has the right type but fails the range check.

## 1.3.2 Establish and maintain data integrity

**Syllabus asks:** what data integrity is, why reliable databases need it, and how clear validation rules keep data correct and consistent.

### Core facts

**Data integrity** is the accuracy, completeness, consistency and reliability of data over its whole life cycle: data changes only through authorized, valid operations. Validation is a check at a moment; integrity is the property you maintain over time.

| Integrity type | Rule | Database mechanism |
|---|---|---|
| Entity | Every row is uniquely identifiable | `PRIMARY KEY` (unique, not null) |
| Referential | A reference points to something that exists | `FOREIGN KEY` |
| Domain | Values are of the right type and in the allowed set or range | Column types, `NOT NULL`, `CHECK`, `DEFAULT` |
| User-defined | Business rules hold | `CHECK` constraints, triggers, application logic |

```sql
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    qty         INTEGER CHECK (qty > 0),
    status      TEXT DEFAULT 'new'
);
```

**Transactions** keep multi-step changes all-or-nothing (the **ACID** properties: atomicity, consistency, isolation, durability). In Python's `sqlite3`, changes become permanent on `commit()` and can be undone with `rollback()`.

Clear validation rules are specific ("`qty` is an integer from 1 to 1,000"), documented, enforced at the point of entry, and tested. Supporting practices: access control, audit logs, backups, and checksums for files.

### Exam traps

> **Trap.** SQLite does not enforce foreign keys unless you run `PRAGMA foreign_keys = ON` on the connection.

> **Trap.** Integrity is not the same as security: security controls *who* can change data; integrity is about the data staying *correct*.

## 1.4.1 Understand file formats in data acquisition

**Syllabus asks:** CSV for tabular data, JSON for structured data, XML for hierarchical data, TXT for unstructured text, and how to import and export each.

### Core facts

| Format | Shape | Read | Write |
|---|---|---|---|
| CSV | Rows and columns of text, one delimiter | `csv.reader` / `csv.DictReader`, `pd.read_csv` | `csv.writer`, `df.to_csv(index=False)` |
| JSON | Nested objects `{}` and arrays `[]` | `json.load(f)` / `json.loads(s)`, `pd.read_json`, `pd.json_normalize` | `json.dump(obj, f)` / `json.dumps(obj)`, `df.to_json` |
| XML | Tree of elements with attributes | `xml.etree.ElementTree`, `pd.read_xml` | `ElementTree.write`, `df.to_xml` |
| TXT | Free text, line by line | `open(...).read()` / `readlines()` / iterate | `f.write()` |

```python
import json

raw = '{"id": 7, "tags": ["a", "b"], "active": true, "score": null}'
record = json.loads(raw)
print(type(record).__name__, record["tags"], record["active"], record["score"])
print(json.dumps({"ok": True, "items": (1, 2)}))
```

```text
dict ['a', 'b'] True None
{"ok": true, "items": [1, 2]}
```

JSON → Python: object → `dict`, array → `list`, `true`/`false` → `True`/`False`, `null` → `None`. Python tuples become JSON arrays. `load`/`dump` work with files; `loads`/`dumps` work with **s**trings.

```python
import xml.etree.ElementTree as ET

xml = "<books><book id='1'><title>Data</title></book><book id='2'><title>SQL</title></book></books>"
root = ET.fromstring(xml)
print([(b.get("id"), b.find("title").text) for b in root.findall("book")])
```

```text
[('1', 'Data'), ('2', 'SQL')]
```

CSV details: a header row names the columns; a field containing the delimiter is quoted (`"Smith, Jane"`); every value is text until you convert it; `sep=";"` or `sep="\t"` for other delimiters; open files for the `csv` module with `newline=""`. Always state `encoding="utf-8"` when text might contain non-ASCII characters.

### Exam traps

> **Trap.** `json.load` takes a file object; `json.loads` takes a string. Passing a filename string to `json.load` fails.

> **Trap.** `df.to_csv("out.csv")` writes the index as an extra first column unless you pass `index=False`.

## 1.4.2 Access, manage and utilize datasets

**Syllabus asks:** access datasets from local files, databases and online repositories; organize, sort and filter data.

### Core facts

```python
import pandas as pd
import sqlite3

local = pd.read_csv("data/sales.csv")                                   # local file (relative path)
remote = pd.read_csv("https://example.org/open-data/air_quality.csv")   # online repository, straight from a URL
with sqlite3.connect("shop.db") as con:
    orders = pd.read_sql_query("SELECT * FROM orders WHERE total > 100", con)
```

Online repositories include government open-data portals, the UCI Machine Learning Repository, Kaggle and GitHub (use the "raw" file URL). Check the licence and the documentation (a data dictionary) before using a dataset.

**First look.** `df.shape`, `df.head()`, `df.info()`, `df.describe()`, `df.columns`.

**Organize.** Keep data *tidy*: each variable a column, each observation a row, each kind of observation its own table. Keep the raw file unchanged and write cleaned versions separately. Use consistent, lowercase column names.

**Sort and filter.**

```python
df.sort_values("total", ascending=False)                  # largest first
df.sort_values(["region", "total"], ascending=[True, False])
df[df["total"] > 100]                                     # boolean mask
df[(df["region"] == "EU") & (df["total"] > 100)]          # & and |, each condition in brackets
df.query("region == 'EU' and total > 100")                 # same filter as a string
df[df["region"].isin(["EU", "UK"])]
```

### Exam traps

> **Trap.** Combine pandas conditions with `&`, `|` and `~`, not `and`/`or`/`not`, and put each condition in parentheses.

> **Trap.** `sort_values` returns a new DataFrame; the original is unchanged unless you assign it back.

## 1.4.3 Extract data from various sources

**Syllabus asks:** extract data from databases, APIs and online services; parse HTML with requests and BeautifulSoup; keep data compatible and intact; scrape ethically (robots.txt, rate limits).

### Core facts

**APIs with requests.**

```python
import requests

resp = requests.get("https://api.example.com/v1/orders",
                    params={"status": "paid", "page": 1},
                    headers={"Authorization": "Bearer <token>"},
                    timeout=10)
resp.raise_for_status()          # raises HTTPError for 4xx / 5xx
data = resp.json()               # parsed JSON → dict / list
```

Status codes to know: **200** OK, **201** created, **400** bad request, **401** unauthorized (no or bad credentials), **403** forbidden, **404** not found, **429** too many requests (rate limit), **500** server error. `resp.text` is the body as a string; `resp.json()` parses it. APIs often **paginate**: loop over pages until one comes back empty or there is no "next" link.

**HTML with BeautifulSoup.**

```python
from bs4 import BeautifulSoup

html = """<table id="prices">
  <tr><td class="item">Tea</td><td class="price">2.50</td></tr>
  <tr><td class="item">Coffee</td><td class="price">3.10</td></tr>
</table>"""
soup = BeautifulSoup(html, "html.parser")
rows = soup.find("table", id="prices").find_all("tr")
print([(r.find("td", class_="item").get_text(), float(r.find("td", class_="price").get_text())) for r in rows])
```

```text
[('Tea', 2.5), ('Coffee', 3.1)]
```

- `find()` returns the first match (or `None`); `find_all()` returns a list.
- Use `class_=` (with the underscore) because `class` is a Python keyword.
- `.get_text(strip=True)` returns the text; `tag["href"]` or `tag.get("href")` returns an attribute.
- `soup.select("table#prices td.price")` uses CSS selectors.
- `pd.read_html(url_or_html)` returns a **list** of DataFrames, one per `<table>`.

Text, attributes and CSS selectors on a small page:

```python
from bs4 import BeautifulSoup

html = """<ul id="links">
  <li><a class="doc" href="/guide.pdf">  Guide  </a></li>
  <li><a class="doc" href="/faq.html">FAQ</a></li>
</ul>"""
soup = BeautifulSoup(html, "html.parser")

first = soup.find("a", class_="doc")
print(repr(first.get_text()), repr(first.get_text(strip=True)))
print(first["href"], first.get("title"))                 # .get returns None if missing
print([a["href"] for a in soup.find_all("a")])
print([a.get_text(strip=True) for a in soup.select("ul#links a.doc")])
print(soup.find("table"))                                # no match -> None
```

```text
'  Guide  ' 'Guide'
/guide.pdf None
['/guide.pdf', '/faq.html']
['Guide', 'FAQ']
None
```

`get_text()` keeps the surrounding spaces; `strip=True` removes them. `tag.get("title")` returns `None` for a missing attribute, where `tag["title"]` would raise `KeyError`.

**Ethical scraping.** Prefer an official API. Read the site's terms of service. Check `robots.txt` at the site root (`https://site.com/robots.txt`), which lists paths crawlers should not visit (`Disallow:`); `urllib.robotparser` can check it. Rate-limit your requests (for example `time.sleep()` between them), identify yourself with a User-Agent, cache what you have fetched, and don't collect personal data without a lawful basis.

Checking paths against `robots.txt` rules with the standard library. Normally you call `set_url("https://site.com/robots.txt")` and `read()`; here the rules are passed in directly:

```python
from urllib.robotparser import RobotFileParser

rules = RobotFileParser()
rules.parse(["User-agent: *", "Disallow: /private/"])
print(rules.can_fetch("my-bot", "https://site.com/products"))
print(rules.can_fetch("my-bot", "https://site.com/private/data"))
```

```text
True
False
```

After extraction, check compatibility and integrity: consistent encodings and types, expected row counts, and no duplicated pages.

### Exam traps

> **Trap.** `robots.txt` is a convention, not an access control. It does not stop a scraper, and respecting it does not make scraping automatically legal.

> **Trap.** `requests.get()` does not raise an error for a 404 or 500 on its own; call `raise_for_status()` or check `status_code`.

## 1.4.4 Apply spreadsheet best practices

**Syllabus asks:** spreadsheet layout and formatting best practices, and basic formulas that keep sheets readable.

### Core facts

**Layout.** One table per sheet starting at A1; a single header row; one variable per column and one record per row; no merged cells, no blank rows or columns inside the data; units in the header (`Weight (kg)`); descriptive sheet names; separate sheets for raw data, calculations and summaries; freeze the header row.

**Formatting.** Consistent date and number formats; right-align numbers; use conditional formatting to highlight, not to store meaning (colour alone is lost on export and invisible to formulas); keep decoration minimal. Formatting changes how a value looks, not the value itself: a cell showing `3.1` may hold `3.14159`.

**Formulas.**

| Formula | Does |
|---|---|
| `=SUM(B2:B100)`, `=AVERAGE(...)`, `=MIN`, `=MAX` | Basic aggregates |
| `=COUNT(...)` / `=COUNTA(...)` | Count numbers / count non-empty cells |
| `=COUNTIF(C:C, "EU")`, `=SUMIF(C:C, "EU", B:B)` | Conditional count / sum |
| `=IF(B2>100, "High", "Low")` | Conditional value |
| `=XLOOKUP(...)` / `=VLOOKUP(...)` | Look up a value in another table |

A **relative** reference (`B2`) shifts when copied; an **absolute** reference (`$B$2`) stays fixed. Put constants such as a tax rate in their own labeled cell and reference it absolutely instead of typing the number into many formulas. Data validation (drop-down lists) stops bad entries at input.

In pandas: `pd.read_excel("file.xlsx", sheet_name="Sales")` and `df.to_excel("out.xlsx", index=False)`.

### Exam traps

> **Trap.** Merged cells and multi-row headers look tidy to people but break sorting, filtering and `read_excel`.

## 1.4.5 Prepare, adapt and pre-process data for analysis

**Syllabus asks:** let the context, objectives and stakeholders guide preparation; sort, filter and prepare the dataset; keep date-time formats and structures aligned; convert between wide and long formats; split training and testing sets; understand how outlier handling affects preprocessing.

### Core facts

**Start from the question.** Clarify the objective and the decision it supports, who the stakeholders are, and what granularity and time frame they need. That decides which columns to keep, how to filter, and what counts as an outlier.

**Dates.** Parse once, in one format and time zone, then use the `.dt` accessor.

```python
df["order_date"] = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
df["month"] = df["order_date"].dt.to_period("M")
df["weekday"] = df["order_date"].dt.day_name()
```

**Wide vs long.**

```python
import pandas as pd

wide = pd.DataFrame({"store": ["A", "B"], "Jan": [10, 7], "Feb": [12, 9]})
long = wide.melt(id_vars="store", var_name="month", value_name="sales")
print(long)
print(long.pivot(index="store", columns="month", values="sales"))
```

```text
  store month  sales
0     A   Jan     10
1     B   Jan      7
2     A   Feb     12
3     B   Feb      9
month  Feb  Jan
store
A       12   10
B        9    7
```

Wide: one row per subject, repeated measurements in separate columns (easy to read). Long (tidy): one row per subject-measurement pair (easy to group, filter and plot; Seaborn expects it). `melt` goes wide → long; `pivot` goes long → wide.

**Train/test split.**

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

`random_state` makes the split reproducible; `stratify=y` keeps class proportions equal in both parts. Split **before** fitting scalers, imputers or encoders, and fit them on the training part only. For time series, split by time (train on the past, test on the future) instead of shuffling.

**Outliers and preprocessing.** Outliers pull the mean and standard deviation, compress min-max scaling, and can dominate a regression line. Decide how to treat them before scaling and modeling, and apply the rule learned on training data to test data too.

### Exam traps

> **Trap.** `pivot` fails when an index/column pair appears more than once; use `pivot_table` with an aggregation function instead.

> **Trap.** Fitting a scaler or imputer on the full dataset before splitting leaks test information into training (data leakage) and makes evaluation look better than it is.
