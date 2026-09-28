import { BLOCKS, BLOCK_WEIGHTS, DIFFICULTY_MIX, EXAM } from './constants.js';

export const MAX_ATTEMPTS = 5000;
export const MAX_HISTORY = 20;
const DIFFICULTIES = [1, 2, 3];

export function emptyProgress() {
  return { version: 1, stats: {}, mocks: [], bookmarks: [], attempts: [], revised: [], history: [] };
}

// Multi-select items are all-or-nothing: every correct option and nothing else.
export function isCorrect(question, chosen) {
  if (chosen.length === 0) return false;
  const set = new Set(chosen);
  return set.size === question.answer.length && question.answer.every((a) => set.has(a));
}

function pct(correct, total) {
  return total === 0 ? 0 : Math.round((correct / total) * 1000) / 10;
}

export function scoreSession(session, byId) {
  const blocks = new Map(BLOCKS.map((b) => [b, { total: 0, correct: 0 }]));
  const objectives = new Map();
  let total = 0;
  let correct = 0;
  for (const sq of session.questions) {
    const q = byId.get(sq.questionId);
    if (!q) continue;
    total += 1;
    const ok = isCorrect(q, sq.chosen);
    if (ok) correct += 1;
    const b = blocks.get(q.block);
    b.total += 1;
    if (ok) b.correct += 1;
    const o = objectives.get(q.objective) ?? { total: 0, correct: 0 };
    o.total += 1;
    if (ok) o.correct += 1;
    objectives.set(q.objective, o);
  }
  const byBlock = {};
  for (const b of BLOCKS) {
    const v = blocks.get(b);
    byBlock[b] = { ...v, pct: pct(v.correct, v.total) };
  }
  const byObjective = {};
  for (const [k, v] of objectives) byObjective[k] = { ...v, pct: pct(v.correct, v.total) };
  const p = pct(correct, total);
  return { total, correct, pct: p, byBlock, byObjective, passed: p >= EXAM.pass * 100 };
}

// Fold a finished session into progress: per-question stats, attempt log, mock log, history.
export function recordSession(progress, session, score, byId, now) {
  const stats = { ...progress.stats };
  const newAttempts = [];
  for (const sq of session.questions) {
    const q = byId.get(sq.questionId);
    if (!q) continue;
    const answered = sq.chosen.length > 0;
    if (!answered && session.mode === 'practice') continue;
    const ok = answered ? isCorrect(q, sq.chosen) : false;
    const prev = stats[q.id];
    stats[q.id] = {
      seen: (prev?.seen ?? 0) + 1,
      correct: (prev?.correct ?? 0) + (ok ? 1 : 0),
      lastAt: now,
      lastCorrect: ok,
    };
    newAttempts.push({ questionId: q.id, correct: ok, at: now, mode: session.mode });
  }
  let attempts = [...progress.attempts, ...newAttempts];
  if (attempts.length > MAX_ATTEMPTS) attempts = attempts.slice(attempts.length - MAX_ATTEMPTS);
  const endedAt = session.submittedAt ?? now;
  const durationSec = Math.max(0, Math.round((endedAt - session.startedAt - pausedMs(session, endedAt)) / 1000));
  let mocks = progress.mocks;
  let bookmarks = progress.bookmarks;
  if (session.mode === 'mock') {
    mocks = [...mocks, { id: session.id, at: now, total: score.total, correct: score.correct, byBlock: score.byBlock, durationSec }];
    for (const sq of session.questions) {
      if (sq.flagged && !bookmarks.includes(sq.questionId)) bookmarks = [...bookmarks, sq.questionId];
    }
  }
  const entry = {
    id: session.id,
    mode: session.mode,
    at: now,
    questions: session.questions.map((sq) => ({ questionId: sq.questionId, chosen: sq.chosen, flagged: sq.flagged })),
    optionOrders: session.questions.map((sq) => sq.optionOrder),
    score,
    durationSec,
  };
  let history = [...progress.history, entry];
  if (history.length > MAX_HISTORY) history = history.slice(history.length - MAX_HISTORY);
  return { ...progress, stats, attempts, mocks, bookmarks, history };
}

export function pausedMs(session, now) {
  return (session.pausedMs ?? 0) + (session.pausedAt ? Math.max(0, now - session.pausedAt) : 0);
}

// Only the last three attempts per question count, so old mistakes fade once fixed.
function recentAttempts(attempts) {
  const map = new Map();
  for (const a of attempts) {
    const list = map.get(a.questionId);
    if (list) list.push(a);
    else map.set(a.questionId, [a]);
  }
  for (const [k, v] of map) map.set(k, v.slice(-3));
  return map;
}

function tally(progress, byId, keyOf) {
  const out = new Map();
  for (const [qid, list] of recentAttempts(progress.attempts)) {
    const q = byId.get(qid);
    if (!q) continue;
    const key = keyOf(q);
    const t = out.get(key) ?? { total: 0, correct: 0 };
    t.total += list.length;
    t.correct += list.filter((a) => a.correct).length;
    out.set(key, t);
  }
  return out;
}

function withPct(map, keys) {
  const out = {};
  for (const k of keys ?? map.keys()) {
    const v = map.get(k) ?? { total: 0, correct: 0 };
    out[k] = { ...v, pct: pct(v.correct, v.total) };
  }
  return out;
}

export function blockAccuracy(progress, byId) {
  return withPct(tally(progress, byId, (q) => q.block), BLOCKS);
}

export function objectiveAccuracy(progress, byId) {
  return withPct(tally(progress, byId, (q) => q.objective));
}

export function difficultyAccuracy(progress, byId) {
  return withPct(tally(progress, byId, (q) => q.difficulty), DIFFICULTIES);
}

// Readiness: per block, accuracy by difficulty weighted to the mock's difficulty mix,
// then blocks weighted by their share of the 48 exam items.
export function readiness(progress, questions, byId) {
  const cells = tally(progress, byId, (q) => `${q.block}:${q.difficulty}`);
  let score = 0;
  for (const b of BLOCKS) {
    let sum = 0;
    let weight = 0;
    for (const d of DIFFICULTIES) {
      const c = cells.get(`${b}:${d}`);
      if (!c || c.total === 0) continue;
      sum += DIFFICULTY_MIX[d] * (c.correct / c.total) * 100;
      weight += DIFFICULTY_MIX[d];
    }
    score += BLOCK_WEIGHTS[b] * (weight > 0 ? sum / weight : 0);
  }
  const seen = questions.filter((q) => progress.stats[q.id] !== undefined).length;
  return { pct: Math.round(score * 10) / 10, coverage: questions.length === 0 ? 0 : seen / questions.length };
}

export function wrongIds(progress, questions) {
  const ids = new Set(questions.map((q) => q.id));
  return Object.entries(progress.stats)
    .filter(([id, s]) => ids.has(id) && s.lastCorrect === false)
    .sort((a, b) => b[1].lastAt - a[1].lastAt)
    .map(([id]) => id);
}

function toggle(list, value) {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
}

export function toggleBookmark(progress, id) {
  return { ...progress, bookmarks: toggle(progress.bookmarks, id) };
}

export function toggleRevised(progress, objective) {
  return { ...progress, revised: toggle(progress.revised, objective) };
}
