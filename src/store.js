import { useCallback, useEffect, useState } from 'preact/hooks';
import { STORAGE_PREFIX } from './constants.js';
import { MAX_ATTEMPTS, MAX_HISTORY, emptyProgress } from './score.js';

const PROGRESS_KEY = `${STORAGE_PREFIX}:v1`;
const SESSION_KEY = `${STORAGE_PREFIX}:session:v1`;
const SYNC_NAME_KEY = `${STORAGE_PREFIX}:sync-name`;
const SYNC_COLLECTION = 'progress';
const MAX_SYNC_CHARS = 230000;
const PUSH_DELAY_MS = 1500;

// ---------- local storage (every access guarded: storage can be blocked) ----------

export function readLocal(key, fallback = null) {
  try {
    const raw = localStorage.getItem(key);
    return raw === null ? fallback : JSON.parse(raw);
  } catch {
    return fallback;
  }
}

export function writeLocal(key, value) {
  try {
    if (value === null || value === undefined) localStorage.removeItem(key);
    else localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage unavailable: keep working in memory */
  }
}

// ---------- validation ----------

const isObj = (v) => typeof v === 'object' && v !== null && !Array.isArray(v);
const isNum = (v) => typeof v === 'number' && Number.isFinite(v);
const isStrArr = (v) => Array.isArray(v) && v.every((s) => typeof s === 'string');

function validTally(v) {
  return isObj(v) && Object.values(v).every((t) => isObj(t) && isNum(t.total) && isNum(t.correct));
}

function validMock(m) {
  return isObj(m) && typeof m.id === 'string' && isNum(m.at) && isNum(m.total) && isNum(m.correct) && isNum(m.durationSec) && validTally(m.byBlock);
}

function validHistory(h) {
  return (
    isObj(h) &&
    typeof h.id === 'string' &&
    (h.mode === 'mock' || h.mode === 'practice') &&
    isNum(h.at) &&
    Array.isArray(h.questions) &&
    h.questions.every((q) => isObj(q) && typeof q.questionId === 'string' && Array.isArray(q.chosen) && typeof q.flagged === 'boolean') &&
    Array.isArray(h.optionOrders) &&
    isObj(h.score) &&
    isNum(h.score.pct) &&
    validTally(h.score.byBlock) &&
    validTally(h.score.byObjective) &&
    isNum(h.durationSec)
  );
}

export function parseProgress(value) {
  if (!isObj(value)) throw new Error('not an object');
  if (value.version !== 1) throw new Error('unsupported version');
  if (!isObj(value.stats) || !Object.values(value.stats).every((s) => isObj(s) && isNum(s.seen) && isNum(s.correct) && isNum(s.lastAt) && typeof s.lastCorrect === 'boolean')) throw new Error('stats');
  if (!Array.isArray(value.mocks) || !value.mocks.every(validMock)) throw new Error('mocks');
  if (!isStrArr(value.bookmarks)) throw new Error('bookmarks');
  if (!Array.isArray(value.attempts) || !value.attempts.every((a) => isObj(a) && typeof a.questionId === 'string' && typeof a.correct === 'boolean' && isNum(a.at) && (a.mode === 'mock' || a.mode === 'practice'))) throw new Error('attempts');
  const revised = value.revised ?? [];
  if (!isStrArr(revised)) throw new Error('revised');
  const history = value.history ?? [];
  if (!Array.isArray(history) || !history.every(validHistory)) throw new Error('history');
  return { ...value, revised, history };
}

function loadProgress() {
  try {
    const raw = readLocal(PROGRESS_KEY);
    return raw === null ? emptyProgress() : parseProgress(raw);
  } catch {
    return emptyProgress();
  }
}

// ---------- merging two copies of progress (this device + synced copy) ----------

function statsFromAttempts(attempts) {
  const out = {};
  for (const a of attempts) {
    const prev = out[a.questionId];
    out[a.questionId] = { seen: (prev?.seen ?? 0) + 1, correct: (prev?.correct ?? 0) + (a.correct ? 1 : 0), lastAt: a.at, lastCorrect: a.correct };
  }
  return out;
}

function unionBy(a, b, key) {
  const map = new Map();
  for (const x of a) map.set(key(x), x);
  for (const x of b) map.set(key(x), x);
  return [...map.values()].sort((x, y) => x.at - y.at);
}

