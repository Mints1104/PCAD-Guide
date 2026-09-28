# The exam

PCAD™ (Certified Associate Data Analyst with Python) is the Python Institute's associate-level data analytics certification, run by OpenEDG. It tests whether you can collect, integrate, clean, validate, analyze and visualize data with Python and SQL: pandas, NumPy, Matplotlib and Seaborn, basic statistics and simple supervised models, plus the Python and database skills that hold the work together. The profile it describes is a junior data analyst who can take a dataset from raw source to a clear recommendation.

## Format

| | PCAD-31-02 |
|---|---|
| Items | 48 |
| Question types | Single-select and multiple-select, including scenario-based items |
| Time | 60 minutes, plus time for the Non-Disclosure Agreement |
| Passing score | 75% cumulative average across all exam blocks |
| Delivery | OpenEDG Testing Service (TestNow™), online proctored |
| Language | English |
| Price | Exam from $195; exam + retake from $225; exam + practice test from $215; all three from $245; practice test alone $49 |
| Retakes | 15-day wait after a failed attempt |
| Validity | 6 years |
| Prerequisites | None formal. Recommended: PCAP and PCED, or equivalent experience |

Source: pythoninstitute.org/pcad and /pcad-exam-syllabus, checked 28 Sep 2026. PCAD-31-02 went live on 15 July 2025 and replaced PCAD-31-01, which retired on 14 July 2025. The Python Institute's own course for it (PD101, Python for Data Analytics 101) is still in development.

PCAD sits in the middle of the data analyst track: **PCED** (entry) → **PCAD** (associate) → **PCPD** (professional, in development).

## Five blocks

The 48 items are split across five blocks. Blocks 1 and 2 together are 30 items, 62.5% of the exam.

<div class="dg"><p class="dg-title">Items per block</p><div class="dg-flow">
<div class="dg-step"><b>Block 1 · 14 items</b><span>Data Acquisition and Pre-Processing, 29.2%</span></div>
<div class="dg-step"><b>Block 2 · 16 items</b><span>Programming and Database Skills, 33.3%</span></div>
<div class="dg-step"><b>Block 3 · 4 items</b><span>Statistical Analysis, 8.3%</span></div>
<div class="dg-step"><b>Block 4 · 9 items</b><span>Data Analysis and Modeling, 18.8%</span></div>
<div class="dg-step"><b>Block 5 · 5 items</b><span>Data Communication and Visualization, 10.4%</span></div>
</div></div>

Each block's item count equals the number of objectives it contains (14, 16, 4, 9 and 5 objectives), so the exam averages one item per syllabus objective. That is why PCAD Prep's full mock takes one question from every objective.

## What each objective covers

