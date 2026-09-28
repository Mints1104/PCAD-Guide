# Glossary

Every key term in the guide, A to Z. Terms link here from each objective's essentials.

## Symbols

**.iloc** — pandas indexer that selects rows and columns by integer position; slice ends are excluded.

**.loc** — pandas indexer that selects rows and columns by label or boolean mask; slice ends are included.

## A

**Absolute reference** — a spreadsheet cell reference with `$` signs (`$B$2`) that stays fixed when a formula is copied.

**ACID** — the four guarantees of a database transaction: atomicity (all or nothing), consistency (rules hold), isolation (concurrent transactions don't interfere) and durability (committed data survives failures).

**Anonymization** — irreversibly removing or transforming personal identifiers so that no one can re-identify the person, even by combining fields.

**Annotation** — text or an arrow added to a chart to point out a specific value or event (`ax.annotate`).

**API** — Application Programming Interface: a documented way for programs to request data or actions from a service, usually over HTTP returning JSON.

**Axes** — in Matplotlib, one plotting area with its own x- and y-axis; a figure can hold several Axes.

**Axis** — in NumPy and pandas, the dimension an operation runs along: `axis=0` down the rows (one result per column), `axis=1` across the columns (one result per row).

## B

**Bar chart** — a chart of rectangular bars whose lengths compare values across categories; the value axis should start at zero.

**Bias-variance trade-off** — the tension between error from overly simple assumptions (bias) and error from sensitivity to the particular training data (variance); more model complexity lowers bias but raises variance.

**Boolean mask** — a Series or array of True/False values used to select the rows where the condition is True (`df[df["qty"] > 2]`).

**Bootstrapping** — estimating the variability of a statistic by repeatedly resampling the observed data with replacement and recomputing the statistic.

**Box plot** — a chart showing the median, the interquartile range (box), whiskers to 1.5 × IQR, and outliers as individual points.

**Broadcasting** — NumPy's rule for operating on arrays of different shapes by stretching dimensions of size 1; shapes are compared from the right.

**Bucketization** — converting a continuous variable into categories (bins), for example with `pd.cut` or `pd.qcut`.

## C

**Cherry-picking** — presenting only the data, period or subgroup that supports a conclusion while ignoring the rest.

**Claim-evidence-reasoning** — a structure for arguments: state the claim, present the supporting data, explain why the data supports the claim.

**Class** — a blueprint for objects that bundles data (attributes) and behaviour (methods).

**Colormap** — a mapping from numeric values to colours (`cmap="viridis"`), used for heatmaps and colour-coded scatter plots.

**Colour-blind-safe palette** — a set of colours distinguishable by people with common colour-vision deficiencies, such as viridis or Seaborn's `"colorblind"` palette.

**Composition** — building a class from other objects held as attributes ("has-a"), such as an Order that has a Customer.

**Concat** — `pd.concat`: stacking DataFrames along rows (`axis=0`) or placing them side by side (`axis=1`).

**Confidence interval** — a range computed from a sample that, over repeated sampling, would contain the true parameter a stated percentage of the time (for example 95%).

**Confounder** — a third variable that influences both variables in a correlation, creating an association without a direct causal link.

**Constructor** — the `__init__` method that runs when an object is created and sets its initial attributes.

**Continuous data** — numeric data that can take any value within a range, such as weight or time.

**Correlation** — a statistical association between two variables; Pearson's r measures its linear strength and direction.

**Cross-field validation** — checking that fields within the same record are consistent, such as an end date on or after the start date.

**Cross-reference check** — checking that a value exists in another dataset or reference list, such as an order's customer ID in the customers table.

**Cross-validation** — evaluating a model by training and testing it k times on different splits (folds) of the data and averaging the scores.

**Crosstab** — `pd.crosstab`: a frequency table counting each combination of two (or more) categorical variables.

**CRUD** — Create, Read, Update, Delete: the four basic data operations, which map to SQL's INSERT, SELECT, UPDATE and DELETE.

**CSV** — Comma-Separated Values: a plain-text tabular format with one record per line and fields separated by a delimiter.

**Cursor** — a database object that executes SQL statements and fetches their results (`con.cursor()`).

## D

**Data integration** — combining data from different sources into one consistent dataset.

**Data integrity** — the accuracy, completeness, consistency and reliability of data over its whole life cycle.

**Data lake** — a repository that stores raw data of any type in its native format, applying structure only when data is read.

**Data leakage** — information from outside the training data (the test set or the future) influencing model training, which inflates evaluation scores.

**Data storytelling** — presenting analysis as a narrative (context, finding, implication, recommendation) supported by visuals.

**Data warehouse** — a central store of cleaned, integrated, structured data designed for analytical queries and reporting.

**DataFrame** — pandas' two-dimensional labeled table: columns (each a Series) sharing a row index.

**ddof** — "delta degrees of freedom": the divisor of variance is n − ddof; 0 gives the population value, 1 the sample value.

**Deep copy** — a copy that duplicates an object and every object nested inside it (`copy.deepcopy`).

**Descriptive statistics** — numbers that summarize data: measures of centre (mean, median, mode) and spread (range, variance, standard deviation, IQR).

**Discrete data** — numeric data with countable, separate values, such as the number of purchases.

**Docstring** — a string literal placed first in a module, class or function to document it; available at run time through `help()`.

## E

**Encapsulation** — bundling data with the methods that manage it and restricting direct access to internal state.

**ETL** — Extract, Transform, Load: pulling data from sources, cleaning and reshaping it, then loading it into a target such as a warehouse.

**Exception** — an object Python raises when an error occurs; it stops normal flow unless handled with `try`/`except`.

## F

**Foreign key** — a column whose values must match primary-key values in another table, enforcing referential integrity.

## G

**Generalization** — a model's ability to perform well on new data it was not trained on.

**Granularity** — the level of detail of data, such as one row per transaction versus one row per day.

**GroupBy** — the pandas operation that splits rows into groups by key and applies a function to each group.

## H

**Hashable** — an object with a fixed hash value, such as an int, str or tuple of immutables; only hashable objects can be dict keys or set members.

**HAVING** — the SQL clause that filters groups after GROUP BY, and can use aggregate functions.

**Heatmap** — a grid of coloured cells representing values in a matrix, commonly used for correlation matrices.

**Histogram** — a chart of how often values of a numeric variable fall into consecutive bins, showing its distribution.

**Homoscedasticity** — constant variance of a regression's residuals across all fitted values; an assumption of linear regression.

## I

**Identity** — whether two names refer to the same object in memory, checked with `is`.

**Immutable** — unchangeable after creation; tuples, strings and numbers are immutable.

**Imputation** — replacing missing values with estimates such as the mean, median, mode or a model's prediction.

**Index** — the row labels of a pandas Series or DataFrame, used for selection and alignment.

**Inheritance** — defining a class that reuses and extends another class's attributes and methods ("is-a").

**INNER JOIN** — a SQL join returning only rows with matching keys in both tables.

**IQR** — interquartile range: Q3 − Q1, the spread of the middle 50% of the data.

**ISO 8601** — the international date and time format, such as `2025-07-15` or `2025-07-15T14:30:00Z`.

## J

**JSON** — JavaScript Object Notation: a text format of nested objects (key-value pairs) and arrays.

## L

**Label encoding** — replacing each category with an integer code.

**Least privilege** — giving each user or account only the permissions it needs.

**LEFT JOIN** — a SQL join returning all rows from the left table, with NULLs where the right table has no match.

**Legend** — the chart key that maps colours or markers to series names.

**Line chart** — a chart connecting data points in order, typically to show change over time.

**Linear regression** — a model predicting a continuous target as a weighted sum of predictors plus an intercept, fitted by least squares.

**Log-odds** — the logarithm of p / (1 − p); logistic regression models it as a linear function of the predictors.

**Logistic regression** — a classification model that predicts the probability of a binary outcome with the sigmoid of a linear score.

**Long format** — a data layout with one row per subject-measurement pair; also called tidy format.

## M

**MAR** — Missing At Random: missingness depends on other observed variables, not on the missing value itself.

**Matplotlib** — Python's foundational plotting library.

**MCAR** — Missing Completely At Random: missingness is unrelated to any data, observed or missing.

**Mean** — the sum of values divided by their count.

**Median** — the middle value of sorted data, or the average of the two middle values.

**Melt** — `df.melt`: reshaping wide data into long format.

**Merge** — `pd.merge`: combining DataFrames side by side by matching values in key columns.

**Method overriding** — a subclass redefining a method it inherited, replacing the parent's behaviour.

**Min-max scaling** — rescaling values to the range [0, 1] with (x − min) / (max − min).

**MNAR** — Missing Not At Random: missingness depends on the missing value itself.

**Mode** — the most frequent value in a dataset.

**Mutable** — changeable in place after creation; lists, dicts and sets are mutable.

## N

**Name mangling** — Python's renaming of `__attr` inside a class to `_ClassName__attr`, which prevents accidental access and name clashes.

**NaN** — "Not a Number": the floating-point marker pandas and NumPy use for missing values.

**ndarray** — NumPy's n-dimensional array of values that all share one data type.

**Normal distribution** — the symmetric, bell-shaped Gaussian distribution defined by its mean and standard deviation.

**NumPy** — Python's core library for fast numerical arrays and mathematics.

## O

**OLAP** — Online Analytical Processing: systems optimized for complex analytical queries over large data.

**OLTP** — Online Transaction Processing: systems optimized for many small, fast transactional reads and writes.

**One-hot encoding** — replacing a categorical column with one 0/1 indicator column per category.

**Outlier** — a value far from the rest of the data, often flagged with the IQR rule or |z| > 3.

**Overfitting** — a model learning noise in the training data, so it scores well on training data but poorly on new data (high variance).

## P

**pandas** — Python's library for labeled tabular data, built around Series and DataFrames.

**Parameterized query** — a SQL statement with placeholders whose values are passed separately to the database driver.

**PCA** — Principal Component Analysis: combining correlated features into fewer uncorrelated components, at the cost of interpretability.

**Pearson's r** — the correlation coefficient measuring the strength and direction of a linear relationship, from −1 to +1.

**PEP 257** — Python's docstring conventions.

**PEP 8** — Python's style guide for code.

**Pie chart** — a circle divided into slices showing parts of a whole; readable only with a few slices.

**PII** — Personally Identifiable Information: data that identifies a person directly or in combination with other data.

**pip** — Python's package installer for the Python Package Index (PyPI).

**Pivot table** — a summary table that aggregates a value by row and column categories (`pivot_table`).

**Polymorphism** — different classes providing the same method name so one call works on any of them.

**Primary key** — a column (or columns) whose values uniquely identify each row and cannot be NULL.

**Pseudonymization** — replacing identifiers with tokens that can be reversed with a separate key; the data remains personal data.

## Q

**Qualitative data** — descriptive, non-numeric data such as interview answers or open-ended comments.

**Quantitative data** — numeric data that can be counted or measured.

## R

**R²** — the coefficient of determination: the share of the variance in the target explained by a regression model.

**Range check** — validating that a value falls between allowed minimum and maximum limits.

**Rate limiting** — restricting how many requests are sent (or accepted) per unit of time.

**Regularization** — penalizing model complexity (for example large coefficients) to reduce overfitting.

**Resampling** — drawing new samples from observed data, as in bootstrapping.

**robots.txt** — a file at a website's root that tells automated crawlers which paths they should not visit.

## S

**scikit-learn** — Python's machine learning library for preprocessing, modeling and evaluation.

**Scatter plot** — a chart plotting pairs of numeric values as points, to show the relationship between two variables.

**Schema-on-read** — applying structure to data when it is read (typical of data lakes).

**Schema-on-write** — defining structure before data is stored (typical of databases and warehouses).

**Scope** — the region of code where a name is visible; Python resolves names in LEGB order.

**Seaborn** — a statistical visualization library built on Matplotlib.

**Selection bias** — distortion from the way individuals are chosen or choose themselves into a sample.

**Semi-structured data** — data with self-describing tags or keys but no fixed table schema, such as JSON and XML.

**Series** — pandas' one-dimensional labeled array.

**SFJWGHOL** — mnemonic for SQL's written clause order: SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT.

**Shallow copy** — a new container whose nested objects are still shared with the original.

**Split-apply-combine** — the groupby pattern: split data into groups, apply a function to each, combine the results.

**SQL injection** — an attack in which input inserted into SQL text changes the query's structure.

**Standard deviation** — the square root of the variance, measuring spread in the data's own units.

**Standard error** — the standard deviation of a statistic across repeated samples; for the mean, s / √n.

**Standard library** — the modules that ship with Python itself, such as `math`, `csv`, `json` and `sqlite3`.

**statsmodels** — a Python library for statistical models with inference output such as p-values and confidence intervals.

**Stratified sampling** — dividing a population into subgroups and sampling from each in proportion.

**Structured data** — data organized in a fixed schema of rows and typed columns.

**Supervised learning** — machine learning from labeled examples to predict a known target.

## T

**Test set** — held-out data used once, at the end, to estimate a model's performance on unseen data.

**Tidy data** — a layout where each variable is a column, each observation a row, and each kind of observation a table.

**Traceback** — the error report Python prints, listing the call chain with the most recent call last and the exception at the bottom.

**Train/test split** — dividing data into a part for fitting a model and a held-out part for evaluating it.

**Type affinity** — SQLite's flexible typing, where a column's declared type is a preference rather than a strict rule.

**Type check** — validating that a value has the expected data type.

## U

**Underfitting** — a model too simple to capture the pattern, scoring poorly on both training and test data (high bias).

**Uniform distribution** — a distribution in which every value in an interval [a, b] is equally likely.

**Unstructured data** — data with no predefined model, such as free text, images, audio and video.

## V

**Validation set** — data used during development to compare models and tune settings, separate from the final test set.

**Variance** — the average squared deviation from the mean.

**Vectorization** — applying an operation to a whole array or column at once in compiled code instead of looping in Python.

**Virtual environment** — an isolated Python environment with its own installed packages (`python -m venv`).

## W

**Web scraping** — automatically extracting data from web pages.

**Wide format** — a data layout with one row per subject and repeated measurements in separate columns.

## X

**XML** — Extensible Markup Language: a text format of nested, tagged elements with optional attributes.

## Z

**Z-score** — the number of standard deviations a value lies from the mean: (x − mean) / std.
