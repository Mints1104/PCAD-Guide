import { useMemo, useState } from 'preact/hooks';
import { BLOCKS, BLOCK_NAMES, DIFFICULTY_LABELS, EXAM, OBJECTIVES, OBJECTIVE_IDS, blockOf } from '../constants.js';
import { QUESTIONS, QUESTION_BY_ID, guideHref, optionLang } from '../data.js';
import { blockAccuracy, difficultyAccuracy, objectiveAccuracy, toggleBookmark, wrongIds } from '../score.js';
import { formatClock } from '../select.js';
import { BlockBadge, Icon, Rich, barStyle } from '../ui.jsx';
import { QuestionBody } from './Test.jsx';
import { startPractice } from './Setup.jsx';

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

function plain(text, n) {
  const t = text.replace(/`/g, '').replace(/\*\*/g, '').replace(/\s+/g, ' ');
  return t.length > n ? `${t.slice(0, n).trimEnd()}…` : t;
}

export function Browse({ store, id }) {
  return id ? <QuestionDetail store={store} id={id} /> : <BrowseList progress={store.progress} />;
}

function BrowseList({ progress }) {
  const [search, setSearch] = useState('');
  const [blocks, setBlocks] = useState(() => new Set());
  const [objective, setObjective] = useState('');
  const [kind, setKind] = useState('all');
  const [bookmarked, setBookmarked] = useState(false);
  const [wrong, setWrong] = useState(false);
  const marks = useMemo(() => new Set(progress.bookmarks), [progress.bookmarks]);
  const wrongSet = useMemo(() => new Set(wrongIds(progress, QUESTIONS)), [progress]);

  const list = useMemo(() => {
    const s = search.trim().toLowerCase();
    return QUESTIONS.filter((q) => {
      if (blocks.size > 0 && !blocks.has(q.block)) return false;
      if (objective && q.objective !== objective) return false;
      if (kind !== 'all' && q.kind !== kind) return false;
      if (bookmarked && !marks.has(q.id)) return false;
      if (wrong && !wrongSet.has(q.id)) return false;
      if (s && !`${q.stem} ${q.code ?? ''} ${q.options.join(' ')} ${q.tags.join(' ')}`.toLowerCase().includes(s)) return false;
      return true;
    });
  }, [search, blocks, objective, kind, bookmarked, wrong, marks, wrongSet]);

  function toggleBlock(b) {
    setBlocks((prev) => {
      const n = new Set(prev);
      n.has(b) ? n.delete(b) : n.add(b);
      return n;
    });
  }

  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Browse questions</h1>
      <input id="browse-search" class="browse-search" type="search" placeholder="Search stems, code, options, tags…" value={search} onInput={(e) => setSearch(e.currentTarget.value)} />
      <div class="chip-group">
        {BLOCKS.map((b) => (
          <button key={b} class={`chip ${blocks.has(b) ? 'chip-selected' : ''}`} title={BLOCK_NAMES[b]} onClick={() => toggleBlock(b)}>
            B{b}
          </button>
        ))}
        <button class={`chip ${bookmarked ? 'chip-selected' : ''}`} onClick={() => setBookmarked((v) => !v)}>
          Bookmarked
        </button>
        <button class={`chip ${wrong ? 'chip-selected' : ''}`} onClick={() => setWrong((v) => !v)}>
          Answered wrong
        </button>
      </div>
      <div class="chip-group">
        {[
          ['all', 'Any kind'],
          ['code', 'Code reading'],
          ['concept', 'Concept'],
        ].map(([k, label]) => (
          <button key={k} class={`chip ${kind === k ? 'chip-selected' : ''}`} onClick={() => setKind(k)}>
            {label}
          </button>
        ))}
      </div>
      <select id="browse-objective" class="browse-objective" value={objective} onChange={(e) => setObjective(e.currentTarget.value)}>
        <option value="">All objectives</option>
        {OBJECTIVE_IDS.map((o) => (
          <option key={o} value={o}>
            {o} — {OBJECTIVES[o]}
          </option>
        ))}
      </select>
      <p class="muted">{list.length} question(s)</p>
      <ul class="browse-list">
        {list.map((q) => {
          const s = progress.stats[q.id];
          return (
            <li key={q.id}>
              <a class="browse-item" href={`#/browse/${q.id}`}>
                <BlockBadge block={q.block} />
                <span class="browse-item-stem">{plain(q.stem, 96)}</span>
                {q.kind === 'code' && <span class="kind-tag">code</span>}
                <span class={`browse-item-mark ${s ? (s.lastCorrect ? 'correct' : 'incorrect') : ''}`}>{s ? <Icon name={s.lastCorrect ? 'check' : 'cross'} size={16} /> : '–'}</span>
                <span class="browse-item-star">{marks.has(q.id) && <Icon name="bookmark-filled" size={14} />}</span>
              </a>
            </li>
          );
        })}
      </ul>
    </main>
  );
}

