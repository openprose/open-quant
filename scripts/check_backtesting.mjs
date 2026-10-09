// Explicit arithmetic for authored five-day cases, not a regulatory test engine.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const dates = [21, 22, 23, 24, 25].map(day => `2026-09-${day}`);
const readCase = name => JSON.parse(readFileSync(new URL(`../examples/backtesting-review/inputs/cases/${name}.json`, import.meta.url)));

function summarize(packet) {
  assert.equal(packet.synthetic, true);
  assert.equal(new Set(packet.observations.map(row => row.id)).size, packet.observations.length, 'duplicate source row IDs');
  const findings = dates.map(date => {
    const matches = packet.observations.filter(row => row.date === date);
    let commonReason = matches.length === 0 ? 'missing record' : matches.length > 1 ? 'ambiguous records' : null;
    const row = matches[0];
    if (!commonReason) {
      if (row.model !== 'TOY-VAR' || row.revision !== 'r1' || row.portfolio !== 'DEMO-BOOK' || row.currency !== 'USD') commonReason = 'identity or unit mismatch';
      else if (!Number.isFinite(row.var) || row.var < 0) commonReason = 'invalid or missing forecast';
      else if (typeof row.forecast_time !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(row.forecast_time) || !Number.isFinite(Date.parse(row.forecast_time)) || Date.parse(row.forecast_time) >= Date.parse(`${date}T09:00:00Z`)) commonReason = 'forecast unavailable before start';
    }
    const series = Object.fromEntries(['apl', 'hpl'].map(name => {
      const reason = commonReason ?? (!Number.isFinite(row[name]) ? 'invalid or missing outcome' : null);
      const observedExceedance = reason === null && row[name] < -row.var;
      return [name, { available: reason === null, reason, observedExceedance, policyException: reason !== null || observedExceedance }];
    }));
    return { date, sourceRecords: matches.map(item => item.id), ...series };
  });
  const series = Object.fromEntries(['apl', 'hpl'].map(name => [name, {
    expected: dates.length,
    available: findings.filter(row => row[name].available).length,
    observedExceedances: findings.filter(row => row[name].observedExceedance).length,
    unavailable: findings.filter(row => !row[name].available).length,
    policyExceptions: findings.filter(row => row[name].policyException).length,
  }]));
  const combined = Math.max(series.apl.policyExceptions, series.hpl.policyExceptions);
  const calculated = { apl_exceptions: series.apl.policyExceptions, hpl_exceptions: series.hpl.policyExceptions, combined };
  const summaryContradictions = packet.producer_summary === null ? [] : Object.keys(calculated).filter(key => packet.producer_summary[key] !== calculated[key]);
  return { findings, series, combined, summaryContradictions, unmatchedRecords: packet.observations.filter(row => !dates.includes(row.date)).map(row => row.id) };
}

const expected = {
  complete: { apl: [1, 0, 1], hpl: [1, 0, 1], combined: 1, contradictions: [] },
  missing: { apl: [1, 1, 2], hpl: [1, 0, 1], combined: 2, contradictions: [] },
  contradictory: { apl: [1, 0, 1], hpl: [1, 0, 1], combined: 1, contradictions: ['apl_exceptions', 'hpl_exceptions', 'combined'] },
  'late-forecast': { apl: [0, 1, 1], hpl: [1, 1, 2], combined: 2, contradictions: [] },
};
const results = {};
for (const [name, target] of Object.entries(expected)) {
  const result = summarize(readCase(name));
  for (const series of ['apl', 'hpl']) {
    const counts = result.series[series];
    assert.deepEqual([counts.observedExceedances, counts.unavailable, counts.policyExceptions], target[series], `${name}/${series}`);
    assert.equal(counts.expected, 5);
    assert.equal(counts.available + counts.unavailable, 5);
  }
  assert.equal(result.combined, target.combined);
  assert.deepEqual(result.summaryContradictions, target.contradictions);
  assert.deepEqual(result.unmatchedRecords, []);
  results[name] = result;
}
assert.equal(results.complete.findings[0].apl.observedExceedance, false, 'equality is not an exceedance');
assert.equal(results.complete.findings.filter(row => row.apl.policyException || row.hpl.policyException).length, 2);
assert.equal(results.complete.combined, 1, 'maximum is not the union of dates');

function mutate(change, inspect) {
  const packet = readCase('complete');
  change(packet.observations);
  packet.producer_summary = null;
  inspect(summarize(packet));
}
mutate(rows => { rows.splice(0, 1); }, result => {
  assert.equal(result.findings[0].apl.reason, 'missing record');
  assert.equal(result.findings[0].hpl.policyException, true);
  assert.equal(result.series.apl.expected, 5);
});
mutate(rows => { rows.push({ ...rows[0], id: 'B1-copy' }); }, result => {
  assert.deepEqual(result.findings[0].sourceRecords, ['B1', 'B1-copy']);
  assert.equal(result.findings[0].apl.reason, 'ambiguous records');
});
for (const field of ['apl', 'var']) for (const value of [null, '100']) {
  mutate(rows => { rows[0][field] = value; }, result => {
    assert.equal(result.findings[0].apl.available, false);
    assert.equal(result.findings[0].apl.policyException, true);
    assert.equal(result.findings[0].hpl.available, field !== 'var');
  });
}
mutate(rows => { rows[0].forecast_time = '2026-09-21T09:00:00Z'; }, result => assert.equal(result.findings[0].apl.available, false));
mutate(rows => { rows[0].forecast_time = 'not-a-date'; }, result => assert.equal(result.findings[0].hpl.available, false));
mutate(rows => { rows[0].revision = 'r2'; }, result => assert.equal(result.findings[0].apl.reason, 'identity or unit mismatch'));
mutate(rows => { rows[0].var = -100; }, result => assert.equal(result.findings[0].apl.reason, 'invalid or missing forecast'));
mutate(rows => { rows.push({ ...rows[0], id: 'OUTSIDE', date: '2026-09-28' }); }, result => assert.deepEqual(result.unmatchedRecords, ['OUTSIDE']));
console.log(JSON.stringify({ cases: results, mutationControls: 'passed', scope: 'Authored five-day arithmetic only; no model execution, annual test or prose evaluation.' }, null, 2));
