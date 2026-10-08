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

**Stacking with `concat`.** Use `pd.concat` when several tables have the **same columns** and you want one longer table, for example one file per month. The rows of the second table go underneath the first:

```python
import pandas as pd

jan = pd.DataFrame({"order": [1, 2], "amount": [50, 20]})
feb = pd.DataFrame({"order": [3], "amount": [35]})

print(pd.concat([jan, feb]))
```

```text
   order  amount
0      1      50
1      2      20
0      3      35
```

Each table keeps its own row labels, so January's 0 and 1 are followed by February's 0: the label 0 now appears twice. `ignore_index=True` throws the old labels away and numbers the rows again:

```python
import pandas as pd

jan = pd.DataFrame({"order": [1, 2], "amount": [50, 20]})
feb = pd.DataFrame({"order": [3], "amount": [35]})

print(pd.concat([jan, feb], ignore_index=True))
```

```text
   order  amount
0      1      50
1      2      20
2      3      35
```

**Joining with `merge`.** Use `merge` when two tables hold **different information about the same things**, and a shared column (the **key**) says which rows belong together. Here each order has a customer code, and a second table gives each customer's city:

```python
import pandas as pd

orders = pd.DataFrame({"cust": ["a", "a", "b"], "amount": [10, 20, 30]})
customers = pd.DataFrame({"cust": ["a", "b"], "city": ["Oslo", "Rome"]})

print(orders.merge(customers, on="cust"))
```

```text
  cust  amount  city
0    a      10  Oslo
1    a      20  Oslo
2    b      30  Rome
```

Each order picks up its customer's city. Customer `a` has two orders, so `Oslo` appears twice.

**Duplicate keys multiply rows.** If a key appears more than once on **both** sides, every matching pair becomes a row. Here customer `a` has 2 orders and, by mistake, 2 rows in the customer table:

```python
import pandas as pd

orders = pd.DataFrame({"cust": ["a", "a", "b"], "amount": [10, 20, 30]})
customers = pd.DataFrame({"cust": ["a", "a"], "city": ["Oslo", "Bergen"]})

merged = orders.merge(customers, on="cust")
print(merged)
print(len(orders), "orders became", len(merged), "rows")
```

```text
  cust  amount    city
0    a      10    Oslo
1    a      10  Bergen
2    a      20    Oslo
3    a      20  Bergen
3 orders became 4 rows
```

Each of `a`'s 2 orders matched both of `a`'s customer rows: 2 × 2 = 4 rows. `b` isn't in the customer table, so it dropped out: by default a merge keeps only rows that match (`how=` changes that). Nothing warned you that any of this happened.

**Catching it with `validate`.** Tell `merge` what shape you expect and it raises an error when the data disagrees. `"many_to_one"` means "many orders can share a customer, but each customer appears only once on the right":

```python
import pandas as pd

orders = pd.DataFrame({"cust": ["a", "a", "b"], "amount": [10, 20, 30]})
customers = pd.DataFrame({"cust": ["a", "a"], "city": ["Oslo", "Bergen"]})

try:
    orders.merge(customers, on="cust", validate="many_to_one")
except pd.errors.MergeError as e:
    print("MergeError:", str(e).splitlines()[0])   # the first line of the message
```

```text
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

The other options are `"one_to_one"` and `"one_to_many"`. `indicator=True`, used in the first example of this section, adds a `_merge` column saying whether each row matched (`both`) or came from one side only (`left_only`, `right_only`).

**Check after merging.** Compare the row count before and after, check that the key is unique where it should be, and look for new missing values.

**ETL vs ELT.** ETL transforms data before loading it into the target (typical for warehouses); ELT loads raw data first and transforms inside the target (typical for lakes and modern cloud warehouses).

### Exam traps

> **Trap.** pandas won't merge a text key with an integer key: `"001"` and `1` are different types, so it raises a ValueError instead of matching them. Convert both keys to the same type first, as the first example does with `astype(int)`.

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
print(((s - s.mean()) / s.std(ddof=0)).round(2).tolist())   # ddof=0: population std (see 3.1.1)
```

