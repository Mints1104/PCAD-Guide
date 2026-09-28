// Content is assembled and validated by scripts/build.mjs into .build/content.json.
import content from '../.build/content.json';
import { OBJECTIVES, blockOf } from './constants.js';

function kindOf(q) {
  if (q.code) return 'code';
  const codeish = q.options.filter((o) => /`/.test(o) || o.includes('\n')).length;
  return codeish >= Math.ceil(q.options.length / 2) ? 'code' : 'concept';
}

export const QUESTIONS = content.questions.map((q) => ({
  ...q,
  block: blockOf(q.objective),
  kind: q.kind ?? kindOf(q),
}));

export const QUESTION_BY_ID = new Map(QUESTIONS.map((q) => [q.id, q]));

export const ESSENTIALS = new Map(content.essentials.map((e) => [e.objective, e]));

export const MAPS = content.maps;
export const MAP_BY_ID = new Map(MAPS.map((m) => [m.id, m]));

export const SYNTAX_CARDS = content.syntaxCards;

export const GUIDE_DOCS = [
  { slug: 'overview', markdown: content.guide.overview },
  { slug: 'b1', markdown: content.guide.b1, block: 1 },
  { slug: 'b2', markdown: content.guide.b2, block: 2 },
  { slug: 'b3', markdown: content.guide.b3, block: 3 },
  { slug: 'b4', markdown: content.guide.b4, block: 4 },
  { slug: 'b5', markdown: content.guide.b5, block: 5 },
  { slug: 'glossary', markdown: content.guide.glossary },
  { slug: 'cheat-sheet', markdown: content.guide.cheat },
].map((d) => ({ ...d, title: (d.markdown.match(/^#\s+(.+)$/m) || [, d.slug])[1].trim() }));

export function guideHref(objective) {
  return `#/guide/b${blockOf(objective)}/${objective.replaceAll('.', '-')}`;
}

// Language for multi-line options: printed output stays plain; queries get SQL colouring.
export function optionLang(q) {
  return q.optlang ?? (q.lang === 'sql' ? 'sql' : 'python');
}

export function objectiveTitle(objective) {
  return OBJECTIVES[objective] ?? objective;
}
