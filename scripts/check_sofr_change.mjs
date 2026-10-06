// Explicit bindings to retained SOFR measures and authored house limits.
// This checks data relationships, not the meaning or fulfillment of a report.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const bytes = readFileSync(new URL('../examples/sofr-curve/inputs/results.json', import.meta.url));
const source = JSON.parse(bytes);
const criteria = [
  { name: 'repricing', limit: 0.000001, field: method => ['repricing_max_abs_error_bp', method] },
  { name: 'daily-forward-move', limit: 2, field: method => ['forward_smoothness', method, 'max_jump_bp'] },
  { name: 'off-window-locality', limit: 1, field: method => ['locality_bump_5Y_plus_1bp', method, 'max_change_outside_4Y_6Y_bp'] },
];
function review(data, mode) {
  assert.ok(['shape', 'shape-and-locality'].includes(mode), 'unknown requirement selection');
  const selected = mode === 'shape' ? criteria.slice(0, 2) : criteria;
  return Object.fromEntries(['A', 'B'].map(method => {
    const findings = selected.map(criterion => {
      const path = criterion.field(method);
      const value = path.reduce((node, key) => node?.[key], data);
      const finding = !Number.isFinite(value) || value < 0 ? 'unresolved' : value <= criterion.limit ? 'met' : 'not met';
      return { criterion: criterion.name, field: path.join('.'), value: value ?? null, unit: 'bp', limit: criterion.limit, finding };
    });
    return [method, { findings, overall: findings.some(row => row.finding === 'not met') ? 'not met' : findings.some(row => row.finding === 'unresolved') ? 'unresolved' : 'met' }];
  }));
}
assert.equal(source.as_of, '2026-09-18');
const shape = review(source, 'shape');
const locality = review(source, 'shape-and-locality');
assert.equal(shape.A.overall, 'not met');
assert.equal(shape.B.overall, 'met');
assert.equal(locality.A.overall, 'not met');
assert.equal(locality.B.overall, 'not met');
assert.equal(locality.A.findings[2].finding, 'met');
assert.equal(locality.B.findings[2].finding, 'not met');
assert.equal(shape.B.findings.length, 2, 'unselected locality must not become an acceptance criterion');
const missing = structuredClone(source);
delete missing.locality_bump_5Y_plus_1bp;
assert.equal(review(missing, 'shape').B.overall, 'met');
assert.equal(review(missing, 'shape-and-locality').B.overall, 'unresolved');
const missingAndBreached = structuredClone(missing);
missingAndBreached.forward_smoothness.B.max_jump_bp = 3;
assert.equal(review(missingAndBreached, 'shape-and-locality').B.overall, 'not met', 'known breach must remain adverse despite another gap');
const equality = structuredClone(source);
equality.forward_smoothness.B.max_jump_bp = 2;
equality.locality_bump_5Y_plus_1bp.B.max_change_outside_4Y_6Y_bp = 1;
assert.equal(review(equality, 'shape-and-locality').B.overall, 'met');
const wrongMeasure = structuredClone(source);
wrongMeasure.forward_smoothness.B.max_jump_bp = source.forward_smoothness.B.max_change_over_5_business_days_bp;
assert.equal(review(wrongMeasure, 'shape').B.overall, 'not met', 'five-day and daily values differ materially');
assert.throws(() => review(source, 'unknown'), /unknown requirement selection/);
console.log(JSON.stringify({ sourceSha256: createHash('sha256').update(bytes).digest('hex'), shape, 'shape-and-locality': locality, mutationControls: 'passed', scope: 'Retained numerical evidence and illustrative limits only; no model rerun or report evaluation.' }, null, 2));
