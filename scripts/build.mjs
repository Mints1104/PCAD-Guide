// Validate content, bundle the app, and write dist/index.html (one self-contained page).
import { build } from 'esbuild';
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { OBJECTIVES, OBJECTIVE_IDS, blockOf } from '../src/constants.js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(join(root, p), 'utf8');
const readJson = (p) => JSON.parse(read(p));
const errors = [];
const warnings = [];
const err = (m) => errors.push(m);
const warn = (m) => warnings.push(m);

// ---------- load ----------
const guide = {
  overview: read('content/guide/overview.md'),
  b1: read('content/guide/block1.md'),
  b2: read('content/guide/block2.md'),
  b3: read('content/guide/block3.md'),
  b4: read('content/guide/block4.md'),
  b5: read('content/guide/block5.md'),
  glossary: read('content/guide/glossary.md'),
  cheat: read('content/guide/cheat-sheet.md'),
};

const questionFiles = readdirSync(join(root, 'content/questions')).filter((f) => f.endsWith('.json')).sort();
const questions = questionFiles.flatMap((f) => readJson(`content/questions/${f}`).map((q) => ({ ...q, _file: f })));
const essentials = readdirSync(join(root, 'content/essentials'))
  .filter((f) => f.endsWith('.json'))
  .sort()
  .flatMap((f) => readJson(`content/essentials/${f}`));
const maps = readJson('content/maps/maps.json');
const syntaxCards = readJson('content/cards/syntax.json');

// ---------- glossary terms ----------
const glossaryTerms = new Set();
for (const line of guide.glossary.split('\n')) {
  const m = line.match(/^\*\*(.+?)\*\*/);
  if (m) glossaryTerms.add(m[1].trim().toLowerCase());
}

