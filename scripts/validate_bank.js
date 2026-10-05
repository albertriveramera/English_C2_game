// scripts/validate_bank.js
// Node.js script to validate all C2 question banks

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const context = {
  window: {}
};
vm.createContext(context);

const dataFiles = [
  'vocabulary.js',
  'collocations.js',
  'phrasal.js',
  'cloze.js',
  'grammar.js',
  'confusables.js'
];

let totalQuestions = 0;
const seenIds = new Set();
const errors = [];

dataFiles.forEach(file => {
  const filePath = path.join(__dirname, '..', 'data', file);
  try {
    const code = fs.readFileSync(filePath, 'utf8');
    vm.runInContext(code, context);
  } catch (err) {
    errors.push(`Error executing ${file}: ${err.message}`);
  }
});

const bank = context.window.C2_DATA || {};

Object.entries(bank).forEach(([category, questions]) => {
  if (!Array.isArray(questions)) {
    errors.push(`Category ${category} is not an array.`);
    return;
  }
  console.log(`Checking category [${category}]: ${questions.length} items`);
  questions.forEach((q, idx) => {
    totalQuestions++;
    if (!q.id) errors.push(`[${category}#${idx}] Missing 'id'`);
    else if (seenIds.has(q.id)) errors.push(`Duplicate ID: ${q.id}`);
    else seenIds.add(q.id);

    if (!q.mode) errors.push(`[${q.id || idx}] Missing 'mode'`);
    if (!q.level || q.level < 1 || q.level > 5) errors.push(`[${q.id || idx}] Invalid level: ${q.level}`);
    if (!q.explain) errors.push(`[${q.id || idx}] Missing 'explain'`);
    if (!q.example) errors.push(`[${q.id || idx}] Missing 'example'`);

    if (q.type === 'choice') {
      if (!Array.isArray(q.options) || q.options.length < 2) {
        errors.push(`[${q.id}] 'options' must be array of at least 2 items`);
      }
      if (typeof q.answer !== 'number' || q.answer < 0 || q.answer >= q.options.length) {
        errors.push(`[${q.id}] 'answer' ${q.answer} out of bounds for options (${q.options ? q.options.length : 0})`);
      }
      if (!q.prompt) errors.push(`[${q.id}] Missing 'prompt'`);
    } else if (q.type === 'transformation') {
      if (!q.leadIn) errors.push(`[${q.id}] Missing 'leadIn'`);
      if (!q.keyWord) errors.push(`[${q.id}] Missing 'keyWord'`);
      if (!Array.isArray(q.accepted) || q.accepted.length === 0) {
        errors.push(`[${q.id}] 'accepted' must be non-empty array`);
      }
    } else {
      errors.push(`[${q.id}] Unknown type: ${q.type}`);
    }
  });
});

console.log(`\n================================`);
console.log(`Total questions checked: ${totalQuestions}`);
console.log(`Unique IDs: ${seenIds.size}`);
if (errors.length > 0) {
  console.error(`FOUND ${errors.length} ERROR(S):`);
  errors.forEach(e => console.error(' - ' + e));
  process.exit(1);
} else {
  console.log(`ALL QUESTIONS PASSED INTEGRITY VALIDATION!`);
  process.exit(0);
}