function QuestionDetail({ store, id }) {
  const q = QUESTION_BY_ID.get(id);
  if (!q) {
    window.location.hash = '#/browse';
    return null;
  }
  const marked = store.progress.bookmarks.includes(q.id);
  return (
    <main class="page">
      <a class="back-link" href="#/browse">
        ← Browse questions
      </a>
      <p class="muted detail-meta">
        <BlockBadge block={q.block} /> {q.id} · {DIFFICULTY_LABELS[q.difficulty]} · {q.type === 'multi' ? 'multiple-select' : 'single-select'}
      </p>
      <QuestionBody q={q} />
      <div class="options">
        {q.options.map((o, i) => {
          const right = q.answer.includes(i);
          return (
            <div key={i} class={`option option-static${right ? ' option-correct' : ''}`}>
              <span class="option-letter">{LETTERS[i]}</span>
              <Rich class="option-text" text={o} lang={optionLang(q)} />
              {!right && q.why_wrong[i] && <Rich class="why-wrong" text={q.why_wrong[i]} />}
            </div>
          );
        })}
      </div>
      <div class="feedback">
        <Rich as="p" class="explanation" text={q.explanation} />
        <p class="source">
          Source: {q.source} ·{' '}
          <a class="nav-link" href={guideHref(q.objective)}>
            Read {q.objective} in the guide →
          </a>
        </p>
        <p class="muted">Tags: {q.tags.join(', ') || '—'}</p>
      </div>
      <button class="btn bookmark-btn" onClick={() => store.setProgress(toggleBookmark(store.progress, q.id))}>
        <Icon name={marked ? 'bookmark-filled' : 'bookmark'} size={18} />
        {marked ? 'Bookmarked' : 'Bookmark'}
      </button>
    </main>
  );
}

function when(ts) {
  return new Date(ts).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}

export function Stats({ store }) {
  const { progress } = store;
  const blocks = blockAccuracy(progress, QUESTION_BY_ID);
  const objs = useMemo(() => objectiveAccuracy(progress, QUESTION_BY_ID), [progress]);
  const diffs = useMemo(() => difficultyAccuracy(progress, QUESTION_BY_ID), [progress]);
  const attempted = OBJECTIVE_IDS.filter((o) => objs[o]?.total > 0);
  const untouched = OBJECTIVE_IDS.filter((o) => !(objs[o]?.total > 0));
  const weakest = attempted
    .slice()
    .sort((a, b) => objs[a].pct - objs[b].pct)
    .slice(0, 3);
  const mocks = progress.mocks.slice().reverse();

  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Stats</h1>
      <section class="card">
        <h2>Mock history</h2>
        {mocks.length === 0 ? (
          <p class="muted">No mock tests taken yet.</p>
        ) : (
          <div class="table-wrap">
            <table class="results-table">
              <thead>
                <tr>
                  <th>When</th>
                  <th>Score</th>
                  <th>Correct</th>
                  <th>Time</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                {mocks.map((m) => {
                  const p = m.total > 0 ? Math.round((m.correct / m.total) * 100) : 0;
                  const open = () => (window.location.hash = `#/results/${m.id}`);
                  const inHistory = progress.history.some((h) => h.id === m.id);
                  return (
                    <tr key={m.id} class={inHistory ? 'row-clickable' : ''} tabIndex={inHistory ? 0 : undefined} role={inHistory ? 'link' : undefined} onClick={inHistory ? open : undefined} onKeyDown={(e) => inHistory && e.key === 'Enter' && open()}>
                      <td>{when(m.at)}</td>
                      <td>{p}%</td>
                      <td>
                        {m.correct} / {m.total}
                      </td>
                      <td>{formatClock(m.durationSec)}</td>
                      <td>
                        <span class={p >= EXAM.pass * 100 ? 'pass-label pass' : 'pass-label fail'}>{p >= EXAM.pass * 100 ? 'Pass' : 'Below'}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section class="card">
        <h2>Block readiness</h2>
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

      <button
        class="btn btn-primary btn-large"
        disabled={weakest.length === 0}
        onClick={() => startPractice(store, { count: 20, objectives: weakest })}
      >
        {weakest.length === 0 ? 'Practice my weakest objectives (answer some questions first)' : `Practice my weakest ${weakest.length}: ${weakest.join(', ')}`}
      </button>

      <section class="card stats-gap">
        <h2>Accuracy by difficulty</h2>
        <div class="table-wrap">
          <table class="results-table">
            <thead>
              <tr>
                <th>Difficulty</th>
                <th>Correct</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3].map((d) => (
                <tr key={d}>
                  <td class={diffs[d].total ? '' : 'muted'}>{DIFFICULTY_LABELS[d]}</td>
                  <td class={diffs[d].total ? '' : 'muted'}>{diffs[d].total ? `${diffs[d].correct} / ${diffs[d].total}` : '—'}</td>
                  <td class={diffs[d].total ? '' : 'muted'}>{diffs[d].total ? `${Math.round(diffs[d].pct)}%` : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section class="card">
        <h2>Objective accuracy</h2>
        <div class="table-wrap">
          <table class="results-table">
            <thead>
              <tr>
                <th>Objective</th>
                <th>Correct</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              {attempted
                .slice()
                .sort((a, b) => objs[a].pct - objs[b].pct)
                .map((o) => (
                  <tr key={o}>
                    <td>
                      <BlockBadge block={blockOf(o)} /> {o} {OBJECTIVES[o]}
                    </td>
                    <td>
                      {objs[o].correct} / {objs[o].total}
                    </td>
                    <td>{Math.round(objs[o].pct)}%</td>
                  </tr>
                ))}
              {untouched.length > 0 && (
                <tr class="stats-divider">
                  <td colSpan={3}>Not yet attempted ({untouched.length})</td>
                </tr>
              )}
              {untouched.map((o) => (
                <tr key={o}>
                  <td class="muted">
                    {o} {OBJECTIVES[o]}
                  </td>
                  <td class="muted">—</td>
                  <td class="muted">—</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
