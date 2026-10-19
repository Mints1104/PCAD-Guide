// Turn a finished session into Markdown to paste into a chatbot: a tutoring prompt,
// the score breakdown, then each question with the answer given and the right one.
import { BLOCKS, BLOCK_ITEMS, BLOCK_NAMES, EXAM, OBJECTIVES } from './constants.js';
import { isCorrect } from './score.js';
import { formatClock } from './select.js';

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
const DIFFICULTY = { 1: 'easy', 2: 'medium', 3: 'hard' };

function fence(text, lang) {
  const body = text.replace(/^```\w*\n?/, '').replace(/\n?```$/, '');
  return `\`\`\`${lang}\n${body}\n\`\`\``;
}

function cell(v) {
  return v === null ? 'NULL' : String(v).replaceAll('|', '\\|');
}

function tableMd(t) {
  return [
    `Table \`${t.name}\`:`,
    '',
    `| ${t.columns.map(cell).join(' | ')} |`,
    `| ${t.columns.map(() => '---').join(' | ')} |`,
    ...t.rows.map((r) => `| ${r.map(cell).join(' | ')} |`),
  ].join('\n');
}

function optionMd(letter, text, lang) {
  return text.includes('\n') ? `${letter}.\n${fence(text, lang)}` : `${letter}. ${text}`;
}

function letters(list) {
  return list.length ? list.join(', ') : '(not answered)';
}

function questionMd(n, q, sq) {
  const order = sq.optionOrder?.length ? sq.optionOrder : q.options.map((_, i) => i);
  const letterOf = (i) => LETTERS[order.indexOf(i)];
  const optLang = q.optlang ?? (q.lang === 'sql' ? 'sql' : 'python');
  const chosen = order.filter((i) => sq.chosen.includes(i));
  const right = order.filter((i) => q.answer.includes(i));
  const out = [
    `### Question ${n} · ${q.objective} ${OBJECTIVES[q.objective] ?? ''} · ${DIFFICULTY[q.difficulty] ?? ''}`.trimEnd(),
    '',
    q.stem + (q.type === 'multi' ? ` (select ${q.answer.length})` : ''),
  ];
  if (q.tables) out.push('', q.tables.map(tableMd).join('\n\n'));
  if (q.code) out.push('', fence(q.code, q.lang === 'text' ? 'text' : (q.lang ?? 'python')));
  out.push('', ...order.map((i, pos) => optionMd(LETTERS[pos], q.options[i], optLang)));
  const result = isCorrect(q, sq.chosen) ? 'correct' : chosen.length ? 'wrong' : 'not answered';
  out.push('', `**My answer:** ${letters(chosen.map(letterOf))} (${result})`, `**Correct answer:** ${letters(right.map(letterOf))}`);
  if (sq.flagged) out.push('**Flagged:** yes, I was unsure about this one.');
  const notes = chosen.filter((i) => !q.answer.includes(i) && q.why_wrong[i]).map((i) => `- ${letterOf(i)}: ${q.why_wrong[i]}`);
  if (notes.length) out.push('', 'Why my choice is wrong (answer key):', ...notes);
  out.push('', `Answer-key explanation: ${q.explanation}`);
  return out.join('\n');
}

