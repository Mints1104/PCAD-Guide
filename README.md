# PCAD Prep

Practice tests and a revision guide for the Python Institute **PCAD-31-02** exam (Certified Associate Data Analyst with Python), in the style of GAIL Prep.

**Live site: https://mints1104.github.io/PCAD-Guide/**

The build produces two copies of the same single-file app: `dist/pages/index.html`, a complete page deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`, and `dist/index.html`, the version published as a claude.ai artifact (where a Sync name carries progress across devices). On GitHub Pages, progress stays in the browser; Export progress and Import move it between devices.

None of the questions are real exam questions: all were written from the official syllabus and the library documentation, and every code answer is checked by running the code.

## Layout

| Path | Holds |
|---|---|
| `content/guide/` | Overview, one Markdown file per block (`## X.Y.Z Title` per objective), glossary, cheat sheet |
| `content/essentials/` | "Know this" facts, exam angles, traps, terms and map links per objective |
| `content/questions/src/` | Question sources (Python, using `Q()` from `qhelp.py`); compiled to `content/questions/*.json` |
| `content/maps/maps.json` | Decision maps |
| `content/cards/syntax.json` | Syntax flashcards |
| `content/notebooks/src/` | Notebook sources (Python, using `NB()` and `T()` from `nbhelp.py`); compiled to `content/notebooks/*.json` |
| `src/` | The Preact app (views, scoring, selection, sync) and `styles.css`; `runner.py` runs notebook cells, both in the browser and in `verify_notebooks.py` |
| `scripts/` | Build and verification scripts |

## Commands

```bash
python scripts/compile_questions.py   # question sources -> JSON
python scripts/compile_notebooks.py   # notebook sources -> JSON
python scripts/verify.py              # run every code question and check its keyed answer
python scripts/verify_guide.py        # run guide examples and compare with their printed output
python scripts/verify_cards.py        # run every syntax flashcard's answer against sample data
python scripts/verify_notebooks.py    # every notebook solution passes its check, every starter fails it
python scripts/render_charts.py       # run guide chart examples and save their images to content/guide/images/
node scripts/build.mjs                # validate all content and write dist/index.html
```

Run `npm install` once before the first build. Verification needs Python with pandas, NumPy, scikit-learn, Matplotlib, Seaborn, BeautifulSoup and requests.

## How answers are checked

- **Code questions** carry a `verify` spec, and `verify.py` runs the real code: the keyed option must match the output (and no wrong option may match it), or the named exception must be raised, or a custom check must pass. SQL questions run against SQLite.
- **Concept questions** were reviewed against the official PCAD-31-02 syllabus and primary sources: the Python, pandas, NumPy, scikit-learn, Matplotlib, Seaborn and SQLite documentation, PEP 8 and PEP 257, and the relevant standards (for example HTTP 429 in RFC 6585, robots.txt in RFC 9309).
- **Version independence:** the three checkers pass on Python 3.11 with pandas 2.2 / NumPy 1.26 / scikit-learn 1.5, on Python 3.13 with pandas 2.3 / NumPy 2.3 / scikit-learn 1.7, and on Python 3.13 with pandas 3.0 / NumPy 2.5 / scikit-learn 1.9 (last full audit: October 2026). Questions whose behaviour differs between versions say which version they mean.

## Notebooks

Each notebook is a setup cell and a list of tasks; a task has a prompt, starter code, a model solution and a check (plain `assert`s with messages the learner sees). On the site, Python runs in the browser through [Pyodide](https://pyodide.org) in a Web Worker (loaded from jsDelivr on the first run, with pandas, NumPy, scikit-learn, Matplotlib, BeautifulSoup and sqlite3 fetched as a task imports them). Run executes the setup and the cell; Check also runs the task's check. In a notebook marked `chain`, running a task first runs the learner's code for the earlier tasks. Every notebook also downloads as a `.ipynb` with a check cell under each task and the solutions at the end. Solved tasks and typed code are kept in the browser only.

`verify_notebooks.py` uses the same `src/runner.py` as the site: each solution must pass its check, each starter must fail it, and each notebook must also pass when run top to bottom in one namespace, as the downloaded `.ipynb` runs in Jupyter. The checks also pass under Pyodide 0.28 (pandas 2.3, scikit-learn 1.7).

## Adding a question

Add a `Q(...)` entry to the right `content/questions/src/blockN.py`. Give every wrong option a reason in `wrong`, and give code questions a `verify` spec (`"stdout"`, `"raises:Name"` or a `{"py": ...}` check) so `verify.py` can confirm the answer. Then compile, verify and build.
