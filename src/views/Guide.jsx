import { Fragment } from 'preact';
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'preact/hooks';
import { AREAS, BLOCK_NAMES, OBJECTIVE_IDS, STORAGE_PREFIX, areaOf, blockOf } from '../constants.js';
import { ESSENTIALS, GLOSSARY, GUIDE_DOCS, MAP_BY_ID, QUESTIONS } from '../data.js';
import { toggleRevised } from '../score.js';
import { BlockBadge, Rich, barStyle, renderMarkdown, slugify } from '../ui.jsx';
import { readLocal, writeLocal } from '../store.js';
import { startObjectivePractice } from './Setup.jsx';

const NOTES_OPEN_KEY = `${STORAGE_PREFIX}:notes-open`;
const OBJ_HEADING = /^##\s+(\d\.\d\.\d)\s+(.+)$/;

// Split a block's Markdown into an intro plus one chunk per "## X.Y.Z Title" heading.
function splitObjectives(markdown) {
  const lines = markdown.split(/\r?\n/);
  const intro = [];
  const chunks = [];
  let cur = null;
  for (const line of lines) {
    const m = line.match(OBJ_HEADING);
    if (m) {
      cur = { objective: m[1], title: m[2].trim(), lines: [] };
      chunks.push(cur);
    } else if (cur) cur.lines.push(line);
    else if (!/^#\s/.test(line)) intro.push(line);
  }
  return { intro: intro.join('\n').trim(), chunks: chunks.map((c) => ({ ...c, md: c.lines.join('\n').trim() })) };
}

function scrollToId(id, behavior = 'smooth') {
  document.getElementById(id)?.scrollIntoView({ behavior, block: 'start' });
}

export function Guide({ store, slug, objective }) {
  if (!slug) return <GuideIndex progress={store.progress} />;
  const index = GUIDE_DOCS.findIndex((d) => d.slug === slug);
  if (index === -1) {
    window.location.hash = '#/guide';
    return null;
  }
  return <GuideDoc key={slug} store={store} index={index} objective={objective} />;
}

function GuideIndex({ progress }) {
  return (
    <main class="page">
      <a class="back-link" href="#/">
        ← Home
      </a>
      <h1>Revision guide</h1>
      <ul class="guide-index">
        {GUIDE_DOCS.map((d) => {
          const objs = d.block ? OBJECTIVE_IDS.filter((o) => blockOf(o) === d.block) : [];
          const done = objs.filter((o) => progress.revised.includes(o)).length;
          return (
            <li key={d.slug}>
              <a class="guide-index-link" href={`#/guide/${d.slug}`}>
                {d.block && <BlockBadge block={d.block} />}
                <span class="guide-index-title">{d.block ? BLOCK_NAMES[d.block] : d.title}</span>
                {d.block && (
                  <span class="muted guide-index-meta">
                    {done} / {objs.length} revised
                  </span>
                )}
              </a>
            </li>
          );
        })}
      </ul>
    </main>
  );
}

function GuideDoc({ store, index, objective }) {
  const { progress, setProgress } = store;
  const doc = GUIDE_DOCS[index];
  const prevDoc = GUIDE_DOCS[index - 1];
  const nextDoc = GUIDE_DOCS[index + 1];
  const split = useMemo(() => (doc.block ? splitObjectives(doc.markdown) : null), [doc]);
  const html = useMemo(() => (doc.block ? null : renderMarkdown(doc.markdown, { dropTitle: true })), [doc]);
  const [openNotes, setOpenNotes] = useState(() => new Set(readLocal(NOTES_OPEN_KEY, [])));
  const wide = typeof window !== 'undefined' && window.matchMedia?.('(min-width: 720px)').matches;

  const toc = useMemo(() => {
    if (split) return split.chunks.map((c) => ({ id: `obj-${c.objective.replaceAll('.', '-')}`, text: `${c.objective} ${c.title}` }));
    return [...doc.markdown.matchAll(/^##\s+(.+)$/gm)].map((m) => ({ id: slugify(m[1]), text: m[1] }));
  }, [doc, split]);

  useEffect(() => {
    if (!objective) return;
    const id = doc.slug === 'glossary' ? objective : `obj-${objective}`;
    const t = setTimeout(() => scrollToId(id, 'auto'), 30);
    return () => clearTimeout(t);
  }, [objective, doc.slug]);

  function setNotes(o, open) {
    setOpenNotes((prev) => {
      const s = new Set(prev);
      open ? s.add(o) : s.delete(o);
      writeLocal(NOTES_OPEN_KEY, [...s]);
      return s;
    });
  }

  const objs = split ? split.chunks.map((c) => c.objective) : [];
  const revisedCount = objs.filter((o) => progress.revised.includes(o)).length;
  const returnBase = `#/guide/${doc.slug}/`;

  return (
    <main class="page guide-page">
      <a class="back-link" href="#/guide">
        ← Revision guide
      </a>
      <h1>{doc.title}</h1>
      {split && (
        <div class="chapter-progress">
          <p class="muted">
            {revisedCount} of {objs.length} objectives revised
          </p>
          <div class="bar-track">
            <div class="bar-fill" style={barStyle(objs.length ? Math.round((revisedCount / objs.length) * 100) : 0, doc.block)} />
          </div>
        </div>
      )}
      {toc.length > 0 && (
        <details class="guide-toc" open={wide}>
          <summary class="guide-toc-label">Contents</summary>
          <ul>
            {toc.map((t) => (
              <li key={t.id}>
                <a
                  href={`#${t.id}`}
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToId(t.id);
                  }}
                >
                  {t.text}
                </a>
              </li>
            ))}
          </ul>
        </details>
      )}
      {split ? (
        <div class="guide">
          {split.intro && <div class="guide-intro" dangerouslySetInnerHTML={{ __html: renderMarkdown(split.intro) }} />}
          {split.chunks.map((c, i) => {
            const area = areaOf(c.objective);
            const newArea = i === 0 || areaOf(split.chunks[i - 1].objective) !== area;
            return (
              <Fragment key={c.objective}>
                {newArea && (
                  <h2 class="area-heading" id={`area-${area.replace('.', '-')}`}>
                    <span class="area-num">{area}</span> {AREAS[area]}
                  </h2>
                )}
                <ObjectiveBlock
                  chunk={c}
                  block={doc.block}
                  revised={progress.revised.includes(c.objective)}
                  notesOpen={openNotes.has(c.objective)}
                  onNotes={(open) => setNotes(c.objective, open)}
                  onRevised={() => setProgress(toggleRevised(progress, c.objective))}
                  onTry={() => startObjectivePractice(store, c.objective, `${returnBase}${c.objective.replaceAll('.', '-')}`)}
                />
              </Fragment>
            );
          })}
        </div>
      ) : (
        <div class="guide" dangerouslySetInnerHTML={{ __html: html }} />
      )}
      <nav class="guide-pager">
        {prevDoc ? (
          <a class="nav-link" href={`#/guide/${prevDoc.slug}`}>
            ← {prevDoc.title}
          </a>
        ) : (
          <span />
        )}
        {nextDoc && (
          <a class="nav-link" href={`#/guide/${nextDoc.slug}`}>
            {nextDoc.title} →
          </a>
        )}
      </nav>
    </main>
  );
}

// Term chips open their glossary definition in a popover under the chip, so reading one
// doesn't leave the page. The popover follows its chip in the DOM to keep tab order.
function TermChips({ terms, objective }) {
  const [open, setOpen] = useState(null);
  const wrapRef = useRef(null);
  const popRef = useRef(null);
  const chipRefs = useRef({});
  const popId = `term-pop-${objective.replaceAll('.', '-')}`;

  useLayoutEffect(() => {
    if (!open) return;
    const place = () => {
      const wrap = wrapRef.current;
      const chip = chipRefs.current[open];
      const pop = popRef.current;
      if (!wrap || !chip || !pop) return;
      const center = chip.offsetLeft + chip.offsetWidth / 2;
      const left = Math.max(0, Math.min(center - pop.offsetWidth / 2, wrap.clientWidth - pop.offsetWidth));
      pop.style.top = `${chip.offsetTop + chip.offsetHeight + 8}px`;
      pop.style.left = `${left}px`;
      pop.style.setProperty('--caret', `${center - left}px`);
    };
    place();
    popRef.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    window.addEventListener('resize', place);
    return () => window.removeEventListener('resize', place);
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onDown = (ev) => {
      if (!wrapRef.current?.contains(ev.target)) setOpen(null);
    };
    const onKey = (ev) => {
      if (ev.key !== 'Escape') return;
      chipRefs.current[open]?.focus();
      setOpen(null);
    };
    document.addEventListener('pointerdown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('pointerdown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  return (
    <div class="chip-group term-chips" ref={wrapRef}>
      {terms.map((t) => {
        const entry = GLOSSARY.get(t.toLowerCase());
        const href = `#/guide/glossary/${slugify(t)}`;
        if (!entry) {
          return (
            <a key={t} class="chip chip-small" href={href}>
              {t}
            </a>
          );
        }
        const isOpen = open === t;
        return (
          <Fragment key={t}>
            <button
              type="button"
              class={`chip chip-small${isOpen ? ' chip-selected' : ''}`}
              ref={(el) => (chipRefs.current[t] = el)}
              aria-expanded={isOpen}
              aria-controls={isOpen ? popId : undefined}
              onClick={() => setOpen(isOpen ? null : t)}
            >
              {t}
            </button>
            {isOpen && (
              <div class="term-pop" id={popId} role="dialog" aria-label={entry.term} ref={popRef}>
                <button type="button" class="term-pop-close" aria-label="Close" onClick={() => setOpen(null)}>
                  ×
                </button>
                <p class="term-pop-title">
                  {entry.term}
                  {entry.note && <span class="gl-note"> {entry.note}</span>}
                </p>
                <Rich as="p" class="term-pop-def" text={entry.def.replace(/^[a-z]/, (c) => c.toUpperCase())} />
                <a class="term-pop-link" href={href}>
                  Open in glossary →
                </a>
              </div>
            )}
          </Fragment>
        );
      })}
    </div>
  );
}

function ObjectiveBlock({ chunk, block, revised, notesOpen, onNotes, onRevised, onTry }) {
  const e = ESSENTIALS.get(chunk.objective);
  const html = useMemo(() => renderMarkdown(chunk.md), [chunk.md]);
  const count = QUESTIONS.filter((q) => q.objective === chunk.objective).length;
  return (
    <section class="objective-block" id={`obj-${chunk.objective.replaceAll('.', '-')}`}>
      <header class="obj-header">
        <BlockBadge block={block} />
        <h3 class="obj-heading">
          {chunk.objective} {chunk.title}
        </h3>
        {revised && <span class="revised-tick">✓ Revised</span>}
      </header>
      {e && (
        <div class="essentials-panel">
          <Rich as="p" class="essentials-lede" text={e.oneLine} />
          <p class="essentials-label">Know this</p>
          <ul class="know-list">
            {e.know.map((k, i) => (
              <li key={i}>
                <Rich as="p" class="know-cue" text={k.cue} />
                <Rich as="p" class="know-fact" text={k.fact} />
                <p class="know-why">
                  <span class="know-why-label">Exam angle:</span> <Rich text={k.why} />
                </p>
              </li>
            ))}
          </ul>
          {e.terms?.length > 0 && <TermChips terms={e.terms} objective={chunk.objective} />}
          {e.maps?.length > 0 && (
            <div class="map-links">
              {e.maps.map((m) => (
                <a key={m} class="map-link" href={`#/maps/${m}`}>
                  Decision map: {MAP_BY_ID.get(m)?.title ?? m}
                </a>
              ))}
            </div>
          )}
        </div>
      )}
      <details class="full-notes" open={notesOpen} onToggle={(ev) => onNotes(ev.currentTarget.open)}>
        <summary>Full notes</summary>
        <div dangerouslySetInnerHTML={{ __html: html }} />
      </details>
      <div class="objective-actions">
        <button class="btn btn-primary" onClick={onTry} disabled={count === 0}>
          Try 5 questions on {chunk.objective}
        </button>
        <label class="revised-check">
          <input type="checkbox" id={`revised-${chunk.objective}`} checked={revised} onChange={onRevised} />
          Mark {chunk.objective} as revised
        </label>
      </div>
    </section>
  );
}
