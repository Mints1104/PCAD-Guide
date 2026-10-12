import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { BLOCKS, BLOCK_NAMES, EXAM, OBJECTIVES, OBJECTIVE_IDS, blockOf } from '../constants.js';
import { QUESTION_BY_ID } from '../data.js';
import { TREND_WINDOW, trendPoints, trendSummary } from '../score.js';

const HEIGHT = 220;
const PAD = { top: 14, right: 14, bottom: 30, left: 40 };
const GRID = [0, 25, 50, 100];
const PASS = EXAM.pass * 100;
const MODE_LABEL = { practice: 'Practice', mock: 'Mock test', mixed: 'Practice + mock' };

export function topicLabel(topic) {
  if (topic === 'all') return 'All topics';
  if (topic.startsWith('b')) return `Block ${topic.slice(1)}: ${BLOCK_NAMES[Number(topic.slice(1))]}`;
  return `${topic} ${OBJECTIVES[topic]}`;
}

function shortDate(ts) {
  return new Date(ts).toLocaleDateString(undefined, { day: 'numeric', month: 'short' });
}

function longWhen(ts, by) {
  return by === 'day'
    ? new Date(ts).toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
    : new Date(ts).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}

// Indices to label on the x-axis: always the first and last, evenly spaced between.
function tickIndices(n, max) {
  if (n <= max) return [...Array(n).keys()];
  const out = new Set([0, n - 1]);
  const step = (n - 1) / (max - 1);
  for (let i = 1; i < max - 1; i += 1) out.add(Math.round(i * step));
  return [...out].sort((a, b) => a - b);
}

function Marker({ x, y, mode, r = 4, cls = 'trend-dot' }) {
  // Mock tests get a square so they read apart from practice without relying on colour.
  return mode === 'mock' ? (
    <rect class={cls} x={x - r} y={y - r} width={r * 2} height={r * 2} rx={1.5} />
  ) : (
    <circle class={cls} cx={x} cy={y} r={r} />
  );
}

