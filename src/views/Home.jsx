import { useState } from 'preact/hooks';
import { BLOCKS, BLOCK_NAMES, EXAM, OBJECTIVE_IDS, STORAGE_PREFIX } from '../constants.js';
import { QUESTIONS, QUESTION_BY_ID } from '../data.js';
import { blockAccuracy, emptyProgress, readiness } from '../score.js';
import { cleanSyncName, parseProgress, readLocal, writeLocal } from '../store.js';
import { barStyle } from '../ui.jsx';

const HELP_SEEN_KEY = `${STORAGE_PREFIX}:help-seen`;

const codeCount = () => QUESTIONS.filter((q) => q.kind === 'code').length;

function StartHere() {
  const [hidden, setHidden] = useState(() => readLocal(HELP_SEEN_KEY) === 1);
  if (hidden) return null;
  return (
    <section class="card start-here">
      <h2>Start here</h2>
      <ul>
        <li>
          <b>Mock test</b> mirrors the exam: {EXAM.items} questions in {EXAM.minutes} minutes, one from each syllabus objective, no feedback until the end.
        </li>
        <li>
          <b>Practice</b> checks each answer at once and explains why the other options are wrong.
        </li>
        <li>
          <b>Revision guide</b> shows the essentials for each objective first; the full notes are one tap below.
        </li>
        <li>
          Progress stays in this browser unless you set a <b>Sync name</b> (bottom of this page). Sharing the link? Use your own name.
        </li>
        <li>
          None of these are real exam questions. All {QUESTIONS.length} were written from the official PCAD-31-02 syllabus, and {codeCount()} ask you to read Python or SQL. Every code answer was checked by running the code.
        </li>
      </ul>
      <div class="actions">
        <button
          class="btn btn-primary"
          onClick={() => {
            writeLocal(HELP_SEEN_KEY, 1);
            setHidden(true);
          }}
        >
          Got it
        </button>
        <a class="btn" href="#/help">
          How this works
        </a>
      </div>
    </section>
  );
}

