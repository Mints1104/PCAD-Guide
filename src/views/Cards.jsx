import { useEffect, useMemo, useState } from 'preact/hooks';
import { BLOCKS, BLOCK_NAMES, OBJECTIVES, OBJECTIVE_IDS, STORAGE_PREFIX, blockOf } from '../constants.js';
import { ESSENTIALS, GUIDE_DOCS, SYNTAX_CARDS } from '../data.js';
import { readLocal, writeLocal } from '../store.js';
import { BlockBadge, CodeBlock, Rich } from '../ui.jsx';
import { newSeed, rng, shuffle } from '../select.js';
import { startObjectivePractice } from './Setup.jsx';

const KIND_LABEL = { fact: 'Know this', trap: 'Trap', term: 'Term', syntax: 'Syntax' };

function glossaryCards() {
  const md = GUIDE_DOCS.find((d) => d.slug === 'glossary')?.markdown ?? '';
  const out = [];
  for (const line of md.split('\n')) {
    const m = line.match(/^\*\*(.+?)\*\*(?:\s*\([^)]*\))?\s*[\u2014\u2013:]\s*(.+)$/);
    if (m) out.push({ id: `term-${out.length + 1}`, front: `What is ${m[1].trim()}?`, back: m[2].trim(), kind: 'term' });
  }
  return out;
}

function syntaxCards(filter) {
  return SYNTAX_CARDS.filter((c) => !filter || filter(c)).map((c) => ({ id: `syntax-${c.id}`, front: c.front, back: c.back, lang: c.lang ?? 'python', kind: 'syntax', objective: c.objective }));
}

function objectiveCards(objective) {
  const e = ESSENTIALS.get(objective);
  if (!e) return [];
  const facts = e.know.map((k, i) => ({ id: `${objective}-fact-${i + 1}`, front: k.cue, back: k.fact, note: k.why, kind: 'fact' }));
  const traps = (e.traps ?? []).map((t, i) => ({ id: `${objective}-trap-${i + 1}`, front: t.cue, back: t.answer, kind: 'trap' }));
  return [...facts, ...traps];
}

const DECKS = [
  { id: 'glossary', title: 'Glossary', subtitle: 'Every key term, definition on the back', group: 'general', cards: glossaryCards },
  { id: 'syntax', title: 'Syntax', subtitle: 'A task on the front, the pandas / SQL / Python on the back', group: 'general', cards: () => syntaxCards() },
  ...BLOCKS.map((b) => ({
    id: `b${b}`,
    title: `Block ${b}`,
    subtitle: BLOCK_NAMES[b],
    group: 'block',
    block: b,
    cards: () => [...OBJECTIVE_IDS.filter((o) => blockOf(o) === b).flatMap(objectiveCards), ...syntaxCards((c) => c.objective && blockOf(c.objective) === b)],
  })),
  ...OBJECTIVE_IDS.filter((o) => ESSENTIALS.has(o)).map((o) => ({
    id: o,
    title: `${o} ${OBJECTIVES[o]}`,
    subtitle: 'Facts and traps for this objective',
    group: 'objective',
    block: blockOf(o),
    objective: o,
    cards: () => objectiveCards(o),
  })),
];
const DECK_BY_ID = new Map(DECKS.map((d) => [d.id, d]));

export function Cards({ store, id }) {
  return id ? <DeckView key={id} store={store} deck={DECK_BY_ID.get(id)} /> : <DeckIndex />;
}