export function mergeProgress(a, b) {
  let attempts = unionBy(a.attempts, b.attempts, (x) => `${x.questionId}|${x.at}`);
  if (attempts.length > MAX_ATTEMPTS) attempts = attempts.slice(attempts.length - MAX_ATTEMPTS);
  const fromAttempts = statsFromAttempts(attempts);
  const stats = {};
  for (const id of new Set([...Object.keys(a.stats), ...Object.keys(b.stats), ...Object.keys(fromAttempts)])) {
    const candidates = [a.stats[id], b.stats[id], fromAttempts[id]].filter(Boolean);
    const most = candidates.reduce((m, s) => (s.seen > m.seen ? s : m));
    const latest = candidates.reduce((m, s) => (s.lastAt > m.lastAt ? s : m));
    stats[id] = { seen: most.seen, correct: most.correct, lastAt: latest.lastAt, lastCorrect: latest.lastCorrect };
  }
  const mocks = unionBy(a.mocks, b.mocks, (m) => m.id);
  let history = unionBy(a.history, b.history, (h) => h.id);
  if (history.length > MAX_HISTORY) history = history.slice(history.length - MAX_HISTORY);
  const bookmarks = [...new Set([...a.bookmarks, ...b.bookmarks])];
  const revised = [...new Set([...a.revised, ...b.revised])];
  return { version: 1, stats, mocks, bookmarks, attempts, revised, history };
}

// Compact form for the synced document; drops the oldest history, then attempts, to fit.
function encodeForSync(p) {
  const stats = {};
  for (const [id, s] of Object.entries(p.stats)) stats[id] = [s.seen, s.correct, s.lastAt, s.lastCorrect ? 1 : 0];
  let attempts = p.attempts.slice(-3000).map((a) => [a.questionId, a.correct ? 1 : 0, a.at, a.mode === 'mock' ? 1 : 0]);
  let history = p.history;
  const doc = { v: 1, updatedAt: Date.now(), stats, attempts, mocks: p.mocks, bookmarks: p.bookmarks, revised: p.revised, history };
  while (history.length > 0 && JSON.stringify(doc).length > MAX_SYNC_CHARS) {
    history = history.slice(1);
    doc.history = history;
  }
  while (attempts.length > 0 && JSON.stringify(doc).length > MAX_SYNC_CHARS) {
    attempts = attempts.slice(Math.ceil(attempts.length / 10));
    doc.attempts = attempts;
  }
  return doc;
}

function decodeFromSync(doc) {
  try {
    if (!isObj(doc) || doc.v !== 1 || !isObj(doc.stats) || !Array.isArray(doc.attempts)) return null;
    const stats = {};
    for (const [id, s] of Object.entries(doc.stats)) {
      if (!Array.isArray(s) || s.length !== 4 || !s.every(isNum)) return null;
      stats[id] = { seen: s[0], correct: s[1], lastAt: s[2], lastCorrect: s[3] === 1 };
    }
    const attempts = [];
    for (const a of doc.attempts) {
      if (!Array.isArray(a) || a.length !== 4 || typeof a[0] !== 'string') return null;
      attempts.push({ questionId: a[0], correct: a[1] === 1, at: a[2], mode: a[3] === 1 ? 'mock' : 'practice' });
    }
    return parseProgress({ version: 1, stats, attempts, mocks: doc.mocks ?? [], bookmarks: doc.bookmarks ?? [], revised: doc.revised ?? [], history: doc.history ?? [] });
  } catch {
    return null;
  }
}

// ---------- sync names ----------

export function cleanSyncName(name) {
  const n = String(name ?? '').trim().toLowerCase().replace(/[^a-z0-9_-]/g, '');
  return n.length >= 2 && n.length <= 32 ? n : null;
}

function readSyncName() {
  try {
    return cleanSyncName(localStorage.getItem(SYNC_NAME_KEY));
  } catch {
    return null;
  }
}

function writeSyncName(name) {
  try {
    const clean = name === null ? null : cleanSyncName(name);
    if (clean === null) localStorage.removeItem(SYNC_NAME_KEY);
    else localStorage.setItem(SYNC_NAME_KEY, clean);
  } catch {
    /* ignore */
  }
}

// ---------- sync engine ----------

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const isUnavailable = (e) => isObj(e) && e.code === 'unavailable';

async function retryOnce(fn) {
  try {
    return await fn();
  } catch (e) {
    if (!isUnavailable(e)) throw e;
    await sleep(800 + Math.random() * 600);
    return fn();
  }
}

const NO_SYNC = { push() {}, stop() {}, async flush() {} };

