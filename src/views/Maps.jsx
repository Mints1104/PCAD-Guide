import { useEffect, useState } from 'preact/hooks';
import { blockOf } from '../constants.js';
import { MAPS, MAP_BY_ID, guideHref } from '../data.js';
import { CodeBlock, Rich, blockStyle } from '../ui.jsx';
import { startObjectivePractice } from './Setup.jsx';

function ObjectivePill({ objective }) {
  return (
    <span class="pill" style={blockStyle(blockOf(objective))}>
      {objective}
    </span>
  );
}

export function Maps({ store, id }) {
  return id ? <MapView key={id} store={store} id={id} /> : <MapIndex />;
}

function MapIndex() {
  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Decision maps</h1>
      <p class="muted">For the "which method?" questions. Answer a few questions about the situation and land on the technique the syllabus expects.</p>
      <ul class="row-list">
        {MAPS.map((m) => (
          <li key={m.id}>
            <a class="row-link" href={`#/maps/${m.id}`}>
              <span class="row-link-title">{m.title}</span>
              <span class="chip-group">
                {m.objectives.map((o) => (
                  <ObjectivePill key={o} objective={o} />
                ))}
              </span>
              <span class="row-link-meta muted">{Object.keys(m.leaves).length} outcomes</span>
            </a>
          </li>
        ))}
      </ul>
    </main>
  );
}

function MapView({ store, id }) {
  const map = MAP_BY_ID.get(id);
  const [node, setNode] = useState(map?.start ?? '');
  const [trail, setTrail] = useState([]);
  const current = map?.nodes[node];

  function choose(opt) {
    setTrail((t) => [...t, { node, label: opt.label }]);
    setNode(opt.next);
  }

  useEffect(() => {
    if (!current) return;
    function onKey(e) {
      const i = Number(e.key) - 1;
      if (Number.isInteger(i) && i >= 0 && i < current.options.length) {
        e.preventDefault();
        choose(current.options[i]);
      }
    }
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [current, node]);

  if (!map) {
    return (
      <main class="page">
        <h1>Decision maps</h1>
        <p class="empty-note">That map does not exist.</p>
        <a class="link-btn" href="#/maps">
          ← All maps
        </a>
      </main>
    );
  }

  const leaf = current ? undefined : map.leaves[node];
  return (
    <main class="page">
      <a class="back-link" href="#/maps">
        ← All maps
      </a>
      <h1>{map.title}</h1>
      <p class="map-intro muted">{map.intro}</p>
      {trail.length > 0 && (
        <div class="chip-group trail">
          {trail.map((t, i) => (
            <button
              key={i}
              type="button"
              class="chip chip-small"
              title="Go back to this step"
              onClick={() => {
                setNode(trail[i].node);
                setTrail((tr) => tr.slice(0, i));
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
      )}
      <div class="card map-card" key={node}>
        {current ? (
          <>
            <p class="stem">{current.text}</p>
            <div class="options">
              {current.options.map((o, i) => (
                <button key={o.next + i} type="button" class="option" onClick={() => choose(o)}>
                  <span class="option-letter">{i + 1}</span>
                  <Rich class="option-text" text={o.label} />
                </button>
              ))}
            </div>
          </>
        ) : leaf ? (
          <div>
            <p class="leaf-eyebrow">Use this</p>
            <h2 class="leaf-title">
              <Rich text={leaf.title} />
            </h2>
            <Rich as="p" text={leaf.detail} />
            {leaf.code && <CodeBlock code={leaf.code} lang={leaf.lang ?? 'python'} label={leaf.lang === 'sql' ? 'SQL' : 'Python'} />}
            <div class="actions">
              <a class="btn" href={guideHref(leaf.objective)}>
                Read {leaf.objective} in the guide →
              </a>
              <button type="button" class="btn btn-primary" onClick={() => startObjectivePractice(store, leaf.objective)}>
                Try 5 questions on {leaf.objective}
              </button>
            </div>
          </div>
        ) : (
          <p class="empty-note">This map is missing a step called "{node}".</p>
        )}
      </div>
      <div class="actions">
        <button
          type="button"
          class="btn"
          onClick={() => {
            setNode(map.start);
            setTrail([]);
          }}
        >
          Start again
        </button>
      </div>
    </main>
  );
}