| Objective | Title | What it asks |
|---|---|---|
| 1.1.1 | Data collection methods | Surveys, interviews and web scraping; sampling; qualitative vs quantitative research; legal and ethical limits; anonymizing PII. |
| 1.1.2 | Aggregating sources | Combining databases, APIs and files into one dataset; aligning formats; keeping it consistent and accurate. |
| 1.1.3 | Storage solutions | Data warehouses, data lakes, CSV and Excel files, cloud storage. |
| 1.2.1 | Structured vs unstructured | What each is, and how it changes storage, retrieval and analysis. |
| 1.2.2 | Erroneous data | Detecting missing, inaccurate, duplicate and invalid values; MCAR, MAR, MNAR; imputation; outliers. |
| 1.2.3 | Normalization and scaling | Min-max scaling, z-scores, one-hot and label encoding, data reduction trade-offs, standard date and number formats. |
| 1.2.4 | Cleaning techniques | Imputation, string cleanup, boolean and case normalization, string-to-number conversion, one-hot encoding, bucketization. |
| 1.3.1 | Validation methods | Type, range and cross-field checks in Python; early type checks in ingestion scripts. |
| 1.3.2 | Data integrity | What integrity means and how clear validation rules protect it. |
| 1.4.1 | File formats | CSV, JSON, XML and TXT: what each is for and how to read and write it. |
| 1.4.2 | Accessing datasets | Local files, databases and online repositories; sorting and filtering. |
| 1.4.3 | Extracting data | Databases, APIs and HTML with requests and BeautifulSoup; ethical scraping (robots.txt, rate limits). |
| 1.4.4 | Spreadsheets | Layout, formatting and simple formulas for readable sheets. |
| 1.4.5 | Preparing data | Aligning to the analysis goal; date formats; wide vs long; train/test split; outliers. |
| 2.1.1 | Syntax and control flow | Variables, scope, basic types, loops and conditionals. |
| 2.1.2 | Functions | Positional vs keyword arguments, required vs optional parameters. |
| 2.1.3 | Data science ecosystem | Which library or tool fits which job. |
| 2.1.4 | Data structures | Lists, tuples, sets, dictionaries and strings. |
| 2.1.5 | Style | PEP 8 code style and PEP 257 docstrings. |
| 2.2.1 | Modules and packages | import forms, aliasing, standard library vs pip vs local modules; pip install, upgrade, uninstall. |
| 2.2.2 | Exceptions | try / except / else / finally, common errors, reading tracebacks. |
| 2.3.1 | Classes for data | Constructors, instance variables, `_protected` and `__private` names, getters and setters. |
| 2.3.2 | OOP reuse | Composition, inheritance, overriding, polymorphism. |
| 2.3.3 | Identity and comparison | Shared vs independent objects, `==` vs `is`, custom `__eq__`. |
| 2.4.1 | SQL queries | SELECT, FROM, JOINs, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT. |
| 2.4.2 | CRUD | INSERT, SELECT, UPDATE, DELETE. |
| 2.4.3 | Connecting from Python | sqlite3 and pymysql connections; common connection problems. |
| 2.4.4 | Parameterized queries | Placeholders instead of string formatting; why that stops SQL injection. |
| 2.4.5 | SQL data types | SQL types, their Python counterparts, conversion on the way in and out. |
| 2.4.6 | Database security | SQL injection and writing safe queries from Python. |
| 3.1.1 | Descriptive measures | Mean, median, mode, variance, standard deviation; Gaussian and uniform distributions; confidence. |
| 3.1.2 | Relationships | Outliers, Pearson's r, and reading box plots, histograms, scatter plots, line plots and heatmaps. |
| 3.2.1 | Bootstrapping | Resampling with replacement to estimate uncertainty; when it applies. |
| 3.2.2 | Regression | Linear vs logistic regression: assumptions, fitting in Python, reading coefficients and fit. |
| 4.1.1 | Cleaning with pandas | Filtering, sorting, missing and inconsistent values. |
| 4.1.2 | Merge and reshape | merge, join, concat, pivot, melt. |
| 4.1.3 | Series and DataFrames | How they relate; indexes; vectorized operations. |
| 4.1.4 | Selecting data | `.loc`, `.iloc`, slicing, boolean masks. |
| 4.1.5 | NumPy | Array arithmetic, broadcasting, aggregations; arrays vs lists vs Series vs DataFrames. |
| 4.1.6 | Grouping | groupby, summary tables, pivot tables, crosstab. |
| 4.2.1 | Descriptive statistics in code | Mean, median, mode, variance and standard deviation with pandas and NumPy. |
| 4.2.2 | Test datasets | Why a held-out test set matters and how to choose one fairly. |
| 4.2.3 | Supervised learning | Overfitting, underfitting, the bias-variance trade-off, linear vs logistic models. |
| 5.1.1 | Matplotlib and Seaborn | Box plots, histograms, scatter plots, line plots, correlation heatmaps. |
| 5.1.2 | Choosing charts | Which chart suits which data and message. |
| 5.1.3 | Refining charts | Titles, axis labels, annotations, colours, legend position and style. |
| 5.2.1 | Audience | Adapting content and visuals for technical and non-technical audiences. |
| 5.2.2 | Evidence | Pulling out key findings and backing every claim with data. |

## How PCAD Prep mirrors the exam

- **Mock test**: 48 questions in 60 minutes, one from each objective, so each block gets its official share (14 / 16 / 4 / 9 / 5). Single- and multiple-select items appear together. Option order is shuffled on every attempt.
- **Shorter mocks**: 12 or 24 questions keep the block proportions and the 75-seconds-per-question pace.
- **Practice mode**: one question at a time with instant feedback, filterable by block, objective or kind (code reading vs concept).
- **Pass mark**: 75%, the Python Institute's published cumulative score.
- **Code**: every code question was run with pandas 3 and NumPy 2 to confirm its answer. Questions avoid behaviour that changed between pandas 2 and 3 unless the change is the point.

## Exam-day tactics

> **Tactic.** Budget 75 seconds per item (60 minutes ÷ 48). Code-reading items take longer, so bank time on the one-line recall items.

> **Tactic.** Blocks 1 and 2 are 30 of the 48 items. If your revision time is short, spend it there first.

> **Tactic.** A multiple-select stem tells you how many to pick. Count your choices before moving on.

> **Tactic.** Trace code line by line on the scratch area in your head: write down each variable's value after every line that changes it. Most wrong options are the value one line too early or too late.

> **Tactic.** Watch the classic off-by-one traps: `.loc` slices include the end label, `.iloc` and Python slices exclude it, and `range(n)` stops at `n - 1`.

> **Tactic.** A pandas method with `inplace=True` returns `None`. If the code assigns that result back to a variable, the variable holds `None`.

> **Tactic.** For "which is best" scenarios, name what the question optimizes (privacy, speed, accuracy, readability for executives) before reading the options. Two options are often correct in general; one fits the stated goal.

> **Tactic.** In SQL, remember the written order (SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT) and the logical order: WHERE filters rows before grouping, HAVING filters groups after it.
