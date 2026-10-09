// Synthetic fixture accounting under explicit house rules; not a prose evaluator.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const load = name => JSON.parse(readFileSync(new URL(`../examples/vendor-inventory-review/inputs/${name}.json`, import.meta.url)));
const identityFields = ['product', 'version', 'configuration', 'use'];
const registerFields = ['model', ...identityFields, 'owner'];
const expectedCases = ['C1', 'C2', 'C3'];
const day = text => {
  if (typeof text !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(text)) return NaN;
  const value = Date.parse(`${text}T00:00:00Z`);
  return Number.isFinite(value) && new Date(value).toISOString().slice(0, 10) === text ? value / 86400000 : NaN;
};
function inspect(packet) {
  const included = packet.deployments.filter(row => row.environment === 'production');
  const excluded = packet.deployments.filter(row => row.environment !== 'production');
  assert.equal(new Set(packet.deployments.map(row => row.id)).size, packet.deployments.length, 'ambiguous deployment population');
  const rows = included.map(deployment => {
    const relatedRegister = packet.register.filter(row => row.deployment === deployment.id);
    const active = relatedRegister.filter(row => row.state === 'active');
    const differences = active.length === 1 ? registerFields.filter(key => active[0][key] !== deployment[key]) : [];
    const registerFinding = active.length !== 1 ? (active.length ? 'ambiguous' : 'missing') : differences.length ? 'conflicting' : 'matched';
    const relatedTests = packet.localTests.filter(test => test.deployment === deployment.id);
    const exact = relatedTests.filter(test => identityFields.every(key => test[key] === deployment[key]) && test.comparison === 'reference-price-difference-bp');
    let localFinding = 'unresolved', reason = 'no exact test', observations = [], ageDays = null;
    if (exact.length > 1) reason = 'multiple exact tests';
    if (exact.length === 1) {
      const test = exact[0];
      ageDays = day(packet.asOf) - day(test.date);
      if (!Number.isFinite(ageDays) || ageDays < 0 || ageDays > 90) reason = 'test date outside policy';
      else {
        observations = expectedCases.map(id => {
          const matches = test.observations.filter(row => row.case === id);
          if (matches.length !== 1 || !Number.isFinite(matches[0].differenceBp)) return { id, finding: 'unresolved' };
          return { id, finding: Math.abs(matches[0].differenceBp) <= 0.5 ? 'met' : 'not met', valueBp: matches[0].differenceBp };
        });
        localFinding = observations.some(row => row.finding === 'not met') ? 'not met' : observations.some(row => row.finding === 'unresolved') ? 'unresolved' : 'met';
        reason = 'case findings';
      }
    }
    return { deployment: deployment.id, registerFinding, relatedRegister: relatedRegister.map(row => row.record), differences,
      vendorRecords: packet.vendorDocuments.filter(record => record.product === deployment.product && record.version === deployment.version).map(record => record.id),
      localFinding, reason, producerConflict: exact.length === 1 && exact[0].producerFinding === 'within limit' && localFinding === 'not met', relatedTests: relatedTests.map(test => test.id), exactTests: exact.map(test => test.id), ageDays, observations,
      unexpectedObservations: exact.flatMap(test => test.observations.filter(row => !expectedCases.includes(row.case)).map(row => ({ test: test.id, case: row.case }))),
    };
  });
  return { included: included.map(row => row.id), excluded: excluded.map(row => row.id), rows,
    unmatchedRegister: packet.register.filter(row => !packet.deployments.some(deployment => deployment.id === row.deployment)).map(row => ({ record: row.record, deployment: row.deployment, state: row.state, retirement: packet.retirements.filter(event => event.deployment === row.deployment) })),
    excludedRegister: packet.register.filter(row => excluded.some(deployment => deployment.id === row.deployment)).map(row => row.record),
    localCounts: rows.reduce((counts, row) => ({ ...counts, [row.localFinding]: (counts[row.localFinding] ?? 0) + 1 }), {}),
  };
}
const complete = load('complete'), cases = Object.fromEntries(['complete', 'missing', 'contradictory'].map(name => [name, inspect(load(name))]));
assert.deepEqual(cases.complete.included, ['D1', 'D2', 'D3']);
assert.deepEqual(cases.complete.excluded, ['D4']);
assert.deepEqual(cases.complete.rows.map(row => row.registerFinding), ['matched', 'conflicting', 'missing']);
assert.deepEqual(cases.complete.rows[1].differences, ['version', 'configuration']);
assert.deepEqual(cases.complete.localCounts, { met: 1, unresolved: 1, 'not met': 1 });
assert.deepEqual(cases.missing.localCounts, { unresolved: 2, 'not met': 1 });
assert.equal(cases.contradictory.rows[0].registerFinding, 'ambiguous');
assert.equal(cases.contradictory.rows[0].localFinding, 'met', 'separate local support survives a register conflict');
assert.equal(cases.complete.rows[2].producerConflict, true);
assert.equal(cases.complete.unmatchedRegister[0].retirement[0].id, 'X1');
const clone = () => structuredClone(complete);
const boundary = clone(); boundary.localTests[0].observations[2].differenceBp = -0.5;
assert.equal(inspect(boundary).rows[0].localFinding, 'met');
const absentAndAdverse = clone(); absentAndAdverse.localTests[2].observations.shift();
assert.equal(inspect(absentAndAdverse).rows[2].localFinding, 'not met', 'known violation remains adverse despite a gap');
for (const [date, finding] of [['2026-07-03', 'met'], ['2026-07-02', 'unresolved'], ['2026-10-01', 'met'], ['2026-10-02', 'unresolved'], ['2026-02-30', 'unresolved']]) {
  const changed = clone(); changed.localTests[0].date = date;
  assert.equal(inspect(changed).rows[0].localFinding, finding, date);
}
const duplicateCase = clone(); duplicateCase.localTests[0].observations.push({ ...duplicateCase.localTests[0].observations[0] });
assert.equal(inspect(duplicateCase).rows[0].localFinding, 'unresolved');
const duplicateTest = clone(); duplicateTest.localTests.push({ ...duplicateTest.localTests[0], id: 'T1b' });
assert.equal(inspect(duplicateTest).rows[0].reason, 'multiple exact tests');
const sameName = clone(); sameName.localTests[0].configuration = 'other';
assert.equal(inspect(sameName).rows[0].localFinding, 'unresolved');
const nan = clone(); nan.localTests[0].observations[0].differenceBp = null;
assert.equal(inspect(nan).rows[0].localFinding, 'unresolved');
const unexpected = clone(); unexpected.localTests[0].observations.push({ case: 'C4', differenceBp: 0 });
assert.deepEqual(inspect(unexpected).rows[0].unexpectedObservations, [{ test: 'T1', case: 'C4' }]);
const duplicatePopulation = clone(); duplicatePopulation.deployments.push({ ...duplicatePopulation.deployments[0] });
assert.throws(() => inspect(duplicatePopulation), /ambiguous deployment population/);
console.log(JSON.stringify({ cases, mutationControls: 'passed', scope: 'Synthetic identity, coverage, date and value checks only; no contract evaluation, model execution or vendor verification.' }, null, 2));