function startSync({ getLocal, applyMerged, onStatus, mode }) {
  const name = readSyncName();
  if (name === null || typeof window === 'undefined' || !window.claude) {
    onStatus('off');
    return NO_SYNC;
  }
  let stopped = false;
  let docRef = null;
  let unsubscribe = null;
  let timer = null;
  let pending = null;
  let writing = Promise.resolve();
  onStatus('connecting');

  function write(progress) {
    const ref = docRef;
    if (ref === null || stopped) return Promise.resolve();
    // One write at a time per document.
    writing = writing
      .then(() => retryOnce(() => ref.set(encodeForSync(progress))))
      .catch(() => {
        if (!stopped) onStatus('error');
      });
    return writing;
  }

  (async () => {
    let db = null;
    try {
      db = (await window.claude.use('db')) ?? null;
    } catch {
      db = null;
    }
    if (stopped) return;
    if (db === null) {
      onStatus('off');
      return;
    }
    try {
      docRef = db.doc(`${SYNC_COLLECTION}/${name}`);
      const snap = await retryOnce(() => docRef.get());
      if (stopped) return;
      const remote = snap.exists ? decodeFromSync(snap.data()) : null;
      if (mode === 'replace') {
        const next = remote ?? emptyProgress();
        applyMerged(next);
        if (remote === null) await write(next);
      } else {
        const local = getLocal();
        const merged = remote === null ? local : mergeProgress(local, remote);
        if (JSON.stringify(merged) !== JSON.stringify(local)) applyMerged(merged);
        if (remote === null || JSON.stringify(merged) !== JSON.stringify(remote)) await write(merged);
      }
      if (stopped) return;
      unsubscribe = docRef.onSnapshot(
        (s) => {
          if (stopped || s.metadata.hasPendingWrites || !s.exists) return;
          const incoming = decodeFromSync(s.data());
          if (incoming === null) return;
          const local = getLocal();
          const merged = mergeProgress(local, incoming);
          if (JSON.stringify(merged) !== JSON.stringify(local)) applyMerged(merged);
        },
        () => {
          if (!stopped) onStatus('error');
        },
      );
      onStatus('synced');
    } catch {
      if (!stopped) onStatus('error');
    }
  })();

  return {
    push(progress) {
      pending = progress;
      if (timer !== null) clearTimeout(timer);
      timer = setTimeout(() => {
        timer = null;
        const p = pending;
        pending = null;
        if (p !== null) write(p);
      }, PUSH_DELAY_MS);
    },
    async flush() {
      if (timer !== null) {
        clearTimeout(timer);
        timer = null;
      }
      const p = pending;
      pending = null;
      if (p !== null) await write(p);
      await writing;
    },
    stop() {
      stopped = true;
      if (timer !== null) clearTimeout(timer);
      if (unsubscribe) unsubscribe();
    },
  };
}

// ---------- global store + hook ----------

let state = {
  progress: loadProgress(),
  session: readLocal(SESSION_KEY),
  syncStatus: 'off',
  syncName: readSyncName(),
};
const listeners = new Set();
let sync = null;
let mounted = 0;

function setState(patch) {
  state = { ...state, ...patch };
  for (const l of listeners) l(state);
}

export function getState() {
  return state;
}

function ensureSync(mode = 'merge') {
  if (sync !== null) return;
  sync = startSync({
    getLocal: () => state.progress,
    applyMerged: (p) => {
      writeLocal(PROGRESS_KEY, p);
      setState({ progress: p });
    },
    onStatus: (s) => setState({ syncStatus: s }),
    mode,
  });
}

function restartSync(mode) {
  sync?.stop();
  sync = null;
  ensureSync(mode);
}

export function useStore() {
  const [s, set] = useState(state);
  useEffect(() => {
    listeners.add(set);
    set(state);
    mounted += 1;
    ensureSync();
    return () => {
      listeners.delete(set);
      mounted -= 1;
      if (mounted === 0) {
        sync?.stop();
        sync = null;
      }
    };
  }, []);

  const setProgress = useCallback((p) => {
    writeLocal(PROGRESS_KEY, p);
    setState({ progress: p });
    sync?.push(p);
  }, []);

  const setSession = useCallback((sess) => {
    writeLocal(SESSION_KEY, sess);
    setState({ session: sess });
  }, []);

  const updateSession = useCallback((fn) => {
    const cur = state.session;
    if (!cur) return;
    const next = fn(cur);
    writeLocal(SESSION_KEY, next);
    setState({ session: next });
  }, []);

  const setSyncName = useCallback(async (name, mode = 'merge') => {
    await sync?.flush();
    writeSyncName(name);
    setState({ syncName: readSyncName() });
    restartSync(mode);
  }, []);

  return { ...s, setProgress, setSession, updateSession, setSyncName };
}
