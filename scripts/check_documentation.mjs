// Fixed source/reference checks; not a methodology-document or citation evaluator.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const root = new URL('../', import.meta.url);
const bytes = path => readFileSync(new URL(path, root));
const text = path => bytes(path).toString('utf8');
const hash = data => createHash('sha256').update(data).digest('hex');
const base = 'examples/sofr-documentation/';
const originalPath = 'examples/sofr-curve/inputs/results.json';
const original = JSON.parse(text(originalPath));
const projection = JSON.parse(text(`${base}inputs/projection.json`));
const missing = JSON.parse(text(`${base}inputs/missing-locality.json`));
assert.equal(projection.original_sha256, hash(bytes(originalPath)));
assert.equal(projection.projected_sha256, hash(bytes(`${base}inputs/missing-locality.json`)));
const expectedMissing = structuredClone(original);
delete expectedMissing.locality_bump_5Y_plus_1bp;
const checkProjection = value => assert.deepEqual(value, expectedMissing, 'only locality observations are withheld');
checkProjection(missing);
const ids = source => [...source.matchAll(/^\| (D\d+) \|/gm)].map(m => m[1]);
const expectedIds = Array.from({ length: 10 }, (_, i) => `D${i + 1}`);
assert.deepEqual(ids(text(`${base}requirements.md`)), expectedIds);
const document = text(`${base}sample-results/document.md`);
const reviews = text(`${base}sample-results/reviews.md`);
const result = text(`${base}sample-results/result.md`);
function checkReference(doc, review) {
  assert.ok(doc.trim().split(/\s+/).length < 1600, 'document size');
  assert.deepEqual(ids(review), expectedIds, 'section-plan population');
  const rows = [...doc.matchAll(/^\| ([^|]+) \| ([^|]+) \| ([^|]+) \|/gm)]
    .map(m => ({ name: m[1].trim(), A: m[2].trim(), B: m[3].trim() }));
  const table = rows.map(row => ({ name: row.name, A: Number(row.A), B: Number(row.B) }));
  const bindings = [
    ['Maximum absolute repricing error, bp', original.repricing_max_abs_error_bp, n => Number(n.toPrecision(6))],
    ['Largest daily forward move, bp', { A: original.forward_smoothness.A.max_jump_bp, B: original.forward_smoothness.B.max_jump_bp }, n => Number(n.toFixed(6))],
    ['Largest five-business-day move, bp', { A: original.forward_smoothness.A.max_change_over_5_business_days_bp, B: original.forward_smoothness.B.max_change_over_5_business_days_bp }, n => Number(n.toFixed(6))],
    ['Largest outside-window response, bp', { A: original.locality_bump_5Y_plus_1bp.A.max_change_outside_4Y_6Y_bp, B: original.locality_bump_5Y_plus_1bp.B.max_change_outside_4Y_6Y_bp }, n => Number(n.toFixed(6))],
  ];
  for (const [name, values, format] of bindings) {
    const candidates = table.filter(row => row.name === name);
    assert.equal(candidates.length, 1, 'comparison row population');
    for (const method of ['A', 'B']) assert.equal(candidates[0][method], format(values[method]), 'comparison value binding');
  }
  for (const [name, field] of [
    ['Daily comparison', 'max_jump_date'],
    ['Five-business-day comparison', 'max_change_over_5_business_days_ending'],
  ]) {
    const candidates = rows.filter(row => row.name === name);
    assert.equal(candidates.length, 1, 'move-date row population');
    for (const method of ['A', 'B']) assert.equal(candidates[0][method], original.forward_smoothness[method][field], 'move-date binding');
  }
  assert.equal((doc.match(/\[INSTITUTION-SUPPLIED:/g) ?? []).length, 3, 'selected institutional-gap count');
}
checkReference(document, reviews);
const identities = [...result.matchAll(/^\| ([^|]+) \| ([a-f0-9]{64}) \|$/gm)].map(m => ({ path: m[1].trim(), sha: m[2] }));
assert.equal(new Set(identities.map(row => row.path)).size, identities.length, 'duplicate reference identity');
assert.equal(identities.length, 21, 'selected artifact/agreement/input population');
for (const row of identities) {
  const path = ['document.md', 'reviews.md'].includes(row.path) ? `${base}sample-results/${row.path}` : row.path;
  assert.equal(hash(bytes(path)), row.sha, `reference identity: ${row.path}`);
}
for (const definition of ['documentation', 'model-description', 'numerical-evidence', 'claim-evidence', 'institutional-facts']) {
  assert.ok(identities.some(row => row.path === `contracts/${definition}.md`), 'adopted definition identity');
}
assert.throws(() => checkReference(document.replace('59.712041', '1.684594'), reviews), /comparison value binding/);
assert.throws(() => checkReference(document.replace('4.147534', '0.030463'), reviews), /comparison value binding/);
assert.throws(() => checkReference(document.replace('| Daily comparison | 2046-09-26 | 2029-09-28 |', '| Daily comparison | 2029-09-28 | 2046-09-26 |'), reviews), /move-date binding/);
assert.throws(() => checkReference(document.replace('| Five-business-day comparison | 2046-09-28 | 2026-12-31 |', '| Five-business-day comparison | 2046-09-26 | 2026-12-31 |'), reviews), /move-date binding/);
assert.throws(() => checkReference(document.replace(/^\| Daily comparison \|.*\n/m, ''), reviews), /move-date row population/);
assert.throws(() => checkReference(document, reviews.replace(/^\| D5 \|.*\n/m, '')), /section-plan population/);
assert.throws(() => checkReference(document, reviews.replace('| D5 |', '| D4 |')), /section-plan population/);
assert.throws(() => checkReference(document.replace('[INSTITUTION-SUPPLIED: accountable model owner]', 'Approved owner'), reviews), /selected institutional-gap count/);
const wrongProjection = structuredClone(missing); wrongProjection.as_of = '2026-09-19';
assert.throws(() => checkProjection(wrongProjection), /only locality observations are withheld/);
console.log(JSON.stringify({ projection: 'matches declared removal', selectedDocumentRequirements: expectedIds,
  numericComparisonRows: 4, moveDateBindings: 4, referenceIdentityCount: identities.length, mutationControls: 'passed',
  scope: 'Fixed identities, numeric correspondences and reference coverage markers; no arbitrary prose, citation-support, contract-fulfillment or execution assessment.' }, null, 2));
