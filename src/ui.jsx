import { Marked } from 'marked';
import { BLOCK_NAMES } from './constants.js';
import { escapeHtml, highlight } from './highlight.js';

const STROKE = 1.75;

export function Icon({ name, size = 20 }) {
  const p = { width: size, height: size, viewBox: '0 0 24 24', 'aria-hidden': 'true' };
  const line = { fill: 'none', stroke: 'currentColor', 'stroke-width': STROKE, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
  switch (name) {
    case 'flag':
      return (
        <svg {...p}>
          <path d="M6 3v18" {...line} />
          <path d="M6 4h12l-3 4 3 4H6z" {...line} />
        </svg>
      );
    case 'flag-filled':
      return (
        <svg {...p}>
          <path d="M6 3v18" {...line} />
          <path d="M6 4h12l-3 4 3 4H6z" fill="currentColor" />
        </svg>
      );
    case 'check':
      return (
        <svg {...p}>
          <path d="M4 12.5l5 5L20 6.5" {...line} />
        </svg>
      );
    case 'cross':
      return (
        <svg {...p}>
          <path d="M5 5l14 14M19 5L5 19" {...line} />
        </svg>
      );
    case 'bookmark':
      return (
        <svg {...p}>
          <path d="M6 3.5h12v17l-6-4-6 4z" {...line} />
        </svg>
      );
    case 'bookmark-filled':
      return (
        <svg {...p}>
          <path d="M6 3.5h12v17l-6-4-6 4z" fill="currentColor" />
        </svg>
      );
    default:
      return null;
  }
}

export function blockStyle(block) {
  return `background:color-mix(in srgb, var(--b${block}) 14%, transparent);color:var(--b${block})`;
}

export function barStyle(pct, block) {
  return `width:${Math.max(0, Math.min(100, pct))}%;background:var(--b${block})`;
}

export function BlockBadge({ block, label }) {
  return (
    <span class="block-badge" style={blockStyle(block)} title={BLOCK_NAMES[block]}>
      {label ?? `B${block}`}
    </span>
  );
}

// Inline markup used in question and card text: `code` and **bold**.
function inlineHtml(text) {
  let out = '';
  let last = 0;
  for (const m of text.matchAll(/`([^`]+)`|\*\*([^*]+)\*\*/g)) {
    out += escapeHtml(text.slice(last, m.index));
    out += m[1] !== undefined ? `<code>${escapeHtml(m[1])}</code>` : `<strong>${escapeHtml(m[2])}</strong>`;
    last = m.index + m[0].length;
  }
  return out + escapeHtml(text.slice(last));
}

export function CodeBlock({ code, lang = 'python', label }) {
  return (
    <div class="code-block">
      {label && <span class="code-label">{label}</span>}
      <pre>
        <code dangerouslySetInnerHTML={{ __html: highlight(code, lang) }} />
      </pre>
    </div>
  );
}

// Text containing a line break is shown as a code block; otherwise inline markup.
export function Rich({ text, lang = 'python', as: Tag = 'span', class: cls }) {
  if (text == null || text === '') return null;
  if (text.includes('\n')) {
    const code = text.replace(/^```\w*\n?/, '').replace(/\n?```$/, '');
    return (
      <pre class={`code-inline-block ${cls ?? ''}`}>
        <code dangerouslySetInnerHTML={{ __html: highlight(code, lang) }} />
      </pre>
    );
  }
  return <Tag class={cls} dangerouslySetInnerHTML={{ __html: inlineHtml(text) }} />;
}

// ---------- Markdown ----------

export function slugify(s) {
  return s
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function headingId(text) {
  const m = text.match(/^(\d)\.(\d)\.(\d)\b/);
  return m ? `obj-${m[1]}-${m[2]}-${m[3]}` : slugify(text) || 'section';
}

// Glossary lines "**Term** — definition" become a definition list.
function glossaryToDl(md) {
  const re = /^\*\*(.+?)\*\*\s*(\([^)]*\))?\s*[\u2014\u2013:-]\s+(.+)$/;
  const out = [];
  let open = false;
  for (const line of md.split(/\r?\n/)) {
    const m = line.match(re);
    if (m) {
      if (!open) {
        out.push('<dl class="glossary">');
        open = true;
      }
      const note = m[2] ? ` <span class="gl-note">${m[2]}</span>` : '';
      out.push(`<dt id="${slugify(m[1])}">${m[1]}${note}</dt><dd>${inlineHtml(m[3])}</dd>`);
    } else {
      if (open) {
        out.push('</dl>');
        open = false;
      }
      out.push(line);
    }
  }
  if (open) out.push('</dl>');
  return out.join('\n');
}

export function renderMarkdown(md, { dropTitle = false } = {}) {
  let source = /^# Glossary/m.test(md) ? glossaryToDl(md) : md;
  // The page already shows the document title as its own heading.
  if (dropTitle) source = source.replace(/^#\s+.+\r?\n/, '');
  const seen = new Map();
  const uniqueId = (text) => {
    const id = headingId(text);
    const n = seen.get(id) ?? 0;
    seen.set(id, n + 1);
    return n === 0 ? id : `${id}-${n + 1}`;
  };
  const marked = new Marked({
    gfm: true,
    renderer: {
      heading({ tokens, depth, text }) {
        const inner = this.parser.parseInline(tokens);
        if (depth !== 2 && depth !== 3) return `<h${depth}>${inner}</h${depth}>\n`;
        return `<h${depth} id="${uniqueId(text)}">${inner}</h${depth}>\n`;
      },
      code({ text, lang }) {
        const l = (lang || 'python').split(/\s/)[0];
        const label = l === 'text' ? 'Output' : l === 'sql' ? 'SQL' : 'Python';
        return `<div class="code-block"><span class="code-label">${label}</span><pre><code>${highlight(text, l)}</code></pre></div>\n`;
      },
    },
  });
  return marked.parse(source).replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, '</table></div>');
}
