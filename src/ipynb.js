// Builds a Jupyter notebook (nbformat 4) from a notebook's content, for offline practice.
import { OBJECTIVES } from './constants.js';

export const LEVEL_NAMES = { 1: 'Warm-up', 2: 'Core', 3: 'Challenge' };

const lines = (text) => {
  const parts = text.split('\n');
  return parts.map((l, i) => (i < parts.length - 1 ? `${l}\n` : l));
};
const markdown = (text) => ({ cell_type: 'markdown', metadata: {}, source: lines(text) });
const code = (text) => ({ cell_type: 'code', execution_count: null, metadata: {}, outputs: [], source: lines(text) });

export function toIpynb(nb) {
  const objectives = nb.objectives.map((o) => `${o} ${OBJECTIVES[o] ?? ''}`.trim()).join(' · ');
  const how = nb.chain
    ? 'Run the cells from top to bottom: each task builds on the ones before it. Write your answer in the code cell under each task, then run the check cell below it. It prints `Task N passed`, or raises an AssertionError that says what is wrong.'
    : 'Run the setup cell first. Write your answer in the code cell under each task, then run the check cell below it. It prints `Task N passed`, or raises an AssertionError that says what is wrong. If a task changes the setup data, run the setup cell again.';
  const cells = [markdown(`# ${nb.title}\n\n**Level:** ${LEVEL_NAMES[nb.level]} · **Syllabus:** ${objectives}\n\n${nb.intro}\n\n${how}`), code(nb.setup)];
  nb.tasks.forEach((t, i) => {
    const n = i + 1;
    const hints = t.hints.map((h, j) => `<details><summary>Hint ${j + 1}</summary>\n\n${h}\n\n</details>`).join('\n\n');
    cells.push(markdown(`## Task ${n}: ${t.title}\n\n${t.prompt}${hints ? `\n\n${hints}` : ''}`));
    cells.push(code(t.starter));
    cells.push(code(`# Check for task ${n}\n${t.check}\nprint("Task ${n} passed")`));
  });
  const solutions = nb.tasks.map((t, i) => `<details><summary>Task ${i + 1}: ${t.title}</summary>\n\n\`\`\`python\n${t.solution}\n\`\`\`\n\n</details>`);
  cells.push(markdown(`## Solutions\n\n${solutions.join('\n\n')}`));
  return {
    cells,
    metadata: {
      kernelspec: { display_name: 'Python 3', language: 'python', name: 'python3' },
      language_info: { name: 'python' },
    },
    nbformat: 4,
    nbformat_minor: 4,
  };
}

export function downloadIpynb(nb) {
  const blob = new Blob([JSON.stringify(toIpynb(nb), null, 1)], { type: 'application/x-ipynb+json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `pcad-${nb.id}.ipynb`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
