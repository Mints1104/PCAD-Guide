import { useCallback, useEffect, useState } from 'preact/hooks';
import { BLOCKS, BLOCK_NAMES, EXAM, OBJECTIVES, blockOf } from '../constants.js';
import { QUESTION_BY_ID, guideHref, optionLang } from '../data.js';
import { isCorrect, recordSession, scoreSession } from '../score.js';
import * as S from '../select.js';
import { BlockBadge, CodeBlock, Icon, Rich } from '../ui.jsx';

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

let lastResult = null;
export function setLastResult(r) {
  lastResult = r;
}

function selectHint(q) {
  if (q.type !== 'multi') return '';
  if (/select (two|three|four|all)/i.test(q.stem)) return '';
  return `Select ${['', 'one', 'two', 'three', 'four'][q.answer.length] ?? q.answer.length}.`;
}

// The tables a SQL question runs against, shown as real tables rather than inline text.
function DataTables({ tables }) {
  return (
    <div class="q-tables">
      {tables.map((t) => (
        <div class="table-wrap" key={t.name}>
          <table class="q-table">
            <caption>{t.name}</caption>
            <thead>
              <tr>
                {t.columns.map((c) => (
                  <th key={c}>{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {t.rows.map((r, i) => (
                <tr key={i}>
                  {r.map((v, j) => (
                    <td key={j} class={v === null ? 'q-null' : undefined}>
                      {v === null ? 'NULL' : String(v)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}

export function QuestionBody({ q }) {
  return (
    <>
      <p class="objective-tag">
        {q.objective} · {OBJECTIVES[q.objective]}
      </p>
      <h2 class="stem">
        <Rich text={q.stem} />
        {q.type === 'multi' && <span class="select-hint"> {selectHint(q)}</span>}
      </h2>
      {q.tables && <DataTables tables={q.tables} />}
      {q.code && <CodeBlock code={q.code} lang={q.lang ?? 'python'} label={q.lang === 'sql' ? 'SQL' : q.lang === 'text' ? 'Data' : 'Python'} />}
    </>
  );
}

function Explanation({ q }) {
  return (
    <>
      <Rich as="p" class="explanation" text={q.explanation} />
      <p class="source">
        Source: {q.source} ·{' '}
        <a class="nav-link" href={guideHref(q.objective)}>
          Read {q.objective} in the guide →
        </a>
      </p>
    </>
  );
}

function QuestionCard({ q, sq, mode, onSelect }) {
  const revealed = mode === 'practice' && sq.revealed;
  const multi = q.type === 'multi';
  const correct = revealed && isCorrect(q, sq.chosen);

  function pick(i) {
    if (revealed) return;
    if (!multi) return onSelect([i]);
    onSelect(sq.chosen.includes(i) ? sq.chosen.filter((c) => c !== i) : [...sq.chosen, i]);
  }

  return (
    <section class="question-card">
      <QuestionBody q={q} />
      <div class="options" role={multi ? 'group' : 'radiogroup'}>
        {sq.optionOrder.map((i, pos) => {
          const chosen = sq.chosen.includes(i);
          const right = q.answer.includes(i);
          let cls = 'option';
          if (multi) cls += ' option-multi';
          if (chosen) cls += ' option-selected';
          if (revealed && right) cls += ' option-correct';
          if (revealed && chosen && !right) cls += ' option-incorrect';
          const why = revealed && !right ? q.why_wrong[i] : '';
          return (
            <button key={i} class={cls} onClick={() => pick(i)} disabled={revealed} role={multi ? 'checkbox' : 'radio'} aria-checked={chosen}>
              <span class="option-letter">{LETTERS[pos]}</span>
              <Rich class="option-text" text={q.options[i]} lang={optionLang(q)} />
              {why && <Rich class="why-wrong" text={why} />}
            </button>
          );
        })}
      </div>
      {revealed && (
        <div class="feedback">
          <p class={correct ? 'feedback-correct' : 'feedback-incorrect'}>{correct ? 'Correct' : 'Incorrect'}</p>
          <Explanation q={q} />
        </div>
      )}
    </section>
  );
}

function Drawer({ session, onClose, onJump }) {
  return (
    <div class="drawer-backdrop" onClick={onClose}>
      <div class="drawer" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Questions">
        <div class="drawer-header">
          <h2>Questions</h2>
          <button class="drawer-close" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>
        <div class="drawer-grid">
          {session.questions.map((sq, i) => {
            let cls = 'drawer-cell';
            if (i === session.cursor) cls += ' drawer-cell-current';
            cls += sq.chosen.length ? ' drawer-cell-answered' : ' drawer-cell-unanswered';
            if (sq.flagged) cls += ' drawer-cell-flagged';
            return (
              <button key={sq.questionId} class={cls} onClick={() => onJump(i)}>
                {i + 1}
              </button>
            );
          })}
        </div>
        <div class="drawer-legend">
          <span>
            <i class="dot dot-answered" /> Answered
          </span>
          <span>
            <i class="dot dot-unanswered" /> Unanswered
          </span>
          <span>
            <i class="dot dot-flagged" /> Flagged
          </span>
        </div>
      </div>
    </div>
  );
}

export function Test({ store }) {
  const { session, progress, setProgress, setSession, updateSession } = store;
  const [now, setNow] = useState(() => Date.now());
  const [drawer, setDrawer] = useState(false);
  const [confirmFinish, setConfirmFinish] = useState(false);

  useEffect(() => {
    if (!session || session.timeLimitSec === null) return;
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [session?.id]);

  const finish = useCallback(() => {
    if (!session) return;
    const at = Date.now();
    const done = S.submit(session, at);
    const score = scoreSession(done, QUESTION_BY_ID);
    setProgress(recordSession(progress, done, score, QUESTION_BY_ID, at));
    setLastResult({ session: done, score });
    setSession(null);
    window.location.hash = '#/results';
  }, [session, progress, setProgress, setSession]);

  useEffect(() => {
    if (session && session.timeLimitSec !== null && !S.isPaused(session) && S.timeLeft(session, now) === 0) finish();
  }, [session, now, finish]);

  const sq = session ? session.questions[session.cursor] : undefined;
  const q = sq ? QUESTION_BY_ID.get(sq.questionId) : undefined;

  const select = useCallback((chosen) => updateSession((s) => S.choose(s, s.cursor, chosen, q.type)), [updateSession, q]);
  const check = useCallback(() => updateSession((s) => S.reveal(s, s.cursor)), [updateSession]);
  const goNext = useCallback(() => updateSession(S.next), [updateSession]);
  const goPrev = useCallback(() => updateSession(S.prev), [updateSession]);
  const flag = useCallback(() => updateSession((s) => S.toggleFlag(s, s.cursor)), [updateSession]);

  useEffect(() => {
    function onKey(e) {
      if (!session || !sq || !q || drawer || confirmFinish || S.isPaused(session)) return;
      if (e.target instanceof HTMLElement && /input|textarea|select/i.test(e.target.tagName)) return;
      if (e.key >= '1' && e.key <= '6') {
        const i = sq.optionOrder[Number(e.key) - 1];
        if (i === undefined || (session.mode === 'practice' && sq.revealed)) return;
        if (q.type === 'single') select([i]);
        else select(sq.chosen.includes(i) ? sq.chosen.filter((c) => c !== i) : [...sq.chosen, i]);
      } else if (e.key === 'f' || e.key === 'F') flag();
      else if (e.key === 'ArrowLeft') goPrev();
      else if (e.key === 'ArrowRight') goNext();
      else if (e.key === 'Enter') {
        // In practice, Enter checks the answer first; with nothing chosen it waits.
        if (session.mode === 'practice' && !sq.revealed) {
          if (sq.chosen.length) check();
        } else goNext();
      }
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [session, sq, q, drawer, confirmFinish, select, flag, goPrev, goNext, check]);

  if (!session) {
    // After submitting, the hash already points at the results; only bounce stale test links.
    if (window.location.hash.startsWith('#/test')) window.location.hash = '#/';
    return null;
  }
  if (!sq || !q) return null;

  const left = S.timeLeft(session, now);
  const low = left !== null && left < 300;
  const paused = S.isPaused(session);
  const isLast = session.cursor === session.questions.length - 1;
  const canAdvance = session.mode === 'mock' || sq.revealed;
  const unanswered = session.questions.length - S.answeredCount(session);

  return (
    <div class="test-view">
      <header class="test-header">
        <a
          class="back-link"
          href="#/"
          onClick={(e) => {
            e.preventDefault();
            if (session.timeLimitSec !== null) updateSession((s) => S.pause(s, Date.now()));
            window.location.hash = '#/';
          }}
        >
          Home
        </a>
        <span class="progress-label">
          {session.cursor + 1} / {session.questions.length}
        </span>
        <BlockBadge block={q.block} />
        {left !== null && <span class={`timer ${session.mode === 'mock' ? 'timer-mock' : ''} ${low ? 'timer-low' : ''}`}>{S.formatClock(left)}</span>}
        {left !== null && (
          <button class="pause-btn" onClick={() => updateSession((s) => S.pause(s, Date.now()))} aria-label="Pause the timer">
            Pause
          </button>
        )}
        <button class={`flag-btn ${sq.flagged ? 'flag-active' : ''} ${left === null ? 'push-right' : ''}`} onClick={flag} aria-pressed={sq.flagged} aria-label="Flag for review">
          <Icon name={sq.flagged ? 'flag-filled' : 'flag'} size={18} />
        </button>
        <button class="drawer-toggle" onClick={() => setDrawer(true)}>
          Questions
        </button>
      </header>

      <QuestionCard key={sq.questionId} q={q} sq={sq} mode={session.mode} onSelect={select} />

      <footer class="test-footer">
        <button class="btn" onClick={goPrev} disabled={session.cursor === 0}>
          Prev
        </button>
        {session.mode === 'practice' && !sq.revealed && (
          <button class="btn btn-primary" onClick={check} disabled={sq.chosen.length === 0}>
            Check answer
          </button>
        )}
        {canAdvance && !isLast && (
          <button class="btn btn-primary" onClick={goNext}>
            Next
          </button>
        )}
        <button class="btn btn-finish" onClick={() => setConfirmFinish(true)}>
          Finish
        </button>
      </footer>

      {paused && (
        <div class="confirm-sheet pause-sheet" role="dialog" aria-modal="true" aria-labelledby="pause-title">
          <div class="confirm-card">
            <p id="pause-title" class="confirm-title">
              Paused
            </p>
            <p class="muted">{S.formatClock(left ?? 0)} left. The clock stays stopped until you resume, even if you close this tab.</p>
            <div class="actions">
              <button class="btn btn-primary" onClick={() => updateSession((s) => S.resume(s, Date.now()))}>
                Resume
              </button>
            </div>
          </div>
        </div>
      )}
      {confirmFinish && !paused && (
        <div class="confirm-sheet" role="dialog" aria-modal="true" aria-labelledby="confirm-finish-title">
          <div class="confirm-card">
            <p id="confirm-finish-title" class="confirm-title">
              {unanswered > 0 ? `You have ${unanswered} unanswered question${unanswered === 1 ? '' : 's'}. Submit anyway?` : 'Submit your answers?'}
            </p>
            <div class="actions">
              <button class="btn btn-primary" onClick={finish}>
                Submit
              </button>
              <button class="btn" onClick={() => setConfirmFinish(false)}>
                Keep going
              </button>
            </div>
          </div>
        </div>
      )}
      {drawer && (
        <Drawer
          session={session}
          onClose={() => setDrawer(false)}
          onJump={(i) => {
            updateSession((s) => S.goTo(s, i));
            setDrawer(false);
          }}
        />
      )}
    </div>
  );
}

function resolveResult(progress, id) {
  if (id !== undefined) {
    const entry = progress.history.find((h) => h.id === id);
    if (!entry) return null;
    const r = S.sessionFromHistory(entry);
    setLastResult(r);
    return r;
  }
  return lastResult;
}

export function Results({ store, id }) {
  const [filter, setFilter] = useState('all');
  const result = resolveResult(store.progress, id);
  if (!result) {
    window.location.hash = '#/';
    return null;
  }
  const { session, score } = result;
  const secs = session.submittedAt === null ? 0 : Math.round((session.submittedAt - session.startedAt - (session.pausedMs ?? 0)) / 1000);
  const rows = session.questions
    .map((sq, i) => {
      const q = QUESTION_BY_ID.get(sq.questionId);
      return q ? { i, sq, q, ok: isCorrect(q, sq.chosen) } : null;
    })
    .filter(Boolean);
  const shown = rows.filter((r) => (filter === 'wrong' ? !r.ok : filter === 'flagged' ? r.sq.flagged : true));

  return (
    <main class="page">
      <h1>Results</h1>
      <section class="score-summary">
        <p class="score-pct">{Math.round(score.pct)}%</p>
        <p class={score.passed ? 'pass-label pass' : 'pass-label fail'}>
          {score.passed ? 'Pass' : 'Below pass mark'} (pass mark {Math.round(EXAM.pass * 100)}%)
        </p>
        <p class="muted">
          {score.correct} / {score.total} correct · Time used {S.formatClock(secs)}
        </p>
        <p class="muted">Saved on this device. Set a Sync name on Home to keep results on every device.</p>
      </section>
      <div class="table-wrap">
        <table class="results-table">
          <thead>
            <tr>
              <th>Block</th>
              <th>Correct</th>
              <th>%</th>
            </tr>
          </thead>
          <tbody>
            {BLOCKS.filter((b) => score.byBlock[b]?.total > 0).map((b) => (
              <tr key={b}>
                <td>
                  <BlockBadge block={b} /> {BLOCK_NAMES[b]}
                </td>
                <td>
                  {score.byBlock[b].correct} / {score.byBlock[b].total}
                </td>
                <td>{Math.round(score.byBlock[b].pct)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <details class="objective-results">
        <summary>By objective</summary>
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
              {Object.entries(score.byObjective)
                .sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true }))
                .map(([o, t]) => (
                  <tr key={o}>
                    <td>
                      <BlockBadge block={blockOf(o)} /> {o} {OBJECTIVES[o] ?? ''}
                    </td>
                    <td>
                      {t.correct} / {t.total}
                    </td>
                    <td>{Math.round(t.pct)}%</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </details>
      <div class="filter-row">
        {[
          ['all', 'All'],
          ['wrong', 'Wrong'],
          ['flagged', 'Flagged'],
        ].map(([k, label]) => (
          <button key={k} class={`chip ${filter === k ? 'chip-selected' : ''}`} onClick={() => setFilter(k)}>
            {label}
          </button>
        ))}
      </div>
      <ul class="review-list">
        {shown.map((r) => (
          <li key={r.i}>
            <a class={`review-item ${r.ok ? 'review-correct' : 'review-incorrect'}`} href={`#/review/${r.i}`}>
              <span class="review-index">{r.i + 1}</span>
              <span class={`review-mark ${r.ok ? 'correct' : 'incorrect'}`}>
                <Icon name={r.ok ? 'check' : 'cross'} size={16} />
              </span>
              <Rich class="review-stem" text={r.q.stem} />
              {r.sq.flagged && (
                <span class="review-flag">
                  <Icon name="flag-filled" size={16} />
                </span>
              )}
            </a>
          </li>
        ))}
      </ul>
      <div class="actions">
        {session.returnTo && (
          <a class="btn btn-primary" href={session.returnTo}>
            Back to the guide
          </a>
        )}
        <a class="btn" href="#/">
          Home
        </a>
      </div>
    </main>
  );
}

export function Review({ index }) {
  const result = lastResult;
  if (!result) {
    window.location.hash = '#/';
    return null;
  }
  const { session } = result;
  const sq = session.questions[index];
  const q = sq ? QUESTION_BY_ID.get(sq.questionId) : undefined;
  if (!sq || !q) {
    window.location.hash = '#/results';
    return null;
  }
  const ok = isCorrect(q, sq.chosen);
  const total = session.questions.length;
  return (
    <main class="page">
      <a class="back-link" href="#/results">
        ← Results
      </a>
      <p class="review-nav">
        <span>
          Question {index + 1} / {total}
        </span>
        {index > 0 && (
          <a class="nav-link" href={`#/review/${index - 1}`}>
            Prev
          </a>
        )}
        {index < total - 1 && (
          <a class="nav-link" href={`#/review/${index + 1}`}>
            Next
          </a>
        )}
      </p>
      <p class={ok ? 'feedback-correct' : 'feedback-incorrect'}>{ok ? 'Correct' : sq.chosen.length ? 'Incorrect' : 'Not answered'}</p>
      <QuestionBody q={q} />
      <div class="options">
        {sq.optionOrder.map((i, pos) => {
          const chosen = sq.chosen.includes(i);
          const right = q.answer.includes(i);
          const cls = `option option-static${right ? ' option-correct' : chosen ? ' option-incorrect' : ''}`;
          return (
            <div key={i} class={cls}>
              <span class="option-letter">{LETTERS[pos]}</span>
              <Rich class="option-text" text={q.options[i]} lang={optionLang(q)} />
              {chosen && <span class="option-your-choice">Your choice</span>}
              {!right && q.why_wrong[i] && <Rich class="why-wrong" text={q.why_wrong[i]} />}
            </div>
          );
        })}
      </div>
      <div class="feedback">
        <Explanation q={q} />
      </div>
    </main>
  );
}
