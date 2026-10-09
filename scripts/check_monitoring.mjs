// Reference arithmetic for a synthetic packet, not an OpenProse evaluator.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const packet = JSON.parse(readFileSync(new URL('../examples/monitoring-review/inputs/packet.json', import.meta.url)));
const key = row => JSON.stringify([row.model, row.revision, row.metric, row.period]);

// Explicit implementation of this example's authored house thresholds only.
function status(observation, expected) {
  if (observation.unit !== expected.unit || !Number.isFinite(observation.value) || observation.value < 0) return 'unresolved';
  if (expected.metric === 'max_repricing_error' && expected.unit === 'bp') return observation.value <= 1 ? 'within limit' : 'breach';
  if (expected.metric === 'missing_required_inputs' && expected.unit === 'count' && Number.isInteger(observation.value)) return observation.value === 0 ? 'within limit' : 'breach';
  return 'unresolved';
}

function summarize(expected, observations) {
  assert.equal(new Set(expected.map(key)).size, expected.length, 'expected population has ambiguous identities');
  assert.equal(new Set(expected.map(row => row.id)).size, expected.length, 'expected IDs must be unique');
  assert.equal(new Set(observations.map(row => row.id)).size, observations.length, 'source row IDs must be unique');
  const findings = expected.map(row => {
    const matches = observations.filter(observation => key(observation) === key(row));
    const finding = matches.length === 1 ? status(matches[0], row) : 'unresolved';
    return {
      expected: row.id,
      observations: matches.map(observation => observation.id),
      finding,
      reason: matches.length === 0 ? 'missing' : matches.length > 1 ? 'ambiguous duplicate' : finding === 'unresolved' ? 'invalid or unsupported metric' : 'value checked',
      contradictoryLabel: matches.length === 1 && finding !== 'unresolved' && matches[0].producer_status !== finding,
    };
  });
  const counts = Object.fromEntries(['within limit', 'breach', 'unresolved'].map(label => [label, findings.filter(row => row.finding === label).length]));
  const unmatched = observations.filter(row => !expected.some(item => key(item) === key(row))).map(row => row.id);
  return {
    findings, counts, denominator: expected.length, unmatched,
    overall: counts.breach ? 'breach' : counts.unresolved ? 'unresolved' : 'within limit',
  };
}

assert.equal(packet.synthetic, true);
assert.equal(packet.expected_observations.length, 4);
const expectedCounts = {
  complete: [3, 1, 0, 'breach', []],
  missing: [3, 0, 1, 'unresolved', []],
  contradictory: [3, 1, 0, 'breach', ['E3']],
};
const summaries = {};
for (const [name, expected] of Object.entries(expectedCounts)) {
  const result = summarize(packet.expected_observations, packet.cases[name]);
  assert.deepEqual([
    result.counts['within limit'], result.counts.breach, result.counts.unresolved,
    result.overall, result.findings.filter(row => row.contradictoryLabel).map(row => row.expected),
  ], expected, name);
  assert.equal(result.denominator, 4);
  assert.deepEqual(result.unmatched, []);
  summaries[name] = result;
}
assert.deepEqual(summaries.missing.findings.find(row => row.expected === 'E3').observations, []);
assert.equal(summaries.complete.findings[0].finding, 'within limit', 'equality must pass');

const checkMutation = (mutate, inspect) => {
  const rows = structuredClone(packet.cases.complete);
  mutate(rows);
  inspect(summarize(packet.expected_observations, rows));
};
checkMutation(rows => { rows[0].unit = 'percent'; }, result => assert.equal(result.findings[0].finding, 'unresolved'));
checkMutation(rows => { rows[0].revision = 'r2'; }, result => {
  assert.equal(result.findings[0].reason, 'missing');
  assert.deepEqual(result.unmatched, ['O1']);
});
checkMutation(rows => { rows.push({ ...rows[0], id: 'O1-duplicate' }); }, result => {
  assert.equal(result.findings[0].reason, 'ambiguous duplicate');
  assert.deepEqual(result.findings[0].observations, ['O1', 'O1-duplicate']);
  assert.equal(result.denominator, 4);
});
for (const invalid of [null, '0', -1, 0.5]) {
  checkMutation(rows => { rows[1].value = invalid; }, result => assert.equal(result.findings[1].finding, 'unresolved'));
}
checkMutation(rows => { rows[1].value = 1; }, result => assert.equal(result.findings[1].finding, 'breach'));
checkMutation(rows => { rows[2].value = 0.9; rows[2].producer_status = 'within limit'; }, result => {
  assert.equal(result.overall, 'within limit');
  assert.equal(result.counts['within limit'], 4);
});
const unsupported = structuredClone(packet.expected_observations);
unsupported[0].metric = 'unknown_metric';
const unsupportedRows = structuredClone(packet.cases.complete);
unsupportedRows[0].metric = 'unknown_metric';
assert.equal(summarize(unsupported, unsupportedRows).findings[0].finding, 'unresolved');
assert.throws(() => summarize([...packet.expected_observations, packet.expected_observations[0]], packet.cases.complete), /ambiguous identities/);
assert.throws(() => summarize(packet.expected_observations, [...packet.cases.complete, packet.cases.complete[0]]), /source row IDs/);

// These assertions preserve the distinguishing closure facts; they do not
// implement arbitrary institutional issue policies or review authenticity.
assert.equal(packet.issues.length, 1);
assert.equal(packet.issues[0].id, 'I1');
assert.equal(packet.issues[0].producer_status, 'closed');
assert.equal(packet.issues[0].closure_observation, null);
assert.equal(packet.issues[0].review_record, null);
assert.ok(packet.issues[0].due < packet.review_date);

console.log(JSON.stringify({ cases: summaries, mutationControls: 'passed', scope: 'Synthetic data mappings only; no model execution or prose evaluation.' }, null, 2));
