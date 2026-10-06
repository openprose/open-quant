// Fixed packet arithmetic and authored policy controls; not a prose evaluator.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const base = new URL('../examples/dependence-review/', import.meta.url);
const bytes = path => readFileSync(new URL(path, base));
const hash = value => createHash('sha256').update(value).digest('hex');
const load = name => JSON.parse(bytes(`inputs/${name}.json`));
const receipt = JSON.parse(bytes('receipt.json'));
assert.equal(hash(bytes('model/measure.py')), receipt.source_sha256, 'calculation source identity');
for (const [name, entry] of Object.entries(receipt.projection.packets)) {
  assert.equal(entry.path, `inputs/${name}.json`);
  assert.equal(hash(bytes(entry.path)), entry.sha256, 'packet projection identity');
}
const policy = bytes('inputs/policy.md').toString();
assert.ok(policy.includes('minimum eigenvalue at least 0.05') && policy.includes('unchanged AB=0.9'), 'fixed policy binding');
assert.ok(policy.includes('absolute tolerance 1e-12') && policy.includes('A singular matrix is permitted'), 'numerical-use policy binding');
const expected = ['identity', 'singular', 'inconsistent', 'pairwise_complete', 'common_complete', 'clipped_rescaled', 'shrunk_half', 'alignment_original', 'alignment_permuted'];
const tolerance = 1e-12;
const finite = x => typeof x === 'number' && Number.isFinite(x);
const close = (x, y) => finite(x) && finite(y) && Math.abs(x - y) <= tolerance;
const sum = xs => xs.reduce((a, b) => a + b, 0);
const determinant = m => m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]);
const quadratic = (w, m) => sum(w.map((x, i) => sum(w.map((y, j) => x*m[i][j]*y))));
const conjunction = xs => xs.includes(false) ? 'breached' : xs.some(x => x !== true) ? 'unresolved' : 'met';
const replacement = (admissible, eigenvalue, ab) => conjunction([admissible, eigenvalue === null ? null : eigenvalue >= .05 - tolerance, ab === null ? null : close(ab, .9)]);

