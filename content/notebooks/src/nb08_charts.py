from nbhelp import NB, T

NOTEBOOK = NB(
    "charts", "Charts with Matplotlib", 2, ["5.1.1", "5.1.2", "5.1.3"],
    "Line, bar and scatter charts, titles and labels, annotation and subplots.",
    """
    Six months of website traffic and the visits per marketing channel. In every task, create the chart with
    `fig, ax = plt.subplots()` and keep those names: the checks read the chart from `ax` (and `fig`).
    """,
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    monthly = pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "visitors": [1200, 1350, 1280, 1600, 1750, 1900],
        "signups": [80, 95, 90, 130, 150, 170],
    })
    by_channel = pd.Series({"Email": 220, "Search": 540, "Direct": 180, "Social": 310})
    """,
    [
        T("line", "A labelled line chart",
          """
          Plot `visitors` against `month` as a line chart, with the title `Monthly visitors`, the x-axis label `Month` and the y-axis label `Visitors`.
          """,
          """
          fig, ax = plt.subplots()
          """,
          """
          fig, ax = plt.subplots()
          ax.plot(monthly["month"], monthly["visitors"], marker="o")
          ax.set_title("Monthly visitors")
          ax.set_xlabel("Month")
          ax.set_ylabel("Visitors")
          """,
          """
          assert len(ax.lines) >= 1, "draw a line on ax (ax.plot)"
          assert list(ax.lines[0].get_ydata()) == monthly["visitors"].tolist(), "the line should show the visitors column"
          assert ax.get_title() == "Monthly visitors", f"title is {ax.get_title()!r}"
          assert ax.get_xlabel() == "Month", f"x label is {ax.get_xlabel()!r}"
          assert ax.get_ylabel() == "Visitors", f"y label is {ax.get_ylabel()!r}"
          """,
          ["`ax.plot(x, y)`, then `ax.set_title`, `ax.set_xlabel` and `ax.set_ylabel`.",
           "A line chart suits values that change over an ordered sequence such as time."]),

        T("bar", "A sorted bar chart",
          """
          Draw a vertical bar chart of `by_channel` with the bars sorted from **largest to smallest**, and the title `Visits by channel`.
          """,
          """
          fig, ax = plt.subplots()
          ax.bar(by_channel.index, by_channel.values)
          """,
          """
          ordered = by_channel.sort_values(ascending=False)
          fig, ax = plt.subplots()
          ax.bar(ordered.index, ordered.values)
          ax.set_title("Visits by channel")
          """,
          """
          ax.figure.canvas.draw()
          heights = [p.get_height() for p in ax.patches]
          assert len(heights) == 4, f"expected 4 bars, found {len(heights)}"
          assert heights == [540, 310, 220, 180], f"bar heights left to right are {heights}; sort the Series descending first"
          labels = [t.get_text() for t in ax.get_xticklabels()]
          assert labels == ["Search", "Social", "Email", "Direct"], f"bar labels are {labels}"
          assert ax.get_title() == "Visits by channel", f"title is {ax.get_title()!r}"
          """,
          ["`by_channel.sort_values(ascending=False)` before plotting.",
           "Sorted bars make the ranking readable at a glance; a pie chart would hide the small differences."]),

        T("scatter", "A scatter plot for a relationship",
          """
          Show the relationship between `visitors` (x) and `signups` (y) as a scatter plot, with the axis labels `Visitors` and `Signups`.
          """,
          """
          fig, ax = plt.subplots()
          ax.plot(monthly["visitors"], monthly["signups"])
          """,
          """
          fig, ax = plt.subplots()
          ax.scatter(monthly["visitors"], monthly["signups"])
          ax.set_xlabel("Visitors")
          ax.set_ylabel("Signups")
          """,
          """
          assert len(ax.collections) >= 1, "use ax.scatter: a scatter plot draws points, not a connected line"
          points = ax.collections[0].get_offsets().tolist()
          assert points == [[v, s] for v, s in zip(monthly["visitors"], monthly["signups"])], "plot visitors on x and signups on y"
          assert ax.get_xlabel() == "Visitors" and ax.get_ylabel() == "Signups", f"labels are {ax.get_xlabel()!r} and {ax.get_ylabel()!r}"
          """,
          ["`ax.scatter(x, y)` draws one marker per pair, which is the chart for a relationship between two numeric variables."]),

        T("annotate", "Annotate the peak",
          """
          Plot `signups` by `month` as a line and annotate the highest point with the text `Peak: 170`, using an arrow.
          Find the peak in code rather than typing its position.
          """,
          """
          fig, ax = plt.subplots()
          ax.plot(monthly["month"], monthly["signups"])
          """,
          """
          fig, ax = plt.subplots()
          ax.plot(monthly["month"], monthly["signups"])
          i = monthly["signups"].idxmax()
          peak = monthly.loc[i, "signups"]
          ax.annotate(f"Peak: {peak}", xy=(i, peak), xytext=(i - 2, peak - 20), arrowprops={"arrowstyle": "->"})
          """,
          """
          assert len(ax.lines) >= 1 and list(ax.lines[0].get_ydata()) == monthly["signups"].tolist(), "plot the signups line"
          notes = [t for t in ax.texts if t.get_text() == "Peak: 170"]
          assert notes, f"no annotation with the text 'Peak: 170'; texts on the axes: {[t.get_text() for t in ax.texts]}"
          assert getattr(notes[0], "arrow_patch", None) is not None, "add an arrow with arrowprops={'arrowstyle': '->'}"
          """,
          ["`ax.annotate(text, xy=point, xytext=label_position, arrowprops={...})`.",
           "With text on the x-axis, Matplotlib places the categories at positions 0, 1, 2, ..., so the row position works as x."]),

        T("subplots", "Two charts side by side",
          """
          Make one figure with two charts side by side: on the left, the visitors line by month; on the right, a bar chart of `by_channel`.
          Give the whole figure the title `Website overview`. Use `fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))`.
          """,
          """
          fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
          """,
          """
          fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
          left.plot(monthly["month"], monthly["visitors"])
          right.bar(by_channel.index, by_channel.values)
          fig.suptitle("Website overview")
          """,
          """
          axes = fig.get_axes()
          assert len(axes) == 2, f"the figure should have 2 axes, found {len(axes)}"
          assert len(axes[0].lines) >= 1, "draw the visitors line on the left axes"
          assert len(axes[1].patches) == 4, "draw the four channel bars on the right axes"
          assert fig._suptitle is not None and fig._suptitle.get_text() == "Website overview", "set the figure title with fig.suptitle"
          """,
          ["Each axes has its own methods: `left.plot(...)`, `right.bar(...)`.",
           "`fig.suptitle` titles the whole figure; `ax.set_title` titles one chart."]),
    ],
)