```text
[0.0, 0.25, 0.5, 0.75, 1.0]
[-1.41, -0.71, 0.0, 0.71, 1.41]
```

**When scaling matters.** Some methods compare rows by measuring the distance between them (k-nearest neighbours, k-means), or learn in small steps (regularized regression). If one column is in thousands and another in single digits, the big column swamps the small one. Scaling puts the columns on a similar range. Tree-based models (decision trees, random forests) look at one column at a time, so they don't need it.

**Fit on the training data only.** A scaler *learns* numbers from the data; min-max scaling learns the minimum and maximum. It must learn them from the **training** data only, then use those same numbers on the test data. If it learned from all the data, facts about the test set would leak into training and the test score would look better than it really is.

In scikit-learn, `fit` learns the numbers and `transform` applies them. scikit-learn expects a table with one row per value, which is why each number below sits in its own `[ ]`:

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler

train = np.array([[10], [20], [30]])
test = np.array([[25], [40]])

scaler = MinMaxScaler()
scaler.fit(train)                          # learns min = 10 and max = 30
print(scaler.transform(train).ravel())     # .ravel() flattens the result for printing
print(scaler.transform(test).ravel())
```

```text
[0.  0.5 1. ]
[0.75 1.5 ]
```

25 is three-quarters of the way from 10 to 30, so it becomes 0.75. 40 is past the training maximum, so it becomes 1.5. That is correct: the scaler is supposed to use the training range, not squeeze the test data into 0–1.

`StandardScaler` works the same way for z-scores. It uses the population standard deviation (`ddof=0`).

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

**Cleaning text.** Adding `.str` to a column lets you call a string method on every value at once.

```python
import pandas as pd

names = pd.Series(["  Ana ", "BEN", "cara"])
print(names.str.strip().tolist())                 # remove spaces at both ends
print(names.str.strip().str.lower().tolist())     # all lowercase
print(names.str.strip().str.title().tolist())     # capital first letter
```

```text
['Ana', 'BEN', 'cara']
['ana', 'ben', 'cara']
['Ana', 'Ben', 'Cara']
```

Make the case consistent before you compare or group. `"BEN"` and `"Ben"` are different strings, so they would be counted as two people.

**Yes/no written many ways.** People type yes/no as `"Y"`, `"yes"`, `"1"`, `"True"` and more. Turn every spelling into a real `True` or `False`:

```python
import pandas as pd

answers = pd.Series(["Yes", "n", "TRUE", "no"])
lookup = {"yes": True, "y": True, "true": True, "no": False, "n": False, "false": False}
print(answers.str.lower().map(lookup).tolist())
```

```text
[True, False, True, False]
```

Lowercasing first means the lookup only needs lowercase spellings. A spelling missing from the lookup becomes `NaN`, which shows you what you forgot.

**Text to numbers.** Numbers stored as text can't be added up. There are two ways to convert them, and they behave differently when a value isn't a number:

```python
import pandas as pd

prices = pd.Series(["12.5", "7", "n/a"])

print(pd.to_numeric(prices, errors="coerce").tolist())   # bad values become NaN

try:
    prices.astype(float)                                  # a bad value stops everything
except ValueError as e:
    print("ValueError:", e)
```

```text
[12.5, 7.0, nan]
ValueError: could not convert string to float: 'n/a'
```

Symbols such as `$` and `,` also count as "not a number", so remove them first: `prices.str.replace(r"[$,]", "", regex=True)`.

**Fill in or drop?** **Imputing** means filling a missing value with an estimate, such as the column's median or most common value. Impute when the row is worth keeping, only a few values are missing, and you can explain the estimate. **Exclude** (drop) the row or column when a value can't be estimated sensibly, the column is mostly empty, or the missing value is the very thing you want to predict.

**One-hot encoding.** Most models need numbers, not words. One-hot encoding replaces a text column with one 0/1 column per category:

```python
import pandas as pd