function inspect(packet) {
  assert.equal(packet.subject, 'DEPENDENCE-2026-10-06', 'subject binding');
  assert.equal(packet.source_sha256, receipt.source_sha256, 'source binding');
  assert.equal(packet.units, 'common synthetic units; variance in squared synthetic units', 'units binding');
  assert.equal(packet.observation_period, 'one shared synthetic period; no financial horizon supplied', 'period binding');
  assert.deepEqual(Object.keys(packet.matrices).sort(), [...expected].sort(), 'matrix population');
  const findings = {};
  for (const [name, record] of Object.entries(packet.matrices)) {
    const m = record.matrix, e = record.eigenvalues;
    assert.equal(m.length, 3, 'matrix shape');
    assert.ok(m.every(row => row.length === 3 && row.every(finite)), 'matrix entries');
    assert.equal(e.length, 3); assert.ok(e.every(finite), 'eigenvalues');
    assert.deepEqual(record.variable_order, name === 'alignment_permuted' ? ['C', 'A', 'B'] : ['A', 'B', 'C'], 'matrix order');
    for (let i = 0; i < 3; i++) {
      assert.ok(close(m[i][i], 1), 'unit diagonal');
      for (let j = 0; j < 3; j++) {
        assert.ok(close(m[i][j], m[j][i]), 'symmetry');
        assert.ok(Math.abs(m[i][j]) <= 1 + tolerance, 'entry bounds');
      }
    }
    assert.ok(close(sum(e), 3), 'eigenvalue trace');
    assert.ok(close(e.reduce((a, b) => a*b, 1), determinant(m)), 'eigenvalue determinant');
    assert.ok(close(sum(e.map(x => x*x)), sum(m.flat().map(x => x*x))), 'eigenvalue square sum');
    const minimum = Math.min(...e), psd = minimum >= -tolerance;
    assert.equal(record.positive_semidefinite_at_tolerance, psd, 'PSD diagnostic');
    assert.equal(record.positive_definite_above_tolerance, minimum > tolerance, 'PD diagnostic');
    const pairs = [[0, 1], [0, 2], [1, 2]];
    assert.equal(record.pair_blocks.length, pairs.length, 'pair block count');
    for (const [n, [i, j]] of pairs.entries()) {
      const pair = record.pair_blocks[n];
      assert.deepEqual(pair.variables, [record.variable_order[i], record.variable_order[j]], 'pair block identity');
      assert.ok(close(pair.eigenvalues[0], 1-Math.abs(m[i][j])) && close(pair.eigenvalues[1], 1+Math.abs(m[i][j])), 'pair spectrum');
    }
    findings[name] = { admissibility: psd ? 'met' : 'breached', minimumEigenvalue: minimum };
    if (['inconsistent', 'clipped_rescaled', 'shrunk_half'].includes(name)) {
      findings[name].eigenvalueFloor = minimum >= .05-tolerance ? 'met' : 'breached';
      findings[name].lockedAB = close(m[0][1], .9) ? 'met' : 'breached';
      findings[name].replacementPolicy = replacement(psd, minimum, m[0][1]);
    }
  }
  const witness = packet.negative_variance_witness;
  assert.ok(close(sum(witness.exposures.map(x => x*x)), 1), 'unit witness');
  assert.ok(close(quadratic(witness.exposures, packet.matrices.inconsistent.matrix), witness.quadratic_form), 'witness arithmetic');
  assert.ok(close(witness.quadratic_form, -.8), 'negative witness preserved');
  for (const name of ['clipped_rescaled', 'shrunk_half']) {
    const adjustment = packet.adjustments[name], matrix = packet.matrices[name].matrix;
    const delta = matrix.map((row, i) => row.map((x, j) => x-packet.matrices.inconsistent.matrix[i][j]));
    assert.ok(delta.flat().every((x, i) => close(x, adjustment.delta.flat()[i])), 'adjustment delta');
    assert.ok(close(adjustment.maximum_absolute_change, Math.max(...delta.flat().map(Math.abs))), 'maximum adjustment');
    assert.ok(close(adjustment.frobenius_change, Math.sqrt(sum(delta.flat().map(x => x*x)))), 'adjustment norm');
    assert.equal(adjustment.preserves_locked_ab, findings[name].lockedAB === 'met', 'locked-entry diagnostic');
    assert.equal(adjustment.meets_illustrative_eigenvalue_floor, findings[name].eigenvalueFloor === 'met', 'floor diagnostic');
    assert.ok(close(adjustment.fixed_vector_quadratic_form, quadratic(witness.exposures, matrix)), 'adjusted witness');
  }
  const data = packet.missing_data, names = ['A', 'B', 'C'];
  assert.deepEqual(data.variable_order, names, 'data variable order');
  assert.equal(data.common_count, 4, 'common count');
  assert.equal(data.pairwise_membership.length, 3, 'pair population');
  let membership = 'unresolved';
  if (data.observations !== null) {
    assert.equal(data.observations.length, 10, 'raw population');
    assert.equal(new Set(data.observations.map(r => r.id)).size, 10, 'duplicate observation');
    assert.ok(data.observations.every(r => r.values.length === 3 && r.values.every(x => x === null || finite(x))), 'raw values');
    const common = data.observations.filter(r => r.values.every(x => x !== null)).map(r => r.id);
    assert.deepEqual(data.common_membership, common, 'common membership');
    assert.equal(common.length, data.common_count);
    membership = 'supported distinct populations';
  }
  for (const [n, [i, j]] of [[0, 1], [0, 2], [1, 2]].entries()) {
    const pair = data.pairwise_membership[n];
    assert.deepEqual(pair.variables, [names[i], names[j]], 'pair identity');
    assert.equal(pair.count, 6, 'pair count');
    assert.ok(close(pair.correlation, packet.matrices.pairwise_complete.matrix[i][j]), 'pair correlation binding');
    if (data.observations !== null) {
      const rows = data.observations.filter(r => r.values[i] !== null && r.values[j] !== null);
      assert.deepEqual(pair.observation_ids, rows.map(r => r.id), 'pair membership');
      assert.equal(rows.length, pair.count);
      const x = rows.map(r => r.values[i]), y = rows.map(r => r.values[j]);
      const xc = x.map(v => v-sum(x)/x.length), yc = y.map(v => v-sum(y)/y.length);
      const value = sum(xc.map((v, k) => v*yc[k])) / Math.sqrt(sum(xc.map(v => v*v))*sum(yc.map(v => v*v)));
      assert.ok(close(pair.correlation, value), 'raw Pearson correspondence');
    } else {
      assert.equal(pair.observation_ids, null, 'missing-case membership scope');
      assert.equal(data.common_membership, null, 'missing-case common scope');
    }
  }
  const a = packet.alignment;
  assert.deepEqual(a.original_labels, ['A', 'B', 'C']); assert.deepEqual(a.permuted_labels, ['C', 'A', 'B']);
  assert.deepEqual(a.original_exposures, [1, 2, -1], 'exposure binding');
  assert.deepEqual(a.permuted_exposures, [-1, 1, 2], 'permuted exposure binding');
  assert.deepEqual(a.original_matrix, packet.matrices.alignment_original.matrix, 'original matrix binding');
  assert.deepEqual(a.permuted_matrix, packet.matrices.alignment_permuted.matrix, 'permuted matrix binding');
  assert.ok(close(a.original_variance, quadratic(a.original_exposures, a.original_matrix)), 'original variance');
  assert.ok(close(a.correctly_bound_variance, quadratic(a.permuted_exposures, a.permuted_matrix)), 'aligned variance');
  assert.ok(close(a.positionally_misbound_variance, quadratic(a.original_exposures, a.permuted_matrix)), 'misbound variance');
  assert.ok(close(a.original_variance, 8.4) && close(a.correctly_bound_variance, 8.4) && close(a.positionally_misbound_variance, 4.6), 'fixed variance observations');
  return { findings, membership, pairCounts: data.pairwise_membership.map(p => p.count), commonCount: data.common_count };
}