export function TrendSection({ topic, setTopic, attempts }) {
  const [by, setBy] = useState('session');
  const [mode, setMode] = useState('all');
  const points = useMemo(() => trendPoints(attempts, QUESTION_BY_ID, { topic, by, mode }), [attempts, topic, by, mode]);
  const summary = trendSummary(points);
  const unit = by === 'day' ? 'day' : 'session';

  return (
    <section class="card" id="trend">
      <h2>Progress over time</h2>
      <p class="muted">Your score on each {unit}, oldest on the left. Pick a topic to see how you're doing on it alone.</p>
      <select class="browse-objective trend-topic" aria-label="Topic" value={topic} onChange={(e) => setTopic(e.currentTarget.value)}>
        <option value="all">All topics</option>
        <optgroup label="Blocks">
          {BLOCKS.map((b) => (
            <option key={b} value={`b${b}`}>
              Block {b}: {BLOCK_NAMES[b]}
            </option>
          ))}
        </optgroup>
        {BLOCKS.map((b) => (
          <optgroup key={b} label={`Block ${b} objectives`}>
            {OBJECTIVE_IDS.filter((o) => blockOf(o) === b).map((o) => (
              <option key={o} value={o}>
                {o} {OBJECTIVES[o]}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
      <div class="trend-controls">
        <div class="chip-group" role="group" aria-label="Group by">
          {[
            ['session', 'Each session'],
            ['day', 'Each day'],
          ].map(([k, label]) => (
            <button key={k} class={`chip chip-small ${by === k ? 'chip-selected' : ''}`} aria-pressed={by === k} onClick={() => setBy(k)}>
              {label}
            </button>
          ))}
        </div>
        <div class="chip-group" role="group" aria-label="Which sessions">
          {[
            ['all', 'Practice + mock'],
            ['practice', 'Practice'],
            ['mock', 'Mock tests'],
          ].map(([k, label]) => (
            <button key={k} class={`chip chip-small ${mode === k ? 'chip-selected' : ''}`} aria-pressed={mode === k} onClick={() => setMode(k)}>
              {label}
            </button>
          ))}
        </div>
      </div>

      {points.length === 0 ? (
        <p class="trend-empty muted">
          No answers {topic === 'all' ? '' : 'on this topic '}yet{mode !== 'all' ? ` in ${mode === 'mock' ? 'mock tests' : 'practice'}` : ''}. Finish a {mode === 'mock' ? 'mock test' : 'practice session or mock test'}
          {topic === 'all' ? '' : ' that includes it'} and it will show here.
        </p>
      ) : (
        <>
          {summary && (
            <p class="trend-summary">
              {summary.change > 0 ? (
                <>
                  <strong>Up {summary.change} points.</strong>{' '}
                </>
              ) : summary.change < 0 ? (
                <>
                  <strong>Down {-summary.change} points.</strong>{' '}
                </>
              ) : (
                <>
                  <strong>Level.</strong>{' '}
                </>
              )}
              Your last {summary.k === 1 ? unit : `${summary.k} ${unit}s`} averaged {summary.last}%; your first {summary.k === 1 ? unit : `${summary.k} ${unit}s`} averaged {summary.first}%.
              {summary.questions < 10 && <span class="muted"> Only {summary.questions} questions so far, so treat this as a rough signal.</span>}
            </p>
          )}
          <TrendChart points={points} by={by} showPass={topic === 'all'} />
          <details class="trend-table">
            <summary>Show as a table</summary>
            <div class="table-wrap">
              <table class="results-table">
                <thead>
                  <tr>
                    <th>{by === 'day' ? 'Day' : 'Session'}</th>
                    <th>Type</th>
                    <th>Correct</th>
                    <th>Score</th>
                  </tr>
                </thead>
                <tbody>
                  {points
                    .slice()
                    .reverse()
                    .map((p) => (
                      <tr key={p.key}>
                        <td>{longWhen(p.at, by)}</td>
                        <td>{MODE_LABEL[p.mode]}</td>
                        <td>
                          {p.correct} / {p.total}
                        </td>
                        <td>{Math.round(p.pct)}%</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </details>
        </>
      )}
    </section>
  );
}

function TrendChart({ points, by, showPass }) {
  const wrap = useRef(null);
  const [width, setWidth] = useState(640);
  const [active, setActive] = useState(null);

  useLayoutEffect(() => {
    const el = wrap.current;
    if (!el) return undefined;
    const measure = () => setWidth(Math.max(240, Math.round(el.clientWidth)));
    measure();
    if (typeof ResizeObserver === 'undefined') return undefined;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => setActive(null), [points]);

  const n = points.length;
  const plotW = width - PAD.left - PAD.right;
  const plotH = HEIGHT - PAD.top - PAD.bottom;
  const step = n > 1 ? plotW / (n - 1) : 0;
  const x = (i) => (n > 1 ? PAD.left + i * step : PAD.left + plotW / 2);
  const y = (v) => PAD.top + plotH * (1 - v / 100);
  const ticks = tickIndices(n, Math.max(2, Math.floor(plotW / 72)));
  const modes = new Set(points.map((p) => p.mode));
  const showAvg = n >= TREND_WINDOW;
  const unit = by === 'day' ? 'day' : 'session';
  const line = (key) => points.map((p, i) => `${i === 0 ? 'M' : 'L'}${x(i).toFixed(1)},${y(p[key]).toFixed(1)}`).join('');
  const dots = n <= 80;

  const pick = (clientX) => {
    const rect = wrap.current.getBoundingClientRect();
    const px = clientX - rect.left;
    const i = n > 1 ? Math.round((px - PAD.left) / step) : 0;
    setActive(Math.min(n - 1, Math.max(0, i)));
  };
  const onKey = (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      e.preventDefault();
      const d = e.key === 'ArrowLeft' ? -1 : 1;
      setActive((a) => Math.min(n - 1, Math.max(0, (a ?? (d < 0 ? n : -1)) + d)));
    } else if (e.key === 'Escape') setActive(null);
  };

  const p = active === null ? null : points[active];
  // The tooltip sits beside the crosshair, on whichever side has more room, so it never covers the point.
  const tipRight = p ? x(active) < width / 2 : true;

  return (
    <div class="trend-chart">
      <div class="trend-key" aria-hidden="true">
        {showAvg && (
          <span>
            <svg width="18" height="10">
              <line class="trend-avg" x1="1" x2="17" y1="5" y2="5" />
            </svg>
            Average of last {TREND_WINDOW} {unit}s
          </span>
        )}
        {(modes.has('practice') || modes.has('mixed')) && (
          <span>
            <svg width="10" height="10">
              <circle class="trend-dot" cx="5" cy="5" r="3.5" />
            </svg>
            {by === 'day' ? 'Each day' : 'Practice session'}
          </span>
        )}
        {modes.has('mock') && (
          <span>
            <svg width="10" height="10">
              <rect class="trend-dot" x="1.5" y="1.5" width="7" height="7" rx="1.5" />
            </svg>
            Mock test
          </span>
        )}
        {showPass && (
          <span>
            <svg width="18" height="10">
              <line class="trend-pass" x1="1" x2="17" y1="5" y2="5" />
            </svg>
            Pass mark ({PASS}%)
          </span>
        )}
      </div>
      <div class="trend-plot" ref={wrap}>
        <svg
          width={width}
          height={HEIGHT}
          role="img"
          tabIndex={0}
          aria-label={`Score per ${unit}: ${n} point${n === 1 ? '' : 's'}, from ${Math.round(points[0].pct)}% to ${Math.round(points[n - 1].pct)}%. Use the left and right arrow keys to read each point.`}
          onPointerMove={(e) => pick(e.clientX)}
          onPointerDown={(e) => pick(e.clientX)}
          onPointerLeave={(e) => e.pointerType === 'mouse' && setActive(null)}
          onKeyDown={onKey}
          onBlur={() => setActive(null)}
        >
          {GRID.map((v) => (
            <g key={v}>
              <line class="trend-grid" x1={PAD.left} x2={width - PAD.right} y1={y(v)} y2={y(v)} />
              <text class="trend-axis" x={PAD.left - 8} y={y(v)} dy="0.32em" text-anchor="end">
                {v}%
              </text>
            </g>
          ))}
          <line class={showPass ? 'trend-pass' : 'trend-grid'} x1={PAD.left} x2={width - PAD.right} y1={y(PASS)} y2={y(PASS)} />
          <text class="trend-axis" x={PAD.left - 8} y={y(PASS)} dy="0.32em" text-anchor="end">
            {PASS}%
          </text>
          {ticks.map((i) => (
            <text key={i} class="trend-axis" x={x(i)} y={HEIGHT - 8} text-anchor={n > 1 && i === 0 ? 'start' : n > 1 && i === n - 1 ? 'end' : 'middle'}>
              {by === 'day' ? shortDate(points[i].at) : `#${i + 1}`}
            </text>
          ))}
          {p && <line class="trend-crosshair" x1={x(active)} x2={x(active)} y1={PAD.top} y2={PAD.top + plotH} />}
          {n > 1 && <path class="trend-line" d={line('pct')} />}
          {(dots || n === 1) && points.map((pt, i) => <Marker key={pt.key} x={x(i)} y={y(pt.pct)} mode={pt.mode} r={3.5} />)}
          {showAvg && <path class="trend-avg" d={line('avg')} />}
          {p && <Marker x={x(active)} y={y(p.pct)} mode={p.mode} r={5.5} cls="trend-dot trend-dot-active" />}
        </svg>
        {p && (
          <div class="trend-tip" style={`left:${x(active) + (tipRight ? 12 : -12)}px;top:${PAD.top}px;transform:translateX(${tipRight ? '0' : '-100%'})`}>
            <strong>{Math.round(p.pct)}%</strong>
            <span>
              {p.correct} / {p.total} correct
            </span>
            {showAvg && (
              <span>
                Average of last {TREND_WINDOW}: {Math.round(p.avg)}%
              </span>
            )}
            <span class="muted">
              {by === 'day' ? longWhen(p.at, by) : `Session ${active + 1} · ${longWhen(p.at, by)}`}
            </span>
            <span class="muted">{MODE_LABEL[p.mode]}</span>
          </div>
        )}
      </div>
    </div>
  );
}

// A tiny line of the rolling average for a table row (single sessions often hold only one or two
// questions on an objective, so raw scores jump between 0 and 100%). The y-scale is always 0–100%.
export function Sparkline({ points }) {
  if (points.length < 2) return <span class="muted">—</span>;
  const pts = points.slice(-12);
  const w = 72;
  const h = 22;
  const xs = (i) => 3 + (i * (w - 6)) / (pts.length - 1);
  const ys = (v) => 3 + (h - 6) * (1 - v / 100);
  const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${xs(i).toFixed(1)},${ys(p.avg).toFixed(1)}`).join('');
  const last = pts[pts.length - 1];
  return (
    <svg class="sparkline" width={w} height={h} role="img" aria-label={`Average over your last ${pts.length} sessions: from ${Math.round(pts[0].avg)}% to ${Math.round(last.avg)}%`}>
      <path d={d} />
      <circle cx={xs(pts.length - 1)} cy={ys(last.avg)} r="2.5" />
    </svg>
  );
}