function DeckIndex() {
  const total = DECKS.filter((d) => d.group !== 'block').reduce((s, d) => s + d.cards().length, 0);
  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Cards</h1>
      <p class="muted">{total} cards. A question on the front, the answer on the back.</p>
      {[
        ['general', 'Terms and syntax'],
        ['block', 'Whole block'],
        ['objective', 'By objective'],
      ].map(([group, heading]) => (
        <section key={group}>
          <h2>{heading}</h2>
          <ul class="row-list">
            {DECKS.filter((d) => d.group === group).map((d) => (
              <li key={d.id}>
                <a class="row-link" href={`#/cards/${d.id}`}>
                  <span class="row-link-title">
                    {d.block !== undefined && <BlockBadge block={d.block} />} {d.title}
                  </span>
                  <span class="row-link-meta muted">
                    {d.group === 'objective' ? '' : `${d.subtitle} · `}
                    {d.cards().length} cards
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </main>
  );
}

const deckKey = (id) => `${STORAGE_PREFIX}:deck:${id}`;

function loadDeckState(id) {
  const s = readLocal(deckKey(id));
  if (!s || !Array.isArray(s.done) || !Array.isArray(s.again) || typeof s.seed !== 'number' || (s.order !== 'shuffled' && s.order !== 'ordered')) return null;
  return s;
}

function orderCards(cards, order, seed) {
  return order === 'ordered' ? cards.slice() : shuffle(cards, rng(seed));
}

function DeckView({ store, deck }) {
  const all = useMemo(() => (deck ? deck.cards() : []), [deck]);
  const saved = useMemo(() => (deck ? loadDeckState(deck.id) : null), [deck]);
  const [order, setOrder] = useState(saved?.order ?? 'shuffled');
  const [seed, setSeed] = useState(saved?.seed ?? newSeed());
  const [done, setDone] = useState(() => new Set(saved?.done ?? []));
  const [again, setAgain] = useState(() => new Set(saved?.again ?? []));
  const [history, setHistory] = useState([]);
  const [flipped, setFlipped] = useState(false);
  const [offerResume, setOfferResume] = useState(saved !== null && (saved.done.length > 0 || saved.again.length > 0));

  const ordered = useMemo(() => orderCards(all, order, seed), [all, order, seed]);
  // Cards not yet done; ones marked "again" go to the back of the queue.
  const queue = useMemo(() => [...ordered.filter((c) => !done.has(c.id) && !again.has(c.id)), ...ordered.filter((c) => again.has(c.id) && !done.has(c.id))], [ordered, done, again]);
  const card = queue[0];

  function persist(d, a, o = order, s = seed) {
    if (deck) writeLocal(deckKey(deck.id), { done: [...d], again: [...a], order: o, seed: s });
  }

  function mark(gotIt) {
    if (!card) return;
    setHistory((h) => [...h, { id: card.id, done: new Set(done), again: new Set(again) }]);
    const d = new Set(done);
    const a = new Set(again);
    if (gotIt) d.add(card.id);
    else a.add(card.id);
    // Re-queue an "again" card behind the rest by removing and re-adding it.
    if (!gotIt && again.has(card.id)) {
      a.delete(card.id);
      a.add(card.id);
    }
    setDone(d);
    setAgain(a);
    setFlipped(false);
    persist(d, a);
  }

  function undo() {
    const last = history[history.length - 1];
    if (!last) return;
    setDone(last.done);
    setAgain(last.again);
    setHistory((h) => h.slice(0, -1));
    setFlipped(false);
    persist(last.done, last.again);
  }

  function restart(nextOrder = order) {
    const s = nextOrder === 'shuffled' ? newSeed() : seed;
    setOrder(nextOrder);
    setSeed(s);
    setDone(new Set());
    setAgain(new Set());
    setHistory([]);
    setFlipped(false);
    setOfferResume(false);
    persist(new Set(), new Set(), nextOrder, s);
  }

  useEffect(() => {
    function onKey(e) {
      if (!card || offerResume) return;
      if (e.key === ' ' || e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        e.preventDefault();
        setFlipped((f) => !f);
      } else if (flipped && (e.key === '1' || e.key === 'ArrowLeft')) mark(false);
      else if (flipped && (e.key === '2' || e.key === 'ArrowRight')) mark(true);
      else if (e.key === 'Backspace') {
        e.preventDefault();
        undo();
      }
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });

  if (!deck || all.length === 0) {
    return (
      <main class="page">
        <h1>{deck ? deck.title : 'Cards'}</h1>
        <p class="empty-note">No cards for this deck yet.</p>
        <a class="link-btn" href="#/cards">
          ← All decks
        </a>
      </main>
    );
  }

  const header = (
    <>
      <a class="back-link" href="#/cards">
        ← All decks
      </a>
      <h1 class="deck-title">
        {deck.block !== undefined && <BlockBadge block={deck.block} />} {deck.title}
      </h1>
      <div class="filter-row" role="group" aria-label="Card order">
        {[
          ['shuffled', 'Shuffled'],
          ['ordered', 'In order'],
        ].map(([o, label]) => (
          <button key={o} type="button" class={`chip ${order === o ? 'chip-selected' : ''}`} onClick={() => o !== order && restart(o)}>
            {label}
          </button>
        ))}
      </div>
    </>
  );

  if (offerResume) {
    return (
      <main class="page">
        {header}
        <div class="card center">
          <p class="muted">
            You have progress saved on this deck: {done.size} of {all.length} done.
          </p>
          <div class="actions">
            <button type="button" class="btn btn-primary" onClick={() => setOfferResume(false)}>
              Resume ({done.size} of {all.length})
            </button>
            <button type="button" class="btn" onClick={() => restart()}>
              Start over
            </button>
          </div>
        </div>
      </main>
    );
  }

  if (!card) {
    const firstTry = [...done].filter((id) => !again.has(id)).length;
    return (
      <main class="page">
        {header}
        <div class="card center">
          <p class="summary-score">
            {firstTry} of {all.length} on first try
          </p>
          <div class="actions">
            <button type="button" class="btn btn-primary" onClick={() => restart()}>
              Go again
            </button>
            {deck.objective && (
              <button type="button" class="btn" onClick={() => startObjectivePractice(store, deck.objective)}>
                Try 5 questions on {deck.objective}
              </button>
            )}
            <a class="btn btn-outline-accent" href="#/cards">
              All decks
            </a>
          </div>
        </div>
      </main>
    );
  }

  const pct = Math.round((done.size / all.length) * 100);
  const toRepeat = [...again].filter((id) => !done.has(id)).length;
  return (
    <main class="page">
      {header}
      <p class="muted deck-count">
        {done.size} of {all.length} done{toRepeat > 0 ? ` · ${toRepeat} to repeat` : ''}
      </p>
      <div class="bar-track deck-progress">
        <div class="bar-fill" style={`width:${pct}%;background:${deck.block ? `var(--b${deck.block})` : 'var(--accent)'}`} />
      </div>
      <div
        class={`deck-card ${flipped ? 'flipped' : ''}`}
        role="button"
        tabIndex={0}
        aria-label={flipped ? 'Answer side. Press space to see the question.' : 'Question side. Press space to see the answer.'}
        onClick={() => setFlipped((f) => !f)}
      >
        <div class="deck-card-inner">
          <div class="deck-face deck-face-front" aria-hidden={flipped}>
            <p class="kind-label muted">{KIND_LABEL[card.kind]}</p>
            <Rich as="p" class="deck-face-text" text={card.front} />
            <p class="muted deck-hint">Tap or press space to flip</p>
          </div>
          <div class="deck-face deck-face-back" aria-hidden={!flipped}>
            <p class="kind-label muted">{card.kind === 'syntax' ? 'Code' : 'Answer'}</p>
            {card.kind === 'syntax' ? <CodeBlock code={card.back} lang={card.lang} /> : <Rich as="p" class="deck-face-text" text={card.back} />}
            {card.note && (
              <p class="deck-face-note muted">
                <b>Exam angle:</b> <Rich text={card.note} />
              </p>
            )}
          </div>
        </div>
      </div>
      <div class="flashcard-controls">
        <button type="button" class="btn" onClick={() => mark(false)} disabled={!flipped}>
          Again
        </button>
        <button type="button" class="btn btn-primary" onClick={() => mark(true)} disabled={!flipped}>
          Got it
        </button>
      </div>
      <div class="deck-footer">
        <button type="button" class="link-btn" onClick={undo} disabled={history.length === 0}>
          Undo
        </button>
        <span class="muted hint">Space flips · 1 again · 2 got it</span>
      </div>
    </main>
  );
}
