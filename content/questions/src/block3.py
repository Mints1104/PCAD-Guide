from qhelp import Q

QUESTIONS = [
    # ---------- 3.1.1 Measures and distributions ----------
    Q("b3-001", "3.1.1", 2,
      "What does this code print?",
      ["`10 5 3`", "`5 5 3`", "`10 7 3`", "`10 5 40`"],
      0,
      {1: "The mean is pulled up by 40: 70 / 7 = 10.",
       2: "The median of 7 sorted values is the 4th: 5.",
       3: "The mode is the most frequent value, 3, not the largest."},
      "Mean = 70 / 7 = 10; median = the middle of 7 sorted values = 5; mode = the most frequent value = 3. The outlier 40 lifts the mean well above the median.",
      "Syllabus 3.1.1 · Python docs: statistics", ["mean", "median", "mode"],
      code="""
      import statistics as st

      data = [2, 3, 3, 5, 7, 10, 40]
      print(st.mean(data), st.median(data), st.mode(data))
      """, verify="stdout"),

    Q("b3-002", "3.1.1", 2,
      "In a company, the mean salary is 72,000 and the median salary is 51,000. What does this suggest about the distribution?",
      ["It is right-skewed: a few very high salaries pull the mean up",
       "It is left-skewed: a few very low salaries pull the mean down",
       "It is symmetric",
       "Half the employees earn more than 72,000"],
      0,
      {1: "Left skew would put the mean below the median.",
       2: "In a symmetric distribution the mean and median are close.",
       3: "Half earn more than the median (51,000), not the mean."},
      "When the mean is well above the median, a long right tail of large values is pulling the mean upward.",
      "Syllabus 3.1.1", ["skew", "mean-vs-median"]),

    Q("b3-003", "3.1.1", 2,
      "What does this code print?",
      ["`5.0 6.667`", "`6.667 5.0`", "`5.0 5.0`", "`2.236 2.582`"],
      0,
      {1: "NumPy defaults to the population formula (divide by n); pandas uses n − 1.",
       2: "pandas' `var` uses ddof=1, so it differs from NumPy's default.",
       3: "Those are standard deviations; the code asks for variances."},
      "The squared deviations from the mean 5 sum to 20. NumPy divides by n = 4 (5.0); pandas divides by n − 1 = 3 (6.667).",
      "Syllabus 3.1.1, 4.2.1", ["variance", "ddof"],
      code="""
      import numpy as np
      import pandas as pd

      x = [4, 8, 6, 2]
      print(np.var(x), round(pd.Series(x).var(), 3))
      """, verify="stdout"),

    Q("b3-004", "3.1.1", 2,
      "Delivery times are normally distributed with mean 30 minutes and standard deviation 5 minutes. About what share of deliveries take between 20 and 40 minutes?",
      ["About 95%", "About 68%", "About 99.7%", "About 50%"],
      0,
      {1: "68% lies within one standard deviation: 25 to 35 minutes.",
       2: "99.7% lies within three standard deviations: 15 to 45 minutes.",
       3: "50% is the share on either side of the mean."},
      "20 to 40 is the mean ± 2 standard deviations, which covers about 95% of a normal distribution.",
      "Syllabus 3.1.1", ["normal-distribution", "empirical-rule"]),

    Q("b3-005", "3.1.1", 2,
      "Values are drawn from a uniform distribution on the interval [2, 8]. Which statement is true?",
      ["Every value between 2 and 8 is equally likely, and the mean is 5",
       "Values near 5 are most likely, and the mean is 5",
       "About 68% of values fall within one standard deviation of the mean, as in a normal distribution",
       "The mean is 8, the upper bound"],
      0,
      {1: "A peak in the middle describes a normal (bell-shaped) distribution, not a flat one.",
       2: "The 68-95-99.7 rule applies to normal distributions.",
       3: "The mean is the midpoint (a + b) / 2."},
      "A uniform distribution is flat: all values in [a, b] are equally likely and the mean is (a + b) / 2 = 5.",
      "Syllabus 3.1.1", ["uniform-distribution", "distributions"]),

    Q("b3-006", "3.1.1", 3,
      "A study reports a 95% confidence interval of [48.2, 51.8] for a population mean. Which interpretation is correct?",
      ["If the sampling were repeated many times, about 95% of intervals built this way would contain the true mean",
       "There is a 95% probability that the true mean lies in [48.2, 51.8]",
       "95% of individual values lie between 48.2 and 51.8",
       "The sample mean is wrong 5% of the time"],
      0,
      {1: "The true mean is fixed; the probability statement describes the method, not this particular interval.",
       2: "A confidence interval is about the mean, not the spread of individual values.",
       3: "The interval quantifies uncertainty; it doesn't say the sample mean is wrong."},
      "Confidence describes the long-run success rate of the procedure that produces the intervals.",
      "Syllabus 3.1.1", ["confidence-interval", "interpretation"]),

    Q("b3-007", "3.1.1", 2,
      "Which two changes make a confidence interval for a mean narrower? Select two.",
      ["Collecting a larger sample", "Using a 90% instead of a 95% confidence level", "Measuring a more variable population", "Using a 99% confidence level", "Rounding the data to whole numbers"],
      [0, 1],
      {2: "More variability widens the interval.",
       3: "Higher confidence requires a wider interval.",
       4: "Rounding doesn't reduce uncertainty; it adds a little error."},
      "The width is roughly 2 × z × s / √n: a larger n or a smaller z (lower confidence) narrows it.",
      "Syllabus 3.1.1", ["confidence-interval", "standard-error"]),

    Q("b3-008", "3.1.1", 1,
      "The heights and weights of 500 adults are studied together, for example in a scatter plot. What kind of distribution is being examined?",
      ["Bivariate", "Univariate", "Uniform", "Categorical"],
      0,
      {1: "Univariate means one variable at a time.",
       2: "Uniform describes a shape, not how many variables are involved.",
       3: "Height and weight are numeric, not categories."},
      "Two variables considered jointly form a bivariate distribution; three or more make it multivariate.",
      "Syllabus 3.1.1", ["bivariate", "distributions"]),

    # ---------- 3.1.2 Relationships ----------
    Q("b3-010", "3.1.2", 1,
      "Pearson's r between hours of overtime and job-satisfaction score is −0.85. How is this best described?",
      ["A strong negative linear relationship", "A weak negative relationship", "No relationship", "A strong positive relationship"],
      0,
      {1: "|r| = 0.85 is strong.",
       2: "Values near 0 mean no linear relationship; −0.85 is far from 0.",
       3: "The sign is negative: as overtime rises, satisfaction tends to fall."},
      "The sign gives the direction (negative) and the size gives the strength (0.85 is strong).",
      "Syllabus 3.1.2", ["pearson", "correlation"]),

    Q("b3-011", "3.1.2", 2,
      "What does this code print?",
      ["`-1.0`", "`1.0`", "`0.0`", "`-2.0`"],
      0,
      {1: "y falls as x rises, so the correlation is negative.",
       2: "The points lie exactly on a straight line.",
       3: "r is bounded between −1 and 1; the slope is −2, but r is not the slope."},
      "y = 12 − 2x is a perfect decreasing straight line, so r = −1. r measures how tightly points follow a line, not the slope.",
      "Syllabus 3.1.2 · pandas: Series.corr", ["pearson", "correlation"],
      code="""
      import pandas as pd

      df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [10, 8, 6, 4, 2]})
      print(round(df["x"].corr(df["y"]), 2))
      """, verify="stdout"),

    Q("b3-012", "3.1.2", 3,
      "What does this code print?",
      ["`0.0`", "`1.0`", "`-1.0`", "`0.5`"],
      0,
      {1: "y depends on x perfectly, but not linearly.",
       2: "Nothing in the relationship is decreasing overall.",
       3: "The symmetric U-shape cancels out any linear trend completely."},
      "y = x² over symmetric x is a perfect U-shaped relationship, yet Pearson's r is 0 because r only measures linear association. Always look at the scatter plot.",
      "Syllabus 3.1.2 · NumPy: corrcoef", ["pearson", "non-linear"],
      code="""
      import numpy as np

      x = np.array([-3, -2, -1, 0, 1, 2, 3])
      y = x ** 2
      print(round(np.corrcoef(x, y)[0, 1], 2))
      """, verify="stdout"),

    Q("b3-013", "3.1.2", 1,
      "Which correlation coefficient shows the strongest linear relationship?",
      ["−0.82", "0.45", "0.10", "0.60"],
      0,
      {1: "0.45 is moderate.",
       2: "0.10 is very weak.",
       3: "0.60 is weaker than 0.82 in absolute value."},
      "Strength is the absolute value of r; the sign only gives the direction.",
      "Syllabus 3.1.2", ["pearson", "strength"]),

    Q("b3-014", "3.1.2", 2,
      "In side-by-side box plots of weekly sales, store A's box is much taller than store B's, but their median lines are at the same height. What does this show?",
      ["Both stores have the same typical week, but store A's sales vary much more",
       "Store A sells more on average",
       "Store B has more outliers",
       "Store A has more weeks of data"],
      0,
      {1: "Equal medians show similar typical sales; the box height shows spread, not level.",
       2: "Outliers appear as individual points beyond the whiskers, which the description doesn't mention.",
       3: "Box plots don't show the number of observations."},
      "The median line is the centre; the box height is the IQR, the spread of the middle 50%.",
      "Syllabus 3.1.2", ["box-plot", "interpretation"]),

    Q("b3-015", "3.1.2", 2,
      "A dataset shows r = 0.8 between daily ice-cream sales and swimming accidents. Which conclusion is justified?",
      ["The two are associated, probably because hot weather drives both",
       "Ice cream causes swimming accidents",
       "Swimming accidents cause people to buy ice cream",
       "The correlation must be a data error"],
      0,
      {1: "Correlation alone can't establish causation.",
       2: "Reversing the direction is just as unsupported.",
       3: "A real confounder explains the pattern; nothing suggests an error."},
      "Correlation is not causation: a confounder (temperature) can drive both variables.",
      "Syllabus 3.1.2, 5.2.2", ["causation", "confounder"]),

    Q("b3-016", "3.1.2", 1,
      "Why is every cell on the diagonal of a correlation heatmap equal to 1?",
      ["Each variable is perfectly correlated with itself",
       "The diagonal shows the number of variables",
       "The diagonal is set to 1 by the colour palette",
       "It shows that all variables are strongly related"],
      0,
      {1: "The diagonal holds correlations, not counts.",
       2: "Palettes only colour the values; they don't change them.",
       3: "The diagonal says nothing about relationships between different variables."},
      "The diagonal compares each variable with itself, so r = 1. The matrix is also symmetric: corr(a, b) = corr(b, a).",
      "Syllabus 3.1.2", ["heatmap", "correlation-matrix"]),

    Q("b3-017", "3.1.2", 2,
      "Which two charts best reveal outliers in a single numeric variable? Select two.",
      ["Box plot", "Histogram", "Pie chart", "Line chart of category totals", "Correlation heatmap"],
      [0, 1],
      {2: "Pie charts show parts of a whole, not a distribution.",
       3: "Category totals hide individual values.",
       4: "A heatmap of correlations summarizes relationships between variables."},
      "Box plots mark outliers explicitly; histograms show isolated bars far from the rest.",
      "Syllabus 3.1.2", ["outliers", "charts"]),

    # ---------- 3.2.1 Bootstrapping ----------
    Q("b3-020", "3.2.1", 1,
      "What is a bootstrap resample of a dataset with n observations?",
      ["n observations drawn from the dataset with replacement",
       "n observations drawn from the dataset without replacement",
       "Half of the observations, chosen at random",
       "n new observations collected from the population"],
      0,
      {1: "Without replacement, you just get the same data reshuffled.",
       2: "The resample keeps the original size.",
       3: "Bootstrapping reuses the existing sample; it collects nothing new."},
      "Drawing n values with replacement means some observations repeat and others are left out, which imitates drawing a fresh sample.",
      "Syllabus 3.2.1", ["bootstrapping", "resampling"]),

    Q("b3-021", "3.2.1", 2,
      "A colleague's bootstrap produces this output. What does it print, and why is the approach useless?",
      ["`{10.0}`: without replacement every resample is the original data reshuffled, so every mean is identical",
       "A set of many different means, which is a correct bootstrap distribution",
       "`{0.0}`, because `choice` returns zeros without replacement",
       "A ValueError, because `size` must be smaller than the data"],
      0,
      {1: "`replace=False` with size equal to n just permutes the data.",
       2: "`choice` returns values from `data`, never zeros.",
       3: "Sampling all 5 values without replacement is allowed."},
      "With `replace=False` and `size=n`, each resample contains exactly the original values, so the mean is always 10.0 and there's no variability to measure. Use `replace=True`.",
      "Syllabus 3.2.1 · NumPy: Generator.choice", ["bootstrapping", "replacement"],
      code="""
      import numpy as np

      rng = np.random.default_rng(1)
      data = np.array([3, 5, 8, 13, 21])
      means = {float(rng.choice(data, size=5, replace=False).mean()) for _ in range(1000)}
      print(means)
      """, verify={"py": "assert run_py(code) == '{10.0}'"}),

    Q("b3-022", "3.2.1", 2,
      "`boot` holds 5,000 bootstrap medians. Which line gives a 95% percentile confidence interval?",
      ["`np.percentile(boot, [2.5, 97.5])`", "`np.percentile(boot, [5, 95])`", "`(np.min(boot), np.max(boot))`", "`np.mean(boot) + [-1, 1] * np.std(boot)`"],
      0,
      {1: "The 5th and 95th percentiles give a 90% interval.",
       2: "The extremes cover 100% and are driven by chance resamples.",
       3: "±1 standard deviation covers about 68%, and adding a list to a number doesn't work as written."},
      "A 95% percentile interval cuts 2.5% from each tail of the bootstrap distribution.",
      "Syllabus 3.2.1", ["bootstrapping", "percentile-interval"]),

    Q("b3-023", "3.2.1", 2,
      "Which scenario is best suited to bootstrapping?",
      ["Estimating the uncertainty of the median delivery time from 200 independent, right-skewed observations",
       "Estimating a population mean from a sample of 4 values",
       "Estimating national sales trends from one store's data",
       "Estimating uncertainty in daily stock prices by resampling days at random"],
      0,
      {1: "Four values can only recombine into a handful of resamples; the result is unreliable.",
       2: "A biased, unrepresentative sample stays biased after resampling.",
       3: "Resampling days at random breaks the time dependence between days."},
      "Bootstrapping works well for statistics without a simple formula (like the median) when the sample is reasonably large, representative and independent.",
      "Syllabus 3.2.1", ["bootstrapping", "appropriateness"]),

    Q("b3-024", "3.2.1", 3,
      "An analyst gets a wide bootstrap interval from 60 observations and raises the number of resamples from 2,000 to 200,000 to narrow it. What happens?",
      ["The interval barely changes: its width depends on the original sample, not on the number of resamples",
       "The interval becomes about 10 times narrower",
       "The interval becomes 100 times narrower",
       "The interval becomes wider"],
      0,
      {1: "More resamples only reduce simulation noise.",
       2: "Resampling the same data can't add information.",
       3: "More resamples don't widen it either; they stabilize it."},
      "The bootstrap can't create information: only a larger (representative) sample narrows the interval.",
      "Syllabus 3.2.1", ["bootstrapping", "reliability"]),

    Q("b3-025", "3.2.1", 1,
      "Which variable is continuous?",
      ["Delivery time measured in minutes and seconds", "Number of items in an order", "Number of complaints per week", "Number of children in a household"],
      0,
      {1: "Item counts are discrete: whole numbers only.",
       2: "Counts of complaints are discrete.",
       3: "Counts of children are discrete."},
      "Continuous data can take any value within a range; counts are discrete.",
      "Syllabus 3.2.1", ["continuous-data", "discrete-data"]),

    # ---------- 3.2.2 Regression ----------
    Q("b3-030", "3.2.2", 1,
      "A subscription company wants to predict whether each customer will cancel next month (yes or no). Which model fits?",
      ["Logistic regression", "Linear regression", "k-means clustering", "Principal component analysis"],
      0,
      {1: "Linear regression predicts a continuous number.",
       2: "k-means groups unlabeled data; it doesn't predict a known label.",
       3: "PCA reduces dimensions; it doesn't classify."},
      "A binary outcome calls for logistic regression, which predicts the probability of the positive class.",
      "Syllabus 3.2.2", ["logistic-regression", "model-choice"]),

    Q("b3-031", "3.2.2", 1,
      "A marketing team wants to predict next month's revenue in euros from advertising spend. Which model fits?",
      ["Linear regression", "Logistic regression", "A decision about the chart type", "A crosstab"],
      0,
      {1: "Logistic regression predicts probabilities of classes, not amounts.",
       2: "Chart choice isn't a model.",
       3: "A crosstab counts category combinations."},
      "Revenue is a continuous target, so linear regression is the natural choice.",
      "Syllabus 3.2.2", ["linear-regression", "model-choice"]),

    Q("b3-032", "3.2.2", 2,
      "A fitted model is: price = 50,000 + 1,200 × area_m2 + 8,000 × has_garage. What does 1,200 mean?",
      ["Each extra square metre is associated with a 1,200 higher price, holding garage status constant",
       "Every house costs at least 1,200",
       "1,200 square metres is the average area",
       "The model explains 1,200 units of variance"],
      0,
      {1: "The baseline value is the intercept, 50,000.",
       2: "Coefficients are effects per unit, not averages.",
       3: "Explained variance is measured by R², not by coefficients."},
      "A coefficient is the expected change in the outcome per one-unit increase in that predictor, with the others held fixed.",
      "Syllabus 3.2.2", ["coefficients", "interpretation"]),

    Q("b3-033", "3.2.2", 2,
      "What does this code print?",
      ["`2.0 1.0`", "`1.0 2.0`", "`2.0 3.0`", "`0.5 1.0`"],
      0,
      {1: "`polyfit` returns the highest power first: slope, then intercept.",
       2: "y = 2x + 1, so the intercept is 1.",
       3: "y rises by 2 for each step in x."},
      "The points lie on y = 2x + 1. `np.polyfit(x, y, 1)` returns [slope, intercept].",
      "Syllabus 3.2.2 · NumPy: polyfit", ["linear-regression", "polyfit"],
      code="""
      import numpy as np

      x = np.array([1, 2, 3, 4])
      y = np.array([3, 5, 7, 9])
      slope, intercept = np.polyfit(x, y, 1)
      print(round(slope, 2), round(intercept, 2))
      """, verify="stdout"),

    Q("b3-034", "3.2.2", 3,
      "What does this code print?",
      ["`(1, 2) [0 1]`", "`(1,) [0 1]`", "`(2, 1) [0 1]`", "`(1, 2) [0.2 0.8]`"],
      0,
      {1: "`predict_proba` returns one column per class, even for one sample.",
       2: "The shape is (samples, classes): one sample, two classes.",
       3: "`predict` returns class labels; probabilities come from `predict_proba`."},
      "`predict_proba` gives an array of shape (n_samples, n_classes); `predict` applies the 0.5 threshold and returns labels.",
      "Syllabus 3.2.2 · scikit-learn: LogisticRegression", ["logistic-regression", "predict-proba"],
      code="""
      import numpy as np
      from sklearn.linear_model import LogisticRegression

      X = np.array([[1], [2], [3], [7], [8], [9]])
      y = np.array([0, 0, 0, 1, 1, 1])
      model = LogisticRegression().fit(X, y)
      proba = model.predict_proba([[5]])
      print(proba.shape, model.predict([[2], [8]]))
      """, verify="stdout"),

    Q("b3-035", "3.2.2", 2,
      "A residual plot of a linear regression shows a funnel: residuals spread wider as fitted values grow. Which assumption is violated?",
      ["Equal variance of residuals (homoscedasticity)", "Linearity", "Independence of observations", "No missing values"],
      0,
      {1: "A curved pattern in residuals signals non-linearity; a funnel signals changing spread.",
       2: "Independence problems show up as patterns over time or groups, not as a funnel.",
       3: "Missing values aren't a regression assumption visible in a residual plot."},
      "Residuals whose spread changes with the fitted values are heteroscedastic, violating the equal-variance assumption.",
      "Syllabus 3.2.2", ["assumptions", "residuals"]),

    Q("b3-036", "3.2.2", 1,
      "A linear regression reports R² = 0.81. What does that mean?",
      ["The model explains 81% of the variance in the target on this data",
       "The model is correct 81% of the time",
       "The correlation between each predictor and the target is 0.81",
       "81% of the predictors are significant"],
      0,
      {1: "Accuracy is a classification measure; R² is about explained variance.",
       2: "R² describes the whole model, not each predictor's correlation.",
       3: "R² says nothing about individual predictors' significance."},
      "R² is the share of the target's variance explained by the model.",
      "Syllabus 3.2.2", ["r-squared", "model-fit"]),

    Q("b3-037", "3.2.2", 3,
      "A linear model trained on houses of 50 to 200 m² is used to price a 900 m² mansion. What is the main concern?",
      ["Extrapolation: the relationship may not hold far outside the training range",
       "Multicollinearity between area and price",
       "The intercept becomes negative",
       "Logistic regression should have been used"],
      0,
      {1: "Multicollinearity is about predictors correlated with each other, not with the target.",
       2: "Nothing suggests the intercept changes.",
       3: "Price is continuous, so linear regression is the right family."},
      "Regression estimates are only reliable within the range of the data they were fitted on.",
      "Syllabus 3.2.2", ["limitations", "extrapolation"]),

    Q("b3-038", "3.2.2", 3,
      "Which two statements about logistic regression are true? Select two.",
      ["It outputs probabilities between 0 and 1",
       "It models the log-odds of the outcome as a linear function of the predictors",
       "It is fitted by minimizing the sum of squared residuals",
       "It requires normally distributed residuals",
       "It predicts continuous values such as revenue"],
      [0, 1],
      {2: "Logistic regression is fitted by maximum likelihood; least squares is linear regression.",
       3: "Normal residuals are a linear-regression assumption.",
       4: "It predicts class probabilities, not continuous amounts."},
      "Logistic regression applies the sigmoid to a linear score (the log-odds), producing probabilities, and is fitted by maximum likelihood.",
      "Syllabus 3.2.2", ["logistic-regression", "theory"]),
]
