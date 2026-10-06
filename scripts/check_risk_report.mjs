// Arithmetic and population controls for authored risk-report fixtures only.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const load = name => JSON.parse(readFileSync(new URL(`../examples/risk-report/inputs/${name}.json`, import.meta.url)));
const positions = ['P1', 'P2'];
const shocks = { rates: [100, 0], spreads: [0, 100], joint: [100, 100] };
const pick = (rows, key, value) => { const matches = rows.filter(row => row[key] === value); return matches.length === 1 ? matches[0] : null; };
const total = values => values.every(Number.isFinite) ? values.reduce((a, b) => a + b, 0) : null;
function inspect(packet) {
  const fixedBook = ['tradesUsd', 'cashFlowsUsd', 'feesUsd', 'adjustmentsUsd'].every(key => packet[key] === 0);
  const marks = positions.map(id => pick(packet.positions, 'id', id));
  const opening = total(marks.map(row => row?.openingUsd)), closing = total(marks.map(row => row?.closingUsd));
  const movement = fixedBook && opening !== null && closing !== null ? closing - opening : null;
  const perPosition = positions.map((id, i) => {
    const sensitivity = pick(packet.pnl.openingSensitivities, 'position', id), carry = pick(packet.pnl.carry, 'position', id);
    const effect = (slope, move) => Number.isFinite(slope) && Number.isFinite(move) ? slope * move : null;
    const components = { rates: effect(sensitivity?.rateUsdPerBp, packet.pnl.rateMoveBp), spreads: effect(sensitivity?.spreadUsdPerBp, packet.pnl.spreadMoveBp), carry: Number.isFinite(carry?.amountUsd) ? carry.amountUsd : null };
    const explained = total(Object.values(components));
    const change = fixedBook && [marks[i]?.closingUsd, marks[i]?.openingUsd].every(Number.isFinite) ? marks[i].closingUsd - marks[i].openingUsd : null;
    return { position: id, movementUsd: change, components, explainedUsd: explained, knownComponentsUsd: Object.values(components).filter(Number.isFinite).reduce((a, b) => a + b, 0), residualUsd: change !== null && explained !== null ? change - explained : null };
  });
  const explained = total(perPosition.map(row => row.explainedUsd));
  const residual = movement !== null && explained !== null ? movement - explained : null;
  const scenarios = Object.entries(shocks).map(([id, shock]) => {
    const scenario = pick(packet.scenarios, 'id', id);
    const compatible = scenario && scenario.base === packet.closing && scenario.portfolioRevision === packet.portfolioRevision && scenario.modelRevision === packet.modelRevision && scenario.currency === packet.currency && scenario.basis === packet.basis && scenario.horizon === 'instantaneous' && scenario.rateMoveBp === shock[0] && scenario.spreadMoveBp === shock[1];
    const effects = positions.map((position, i) => {
      const value = scenario && pick(scenario.values, 'position', position);
      return { position, changeUsd: compatible && Number.isFinite(value?.valueUsd) && Number.isFinite(marks[i]?.closingUsd) ? value.valueUsd - marks[i].closingUsd : null };
    });
    const pnl = total(effects.map(row => row.changeUsd)), hedge = packet.assumedHedge.pnlUsdByScenario[id];
    return { id, compatible: Boolean(compatible), effects, fullBookPnlUsd: pnl, knownSubsetPnlUsd: effects.filter(row => row.changeUsd !== null).reduce((sum, row) => sum + row.changeUsd, 0),
      finding: pnl === null ? 'unresolved' : pnl < -25000 ? 'not met' : 'met',
      conditionalHedgePnlUsd: pnl !== null && Number.isFinite(hedge) ? pnl + hedge : null,
      unexpectedPositions: scenario?.values.filter(row => !positions.includes(row.position)).map(row => row.position) ?? [],
    };
  });
  const singleSum = total(scenarios.slice(0, 2).map(row => row.fullBookPnlUsd));
  const joint = scenarios[2].fullBookPnlUsd;
  return { openingUsd: opening, closingUsd: closing, movementUsd: movement, perPosition,
    explainedUsd: explained, knownComponentsUsd: perPosition.reduce((sum, row) => sum + row.knownComponentsUsd, 0), residualUsd: residual,
    pnlFinding: residual === null ? 'unresolved' : Math.abs(residual) <= 1000 ? 'met' : 'not met',
    scenarios, singleFactorSumUsd: singleSum, jointDifferenceUsd: joint !== null && singleSum !== null ? joint - singleSum : null,
    scenarioFinding: scenarios.some(row => row.finding === 'not met') ? 'not met' : scenarios.some(row => row.finding === 'unresolved') ? 'unresolved' : 'met',
    unexplainedProducerConflict: explained !== null && packet.pnl.producerExplainedUsd !== explained,
    fullyExplainedProducerConflict: packet.producerSummary.fullyExplained && residual !== null && residual !== 0,
    scenarioProducerConflict: packet.producerSummary.allUnmitigatedScenariosWithinLimit && scenarios.some(row => row.finding === 'not met'),
    hedgeExecutionConflict: packet.producerSummary.hedgeExecuted && packet.assumedHedge.status === 'assumed-only',
    unexpectedPositions: packet.positions.filter(row => !positions.includes(row.id)).map(row => row.id),
    unexpectedScenarios: packet.scenarios.filter(row => !Object.hasOwn(shocks, row.id)).map(row => row.id),
  };
}
const cases = Object.fromEntries(['complete', 'missing', 'contradictory'].map(name => [name, inspect(load(name))]));
assert.equal(cases.complete.movementUsd, 5000);
assert.equal(cases.complete.explainedUsd, 8000);
assert.equal(cases.complete.residualUsd, -3000);
assert.deepEqual(cases.complete.perPosition.map(row => row.residualUsd), [6400, -9400]);
assert.equal(cases.complete.pnlFinding, 'not met');
assert.deepEqual(cases.complete.scenarios.map(row => row.fullBookPnlUsd), [-50000, -20000, -85000]);
assert.deepEqual(cases.complete.scenarios.map(row => row.conditionalHedgePnlUsd), [-10000, -20000, -45000]);
assert.deepEqual(cases.complete.scenarios.map(row => row.finding), ['not met', 'met', 'not met']);
assert.equal(cases.complete.singleFactorSumUsd, -70000);
assert.equal(cases.complete.jointDifferenceUsd, -15000);
assert.equal(cases.missing.explainedUsd, null);
assert.equal(cases.missing.knownComponentsUsd, 7600);
assert.equal(cases.missing.residualUsd, null);
assert.equal(cases.missing.scenarios[2].knownSubsetPnlUsd, -45000);
assert.equal(cases.missing.scenarios[2].fullBookPnlUsd, null);
assert.equal(cases.missing.scenarios[2].finding, 'unresolved');
assert.equal(cases.missing.scenarios[2].conditionalHedgePnlUsd, null);
assert.equal(cases.missing.jointDifferenceUsd, null);
assert.equal(cases.missing.scenarioFinding, 'not met');
for (const field of ['unexplainedProducerConflict', 'fullyExplainedProducerConflict', 'scenarioProducerConflict', 'hedgeExecutionConflict']) assert.equal(cases.contradictory[field], true);
const clone = () => load('complete');
const equality = clone(); equality.pnl.carry[1].amountUsd = -1600;
assert.equal(inspect(equality).residualUsd, -1000); assert.equal(inspect(equality).pnlFinding, 'met');
const scenarioEquality = clone(); scenarioEquality.scenarios[0].values[0].valueUsd = 595000;
assert.equal(inspect(scenarioEquality).scenarios[0].fullBookPnlUsd, -25000); assert.equal(inspect(scenarioEquality).scenarios[0].finding, 'met');
for (const [field, value] of [['base', '2026-09-29T20:00:00Z'], ['currency', 'EUR'], ['basis', 'dirty-value'], ['horizon', 'one-year'], ['modelRevision', 'r0'], ['rateMoveBp', 1]]) {
  const changed = clone(); changed.scenarios[0][field] = value;
  assert.equal(inspect(changed).scenarios[0].finding, 'unresolved', field);
}
const duplicate = clone(); duplicate.scenarios[0].values.push({ ...duplicate.scenarios[0].values[0] });
assert.equal(inspect(duplicate).scenarios[0].finding, 'unresolved');
const duplicateScenario = clone(); duplicateScenario.scenarios.push(structuredClone(duplicateScenario.scenarios[0]));
assert.equal(inspect(duplicateScenario).scenarios[0].finding, 'unresolved');
const duplicateCarry = clone(); duplicateCarry.pnl.carry.push({ ...duplicateCarry.pnl.carry[0] });
assert.equal(inspect(duplicateCarry).pnlFinding, 'unresolved');
const wrongType = clone(); wrongType.pnl.openingSensitivities[0].rateUsdPerBp = false;
assert.equal(inspect(wrongType).pnlFinding, 'unresolved');
const flow = clone(); flow.cashFlowsUsd = 1;
assert.equal(inspect(flow).movementUsd, null, 'fixed-book convention is no longer supported');
const extras = clone(); extras.scenarios.push({ id: 'other', values: [] }); extras.positions.push({ id: 'P3', openingUsd: 1, closingUsd: 1 });
assert.deepEqual(inspect(extras).unexpectedPositions, ['P3']); assert.deepEqual(inspect(extras).unexpectedScenarios, ['other']);
console.log(JSON.stringify({ cases, mutationControls: 'passed', scope: 'Authored fixture arithmetic and identities; no financial-model run, causal attribution, accounting action or prose evaluation.' }, null, 2));
