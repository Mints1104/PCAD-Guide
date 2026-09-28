# Block 5: Data Communication and Visualization

Block 5 is 5 items, 10.4% of the exam: building charts with Matplotlib and Seaborn, choosing the right chart, labeling and refining it, and communicating findings to different audiences with evidence behind every claim. Code items here usually ask which call draws a given chart or changes a given element.

## 5.1.1 Demonstrate proficiency with Matplotlib and Seaborn

**Syllabus asks:** create box plots, histograms, scatter plots, line plots and correlation heatmaps, and interpret the data and findings they show.

### Core facts

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

rng = np.random.default_rng(0)
df = pd.DataFrame({"month": np.tile(np.arange(1, 13), 2),
                   "store": np.repeat(["A", "B"], 12),
                   "sales": rng.normal(100, 15, 24).round(1),
                   "visits": rng.normal(900, 120, 24).round()})

fig, axes = plt.subplots(2, 2, figsize=(10, 7))              # object-oriented API: a grid of Axes
axes[0, 0].hist(df["sales"], bins=8)                          # histogram
axes[0, 1].scatter(df["visits"], df["sales"], alpha=0.7)      # scatter plot
sns.boxplot(data=df, x="store", y="sales", ax=axes[1, 0])     # box plot per group
sns.heatmap(df[["sales", "visits", "month"]].corr(), annot=True, fmt=".2f",
            cmap="coolwarm", vmin=-1, vmax=1, ax=axes[1, 1])  # correlation heatmap
fig.tight_layout()
fig.savefig("dashboard.png", dpi=150)
```

| Chart | Matplotlib | Seaborn |
|---|---|---|
| Line plot | `ax.plot(x, y)` | `sns.lineplot(data=df, x=, y=, hue=)` |
| Scatter plot | `ax.scatter(x, y)` | `sns.scatterplot(data=df, x=, y=, hue=)`; `sns.regplot` adds a fitted line |
| Histogram | `ax.hist(values, bins=20)` | `sns.histplot(data=df, x=, bins=, kde=True)` |
| Box plot | `ax.boxplot(values)` | `sns.boxplot(data=df, x="group", y="value")` |
| Bar chart | `ax.bar(labels, heights)` / `ax.barh` | `sns.barplot` (shows the **mean** with an error bar), `sns.countplot` (counts rows) |
| Heatmap | `ax.imshow(matrix)` | `sns.heatmap(df.corr(), annot=True)` |

- **Two Matplotlib styles.** The pyplot (state-based) style calls `plt.plot`, `plt.title` on the "current" figure. The object-oriented style creates `fig, ax = plt.subplots()` and calls methods on `ax`. Prefer the object-oriented style for anything with more than one chart.
- `plt.subplots(nrows, ncols)` returns a figure and an array of Axes; index it as `axes[row, col]`.
- Seaborn's axes-level functions (`histplot`, `boxplot`, `scatterplot`, `heatmap`) draw on one Axes and accept `ax=`; figure-level functions (`relplot`, `displot`, `catplot`, `pairplot`) create their own figure with facets.
- Seaborn takes a DataFrame with `data=` and column names for `x=`, `y=` and `hue=` (colour by group). It works best with long (tidy) data.
- `sns.lineplot` averages repeated x values and draws a confidence band by default.
- `plt.show()` displays the figure; `fig.savefig("file.png", dpi=150, bbox_inches="tight")` writes it to disk. Call `savefig` before `show`, which may clear the figure.
- pandas can plot directly: `df.plot(x="month", y="sales")`, `df["sales"].plot(kind="hist")`.

### Exam traps

> **Trap.** `sns.barplot` shows the mean of each category, not the count; `sns.countplot` counts rows.

> **Trap.** `plt.title()` and `ax.set_title()` do the same job in different styles; in the object-oriented style the setters start with `set_`.

## 5.1.2 Assess the pros and cons of data representations

**Syllabus asks:** judge which chart types suit which data and objective, and how well a visualization conveys its message.

### Core facts

| Goal | Best choice | Avoid |
|---|---|---|
| Compare values across categories | Bar chart (sorted; horizontal for long labels) | Pie with many slices; line chart for unordered categories |
| Show a trend over time | Line chart | Bars for long, dense time series |
| Show the distribution of one variable | Histogram, box plot, density (KDE) | A bar chart of means (hides spread) |
| Compare distributions across groups | Side-by-side box plots or violin plots | Overlapping histograms of many groups |
| Show the relationship between two numbers | Scatter plot (plus a trend line) | Line chart when x isn't ordered |
| Show correlations among many variables | Correlation heatmap, pair plot | A wall of scatter plots |
| Show parts of a whole | Stacked bar, or a pie with two to five slices | 3D pies |

**Pros and cons.**

- **Bar charts** are precise (length is easy to compare) but their value axis must start at zero; a truncated axis exaggerates differences.
- **Pie charts** show part-to-whole at a glance but angles are hard to compare; beyond a few slices, use a bar chart.
- **Line charts** make trends and seasonality obvious; they imply continuity, so don't connect unrelated categories.
- **Histograms** show shape, but the bin width changes the story; try a few.
- **Box plots** summarize centre, spread and outliers compactly but hide multiple peaks (bimodality); a violin or histogram shows those.
- **Scatter plots** reveal form, direction and outliers; with thousands of points, reduce overplotting with transparency (`alpha`), smaller markers, or a hexbin plot.
- **Heatmaps** show many values at once; they depend on a sensible colour scale (diverging and centred on 0 for correlations).
- **3D effects, dual y-axes and decorative clutter** make charts harder to read.

A chart is effective when it answers one question, the takeaway is visible within seconds, and nothing on it distracts from that.

### Exam traps

> **Trap.** "How has monthly revenue changed over two years?" → line chart. "Which of eight regions sold most?" → sorted bar chart.

> **Trap.** A bar chart whose y-axis starts at 95 makes a 2% difference look like a 50% one.

## 5.1.3 Label, annotate and refine visualizations

**Syllabus asks:** add labels, titles and annotations for clarity and emphasis; use visual exploration to form hypotheses and support data-driven decisions; customize scatter plot colours; label axes and add titles; set legend properties (position, font size, background colour).

### Core facts

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
online = [120, 135, 150, 148, 190, 210]
store = [200, 195, 190, 185, 180, 176]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(months, online, marker="o", color="tab:blue", label="Online")
ax.plot(months, store, marker="o", color="tab:gray", label="In store")
ax.set_title("Online sales overtook in-store sales in May")
ax.set_xlabel("Month (2025)")
ax.set_ylabel("Revenue (thousand EUR)")
ax.annotate("Spring campaign", xy=(4, 190), xytext=(1.5, 215),
            arrowprops={"arrowstyle": "->"})
ax.axhline(180, linestyle="--", linewidth=1, color="black", label="Target")
ax.legend(loc="lower right", fontsize=9, facecolor="whitesmoke", framealpha=1, title="Channel")
ax.set_ylim(0, 240)
fig.tight_layout()
```