df = pd.DataFrame({"color": ["red", "blue", "red"], "qty": [1, 2, 3]})
print(pd.get_dummies(df, columns=["color"], dtype=int))
```

```text
   qty  color_blue  color_red
0    1           0          1
1    2           1          0
2    3           0          1
```

Row 0 is red, so it has a 1 under `color_red` and a 0 under `color_blue`. (`dtype=int` asks for 0 and 1; without it, recent pandas shows `True` and `False`.)

With two colours, one column is enough: if `color_red` is 0, the row must be blue. `drop_first=True` drops the first column for you. This matters for linear models, which get confused by columns that can be worked out from each other.

```python
import pandas as pd

df = pd.DataFrame({"color": ["red", "blue", "red"], "qty": [1, 2, 3]})
print(pd.get_dummies(df, columns=["color"], dtype=int, drop_first=True))
```

```text
   qty  color_red
0    1          1
1    2          0
2    3          1
```

**Putting numbers into groups.** `pd.cut` sorts numbers into ranges whose **edges you choose**:

```python
import pandas as pd

ages = pd.Series([5, 18, 30, 31, 45, 70])
bands = pd.cut(ages, bins=[0, 30, 60, 120], labels=["young", "middle", "senior"])
print(bands.tolist())
```

```text
['young', 'young', 'young', 'middle', 'middle', 'senior']
```

The edges 0, 30, 60 and 120 make three ranges. Each range includes its right edge but not its left (pandas writes the first one as `(0, 30]`). So 30 is "young" and 31 is "middle". A value outside all the ranges, such as 0 or 130, becomes `NaN`.

`pd.qcut` instead splits the values into groups of **equal size**, wherever the edges end up:

```python
import pandas as pd

ages = pd.Series([5, 18, 30, 31, 45, 70])
print(pd.qcut(ages, q=3, labels=["low", "mid", "high"]).tolist())
```

```text
['low', 'low', 'mid', 'mid', 'high', 'high']
```

Six values in three groups: two in each.

**Putting it together.** One small table with all of these problems at once: names with stray spaces and mixed case, yes/no written different ways, prices stored as text with symbols, and ages to put into bands.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["  Ana ", "BEN", "cara"],
    "active": ["Yes", "n", "TRUE"],
    "price": ["$1,200", "85", "n/a"],
    "age": [23, 41, 67],
})

df["name"] = df["name"].str.strip().str.title()
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

The names are trimmed and capitalised, `active` holds real booleans, `"$1,200"` became the number 1200.0 once `$` and `,` were removed, `"n/a"` became `NaN`, and each age has a band.

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

**Loading data into pandas.** Each data source has a `read_` function that returns a DataFrame. These three lines show the usual sources (they need real files and a network, so there's no output here):

```python
import pandas as pd
import sqlite3

local = pd.read_csv("data/sales.csv")                                   # a file on your computer
remote = pd.read_csv("https://example.org/open-data/air_quality.csv")   # a file online, read straight from its URL
with sqlite3.connect("shop.db") as con:
    orders = pd.read_sql_query("SELECT * FROM orders WHERE total > 100", con)   # a database query
```

- `"data/sales.csv"` is a **relative path**: it is looked up starting from the folder the program runs in.
- `read_csv` accepts a web address just like a file path.
- `read_sql_query` runs a SQL query and returns the result as a DataFrame (section 2.4.3).

Online repositories include government open-data portals, the UCI Machine Learning Repository, Kaggle and GitHub (use the "raw" file URL). Check the licence and the documentation (a data dictionary) before using a dataset.

**A first look.** Before doing anything with a new dataset, check its size, its columns and a few rows. The example below reads a small CSV from a string, which behaves exactly like reading a file:

```python
import io
import pandas as pd

csv_text = """region,product,total
EU,tea,120
US,jam,80
EU,jam,150
UK,tea,60
"""
df = pd.read_csv(io.StringIO(csv_text))     # io.StringIO makes a string behave like a file

