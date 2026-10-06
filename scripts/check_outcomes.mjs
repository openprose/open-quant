// Synthetic outcome pairing and arithmetic; not financial or prose validation.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const load = name => JSON.parse(readFileSync(new URL(`../examples/outcomes-review/inputs/${name}.json`, import.meta.url)));
const time = text => {
  if (typeof text !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(text)) return NaN;
  const value = Date.parse(text);
  return Number.isFinite(value) && new Date(value).toISOString().replace('.000Z', 'Z') === text ? value : NaN;
};
const metric = pairs => ({ ids: pairs.map(row => row.id), count: pairs.length, maeUsd: pairs.length ? pairs.reduce((sum, row) => sum + row.error, 0) / pairs.length : null });
function inspect(packet) {
  assert.equal(new Set(packet.cohort.map(row => row.id)).size, packet.cohort.length, 'ambiguous cohort identity');
  const cutoff = time(packet.cutoff);
  assert.ok(Number.isFinite(cutoff), 'invalid cutoff');
  const rows = packet.cohort.map(item => {
    const start = time(item.windowStart), end = time(item.windowEnd);
    const validWindow = Number.isFinite(start) && Number.isFinite(end) && start < end;
    const mature = validWindow ? end <= cutoff : null;
    const outcomes = packet.outcomes.filter(row => row.observation === item.id);
    const outcome = outcomes.length === 1 ? outcomes[0] : null;
    let outcomeReason = !validWindow ? 'invalid window' : !mature ? 'immature' : !outcome ? 'missing or duplicate outcome' : null;
    if (outcomeReason === null && (outcome.book !== item.book || outcome.currency !== 'USD' || outcome.windowStart !== item.windowStart || outcome.windowEnd !== item.windowEnd || !Number.isFinite(outcome.netFlowUsd))) outcomeReason = 'outcome identity, unit or value';
    if (outcomeReason === null && (!Number.isFinite(time(outcome.available)) || time(outcome.available) < end || time(outcome.available) > cutoff)) outcomeReason = 'outcome availability';
    const models = Object.fromEntries(['A', 'B'].map(model => {
      const candidates = packet.forecasts.filter(row => row.observation === item.id && row.model === model);
      const forecast = candidates.length === 1 ? candidates[0] : null;
      let reason = !forecast ? 'missing or duplicate forecast' : null;
      if (reason === null && (forecast.revision !== 'r1' || forecast.book !== item.book || forecast.currency !== 'USD' || forecast.windowStart !== item.windowStart || forecast.windowEnd !== item.windowEnd || !Number.isFinite(forecast.netFlowUsd))) reason = 'forecast identity, unit or value';
      if (reason === null && (!validWindow || !Number.isFinite(time(forecast.issued)) || time(forecast.issued) >= start || time(forecast.issued) > cutoff)) reason = 'forecast timing';
      return [model, { forecastReason: reason, eligible: reason === null && outcomeReason === null, errorUsd: reason === null && outcomeReason === null ? Math.abs(forecast.netFlowUsd - outcome.netFlowUsd) : null }];
    }));
    return { id: item.id, mature, outcomeReason, models };
  });
  const own = Object.fromEntries(['A', 'B'].map(model => [model, metric(rows.filter(row => row.models[model].eligible).map(row => ({ id: row.id, error: row.models[model].errorUsd })))]));
  const commonRows = rows.filter(row => row.models.A.eligible && row.models.B.eligible);
  const common = Object.fromEntries(['A', 'B'].map(model => [model, metric(commonRows.map(row => ({ id: row.id, error: row.models[model].errorUsd })))]));
  const difference = commonRows.length ? common.B.maeUsd - common.A.maeUsd : null;
  return { expected: rows.length, mature: rows.filter(row => row.mature === true).length, immature: rows.filter(row => row.mature === false).length, rows, own, common,
    bMinusAMaeUsd: difference, relativeReductionAgainstA: common.A.maeUsd > 0 ? (common.A.maeUsd - common.B.maeUsd) / common.A.maeUsd : null,
    coversMatureCohort: rows.every(row => row.mature === false || (row.mature === true && row.models.A.eligible && row.models.B.eligible)),
    unmatchedForecasts: packet.forecasts.filter(row => !packet.cohort.some(item => item.id === row.observation) || !['A', 'B'].includes(row.model)).map(row => row.id),
    unmatchedOutcomes: packet.outcomes.filter(row => !packet.cohort.some(item => item.id === row.observation)).map(row => row.id),
  };
}
const cases = Object.fromEntries(['complete', 'missing', 'late-forecast'].map(name => [name, inspect(load(name))]));
assert.equal(cases.complete.expected, 4); assert.equal(cases.complete.mature, 3); assert.equal(cases.complete.immature, 1);
assert.equal(cases.complete.common.A.maeUsd, 100000 / 3); assert.equal(cases.complete.common.B.maeUsd, 20000 / 3);
assert.ok(Math.abs(cases.complete.relativeReductionAgainstA - 0.8) < 1e-12);
assert.equal(cases.complete.coversMatureCohort, true);
for (const name of ['missing', 'late-forecast']) {
  const row = cases[name];
  assert.deepEqual(row.common.A.ids, ['F1', 'F2']);
  assert.equal(row.own.A.maeUsd, 100000 / 3); assert.equal(row.own.B.maeUsd, 10000);
  assert.ok(row.own.B.maeUsd < row.own.A.maeUsd, 'unequal populations appear to favor B');
  assert.equal(row.common.A.maeUsd, 0); assert.equal(row.common.B.maeUsd, 10000);
  assert.equal(row.bMinusAMaeUsd, 10000); assert.equal(row.relativeReductionAgainstA, null);
  assert.equal(row.coversMatureCohort, false);
}
assert.equal(cases.missing.rows[2].models.B.forecastReason, 'missing or duplicate forecast');
assert.equal(cases['late-forecast'].rows[2].models.B.forecastReason, 'forecast timing');
const clone = () => load('complete');
const exactStart = clone(); exactStart.forecasts.find(row => row.id === 'B3').issued = '2026-09-30T09:00:00Z';
assert.equal(inspect(exactStart).common.B.count, 2);
const atCutoff = clone(); atCutoff.outcomes[2].available = atCutoff.cutoff;
assert.equal(inspect(atCutoff).common.B.count, 3);
const afterCutoff = clone(); afterCutoff.outcomes[2].available = '2026-10-01T18:00:01Z';
assert.equal(inspect(afterCutoff).common.B.count, 2);
const earlyOutcome = clone(); earlyOutcome.outcomes[2].available = '2026-09-30T16:59:59Z';
assert.equal(inspect(earlyOutcome).common.B.count, 2);
const invalidTime = clone(); invalidTime.forecasts[0].issued = '2026-02-30T18:00:00Z';
assert.equal(inspect(invalidTime).own.A.count, 2);
const duplicateForecast = clone(); duplicateForecast.forecasts.push({ ...duplicateForecast.forecasts[0], id: 'A1b' });
assert.equal(inspect(duplicateForecast).own.A.count, 2);
const duplicateOutcome = clone(); duplicateOutcome.outcomes.push({ ...duplicateOutcome.outcomes[0], id: 'O1b' });
assert.equal(inspect(duplicateOutcome).common.A.count, 2);
const wrongCurrency = clone(); wrongCurrency.forecasts[0].currency = 'EUR';
assert.equal(inspect(wrongCurrency).own.A.count, 2);
const badNumber = clone(); badNumber.forecasts[0].netFlowUsd = null;
assert.equal(inspect(badNumber).own.A.count, 2);
const noOutcomes = clone(); noOutcomes.outcomes = [];
assert.equal(inspect(noOutcomes).common.A.maeUsd, null); assert.equal(inspect(noOutcomes).bMinusAMaeUsd, null);
assert.equal(inspect(noOutcomes).coversMatureCohort, false);
const unmatched = clone(); unmatched.outcomes.push({ ...unmatched.outcomes[0], id: 'O9', observation: 'F9' });
assert.deepEqual(inspect(unmatched).unmatchedOutcomes, ['O9']);
const duplicateCohort = clone(); duplicateCohort.cohort.push({ ...duplicateCohort.cohort[0] });
assert.throws(() => inspect(duplicateCohort), /ambiguous cohort identity/);
console.log(JSON.stringify({ cases, mutationControls: 'passed', scope: 'Authored pairing, timing, denominator and metric controls; no predictive validation, significance test or report evaluation.' }, null, 2));