| Element | Call |
|---|---|
| Title | `ax.set_title("...")` / `plt.title("...")`; `fig.suptitle` for a whole figure |
| Axis labels (with units) | `ax.set_xlabel`, `ax.set_ylabel` / `plt.xlabel`, `plt.ylabel` |
| Legend | `label=` on each plotted series, then `ax.legend(loc=, fontsize=, facecolor=, framealpha=, frameon=, title=, ncol=)`; `bbox_to_anchor=(1.02, 1), loc="upper left"` moves it outside the plot |
| Annotation | `ax.annotate(text, xy=point, xytext=text_position, arrowprops={...})`; `ax.text(x, y, text)` for plain text |
| Reference line | `ax.axhline(y)` / `ax.axvline(x)` |
| Axis range and ticks | `ax.set_xlim`, `ax.set_ylim`; `ax.tick_params(axis="x", rotation=45)` or `plt.xticks(rotation=45)` |
| Scatter colours | `color="tab:red"` for one colour; `c=values, cmap="viridis"` to colour by a numeric variable (add `fig.colorbar`); `alpha=0.5` for overlap; `s=` for marker size; `hue=` in Seaborn |
| Layout | `fig.tight_layout()` stops labels overlapping |

**Refining.** Write titles that state the takeaway, not just the topic. Put units in axis labels. Highlight the series that matters in a strong colour and push the rest to grey. Remove what doesn't help (heavy gridlines, borders, extra decimals). Label lines directly when a legend would make readers look back and forth.

**Exploration vs explanation.** Early charts are for you: plot distributions, relationships and breakdowns quickly to spot patterns and form hypotheses ("returns spike after promotions?"), then test them. Final charts are for others: one clear message, fully labeled.

### Exam traps

