// Python in the browser: Pyodide runs in a Web Worker so a long or endless cell cannot freeze the page,
// and a stuck run can be stopped by terminating the worker. The same runner.py the verify script uses
// executes each cell (setup, then the learner's code, then the check).
import { useEffect, useState } from 'preact/hooks';
import RUNNER from './runner.py';

export const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/';
const RUN_LIMIT_MS = 30000;

const WORKER_SRC = `
importScripts(${JSON.stringify(`${PYODIDE_URL}pyodide.js`)});
let ready = null;
function boot(runner) {
  if (!ready) {
    ready = loadPyodide({ indexURL: ${JSON.stringify(PYODIDE_URL)} }).then((py) => {
      py.runPython(runner);
      return py;
    });
  }
  return ready;
}
self.onmessage = async (e) => {
  const { id, runner, setup, code, check, before } = e.data;
  try {
    const py = await boot(runner);
    postMessage({ id, status: 'packages' });
    try {
      await py.loadPackagesFromImports([setup, ...before, code, check || ''].join('\\n'), {
        messageCallback: (m) => postMessage({ id, log: m }),
      });
    } catch (err) {
      postMessage({ id, log: String((err && err.message) || err) });
    }
    postMessage({ id, status: 'running' });
    const run = py.globals.get('run_cell');
    const pyBefore = py.toPy(before);
    // JS null would arrive as JsNull, not None; undefined converts to None.
    const res = run(setup, code, check ?? undefined, pyBefore);
    const out = res.toJs({ dict_converter: Object.fromEntries });
    res.destroy();
    pyBefore.destroy();
    run.destroy();
    postMessage({ id, result: out });
  } catch (err) {
    postMessage({ id, fatal: String((err && err.message) || err) });
  }
};
`;

// ---------- shared state, observed by every notebook cell ----------

let worker = null;
let started = false; // Pyodide has finished loading at least once in this worker
let current = null; // { id, resolve, timer }
let nextId = 1;
let state = { phase: 'off', message: '' }; // off | starting | packages | running | ready | failed
const listeners = new Set();

function setState(next) {
  state = { ...state, ...next };
  for (const l of listeners) l(state);
}

export function usePython() {
  const [s, set] = useState(state);
  useEffect(() => {
    listeners.add(set);
    set(state);
    return () => listeners.delete(set);
  }, []);
  return s;
}

function finish(payload) {
  if (!current) return;
  clearTimeout(current.timer);
  const { resolve } = current;
  current = null;
  resolve(payload);
}

function onMessage(e) {
  const msg = e.data;
  if (!current || msg.id !== current.id) return;
  if (msg.status === 'packages') {
    started = true;
    setState({ phase: 'packages', message: '' });
  } else if (msg.log) {
    setState({ message: msg.log });
  } else if (msg.status === 'running') {
    setState({ phase: 'running', message: '' });
    current.timer = setTimeout(() => {
      terminate();
      finish({ stopped: `Stopped after ${RUN_LIMIT_MS / 1000} seconds. Look for a loop that never ends; Python restarts on the next run.` });
    }, RUN_LIMIT_MS);
  } else if (msg.result) {
    setState({ phase: 'ready', message: '' });
    finish({ result: msg.result });
  } else if (msg.fatal) {
    const loading = !started;
    if (loading) terminate();
    setState({ phase: loading ? 'failed' : 'ready', message: loading ? msg.fatal : '' });
    finish({ fatal: loading ? `Python could not start: ${msg.fatal}` : msg.fatal });
  }
}

function ensureWorker() {
  if (worker) return worker;
  const url = URL.createObjectURL(new Blob([WORKER_SRC], { type: 'text/javascript' }));
  worker = new Worker(url);
  URL.revokeObjectURL(url);
  started = false;
  worker.onmessage = onMessage;
  worker.onerror = (e) => {
    e.preventDefault?.();
    terminate();
    setState({ phase: 'failed', message: e.message || 'the Python worker failed to load' });
    finish({ fatal: `Python could not start: ${e.message || 'the Python runtime could not be downloaded'}.` });
  };
  return worker;
}

function terminate() {
  if (worker) worker.terminate();
  worker = null;
  started = false;
  setState({ phase: 'off', message: '' });
}

// Ends the worker and any run in progress. The next run starts a fresh one.
export function stopPython() {
  terminate();
  finish({ stopped: 'Stopped. Python restarts on the next run.' });
}

// Resolves to { result } | { stopped } | { fatal }. One run at a time.
export function runPython({ setup, code, check = null, before = [] }) {
  if (current) return Promise.resolve({ fatal: 'Another cell is still running.' });
  return new Promise((resolve) => {
    let w;
    try {
      w = ensureWorker();
    } catch (err) {
      setState({ phase: 'failed', message: String(err?.message ?? err) });
      resolve({ fatal: `Python could not start in this browser (${err?.message ?? err}).` });
      return;
    }
    current = { id: nextId++, resolve, timer: null };
    setState({ phase: started ? 'packages' : 'starting', message: '' });
    w.postMessage({ id: current.id, runner: RUNNER, setup, code, check, before });
  });
}
