// Finite supplied-record checks and authored interpretation controls, not prose evaluation.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const base = new URL('../examples/simulation-review/', import.meta.url);
const bytes = path => readFileSync(new URL(path, base));
const hash = data => createHash('sha256').update(data).digest('hex');
const load = name => JSON.parse(bytes(`inputs/${name}.json`));
const receipt = JSON.parse(bytes('receipt.json'));
const sourceHash = hash(bytes('model/measure.py'));
assert.equal(receipt.source_sha256, sourceHash);
for (const [name, record] of Object.entries(receipt.projection.packets)) {
  assert.equal(record.path, `inputs/${name}.json`);
  assert.equal(hash(bytes(record.path)), record.sha256, 'projection bytes');
}
const names = ['independent_units', 'duplicated_naive', 'duplicated_grouped', 'omitted_discount'];
const finite = n => typeof n === 'number' && Number.isFinite(n);
const close = (a, b) => finite(a) && finite(b) && Math.abs(a - b) <= 1e-10 * Math.max(1, Math.abs(a), Math.abs(b));
const conjunction = values => values.includes(false) ? 'breached' : values.some(x => x !== true) ? 'unresolved' : 'met';
const precision = (target, method, se) => conjunction([target, method, se === null ? null : se <= .30]);
function inspect(packet) {
  assert.equal(packet.study, 'BLACK-SIMULATION-2026-10-06', 'study binding');
  assert.equal(packet.source_sha256, sourceHash, 'source binding');
  assert.equal(packet.target_units, 'present-value USD per underlying unit', 'target units');
  assert.deepEqual(packet.inputs, { forward_usd: 100, strike_usd: 100, annual_volatility: .3, expiry_years: 2, continuous_rate: .05 }, 'model inputs');
  assert.deepEqual(packet.rng, { algorithm: 'PCG64DXSM', root_seed: 2026100601, spawning: 'SeedSequence.spawn(64), sequential' }, 'stream binding');
  assert.ok(close(packet.discount, Math.exp(-.1)), 'discount binding');
  // Fixed observed reference bindings, not financial repricing.
  assert.ok(close(packet.intended_target_price, 15.200904102677832), 'target price');
  assert.ok(close(packet.undiscounted_target_price, packet.intended_target_price / packet.discount), 'alternative target');
  assert.equal(new Set(packet.observations.map(row => row.sample_size)).size, packet.observations.length, 'duplicate selected observation');
  for (const row of packet.observations) {
    assert.equal(row.replicate, 0, 'replicate binding');
    assert.deepEqual(row.spawn_key, [0], 'spawn binding');
    assert.ok([4096, 16384].includes(row.sample_size), 'sample-size binding');
    const n = row.sample_size;
    assert.equal(row.known_independent_units, n, 'underlying units');
    assert.deepEqual(Object.keys(row.views).sort(), [...names].sort(), 'view population');
    for (const [name, v] of Object.entries(row.views)) {
      const units = name === 'duplicated_naive' ? 2 * n : n;
      assert.equal(v.units_used_for_uncertainty, units, 'uncertainty denominator');
      assert.equal(v.recorded_rows, name.startsWith('duplicated_') ? 2 * n : n, 'recorded row count');
      assert.equal(v.ddof, 1); assert.equal(v.degrees_of_freedom, units - 1);
      assert.equal(v.nominal_confidence, .95, 'confidence binding');
      assert.ok(finite(v.sample_variance) && v.sample_variance > 0, 'sample variance');
      assert.ok(close(v.standard_error, Math.sqrt(v.sample_variance / units)), 'standard-error arithmetic');
      assert.ok(finite(v.critical_t) && v.critical_t > 1.959 && v.critical_t < 1.962, 'critical-value range');
      const [low, high] = v.interval;
      assert.ok(close(low, v.mean - v.critical_t * v.standard_error) && close(high, v.mean + v.critical_t * v.standard_error), 'interval arithmetic');
      assert.equal(v.contains_intended_target, low <= packet.intended_target_price && packet.intended_target_price <= high, 'intended interval membership');
      const actual = name === 'omitted_discount' ? packet.undiscounted_target_price : packet.intended_target_price;
      assert.equal(v.contains_actual_target, low <= actual && actual <= high, 'actual interval membership');
      assert.ok(close(v.intended_target_error, v.mean - packet.intended_target_price), 'target residual');
    }
    const a = row.views.independent_units, b = row.views.duplicated_naive;
    const c = row.views.duplicated_grouped, d = row.views.omitted_discount;
    assert.ok(close(a.mean, b.mean), 'duplication preserves estimate');
    for (const key of ['mean', 'sample_variance', 'standard_error']) assert.ok(close(a[key], c[key]), 'grouped units recover original');
    assert.ok(close(b.standard_error / a.standard_error, Math.sqrt((n - 1) / (2 * n - 1))), 'duplicate standard-error ratio');
    assert.ok(close(d.mean, a.mean / packet.discount) && close(d.standard_error, a.standard_error / packet.discount), 'different-target scaling');
  }
  const large = packet.observations.find(row => row.sample_size === 16384);
  // These source-inspection findings are authored for this fixed construction.
  const findings = Object.fromEntries(names.map(name => {
    const target = name !== 'omitted_discount', method = name !== 'duplicated_naive';
    const se = large ? large.views[name].standard_error : null;
    return [name, { target: target ? 'met' : 'breached', uncertaintyMethod: method ? 'met' : 'breached',
      observedLargeSampleStandardError: se, precision: precision(target, method, se),
      missingSampleSizes: [4096, 16384].filter(n => !packet.observations.some(row => row.sample_size === n)) }];
  }));
  return { findings, allViewsMeetSelectedCriteria: Object.values(findings).every(row => row.precision === 'met') };
}
const cases = Object.fromEntries(['complete', 'missing-large-sample', 'contradictory'].map(name => [name, inspect(load(name))]));
assert.deepEqual(cases.complete, cases.contradictory, 'authored producer label cannot override numerical or method evidence');
for (const name of names) {
  assert.equal(cases.complete.findings[name].precision, ['independent_units', 'duplicated_grouped'].includes(name) ? 'met' : 'breached');
  assert.equal(cases['missing-large-sample'].findings[name].precision, ['independent_units', 'duplicated_grouped'].includes(name) ? 'unresolved' : 'breached');
  assert.deepEqual(cases['missing-large-sample'].findings[name].missingSampleSizes, [16384]);
}
assert.equal(cases.contradictory.allViewsMeetSelectedCriteria, false);
assert.equal(precision(true, true, .30), 'met');
assert.equal(precision(true, true, .300001), 'breached');
assert.equal(precision(true, true, null), 'unresolved');
assert.equal(precision(true, false, .01), 'breached');
assert.equal(precision(false, true, .01), 'breached');
const mutate = change => { const p = load('complete'); change(p); return p; };
for (const [change, error] of [
  [p => { p.study = 'OTHER'; }, /study binding/],
  [p => { p.target_units = 'undiscounted USD'; }, /target units/],
  [p => { p.rng.root_seed = 0; }, /stream binding/],
  [p => { p.inputs.expiry_years = 1; }, /model inputs/],
  [p => { p.observations.push(p.observations[0]); }, /duplicate selected observation/],
  [p => { p.observations[0].replicate = 1; }, /replicate binding/],
  [p => { p.observations[0].sample_size = 20000; }, /sample-size binding/],
  [p => { p.observations[0].views.independent_units.standard_error = .01; }, /standard-error arithmetic/],
  [p => { p.observations[0].views.duplicated_grouped.units_used_for_uncertainty *= 2; }, /uncertainty denominator/],
  [p => { p.observations[0].views.independent_units.nominal_confidence = .99; }, /confidence binding/],
  [p => { p.observations[0].views.independent_units.interval[0] = 0; }, /interval arithmetic/],
  [p => { p.observations[0].views.independent_units.contains_intended_target = false; }, /intended interval membership/],
  [p => { p.intended_target_price = 100; }, /target price/],
]) assert.throws(() => inspect(mutate(change)), error);
const absent = inspect(mutate(p => { p.observations = []; }));
assert.equal(absent.findings.independent_units.precision, 'unresolved');
assert.equal(absent.findings.omitted_discount.precision, 'breached', 'known target convention is not cleared by missing numerical records');
console.log(JSON.stringify({ cases, mutationControls: 'passed', scope: 'Selected numerical records, arithmetic and authored policy/method controls; no sample regeneration, price calculation or report assessment.' }, null, 2));
