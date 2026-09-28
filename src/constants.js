// Exam facts from pythoninstitute.org/pcad and /pcad-exam-syllabus (PCAD-31-02, checked 28 Sep 2026).
export const EXAM = {
  code: 'PCAD-31-02',
  name: 'Certified Associate Data Analyst with Python',
  items: 48,
  minutes: 60,
  pass: 0.75,
};

export const BLOCKS = [1, 2, 3, 4, 5];

export const BLOCK_NAMES = {
  1: 'Data Acquisition and Pre-Processing',
  2: 'Programming and Database Skills',
  3: 'Statistical Analysis',
  4: 'Data Analysis and Modeling',
  5: 'Data Communication and Visualization',
};

// Items per block on the real exam; weights are items / 48.
export const BLOCK_ITEMS = { 1: 14, 2: 16, 3: 4, 4: 9, 5: 5 };
export const BLOCK_WEIGHTS = Object.fromEntries(BLOCKS.map((b) => [b, BLOCK_ITEMS[b] / 48]));

export const AREAS = {
  '1.1': 'Data Collection, Integration, and Storage',
  '1.2': 'Data Cleaning and Standardization',
  '1.3': 'Data Validation and Integrity',
  '1.4': 'Data Preparation Techniques',
  '2.1': 'Core Python Proficiency',
  '2.2': 'Module Management and Exception Handling',
  '2.3': 'Object-Oriented Programming for Data Modeling',
  '2.4': 'SQL for Data Analysts',
  '3.1': 'Descriptive Statistics',
  '3.2': 'Inferential Statistics',
  '4.1': 'Data Analysis with Pandas and NumPy',
  '4.2': 'Statistical Methods and Machine Learning',
  '5.1': 'Data Visualization Techniques',
  '5.2': 'Effective Communication of Data Insights',
};

export const OBJECTIVES = {
  '1.1.1': 'Compare data collection methods',
  '1.1.2': 'Aggregate data from diverse sources',
  '1.1.3': 'Explain data storage solutions',
  '1.2.1': 'Structured vs unstructured data',
  '1.2.2': 'Identify and rectify erroneous data',
  '1.2.3': 'Normalization, scaling and encoding',
  '1.2.4': 'Apply cleaning and standardization',
  '1.3.1': 'Basic data validation methods',
  '1.3.2': 'Establish and maintain data integrity',
  '1.4.1': 'File formats in data acquisition',
  '1.4.2': 'Access, manage and organize datasets',
  '1.4.3': 'Extract data from databases, APIs and HTML',
  '1.4.4': 'Spreadsheet best practices',
  '1.4.5': 'Prepare and pre-process data for analysis',
  '2.1.1': 'Syntax, scope and control flow',
  '2.1.2': 'Design and analyze functions',
  '2.1.3': 'The Python data science ecosystem',
  '2.1.4': 'Core data structures',
  '2.1.5': 'PEP 8 and PEP 257',
  '2.2.1': 'Import modules and manage packages',
  '2.2.2': 'Basic exception handling',
  '2.3.1': 'Model data with classes',
  '2.3.2': 'Composition, inheritance and polymorphism',
  '2.3.3': 'Object identity and comparison',
  '2.4.1': 'SQL queries to retrieve data',
  '2.4.2': 'CRUD commands',
  '2.4.3': 'Connect to databases from Python',
  '2.4.4': 'Parameterized queries',
  '2.4.5': 'SQL and Python data types',
  '2.4.6': 'Database security basics',
  '3.1.1': 'Center, spread and distributions',
  '3.1.2': 'Relationships, correlation and outliers',
  '3.2.1': 'Bootstrapping',
  '3.2.2': 'Linear and logistic regression',
  '4.1.1': 'Organize and clean data with pandas',
  '4.1.2': 'Merge and reshape DataFrames',
  '4.1.3': 'Series and DataFrames',
  '4.1.4': '.loc, .iloc and slicing',
  '4.1.5': 'NumPy arrays and broadcasting',
  '4.1.6': 'Group, summarize and cross-tabulate',
  '4.2.1': 'Descriptive statistics in pandas and NumPy',
  '4.2.2': 'Test datasets in model evaluation',
  '4.2.3': 'Supervised learning and the bias-variance trade-off',
  '5.1.1': 'Charts with Matplotlib and Seaborn',
  '5.1.2': 'Choose the right chart',
  '5.1.3': 'Label, annotate and refine charts',
  '5.2.1': 'Tailor communication to the audience',
  '5.2.2': 'Summarize findings with evidence',
};

export const OBJECTIVE_IDS = Object.keys(OBJECTIVES);

export function blockOf(objective) {
  return Number(objective.charAt(0));
}

export function areaOf(objective) {
  return objective.split('.').slice(0, 2).join('.');
}

export const DIFFICULTY_LABELS = { 1: '1 · Recall', 2: '2 · Apply', 3: '3 · Analyze' };

// Difficulty mix used by the mock test and the readiness score.
export const DIFFICULTY_MIX = { 1: 0.2, 2: 0.55, 3: 0.25 };

export const STORAGE_PREFIX = 'pcad-prep';