print(df.shape)                  # (rows, columns)
print(df.columns.tolist())
print(df.head(2))                # the first 2 rows
```

```text
(4, 3)
['region', 'product', 'total']
  region product  total
0     EU     tea    120
1     US     jam     80
```

`df.info()` lists each column with its type and how many values are missing, and `df.describe()` gives summary statistics (section 4.2.1).

**Keep it organized.** Keep data **tidy**: each variable in its own column, each observation in its own row, and each kind of observation in its own table. Never change the raw file; save cleaned versions separately. Use consistent, lowercase column names.

**Sorting.** `sort_values` sorts by a column. By default it goes from smallest to largest:

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "US", "EU", "UK"],
                   "total": [120, 80, 150, 60]})

print(df.sort_values("total"))
```

```text
  region  total
3     UK     60
1     US     80
0     EU    120
2     EU    150
```

`ascending=False` reverses the order, so the largest comes first:

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "US", "EU", "UK"],
                   "total": [120, 80, 150, 60]})

print(df.sort_values("total", ascending=False))
```

```text
  region  total
2     EU    150
0     EU    120
1     US     80
3     UK     60
```

To sort by one column and then another, give a list of columns, and a list of directions to match:

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "US", "EU", "UK"],
                   "total": [120, 80, 150, 60]})

print(df.sort_values(["region", "total"], ascending=[True, False]))
```

```text
  region  total
2     EU    150
0     EU    120
3     UK     60
1     US     80
```

The regions are in A–Z order, and within EU the larger total comes first. Notice the row labels on the left move with their rows. `sort_values` returns a new DataFrame; `df` itself is unchanged unless you assign the result back.

**Filtering with a condition.** Put a condition in square brackets to keep only the rows where it is true. This is called a **boolean mask**: `df["total"] > 100` is a True/False for every row.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "US", "EU", "UK"],
                   "total": [120, 80, 150, 60]})

print((df["total"] > 100).tolist())      # the mask
print(df[df["total"] > 100])             # the rows where it is True
```

```text
[True, False, True, False]
  region  total
0     EU    120
2     EU    150
```

**Combining conditions.** Use `&` for "and", `|` for "or" and `~` for "not", and put **each condition in brackets**. Python's `and` and `or` don't work here.

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "US", "EU", "UK"],
                   "total": [120, 80, 150, 60]})

print(df[(df["region"] == "EU") & (df["total"] > 130)])
print(df[(df["region"] == "US") | (df["region"] == "UK")])
```

```text
  region  total
2     EU    150
  region  total
1     US     80
3     UK     60
```

**Two shortcuts.** `isin` checks against a list of values, and `query` lets you write the condition as a string:

```python
import pandas as pd

df = pd.DataFrame({"region": ["EU", "US", "EU", "UK"],
                   "total": [120, 80, 150, 60]})

print(df[df["region"].isin(["US", "UK"])])
print(df.query("region == 'EU' and total > 130"))     # inside query, "and" is allowed
```

```text
  region  total
1     US     80
3     UK     60
  region  total
2     EU    150
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

**Finding tags.** `find` returns the **first** matching tag, or `None` if there isn't one. `find_all` returns a **list** of every match.

```python
from bs4 import BeautifulSoup

html = """<ul>
  <li><a href="/guide.pdf">Guide</a></li>
  <li><a href="/faq.html">FAQ</a></li>
</ul>"""
soup = BeautifulSoup(html, "html.parser")

print(soup.find("a"))              # the first <a> tag
print(len(soup.find_all("a")))     # how many <a> tags there are
print(soup.find("table"))          # there is no <table>, so None
```

```text
<a href="/guide.pdf">Guide</a>
2
None
```

To match a CSS class, write `class_=` with an underscore, because `class` on its own is a reserved word in Python: `soup.find("a", class_="doc")`.

**Getting text and attributes.** `.get_text()` returns the text between the tags, and `strip=True` removes the spaces around it. Square brackets read an attribute, such as a link's address in `href`.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup('<a href="/guide.pdf">  Guide  </a>', "html.parser")
link = soup.find("a")

print(repr(link.get_text()))             # repr() makes the spaces visible
print(repr(link.get_text(strip=True)))
print(link["href"])
print(link.get("title"))                 # no title attribute, so None
```