export function Home({ store }) {
  const { progress, session, setProgress, setSession, syncStatus, syncName, setSyncName } = store;
  const [nameInput, setNameInput] = useState(syncName ?? '');
  const [message, setMessage] = useState(null);
  const [exported, setExported] = useState(null);
  const [importOpen, setImportOpen] = useState(false);
  const [importText, setImportText] = useState('');
  const [confirmReset, setConfirmReset] = useState(false);
  const [confirmLoad, setConfirmLoad] = useState(null);
  const [loaded, setLoaded] = useState(null);

  const ready = readiness(progress, QUESTIONS, QUESTION_BY_ID);
  const blocks = blockAccuracy(progress, QUESTION_BY_ID);
  const canResume = session !== null && session.submittedAt === null;
  const syncAvailable = typeof window !== 'undefined' && window.claude !== undefined;
  const typedName = cleanSyncName(nameInput);
  const alreadyLoaded = syncName !== null && typedName === syncName;

  function save() {
    setLoaded(null);
    if (nameInput.trim() === '') {
      setSyncName(null);
      return;
    }
    if (typedName === null) {
      setMessage('Sync names use 2 to 32 letters, digits, dashes or underscores.');
      return;
    }
    setMessage(null);
    setSyncName(typedName);
  }

  async function switchTo(name) {
    setConfirmLoad(null);
    await setSyncName(name, 'replace');
    setLoaded(name);
  }

  function load() {
    if (typedName === null || alreadyLoaded) return;
    if (JSON.stringify(progress) === JSON.stringify(emptyProgress())) switchTo(typedName);
    else setConfirmLoad(typedName);
  }

  async function exportProgress() {
    const text = JSON.stringify(progress);
    setExported(text);
    try {
      await navigator.clipboard.writeText(text);
      setMessage('Progress copied to the clipboard. Paste it into Import on another device.');
    } catch {
      setMessage('Copy the text below and paste it into Import on another device.');
    }
  }

  function doImport() {
    try {
      setProgress(parseProgress(JSON.parse(importText)));
      setImportText('');
      setImportOpen(false);
      setMessage('Progress imported.');
    } catch {
      setMessage('That text is not valid PCAD Prep progress. Paste the whole export, starting with {"version":1.');
    }
  }

  function reset() {
    setProgress(emptyProgress());
    setSession(null);
    setConfirmReset(false);
    setMessage('Progress reset.');
  }

  return (
    <main class="page">
      <header class="hero">
        <p class="hero-code">{EXAM.code}</p>
        <h1>PCAD Prep</h1>
        <p class="subtitle">Python Institute Certified Associate Data Analyst with Python — practice tests</p>
      </header>

      <StartHere />

      <section class="card">
        <h2>Readiness</h2>
        <p class="readiness-pct">{Math.round(ready.pct)}%</p>
        <p class="muted">
          Coverage: {Math.round(ready.coverage * 100)}% of {QUESTIONS.length} questions seen
        </p>
        <p class="muted">Pass mark: {Math.round(EXAM.pass * 100)}%</p>
        <p class="muted">
          Guide: {progress.revised.length} of {OBJECTIVE_IDS.length} objectives revised
        </p>
        <div class="bars">
          {BLOCKS.map((b) => (
            <div class="bar-row" key={b}>
              <span class="bar-label">
                <span class="bar-block" style={`color:var(--b${b})`}>
                  B{b}
                </span>{' '}
                {BLOCK_NAMES[b]}
              </span>
              <div class="bar-track">
                <div class="bar-fill" style={barStyle(blocks[b].pct, b)} />
              </div>
              <span class="bar-pct">{Math.round(blocks[b].pct)}%</span>
            </div>
          ))}
        </div>
      </section>

      <div class="actions">
        {canResume && (
          <a class="btn btn-outline-accent" href="#/test">
            Resume {session.mode === 'mock' ? 'mock test' : 'practice'}
          </a>
        )}
        <a class="btn btn-primary" href="#/mock">
          Start mock test
        </a>
        <a class="btn" href="#/practice">
          Practice
        </a>
      </div>
      <a class="btn btn-block" href="#/guide">
        Revision guide
      </a>
      <div class="actions-secondary">
        <a class="btn" href="#/maps">
          Decision maps
        </a>
        <a class="btn" href="#/cards">
          Cards
        </a>
        <a class="btn" href="#/browse">
          Browse questions
        </a>
        <a class="btn" href="#/stats">
          Stats
        </a>
      </div>
      <p class="muted center">{QUESTIONS.length} questions in the bank</p>

      <div class="sync-row">
        {!syncAvailable ? (
          <p class="muted center">Progress is saved in this browser. To move it to another device, use Export progress and Import below.</p>
        ) : (
          <>
            <label class="sync-label" for="sync-name">
              Sync name
            </label>
            <div class="filter-row">
              <input id="sync-name" type="text" value={nameInput} onInput={(e) => setNameInput(e.currentTarget.value)} placeholder="e.g. amara" autocomplete="off" />
              <button class="btn" onClick={save}>
                Save
              </button>
              <button class="btn" onClick={load} disabled={alreadyLoaded || typedName === null}>
                Load
              </button>
            </div>
            <p class="hint">Save merges this device's progress into that name. Load switches this device to that name's progress; a new name starts blank.</p>
            {loaded !== null && <p class="muted center">Loaded {loaded}</p>}
            {syncStatus === 'connecting' && <p class="muted center">Connecting…</p>}
            {syncStatus === 'synced' && syncName !== null && <p class="muted center">Synced across devices as {syncName}</p>}
            {syncStatus === 'error' && <p class="muted center">Sync error. Progress is still saved on this device.</p>}
          </>
        )}
      </div>

      <footer class="footer">
        <button class="link-btn" onClick={exportProgress}>
          Export progress
        </button>
        <button class="link-btn" onClick={() => setImportOpen((v) => !v)}>
          Import
        </button>
        <button class="link-btn danger" onClick={() => setConfirmReset(true)}>
          Reset
        </button>
        <a class="link-btn" href="#/help">
          How this works
        </a>
      </footer>

      {confirmReset && (
        <div class="import-box confirm-inline" role="alertdialog" aria-labelledby="confirm-reset-title">
          <p id="confirm-reset-title" class="confirm-title">
            Reset all progress? This cannot be undone.
          </p>
          <div class="actions">
            <button class="btn btn-danger" onClick={reset}>
              Reset
            </button>
            <button class="btn" onClick={() => setConfirmReset(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}
      {confirmLoad !== null && (
        <div class="import-box confirm-inline" role="alertdialog" aria-labelledby="confirm-load-title">
          <p id="confirm-load-title" class="confirm-title">
            {syncName !== null
              ? `Switch to ${confirmLoad}? This device's current progress stays saved under ${syncName}.`
              : `Switch to ${confirmLoad}? This device's progress is not saved under any name and will be replaced. Export it first to keep a copy.`}
          </p>
          <div class="actions">
            <button class="btn btn-danger" onClick={() => switchTo(confirmLoad)}>
              Switch
            </button>
            <button class="btn" onClick={() => setConfirmLoad(null)}>
              Cancel
            </button>
          </div>
        </div>
      )}
      {exported !== null && (
        <div class="import-box">
          <textarea id="export-text" value={exported} readOnly rows={6} onFocus={(e) => e.currentTarget.select()} />
          <button class="btn" onClick={() => setExported(null)}>
            Close
          </button>
        </div>
      )}
      {importOpen && (
        <div class="import-box">
          <textarea id="import-text" value={importText} onInput={(e) => setImportText(e.currentTarget.value)} placeholder="Paste exported progress here" rows={6} />
          <button class="btn btn-primary" onClick={doImport}>
            Import
          </button>
        </div>
      )}
      {message && <p class="message">{message}</p>}
    </main>
  );
}

const HELP = [
  {
    title: 'Mock test',
    body: `${EXAM.items} questions in ${EXAM.minutes} minutes, single- and multiple-select, like the real ${EXAM.code}. A full mock draws one question from each of the 48 syllabus objectives, which gives the official block split of 14 / 16 / 4 / 9 / 5. Shorter 12- and 24-question mocks keep the same proportions and the same time per question. No feedback until you finish; results break down by block and objective, and every question can be reviewed with its explanation.`,
  },
  {
    title: 'Mixes',
    body: 'Blueprint mix follows the syllabus with mostly apply-level questions. Code-heavy mix prefers questions where you read Python, pandas or SQL and predict what happens. Harder mix pulls the analyze-level questions first; it is above exam level.',
  },
  {
    title: 'Practice',
    body: 'Pick blocks, objectives or question kind (code reading or concept). Each answer is checked at once, with the explanation, why each other option is wrong, and a link to the guide section it tests.',
  },
  {
    title: 'Revision guide',
    body: 'Every objective opens with "Know this" and the exam angle on each fact. The full notes, with runnable examples, sit underneath. Use "Try 5 questions" after reading, and tick "Mark as revised" to track coverage.',
  },
  {
    title: 'Decision maps',
    body: 'For the "which method, chart or join?" questions: answer two to four questions and land on the technique the syllabus expects, with a link to the notes.',
  },
  {
    title: 'Cards',
    body: 'A question on the front, the answer on the back. Decks for the glossary, pandas / SQL / Python syntax, each block and each objective.',
  },
  {
    title: 'Scoring',
    body: `The pass mark is ${Math.round(EXAM.pass * 100)}%, the Python Institute's published cumulative score. PCAD Prep scores multiple-select questions all-or-nothing, since the Institute does not publish partial-credit rules. Readiness weights your recent accuracy by each block's share of the 48 exam items.`,
  },
  {
    title: 'Your progress',
    body: 'Progress is kept in this browser. To carry it to another device, type the same Sync name on both and press Save. Load switches this device to another name (a new name starts blank). If several people use this link, each should choose their own name.',
  },
  {
    title: 'Where the questions come from',
    body: `All ${QUESTIONS.length} questions were written for PCAD Prep from the official PCAD-31-02 syllabus and the Python, pandas, NumPy, Matplotlib, Seaborn, scikit-learn and sqlite3 documentation. Each one names the objective it tests. Code answers were checked by running the code with pandas 3 and NumPy 2. Leaked "exam dump" questions were deliberately not used.`,
  },
];

export function Help() {
  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>How this works</h1>
      <p class="muted">Practice tests and a revision guide for the Python Institute {EXAM.code} exam, built from the official syllabus.</p>
      <dl class="help-list">
        {HELP.map((h) => (
          <div class="help-item" key={h.title}>
            <dt>{h.title}</dt>
            <dd>{h.body}</dd>
          </div>
        ))}
      </dl>
    </main>
  );
}
