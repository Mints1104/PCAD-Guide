import { useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { STORAGE_PREFIX, blockOf } from '../constants.js';
import { NOTEBOOKS, NOTEBOOK_BY_ID, guideHref, objectiveTitle } from '../data.js';
import { highlight } from '../highlight.js';
import { LEVEL_NAMES, downloadIpynb } from '../ipynb.js';
import { runPython, stopPython, usePython } from '../python.js';
import { readLocal, writeLocal } from '../store.js';
import { BlockBadge, CodeBlock, Icon, blockStyle, renderMarkdown } from '../ui.jsx';

// Solved tasks and the code typed into each cell stay in this browser (not part of synced progress).
const NB_KEY = `${STORAGE_PREFIX}:notebooks:v1`;
const isObj = (v) => typeof v === 'object' && v !== null && !Array.isArray(v);

function loadNbState() {
  const s = readLocal(NB_KEY);
  return isObj(s) && isObj(s.solved) && isObj(s.code) ? s : { solved: {}, code: {} };
}

const LEVEL_BLURB = {
  1: 'One idea per task, with the data already in place.',
  2: 'Exam-level tasks on one syllabus area.',
  3: 'Multi-step tasks and edge cases, above exam level.',
};

const taskKey = (nb, t) => `${nb.id}/${t.id}`;
const solvedIn = (nb, state) => nb.tasks.filter((t) => state.solved[taskKey(nb, t)]).length;

export function Notebooks({ id }) {
  if (!id) return <NotebookIndex />;
  const nb = NOTEBOOK_BY_ID.get(id);
  if (!nb) {
    return (
      <main class="page">
        <a class="back-link" href="#/notebooks">
          ← Notebooks
        </a>
        <p>That notebook does not exist.</p>
      </main>
    );
  }
  return <NotebookView key={id} nb={nb} />;
}

function NotebookIndex() {
  const state = useMemo(loadNbState, []);
  const tasks = NOTEBOOKS.reduce((s, nb) => s + nb.tasks.length, 0);
  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Notebooks</h1>
      <p class="muted">
        {NOTEBOOKS.length} notebooks, {tasks} tasks. Write Python for each task and press Check to see if it is right. Python runs in this browser; each notebook also downloads as a Jupyter notebook (.ipynb) with the same checks.
      </p>
      {[1, 2, 3].map((level) => (
        <section key={level}>
          <h2>{LEVEL_NAMES[level]}</h2>
          <p class="hint">{LEVEL_BLURB[level]}</p>
          <ul class="row-list">
            {NOTEBOOKS.filter((nb) => nb.level === level).map((nb) => {
              const solved = solvedIn(nb, state);
              const blocks = [...new Set(nb.objectives.map(blockOf))];
              return (
                <li key={nb.id}>
                  <a class="row-link nb-row" href={`#/notebooks/${nb.id}`}>
                    <span class="row-link-title">
                      {nb.title}
                      <span class="nb-row-summary">{nb.summary}</span>
                    </span>
                    <span class="chip-group">
                      {blocks.map((b) => (
                        <BlockBadge key={b} block={b} />
                      ))}
                    </span>
                    <span class={`row-link-meta muted ${solved === nb.tasks.length ? 'nb-done' : ''}`}>
                      {solved > 0 ? `${solved} of ${nb.tasks.length} solved` : `${nb.tasks.length} tasks`}
                    </span>
                  </a>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </main>
  );
}

function NotebookView({ nb }) {
  const [state, setState] = useState(loadNbState);
  const saveTimer = useRef(null);
  const latest = useRef(state);
  latest.current = state;
  const intro = useMemo(() => renderMarkdown(nb.intro), [nb]);
  const python = usePython();

  // Code is saved shortly after typing stops; solved marks are saved at once.
  function persist(next, now) {
    clearTimeout(saveTimer.current);
    if (now) writeLocal(NB_KEY, next);
    else saveTimer.current = setTimeout(() => writeLocal(NB_KEY, latest.current), 400);
  }
  useEffect(
    () => () => {
      clearTimeout(saveTimer.current);
      writeLocal(NB_KEY, latest.current);
    },
    [],
  );

  const codeOf = (t) => state.code[taskKey(nb, t)] ?? t.starter;
  function setCode(t, value) {
    const code = { ...latest.current.code };
    if (value === t.starter) delete code[taskKey(nb, t)];
    else code[taskKey(nb, t)] = value;
    const next = { ...latest.current, code };
    latest.current = next;
    setState(next);
    persist(next, false);
  }
  function markSolved(t) {
    if (latest.current.solved[taskKey(nb, t)]) return;
    const next = { ...latest.current, solved: { ...latest.current.solved, [taskKey(nb, t)]: Date.now() } };
    latest.current = next;
    setState(next);
    persist(next, true);
  }

  const solved = solvedIn(nb, state);
  return (
    <main class="page notebook">
      <a class="back-link" href="#/notebooks">
        ← Notebooks
      </a>
      <p class="nb-eyebrow">
        {LEVEL_NAMES[nb.level]} · {nb.tasks.length} tasks{solved > 0 ? ` · ${solved} solved` : ''}
      </p>
      <h1>{nb.title}</h1>
      <div class="chip-group nb-objectives">
        {nb.objectives.map((o) => (
          <a key={o} class="pill nb-pill" style={blockStyle(blockOf(o))} href={guideHref(o)} title={`Revision guide: ${objectiveTitle(o)}`}>
            {o} {objectiveTitle(o)}
          </a>
        ))}
      </div>
      <div class="nb-intro guide" dangerouslySetInnerHTML={{ __html: intro }} />
      <div class="nb-toolbar">
        <button class="btn" onClick={() => downloadIpynb(nb)}>
          Download .ipynb
        </button>
        <PythonStatus python={python} />
      </div>

      <details class="nb-setup" open>
        <summary>Setup{nb.chain ? '' : ' · runs before every task'}</summary>
        <CodeBlock code={nb.setup} />
      </details>

      {nb.tasks.map((t, i) => (
        <TaskCell
          key={t.id}
          nb={nb}
          task={t}
          index={i}
          code={codeOf(t)}
          onCode={(v) => setCode(t, v)}
          solved={Boolean(state.solved[taskKey(nb, t)])}
          onSolved={() => markSolved(t)}
          before={() => (nb.chain ? nb.tasks.slice(0, i).map((p) => latest.current.code[taskKey(nb, p)] ?? p.starter) : [])}
          python={python}
        />
      ))}
    </main>
  );
}

function PythonStatus({ python }) {
  const text = {
    off: 'Python starts on your first run.',
    starting: 'Starting Python…',
    packages: 'Loading packages…',
    running: 'Running…',
    ready: 'Python is ready.',
    failed: `Python could not start here${python.message ? ` (${python.message})` : ''}. The .ipynb download runs in Jupyter or VS Code instead.`,
  }[python.phase];
  return <p class={`nb-status ${python.phase === 'failed' ? 'nb-status-failed' : ''}`}>{text}</p>;
}

const BUSY = new Set(['starting', 'packages', 'running']);

function TaskCell({ nb, task, index, code, onCode, solved, onSolved, before, python }) {
  const [out, setOut] = useState(null);
  const [pending, setPending] = useState(null);
  const [hints, setHints] = useState(0);
  const [undo, setUndo] = useState(null);
  const prompt = useMemo(() => renderMarkdown(task.prompt), [task]);
  const busy = BUSY.has(python.phase);

  async function run(withCheck) {
    if (busy) return;
    setPending(withCheck ? 'check' : 'run');
    const res = await runPython({ setup: nb.setup, code, check: withCheck ? task.check : null, before: before() });
    setPending(null);
    setOut(res);
    if (res.result?.check?.ok) onSolved();
  }

  function reset() {
    setUndo(code);
    onCode(task.starter);
    setOut(null);
  }

  return (
    <section class={`card nb-task ${solved ? 'nb-task-solved' : ''}`} aria-labelledby={`task-${task.id}`}>
      <h2 id={`task-${task.id}`} class="nb-task-title">
        <span class="nb-task-num">Task {index + 1}</span> {task.title}
        {solved && (
          <span class="nb-solved-mark" title="Solved">
            <Icon name="check" size={18} />
            <span class="sr-only">Solved</span>
          </span>
        )}
      </h2>
      <div class="nb-prompt guide" dangerouslySetInnerHTML={{ __html: prompt }} />
      <CodeEditor
        value={code}
        label={`Code for task ${index + 1}`}
        onInput={(v) => {
          setUndo(null);
          onCode(v);
        }}
        onRun={() => run(false)}
      />
      <div class="nb-actions">
        <button class="btn" onClick={() => run(false)} disabled={busy} title="Run (Shift+Enter)">
          {pending === 'run' ? 'Running…' : 'Run'}
        </button>
        <button class="btn btn-primary" onClick={() => run(true)} disabled={busy}>
          {pending === 'check' ? 'Checking…' : 'Check'}
        </button>
        {pending !== null && (
          <button class="btn" onClick={stopPython}>
            Stop
          </button>
        )}
        <span class="nb-actions-spacer" />
        {hints < task.hints.length && (
          <button class="link-btn" onClick={() => setHints((h) => h + 1)}>
            Hint{task.hints.length > 1 ? ` ${hints + 1} of ${task.hints.length}` : ''}
          </button>
        )}
        {undo !== null ? (
          <button
            class="link-btn"
            onClick={() => {
              onCode(undo);
              setUndo(null);
            }}
          >
            Undo reset
          </button>
        ) : (
          code !== task.starter && (
            <button class="link-btn" onClick={reset}>
              Reset
            </button>
          )
        )}
      </div>
      {pending !== null && python.phase !== 'running' && (
        <p class="nb-loading">
          {python.phase === 'starting' ? 'Starting Python (first run only)…' : 'Loading packages…'} {python.message && <span class="muted">{python.message}</span>}
        </p>
      )}
      {hints > 0 && (
        <ul class="nb-hints">
          {task.hints.slice(0, hints).map((h, i) => (
            <li key={i} dangerouslySetInnerHTML={{ __html: renderMarkdown(h).replace(/^<p>|<\/p>\s*$/g, '') }} />
          ))}
        </ul>
      )}
      <Output out={out} />
      <details class="nb-solution">
        <summary>Solution</summary>
        <CodeBlock code={task.solution} />
      </details>
    </section>
  );
}

function Output({ out }) {
  if (!out) return null;
  if (out.stopped || out.fatal) {
    return (
      <div class="nb-out" aria-live="polite">
        <pre class="nb-error">{out.stopped ?? out.fatal}</pre>
      </div>
    );
  }
  const r = out.result;
  const nothing = !r.setup_error && !r.stdout && !r.error && !r.display && r.figures.length === 0 && !r.check;
  return (
    <div class="nb-out" aria-live="polite">
      {r.setup_error && <pre class="nb-error">The setup failed: {r.setup_error}</pre>}
      {r.stdout && <pre class="nb-stdout">{r.stdout}</pre>}
      {r.error && <pre class="nb-error">{r.error}</pre>}
      {r.display?.html && <div class="nb-html table-wrap" dangerouslySetInnerHTML={{ __html: r.display.html }} />}
      {r.display?.text !== undefined && <pre class="nb-stdout">{r.display.text}</pre>}
      {r.figures.map((b64, i) => (
        <img key={i} class="nb-figure" src={`data:image/png;base64,${b64}`} alt={`Figure ${i + 1} drawn by this cell`} />
      ))}
      {r.check && (
        <p class={`nb-check ${r.check.ok ? 'nb-check-ok' : 'nb-check-bad'}`}>
          <Icon name={r.check.ok ? 'check' : 'cross'} size={18} />
          <span>{r.check.ok ? 'Correct.' : r.check.message}</span>
        </p>
      )}
      {nothing && <p class="muted nb-empty">Ran with no output. End the cell with an expression, or print(), to see a value.</p>}
    </div>
  );
}

// ---------- editor: a textarea over a highlighted copy of the same text ----------

const INDENT = '    ';

function insertText(ta, text) {
  ta.focus();
  // execCommand keeps the browser's undo history; setRangeText is the fallback.
  if (!document.execCommand('insertText', false, text)) {
    ta.setRangeText(text, ta.selectionStart, ta.selectionEnd, 'end');
    ta.dispatchEvent(new Event('input', { bubbles: true }));
  }
}

function shiftLines(ta, dedent) {
  const { value, selectionStart: s, selectionEnd: e } = ta;
  const start = value.lastIndexOf('\n', s - 1) + 1;
  let end = e > s && value[e - 1] === '\n' ? e - 1 : e;
  const nl = value.indexOf('\n', end);
  end = nl === -1 ? value.length : nl;
  const block = value.slice(start, end);
  const lines = block.split('\n');
  const changed = lines.map((l) => (dedent ? l.replace(/^ {1,4}/, '') : INDENT + l)).join('\n');
  if (changed === block) return;
  ta.setSelectionRange(start, end);
  insertText(ta, changed);
  if (lines.length > 1) ta.setSelectionRange(start, start + changed.length);
  else {
    const moved = dedent ? Math.max(start, s - (block.length - changed.length)) : s + INDENT.length;
    ta.setSelectionRange(moved, moved);
  }
}

function CodeEditor({ value, label, onInput, onRun }) {
  const escaped = useRef(false);

  function onKeyDown(e) {
    const ta = e.currentTarget;
    if (e.key === 'Enter' && (e.shiftKey || e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onRun();
      return;
    }
    if (e.key === 'Escape') {
      escaped.current = true; // the next Tab moves focus out instead of indenting
      return;
    }
    if (e.key === 'Tab' && !e.ctrlKey && !e.altKey && !e.metaKey) {
      if (escaped.current) {
        escaped.current = false;
        return;
      }
      e.preventDefault();
      const multi = ta.value.slice(ta.selectionStart, ta.selectionEnd).includes('\n');
      if (e.shiftKey || multi) shiftLines(ta, e.shiftKey);
      else insertText(ta, INDENT);
      return;
    }
    escaped.current = false;
    if (e.key === 'Enter' && !e.altKey) {
      e.preventDefault();
      const head = ta.value.slice(ta.value.lastIndexOf('\n', ta.selectionStart - 1) + 1, ta.selectionStart);
      const indent = head.match(/^ */)[0];
      insertText(ta, `\n${indent}${/:\s*$/.test(head) ? INDENT : ''}`);
    }
  }

  return (
    <div class="nb-editor">
      <pre aria-hidden="true">
        <code dangerouslySetInnerHTML={{ __html: highlight(value, 'python') + (value.endsWith('\n') || value === '' ? ' ' : '') }} />
      </pre>
      <textarea
        value={value}
        aria-label={label}
        spellcheck={false}
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        onInput={(e) => onInput(e.currentTarget.value)}
        onKeyDown={onKeyDown}
      />
    </div>
  );
}
