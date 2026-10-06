// Finite numerical-record controls, not contract interpretation or prose evaluation.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const base = new URL('../examples/implementation-review/', import.meta.url);
const bytes = path => readFileSync(new URL(path, base));
const sha = value => createHash('sha256').update(value).digest('hex');
const load = name => JSON.parse(bytes(`inputs/${name}.json`));
const receipt = JSON.parse(bytes('receipt.json'));
const sourceHash = sha(bytes('model/measure.py'));
assert.equal(receipt.observer_sha256, sourceHash, 'observed calculation identity');
for (const [name, record] of Object.entries(receipt.projection.packets)) {
  assert.equal(record.path, `inputs/${name}.json`);
  assert.equal(sha(bytes(record.path)), record.sha256, `${name} projection identity`);
}
const tolerance = 1e-9;
// Caller-selected scope is independent of each packet's self-description.
const expected = {
  baseline: [100, 100, .2, 1, 0],
  'short-expiry': [100, 100, .2, .25, .03],
  'long-expiry': [100, 100, .2, 4, .03],
  'in-the-money': [120, 100, .2, 2, .03],
  'out-of-the-money': [80, 100, .2, 2, .03],
  'zero-volatility': [120, 100, 0, 2, .03],
  'zero-expiry': [120, 100, .2, 0, .03],
  'zero-strike': [100, 0, .2, 2, .03],
  'negative-rate': [100, 100, .2, 2, -.01],
  'higher-volatility': [100, 100, .8, 5, .04],
};
const invalid = {
  'zero-forward': [0, 100, .2, 1, .03],
  'negative-strike': [100, -1, .2, 1, .03],
  'negative-volatility': [100, 100, -.2, 1, .03],
  'negative-expiry': [100, 100, .2, -1, .03],
};
const variants = ['correct', 'wrong-time-scaling', 'omitted-discount'];
const inputKeys = ['forward_usd', 'strike_usd', 'annual_volatility', 'expiry_years', 'continuous_rate'];
const finite = value => typeof value === 'number' && Number.isFinite(value);
const close = (a, b) => finite(a) && finite(b) && Math.abs(a - b) <= 1e-12 * Math.max(1, Math.abs(a), Math.abs(b));
const aggregate = values => values.includes(false) ? 'breached' : values.some(x => x !== true) ? 'unresolved' : 'met';
function inspect(packet) {
  assert.equal(packet.study, 'BLACK-ADAPTERS-2026-10-06', 'study binding');
  assert.equal(packet.source_sha256, sourceHash, 'source binding');
  assert.equal(packet.price_units, 'present-value USD per underlying unit', 'unit binding');
  assert.equal(packet.absolute_tolerance, tolerance, 'tolerance binding');
  assert.equal(new Set(packet.observations.map(row => row.case)).size, packet.observations.length, 'duplicate case');
  assert.ok(packet.observations.every(row => Object.hasOwn(expected, row.case)), 'unexpected case');
  const controlIds = packet.invalid_input_controls.map(row => `${row.variant}/${row.case}`);
  assert.equal(new Set(controlIds).size, controlIds.length, 'duplicate invalid-input record');
  for (const row of packet.invalid_input_controls) {
    assert.ok(variants.includes(row.variant) && Object.hasOwn(invalid, row.case), 'unexpected invalid-input record');
    assert.deepEqual(row.inputs, invalid[row.case], 'invalid-input binding');
    assert.equal(typeof row.rejected, 'boolean');
    if (row.rejected) assert.equal(typeof row.error, 'string');
  }
  const rows = Object.entries(expected).map(([name, inputs]) => {
    const row = packet.observations.find(item => item.case === name);
    if (!row) return { case: name, supplied: false };
    assert.deepEqual(Object.keys(row.inputs).sort(), [...inputKeys].sort(), 'input fields');
    assert.deepEqual(inputKeys.map(key => row.inputs[key]), inputs, 'case input binding');
    assert.deepEqual(Object.keys(row.variants).sort(), [...variants].sort(), 'adapter population');
    const [f, k, , expiry, rate] = inputs;
    const parity = Math.exp(-rate * expiry) * (f - k);
    assert.ok(close(row.expected_parity, parity), 'expected parity arithmetic');
    const usable = ['call', 'put'].map(side => {
      const ref = row.reference[side];
      assert.ok(ref && finite(ref.price) && ref.price >= 0, 'reference price');
      assert.ok(finite(ref.estimated_error) && ref.estimated_error >= 0 && finite(ref.tail_bound) && ref.tail_bound >= 0, 'reference error estimate');
      assert.ok(Array.isArray(ref.warnings), 'reference warning record');
      return ref.warnings.length === 0 && ref.estimated_error + ref.tail_bound <= tolerance;
    }).every(Boolean);
    assert.equal(row.reference_usable, usable, 'reference qualification');
    const results = Object.fromEntries(variants.map(variant => {
      const observed = row.variants[variant];
      const errors = ['call', 'put'].map(side => {
        assert.ok(finite(observed.prices[side]) && observed.prices[side] >= 0, 'observed price');
        const error = observed.prices[side] - row.reference[side].price;
        assert.ok(close(error, observed.price_errors[side]), 'price error arithmetic');
        return error;
      });
      const price = usable ? errors.every(error => Math.abs(error) <= tolerance) : null;
      const parityError = observed.prices.call - observed.prices.put - parity;
      const parityPass = Math.abs(parityError) <= tolerance;
      assert.equal(observed.price_agreement, price, 'price agreement flag');
      assert.ok(close(observed.parity_error, parityError), 'parity residual arithmetic');
      assert.equal(observed.parity_agreement, parityPass, 'parity agreement flag');
      return [variant, { price, parity: parityPass, errors }];
    }));
    return { case: name, supplied: true, referenceUsable: usable, results };
  });
  const findings = Object.fromEntries(variants.map(variant => {
    const prices = rows.map(row => row.supplied ? row.results[variant].price : null);
    const parities = rows.map(row => row.supplied ? row.results[variant].parity : null);
    const controls = Object.keys(invalid).map(name => packet.invalid_input_controls.find(row => row.variant === variant && row.case === name)?.rejected ?? null);
    // Mapping findings are source-inspection references, not inferred from favorable prices.
    const mapping = variant === 'correct';
    return [variant, {
      mapping: mapping ? 'met' : 'breached',
      suppliedCases: rows.filter(row => row.supplied).length,
      missingCases: rows.filter(row => !row.supplied).map(row => row.case),
      priceAgreement: aggregate(prices), parity: aggregate(parities), invalidInputRejection: aggregate(controls),
      pricePasses: prices.filter(value => value === true).length,
      parityPasses: parities.filter(value => value === true).length,
      invalidRejections: controls.filter(value => value === true).length,
      overall: aggregate([mapping, ...prices, ...parities, ...controls]),
    }];
  }));
  return { findings, allAdapterPricesMet: Object.values(findings).every(row => row.priceAgreement === 'met') };
}
const cases = Object.fromEntries(['complete', 'baseline-only', 'contradictory'].map(name => [name, inspect(load(name))]));
assert.deepEqual(cases.complete, cases.contradictory, 'producer annotation does not change observed calculation findings');
assert.equal(cases.complete.findings.correct.overall, 'met');
assert.equal(cases.complete.findings['wrong-time-scaling'].pricePasses, 3);
assert.equal(cases.complete.findings['wrong-time-scaling'].parityPasses, 10);
assert.equal(cases.complete.findings['omitted-discount'].pricePasses, 2);
assert.equal(cases.complete.findings['omitted-discount'].parityPasses, 6);
assert.equal(cases.contradictory.allAdapterPricesMet, false);
for (const variant of variants) {
  const limited = cases['baseline-only'].findings[variant];
  assert.equal(limited.pricePasses, 1); assert.equal(limited.parityPasses, 1);
  assert.equal(limited.priceAgreement, 'unresolved'); assert.equal(limited.parity, 'unresolved');
  assert.equal(limited.invalidInputRejection, 'unresolved'); assert.equal(limited.missingCases.length, 9);
  assert.equal(limited.overall, variant === 'correct' ? 'unresolved' : 'breached');
}
const mutate = change => { const p = load('complete'); change(p); return p; };
for (const [change, pattern] of [
  [p => { p.study = 'OTHER-STUDY'; }, /study binding/],
  [p => { p.source_sha256 = '0'.repeat(64); }, /source binding/],
  [p => { p.price_units = 'undiscounted USD per underlying unit'; }, /unit binding/],
  [p => { p.absolute_tolerance = 1; }, /tolerance binding/],
  [p => { p.observations[0].inputs.expiry_years = 2; }, /case input binding/],
  [p => { p.observations.push(p.observations[0]); }, /duplicate case/],
  [p => { p.observations[0].case = 'unselected'; }, /unexpected case/],
  [p => { p.observations[0].reference.call.price += 1; }, /price error arithmetic/],
  [p => { p.observations[0].reference.call.estimated_error = -1; }, /reference error estimate/],
  [p => { p.observations[0].reference.call.warnings.push('observer warning'); }, /reference qualification/],
  [p => { p.observations[0].variants.correct.price_agreement = false; }, /price agreement flag/],
  [p => { p.observations[0].variants.correct.prices.call = null; }, /observed price/],
  [p => { p.observations[0].expected_parity = 1; }, /expected parity arithmetic/],
  [p => { p.invalid_input_controls.push(p.invalid_input_controls[0]); }, /duplicate invalid-input record/],
  [p => { p.invalid_input_controls[0].inputs[0] = 100; }, /invalid-input binding/],
]) assert.throws(() => inspect(mutate(change)), pattern);
const missing = inspect(mutate(p => { p.observations.pop(); }));
assert.equal(missing.findings.correct.overall, 'unresolved');
assert.equal(missing.findings['wrong-time-scaling'].priceAgreement, 'breached', 'remaining observed violation dominates missing record');
const unusable = inspect(mutate(p => {
  p.observations[0].reference.call.warnings.push('observer warning');
  p.observations[0].reference_usable = false;
  for (const v of variants) p.observations[0].variants[v].price_agreement = null;
}));
assert.equal(unusable.findings.correct.priceAgreement, 'unresolved');
assert.equal(unusable.findings['wrong-time-scaling'].priceAgreement, 'breached');
const acceptedInvalid = inspect(mutate(p => { p.invalid_input_controls[0].rejected = false; p.invalid_input_controls[0].value = 0; delete p.invalid_input_controls[0].error; }));
assert.equal(acceptedInvalid.findings.correct.invalidInputRejection, 'breached');
console.log(JSON.stringify({ cases, mutationControls: 'passed', scope: 'Finite supplied-record integrity, arithmetic, coverage and authored mapping controls; no financial repricing, prose evaluation or agent trial.' }, null, 2));