function promptMd({ mockMode, total, wrong, unsure, scope }) {
  const what = mockMode ? `a timed mock exam of ${total} questions` : `a practice session of ${total} questions`;
  const lines = [
    `I am studying for the Python Institute ${EXAM.code} exam (${EXAM.name}). The pass mark is ${Math.round(EXAM.pass * 100)}%. Below are my results from ${what}, with ${scope === 'all' ? 'all my answers' : 'every question I got wrong or flagged as unsure'}: the question, the options as I saw them, my answer, the correct answer, and the answer key's explanation.`,
    '',
    'Please act as my tutor:',
  ];
  if (wrong > 0) {
    lines.push(
      '1. **Diagnose my misconceptions.** Look across all my mistakes and name the underlying ideas I seem to misunderstand, rather than restating each question. Point out patterns (for example, mixing up two similar functions, or misreading what code prints).',
      '2. **Explain each mistake.** For every question I got wrong, say why my answer is wrong and why the correct one is right. Trace code line by line where it helps, and show small runnable examples. Do not just repeat the answer key; explain it so I would get a variation of the question right.',
      '3. **Rank my weak areas.** List the topics I should study first, weighing how badly I did on each against how many exam items its block carries (shown below).',
      '4. **Test me.** Finish with 5 new exam-style multiple-choice questions aimed at my weakest areas. Put the answers and short explanations at the very end so I can try them first.',
    );
  } else {
    lines.push(
      '1. I answered everything correctly, but I flagged the questions below as unsure. Explain the concept behind each one so my right answer stops being a guess.',
      '2. Point out the traps a harder variation of each question could set.',
      '3. Finish with 5 new, harder exam-style multiple-choice questions on these topics. Put the answers at the very end.',
    );
  }
  if (unsure > 0 && wrong > 0) lines.push('', 'Questions marked "Flagged" are ones I was unsure about. If I got a flagged one right, briefly confirm the reasoning so it sticks.');
  lines.push('', 'Keep the explanations concise and practical. Use Python 3, pandas, NumPy, SciPy, scikit-learn, matplotlib, seaborn and SQL as the exam does.');
  return lines.join('\n');
}

// scope: 'mistakes' (wrong, unanswered and flagged questions) or 'all'.
export function tutorPrompt(session, score, byId, scope = 'mistakes') {
  const rows = session.questions.map((sq, i) => ({ n: i + 1, sq, q: byId.get(sq.questionId) })).filter((r) => r.q);
  for (const r of rows) r.ok = isCorrect(r.q, r.sq.chosen);
  const wrong = rows.filter((r) => !r.ok);
  const unsure = rows.filter((r) => r.ok && r.sq.flagged);
  const mockMode = session.mode === 'mock';
  const secs = session.submittedAt === null ? 0 : Math.round((session.submittedAt - session.startedAt - (session.pausedMs ?? 0)) / 1000);

  const out = [promptMd({ mockMode, total: rows.length, wrong: wrong.length, unsure: unsure.length, scope }), '', '---', '', '## My results', ''];
  out.push(
    `- Score: ${Math.round(score.pct)}% (${score.correct} / ${score.total} correct), ${score.passed ? 'above' : 'below'} the ${Math.round(EXAM.pass * 100)}% pass mark`,
    `- Time used: ${formatClock(secs)}${session.timeLimitSec ? ` of ${formatClock(session.timeLimitSec)}` : ''}`,
    `- Wrong or unanswered: ${wrong.length} · Flagged as unsure: ${rows.filter((r) => r.sq.flagged).length}`,
  );
  out.push('', '### By block (exam items per block in brackets)', '', '| Block | Correct | % |', '| --- | --- | --- |');
  for (const b of BLOCKS) {
    const t = score.byBlock[b];
    if (t?.total > 0) out.push(`| ${b}. ${BLOCK_NAMES[b]} (${BLOCK_ITEMS[b]} of ${EXAM.items}) | ${t.correct} / ${t.total} | ${Math.round(t.pct)}% |`);
  }
  const objectives = Object.entries(score.byObjective).sort(([a, x], [b, y]) => x.pct - y.pct || a.localeCompare(b, undefined, { numeric: true }));
  out.push('', '### By objective (weakest first)', '', '| Objective | Correct | % |', '| --- | --- | --- |');
  for (const [o, t] of objectives) out.push(`| ${o} ${OBJECTIVES[o] ?? ''} | ${t.correct} / ${t.total} | ${Math.round(t.pct)}% |`);

  if (scope === 'all') {
    out.push('', '## Every question');
    for (const r of rows) out.push('', questionMd(r.n, r.q, r.sq));
  } else {
    if (wrong.length) {
      out.push('', `## Questions I got wrong (${wrong.length})`);
      for (const r of wrong) out.push('', questionMd(r.n, r.q, r.sq));
    }
    if (unsure.length) {
      out.push('', `## Correct, but I flagged them as unsure (${unsure.length})`);
      for (const r of unsure) out.push('', questionMd(r.n, r.q, r.sq));
    }
  }
  return out.join('\n').trimEnd() + '\n';
}
