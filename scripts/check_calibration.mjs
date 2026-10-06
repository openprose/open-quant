// Fixture-specific calculations, not a natural-language evaluator or model run.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const read = path => readFileSync(new URL(`../${path}`, import.meta.url));
function csv(bytes) {
  const [header, ...lines] = bytes.toString().trim().split(/\r?\n/).map(line => line.split(','));
  return lines.map(values => {
    assert.equal(values.length, header.length);
    return Object.fromEntries(header.map((key, i) => [key, values[i]]));
  });
}
function number(value) {
  return typeof value === 'string' && /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/i.test(value) && Number.isFinite(Number(value)) ? Number(value) : NaN;
}
function halfUnit(value) {
  if (!Number.isFinite(number(value))) return NaN;
  // The source uses normalized Python .3e formatting for residuals.
  // Its 0.000e+00 represents a computed zero, not rounding to 0.001 bp.
  if (number(value) === 0 && /^[+-]?0\.000e[+]00$/i.test(value)) return 0;
  const [mantissa, exponent = '0'] = value.toLowerCase().split('e');
  return 0.5 * 10 ** (Number(exponent) - (mantissa.split('.')[1]?.length ?? 0));
}
const quotes = csv(read('examples/sofr-curve/inputs/quotes.csv'));
const fixing = JSON.parse(read('examples/sofr-curve/inputs/sofr-fixing.json')).sofr_percent;
const expected = new Map([['O/N', fixing], ['T/N', fixing], ...quotes.filter(row => row.used_in_bootstrap === 'True').map(row => [row.tenor, number(row.quote_pct)])]);
const excluded = quotes.filter(row => row.used_in_bootstrap === 'False').map(row => row.tenor);
assert.equal(expected.size, 22);
assert.deepEqual(excluded, ['9M', '25Y']);
const limit = 0.000001;
function review(rows) {
  return { unexpected: rows.filter(row => !expected.has(row.instrument)).map(row => row.instrument), ...Object.fromEntries(['A', 'B'].map(method => {
    const findings = [...expected].map(([instrument, target]) => {
      const matches = rows.filter(row => row.instrument === instrument);
      if (matches.length !== 1) return { instrument, finding: 'unresolved', reason: matches.length ? 'duplicate' : 'missing' };
      const row = matches[0], residual = number(row[`error_${method}_bp`]);
      const market = number(row.market_pct), implied = number(row[`implied_${method}_pct`]);
      if (![residual, market, implied].every(Number.isFinite)) return { instrument, finding: 'unresolved', reason: 'nonnumeric' };
      const uncertainty = halfUnit(row[`error_${method}_bp`]);
      const displayBound = (halfUnit(row.market_pct) + halfUnit(row[`implied_${method}_pct`])) * 100 + uncertainty;
      const rateConflict = Math.abs((implied - market) * 100 - residual) > displayBound;
      const targetConflict = Math.abs(market - target) > halfUnit(row.market_pct);
      const reportedBreach = Math.abs(residual) - uncertainty > limit;
      const finding = rateConflict || targetConflict ? 'conflicting' : reportedBreach ? 'not met' : Math.abs(residual) + uncertainty <= limit ? 'met' : 'unresolved';
      return { instrument, residual, reportedBreach, rateConflict, targetConflict, finding };
    });
    const counts = findings.reduce((counts, row) => ({ ...counts, [row.finding]: (counts[row.finding] ?? 0) + 1 }), {});
    return [method, { counts, findings }];
  })) };
}
const cases = {};
for (const [name, file] of [['complete', 'repricing.csv'], ['missing', 'missing.csv'], ['contradictory', 'contradictory.csv']]) {
  const bytes = read(`examples/calibration-review/inputs/${file}`);
  cases[name] = { sha256: createHash('sha256').update(bytes).digest('hex'), ...review(csv(bytes)) };
}
const receipt = JSON.parse(read('provenance/reproduction/2026-10-06.json'));
assert.equal(cases.complete.sha256, receipt.generatedFiles['out/repricing.csv']);
assert.deepEqual(cases.complete.A.counts, { met: 22 });
assert.deepEqual(cases.complete.B.counts, { met: 22 });
assert.deepEqual(cases.missing.A.counts, { met: 21, unresolved: 1 });
assert.deepEqual(cases.missing.B.counts, { met: 21, unresolved: 1 });
assert.deepEqual(cases.contradictory.A.counts, { met: 21, conflicting: 1 });
assert.deepEqual(cases.contradictory.B.counts, { met: 22 });
assert.equal(cases.contradictory.A.findings.find(row => row.instrument === '6M').reportedBreach, true);
const rows = csv(read('examples/calibration-review/inputs/repricing.csv'));
const summary = JSON.parse(read('examples/sofr-curve/inputs/results.json'));
for (const method of ['A', 'B']) {
  const worst = rows.reduce((left, right) => Math.abs(number(left[`error_${method}_bp`])) > Math.abs(number(right[`error_${method}_bp`])) ? left : right);
  assert.ok(Math.abs(Math.abs(number(worst[`error_${method}_bp`])) - summary.repricing_max_abs_error_bp[method]) <= halfUnit(worst[`error_${method}_bp`]));
}
assert.deepEqual(review([...rows, { ...rows[0], instrument: '9M' }]).unexpected, ['9M']);
assert.equal(review([...rows, rows[0]]).A.findings[0].reason, 'duplicate');
const bad = structuredClone(rows); bad[0].error_A_bp = '';
assert.equal(review(bad).A.findings[0].reason, 'nonnumeric');
const wrongTarget = structuredClone(rows); wrongTarget[0].market_pct = '3.000000';
assert.equal(review(wrongTarget).A.findings[0].targetConflict, true);
const adverse = structuredClone(rows); adverse[0].implied_A_pct = '3.850020'; adverse[0].error_A_bp = '2.000e-03';
assert.equal(review(adverse).A.findings[0].finding, 'not met');
const roundedBoundary = structuredClone(rows); roundedBoundary[0].error_A_bp = '1.000e-06';
assert.equal(review(roundedBoundary).A.findings[0].finding, 'unresolved', 'rounded boundary cannot prove exact equality');
assert.ok(rows.every(row => row.market_pct === row.implied_A_pct && row.market_pct === row.implied_B_pct));
assert.ok(rows.some(row => number(row.error_A_bp) !== 0), 'equal rounded displays must not erase measured residuals');
console.log(JSON.stringify({ expectedPerMethod: expected.size, excluded, limitBp: limit, cases, mutationControls: 'passed', scope: 'Explicit table/precision relationships only; no report evaluation or financial-model execution.' }, null, 2));