```text
'  Guide  '
'Guide'
/guide.pdf
None
```

`link["title"]` would raise a `KeyError` instead, because this tag has no `title`. Use `.get()` when an attribute might be missing.

**CSS selectors.** `soup.select()` finds tags with the same patterns CSS uses. `ul#links a.doc` means "`<a>` tags with class `doc`, inside the `<ul>` whose id is `links`". It always returns a list.

```python
from bs4 import BeautifulSoup

html = """<ul id="links">
  <li><a class="doc" href="/guide.pdf">Guide</a></li>
  <li><a class="ad" href="/buy">Buy now</a></li>
</ul>"""
soup = BeautifulSoup(html, "html.parser")
print([a.get_text() for a in soup.select("ul#links a.doc")])
```

```text
['Guide']
```

The "Buy now" link has class `ad`, not `doc`, so it is left out.

**Tables straight into pandas.** `pd.read_html(url_or_html)` reads every `<table>` on a page and returns a **list** of DataFrames, one per table. Take `[0]` for the first.

**Ethical scraping.** Prefer an official API. Read the site's terms of service. Check `robots.txt` at the site root (`https://site.com/robots.txt`), which lists paths crawlers should not visit (`Disallow:`); `urllib.robotparser` can check it. Rate-limit your requests (for example `time.sleep()` between them), identify yourself with a User-Agent, cache what you have fetched, and don't collect personal data without a lawful basis.

Python's standard library can read `robots.txt` rules and tell you whether a page is allowed. Normally you point it at the site with `set_url("https://site.com/robots.txt")` and call `read()`. Here the rules are passed in directly, so the example works offline:

```python
from urllib.robotparser import RobotFileParser

rules = RobotFileParser()
rules.parse(["User-agent: *", "Disallow: /private/"])   # every bot: stay out of /private/

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

**Dates.** `pd.to_datetime` turns date text into real dates. By default, a single value it can't read stops the whole conversion with an error:

```python
import pandas as pd

s = pd.Series(["2025-07-15", "2025-07-16", "not a date"])
try:
    pd.to_datetime(s)
except ValueError:
    print("ValueError: the whole conversion failed")
```

```text
ValueError: the whole conversion failed
```

With `errors="coerce"`, the bad value becomes `NaT` ("not a time", the date version of NaN) and the others convert. After that, the `.dt` accessor reads parts of each date:

```python
import pandas as pd

s = pd.Series(["2025-07-15", "2025-07-16", "not a date"])
dates = pd.to_datetime(s, errors="coerce")
print(dates.dt.day_name().tolist())
```

```text
['Tuesday', 'Wednesday', nan]
```

Parse dates once, in one format and one time zone, before you analyze them. `format="%Y-%m-%d"` tells pandas the exact layout, which is faster and avoids guessing.

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

**Train/test split.** Before fitting any model, set part of the data aside for testing with `train_test_split`. Split **before** fitting scalers, imputers or encoders, and fit them on the training part only. `stratify=y` keeps the class proportions the same in both parts: [section 4.2.2](#/guide/b4/4-2-2) shows a split with and without it. For time series, split by time (train on the past, test on the future) instead of shuffling.

**Outliers and preprocessing.** Outliers pull the mean and standard deviation, compress min-max scaling, and can dominate a regression line. Decide how to treat them before scaling and modeling, and apply the rule learned on training data to test data too.

### Exam traps

> **Trap.** `pivot` fails when an index/column pair appears more than once; use `pivot_table` with an aggregation function instead.

> **Trap.** Fitting a scaler or imputer on the full dataset before splitting leaks test information into training (data leakage) and makes evaluation look better than it is.
