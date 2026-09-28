from qhelp import Q

QUESTIONS = [
    # ---------- 1.1.1 Data collection methods ----------
    Q("b1-001", "1.1.1", 1,
      "A product team wants to understand why users abandon the checkout page. They plan twelve one-hour conversations with people who recently abandoned a basket. Which collection method is this, and what kind of data will it produce?",
      ["Interviews, producing qualitative data",
       "A survey, producing quantitative data",
       "Web scraping, producing semi-structured data",
       "An A/B experiment, producing causal estimates"],
      0,
      {1: "A survey reaches many people with fixed questions; twelve open conversations are interviews.",
       2: "Scraping extracts published web content; it doesn't talk to users.",
       3: "An experiment randomly assigns users to versions; nothing is being varied here."},
      "Long, open conversations with a small group are interviews, and they produce qualitative data that explains why people behave as they do.",
      "Syllabus 1.1.1", ["collection-methods", "qualitative"]),

    Q("b1-002", "1.1.1", 2,
      "A national retailer will survey 2,000 loyalty members. Rural stores serve only 8% of members, and the team must be sure rural views are represented in proportion. Which sampling method fits best?",
      ["Stratified random sampling by store type",
       "Convenience sampling at the five largest stores",
       "Systematic sampling of every 10th visitor to the website",
       "Cluster sampling of three city stores"],
      0,
      {1: "The largest stores are urban, so rural members would be missed: a biased convenience sample.",
       2: "Website visitors are a different population from loyalty members, and nothing guarantees rural coverage.",
       3: "Picking three city clusters excludes rural members entirely."},
      "Stratified sampling divides the population into groups (urban and rural stores) and samples each in proportion, guaranteeing that small groups are represented.",
      "Syllabus 1.1.1", ["sampling", "stratified"]),

    Q("b1-003", "1.1.1", 2,
      "A hospital wants to share patient records with researchers so that no patient can be re-identified by anyone, including the hospital. Which approach achieves anonymization rather than pseudonymization?",
      ["Remove names and IDs, generalize birth dates to 10-year bands and postcodes to regions, and keep no key that links records back to patients",
       "Replace each patient name with a random token and keep the token-to-name table in a secure vault",
       "Hash each national ID with a secret key held by the hospital",
       "Encrypt the whole dataset and give researchers the decryption key"],
      0,
      {1: "A stored lookup table makes the tokens reversible: that is pseudonymization, still personal data.",
       2: "A keyed hash can be recomputed by the key holder to re-link records: pseudonymization.",
       3: "Encryption is reversible by design; anyone with the key sees the identities."},
      "Anonymization is irreversible: direct identifiers are removed and quasi-identifiers (birth date, postcode) are generalized so that nobody can re-identify a person, even by combining fields.",
      "Syllabus 1.1.1 · GDPR recital 26", ["pii", "anonymization"]),

    Q("b1-004", "1.1.1", 2,
      "Which two survey questions should be rewritten because they bias or confuse the answers? Select two.",
      ["How satisfied are you with our delivery speed? (1 = very unsatisfied, 5 = very satisfied)",
       "Don't you agree that our new app is much better than the old one?",
       "How quick and easy was the checkout process?",
       "In the last 30 days, how many times did you order online?",
       "Which payment method did you use most recently?"],
      [1, 2],
      {0: "A balanced 1-to-5 scale on one topic is a well-formed question.",
       3: "A single, specific, neutral frequency question.",
       4: "A single, factual question with no pressure toward an answer."},
      "\"Don't you agree…\" is a leading question that pushes respondents toward yes. \"Quick and easy\" is double-barreled: it asks about two things, so an answer can't be interpreted.",
      "Syllabus 1.1.1", ["survey-design", "bias"]),

    Q("b1-005", "1.1.1", 2,
      "An analyst plans to scrape a competitor's public product pages every day to track prices. What should come first to address the legal and ethical considerations?",
      ["Read the site's terms of service and robots.txt, and plan a slow, rate-limited schedule",
       "Rotate IP addresses so the site cannot block the scraper",
       "Scrape every page as fast as possible overnight when traffic is low",
       "Also collect reviewers' names and profile pages for richer data"],
      0,
      {1: "Evading blocks ignores the site owner's wishes and can breach terms of service.",
       2: "Speed is still load on someone else's server, and nothing here checks what is allowed.",
       3: "Collecting personal data needs a lawful basis and adds privacy risk without serving the goal."},
      "Ethical scraping starts with what the site permits (terms of service, robots.txt) and continues with gentle, rate-limited collection of only the data you need.",
      "Syllabus 1.1.1, 1.4.3", ["web-scraping", "ethics"]),

    Q("b1-006", "1.1.1", 3,
      "An email survey about workload goes to all 4,000 employees. Only 9% respond, and most responses come from managers, who answer during quiet periods. Which problem most threatens the conclusions?",
      ["Non-response bias: the people who answered differ from those who didn't",
       "Survivorship bias: only successful projects are counted",
       "Measurement error: the rating scale is too coarse",
       "Overfitting: the sample is too small for a model"],
      0,
      {1: "Survivorship bias is about only seeing survivors (such as firms that didn't fail); here it's about who chose to reply.",
       2: "Nothing suggests the scale is the problem; the issue is who answered.",
       3: "Overfitting is a modeling problem, not a sampling one."},
      "When responders systematically differ from non-responders (managers with lighter workloads answer; busy staff don't), the results are skewed by non-response bias no matter how many answers arrive.",
      "Syllabus 1.1.1", ["sampling", "bias"]),

    # ---------- 1.1.2 Aggregating sources ----------
    Q("b1-010", "1.1.2", 2,
      "The CRM exports customer IDs as zero-padded text; the web shop stores them as integers. What does this code print?",
      ["`2`", "`3`", "`0`", "`1`"],
      0,
      {1: "Customer 4 exists only in `web` and customer 3 only in `crm`; an inner merge keeps matches only.",
       2: "Zero would be the result without the `astype(int)` step, when the key types don't match.",
       3: "Both 1 and 2 match once the keys are integers."},
      "After `astype(int)`, \"001\" becomes 1 and \"002\" becomes 2, so the inner merge matches customers 1 and 2: two rows.",
      "Syllabus 1.1.2 · pandas: DataFrame.merge", ["merge", "data-types"],
      code="""
      import pandas as pd

      crm = pd.DataFrame({"cust_id": ["001", "002", "003"], "tier": ["gold", "silver", "gold"]})
      web = pd.DataFrame({"cust_id": [1, 2, 4], "visits": [5, 3, 8]})

      crm["cust_id"] = crm["cust_id"].astype(int)
      merged = web.merge(crm, on="cust_id", how="inner")
      print(len(merged))
      """, verify="stdout"),

    Q("b1-011", "1.1.2", 1,
      "Twelve stores each send a monthly CSV with identical columns (date, sku, units, revenue). Which pandas operation combines them into one dataset?",
      ["`pd.concat(frames, ignore_index=True)`",
       "`frames[0].merge(frames[1], on=\"sku\")`, repeated for each file",
       "`frames[0].pivot_table(values=\"units\", index=\"sku\")`",
       "`frames[0].join(frames[1])`"],
      0,
      {1: "Merging joins columns side by side on a key; it would create wide, duplicated columns.",
       2: "A pivot table reshapes and aggregates one table; it doesn't combine files.",
       3: "`join` aligns on the index and adds columns; the files need stacking, not joining."},
      "Files with the same columns are stacked row-wise with `pd.concat`; `ignore_index=True` renumbers the rows.",
      "Syllabus 1.1.2 · pandas: concat", ["concat", "integration"]),

    Q("b1-012", "1.1.2", 2,
      "EU revenue arrives in euros with dates like 31/01/2025; US revenue arrives in dollars with dates like 2025-01-31. The goal is one monthly revenue report. What should happen before the data is combined?",
      ["Convert both to one currency and parse both date columns into real datetimes",
       "Concatenate first and let the monthly totals average out the differences",
       "Drop the date column, since the months can be inferred from the file names",
       "Round every amount to whole numbers so the currencies line up"],
      0,
      {1: "Summing euros and dollars produces meaningless totals, and unparsed dates won't group by month.",
       2: "Dropping dates removes the key needed for a monthly report.",
       3: "Rounding doesn't convert currencies."},
      "Standardize before integrating: one unit (currency) and one parsed date format, so values are comparable and group correctly.",
      "Syllabus 1.1.2", ["standardization", "integration"]),

    Q("b1-013", "1.1.2", 3,
      "Customer `a` appears twice in both tables. What is the shape of the merged result?",
      ["`(5, 3)`", "`(3, 3)`", "`(4, 3)`", "`(6, 3)`"],
      0,
      {1: "Three rows would mean each order matched exactly one email, but `a` has two of each.",
       2: "Four is the count for customer `a` alone; customer `b` adds one more.",
       3: "Six would need three matches for `b` too."},
      "A many-to-many key produces every combination: customer `a` gives 2 × 2 = 4 rows and `b` gives 1, so 5 rows with columns cust, amount and email.",
      "Syllabus 1.1.2 · pandas: DataFrame.merge", ["merge", "duplicates"],
      code="""
      import pandas as pd

      orders = pd.DataFrame({"cust": ["a", "a", "b"], "amount": [10, 20, 30]})
      emails = pd.DataFrame({"cust": ["a", "a", "b"], "email": ["x@1", "x@2", "y@1"]})
      print(orders.merge(emails, on="cust").shape)
      """, verify="stdout"),

    Q("b1-014", "1.1.2", 2,
      "After left-merging a transactions table with a customer table, which two checks best confirm the integration kept the data consistent? Select two.",
      ["Compare the number of rows before and after the merge",
       "Count new missing values in the customer columns",
       "Sort the result alphabetically by customer name",
       "Convert every column to text",
       "Drop the key column to avoid duplicates"],
      [0, 1],
      {2: "Sorting changes order, not correctness; it reveals nothing about bad matches.",
       3: "Converting to text loses types and checks nothing.",
       4: "Dropping the key removes the ability to trace records; it doesn't check anything."},
      "A row count that grew reveals duplicate keys; new NaNs in customer columns reveal transactions with no matching customer.",
      "Syllabus 1.1.2", ["merge", "validation"]),

    Q("b1-015", "1.1.2", 1,
      "A team loads raw clickstream data straight into a cloud warehouse and cleans and reshapes it there with SQL. Which integration pattern is this?",
      ["ELT (extract, load, transform)", "ETL (extract, transform, load)", "OLTP", "CRUD"],
      0,
      {1: "ETL transforms data before loading it into the target.",
       2: "OLTP describes transactional databases, not an integration pattern.",
       3: "CRUD names the basic data operations, not an integration pattern."},
      "Loading raw data first and transforming it inside the target system is ELT.",
      "Syllabus 1.1.2", ["elt", "integration"]),

    # ---------- 1.1.3 Storage ----------
    Q("b1-020", "1.1.3", 1,
      "An IoT company wants to keep raw sensor logs, JSON events and camera images for future machine-learning projects, without deciding their structure yet. Which storage suits this?",
      ["A data lake", "A data warehouse", "A shared Excel workbook", "The production OLTP database"],
      0,
      {1: "Warehouses need a schema before loading and suit cleaned, structured data.",
       2: "Excel can't hold images or billions of log lines.",
       3: "OLTP databases run day-to-day transactions; loading bulk raw data would slow them and doesn't fit images."},
      "A data lake stores raw data of any type in its native format and applies structure only when it is read (schema-on-read).",
      "Syllabus 1.1.3", ["data-lake", "storage"]),

    Q("b1-021", "1.1.3", 2,
      "Finance wants consistent monthly KPI dashboards built with SQL from cleaned, integrated sales, inventory and HR data. Which storage fits best?",
      ["A data warehouse", "A data lake", "One CSV file per department", "An in-memory Python dictionary"],
      0,
      {1: "A lake holds raw data; dashboards would each have to repeat the cleaning.",
       2: "Separate CSVs have no shared schema or integration for cross-department KPIs.",
       3: "In-memory data disappears when the program stops and isn't shared."},
      "A warehouse stores cleaned, integrated, structured data with a defined schema, optimized for SQL analytics and BI.",
      "Syllabus 1.1.3", ["data-warehouse", "storage"]),

    Q("b1-022", "1.1.3", 2,
      "Which statement correctly contrasts data warehouses and data lakes?",
      ["A warehouse applies a schema before data is loaded; a lake applies it when data is read",
       "A lake applies a schema before loading; a warehouse applies it when data is read",
       "Lakes can only store structured tables",
       "Warehouses cannot be queried with SQL"],
      0,
      {1: "This reverses the two: lakes are schema-on-read.",
       2: "Lakes are defined by accepting any format, including unstructured data.",
       3: "SQL is the main way warehouses are queried."},
      "Warehouses are schema-on-write (structure defined up front); lakes are schema-on-read (structure applied at query time).",
      "Syllabus 1.1.3", ["schema-on-read", "storage"]),

    Q("b1-023", "1.1.3", 2,
      "A marketing analyst saves a three-sheet Excel workbook full of formulas as a CSV and emails it. What does the recipient receive?",
      ["The values of the active sheet only, with no formulas or formatting",
       "All three sheets, one after another",
       "The formulas as text, ready to recalculate",
       "The values and the cell formatting of all sheets"],
      0,
      {1: "CSV holds one table; the other sheets are not included.",
       2: "CSV stores the computed values, not the formulas.",
       3: "CSV is plain text: no formatting survives."},
      "CSV is a plain-text, single-table format: saving a workbook as CSV keeps only the active sheet's values.",
      "Syllabus 1.1.3, 1.4.4", ["csv", "excel"]),

    Q("b1-024", "1.1.3", 2,
      "Which two are genuine advantages of cloud object storage for an analytics team? Select two.",
      ["Capacity scales up and down with pay-as-you-go pricing",
       "Data is replicated for high durability",
       "It enforces relational schemas and foreign keys automatically",
       "It removes the need for access control",
       "It is always faster than reading from local memory"],
      [0, 1],
      {2: "Object storage holds files; schemas and keys are enforced by databases, not by the storage layer.",
       3: "Cloud data still needs access control; misconfigured permissions are a common leak.",
       4: "Local memory is faster; the cloud's advantages are scale, durability and sharing."},
      "Cloud storage offers elastic, pay-as-you-go capacity and durability through replication, and lets storage and compute scale separately.",
      "Syllabus 1.1.3", ["cloud-storage", "storage"]),

    # ---------- 1.2.1 Structured vs unstructured ----------
    Q("b1-030", "1.2.1", 1,
      "Which of these is semi-structured data?",
      ["A JSON response from a weather API", "An orders table in PostgreSQL", "A JPEG product photo", "An MP3 call recording"],
      0,
      {1: "A relational table with fixed, typed columns is structured.",
       2: "Images have no predefined data model: unstructured.",
       3: "Audio is unstructured."},
      "JSON carries self-describing keys and nesting but no fixed table schema, which makes it semi-structured.",
      "Syllabus 1.2.1", ["semi-structured", "data-types"]),

    Q("b1-031", "1.2.1", 2,
      "A company has 50,000 recorded support calls and wants to count complaints by topic with pandas. What must happen first?",
      ["Transcribe the audio and extract topics into structured columns",
       "Load the recordings with `pd.read_csv`",
       "Min-max scale the recordings",
       "Nothing; pandas reads audio files directly"],
      0,
      {1: "`read_csv` reads delimited text, not audio.",
       2: "Scaling applies to numeric columns; there are none yet.",
       3: "pandas works with tabular data; audio must be converted first."},
      "Unstructured data needs a processing step (here speech-to-text plus topic extraction) that turns it into structured features before tabular analysis.",
      "Syllabus 1.2.1", ["unstructured", "preprocessing"]),

    Q("b1-032", "1.2.1", 1,
      "Which two are examples of structured data? Select two.",
      ["An orders table in a relational database",
       "A spreadsheet of employee IDs, departments and salaries",
       "Product photos",
       "Free-text survey comments",
       "Scanned PDF invoices"],
      [0, 1],
      {2: "Images are unstructured.",
       3: "Free text is unstructured, even when stored in a column.",
       4: "Scanned documents are images: unstructured until text is extracted."},
      "Structured data follows a fixed schema of rows and typed columns, like database tables and well-formed spreadsheets.",
      "Syllabus 1.2.1", ["structured", "data-types"]),

    Q("b1-033", "1.2.1", 2,
      "How does unstructured data usually differ from structured data in storage and retrieval?",
      ["It is kept in object storage or data lakes and found through metadata and search indexes rather than SQL on typed columns",
       "It is kept in relational tables and retrieved with joins on primary keys",
       "It needs less storage because it has no schema",
       "Storage and retrieval work exactly the same way"],
      0,
      {1: "That describes structured data.",
       2: "Images, audio and video usually need far more storage than tabular records.",
       3: "The lack of a schema changes both where it lives and how it is found."},
      "Without a schema you can't query columns directly, so unstructured data lives in object stores and lakes and is located via metadata, tags or search indexes.",
      "Syllabus 1.2.1", ["unstructured", "storage"]),

    # ---------- 1.2.2 Erroneous data ----------
    Q("b1-040", "1.2.2", 2,
      "In a health survey, older participants skip the \"weekly exercise hours\" question more often than younger ones. Age is recorded for everyone. Which type of missingness is this?",
      ["MAR (missing at random)", "MCAR (missing completely at random)", "MNAR (missing not at random)", "Structural zeros"],
      0,
      {1: "MCAR would mean missingness is unrelated to anything, but it depends on age.",
       2: "MNAR would mean it depends on the exercise hours themselves; here it depends on an observed variable, age.",
       3: "Structural zeros are true zeros by design, not missing answers."},
      "When missingness depends on another observed variable (age) rather than on the missing value itself, it is MAR, so impute using the related variables.",
      "Syllabus 1.2.2", ["missing-data", "mar"]),

    Q("b1-041", "1.2.2", 2,
      "Customers with the largest debts are the least likely to report their debt in a financial survey. Which type of missingness is this?",
      ["MNAR (missing not at random)", "MAR (missing at random)", "MCAR (missing completely at random)", "Duplicate data"],
      0,
      {1: "MAR depends on other observed variables; here missingness depends on the debt amount itself.",
       2: "MCAR would be unrelated to anything.",
       3: "Nothing is duplicated; values are absent."},
      "Missingness driven by the unobserved value itself (large debts are hidden because they are large) is MNAR, the hardest case, where deletion and simple imputation are biased.",
      "Syllabus 1.2.2", ["missing-data", "mnar"]),

    Q("b1-042", "1.2.2", 1,
      "A lab technician accidentally drops a random 2% of blood samples before testing. The lost results are:",
      ["MCAR (missing completely at random)", "MAR (missing at random)", "MNAR (missing not at random)", "Outliers"],
      0,
      {1: "No other variable explains which samples were dropped.",
       2: "The dropped samples' values had nothing to do with being dropped.",
       3: "Outliers are extreme values, not missing ones."},
      "Accidental, random loss unrelated to any variable is MCAR; dropping those rows loses power but doesn't bias results.",
      "Syllabus 1.2.2", ["missing-data", "mcar"]),

    Q("b1-043", "1.2.2", 2,
      "What does this IQR outlier check print?",
      ["`[45]`", "`[12, 45]`", "`[]`", "`[19, 45]`"],
      0,
      {1: "The lower fence is 9.5, so 12 is inside the normal range.",
       2: "45 is far above the upper fence of 23.5.",
       3: "19 is below the upper fence of 23.5."},
      "Q1 = 14.75 and Q3 = 18.25, so IQR = 3.5 and the fences are 9.5 and 23.5. Only 45 lies outside.",
      "Syllabus 1.2.2 · pandas: Series.quantile", ["outliers", "iqr"],
      code="""
      import pandas as pd

      s = pd.Series([12, 14, 15, 15, 16, 18, 19, 45])
      q1, q3 = s.quantile(0.25), s.quantile(0.75)
      iqr = q3 - q1
      print(s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)].tolist())
      """, verify="stdout"),

    Q("b1-044", "1.2.2", 2,
      "The source system writes -999 for unknown ages and \"N/A\" for unknown cities. What does this code print?",
      ["`1`", "`3`", "`2`", "`4`"],
      0,
      {1: "-999, \"N/A\" and the empty string are ordinary values to pandas; only the real NaN counts.",
       2: "The empty string is not NaN either.",
       3: "Only one cell holds an actual NaN."},
      "`isna()` only recognizes real missing markers (NaN, None). Sentinels such as -999, \"N/A\" or \"\" must be converted first, for example with `na_values=` or `replace`.",
      "Syllabus 1.2.2 · pandas: isna", ["missing-data", "sentinels"],
      code="""
      import numpy as np
      import pandas as pd

      df = pd.DataFrame({"age": [34, -999, 29, np.nan],
                         "city": ["Oslo", "N/A", "", "Rome"]})
      print(df.isna().sum().sum())
      """, verify="stdout"),

    Q("b1-045", "1.2.2", 2,
      "An income column is strongly right-skewed by a few very high earners, and 6% of values are missing completely at random. Which simple imputation is most appropriate?",
      ["The median income", "The mean income", "The mode of income", "Zero"],
      0,
      {1: "The high earners pull the mean upward, so it overstates a typical income.",
       2: "Continuous incomes rarely repeat, so the mode is unstable and unrepresentative.",
       3: "Zero invents a false value and drags every statistic down."},
      "The median is robust to skew and outliers, so it gives a representative fill value for a skewed numeric column.",
      "Syllabus 1.2.2", ["imputation", "median"]),

    Q("b1-046", "1.2.2", 3,
      "What is the effect of replacing every missing value in a numeric column with the column's mean?",
      ["The mean stays the same, the variance shrinks and correlations with other columns weaken",
       "The mean increases and the variance grows",
       "The median always becomes equal to the mean",
       "No statistic changes, because only missing cells are touched"],
      0,
      {1: "Filling with the mean leaves the mean unchanged and adds values at the centre, reducing spread.",
       2: "The median can move, but it doesn't have to equal the mean.",
       3: "Adding many identical central values changes the variance and correlations."},
      "Mean imputation piles values at the centre: the mean is preserved, but the spread shrinks and relationships with other variables are diluted.",
      "Syllabus 1.2.2", ["imputation", "variance"]),

    Q("b1-047", "1.2.2", 2,
      "Which two checks help detect inconsistent entries in a categorical `country` column? Select two.",
      ["`df[\"country\"].value_counts()` to spot variants such as \"UK\", \"U.K.\" and \"uk \"",
       "Comparing the values with an allowed list of ISO country codes",
       "Computing z-scores of the column",
       "`df[\"country\"].mean()`",
       "Min-max scaling the column"],
      [0, 1],
      {2: "Z-scores need numbers; they are meaningless for categories.",
       3: "A mean of text categories isn't defined.",
       4: "Scaling applies to numeric columns."},
      "For categorical data, frequency tables and allowed-value lists reveal spelling, case and whitespace variants; numeric statistics don't apply.",
      "Syllabus 1.2.2", ["categorical", "data-quality"]),

    Q("b1-048", "1.2.2", 3,
      "A sales dataset shows one transaction of €250,000; typical transactions are €20 to €300. The store confirms it was a genuine bulk order from a corporate client. What should the analyst do?",
      ["Keep it, and analyze it separately or use robust statistics where it would distort typical-customer results",
       "Delete it, because it is an outlier",
       "Replace it with the mean transaction value",
       "Cap it at €300 and don't mention it"],
      0,
      {1: "Deleting a confirmed, real transaction throws away true information.",
       2: "Replacing a verified value with the mean falsifies the data.",
       3: "Silently capping a real value distorts revenue and hides a key customer."},
      "Outliers that are genuine are information. Keep them, document the decision, and use methods (median, separate segment) that stop them dominating typical-case analysis.",
      "Syllabus 1.2.2", ["outliers", "judgement"]),

    # ---------- 1.2.3 Normalization, scaling, encoding ----------
    Q("b1-050", "1.2.3", 2,
      "What does this min-max scaling print?",
      ["`[0.0, 0.125, 0.375, 1.0]`", "`[0.2, 0.3, 0.5, 1.0]`", "`[0.0, 0.1, 0.3, 0.8]`", "`[0.0, 0.25, 0.5, 1.0]`"],
      0,
      {1: "That divides by the maximum only (x / max) without subtracting the minimum.",
       2: "That subtracts the minimum but divides by 100 instead of the range, 80.",
       3: "That treats the values as evenly spaced; they aren't."},
      "Min-max scaling computes (x − 20) / (100 − 20): 0/80, 10/80, 30/80 and 80/80.",
      "Syllabus 1.2.3", ["min-max", "scaling"],
      code="""
      import pandas as pd

      s = pd.Series([20, 30, 50, 100])
      print(((s - s.min()) / (s.max() - s.min())).tolist())
      """, verify="stdout"),

    Q("b1-051", "1.2.3", 1,
      "A feature has mean 50 and standard deviation 10. What is the z-score of the value 75?",
      ["2.5", "0.75", "25", "0.25"],
      0,
      {1: "0.75 is 75/100, which is not the z-score formula.",
       2: "25 is the raw distance from the mean, not divided by the standard deviation.",
       3: "0.25 would divide 25 by 100."},
      "z = (x − mean) / std = (75 − 50) / 10 = 2.5: the value is 2.5 standard deviations above the mean.",
      "Syllabus 1.2.3", ["z-score", "standardization"]),

    Q("b1-052", "1.2.3", 2,
      "A linear regression will use `payment_method` (card, cash or voucher) as a feature. Which encoding avoids implying a false order?",
      ["One-hot encoding", "Label encoding (card = 0, cash = 1, voucher = 2)", "Min-max scaling", "Z-score standardization"],
      0,
      {1: "Integer codes tell a linear model that voucher > cash > card, an order that doesn't exist.",
       2: "Scaling applies to numbers; the column is categorical.",
       3: "Standardization also needs numeric input."},
      "One-hot encoding creates one 0/1 column per category, so a nominal variable gets no artificial ordering.",
      "Syllabus 1.2.3", ["one-hot", "encoding"]),

    Q("b1-053", "1.2.3", 2,
      "A `satisfaction` column holds \"low\", \"medium\" and \"high\". The model should be able to use the fact that high > medium > low. Which encoding does that?",
      ["An explicit ordinal mapping: low = 0, medium = 1, high = 2",
       "One-hot encoding into three indicator columns",
       "Alphabetical label encoding (high = 0, low = 1, medium = 2)",
       "Dropping the column"],
      0,
      {1: "One-hot columns are valid but carry no order information between levels.",
       2: "Alphabetical codes scramble the real order.",
       3: "Dropping the column loses a useful feature."},
      "For ordered categories, map to integers that follow the real order so the model can use it.",
      "Syllabus 1.2.3", ["ordinal", "encoding"]),

    Q("b1-054", "1.2.3", 3,
      "An `income` feature contains one extreme outlier. What happens if it is min-max scaled?",
      ["Most values are squeezed into a narrow band near 0",
       "All values are bounded to the range [−1, 1]",
       "Min-max scaling is unaffected by outliers",
       "The outlier is removed automatically"],
      0,
      {1: "Min-max scaling maps to [0, 1], and z-scores are unbounded; neither gives [−1, 1].",
       2: "The outlier becomes the maximum, which sets the scale for everything else.",
       3: "Scaling transforms values; it removes nothing."},
      "The outlier becomes the max, so (x − min) / (max − min) is tiny for every ordinary value: they crowd near 0. Z-scores or robust scaling are less affected.",
      "Syllabus 1.2.3", ["min-max", "outliers"]),

    Q("b1-055", "1.2.3", 2,
      "A team reduces 40 customer attributes to 5 principal components with PCA, and model accuracy stays the same. What is the main cost when presenting the model to the marketing department?",
      ["Each component mixes many original attributes, so the results are harder to explain",
       "The model becomes much slower",
       "The data needs more storage",
       "PCA introduces missing values"],
      0,
      {1: "Five features are faster to process than forty.",
       2: "Five columns need less storage than forty.",
       3: "PCA doesn't create missing values."},
      "Data reduction trades explainability for simplicity: a component is a weighted blend of attributes, not a business variable anyone recognizes.",
      "Syllabus 1.2.3", ["pca", "data-reduction"]),

    Q("b1-056", "1.2.3", 1,
      "Which date is written in ISO 8601 format?",
      ["2025-07-15", "15/07/2025", "07-15-2025", "July 15, 2025"],
      0,
      {1: "Day/month/year is a regional format.",
       2: "Month-day-year is the US convention, not ISO.",
       3: "Written-out months are for people, not a standard exchange format."},
      "ISO 8601 writes dates as YYYY-MM-DD, which is unambiguous and sorts correctly as text.",
      "Syllabus 1.2.3", ["dates", "standardization"]),

    # ---------- 1.2.4 Cleaning techniques ----------
    Q("b1-060", "1.2.4", 2,
      "What does this bucketization print?",
      ["`['young', 'young', 'mid', 'senior']`",
       "`['young', 'mid', 'mid', 'senior']`",
       "`['young', 'young', 'mid', 'mid']`",
       "`['young', 'mid', 'mid', 'mid']`"],
      0,
      {1: "Bins are right-closed, so 30 belongs to (0, 30], the \"young\" band.",
       2: "65 is above 64, so it falls in (64, 120], \"senior\".",
       3: "30 is included in the first bin and 65 in the last."},
      "`pd.cut` intervals are right-closed by default: (0, 30], (30, 64], (64, 120]. So 18 and 30 are young, 31 is mid and 65 is senior.",
      "Syllabus 1.2.4 · pandas: cut", ["bucketization", "cut"],
      code="""
      import pandas as pd

      ages = pd.Series([18, 30, 31, 65])
      bands = pd.cut(ages, bins=[0, 30, 64, 120], labels=["young", "mid", "senior"])
      print(bands.tolist())
      """, verify="stdout"),

    Q("b1-061", "1.2.4", 2,
      "What does this conversion print?",
      ["`22.5`", "`nan`", "`21.5`", "A ValueError is raised"],
      0,
      {1: "pandas' `sum` skips NaN by default.",
       2: "12 + 7.5 + 3 is 22.5.",
       3: "`errors=\"coerce\"` turns \"n/a\" into NaN instead of raising."},
      "`errors=\"coerce\"` converts unparseable text to NaN, and `sum` skips NaN: 12 + 7.5 + 3 = 22.5.",
      "Syllabus 1.2.4 · pandas: to_numeric", ["to-numeric", "cleaning"],
      code="""
      import pandas as pd

      s = pd.Series(["12", "7.5", "n/a", "3"])
      print(pd.to_numeric(s, errors="coerce").sum())
      """, verify="stdout"),

    Q("b1-062", "1.2.4", 2,
      "What happens when this code runs?",
      ["A ValueError is raised", "It returns `[12.0, 7.5, nan]`", "It returns `[12.0, 7.5, 0.0]`", "A TypeError is raised"],
      0,
      {1: "Only `pd.to_numeric(..., errors=\"coerce\")` silently produces NaN.",
       2: "pandas never substitutes 0 for text it can't parse.",
       3: "The type (string) is acceptable for conversion; the value \"n/a\" is not, so it's a ValueError."},
      "`astype(float)` fails on the first string it can't parse, raising ValueError: could not convert string to float.",
      "Syllabus 1.2.4 · pandas: Series.astype", ["astype", "errors"],
      code="""
      import pandas as pd

      s = pd.Series(["12", "7.5", "n/a"])
      s.astype(float)
      """, verify="raises:ValueError"),

    Q("b1-063", "1.2.4", 2,
      "Which column names does this print?",
      ["`['id', 'color_blue', 'color_red']`",
       "`['id', 'color', 'color_blue', 'color_red']`",
       "`['color_blue', 'color_red']`",
       "`['id', 'blue', 'red']`"],
      0,
      {1: "The original `color` column is replaced, not kept.",
       2: "Columns not listed in `columns=` (such as `id`) are kept.",
       3: "pandas prefixes the new columns with the original column name."},
      "`get_dummies` replaces `color` with one indicator column per category, named `<column>_<value>` and sorted: `color_blue`, `color_red`.",
      "Syllabus 1.2.4 · pandas: get_dummies", ["one-hot", "get-dummies"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"id": [1, 2, 3], "color": ["red", "blue", "red"]})
      print(list(pd.get_dummies(df, columns=["color"]).columns))
      """, verify="stdout"),

    Q("b1-064", "1.2.4", 2,
      "How many missing values does the normalized column contain?",
      ["`1`", "`0`", "`2`", "`4`"],
      0,
      {1: "\"maybe\" has no key in the mapping dict.",
       2: "\"Yes\" and \"Y\" become \"yes\" and \"y\" after `lower()`, which are both mapped.",
       3: "Three of the four values are mapped."},
      "`map` with a dict returns NaN for any value that isn't a key. After lowercasing, only \"maybe\" is unmapped.",
      "Syllabus 1.2.4 · pandas: Series.map", ["boolean-normalization", "map"],
      code="""
      import pandas as pd

      s = pd.Series(["Yes", "no", "Y", "maybe"])
      clean = s.str.lower().map({"yes": True, "y": True, "no": False, "n": False})
      print(clean.isna().sum())
      """, verify="stdout"),

    Q("b1-065", "1.2.4", 2,
      "An analyst wants four spending groups, each containing roughly the same number of customers. Which call does that?",
      ["`pd.qcut(df[\"spend\"], q=4)`", "`pd.cut(df[\"spend\"], bins=4)`", "`df[\"spend\"].rank()`", "`pd.get_dummies(df[\"spend\"])`"],
      0,
      {1: "`cut` with `bins=4` makes four equal-width ranges; skewed spending would put most customers in one bin.",
       2: "Ranking orders customers but doesn't create groups.",
       3: "One-hot encoding a continuous column creates one column per distinct value."},
      "`qcut` bins by quantiles, so each of the four groups holds about a quarter of the customers.",
      "Syllabus 1.2.4 · pandas: qcut", ["bucketization", "qcut"]),

    Q("b1-066", "1.2.4", 3,
      "When is excluding data a better choice than imputing it? Select two.",
      ["The target variable itself is missing for those rows",
       "A column is 85% empty and nothing reliable can estimate its values",
       "2% of a feature is missing at random and related columns predict it well",
       "The rows with gaps are the only examples of a rare class",
       "The column's mean can be calculated"],
      [0, 1],
      {2: "Few, predictable gaps are the ideal case for imputation.",
       3: "Dropping the only rare-class examples would cripple the analysis; impute instead.",
       4: "Being able to compute a mean says nothing about whether imputing is sensible."},
      "Exclude when imputation would invent answers (a missing target) or when there is too little information to estimate values (a mostly empty column).",
      "Syllabus 1.2.4", ["imputation", "exclusion"]),

    # ---------- 1.3.1 Validation ----------
    Q("b1-070", "1.3.1", 1,
      "A rule states that a booking's `end_date` must be on or after its `start_date`. Which type of validation check is this?",
      ["Cross-field check", "Cross-reference check", "Range check", "Type check"],
      0,
      {1: "Cross-reference checks look a value up in another dataset.",
       2: "A range check compares one field with fixed limits.",
       3: "A type check confirms the kind of value, not how two fields relate."},
      "Comparing two fields within the same record is a cross-field check.",
      "Syllabus 1.3.1", ["validation", "cross-field"]),

    Q("b1-071", "1.3.1", 1,
      "Every `product_code` in the sales file must exist in the product master list. Which check enforces this?",
      ["Cross-reference check", "Cross-field check", "Format check", "Range check"],
      0,
      {1: "Cross-field checks compare fields inside the same record.",
       2: "A code can have the right format and still not exist in the master list.",
       3: "Codes aren't numeric limits."},
      "Looking a value up in another dataset is a cross-reference (referential) check, the job a foreign key does in a database.",
      "Syllabus 1.3.1", ["validation", "cross-reference"]),

    Q("b1-072", "1.3.1", 2,
      "Which row positions does this validation flag?",
      ["`[1, 2]`", "`[2]`", "`[1]`", "`[0, 3]`"],
      0,
      {1: "Row 1 fails too: a quantity of 0 is outside 1 to 10.",
       2: "Row 2 fails both rules (quantity 12, price −2).",
       3: "Rows 0 and 3 pass both rules."},
      "Row 1 has qty 0 (out of range) and row 2 has qty 12 and a negative price. `~between(1, 10)` OR `price <= 0` flags rows 1 and 2.",
      "Syllabus 1.3.1 · pandas: Series.between", ["validation", "range-check"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"qty": [3, 0, 12, 7], "price": [9.5, 4.0, -2.0, 15.0]})
      bad = ~df["qty"].between(1, 10) | (df["price"] <= 0)
      print(df.index[bad].tolist())
      """, verify="stdout"),

    Q("b1-073", "1.3.1", 2,
      "Why add type checks at the very start of a data ingestion script?",
      ["A bad file fails immediately, before its errors spread into joins, aggregates and reports",
       "Type checks make the script run faster",
       "Type checks replace the need for range checks",
       "Type checks convert every column to the right type automatically"],
      0,
      {1: "Checks add a little work; their value is catching problems, not speed.",
       2: "A correctly typed value can still be out of range.",
       3: "A check detects problems; converting is a separate step."},
      "Validating early (fail fast) stops bad input at the door, where the cause is obvious, instead of letting it corrupt later results.",
      "Syllabus 1.3.1", ["validation", "fail-fast"]),

    Q("b1-074", "1.3.1", 3,
      "What does this validation code print?",
      ["`['ok', 'type', 'range', 'ok']`",
       "`['ok', 'type', 'range', 'type']`",
       "`['ok', 'ok', 'range', 'type']`",
       "`['ok', 'type', 'type', 'type']`"],
      0,
      {1: "`bool` is a subclass of `int`, so `isinstance(True, int)` is True and True (1) is within 0–120.",
       2: "The string \"42\" is not an int, so it fails the type check.",
       3: "130 is an int; it fails the range check, not the type check."},
      "42 passes; \"42\" is a str (type); 130 is an int outside 0–120 (range); True counts as the int 1, so it passes both checks, a known gap in naive type checks.",
      "Syllabus 1.3.1", ["validation", "isinstance"],
      code="""
      def validate(row):
          if not isinstance(row["age"], int):
              return "type"
          if not 0 <= row["age"] <= 120:
              return "range"
          return "ok"

      rows = [{"age": 42}, {"age": "42"}, {"age": 130}, {"age": True}]
      print([validate(r) for r in rows])
      """, verify="stdout"),

    # ---------- 1.3.2 Integrity ----------
    Q("b1-080", "1.3.2", 1,
      "Which constraint enforces referential integrity between an `orders` table and a `customers` table?",
      ["FOREIGN KEY", "PRIMARY KEY", "CHECK", "DEFAULT"],
      0,
      {1: "A primary key identifies rows uniquely within one table (entity integrity).",
       2: "CHECK restricts a column's values (domain integrity).",
       3: "DEFAULT supplies a value when none is given."},
      "A foreign key requires every referenced customer to exist in the customers table.",
      "Syllabus 1.3.2", ["integrity", "foreign-key"]),

    Q("b1-081", "1.3.2", 1,
      "Which statement best describes data integrity?",
      ["Data stays accurate, complete, consistent and reliable throughout its life cycle",
       "Data is encrypted while stored",
       "Data can be retrieved quickly",
       "Data takes up as little storage as possible"],
      0,
      {1: "Encryption is a security measure; encrypted data can still be wrong.",
       2: "Speed is performance, not correctness.",
       3: "Compact storage says nothing about correctness."},
      "Integrity is about correctness over time: data changes only through valid, authorized operations.",
      "Syllabus 1.3.2", ["integrity", "definitions"]),

    Q("b1-082", "1.3.2", 3,
      "Customer 99 does not exist. What does this code print?",
      ["`1`", "`0`", "An IntegrityError is raised", "An OperationalError is raised"],
      0,
      {1: "The insert succeeds, so the table has one row.",
       2: "SQLite only enforces foreign keys after `PRAGMA foreign_keys = ON`.",
       3: "The SQL is valid, so no OperationalError occurs."},
      "SQLite ignores FOREIGN KEY constraints unless the connection runs `PRAGMA foreign_keys = ON`, so the orphan order is inserted.",
      "Syllabus 1.3.2 · SQLite docs: foreign key support", ["integrity", "sqlite"],
      code="""
      import sqlite3

      con = sqlite3.connect(":memory:")
      con.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY)")
      con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, "
                  "customer_id INTEGER REFERENCES customers(id))")
      con.execute("INSERT INTO orders VALUES (1, 99)")
      print(con.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
      """, verify="stdout"),

    Q("b1-083", "1.3.2", 2,
      "A script moves stock between warehouses with one UPDATE that subtracts and another that adds. It crashes between the two statements. What prevents the totals from becoming inconsistent?",
      ["Running both updates in one transaction and committing only after both succeed",
       "A CHECK constraint on the quantity column",
       "An index on the warehouse column",
       "Running `SELECT DISTINCT` after the updates"],
      0,
      {1: "CHECK validates individual values; it can't tie two updates together.",
       2: "Indexes speed up lookups; they don't make changes atomic.",
       3: "A query after the fact can't undo half a transfer."},
      "Transactions are atomic: either both updates are committed, or a failure rolls both back.",
      "Syllabus 1.3.2", ["transactions", "acid"]),

    Q("b1-084", "1.3.2", 2,
      "Which two constraints help maintain domain integrity for an order quantity column? Select two.",
      ["`NOT NULL`", "`CHECK (qty > 0)`", "`FOREIGN KEY`", "`ORDER BY qty`", "`LIMIT 1`"],
      [0, 1],
      {2: "A foreign key protects references between tables, not the quantity's domain.",
       3: "ORDER BY sorts query results; it isn't a constraint.",
       4: "LIMIT restricts how many rows a query returns."},
      "Domain integrity keeps values in their allowed set: NOT NULL requires a value and CHECK enforces a rule on it.",
      "Syllabus 1.3.2", ["integrity", "constraints"]),

    # ---------- 1.4.1 File formats ----------
    Q("b1-090", "1.4.1", 1,
      "What does this code print?",
      ["`False None list`", "`false null list`", "`False None tuple`", "`0 None list`"],
      0,
      {1: "`json.loads` converts JSON `false` and `null` to Python `False` and `None`.",
       2: "JSON arrays become Python lists, never tuples.",
       3: "JSON `false` becomes the boolean `False`, not the integer 0."},
      "JSON → Python: false → False, null → None, array → list.",
      "Syllabus 1.4.1 · Python docs: json", ["json", "types"],
      code="""
      import json

      record = json.loads('{"id": 7, "active": false, "tags": ["a", "b"], "score": null}')
      print(record["active"], record["score"], type(record["tags"]).__name__)
      """, verify="stdout"),

    Q("b1-091", "1.4.1", 2,
      "What does this code print?",
      ["`{\"point\": [1, 2], \"ok\": true}`", "`{\"point\": (1, 2), \"ok\": True}`", "`{'point': [1, 2], 'ok': True}`", "A TypeError is raised"],
      0,
      {1: "JSON has no tuples and writes booleans in lowercase.",
       2: "That is Python's own dict notation; JSON uses double quotes.",
       3: "Tuples are serializable; they become arrays."},
      "`json.dumps` writes tuples as JSON arrays, `True` as `true`, and uses double-quoted keys.",
      "Syllabus 1.4.1 · Python docs: json", ["json", "serialization"],
      code="""
      import json

      print(json.dumps({"point": (1, 2), "ok": True}))
      """, verify="stdout"),

    Q("b1-092", "1.4.1", 2,
      "What does this code print?",
      ["`8 Tea`", "`35 Tea`", "`8 A1`", "`2 Tea`"],
      0,
      {1: "The attributes are converted with `int()` before summing, so 3 + 5 = 8, not string concatenation.",
       2: "`.text` is the element's content (\"Tea\"); the sku is an attribute.",
       3: "The sum adds the qty attributes, not the number of items."},
      "`findall(\"item\")` returns both items; `get(\"qty\")` reads each attribute (3 and 5); `find(\"item\").text` is the first item's content.",
      "Syllabus 1.4.1 · Python docs: xml.etree.ElementTree", ["xml", "elementtree"],
      code="""
      import xml.etree.ElementTree as ET

      xml = "<shop><item sku='A1' qty='3'>Tea</item><item sku='B2' qty='5'>Coffee</item></shop>"
      root = ET.fromstring(xml)
      print(sum(int(i.get("qty")) for i in root.findall("item")), root.find("item").text)
      """, verify="stdout"),

    Q("b1-093", "1.4.1", 1,
      "Which function reads JSON from an open file object?",
      ["`json.load(f)`", "`json.loads(f)`", "`json.dump(f)`", "`json.dumps(f)`"],
      0,
      {1: "`loads` parses a string, not a file object.",
       2: "`dump` writes an object to a file.",
       3: "`dumps` converts an object to a JSON string."},
      "`load` / `dump` work with files; `loads` / `dumps` work with strings.",
      "Syllabus 1.4.1 · Python docs: json", ["json", "file-io"]),

    Q("b1-094", "1.4.1", 2,
      "What does this code print?",
      ["`3 Smith, Jane`", "`3 \"Smith`", "`4 Smith`", "`2 Smith, Jane`"],
      0,
      {1: "The csv module honours quotes, so the comma inside the quotes doesn't split the field.",
       2: "The quoted field stays one field, so there are 3 rows and the name is complete.",
       3: "The header row is also returned by `csv.reader`, giving 3 rows."},
      "`csv.reader` returns the header plus two data rows, and keeps the quoted \"Smith, Jane\" as one field.",
      "Syllabus 1.4.1 · Python docs: csv", ["csv", "quoting"],
      code="""
      import csv
      import io

      data = 'name,city\\n"Smith, Jane",Oslo\\nLee,Rome\\n'
      rows = list(csv.reader(io.StringIO(data)))
      print(len(rows), rows[1][0])
      """, verify="stdout"),

    Q("b1-095", "1.4.1", 1,
      "A supplier sends a product feed where categories contain products, and each product carries attributes such as `sku` and `currency`. Which format is designed for this kind of tagged, hierarchical data?",
      ["XML", "CSV", "TXT", "A single-sheet spreadsheet"],
      0,
      {1: "CSV is flat: one table of rows and columns.",
       2: "Plain text has no structure at all.",
       3: "A sheet is a flat grid; nesting would have to be flattened."},
      "XML represents a tree of nested elements with attributes, which is exactly this structure.",
      "Syllabus 1.4.1", ["xml", "file-formats"]),

    # ---------- 1.4.2 Accessing datasets ----------
    Q("b1-100", "1.4.2", 2,
      "What happens when this code runs?",
      ["A ValueError is raised", "It prints the row where `a` is 2", "It prints the rows where `a` is 2 and 3", "A TypeError is raised"],
      0,
      {1: "`and` needs a single True/False, so it never reaches the filtering step.",
       2: "The code fails before any filtering happens.",
       3: "The error is about an ambiguous truth value, which pandas reports as ValueError."},
      "Python's `and` asks for the truth value of a whole Series, which is ambiguous, so pandas raises ValueError. Use `&` with parentheses.",
      "Syllabus 1.4.2 · pandas: boolean indexing", ["filtering", "boolean-mask"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
      print(df[df["a"] > 1 and df["b"] < 6])
      """, verify="raises:ValueError"),

    Q("b1-101", "1.4.2", 2,
      "What does this code print?",
      ["`[90, 70, 50, 20]`", "`[70, 90, 20, 50]`", "`[50, 20, 90, 70]`", "`[20, 50, 70, 90]`"],
      0,
      {1: "`total` is sorted descending within each region.",
       2: "EU sorts before US because region is ascending.",
       3: "That is a single ascending sort on `total`."},
      "Region sorts A→Z (EU, then US) and, within each region, `total` sorts high to low: EU 90, 70; US 50, 20.",
      "Syllabus 1.4.2 · pandas: DataFrame.sort_values", ["sorting", "pandas"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"region": ["US", "EU", "EU", "US"], "total": [50, 70, 90, 20]})
      print(df.sort_values(["region", "total"], ascending=[True, False])["total"].tolist())
      """, verify="stdout"),

    Q("b1-102", "1.4.2", 1,
      "An open-data portal publishes a CSV at a public URL. How can pandas load it in one step?",
      ["`pd.read_csv(\"https://…/air_quality.csv\")`",
       "`pd.read_sql(\"https://…/air_quality.csv\")`",
       "`pd.read_html(\"https://…/air_quality.csv\")`",
       "`pd.DataFrame(\"https://…/air_quality.csv\")`"],
      0,
      {1: "`read_sql` runs a query against a database connection.",
       2: "`read_html` looks for `<table>` elements in HTML, not CSV text.",
       3: "The constructor would treat the URL as a single string value."},
      "`pd.read_csv` accepts URLs as well as local paths, so online repositories can be read directly.",
      "Syllabus 1.4.2 · pandas: read_csv", ["read-csv", "online-data"]),

    Q("b1-103", "1.4.2", 2,
      "How many rows does this filter return?",
      ["`3`", "`2`", "`1`", "`4`"],
      0,
      {1: "APAC also qualifies because its sales exceed 100.",
       2: "Both EU rows qualify through the region condition.",
       3: "The US row fails both conditions."},
      "EU 120 and EU 95 match `region == 'EU'`; APAC 130 matches `sales > 100`; US 80 matches neither. Three rows.",
      "Syllabus 1.4.2 · pandas: DataFrame.query", ["filtering", "query"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"region": ["EU", "US", "EU", "APAC"], "sales": [120, 80, 95, 130]})
      print(len(df.query("region == 'EU' or sales > 100")))
      """, verify="stdout"),

    Q("b1-104", "1.4.2", 2,
      "Monthly temperatures for three cities are stored with one row per city and one column per month. Which layout is tidy?",
      ["One row per city and month, with columns `city`, `month` and `temperature`",
       "One row per month, with one column per city",
       "One row per city, with one column per month (as now)",
       "One row holding every value, with a column per city-month pair"],
      0,
      {1: "Cities as columns spreads one variable (city) across column names.",
       2: "Month values in column names mean one variable is stored as headers.",
       3: "A single row hides both variables in column names."},
      "Tidy data has each variable as a column and each observation (a city in a month) as a row.",
      "Syllabus 1.4.2", ["tidy-data", "organization"]),

    # ---------- 1.4.3 Extracting data ----------
    Q("b1-110", "1.4.3", 3,
      "What does this parsing code print?",
      ["`[2.5, 3.1]`", "`[2.5]`", "`['2.50', '3.10']`", "An AttributeError is raised"],
      0,
      {1: "`class_=\"item\"` also matches an element whose classes are \"item sale\".",
       2: "Each price is converted with `float()`.",
       3: "Both matched items contain a price span, so `find` never returns None."},
      "BeautifulSoup matches `class_=\"item\"` against each of an element's classes, so both list items match; their prices convert to 2.5 and 3.1. The note isn't an item.",
      "Syllabus 1.4.3 · Beautiful Soup docs: searching by CSS class", ["beautifulsoup", "html"],
      code="""
      from bs4 import BeautifulSoup

      html = '''<ul>
        <li class="item">Tea <span class="price">2.50</span></li>
        <li class="item sale">Coffee <span class="price">3.10</span></li>
        <li class="note">Prices in EUR</li>
      </ul>'''
      soup = BeautifulSoup(html, "html.parser")
      prices = [float(li.find("span", class_="price").get_text())
                for li in soup.find_all("li", class_="item")]
      print(prices)
      """, verify="stdout"),

    Q("b1-111", "1.4.3", 1,
      "An API starts returning HTTP status 429. What does it mean, and what should the client do?",
      ["Too many requests: slow down and retry later, respecting any Retry-After header",
       "Not found: fix the URL",
       "Unauthorized: supply valid credentials",
       "Server error: the request was fine, so retry immediately in a tight loop"],
      0,
      {1: "\"Not found\" is 404.",
       2: "Missing or invalid credentials give 401.",
       3: "Server errors are 5xx, and hammering the server makes things worse."},
      "429 Too Many Requests signals a rate limit; back off before retrying.",
      "Syllabus 1.4.3", ["http", "rate-limiting"]),

    Q("b1-112", "1.4.3", 2,
      "A request to an API endpoint returns 404. What does `resp = requests.get(url)` do?",
      ["Returns a Response whose `status_code` is 404; no exception is raised unless you call `resp.raise_for_status()`",
       "Raises an HTTPError immediately",
       "Returns None",
       "Retries automatically until it succeeds"],
      0,
      {1: "requests only raises for HTTP error codes when you call `raise_for_status()`.",
       2: "`get` always returns a Response object when the server answers.",
       3: "requests doesn't retry failed status codes by default."},
      "HTTP errors are data, not exceptions, in requests: check `status_code` or call `raise_for_status()`.",
      "Syllabus 1.4.3 · requests docs", ["requests", "http"]),

    Q("b1-113", "1.4.3", 1,
      "Where is a site's robots.txt, and what does it do?",
      ["At the root of the domain; it lists paths that automated crawlers are asked not to visit",
       "In each page's HTML head; it technically blocks all scrapers",
       "In the API documentation; it holds the API key",
       "In the sitemap; it lists the prices of all products"],
      0,
      {1: "robots.txt is a separate file at the site root and doesn't block anything by force.",
       2: "API keys are never published in robots.txt.",
       3: "A sitemap lists URLs; robots.txt lists crawl rules."},
      "robots.txt (e.g. https://example.com/robots.txt) uses `Disallow:` lines to tell crawlers what not to fetch. It is a convention that ethical scrapers respect.",
      "Syllabus 1.4.3", ["robots-txt", "ethics"]),

    Q("b1-114", "1.4.3", 2,
      "Which two practices make a web-scraping project more ethical? Select two.",
      ["Pausing between requests so the server isn't overloaded",
       "Using the site's official API when one exists",
       "Spoofing a browser to get past blocks",
       "Ignoring robots.txt because the pages are public",
       "Collecting personal data from user profiles for later use"],
      [0, 1],
      {2: "Evading blocks overrides the owner's choice and may breach terms of service.",
       3: "Public doesn't mean unrestricted; robots.txt states the owner's wishes.",
       4: "Personal data needs a lawful basis and a clear purpose."},
      "Rate-limiting protects the site, and an official API is the sanctioned route to the data.",
      "Syllabus 1.4.3", ["web-scraping", "ethics"]),

    Q("b1-115", "1.4.3", 2,
      "What does this code print?",
      ["`a 2 None`", "`a 2 []`", "`ab 3 None`", "`a 1 None`"],
      0,
      {1: "`find` returns None when there's no match; only `find_all` returns an empty list.",
       2: "`find` returns only the first `<p>`, and `find_all(\"p\")` ignores the `<div>`.",
       3: "`find_all` returns every `<p>`, and there are two."},
      "`find` returns the first match (\"a\"), `find_all` returns a list of all matches (2 paragraphs), and `find` gives None when nothing matches.",
      "Syllabus 1.4.3 · Beautiful Soup docs", ["beautifulsoup", "find"],
      code="""
      from bs4 import BeautifulSoup

      soup = BeautifulSoup("<p>a</p><p>b</p><div>c</div>", "html.parser")
      print(soup.find("p").get_text(), len(soup.find_all("p")), soup.find("span"))
      """, verify="stdout"),

    Q("b1-116", "1.4.3", 1,
      "A page contains three HTML tables. What does `pd.read_html(page_html)` return?",
      ["A list of three DataFrames", "One DataFrame with all tables stacked", "A dict keyed by table id", "A BeautifulSoup object"],
      0,
      {1: "Tables are returned separately, never stacked.",
       2: "It returns a list, in page order.",
       3: "It parses tables into DataFrames, not a soup object."},
      "`pd.read_html` returns a list with one DataFrame per `<table>` found.",
      "Syllabus 1.4.3 · pandas: read_html", ["read-html", "html"]),

    # ---------- 1.4.4 Spreadsheets ----------
    Q("b1-120", "1.4.4", 1,
      "A tax rate sits in cell B1. The formula `=A2*B1` in C2 gives wrong results when filled down to C3:C100. What should C2 contain?",
      ["`=A2*$B$1`", "`=$A$2*B1`", "`=A2*B$2`", "`=SUM(A2:B1)`"],
      0,
      {1: "Locking A2 would multiply the same first value in every row.",
       2: "B$2 points at row 2, not the rate in row 1.",
       3: "SUM of a range isn't a multiplication by the rate."},
      "An absolute reference ($B$1) stays fixed when the formula is copied, while the relative A2 moves to A3, A4…",
      "Syllabus 1.4.4", ["spreadsheets", "absolute-reference"]),

    Q("b1-121", "1.4.4", 1,
      "Column D holds order statuses. Which formula counts how many orders are \"Late\"?",
      ["`=COUNTIF(D:D, \"Late\")`", "`=COUNT(D:D)`", "`=COUNTA(D:D)`", "`=SUM(D:D)`"],
      0,
      {1: "COUNT counts numeric cells; statuses are text.",
       2: "COUNTA counts every non-empty cell, whatever the status.",
       3: "SUM adds numbers; it can't count text values."},
      "COUNTIF counts cells that meet a condition.",
      "Syllabus 1.4.4", ["spreadsheets", "formulas"]),

    Q("b1-122", "1.4.4", 2,
      "Which two layout choices make a sheet easiest to sort, filter and read with `pd.read_excel`? Select two.",
      ["A single header row in the first row",
       "No merged cells and no blank rows inside the data",
       "A subtotal row inserted after every ten orders",
       "Colour-coding late orders instead of using a status column",
       "A two-row header with merged group labels"],
      [0, 1],
      {2: "Subtotal rows mix summaries with records and break sorting and imports.",
       3: "Colour isn't data; it is lost on import and can't be filtered by formulas.",
       4: "Multi-row, merged headers need special handling to import."},
      "One header row and a continuous block of records (no merges, no gaps) is the layout tools read without surprises.",
      "Syllabus 1.4.4", ["spreadsheets", "layout"]),

    Q("b1-123", "1.4.4", 2,
      "Cells formatted to one decimal show 3.1, but each holds 3.14159. What does `=SUM` of ten such cells return?",
      ["31.4159, using the stored values", "31.0, using the displayed values", "An error, because formats differ", "31, rounded to an integer"],
      0,
      {1: "Formatting changes appearance only; calculations use the full stored value.",
       2: "Formatting never causes calculation errors.",
       3: "No rounding happens unless a formula rounds."},
      "Number formatting is cosmetic: formulas use the underlying values (the result then displays with the cell's format).",
      "Syllabus 1.4.4", ["spreadsheets", "formatting"]),

    # ---------- 1.4.5 Preparing data ----------
    Q("b1-130", "1.4.5", 2,
      "What does this code print?",
      ["`(9, 3)`", "`(3, 4)`", "`(9, 4)`", "`(3, 9)`"],
      0,
      {1: "That's the original wide shape.",
       2: "Melting keeps one id column plus the new `quarter` and `sales` columns: three.",
       3: "Rows multiply (3 stores × 3 quarters); columns shrink."},
      "`melt` turns 3 stores × 3 quarter columns into 9 rows, with columns store, quarter and sales.",
      "Syllabus 1.4.5 · pandas: DataFrame.melt", ["melt", "reshaping"],
      code="""
      import pandas as pd

      wide = pd.DataFrame({"store": ["A", "B", "C"],
                           "Q1": [5, 3, 4], "Q2": [6, 2, 7], "Q3": [4, 4, 5]})
      long = wide.melt(id_vars="store", var_name="quarter", value_name="sales")
      print(long.shape)
      """, verify="stdout"),

    Q("b1-131", "1.4.5", 2,
      "An analyst standardizes all 10,000 rows with `StandardScaler().fit_transform(X)`, then splits them 80/20 into training and test sets. What is the problem?",
      ["The scaler learned the mean and standard deviation from test rows too, leaking information into training",
       "StandardScaler cannot be used before a split",
       "The split should be 50/50",
       "Standardization removes outliers from the test set"],
      0,
      {1: "It can be used, but must be fitted on training rows only.",
       2: "80/20 is a normal split; the size isn't the issue.",
       3: "Standardization rescales values; it removes nothing."},
      "Fitting any preprocessing on all data before splitting is data leakage; split first, fit on training data, then transform both.",
      "Syllabus 1.4.5, 4.2.2", ["data-leakage", "train-test-split"]),

    Q("b1-132", "1.4.5", 2,
      "Only 5% of transactions in a dataset are fraud. Which `train_test_split` argument keeps that 5% share in both the training and test sets?",
      ["`stratify=y`", "`shuffle=False`", "`random_state=42`", "`test_size=0.05`"],
      0,
      {1: "Turning off shuffling doesn't balance classes; it can make it worse.",
       2: "`random_state` makes the split reproducible, not proportional.",
       3: "This sets the test set to 5% of rows, not the fraud share."},
      "`stratify=y` splits within each class, preserving class proportions in both sets.",
      "Syllabus 1.4.5 · scikit-learn: train_test_split", ["train-test-split", "stratify"]),

    Q("b1-133", "1.4.5", 2,
      "A model will forecast daily demand. How should the data be split for testing?",
      ["Train on earlier dates and test on later dates, without shuffling",
       "Shuffle all days, then take a random 20% as the test set",
       "Use every other day for testing",
       "Test on the same days used for training"],
      0,
      {1: "Shuffling lets the model train on days after the ones it's tested on: leakage from the future.",
       2: "Interleaved days still let the model see the future around each test day.",
       3: "Testing on training data measures memorization, not forecasting."},
      "Time series must be split by time so that evaluation mimics forecasting the unknown future.",
      "Syllabus 1.4.5, 4.2.2", ["time-series", "train-test-split"]),

    Q("b1-134", "1.4.5", 2,
      "Store A has two January rows. What happens when this code runs?",
      ["A ValueError is raised", "It returns 5 for store A", "It returns 12 for store A", "It returns 6 for store A"],
      0,
      {1: "`pivot` doesn't pick one of the duplicates.",
       2: "`pivot` doesn't aggregate; that would need `pivot_table(aggfunc=\"sum\")`.",
       3: "Averaging duplicates is `pivot_table`'s default, not `pivot`'s behaviour."},
      "`pivot` requires each index/column pair to be unique; duplicates raise ValueError (\"Index contains duplicate entries\"). Use `pivot_table` to aggregate them.",
      "Syllabus 1.4.5 · pandas: DataFrame.pivot", ["pivot", "reshaping"],
      code="""
      import pandas as pd

      long = pd.DataFrame({"store": ["A", "A", "B"],
                           "month": ["Jan", "Jan", "Jan"],
                           "sales": [5, 7, 3]})
      long.pivot(index="store", columns="month", values="sales")
      """, verify="raises:ValueError"),

    Q("b1-135", "1.4.5", 2,
      "Forty rows have label 0 and ten have label 1. What does this code print?",
      ["`10 2`", "`10 5`", "`5 1`", "`10 0`"],
      0,
      {1: "Stratifying keeps the 20% share of class 1: 2 of the 10 test rows.",
       2: "`test_size=0.2` of 50 rows is 10 rows.",
       3: "With stratification, class 1 must appear in the test set in proportion."},
      "The test set gets 20% of 50 = 10 rows, and stratification keeps 20% of them (2) in class 1.",
      "Syllabus 1.4.5 · scikit-learn: train_test_split", ["train-test-split", "stratify"],
      code="""
      from sklearn.model_selection import train_test_split

      X = list(range(50))
      y = [0] * 40 + [1] * 10
      X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
      print(len(X_te), sum(y_te))
      """, verify="stdout"),

    Q("b1-136", "1.4.5", 1,
      "An analyst is asked to prepare customer data for a churn dashboard. What should they clarify first?",
      ["The business question and how the stakeholders define churn and the time frame",
       "Which chart colours to use",
       "Whether to use pandas or SQL",
       "How to scale every numeric column"],
      0,
      {1: "Styling comes long after deciding what the data must show.",
       2: "Tools follow from the task, not the other way round.",
       3: "Scaling may not even be needed for a dashboard."},
      "Preparation follows the objective: the definition of churn and the decision it supports determine which columns, filters and periods matter.",
      "Syllabus 1.4.5", ["stakeholders", "preparation"]),
]