// ---------- guide coverage ----------
for (const b of [1, 2, 3, 4, 5]) {
  const md = guide[`b${b}`];
  const found = [...md.matchAll(/^##\s+(\d\.\d\.\d)\s+/gm)].map((m) => m[1]);
  for (const o of OBJECTIVE_IDS.filter((o) => blockOf(o) === b)) if (!found.includes(o)) err(`guide block${b}.md is missing "## ${o}"`);
  for (const o of found) if (!OBJECTIVES[o] || blockOf(o) !== b) err(`guide block${b}.md has unknown objective ${o}`);
}

// ---------- maps ----------
const mapIds = new Set();
for (const m of maps) {
  if (mapIds.has(m.id)) err(`duplicate map id ${m.id}`);
  mapIds.add(m.id);
  for (const o of m.objectives) if (!OBJECTIVES[o]) err(`map ${m.id}: unknown objective ${o}`);
  if (!m.nodes[m.start]) err(`map ${m.id}: start node ${m.start} missing`);
  const reached = new Set();
  const stack = [m.start];
  while (stack.length) {
    const id = stack.pop();
    if (reached.has(id)) continue;
    reached.add(id);
    const node = m.nodes[id];
    if (!node) {
      if (!m.leaves[id]) err(`map ${m.id}: "${id}" is neither a node nor a leaf`);
      continue;
    }
    for (const opt of node.options) stack.push(opt.next);
  }
  for (const k of [...Object.keys(m.nodes), ...Object.keys(m.leaves)]) if (!reached.has(k)) warn(`map ${m.id}: "${k}" is unreachable`);
  for (const [k, leaf] of Object.entries(m.leaves)) if (!OBJECTIVES[leaf.objective]) err(`map ${m.id} leaf ${k}: unknown objective ${leaf.objective}`);
}

// ---------- essentials ----------
const essentialIds = new Set();
for (const e of essentials) {
  if (!OBJECTIVES[e.objective]) err(`essentials: unknown objective ${e.objective}`);
  if (essentialIds.has(e.objective)) err(`essentials: duplicate ${e.objective}`);
  essentialIds.add(e.objective);
  if (!e.oneLine) err(`essentials ${e.objective}: missing oneLine`);
  if (!Array.isArray(e.know) || e.know.length < 3) err(`essentials ${e.objective}: needs at least 3 know items`);
  for (const k of e.know ?? []) if (!k.cue || !k.fact || !k.why) err(`essentials ${e.objective}: know item missing cue/fact/why`);
  for (const t of e.traps ?? []) if (!t.cue || !t.answer) err(`essentials ${e.objective}: trap missing cue/answer`);
  for (const m of e.maps ?? []) if (!mapIds.has(m)) err(`essentials ${e.objective}: unknown map ${m}`);
  for (const t of e.terms ?? []) if (!glossaryTerms.has(t.toLowerCase())) warn(`essentials ${e.objective}: term "${t}" not in glossary`);
}
for (const o of OBJECTIVE_IDS) if (!essentialIds.has(o)) err(`essentials: missing ${o}`);

// ---------- syntax cards ----------
const cardIds = new Set();
for (const c of syntaxCards) {
  if (!c.id || !c.front || !c.back) err(`syntax card missing id/front/back: ${JSON.stringify(c).slice(0, 80)}`);
  if (cardIds.has(c.id)) err(`duplicate syntax card ${c.id}`);
  cardIds.add(c.id);
  if (c.objective && !OBJECTIVES[c.objective]) err(`syntax card ${c.id}: unknown objective ${c.objective}`);
}

// ---------- questions ----------
const ids = new Set();
const COUNT_WORDS = { 2: 'two', 3: 'three', 4: 'four' };
for (const q of questions) {
  const where = `${q._file} ${q.id ?? '(no id)'}`;
  for (const f of ['id', 'objective', 'type', 'stem', 'options', 'answer', 'explanation', 'why_wrong', 'source', 'difficulty', 'tags']) if (q[f] === undefined) err(`${where}: missing ${f}`);
  if (ids.has(q.id)) err(`${where}: duplicate id`);
  ids.add(q.id);
  if (!OBJECTIVES[q.objective]) err(`${where}: unknown objective ${q.objective}`);
  if (!Array.isArray(q.options) || q.options.length < 3 || q.options.length > 6) err(`${where}: needs 3-6 options`);
  if (!Array.isArray(q.answer) || q.answer.length === 0) err(`${where}: empty answer`);
  for (const a of q.answer ?? []) if (!(a >= 0 && a < (q.options?.length ?? 0))) err(`${where}: answer index ${a} out of range`);
  if (new Set(q.answer).size !== q.answer?.length) err(`${where}: repeated answer index`);
  if (q.type === 'single' && q.answer?.length !== 1) err(`${where}: single-select needs exactly one answer`);
  if (q.type === 'multi') {
    if (q.answer?.length < 2) err(`${where}: multi-select needs two or more answers`);
    const word = COUNT_WORDS[q.answer?.length];
    if (!new RegExp(`select ${word}`, 'i').test(q.stem)) err(`${where}: multi-select stem must say "Select ${word}"`);
  }
  if (q.type !== 'single' && q.type !== 'multi') err(`${where}: bad type ${q.type}`);
  if (![1, 2, 3].includes(q.difficulty)) err(`${where}: difficulty must be 1-3`);
  if (!Array.isArray(q.why_wrong) || q.why_wrong.length !== q.options?.length) err(`${where}: why_wrong must match options length`);
  else
    q.why_wrong.forEach((w, i) => {
      const right = q.answer.includes(i);
      if (right && w !== '') err(`${where}: why_wrong[${i}] should be empty for a correct option`);
      if (!right && !w) err(`${where}: why_wrong[${i}] missing for a wrong option`);
    });
  if (new Set(q.options?.map((o) => o.trim())).size !== q.options?.length) err(`${where}: duplicate options`);
  if (q.lang && !['python', 'sql', 'text'].includes(q.lang)) err(`${where}: lang must be python, sql or text`);
}

// ---------- report ----------
if (warnings.length) console.warn(`${warnings.length} warning(s):\n  ${warnings.join('\n  ')}`);
if (errors.length) {
  console.error(`${errors.length} error(s):\n  ${errors.join('\n  ')}`);
  process.exit(1);
}

const perBlock = {};
const perObjective = {};
for (const q of questions) {
  const b = blockOf(q.objective);
  perBlock[b] = (perBlock[b] ?? 0) + 1;
  perObjective[q.objective] = (perObjective[q.objective] ?? 0) + 1;
}
const thin = OBJECTIVE_IDS.filter((o) => (perObjective[o] ?? 0) < 3);
console.log(`questions: ${questions.length}  by block: ${JSON.stringify(perBlock)}`);
console.log(`multi: ${questions.filter((q) => q.type === 'multi').length}  with code: ${questions.filter((q) => q.code).length}  difficulty: ${JSON.stringify(questions.reduce((a, q) => ((a[q.difficulty] = (a[q.difficulty] ?? 0) + 1), a), {}))}`);
if (thin.length) console.log(`objectives with fewer than 3 questions: ${thin.map((o) => `${o}(${perObjective[o] ?? 0})`).join(' ')}`);

// ---------- write content + bundle ----------
const shipped = questions.map(({ _file, verify, setup, ...q }) => q);
mkdirSync(join(root, '.build'), { recursive: true });
writeFileSync(join(root, '.build/content.json'), JSON.stringify({ questions: shipped, essentials, maps, syntaxCards, guide }));

const result = await build({
  entryPoints: [join(root, 'src/main.jsx')],
  bundle: true,
  minify: true,
  format: 'iife',
  target: ['es2020'],
  jsx: 'automatic',
  jsxImportSource: 'preact',
  write: false,
  legalComments: 'none',
});
const js = result.outputFiles[0].text.replace(/<\/script/gi, '<\\/script').replace(/<!--/g, '<\\!--');
const css = read('src/styles.css');

const head = `<title>PCAD Prep</title>
<meta name="description" content="Practice tests, mock exams and a revision guide for the Python Institute PCAD-31-02 Certified Associate Data Analyst with Python exam.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap">
<style>
${css}
</style>`;
const body = `<div id="app"></div>
<script>
${js}
</script>
`;

// dist/index.html is the claude.ai artifact: the artifact host wraps it in its own
// doctype, head (charset, viewport) and body, so it must not carry them itself.
const artifact = `${head}\n${body}`;
// dist/pages/index.html is a complete document for static hosting (GitHub Pages).
const standalone = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
${head}
</head>
<body>
${body}</body>
</html>
`;
mkdirSync(join(root, 'dist/pages'), { recursive: true });
writeFileSync(join(root, 'dist/index.html'), artifact);
writeFileSync(join(root, 'dist/pages/index.html'), standalone);
console.log(`dist/index.html: ${(artifact.length / 1024).toFixed(0)} KB · dist/pages/index.html: ${(standalone.length / 1024).toFixed(0)} KB`);
