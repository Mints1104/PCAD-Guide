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

- **Univariate**: one variable (a histogram of heights).
- **Bivariate**: two variables together (height and weight); described by both means, both spreads and their correlation; a bivariate normal looks like an elliptical cloud in a scatter plot.
- **Multivariate**: three or more variables; a multivariate normal is described by a mean vector and a covariance matrix.

Simulated samples show the rules of thumb in the table:

```python
import numpy as np

rng = np.random.default_rng(0)
normal = rng.normal(loc=50, scale=10, size=100_000)
uniform = rng.uniform(low=0, high=12, size=100_000)

print(round(normal.mean(), 1), round(np.median(normal), 1), round(normal.std(), 1))
print(round(np.mean(np.abs(normal - 50) < 10), 2), round(np.mean(np.abs(normal - 50) < 20), 2))  # ~68%, ~95%
print(round(uniform.mean(), 1), round(uniform.var(), 1))   # (0 + 12) / 2 = 6 and 12**2 / 12 = 12
```

```text
50.0 50.0 10.0
0.68 0.95
6.0 11.9
```

About 68% of the normal values are within one standard deviation (10) of the mean and 95% within two. The uniform sample's mean and variance are close to the formulas: (0 + 12) / 2 = 6 and 12² / 12 = 12.

**Confidence.** The **standard error** of the mean is s / √n: it shrinks as the sample grows. A 95% **confidence interval** for the mean is roughly mean ± 1.96 × SE for large samples (use the t-distribution for small ones). It means: if we repeated the sampling many times, about 95% of intervals built this way would contain the true mean. It does not mean there is a 95% chance this particular interval contains it. Intervals get wider with more variability, smaller samples, or a higher confidence level.

A standard error and a 95% interval from a sample of 10:

```python
import numpy as np

sample = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13])
mean = sample.mean()
se = sample.std(ddof=1) / np.sqrt(len(sample))           # standard error = s / sqrt(n)
print(round(mean, 2), round(se, 3))
print(round(mean - 1.96 * se, 2), round(mean + 1.96 * se, 2))   # approximate 95% interval

bigger = np.tile(sample, 4)                               # same values, 4 times the n
print(round(bigger.std(ddof=1) / np.sqrt(len(bigger)), 3))     # smaller SE, narrower interval
```

```text
13.5 0.5
12.52 14.48
0.24
```

With four times the data (and the same spread), the standard error roughly halves, because it divides by √n.

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

- Positive r: as one goes up, the other tends to go up. Negative r: as one goes up, the other tends to go down.
- r has no units and doesn't change if you rescale a variable (metres to centimetres).
- It is sensitive to outliers: one extreme point can create or hide a correlation.
- **Correlation is not causation**: a third variable (a confounder) can drive both.
- In simple linear regression, r² is the share of the variance in y explained by x.

```python
import pandas as pd

df = pd.DataFrame({"ads": [1, 2, 3, 4, 5], "sales": [3, 5, 7, 9, 11], "returns": [9, 7, 6, 3, 1]})
print(df.corr().round(2))
```

```text
          ads  sales  returns
ads      1.00   1.00    -0.99
sales    1.00   1.00    -0.99
returns -0.99  -0.99     1.00
```

`df.corr()` uses Pearson by default (`method="spearman"` ranks first, for monotonic but non-linear relationships). `s1.corr(s2)`, `np.corrcoef(x, y)` and `scipy.stats.pearsonr(x, y)` (which also returns a p-value) do the same.

Rescaling, an outlier, a curve, and Pearson versus Spearman:

```python
import pandas as pd

df = pd.DataFrame({"height_m": [1.60, 1.65, 1.70, 1.75, 1.80],
                   "weight": [55, 60, 62, 70, 72]})
print(round(df["height_m"].corr(df["weight"]), 3))
print(round((df["height_m"] * 100).corr(df["weight"]), 3))      # in cm: r is unchanged

x = pd.Series([1, 2, 3, 4, 5, 6])
y = pd.Series([2, 1, 3, 2, 1, 2])
print(round(x.corr(y), 2))
y_out = pd.Series([2, 1, 3, 2, 1, 20])                           # one extreme point
print(round(x.corr(y_out), 2))

x = pd.Series([-2, -1, 0, 1, 2])
print(round(x.corr(x ** 2), 2))                                   # perfect curve, r = 0
s = pd.Series([1, 2, 3, 4, 5])
print(round(s.corr(s ** 3), 3), round(s.corr(s ** 3, method="spearman"), 3)) # monotonic: Spearman = 1
```

```text
0.982
0.982
-0.07
0.64
0.0
0.943 1.0
```

Converting metres to centimetres leaves r at 0.982. One extreme point lifts a near-zero r to 0.64. y = x² is a perfect curve but r = 0. For y = x³, Pearson is below 1 because the points are not on a straight line, while Spearman, which only checks that the ranks rise together, gives exactly 1.

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

- `.coef_` holds the slopes, `.intercept_` the intercept; `LinearRegression.score()` returns R², while `LogisticRegression.score()` returns accuracy.
- `predict_proba` returns one column per class (here P(fail), P(pass)); `predict` applies the 0.5 threshold.
- `np.polyfit(x, y, 1)` returns `[slope, intercept]` for a straight line; `scipy.stats.linregress` and statsmodels' `OLS` / `Logit` add p-values and confidence intervals.

The same straight line as the `LinearRegression` example, from `polyfit`:

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
slope, intercept = np.polyfit(x, y, 1)
print(round(slope, 2), round(intercept, 2))
print(round(slope * 6 + intercept, 2))      # prediction for x = 6
```

```text
1.97 1.09
12.91
```

- R² is the share of variance in y the model explains (0 to 1 on training data for OLS). A high R² does not prove the model is right: check residuals.

**Choosing.** Ask what the outcome is. A quantity → linear. A yes/no → logistic (despite its name, it is a classification method). More than two categories → multinomial logistic regression.

**Limitations and biases.** Both are sensitive to outliers and to omitted variables (a missing confounder biases the coefficients); both find association, not causation; extrapolating beyond the range of the training data is unreliable; linear regression used on a 0/1 target can predict impossible values below 0 or above 1; many predictors relative to observations leads to overfitting.

### Exam traps

> **Trap.** Predicting whether a customer will churn is logistic; predicting how much they will spend is linear.

> **Trap.** A logistic coefficient is not a change in probability. It is a change in log-odds; exponentiate it for the odds ratio.
