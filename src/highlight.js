// A small tokenizer for the two languages the exam uses. Output is escaped HTML with
// <span class="tk-..."> wrappers; anything unrecognized passes through as plain text.

const PY_KEYWORDS = new Set(
  'False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case'.split(' '),
);
const PY_BUILTINS = new Set(
  'print len range int float str bool list dict set tuple type isinstance sum min max abs round sorted enumerate zip map filter open super object Exception ValueError TypeError KeyError IndexError ZeroDivisionError AttributeError NameError FileNotFoundError ImportError ModuleNotFoundError StopIteration id any all repr hash iter next reversed self cls'.split(' '),
);
const SQL_KEYWORDS = new Set(
  'select from where join inner left right full outer cross on group by having order limit offset as and or not in is null like between distinct insert into values update set delete create table drop alter add primary key foreign references integer int text real blob varchar char numeric boolean date default unique union all asc desc count sum avg min max case when then else end exists if'.split(' '),
);

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const span = (cls, s) => `<span class="tk-${cls}">${esc(s)}</span>`;

const PY_RE =
  /(#[^\n]*)|([rbfuRBFU]{0,2}"""[\s\S]*?"""|[rbfuRBFU]{0,2}'''[\s\S]*?'''|[rbfuRBFU]{0,2}"(?:\\.|[^"\\\n])*"|[rbfuRBFU]{0,2}'(?:\\.|[^'\\\n])*')|(@[A-Za-z_][\w.]*)|(\b\d[\d_]*(?:\.\d+)?(?:e[+-]?\d+)?j?\b)|([A-Za-z_]\w*)/g;

const SQL_RE = /(--[^\n]*)|('(?:''|[^'])*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\?|:[A-Za-z_]\w*|%s)/g;

function highlightPython(code) {
  let out = '';
  let last = 0;
  let prevWord = '';
  for (const m of code.matchAll(PY_RE)) {
    out += esc(code.slice(last, m.index));
    last = m.index + m[0].length;
    const [tok, comment, str, deco, num, word] = m;
    if (comment) out += span('comment', tok);
    else if (str) out += span('string', tok);
    else if (deco) out += span('deco', tok);
    else if (num) out += span('number', tok);
    else if (word) {
      const after = code.slice(last).match(/^\s*\(/);
      if (PY_KEYWORDS.has(word)) out += span('keyword', word);
      else if (prevWord === 'def' || prevWord === 'class') out += span('def', word);
      else if (PY_BUILTINS.has(word)) out += span('builtin', word);
      else if (after) out += span('call', word);
      else out += esc(word);
      prevWord = word;
      continue;
    }
    prevWord = '';
  }
  return out + esc(code.slice(last));
}

function highlightSql(code) {
  let out = '';
  let last = 0;
  for (const m of code.matchAll(SQL_RE)) {
    out += esc(code.slice(last, m.index));
    last = m.index + m[0].length;
    const [tok, comment, str, num, word, param] = m;
    if (comment) out += span('comment', tok);
    else if (str) out += span('string', tok);
    else if (num) out += span('number', tok);
    else if (word) out += SQL_KEYWORDS.has(word.toLowerCase()) ? span('keyword', word) : esc(word);
    else if (param) out += span('deco', tok);
  }
  return out + esc(code.slice(last));
}

export function highlight(code, lang) {
  const l = (lang || '').toLowerCase();
  if (l === 'sql') return highlightSql(code);
  if (l === 'python' || l === 'py' || l === '') return highlightPython(code);
  return esc(code);
}

export { esc as escapeHtml };
