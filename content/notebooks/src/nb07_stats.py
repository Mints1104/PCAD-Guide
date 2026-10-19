from nbhelp import NB, T

NOTEBOOK = NB(
    "stats", "Descriptive statistics with NumPy and pandas", 2, ["3.1.1", "3.1.2", "4.1.5", "4.2.1"],
    "Center and spread, IQR and z-score outliers, correlation, broadcasting and binned summaries.",
    """
    `times` holds ten task times in minutes, one of them suspiciously long. `df` records study hours, exam score and absences for ten students.
    """,
    """
    import numpy as np
    import pandas as pd

    times = np.array([12.0, 15.5, 11.2, 14.8, 13.1, 45.0, 12.7, 14.2, 13.9, 12.4])
    df = pd.DataFrame({
        "hours": [1, 2, 2, 3, 4, 5, 6, 6, 7, 8],
        "score": [52, 55, 61, 60, 68, 70, 75, 79, 80, 88],
        "absences": [9, 8, 8, 6, 5, 5, 3, 2, 2, 1],
    })
    """,
    [
        T("center-spread", "Mean, median and sample standard deviation",
          """
          Compute `mean_t`, `median_t` and `sd_t` for `times`, where `sd_t` is the **sample** standard deviation (divide by n − 1).
          Notice how far the mean is pulled from the median by the one long time.
          """,
          """
          mean_t = times.mean()
          median_t = None
          sd_t = times.std()
          """,
          """
          mean_t = times.mean()
          median_t = np.median(times)
          sd_t = times.std(ddof=1)
          """,
          """
          assert mean_t is not None and np.isclose(mean_t, 16.48), f"mean_t should be 16.48, got {mean_t}"
          assert median_t is not None and np.isclose(median_t, 13.5), f"median_t should be 13.5, got {median_t}"
          assert not np.isclose(sd_t, np.std(times)), "that is the population standard deviation (NumPy's default ddof=0); a sample uses ddof=1"
          assert np.isclose(sd_t, np.std(times, ddof=1)), f"sd_t should be the sample standard deviation, got {sd_t}"
          """,
          ["NumPy arrays have `.mean()` and `.std()`; the median is `np.median(arr)`.",
           "`np.std` divides by n by default (`ddof=0`). pandas' `.std()` divides by n − 1 by default."]),

        T("iqr", "Outliers by the IQR rule",
          """
          Using `np.percentile`, find the first and third quartiles of `times`, then store in `outliers` every value
          below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR, as an array.
          """,
          """
          q1, q3 = 0, 0
          outliers = times
          """,
          """
          q1, q3 = np.percentile(times, [25, 75])
          iqr = q3 - q1
          outliers = times[(times < q1 - 1.5 * iqr) | (times > q3 + 1.5 * iqr)]
          """,
          """
          assert list(outliers) == [45.0], f"outliers should be [45.0], got {list(outliers)}"
          """,
          ["`np.percentile(arr, [25, 75])` returns both quartiles at once.",
           "Combine the two conditions with `|` and index the array with the mask."]),

        T("zscore", "z-scores with broadcasting",
          """
          Compute `z`, the z-score of every value in `times` (subtract the mean, divide by the standard deviation with the default `ddof=0`),
          without a loop. Then store the values whose z-score is above 2 in absolute value in `far`.
          """,
          """
          z = times
          far = times
          """,
          """
          z = (times - times.mean()) / times.std()
          far = times[np.abs(z) > 2]
          """,
          """
          assert np.shape(z) == times.shape, "z should have one value per time"
          assert np.allclose(z, (times - times.mean()) / times.std()), "z should be (times - mean) / std, with std using ddof=0"
          assert list(far) == [45.0], f"far should be [45.0], got {list(far)}"
          """,
          ["`times - times.mean()` subtracts one number from every element: that is broadcasting.",
           "`np.abs(z) > 2` is a boolean mask."]),

        T("correlation", "Correlation",
          """
          Store the Pearson correlation between `hours` and `score` in `r_hours`, and the **name** of the column
          most negatively correlated with `score` in `most_negative`.
          """,
          """
          r_hours = 0
          most_negative = ""
          """,
          """
          r_hours = df["hours"].corr(df["score"])
          most_negative = df.corr()["score"].drop("score").idxmin()
          """,
          """
          assert np.isclose(r_hours, np.corrcoef(df["hours"], df["score"])[0, 1]), f"r_hours should be the Pearson correlation of hours and score, got {r_hours}"
          assert most_negative == "absences", f"most_negative should be 'absences', got {most_negative!r}"
          """,
          ["`s1.corr(s2)` gives Pearson's r by default; `df.corr()` gives every pair at once.",
           "`.idxmin()` returns the label of the smallest value."]),

        T("standardize", "Standardize every column at once",
          """
          `X = df.to_numpy(dtype=float)` is a 10 × 3 array. Make `X_std`, where every **column** has mean 0 and standard deviation 1
          (`ddof=0`), using `axis=0` and broadcasting instead of a loop.
          """,
          """
          X = df.to_numpy(dtype=float)
          X_std = X
          """,
          """
          X = df.to_numpy(dtype=float)
          X_std = (X - X.mean(axis=0)) / X.std(axis=0)
          """,
          """
          assert np.shape(X_std) == (10, 3), f"X_std should keep the 10 x 3 shape, got {np.shape(X_std)}"
          assert np.allclose(X_std.mean(axis=0), 0), "every column should have mean 0 (use axis=0: down the rows)"
          assert np.allclose(X_std.std(axis=0), 1), "every column should have standard deviation 1"
          """,
          ["`X.mean(axis=0)` has shape `(3,)`: one mean per column. Subtracting it from a `(10, 3)` array broadcasts across the rows."]),

        T("binned", "Summaries by band",
          """
          Cut `hours` into the bands (0, 3], (3, 6] and (6, 9] labelled `"low"`, `"mid"` and `"high"`,
          and store the mean `score` per band in the Series `by_band`.
          """,
          """
          bands = pd.cut(df["hours"], bins=[0, 3, 6, 9])
          by_band = df["score"]
          """,
          """
          bands = pd.cut(df["hours"], bins=[0, 3, 6, 9], labels=["low", "mid", "high"])
          by_band = df.groupby(bands, observed=True)["score"].mean()
          """,
          """
          assert isinstance(by_band, pd.Series), "by_band should be a Series"
          assert [str(i) for i in by_band.index] == ["low", "mid", "high"], f"the index should be low, mid, high, got {list(by_band.index)}"
          assert by_band.tolist() == [57.0, 73.0, 84.0], f"got {by_band.tolist()}"
          """,
          ["`pd.cut(values, bins=[...], labels=[...])`: bins are right-inclusive by default, so 3 falls in (0, 3].",
           "You can group by a Series that is not a column: `df.groupby(bands)`."]),
    ],
)