const cases = Object.fromEntries(['complete', 'missing-membership', 'contradictory'].map(name => [name, inspect(load(name))]));
assert.deepEqual(cases.complete, cases.contradictory, 'producer claims cannot override evidence');
assert.deepEqual(cases.complete.findings, cases['missing-membership'].findings, 'missing populations do not hide observed matrix violations');
assert.equal(cases['missing-membership'].membership, 'unresolved');
assert.equal(cases.complete.membership, 'supported distinct populations');
assert.equal(cases.complete.findings.singular.admissibility, 'met');
assert.equal(cases.complete.findings.pairwise_complete.admissibility, 'breached');
assert.ok(['inconsistent', 'clipped_rescaled', 'shrunk_half'].every(name => cases.complete.findings[name].replacementPolicy === 'breached'));
assert.equal(replacement(true, .05, .9), 'met');
assert.equal(replacement(true, .04999, .9), 'breached');
assert.equal(replacement(true, null, .9), 'unresolved');
assert.equal(replacement(false, null, .9), 'breached');
const mutations = [
  ['subject', p => p.subject = 'OTHER'],
  ['units', p => p.units = 'USD'],
  ['period', p => p.observation_period = 'one year'],
  ['asymmetry', p => p.matrices.inconsistent.matrix[0][1] = .8],
  ['matrix omission', p => delete p.matrices.singular],
  ['eigenvalue label', p => p.matrices.inconsistent.positive_semidefinite_at_tolerance = true],
  ['equal-count population swap', p => p.missing_data.pairwise_membership[1].observation_ids = p.missing_data.pairwise_membership[0].observation_ids],
  ['duplicate raw row', p => p.missing_data.observations[1].id = p.missing_data.observations[0].id],
  ['hidden adjustment', p => p.adjustments.clipped_rescaled.maximum_absolute_change = 0],
  ['false locked-entry claim', p => p.adjustments.shrunk_half.preserves_locked_ab = true],
  ['misbound variance hidden', p => p.alignment.positionally_misbound_variance = 8.4],
  ['wrong exposure order', p => p.alignment.permuted_exposures = [1, 2, -1]],
];
for (const [name, mutate] of mutations) {
  const p = load('complete'); mutate(p);
  assert.throws(() => inspect(p), { name: 'AssertionError' }, name);
}
console.log(JSON.stringify({ cases, rejectedMutations: mutations.map(([name]) => name), limits: 'Fixed records and authored policy only; no model call or arbitrary prose evaluation.' }, null, 2));