> **Trap.** `ax.legend()` shows nothing useful unless the plotted series were given `label=` values.

> **Trap.** The legend's position argument is `loc` (for example `"upper left"` or `"best"`), and its background is `facecolor`.

## 5.2.1 Tailor communication to audience needs

**Syllabus asks:** analyze the audience's background, interests and knowledge; adapt style and content; build presentations for technical and non-technical stakeholders; integrate visuals smoothly into reports and slides; write concise text that complements visuals; avoid clutter; build a data narrative with actionable takeaways; choose colour palettes for clarity and accessibility.

### Core facts

| | Executives / non-technical | Technical peers |
|---|---|---|
| Want | The decision, the impact, the recommendation | How you got there and how far to trust it |
| Lead with | The answer (bottom line up front) | The question and the approach |
| Detail | A few key numbers in business terms (revenue, cost, customers) | Methods, assumptions, data sources, limitations, code |
| Charts | Simple, one message each, takeaway titles | Can be denser: distributions, residuals, diagnostics |
| Language | Plain; no jargon ("most customers" beats "the modal segment") | Precise terms welcome |

**A data narrative** follows context → finding → implication → recommendation: what we looked at and why, what we found, why it matters, and what to do next. Each slide or section makes one point, and its title says that point.

**Integrating visuals.** Place each chart next to the text that interprets it. The text adds what the chart can't show (the cause, the size of the effect in money, the action); it doesn't repeat what readers can see. Use the same colour for the same thing everywhere (if "online" is blue in one chart, it is blue in all of them), and match highlighted words in the text to the highlighted series.

**Avoiding clutter.** One message per slide; remove decoration, 3D, unnecessary gridlines and legends that direct labels can replace; round numbers sensibly; move detail to an appendix.

**Colour and accessibility.** Around 1 in 12 men has some colour-vision deficiency, most often red-green. Don't rely on red vs green alone; use colour-blind-safe palettes (viridis, Seaborn's `"colorblind"`), add labels, markers or patterns, and keep enough contrast.

| Palette type | For | Seaborn / Matplotlib examples |
|---|---|---|
| Qualitative (categorical) | Unordered groups | `"colorblind"`, `"tab10"`, `"Set2"` |
| Sequential | Ordered values from low to high | `"viridis"`, `"Blues"` |
| Diverging | Values above and below a meaningful midpoint (correlation, change vs target) | `"coolwarm"`, `"RdBu"`, centred on 0 |

### Exam traps

> **Trap.** For a board presentation, lead with the recommendation and its business impact; methodology belongs in the appendix.

> **Trap.** A correlation heatmap needs a diverging palette centred on 0, so positive and negative correlations are visibly different.

## 5.2.2 Summarize key findings with evidence

**Syllabus asks:** identify and extract key findings; condense information into concise summaries; prioritize insights by context; explain why data-driven evidence matters; state the basis for claims and recommendations; present evidence that supports them.

### Core facts

**Finding what matters.** Go back to the original question and the decision it serves. A finding is key when it is relevant to that decision, large enough to matter in practice, and reliable (enough data, consistent across checks). Rank findings by impact; three strong points beat ten weak ones.

**Condensing.** Start with a two- or three-sentence summary. Give numbers context: compared with what (last year, a target, a control group), over what period, and in what units. "Churn fell from 8.1% to 6.4% after the loyalty launch in Q2" says more than "churn improved".

**Claim, evidence, reasoning.**

| Part | Example |
|---|---|
| Claim | Free-shipping thresholds raise average order value. |
| Evidence | In the A/B test (n = 12,400 orders, 4 weeks), the €50-threshold group averaged €58.20 vs €51.70 in the control group (95% CI of the difference: €4.90 to €8.10). |
| Reasoning | Customers added items to reach the threshold; the gain exceeds the extra shipping cost of €2.10 per order. |
| Recommendation | Roll out the €50 threshold and monitor margin monthly. |

**Good evidence** names the data source, time frame, sample size and method; shows the chart or table behind the claim; states uncertainty and limitations; and doesn't cherry-pick the favourable period or subgroup. Keep correlation and causation apart: observational data supports "is associated with", while a randomized experiment supports "causes".

### Exam traps

> **Trap.** A recommendation must follow from the evidence shown. A strong claim resting on a small or unrepresentative sample should be flagged as a limitation, not presented as proof.

> **Trap.** A percentage without its base can mislead: "sales doubled" from 3 units to 6 is not a trend.
