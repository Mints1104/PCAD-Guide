import { BLOCKS, BLOCK_ITEMS, DIFFICULTY_MIX, EXAM, OBJECTIVE_IDS, blockOf } from './constants.js';
import { pausedMs } from './score.js';

const DAY_MS = 86400000;

export function rng(seed) {
  let t = seed >>> 0;
  return {
    next() {
      t = (t + 0x6d2b79f5) | 0;
      let x = Math.imul(t ^ (t >>> 15), 1 | t);
      x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    },
  };
}

export function shuffle(list, r) {
  const a = list.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(r.next() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export function newSeed() {
  return Math.floor(Math.random() * 2 ** 31);
}

// Unseen questions first, then ones answered wrong, then the longest-unseen.
function priority(q, progress, now) {
  const s = progress.stats[q.id];
  if (s === undefined) return 3;
  if (s.lastCorrect === false) return 2;
  const days = Math.max(0, (now - s.lastAt) / DAY_MS);
  return 1 + Math.min(1, days / 14) * 0.9;
}

// Largest-remainder split of `count` across keys by weight.
function apportion(count, weights) {
  const keys = Object.keys(weights);
  const total = keys.reduce((s, k) => s + weights[k], 0);
  const raw = keys.map((k) => ({ k, v: (weights[k] / total) * count }));
  const out = Object.fromEntries(raw.map(({ k, v }) => [k, Math.floor(v)]));
  let left = count - Object.values(out).reduce((s, v) => s + v, 0);
  for (const { k } of raw.slice().sort((a, b) => (b.v % 1) - (a.v % 1))) {
    if (left <= 0) break;
    out[k] += 1;
    left -= 1;
  }
  return out;
}

function sampleDifficulty(r, mix) {
  if (mix === 'hard') return r.next() < 0.7 ? 3 : 2;
  let x = r.next();
  for (const d of [1, 2, 3]) {
    x -= DIFFICULTY_MIX[d];
    if (x <= 0) return d;
  }
  return 2;
}

// Mock: draws across the 48 syllabus objectives in the official 14/16/4/9/5 block split.
// A full-length mock takes one question from every objective.
export function buildMock(questions, { count, mix }, progress, r, now) {
  const byObjective = new Map();
  for (const q of questions) {
    const list = byObjective.get(q.objective) ?? [];
    list.push(q);
    byObjective.set(q.objective, list);
  }
  const perBlock = apportion(count, BLOCK_ITEMS);
  const chosenObjectives = [];
  for (const b of BLOCKS) {
    const objs = OBJECTIVE_IDS.filter((o) => blockOf(o) === b && byObjective.has(o));
    const want = perBlock[b];
    // Weakest objectives first when a short mock can't cover them all.
    const ranked = shuffle(objs, r)
      .map((o) => ({ o, p: Math.max(...byObjective.get(o).map((q) => priority(q, progress, now))) + r.next() * 0.3 }))
      .sort((x, y) => y.p - x.p)
      .map((x) => x.o);
    for (let i = 0; i < want; i++) chosenObjectives.push(ranked[i % Math.max(1, ranked.length)]);
  }
  const used = new Set();
  const picked = [];
  for (const o of chosenObjectives) {
    if (o === undefined) continue;
    const target = sampleDifficulty(r, mix);
    const pool = byObjective.get(o).filter((q) => !used.has(q.id));
    if (pool.length === 0) continue;
    const scored = pool
      .map((q) => {
        let s = priority(q, progress, now) - Math.abs(q.difficulty - target) * 1.2 + r.next() * 0.5;
        if (mix === 'code' && q.kind === 'code') s += 2.5;
        return { q, s };
      })
      .sort((a, b) => b.s - a.s);
    used.add(scored[0].q.id);
    picked.push(scored[0].q);
  }
  return shuffle(picked, r);
}

export function filterQuestions(questions, f, progress) {
  return questions.filter((q) => {
    if (f.blocks && !f.blocks.includes(q.block)) return false;
    if (f.objectives && !f.objectives.includes(q.objective)) return false;
    if (f.kinds && !f.kinds.includes(q.kind)) return false;
    if (f.weakOnly) {
      const s = progress.stats[q.id];
      if (s !== undefined && s.lastCorrect !== false) return false;
    }
    return true;
  });
}

export function buildPractice(questions, f, progress, r, now) {
  const pool = filterQuestions(questions, f, progress);
  const ordered = f.random
    ? shuffle(pool, r)
    : pool.map((q) => ({ q, s: priority(q, progress, now) + r.next() * 0.5 })).sort((a, b) => b.s - a.s).map((x) => x.q);
  return shuffle(ordered.slice(0, Math.min(f.count, ordered.length)), r);
}

export function createSession(questions, { mode, seed, now, timeLimitSec, returnTo }, r) {
  return {
    id: `${mode}-${now}-${seed}`,
    mode,
    seed,
    startedAt: now,
    timeLimitSec,
    questions: questions.map((q) => ({
      questionId: q.id,
      optionOrder: shuffle(q.options.map((_, i) => i), r),
      chosen: [],
      flagged: false,
      revealed: false,
    })),
    cursor: 0,
    submittedAt: null,
    returnTo: returnTo ?? null,
  };
}

export function mockTimeLimit(count) {
  return Math.round((EXAM.minutes * 60 * count) / EXAM.items);
}

function updateAt(session, i, fn) {
  const sq = session.questions[i];
  if (!sq) return session;
  const questions = session.questions.slice();
  questions[i] = fn(sq);
  return { ...session, questions };
}

export function choose(session, i, chosen, type) {
  return updateAt(session, i, (sq) => ({
    ...sq,
    chosen: type === 'single' ? (chosen.length ? [chosen[chosen.length - 1]] : []) : [...new Set(chosen)].sort((a, b) => a - b),
  }));
}

export const toggleFlag = (s, i) => updateAt(s, i, (sq) => ({ ...sq, flagged: !sq.flagged }));
export const reveal = (s, i) => (s.mode === 'practice' ? updateAt(s, i, (sq) => ({ ...sq, revealed: true })) : s);
export const goTo = (s, i) => ({ ...s, cursor: Math.min(Math.max(i, 0), Math.max(s.questions.length - 1, 0)) });
export const next = (s) => goTo(s, s.cursor + 1);
export const prev = (s) => goTo(s, s.cursor - 1);
export const submit = (s, now) => (s.submittedAt === null ? { ...s, submittedAt: now } : s);
export const isPaused = (s) => s.pausedAt != null;
export const pause = (s, now) => (s.timeLimitSec === null || s.submittedAt !== null || isPaused(s) ? s : { ...s, pausedAt: now });
export const resume = (s, now) => (isPaused(s) ? { ...s, pausedAt: null, pausedMs: (s.pausedMs ?? 0) + Math.max(0, now - s.pausedAt) } : s);

export function timeLeft(s, now) {
  if (s.timeLimitSec === null) return null;
  const used = Math.floor((now - s.startedAt - pausedMs(s, now)) / 1000);
  return Math.max(0, s.timeLimitSec - used);
}

export const answeredCount = (s) => s.questions.filter((q) => q.chosen.length > 0).length;

export function formatClock(sec) {
  const t = Math.max(0, Math.round(sec));
  const h = Math.floor(t / 3600);
  const m = Math.floor((t % 3600) / 60);
  const ss = String(t % 60).padStart(2, '0');
  return h > 0 ? `${h}:${String(m).padStart(2, '0')}:${ss}` : `${m}:${ss}`;
}

// Rebuild a finished session from history so its results can be reopened.
export function sessionFromHistory(entry) {
  const startedAt = entry.at - entry.durationSec * 1000;
  return {
    session: {
      id: entry.id,
      mode: entry.mode,
      seed: 0,
      startedAt,
      timeLimitSec: null,
      questions: entry.questions.map((q, i) => ({ ...q, optionOrder: entry.optionOrders[i] ?? [], revealed: true })),
      cursor: 0,
      submittedAt: entry.at,
    },
    score: entry.score,
  };
}
