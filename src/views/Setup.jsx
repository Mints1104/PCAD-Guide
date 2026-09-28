import { useState } from 'preact/hooks';
import { BLOCKS, BLOCK_ITEMS, BLOCK_NAMES, EXAM, OBJECTIVES, OBJECTIVE_IDS, blockOf } from '../constants.js';
import { QUESTIONS } from '../data.js';
import { buildMock, buildPractice, createSession, mockTimeLimit, newSeed, rng } from '../select.js';

const MOCK_COUNTS = [12, 24, 48];
const MIXES = [
  { id: 'blueprint', label: 'Blueprint mix', note: 'follows the syllabus, mostly apply-level questions' },
  { id: 'code', label: 'Code-heavy mix', note: 'prefers questions where you read Python, pandas or SQL' },
  { id: 'hard', label: 'Harder mix', note: 'analyze-level questions first; above exam level' },
];

export function startPractice(store, filter, returnTo) {
  const seed = newSeed();
  const now = Date.now();
  const r = rng(seed);
  const picked = buildPractice(QUESTIONS, filter, store.progress, r, now);
  if (picked.length === 0) return false;
  store.setSession(createSession(picked, { mode: 'practice', seed, now, timeLimitSec: null, returnTo }, r));
  window.location.hash = '#/test';
  return true;
}

export function startObjectivePractice(store, objective, returnTo) {
  return startPractice(store, { count: 5, objectives: [objective] }, returnTo);
}

export function Mock({ store }) {
  const [count, setCount] = useState(48);
  const [mix, setMix] = useState('blueprint');
  const minutes = Math.round(mockTimeLimit(count) / 60);

  function start() {
    const seed = newSeed();
    const now = Date.now();
    const r = rng(seed);
    const picked = buildMock(QUESTIONS, { count, mix }, store.progress, r, now);
    store.setSession(createSession(picked, { mode: 'mock', seed, now, timeLimitSec: mockTimeLimit(count) }, r));
    window.location.hash = '#/test';
  }

  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Mock test</h1>
      <p class="muted">
        {count} questions in {minutes} minutes, split across the five blocks like the real exam ({BLOCKS.map((b) => BLOCK_ITEMS[b]).join(' / ')} of {EXAM.items}).
      </p>
      <section class="setup-group">
        <h2>Length</h2>
        <div class="option-group">
          {MOCK_COUNTS.map((n) => (
            <button key={n} class={`chip ${count === n ? 'chip-selected' : ''}`} onClick={() => setCount(n)}>
              {n === 48 ? '48 · full exam' : n}
            </button>
          ))}
        </div>
      </section>
      <section class="setup-group">
        <h2>Mix</h2>
        <div class="mix-options">
          {MIXES.map((m) => (
            <label key={m.id} class={`checkbox-row ${mix === m.id ? 'mix-selected' : ''}`}>
              <input type="radio" name="mix" id={`mix-${m.id}`} checked={mix === m.id} onChange={() => setMix(m.id)} />
              <span>
                <b>{m.label}</b> <span class="muted">{m.note}</span>
              </span>
            </label>
          ))}
        </div>
      </section>
      <p class="muted">Single- and multiple-select questions, one point each. A multiple-select question scores only when every correct option is chosen.</p>
      <button class="btn btn-primary btn-large" onClick={start}>
        Start mock test
      </button>
    </main>
  );
}

const COUNTS = [10, 20, 40, 'all'];

export function Practice({ store }) {
  const [blocks, setBlocks] = useState(() => new Set(BLOCKS));
  const [objectives, setObjectives] = useState(() => new Set(OBJECTIVE_IDS));
  const [kinds, setKinds] = useState(() => new Set(['code', 'concept']));
  const [count, setCount] = useState(20);
  const [weakOnly, setWeakOnly] = useState(false);
  const [random, setRandom] = useState(false);
  const [empty, setEmpty] = useState(false);

  function toggleBlock(b) {
    const inBlock = OBJECTIVE_IDS.filter((o) => blockOf(o) === b);
    const on = !blocks.has(b);
    setBlocks((prev) => {
      const s = new Set(prev);
      on ? s.add(b) : s.delete(b);
      return s;
    });
    setObjectives((prev) => {
      const s = new Set(prev);
      for (const o of inBlock) on ? s.add(o) : s.delete(o);
      return s;
    });
  }

  const toggleIn = (setter) => (v) =>
    setter((prev) => {
      const s = new Set(prev);
      s.has(v) ? s.delete(v) : s.add(v);
      return s;
    });

  function start() {
    const ok = startPractice(store, {
      count: count === 'all' ? QUESTIONS.length : count,
      blocks: [...blocks],
      objectives: [...objectives],
      kinds: [...kinds],
      weakOnly,
      random,
    });
    setEmpty(!ok);
  }

  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Practice</h1>
      <section class="setup-group">
        <h2>Blocks</h2>
        {BLOCKS.map((b) => (
          <label class="checkbox-row" key={b}>
            <input type="checkbox" id={`block-${b}`} checked={blocks.has(b)} onChange={() => toggleBlock(b)} />
            <span>
              <b style={`color:var(--b${b})`}>B{b}</b> {BLOCK_NAMES[b]}
            </span>
          </label>
        ))}
      </section>
      <section class="setup-group">
        <h2>Objectives</h2>
        {BLOCKS.map((b) => (
          <div class="objective-section" key={b}>
            <p class="objective-section-label">{BLOCK_NAMES[b]}</p>
            <div class="chip-group">
              {OBJECTIVE_IDS.filter((o) => blockOf(o) === b).map((o) => (
                <button key={o} class={`chip chip-small ${objectives.has(o) ? 'chip-selected' : ''}`} title={OBJECTIVES[o]} onClick={() => toggleIn(setObjectives)(o)}>
                  {o}
                </button>
              ))}
            </div>
          </div>
        ))}
      </section>
      <section class="setup-group">
        <h2>Question kind</h2>
        <p class="hint">Code reading means a snippet of Python, pandas or SQL to trace; concept questions test definitions, choices and scenarios.</p>
        <div class="option-group">
          {[
            ['code', 'Code reading'],
            ['concept', 'Concept'],
          ].map(([k, label]) => (
            <button key={k} class={`chip ${kinds.has(k) ? 'chip-selected' : ''}`} onClick={() => toggleIn(setKinds)(k)}>
              {label} · {QUESTIONS.filter((q) => q.kind === k).length}
            </button>
          ))}
        </div>
      </section>
      <section class="setup-group">
        <h2>Count</h2>
        <div class="option-group">
          {COUNTS.map((c) => (
            <button key={c} class={`chip ${count === c ? 'chip-selected' : ''}`} onClick={() => setCount(c)}>
              {c === 'all' ? 'All' : c}
            </button>
          ))}
        </div>
      </section>
      <section class="setup-group">
        <label class="checkbox-row">
          <input type="checkbox" id="weak-only" checked={weakOnly} onChange={() => setWeakOnly((v) => !v)} />
          Weak areas only (unseen or last answered wrong)
        </label>
        <label class="checkbox-row">
          <input type="checkbox" id="random-order" checked={random} onChange={() => setRandom((v) => !v)} />
          Random order
        </label>
      </section>
      {empty && <p class="empty-note">No questions match these filters. Turn on more blocks, objectives or kinds.</p>}
      <button class="btn btn-primary btn-large" onClick={start}>
        Start practice
      </button>
    </main>
  );
}
