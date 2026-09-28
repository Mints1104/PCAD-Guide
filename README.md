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
| `src/` | The Preact app (views, scoring, selection, sync) and `styles.css` |
| `scripts/` | Build and verification scripts |

## Commands

```bash
python scripts/compile_questions.py   # question sources -> JSON
python scripts/verify.py              # run every code question and check its keyed answer
python scripts/verify_guide.py        # run guide examples and compare with their printed output
node scripts/build.mjs                # validate all content and write dist/index.html
```

Run `npm install` once before the first build. Verification needs Python with pandas, NumPy, scikit-learn, Matplotlib, Seaborn and BeautifulSoup.

## Adding a question

Add a `Q(...)` entry to the right `content/questions/src/blockN.py`. Give every wrong option a reason in `wrong`, and give code questions a `verify` spec (`"stdout"`, `"raises:Name"` or a `{"py": ...}` check) so `verify.py` can confirm the answer. Then compile, verify and build.
