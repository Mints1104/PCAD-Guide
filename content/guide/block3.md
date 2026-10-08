# Block 3: Statistical Analysis

Block 3 is the smallest block: 4 items, 8.3% of the exam, one per objective. It covers descriptive statistics and distributions, correlation and chart reading, bootstrapping, and when to use linear vs logistic regression. The same ideas return in Block 4 as pandas and scikit-learn code, so time spent here pays twice.

## 3.1.1 Understand and apply statistical measures

**Syllabus asks:** central tendency (mean, median, mode); spread (standard deviation, variance); Gaussian and uniform distributions in univariate, bivariate and multivariate settings; measures of confidence.

### Core facts

| Measure | What it is | Sensitive to outliers? |
|---|---|---|
| Mean | Sum ÷ count | Yes |
| Median | Middle value of the sorted data (mean of the two middle values when n is even) | No |
| Mode | Most frequent value; the only average for nominal categories | No |
| Range | max − min | Very |
| Variance | Average squared distance from the mean | Yes |
| Standard deviation | √variance, in the data's own units | Yes |
| IQR | Q3 − Q1, the spread of the middle 50% | No |

**Population vs sample.** Population variance divides by N; sample variance divides by **n − 1** (Bessel's correction), because a sample underestimates spread. The `ddof` argument ("delta degrees of freedom") sets the divisor to n − ddof.

```python
import numpy as np
import pandas as pd
import statistics as st

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(st.mean(data), st.median(data), st.mode(data))
print(np.std(data), round(pd.Series(data).std(), 4))       # NumPy: ddof=0; pandas: ddof=1
print(st.pstdev(data), round(st.stdev(data), 4))           # population vs sample
```

```text
5 4.5 4
2.0 2.1381
2.0 2.1381
```

**Skew.** In right-skewed data (a long tail of high values, such as incomes or house prices) the mean is pulled above the median. In left-skewed data the mean is below the median. In symmetric data they are close.

**Distributions.**

| | Gaussian (normal) | Uniform |
|---|---|---|
| Shape | Symmetric bell curve | Flat: every value in [a, b] equally likely |
| Parameters | Mean μ, standard deviation σ | Lower bound a, upper bound b |
| Centre | Mean = median = mode | Mean = (a + b) / 2 |
| Spread | ~68% within 1σ, ~95% within 2σ, ~99.7% within 3σ | Variance = (b − a)² / 12 |
| NumPy | `rng.normal(loc=μ, scale=σ, size=n)` | `rng.uniform(low=a, high=b, size=n)` |

**One, two or many variables.**

- **Univariate** means looking at one variable on its own, for example a histogram of heights.
- **Bivariate** means two variables together, such as height and weight. You describe each one's centre and spread, plus how they move together (their correlation). Two normally distributed variables that are correlated form an oval-shaped cloud in a scatter plot.
- **Multivariate** means three or more variables. A multivariate normal distribution is described by the mean of each variable plus a table (the covariance matrix) of how each pair moves together.

**Seeing the rules in simulated data.** NumPy can generate random numbers from a distribution, which is a good way to check the table above. `rng.normal(loc=50, scale=10, ...)` draws from a normal distribution with mean 50 and standard deviation 10:

```python
import numpy as np

rng = np.random.default_rng(0)               # a random generator with a fixed seed
heights = rng.normal(loc=50, scale=10, size=100_000)

print(round(heights.mean(), 1), round(np.median(heights), 1))
print(round(np.mean(abs(heights - 50) < 10), 2))   # share within 1 standard deviation
print(round(np.mean(abs(heights - 50) < 20), 2))   # share within 2 standard deviations
```

```text
50.0 50.0
0.68
0.95
```

The mean and median are both 50 because the curve is symmetric. About 68% of values fall within one standard deviation (40 to 60), and 95% within two (30 to 70).

A uniform distribution makes every value in a range equally likely. Its mean is the midpoint, (a + b) / 2, and its variance is (b − a)² / 12:

```python
import numpy as np

rng = np.random.default_rng(0)
waits = rng.uniform(low=0, high=12, size=100_000)

print(round(waits.mean(), 1))      # (0 + 12) / 2 = 6
print(round(waits.var(), 1))       # 12 ** 2 / 12 = 12
```

```text
6.0
12.0
```

Both are close to the formulas. A random sample never matches exactly.

**Confidence: how sure is a sample mean?** You usually measure a sample, not everyone, so the sample mean is only an estimate of the true (population) mean. Two ideas describe how good that estimate is.

**Standard error.** The **standard error** (SE) of the mean is the sample's standard deviation divided by the square root of the sample size: s / √n. It measures how much the sample mean would vary if you took many samples. Bigger samples give a smaller SE.

```python
import numpy as np

sample = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13])

mean = sample.mean()
s = sample.std(ddof=1)                 # sample standard deviation
se = s / np.sqrt(len(sample))          # n = 10

print(round(mean, 2), round(s, 3), round(se, 3))
```

```text
13.5 1.581 0.5
```

**A 95% confidence interval.** For a large sample, a 95% confidence interval for the mean is roughly the mean ± 1.96 standard errors. (For small samples like this one, a slightly wider multiplier from the t-distribution is more accurate; the idea is the same.)

```python
import numpy as np

sample = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13])
mean = sample.mean()
se = sample.std(ddof=1) / np.sqrt(len(sample))

print(round(mean - 1.96 * se, 2), "to", round(mean + 1.96 * se, 2))
```

```text
12.52 to 14.48
```

**What "95% confident" means.** If you repeated the sampling many times and built an interval each time, about 95% of those intervals would contain the true mean. It does **not** mean there is a 95% chance that this particular interval contains it.

**What makes an interval wider or narrower.**

- **More data** makes it narrower, because SE divides by √n.
- **More variable data** makes it wider, because SE multiplies by s.
- **A higher confidence level** makes it wider: 99% uses about 2.58 standard errors instead of 1.96.

```python
import numpy as np

sample = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13])
bigger = np.tile(sample, 4)            # the same values repeated: 4 times the data, same spread

for data in (sample, bigger):
    se = data.std(ddof=1) / np.sqrt(len(data))
    print(len(data), "values: SE =", round(se, 3))
```

```text
10 values: SE = 0.5
40 values: SE = 0.24
```

Four times the data roughly halves the standard error, because √4 = 2.

### Exam traps

> **Trap.** `np.std(x)` divides by n (ddof=0); `pd.Series(x).std()` divides by n − 1 (ddof=1). Same data, different answers.

> **Trap.** With outliers or skew, the median describes a "typical" value better than the mean.

> **Trap.** A 99% confidence interval is **wider** than a 95% one from the same data.

## 3.1.2 Analyze and evaluate data relationships

**Syllabus asks:** identify and evaluate outliers; positive and negative correlation with Pearson's r; interpret box plots, histograms, scatter plots, line plots and correlation heatmaps.

### Core facts

**Pearson's r** measures the strength and direction of a **linear** relationship between two numeric variables. It runs from −1 to +1.

| r | Reading |
|---|---|
| +1 / −1 | Perfect positive / negative straight line |
| around ±0.7 or beyond | Strong |
| around ±0.3 to ±0.7 | Moderate |
| near 0 | No **linear** relationship (a curved one may still exist) |

**Positive and negative.** A positive r means that as one variable goes up, the other tends to go up too. A negative r means that as one goes up, the other tends to go down. `df.corr()` shows r for every pair of columns:

```python
import pandas as pd

df = pd.DataFrame({"ads": [1, 2, 3, 4, 5],
                   "sales": [3, 5, 7, 9, 11],
                   "returns": [9, 7, 6, 3, 1]})
print(df.corr().round(2))
```

```text
          ads  sales  returns
ads      1.00   1.00    -0.99
sales    1.00   1.00    -0.99
returns -0.99  -0.99     1.00
```

More ads go with more sales (r = 1.00, a perfect straight line) and with fewer returns (r = −0.99). Each column correlates perfectly with itself, so the diagonal is all 1s.

`df.corr()` uses Pearson's r by default. For two single columns, `df["ads"].corr(df["sales"])` gives the same number; `np.corrcoef(x, y)` and `scipy.stats.pearsonr(x, y)` (which also gives a p-value) work too.

**Units don't matter.** r has no units, so converting a column (metres to centimetres, say) doesn't change it:

```python
import pandas as pd

height_m = pd.Series([1.60, 1.65, 1.70, 1.75, 1.80])
weight = pd.Series([55, 60, 62, 70, 72])

print(round(height_m.corr(weight), 3))
print(round((height_m * 100).corr(weight), 3))     # heights in centimetres
```

```text
0.982
0.982
```

**One outlier can create a correlation.** These two variables have almost no relationship until a single extreme point is added:

```python
import pandas as pd

x = pd.Series([1, 2, 3, 4, 5, 6])
y = pd.Series([2, 1, 3, 2, 1, 2])
print(round(x.corr(y), 2))

y_with_outlier = pd.Series([2, 1, 3, 2, 1, 20])    # the last value is extreme
print(round(x.corr(y_with_outlier), 2))
```

```text
-0.07
0.64
```

One point moved r from about 0 to a moderate 0.64. Always look at a scatter plot before trusting r.

**r = 0 doesn't mean "unrelated".** r only measures **straight-line** relationships. Here y is completely determined by x (y = x²), yet r is 0, because the points form a U shape:

```python
import pandas as pd

x = pd.Series([-2, -1, 0, 1, 2])
y = x ** 2
print(y.tolist())
print(round(x.corr(y), 2))
```

```text
[4, 1, 0, 1, 4]
0.0
```

**Pearson versus Spearman.** Spearman's correlation (`method="spearman"`) only asks whether the values **rise together in order**, not whether they form a straight line. For y = x³, y always goes up when x goes up, but along a curve:

```python
import pandas as pd

x = pd.Series([1, 2, 3, 4, 5])
y = x ** 3
print(round(x.corr(y), 3))                       # Pearson: not quite a straight line
print(round(x.corr(y, method="spearman"), 3))    # Spearman: perfectly in step
```

```text
0.943
1.0
```

**Correlation is not causation.** A third variable (a **confounder**) can drive both. Ice-cream sales and drownings rise together because hot weather increases both.

**r² in regression.** In simple linear regression, r² is the share of the variation in y that the line explains. r = 0.9 gives r² = 0.81, so the line explains 81% of the variation.

**Outliers.** Box plots show them as points beyond the whiskers (1.5 × IQR past the box). The z-score rule flags |z| > 3. Always ask whether an outlier is an error or a real, important case.

**Reading charts.**

| Chart | Shows | Look for |
|---|---|---|
| Box plot | Median (line), IQR (box), whiskers to 1.5 × IQR, outliers (points) | Centre, spread, skew (median off-centre, one long whisker), outliers; compare groups side by side |
| Histogram | Distribution of one numeric variable in bins | Shape (symmetric, skewed, bimodal), spread, gaps; bin width changes the picture |
| Scatter plot | Two numeric variables, one point per observation | Direction, form (linear or curved), strength, clusters, outliers |
| Line plot | A value over an ordered variable, usually time | Trend, seasonality, sudden changes |
| Correlation heatmap | Matrix of pairwise r, coloured | Strongest pairs; the diagonal is always 1; the matrix is symmetric; a diverging palette centred on 0 |

### Exam traps

> **Trap.** r = 0 does not mean "no relationship": y = x² over symmetric x has r ≈ 0 but a perfect curve.

> **Trap.** A strong correlation between ice-cream sales and drownings is driven by temperature; neither causes the other.

## 3.2.1 Understand and apply bootstrapping

**Syllabus asks:** the theory and statistical principles behind bootstrapping; discrete vs continuous data; when bootstrapping is appropriate; applying it in Python; judging how reliable and valid the result is.

### Core facts

**Bootstrapping** estimates how much a statistic would vary from sample to sample, using only the one sample you have:

<div class="dg"><p class="dg-title">The bootstrap loop</p><div class="dg-flow">
<div class="dg-step"><b>1. Resample</b><span>Draw n values from the sample <b>with replacement</b></span></div><div class="dg-arrow">→</div>
<div class="dg-step"><b>2. Compute</b><span>Calculate the statistic (mean, median, ratio…) on the resample</span></div><div class="dg-arrow">→</div>
<div class="dg-step"><b>3. Repeat</b><span>Thousands of times, e.g. 1,000 to 10,000</span></div><div class="dg-arrow">→</div>
<div class="dg-step"><b>4. Summarize</b><span>Std of the results = standard error; 2.5th and 97.5th percentiles = 95% CI</span></div>
</div></div>

The principle: the sample stands in for the population, so resampling from it imitates drawing new samples. Because it needs no formula and no assumption about the distribution's shape, it works for statistics with no simple standard-error formula (the median, a trimmed mean, a ratio, a correlation).

```python
import numpy as np

rng = np.random.default_rng(42)
delivery_days = np.array([2, 3, 3, 4, 5, 5, 6, 8, 12, 15])
boot_medians = [np.median(rng.choice(delivery_days, size=delivery_days.size, replace=True))
                for _ in range(5000)]
low, high = np.percentile(boot_medians, [2.5, 97.5])
print(np.median(delivery_days), low, high)
```

```text
5.0 3.0 9.0
```

`scipy.stats.bootstrap((data,), np.median, confidence_level=0.95)` does the same with better interval methods.

**Why with replacement?** Compare the two settings on the same small sample. Without replacement (`replace=False`), drawing all n values just shuffles the original data, so every resample has the same mean:

```python
import numpy as np

rng = np.random.default_rng(7)
data = np.array([2, 4, 6, 9, 14])
means = {float(rng.choice(data, size=5, replace=False).mean()) for _ in range(1000)}
print(means)
```

```text
{7.0}
```

With replacement (`replace=True`), some values are drawn twice and others not at all, so the means vary, which is the variation the bootstrap measures:

```python
import numpy as np

rng = np.random.default_rng(7)
data = np.array([2, 4, 6, 9, 14])
means = [float(rng.choice(data, size=5, replace=True).mean()) for _ in range(1000)]
print(len(set(means)), "different means, from", min(means), "to", max(means))
```

```text
45 different means, from 2.4 to 13.0
```

**When it fits.** The sample is representative and the observations are independent; the statistic is smooth (mean, median, proportion, correlation); the data are not normal or n is moderate. **When it doesn't.** Tiny samples (the resamples can only recombine a handful of values); extreme statistics such as the maximum; biased samples (bootstrapping reproduces the bias); dependent data such as time series (plain resampling breaks the order; block bootstrap exists for that).

**Discrete vs continuous data.** Discrete data take countable values (number of purchases, defects per batch); continuous data can take any value in a range (weight, time). Bootstrapping works with both, but with discrete data or small samples the bootstrap distribution is "lumpy": the median of 10 integer values can only land on a few values, so percentile intervals are coarse, as in the example.

**Reliability and validity.** More resamples reduce the random noise of the simulation but do not add information: the width of the interval is set by the original sample. A larger, representative sample is the only way to a narrower, more trustworthy interval.

### Exam traps

> **Trap.** Bootstrapping samples **with** replacement and keeps the resample the **same size** as the original. Without replacement, every resample is just a reshuffle of the same data.

> **Trap.** Bootstrapping cannot fix a biased or unrepresentative sample.

## 3.2.2 Explain linear and logistic regression

**Syllabus asks:** the theory, assumptions and mathematics of linear regression; logistic regression's concepts and use cases; choosing between them based on the data and the question; fitting them in Python; interpreting coefficients and fit statistics; limitations and biases.

### Core facts

| | Linear regression | Logistic regression |
|---|---|---|
| Target | Continuous number (price, demand, time) | Binary category (churn / stay, fraud / genuine) |
| Model | y = β₀ + β₁x₁ + … + ε | log(p / (1 − p)) = β₀ + β₁x₁ + …, so p = 1 / (1 + e^−z) |
| Output | Any real number | A probability between 0 and 1, turned into a class with a threshold (0.5 by default) |
| Fitting | Ordinary least squares: minimize the sum of squared residuals | Maximum likelihood |
| Coefficient β₁ | Change in y for a one-unit increase in x₁, others held constant | Change in the log-odds; e^β₁ is the odds ratio |
| Fit statistics | R², adjusted R², RMSE, MAE, residual plots | Accuracy, precision, recall, confusion matrix, ROC AUC, log loss |

**Linear regression assumptions (LINE).** **L**inearity between predictors and outcome; **I**ndependent errors; **N**ormally distributed residuals; **E**qual variance of residuals (homoscedasticity). Also: no strong multicollinearity among predictors. Logistic regression drops the normality and equal-variance assumptions but still needs independent observations and a linear relationship between predictors and the **log-odds**.

```python
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression

X = np.array([[1], [2], [3], [4], [5]])          # scikit-learn wants 2-D X
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
lin = LinearRegression().fit(X, y)
print(round(lin.coef_[0], 2), round(lin.intercept_, 2), round(lin.score(X, y), 3))

hours = np.array([[1], [2], [3], [4], [5], [6]])
passed = np.array([0, 0, 0, 1, 1, 1])
log = LogisticRegression().fit(hours, passed)
print(log.predict([[2], [5]]), log.predict_proba([[3.5]]).round(2))
```

```text
1.97 1.09 0.998
[0 1] [[0.5 0.5]]
```

**Reading a fitted line.** After `fit`, a `LinearRegression` model holds the line it found. `.coef_` is the slope (one per input column, so it's a list) and `.intercept_` is where the line crosses x = 0. The example above found y ≈ 1.97x + 1.09: each extra unit of x adds about 1.97 to y.

**R² and accuracy: what `.score()` returns.** The same method name means different things for the two models:

- `LinearRegression.score(X, y)` returns **R²**, the share of the variation in y the line explains. 0.998 above means almost all of it.
- `LogisticRegression.score(X, y)` returns **accuracy**, the share of predictions that were right.

A high R² doesn't prove the model is right. Check the residuals (actual minus predicted) for patterns too.

**Probabilities and classes in logistic regression.** `predict_proba` gives a probability for each class, one column per class: here P(fail) and P(pass). `predict` turns that into a class using a 0.5 cut-off.

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

hours = np.array([[1], [2], [3], [4], [5], [6]])
passed = np.array([0, 0, 0, 1, 1, 1])
model = LogisticRegression().fit(hours, passed)

print(model.predict_proba([[1], [6]]).round(2))   # [P(fail), P(pass)] for each student
print(model.predict([[1], [6]]))                  # the class with probability above 0.5
```

```text
[[0.94 0.06]
 [0.06 0.94]]
[0 1]
```

1 hour of study gives a high chance of failing, so the prediction is 0. 6 hours gives a high chance of passing, so the prediction is 1.

**A quick line with `np.polyfit`.** `np.polyfit(x, y, 1)` fits a straight line (degree 1) and returns `[slope, intercept]`. It needs no scikit-learn and takes plain 1-D lists:

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])

slope, intercept = np.polyfit(x, y, 1)
print(round(slope, 2), round(intercept, 2))      # the same line as LinearRegression found
print(round(slope * 6 + intercept, 2))           # predict y when x = 6
```

```text
1.97 1.09
12.91
```

`scipy.stats.linregress`, and statsmodels' `OLS` and `Logit`, also report p-values and confidence intervals for the coefficients.

**Choosing.** Ask what the outcome is. A quantity → linear. A yes/no → logistic (despite its name, it is a classification method). More than two categories → multinomial logistic regression.

**Limitations and biases.** Both are sensitive to outliers and to omitted variables (a missing confounder biases the coefficients); both find association, not causation; extrapolating beyond the range of the training data is unreliable; linear regression used on a 0/1 target can predict impossible values below 0 or above 1; many predictors relative to observations leads to overfitting.

### Exam traps

> **Trap.** Predicting whether a customer will churn is logistic; predicting how much they will spend is linear.

> **Trap.** A logistic coefficient is not a change in probability. It is a change in log-odds; exponentiate it for the odds ratio.
