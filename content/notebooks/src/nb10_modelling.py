from nbhelp import NB, T

NOTEBOOK = NB(
    "modelling", "Modelling with scikit-learn", 3, ["1.2.3", "3.2.1", "3.2.2", "4.2.2", "4.2.3"],
    "Train/test split, linear and logistic regression, scaling without leakage, overfitting and a bootstrap interval.",
    """
    200 simulated house sales: `price` depends on `size` (m²) and `rooms`, plus noise. `expensive` is 1 for prices above the median.

    The tasks build on each other, like a notebook run from top to bottom: running a task first runs your code
    for the tasks before it.
    """,
    """
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(0)
    n = 200
    size = rng.uniform(40, 160, n).round(1)
    rooms = rng.integers(1, 6, n)
    price = (1500 * size + 8000 * rooms + rng.normal(0, 15000, n)).round(-2)
    houses = pd.DataFrame({"size": size, "rooms": rooms, "price": price})
    houses["expensive"] = (houses["price"] > houses["price"].median()).astype(int)
    """,
    [
        T("split", "Hold out a test set",
          """
          Split the features `X` (the `size` and `rooms` columns) and the target `y` (`price`) into
          `X_train, X_test, y_train, y_test`, with 25% for testing and `random_state=42`.
          """,
          """
          X = houses[["size", "rooms"]]
          y = houses["price"]
          # split into X_train, X_test, y_train, y_test
          """,
          """
          from sklearn.model_selection import train_test_split

          X = houses[["size", "rooms"]]
          y = houses["price"]
          X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
          """,
          """
          from sklearn.model_selection import train_test_split as _tts
          _Xtr, _Xte, _ytr, _yte = _tts(houses[["size", "rooms"]], houses["price"], test_size=0.25, random_state=42)
          assert X_train.shape == (150, 2) and X_test.shape == (50, 2), f"shapes are {X_train.shape} and {X_test.shape}; expected (150, 2) and (50, 2)"
          assert list(X_test.index) == list(_Xte.index), "use test_size=0.25 and random_state=42 so the split is reproducible"
          assert list(y_test.index) == list(X_test.index), "keep the order: X_train, X_test, y_train, y_test"
          """,
          ["`train_test_split(X, y, test_size=0.25, random_state=42)` returns four pieces in the order X_train, X_test, y_train, y_test."]),

        T("linear", "Linear regression",
          """
          Fit a `LinearRegression` called `lin` on the **training** data. Store its R² on the **test** data in `r2_test`
          and the coefficient for `size` in `coef_size` (about 1500, the price per extra m²).
          """,
          """
          from sklearn.linear_model import LinearRegression

          lin = LinearRegression()
          r2_test = 0
          coef_size = 0
          """,
          """
          from sklearn.linear_model import LinearRegression

          lin = LinearRegression().fit(X_train, y_train)
          r2_test = lin.score(X_test, y_test)
          coef_size = lin.coef_[0]
          """,
          """
          from sklearn.linear_model import LinearRegression as _LR
          _m = _LR().fit(X_train, y_train)
          assert hasattr(lin, "coef_"), "fit the model: lin.fit(X_train, y_train)"
          assert np.allclose(lin.coef_, _m.coef_), "fit lin on the training data only (X_train, y_train)"
          assert np.isclose(r2_test, _m.score(X_test, y_test)), f"r2_test should be the R² on the test set, got {r2_test}"
          assert np.isclose(coef_size, _m.coef_[0]), f"coef_size should be the first coefficient (size), got {coef_size}"
          """,
          ["`model.score(X, y)` returns R² for a regressor.",
           "`coef_` holds one coefficient per feature, in the column order of X."]),

        T("scale", "Scale without leaking",
          """
          Standardize the features with a `StandardScaler` that learns its mean and standard deviation from the
          **training set only**, then transform both sets into `X_train_s` and `X_test_s`.
          """,
          """
          from sklearn.preprocessing import StandardScaler

          scaler = StandardScaler()
          X_train_s = scaler.fit_transform(X_train)
          X_test_s = scaler.fit_transform(X_test)
          """,
          """
          from sklearn.preprocessing import StandardScaler

          scaler = StandardScaler().fit(X_train)
          X_train_s = scaler.transform(X_train)
          X_test_s = scaler.transform(X_test)
          """,
          """
          from sklearn.preprocessing import StandardScaler as _SS
          _s = _SS().fit(X_train)
          assert np.allclose(X_train_s, _s.transform(X_train)), "X_train_s should be the training features standardized with the training mean and std"
          assert np.allclose(X_test_s, _s.transform(X_test)), "X_test_s should be transformed with the scaler fitted on the training data; refitting on the test set leaks information and gives a different scale"
          """,
          ["Fit once on the training data, then call `transform` (not `fit_transform`) on the test data.",
           "Statistics computed from the test set would let information about it into training: data leakage."]),

        T("logistic", "Logistic regression against a baseline",
          """
          Classify `expensive` with a `LogisticRegression` called `clf`, trained on `X_train_s`. Use the same rows as the split:
          `yc_train = houses.loc[X_train.index, "expensive"]` and likewise `yc_test`.

          Store the test-set predictions in `pred`, the test accuracy in `acc`, and in `baseline` the accuracy of always predicting
          the most common class of `yc_train`.
          """,
          """
          from sklearn.linear_model import LogisticRegression

          yc_train = houses.loc[X_train.index, "expensive"]
          yc_test = houses.loc[X_test.index, "expensive"]
          clf = LogisticRegression()
          pred = None
          acc = 0
          baseline = 0
          """,
          """
          from sklearn.linear_model import LogisticRegression

          yc_train = houses.loc[X_train.index, "expensive"]
          yc_test = houses.loc[X_test.index, "expensive"]
          clf = LogisticRegression().fit(X_train_s, yc_train)
          pred = clf.predict(X_test_s)
          acc = (pred == yc_test).mean()
          baseline = (yc_test == yc_train.mode()[0]).mean()
          """,
          """
          _yte = houses.loc[X_test.index, "expensive"].to_numpy()
          _ytr = houses.loc[X_train.index, "expensive"]
          assert hasattr(clf, "coef_"), "fit clf on X_train_s and yc_train"
          assert pred is not None and len(pred) == 50, "pred should hold one prediction per test row"
          assert np.isclose(acc, np.mean(np.asarray(pred) == _yte)), f"acc should be the share of test predictions that are right, got {acc}"
          _base = np.mean(_yte == _ytr.mode()[0])
          assert np.isclose(baseline, _base), f"baseline should be {_base:.2f}: the accuracy of always predicting the training set's most common class"
          assert acc > baseline + 0.1, f"accuracy {acc:.2f} should clearly beat the baseline {baseline:.2f}"
          """,
          ["`clf.predict(X)` gives class labels; `(pred == y).mean()` is the accuracy.",
           "`yc_train.mode()[0]` is the most common class. A model is only useful if it beats this."]),

        T("overfit", "Spot overfitting",
          """
          Fit two `DecisionTreeRegressor` models on the training data, both with `random_state=0`: `deep` with no depth limit and
          `shallow` with `max_depth=3`. For each, compute the gap between training R² and test R² (`gap_deep`, `gap_shallow`).
          Set `overfits` to `"deep"` or `"shallow"`, whichever has the larger gap.
          """,
          """
          from sklearn.tree import DecisionTreeRegressor

          gap_deep = 0
          gap_shallow = 0
          overfits = ""
          """,
          """
          from sklearn.tree import DecisionTreeRegressor

          deep = DecisionTreeRegressor(random_state=0).fit(X_train, y_train)
          shallow = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X_train, y_train)
          gap_deep = deep.score(X_train, y_train) - deep.score(X_test, y_test)
          gap_shallow = shallow.score(X_train, y_train) - shallow.score(X_test, y_test)
          overfits = "deep" if gap_deep > gap_shallow else "shallow"
          """,
          """
          from sklearn.tree import DecisionTreeRegressor as _DT
          _d = _DT(random_state=0).fit(X_train, y_train)
          _s = _DT(max_depth=3, random_state=0).fit(X_train, y_train)
          _gd = _d.score(X_train, y_train) - _d.score(X_test, y_test)
          _gs = _s.score(X_train, y_train) - _s.score(X_test, y_test)
          assert np.isclose(gap_deep, _gd), f"gap_deep should be train R² minus test R² for the unlimited tree ({_gd:.3f}), got {gap_deep}"
          assert np.isclose(gap_shallow, _gs), f"gap_shallow should be train R² minus test R² for the depth-3 tree ({_gs:.3f}), got {gap_shallow}"
          assert overfits == "deep", f"overfits is {overfits!r}: the unlimited tree fits the training noise (training R² of 1.0) and has the larger gap"
          """,
          ["A tree with no depth limit can memorize the training set: low bias, high variance.",
           "A large gap between training and test scores is the sign of overfitting."]),

        T("bootstrap", "A bootstrap confidence interval",
          """
          Estimate a 95% confidence interval for the mean `price` by bootstrapping: draw 1000 resamples of `houses["price"]`
          **with replacement**, each the same size as the data, using `rng = np.random.default_rng(1)`. Store the 1000 resample
          means in `boot_means` and the 2.5th and 97.5th percentiles in `ci`.
          """,
          """
          rng = np.random.default_rng(1)
          prices = houses["price"].to_numpy()
          boot_means = []
          ci = (0, 0)
          """,
          """
          rng = np.random.default_rng(1)
          prices = houses["price"].to_numpy()
          boot_means = np.array([rng.choice(prices, size=len(prices), replace=True).mean() for _ in range(1000)])
          ci = np.percentile(boot_means, [2.5, 97.5])
          """,
          """
          _p = houses["price"].to_numpy()
          assert len(boot_means) == 1000, f"boot_means should hold 1000 means, has {len(boot_means)}"
          assert np.std(boot_means) > 0, "every resample has the same mean: sample with replacement (replace=True)"
          assert len(ci) == 2 and ci[0] < _p.mean() < ci[1], f"ci {ci} should contain the sample mean {_p.mean():.0f}"
          _expected = 2 * 1.96 * _p.std(ddof=1) / np.sqrt(len(_p))
          assert 0.7 * _expected < ci[1] - ci[0] < 1.3 * _expected, f"the interval is {ci[1] - ci[0]:.0f} wide; expected about {_expected:.0f}. Each resample should have {len(_p)} values"
          assert np.isclose(ci[0], np.percentile(boot_means, 2.5)) and np.isclose(ci[1], np.percentile(boot_means, 97.5)), "ci should be the 2.5th and 97.5th percentiles of boot_means"
          """,
          ["`rng.choice(prices, size=len(prices), replace=True)` draws one resample.",
           "`np.percentile(boot_means, [2.5, 97.5])` gives both ends of the interval."]),
    ],
    chain=True,
)
