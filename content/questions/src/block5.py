from qhelp import Q

QUESTIONS = [
    # ---------- 5.1.1 Matplotlib and Seaborn ----------
    Q("b5-001", "5.1.1", 1,
      "Which Seaborn function draws a histogram of a numeric column?",
      ["`sns.histplot(data=df, x=\"order_value\")`", "`sns.lineplot(data=df, x=\"order_value\")`", "`sns.heatmap(df[\"order_value\"])`", "`sns.countplot(data=df, x=\"order_value\")`"],
      0,
      {1: "A line plot connects values in order; it doesn't bin them.",
       2: "A heatmap needs a 2-D matrix of values.",
       3: "`countplot` counts each distinct value, as for categories, instead of binning a continuous range."},
      "`sns.histplot` bins a numeric variable and shows the count in each bin (add `kde=True` for a density curve).",
      "Syllabus 5.1.1 · Seaborn: histplot", ["seaborn", "histogram"]),

    Q("b5-002", "5.1.1", 2,
      "An analyst wants a chart of how many orders fall into each product category. Which Seaborn call does that?",
      ["`sns.countplot(data=df, x=\"category\")`", "`sns.barplot(data=df, x=\"category\", y=\"amount\")`", "`sns.boxplot(data=df, x=\"category\")`", "`sns.scatterplot(data=df, x=\"category\", y=\"amount\")`"],
      0,
      {1: "`barplot` shows the mean of `amount` per category, not the number of orders.",
       2: "A box plot shows a distribution, not counts.",
       3: "A scatter plot shows individual points."},
      "`countplot` counts rows per category; `barplot` aggregates a numeric column (the mean by default).",
      "Syllabus 5.1.1 · Seaborn: countplot", ["seaborn", "countplot"]),

    Q("b5-003", "5.1.1", 2,
      "What does this code print?",
      ["`(2, 3) Axes`", "`(3, 2) Axes`", "`(2, 3) Figure`", "`6 Axes`"],
      0,
      {1: "The first argument is the number of rows.",
       2: "Each element of the array is an Axes; the Figure is returned separately.",
       3: "The Axes come back as a 2-D array, so `shape` is (2, 3)."},
      "`plt.subplots(2, 3)` returns a Figure and a 2 × 3 array of Axes, indexed `axes[row, col]`.",
      "Syllabus 5.1.1 · Matplotlib: subplots", ["matplotlib", "subplots"],
      code="""
      import matplotlib
      matplotlib.use("Agg")
      import matplotlib.pyplot as plt

      fig, axes = plt.subplots(2, 3)
      print(axes.shape, type(axes[0, 1]).__name__)
      """, verify="stdout"),

    Q("b5-004", "5.1.1", 2,
      "In `sns.heatmap(df.corr(), annot=True, fmt=\".2f\", cmap=\"coolwarm\", vmin=-1, vmax=1)`, what do `annot=True` and `vmin`/`vmax` do?",
      ["`annot` writes each correlation value in its cell; `vmin`/`vmax` fix the colour scale to the full −1 to 1 range",
       "`annot` adds a title; `vmin`/`vmax` hide values outside the range",
       "`annot` sorts the variables; `vmin`/`vmax` set the figure size",
       "`annot` adds arrows; `vmin`/`vmax` set the number of decimal places"],
      0,
      {1: "Titles come from `ax.set_title`; values outside the range are clipped to the end colours, not hidden.",
       2: "The heatmap doesn't reorder variables, and figure size is set elsewhere.",
       3: "Decimal places are set by `fmt`."},
      "Annotating shows the numbers; fixing vmin and vmax makes colours comparable across heatmaps and keeps 0 at the palette's centre.",
      "Syllabus 5.1.1 · Seaborn: heatmap", ["heatmap", "seaborn"]),

    Q("b5-005", "5.1.1", 2,
      "A script calls `plt.show()` and then `plt.savefig(\"chart.png\")`, and the saved file is blank. What is the fix?",
      ["Call `savefig` before `show`", "Increase the `dpi`", "Save as JPG instead of PNG", "Call `plt.title` after saving"],
      0,
      {1: "Resolution doesn't matter if the figure was already cleared.",
       2: "The format isn't the problem.",
       3: "Anything added after saving isn't in the file."},
      "`plt.show()` can close or clear the current figure; save first (or save through the Figure object `fig.savefig`).",
      "Syllabus 5.1.1 · Matplotlib: savefig", ["matplotlib", "savefig"]),

    Q("b5-006", "5.1.1", 2,
      "A DataFrame has several sales rows per month. What does `sns.lineplot(data=df, x=\"month\", y=\"sales\")` draw by default?",
      ["The mean sales per month, with a shaded confidence band",
       "Every raw row connected in file order",
       "The total sales per month, with no band",
       "A separate line for every row"],
      0,
      {1: "Seaborn aggregates repeated x values rather than connecting raw rows.",
       2: "The default estimator is the mean, and a confidence band is added.",
       3: "Separate lines come from `hue=`."},
      "When x values repeat, `lineplot` plots the mean at each x and shades a 95% confidence interval (`errorbar=None` removes it).",
      "Syllabus 5.1.1 · Seaborn: lineplot", ["seaborn", "lineplot"]),

    Q("b5-007", "5.1.1", 3,
      "What does this code print?",
      ["`[20, 40]`", "`[60, 40]`", "`[3, 1]`", "`[10, 40, 20, 30]`"],
      0,
      {1: "`barplot` shows the mean of each category by default, not the sum (pass `estimator=\"sum\"` for totals).",
       2: "Counting rows per category is what `sns.countplot` does.",
       3: "Seaborn combines the rows that share a category into one bar."},
      "`sns.barplot` draws one bar per category whose height is the mean of `y`: Oslo (10 + 20 + 30) / 3 = 20 and Rome 40. `errorbar=None` only removes the error bars.",
      "Syllabus 5.1.1 · Seaborn docs", ["seaborn", "barplot"],
      code="""
      import matplotlib
      matplotlib.use("Agg")
      import pandas as pd
      import seaborn as sns

      df = pd.DataFrame({"city": ["Oslo", "Rome", "Oslo", "Oslo"], "sales": [10, 40, 20, 30]})
      ax = sns.barplot(data=df, x="city", y="sales", errorbar=None)
      print([round(bar.get_height()) for bar in ax.patches])
      """, verify="stdout"),

    Q("b5-008", "5.1.1", 3,
      "What does this code print?",
      ["`3 (3,) True [9.0, 3.0]`", "`3 (1, 3) True [9.0, 3.0]`", "`3 (3,) False [9.0, 3.0]`", "`1 (3,) True [9.0, 3.0]`"],
      0,
      {1: "With one row, `plt.subplots(1, 3)` returns a flat array of 3 Axes, not a 2-D array.",
       2: "`sharey=True` gives all three charts the same y-axis range.",
       3: "A figure with a 1 × 3 grid holds three Axes."},
      "`plt.subplots(1, 3)` makes one figure with three Axes in a 1-D array (a 2-D grid only comes back when there are several rows and columns). `sharey=True` locks their y-axes to one range, which makes side-by-side panels honest to compare. `figsize` is in inches.",
      "Syllabus 5.1.1 · Matplotlib docs", ["subplots", "sharey", "figsize"],
      code="""
      import matplotlib
      matplotlib.use("Agg")
      import matplotlib.pyplot as plt

      fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
      for ax, k in zip(axes, [1, 2, 3]):
          ax.plot([0, 1], [0, k])
      print(len(fig.axes), axes.shape, axes[0].get_ylim() == axes[2].get_ylim(),
            fig.get_size_inches().tolist())
      """, verify="stdout"),

    # ---------- 5.1.2 Choosing charts ----------
    Q("b5-010", "5.1.2", 1,
      "Management asks how monthly revenue has changed over the last 24 months. Which chart fits best?",
      ["Line chart", "Pie chart", "Histogram", "Box plot"],
      0,
      {1: "A pie shows parts of one whole at one moment.",
       2: "A histogram shows the distribution of values, losing the time order.",
       3: "A box plot summarizes a distribution, hiding the trend."},
      "Line charts show change over an ordered variable such as time.",
      "Syllabus 5.1.2", ["chart-choice", "line-chart"]),

    Q("b5-011", "5.1.2", 1,
      "Which chart best compares total sales across 8 regions?",
      ["A bar chart sorted by sales", "A pie chart with 8 slices", "A line chart with regions on the x-axis", "A scatter plot"],
      0,
      {1: "Eight slices are hard to compare by angle.",
       2: "Regions have no order, so a line implies a trend that doesn't exist.",
       3: "A scatter plot needs two numeric variables."},
      "Bar lengths are easy to compare; sorting makes the ranking obvious.",
      "Syllabus 5.1.2", ["chart-choice", "bar-chart"]),

    Q("b5-012", "5.1.2", 2,
      "HR wants to compare the spread of salaries, including outliers, across 5 departments. Which chart fits best?",
      ["Side-by-side box plots", "A bar chart of mean salary per department", "A pie chart of total salary", "A line chart of salaries"],
      0,
      {1: "Means hide spread and outliers.",
       2: "Totals show share of payroll, not distribution.",
       3: "Salaries aren't ordered in time."},
      "Box plots show median, IQR and outliers for each group side by side.",
      "Syllabus 5.1.2, 3.1.2", ["chart-choice", "box-plot"]),

    Q("b5-013", "5.1.2", 1,
      "Which chart shows whether higher advertising spend tends to go with higher revenue across 200 campaigns?",
      ["Scatter plot", "Pie chart", "Histogram of revenue", "Stacked bar chart"],
      0,
      {1: "A pie can't relate two numeric variables.",
       2: "A histogram shows one variable only.",
       3: "Stacked bars show composition, not a relationship between two measures."},
      "A scatter plot places each campaign by spend and revenue, revealing direction, form and strength.",
      "Syllabus 5.1.2", ["chart-choice", "scatter-plot"]),

    Q("b5-014", "5.1.2", 3,
      "A bar chart shows satisfaction of 96% for Team A and 98% for Team B, with the y-axis running from 95% to 100%. What is wrong with it?",
      ["The truncated axis makes a 2-point gap look like Team B scores several times higher; bars should start at zero",
       "Bar charts can't show percentages",
       "It should be a pie chart",
       "The bars should be sorted alphabetically"],
      0,
      {1: "Percentages are fine on a bar chart.",
       2: "Two separate scores aren't parts of one whole.",
       3: "Sorting doesn't fix the misleading scale."},
      "Bar length encodes value, so a bar chart's value axis must start at zero; otherwise small differences are exaggerated.",
      "Syllabus 5.1.2", ["misleading-charts", "axes"]),

    Q("b5-015", "5.1.2", 2,
      "Which two are genuine weaknesses of pie charts? Select two.",
      ["Angles and areas are harder to compare precisely than bar lengths",
       "With many slices they become unreadable",
       "They cannot show parts of a whole",
       "They must always be drawn in 3D",
       "They cannot be labeled with percentages"],
      [0, 1],
      {2: "Showing parts of a whole is exactly what pies do.",
       3: "3D pies are optional and discouraged.",
       4: "Pie slices can be labeled."},
      "Pies work only for a few parts; people judge lengths far more accurately than angles.",
      "Syllabus 5.1.2", ["pie-chart", "chart-choice"]),

    Q("b5-016", "5.1.2", 2,
      "A survey asked customers to pick one of 9 reasons for cancelling. The report should show what share chose each reason. Which chart fits best?",
      ["A horizontal bar chart sorted from the most to the least chosen reason",
       "A pie chart with 9 slices",
       "A line chart with the reasons along the x-axis",
       "A scatter plot of reason against share"],
      0,
      {1: "Nine slices are hard to compare; angles are read less accurately than lengths.",
       2: "A line implies order and continuity between the reasons, which they don't have.",
       3: "Scatter plots show a relationship between two numeric variables; reasons are categories."},
      "Bars make category comparisons easy, sorting shows the ranking at once, and a horizontal layout leaves room for long reason labels.",
      "Syllabus 5.1.2", ["bar-chart", "chart-choice"]),

    Q("b5-017", "5.1.2", 2,
      "Which two charts suit comparing the distribution of delivery times across four couriers? Select two.",
      ["Side-by-side box plots, one per courier",
       "A row of four histograms, one per courier, sharing the same x-axis",
       "A bar chart of each courier's mean delivery time",
       "A pie chart of each courier's number of deliveries",
       "A line chart connecting the couriers in alphabetical order"],
      [0, 1],
      {2: "A mean hides the spread, the skew and the outliers.",
       3: "A pie shows shares of deliveries, not how long they took.",
       4: "Couriers have no order, so connecting them with a line implies a trend that isn't there."},
      "Comparing distributions needs charts that show centre, spread and shape: box plots side by side, or small multiple histograms on a shared axis.",
      "Syllabus 5.1.2", ["box-plot", "histogram", "distributions"]),

    # ---------- 5.1.3 Labels and refinement ----------
    Q("b5-020", "5.1.3", 1,
      "In Matplotlib's object-oriented style, which call sets the y-axis label?",
      ["`ax.set_ylabel(\"Revenue (EUR)\")`", "`ax.ylabel(\"Revenue (EUR)\")`", "`ax.label_y(\"Revenue (EUR)\")`", "`ax.set_title(\"Revenue (EUR)\")`"],
      0,
      {1: "`ylabel` is the pyplot function (`plt.ylabel`); Axes methods use `set_`.",
       2: "There is no `label_y` method.",
       3: "`set_title` sets the title, not the axis label."},
      "Axes setters are `set_title`, `set_xlabel` and `set_ylabel`.",
      "Syllabus 5.1.3 · Matplotlib: Axes.set_ylabel", ["labels", "matplotlib"]),

    Q("b5-021", "5.1.3", 2,
      "Which call puts the legend in the upper-left corner, with small text on a white background?",
      ["`ax.legend(loc=\"upper left\", fontsize=8, facecolor=\"white\")`",
       "`ax.legend(position=\"top-left\", size=8, background=\"white\")`",
       "`ax.set_legend(\"upper left\", 8, \"white\")`",
       "`plt.legend(align=\"left\", font=8, color=\"white\")`"],
      0,
      {1: "Those parameter names don't exist; they are `loc`, `fontsize` and `facecolor`.",
       2: "There is no `set_legend` method.",
       3: "`align`, `font` and `color` aren't the legend's parameters for these properties."},
      "Legend position is `loc`, text size `fontsize`, and background colour `facecolor`.",
      "Syllabus 5.1.3 · Matplotlib: legend", ["legend", "matplotlib"],
      verify={"py": """
      import matplotlib
      matplotlib.use("Agg")
      import matplotlib.pyplot as plt
      fig, ax = plt.subplots()
      ax.plot([1, 2], [1, 2], label="a")
      leg = eval(opt(0), {"ax": ax, "plt": plt})
      assert leg._loc == 2          # 2 == "upper left"
      assert leg.get_texts()[0].get_fontsize() == 8
      assert leg.get_frame().get_facecolor()[:3] == (1.0, 1.0, 1.0)
      for i in (1, 2, 3):           # the other calls don't exist or take no such arguments
          try:
              eval(opt(i), {"ax": ax, "plt": plt})
              raise AssertionError(f"option {i} should fail")
          except (TypeError, AttributeError):
              pass
      """}),

    Q("b5-022", "5.1.3", 2,
      "Which call draws the text \"Campaign launch\" with an arrow pointing at the data point (4, 190)?",
      ["`ax.annotate(\"Campaign launch\", xy=(4, 190), xytext=(2, 215), arrowprops={\"arrowstyle\": \"->\"})`",
       "`ax.text(4, 190, \"Campaign launch\", arrow=True)`",
       "`ax.set_title(\"Campaign launch\", xy=(4, 190))`",
       "`ax.legend(\"Campaign launch\", loc=(4, 190))`"],
      0,
      {1: "`text` places plain text; it has no arrow option.",
       2: "A title labels the whole chart.",
       3: "A legend lists series; it doesn't point at data."},
      "`annotate` places text at `xytext` and draws an arrow to the point `xy`.",
      "Syllabus 5.1.3 · Matplotlib: annotate", ["annotation", "matplotlib"]),

    Q("b5-023", "5.1.3", 2,
      "Which code colours scatter points by a numeric column `z` and adds a colour scale?",
      ["sc = ax.scatter(df[\"x\"], df[\"y\"], c=df[\"z\"], cmap=\"viridis\")\nfig.colorbar(sc, ax=ax)",
       "ax.scatter(df[\"x\"], df[\"y\"], color=\"z\")\nax.legend()",
       "ax.scatter(df[\"x\"], df[\"y\"], hue=df[\"z\"])\nfig.colorbar()",
       "ax.plot(df[\"x\"], df[\"y\"], cmap=\"viridis\")"],
      0,
      {1: "`color` expects one colour, and \"z\" isn't a colour name.",
       2: "`hue` is a Seaborn parameter, not Matplotlib's `scatter`.",
       3: "`plot` draws lines and doesn't map values through a colormap."},
      "Pass the values to `c=` with a colormap; `fig.colorbar` adds the scale that explains the colours.",
      "Syllabus 5.1.3 · Matplotlib: scatter, colorbar", ["scatter", "colormap"],
      verify={"py": """
      import matplotlib
      matplotlib.use("Agg")
      import matplotlib.pyplot as plt
      import pandas as pd
      df = pd.DataFrame({"x": [1, 2, 3], "y": [3, 1, 2], "z": [0.1, 0.5, 0.9]})
      fig, ax = plt.subplots()
      exec(opt(0), {"ax": ax, "fig": fig, "df": df})
      assert len(fig.axes) == 2                   # the colour bar adds an Axes
      """}),

    Q("b5-024", "5.1.3", 3,
      "What does this code print?",
      ["`['Target']`", "`[]`", "`['_child0', 'Target']`", "`['line 1', 'Target']`"],
      0,
      {1: "The second line has a label, so it appears.",
       2: "Unlabeled lines get internal names starting with an underscore, which the legend skips.",
       3: "Matplotlib doesn't invent labels like \"line 1\"."},
      "Only artists with a `label=` appear in the legend; the unlabeled first line is left out.",
      "Syllabus 5.1.3 · Matplotlib: legend", ["legend", "labels"],
      code="""
      import matplotlib
      matplotlib.use("Agg")
      import matplotlib.pyplot as plt

      fig, ax = plt.subplots()
      ax.plot([1, 2, 3], [2, 4, 6])
      ax.plot([1, 2, 3], [1, 3, 5], label="Target")
      print([t.get_text() for t in ax.legend().get_texts()])
      """, verify="stdout"),

    Q("b5-025", "5.1.3", 2,
      "Which chart title works best for a slide shown to executives?",
      ["\"Online sales overtook in-store sales in May\"", "\"Sales by channel\"", "\"Figure 3\"", "\"Line chart of df.groupby(['month', 'channel'])\""],
      0,
      {1: "A topic title makes readers work out the point themselves.",
       2: "A figure number says nothing.",
       3: "Code belongs in the appendix, not the title."},
      "Explanatory charts carry a title that states the takeaway.",
      "Syllabus 5.1.3, 5.2.1", ["titles", "storytelling"]),

    Q("b5-026", "5.1.3", 2,
      "Early in an analysis, a quick scatter-plot matrix suggests that product returns rise in the weeks after promotions. What is the right next step?",
      ["Treat it as a hypothesis and test it, for example by comparing return rates before and after promotions",
       "Report to management that promotions cause returns",
       "Remove the promotion weeks from the data",
       "Polish the scatter matrix and put it in the final report"],
      0,
      {1: "An exploratory pattern isn't yet evidence of causation.",
       2: "Deleting data hides the pattern instead of testing it.",
       3: "Exploratory charts generate questions; explanatory charts come after the answer."},
      "Visual exploration generates hypotheses; they need testing before they become findings.",
      "Syllabus 5.1.3", ["exploration", "hypotheses"]),

    Q("b5-027", "5.1.3", 2,
      "A scatter plot of 50,000 transactions is a solid blob of overlapping points. Which two changes make the pattern readable? Select two.",
      ["Make the points partly transparent, for example `alpha=0.1`",
       "Use smaller markers, for example `s=4`",
       "Draw the plot in 3D",
       "Give every point a random colour",
       "Add a thicker frame around the plot"],
      [0, 1],
      {2: "3D adds distortion and makes positions harder to read.",
       3: "Random colours carry no information and add noise.",
       4: "The frame doesn't change how the points overlap."},
      "Transparency lets dense areas show up darker, and smaller markers overlap less. Both reduce overplotting, so the shape of the data appears.",
      "Syllabus 5.1.3 · Matplotlib docs", ["scatter", "overplotting", "alpha"]),

    Q("b5-028", "5.1.3", 2,
      "In a notebook, which two calls change the look of every chart drawn after them? Select two.",
      ["`plt.style.use(\"ggplot\")`",
       "`sns.set_theme(style=\"whitegrid\", palette=\"colorblind\")`",
       "`fig, ax = plt.subplots(figsize=(8, 4))`",
       "`ax.set_title(\"Sales by month\")`",
       "`ax.legend(loc=\"upper left\")`"],
      [0, 1],
      {2: "`figsize` sets the size of this one figure only.",
       3: "A title belongs to one Axes.",
       4: "Legend settings apply to one Axes."},
      "Styles and themes change Matplotlib's global defaults (backgrounds, gridlines, colours, fonts), so they affect every later chart. The other calls customize a single figure or Axes.",
      "Syllabus 5.1.3 · Matplotlib and Seaborn docs", ["style", "theme", "figsize"],
      verify={"py": """
      import matplotlib
      matplotlib.use("Agg")
      import matplotlib.pyplot as plt
      import seaborn as sns
      for i in (0, 1):
          plt.rcdefaults()
          before = dict(plt.rcParams)
          eval(opt(i))
          assert dict(plt.rcParams) != before, i
      plt.rcdefaults()
      """}),

    # ---------- 5.2.1 Audience ----------
    Q("b5-030", "5.2.1", 2,
      "You are presenting a churn analysis to the executive board. How should you structure it?",
      ["Lead with the recommendation and its business impact, support it with two or three simple charts, and put the methodology in an appendix",
       "Start with the data-cleaning steps and model code, then reveal the result at the end",
       "Show every chart you produced so nothing is missed",
       "Use technical terms precisely and skip the recommendation"],
      0,
      {1: "Executives need the answer first; method details can wait for questions.",
       2: "Too many charts bury the key message.",
       3: "A board presentation must end in a decision; jargon gets in the way."},
      "For decision-makers: bottom line up front, business impact, minimal but clear evidence, details on request.",
      "Syllabus 5.2.1", ["audience", "executives"]),

    Q("b5-031", "5.2.1", 2,
      "The same analysis goes to a peer review by other data analysts. What should be added compared with the board version?",
      ["Data sources, methods, assumptions and limitations, so reviewers can judge how far to trust the result",
       "More decorative visuals",
       "Fewer numbers",
       "Only the final recommendation"],
      0,
      {1: "Decoration doesn't help a technical review.",
       2: "Technical audiences want more detail, not less.",
       3: "Reviewers need to see how the recommendation was reached."},
      "Technical audiences evaluate the reasoning, so they need the method and its caveats.",
      "Syllabus 5.2.1", ["audience", "technical"]),

    Q("b5-032", "5.2.1", 2,
      "Which palette suits a correlation heatmap?",
      ["A diverging palette centred on 0, such as \"coolwarm\"", "A qualitative palette such as \"tab10\"", "A single-colour sequential palette starting at −1", "Random colours for each cell"],
      0,
      {1: "Qualitative palettes are for unordered groups, not a numeric scale.",
       2: "A one-colour ramp hides the difference between positive and negative correlations.",
       3: "Colour must encode the value consistently."},
      "Correlations run from −1 through 0 to +1; a diverging palette makes the sign and strength visible.",
      "Syllabus 5.2.1", ["palettes", "heatmap"]),

    Q("b5-033", "5.2.1", 2,
      "A dashboard marks targets met in green and missed in red. Some managers can't tell them apart. What is the best fix?",
      ["Use a colour-blind-safe palette (for example blue and orange) and add labels or icons",
       "Make the red darker",
       "Remove all colour",
       "Add a note asking users to zoom in"],
      0,
      {1: "Red-green colour blindness affects hue, not just brightness.",
       2: "Colour is useful; it just shouldn't be the only cue.",
       3: "Zooming doesn't help anyone distinguish hues."},
      "Pick palettes that stay distinct for common colour-vision deficiencies, and never rely on colour alone.",
      "Syllabus 5.2.1", ["accessibility", "colour"]),

    Q("b5-034", "5.2.1", 2,
      "Which two practices reduce clutter on report slides? Select two.",
      ["One key message per slide, stated in the title",
       "Removing decoration such as 3D effects, heavy gridlines and extra decimals",
       "Adding every table from the analysis to each slide",
       "Giving every bar a different colour for variety",
       "Pasting the full code under each chart"],
      [0, 1],
      {2: "Full tables belong in an appendix.",
       3: "Colour should encode meaning; random variety distracts.",
       4: "Code belongs in an appendix or repository."},
      "Focus each slide on one message and strip anything that doesn't carry information.",
      "Syllabus 5.2.1", ["clutter", "slides"]),

    Q("b5-035", "5.2.1", 1,
      "A map colours regions by population density, from low to high. Which palette type fits?",
      ["Sequential", "Diverging", "Qualitative", "Rainbow with random order"],
      0,
      {1: "Diverging palettes need a meaningful midpoint.",
       2: "Qualitative palettes are for unordered categories.",
       3: "Random hue order breaks the low-to-high reading."},
      "Ordered values from low to high use a sequential palette (for example viridis).",
      "Syllabus 5.2.1", ["palettes", "sequential"]),

    Q("b5-036", "5.2.1", 3,
      "A churn slide for the operations director is titled \"Logistic regression coefficients (L2, C=1.0)\" and shows a table of 14 coefficients to four decimals, shaded red and green. Which revision serves this audience best?",
      ["Title it with the finding (\"Late deliveries are the biggest driver of churn\"), show the top three drivers as a sorted bar chart in business terms with one colour-blind-safe highlight, and move the coefficient table to an appendix",
       "Keep the table, and add a paragraph explaining L2 regularization and the `C` parameter",
       "Replace the table with a 3D pie chart of all 14 coefficients",
       "Keep the table and its red/green shading, but round the coefficients to two decimals"],
      0,
      {1: "The director needs the finding and its impact, not the method; technical detail belongs in an appendix or a peer review.",
       2: "A 14-slice 3D pie is hard to read, and coefficients (some negative) aren't parts of a whole.",
       3: "Rounding helps a little, but the slide still has no takeaway, too much detail, and colours many viewers can't tell apart."},
      "For a non-technical decision-maker: a title that states the takeaway, only the few numbers that drive the decision, in business terms, a chart that makes the ranking obvious, accessible colours, and the methodology moved out of the way.",
      "Syllabus 5.2.1", ["audience", "slides", "accessibility"]),

    Q("b5-037", "5.2.1", 2,
      "Which sentence best opens a one-page summary for a non-technical regional manager?",
      ["\"Stores that opened in the evening sold 12% more (about €40,000 a month); we recommend extending evening hours to the 8 similar stores.\"",
       "\"The regression coefficient for evening_open was 0.118 (p < 0.01, R² = 0.62).\"",
       "\"We ran several analyses, and some of the results were interesting.\"",
       "\"Sales depend on many factors; see appendix tables A1 to A14.\""],
      0,
      {1: "Accurate, but in technical terms that don't say what it means for the business.",
       2: "Vague: no finding, no number, no action.",
       3: "It sends the reader to the appendix instead of giving the answer."},
      "For a non-technical decision-maker, lead with the finding in business terms, its size in money, and the recommended action.",
      "Syllabus 5.2.1", ["audience", "summary", "bluf"]),

    # ---------- 5.2.2 Evidence ----------
    Q("b5-040", "5.2.2", 2,
      "Which summary statement is the most informative?",
      ["\"Monthly churn fell from 8.1% to 6.4% in the three months after the loyalty launch (40,000 customers).\"",
       "\"Churn improved a lot.\"",
       "\"The loyalty program is a success.\"",
       "\"Churn went down 1.7.\""],
      0,
      {1: "No numbers, period or base.",
       2: "A judgement without evidence.",
       3: "1.7 what? Points or percent? Over what period?"},
      "Good summaries give the comparison, the size of the change with units, the period and the base.",
      "Syllabus 5.2.2", ["summaries", "evidence"]),

    Q("b5-041", "5.2.2", 2,
      "Observational data show that customers who use the mobile app spend 30% more. Which statement is justified?",
      ["App users spend more; the app may or may not be the cause, since heavy spenders may simply be likelier to install it",
       "The app causes customers to spend 30% more",
       "Removing the app would cut spending by 30%",
       "The data prove nothing at all"],
      0,
      {1: "Without random assignment, a causal claim isn't supported.",
       2: "That also assumes causation.",
       3: "The association is real information; it just isn't causal proof."},
      "Observational data support \"associated with\"; causal claims need an experiment such as an A/B test.",
      "Syllabus 5.2.2", ["causation", "claims"]),

    Q("b5-042", "5.2.2", 2,
      "A 12-week test of a new checkout shows gains in weeks 3 and 4 and no difference in the other 10 weeks. The draft report shows only weeks 3 and 4. What is the problem?",
      ["Cherry-picking: the full period doesn't support the claim",
       "Nothing; the best weeks show the potential",
       "The chart type is wrong",
       "The test was too long"],
      0,
      {1: "Selecting favourable periods misrepresents the result.",
       2: "The issue is which data is shown, not how.",
       3: "Test length isn't the problem."},
      "Report the whole test period (or justify any subset), otherwise the claim rests on selected evidence.",
      "Syllabus 5.2.2", ["cherry-picking", "integrity"]),

    Q("b5-043", "5.2.2", 2,
      "The CFO must decide whether to renew a €2 million marketing contract. Which finding should lead the summary?",
      ["The campaign's measured return: incremental revenue compared with its cost",
       "The number of charts produced",
       "That the data needed a lot of cleaning",
       "The Python libraries used"],
      0,
      {1: "Output volume doesn't inform the decision.",
       2: "Process details matter less than the result.",
       3: "Tools are irrelevant to the decision."},
      "Prioritize the finding most relevant to the decision being made.",
      "Syllabus 5.2.2", ["prioritization", "findings"]),

    Q("b5-044", "5.2.2", 3,
      "Which two elements best support a claim that a new checkout increased conversion? Select two.",
      ["A randomized A/B test result with sample sizes and a confidence interval for the difference",
       "The data source and the exact time period analyzed",
       "A single customer's positive comment",
       "A bar chart whose y-axis starts at 95%",
       "The claim repeated in bold on every slide"],
      [0, 1],
      {2: "An anecdote isn't representative evidence.",
       3: "A truncated axis exaggerates the effect.",
       4: "Repetition isn't evidence."},
      "Strong evidence shows the method (randomized), the size and uncertainty of the effect, and where and when the data came from.",
      "Syllabus 5.2.2", ["evidence", "a-b-testing"]),

    Q("b5-045", "5.2.2", 2,
      "A slide says \"Sales of the new flavour doubled this week!\" What is missing?",
      ["The base: doubling from 3 units to 6 is very different from 3,000 to 6,000",
       "A pie chart",
       "A darker font",
       "A longer title"],
      0,
      {1: "The chart type doesn't fix a missing base.",
       2: "Typography doesn't add information.",
       3: "A longer title without numbers adds nothing."},
      "Percentages and ratios need the absolute numbers behind them.",
      "Syllabus 5.2.2", ["context", "percentages"]),

    Q("b5-046", "5.2.2", 3,
      "A draft report says: \"Customers who used live chat were 25% more likely to renew, so live chat increases renewals.\" The data is observational. What is the best revision?",
      ["Say chat users renewed more often, note they may differ (for example, be more engaged) so the link isn't proven causal, and propose a test that offers chat to a random half",
       "Keep the claim and add a bigger chart of chat usage",
       "Remove the customers who didn't renew so the effect is clearer",
       "Strengthen the claim to \"live chat guarantees renewals\""],
      0,
      {1: "A bigger chart doesn't make an association causal.",
       2: "Dropping non-renewers destroys the comparison the claim depends on.",
       3: "That overstates the evidence even further."},
      "Observational data supports \"is associated with\". State the evidence honestly, name the likely confounder, and recommend a randomized test that could show cause and effect.",
      "Syllabus 5.2.2", ["causation", "evidence", "limitations"]),

    Q("b5-047", "5.2.2", 2,
      "Which two belong in the evidence behind a recommendation to switch suppliers? Select two.",
      ["Late-delivery rates for both suppliers over the same six months, with the number of deliveries behind each",
       "Where the delivery data came from and how \"late\" was defined",
       "The analyst's opinion of each supplier's website",
       "A bar chart whose axis starts at 90% to make the gap look bigger",
       "One store manager's story about a late delivery"],
      [0, 1],
      {2: "Opinions about unrelated features aren't evidence about deliveries.",
       3: "A truncated axis exaggerates the difference and misleads the reader.",
       4: "One anecdote can't show a pattern across thousands of deliveries."},
      "Strong evidence compares like with like (same period), shows the sample sizes, and is transparent about the data source and definitions so others can check it.",
      "Syllabus 5.2.2", ["evidence", "transparency"]),
]
