// Fixed selection records and authored policy bindings, not report evaluation.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const base = new URL('../examples/selection-review/', import.meta.url);
const bytes = path => readFileSync(new URL(path, base));
const hash = data => createHash('sha256').update(data).digest('hex');
const receipt = JSON.parse(bytes('receipt.json'));
const load = name => JSON.parse(bytes(`inputs/${name}.json`));
assert.equal(hash(bytes('model/measure.py')), receipt.source_sha256, 'source receipt');
for (const [name, entry] of Object.entries(receipt.projection.packets)) {
  assert.equal(entry.path, `inputs/${name}.json`);
  assert.equal(hash(bytes(entry.path)), entry.sha256, 'projection receipt');
}
const policy = bytes('inputs/policy.md').toString();
assert.ok(policy.includes('strictly above its applicable threshold') && policy.includes('equality does not exceed'), 'comparison boundary');
assert.ok(policy.includes('For selected maxima, use the supplied independent-family threshold') && policy.includes('ordinary one-candidate threshold'), 'inference binding');
const finite = x => typeof x === 'number' && Number.isFinite(x);
const close = (x, y) => finite(x) && finite(y) && Math.abs(x-y) <= 1e-12;
const ids = Array.from({ length: 64 }, (_, i) => `M${String(i+1).padStart(2, '0')}`);
const winner = scores => scores.reduce((best, value, i) => value > scores[best] ? i : best, 0);
const classify = (score, threshold) => score === null ? 'unresolved' : score > threshold ? 'met' : 'not met';
function vectorHash(scores) {
  const buffer = Buffer.alloc(scores.length*8);
  scores.forEach((x, i) => buffer.writeDoubleLE(x, i*8));
  return hash(buffer);
}
// These three tails are observed fixed bindings, not a general normal CDF implementation.
const observed = {
  selection_winner: [2.1615274848032553, .01532730810124677],
  frozen_evaluation: [-.2660376689153749, .6048949007826683],
  reselected_evaluation: [2.510286421381728, .006031663560936048],
};
function inspect(packet) {
  assert.equal(packet.subject, 'SELECTION-2026-10-06', 'subject binding');
  assert.equal(packet.source_sha256, receipt.source_sha256, 'source binding');
  assert.equal(packet.units, 'dimensionless synthetic standard-normal score', 'units binding');
  assert.deepEqual(packet.candidate_ids, ids, 'candidate population/order');
  assert.deepEqual(packet.rng, { algorithm: 'PCG64DXSM', root_seed: 2026100602, replicates: 256,
    streams: 'root.spawn(256); each replicate spawns selection/evaluation children' }, 'stream design');
  const r = packet.observation, t = packet.theory;
  assert.equal(r.replicate, 0, 'replicate binding');
  assert.equal(r.candidate_count, 64, 'search-size binding');
  assert.deepEqual(r.selection_spawn_key, [0, 0]); assert.deepEqual(r.evaluation_spawn_key, [0, 1]);
  assert.equal(r.score_hash_format, '64 little-endian float64 values in candidate-index order');
  assert.ok(close(t.ordinary_threshold, 1.6448536269514715), 'ordinary threshold');
  assert.ok(close(t.family_threshold, 3.155492603794282), 'family threshold');
  assert.ok(close(t.maximum_ordinary_exceedance_probability, 1-.95**64), 'search null probability');
  assert.equal(t.frozen_evaluation_exceedance_probability, .05);
  assert.equal(t.maximum_family_exceedance_probability, .05);
  assert.equal(r.selection_scores.length, 64, 'selection population');
  assert.ok(r.selection_scores.every(finite), 'selection scores');
  assert.equal(vectorHash(r.selection_scores), r.selection_scores_sha256, 'selection identity');
  const selected = winner(r.selection_scores), evaluationAvailable = r.evaluation_scores !== null;
  if (evaluationAvailable) {
    assert.equal(r.evaluation_scores.length, 64, 'evaluation population');
    assert.ok(r.evaluation_scores.every(finite), 'evaluation scores');
    assert.equal(vectorHash(r.evaluation_scores), r.evaluation_scores_sha256, 'evaluation identity');
    assert.equal(r.evaluation_changes_candidate, selected !== winner(r.evaluation_scores), 'candidate-switch observation');
  } else {
    assert.equal(r.evaluation_scores_sha256, null, 'withheld evaluation identity');
    assert.equal(r.evaluation_changes_candidate, null, 'withheld switch observation');
    assert.equal(r.views.frozen_evaluation, null, 'withheld frozen observation');
    assert.equal(r.views.reselected_evaluation, null, 'withheld reselection observation');
  }
  assert.deepEqual(Object.keys(r.views).sort(), Object.keys(observed).sort(), 'view population');
  const findings = {};
  for (const name of Object.keys(observed)) {
    const v = r.views[name];
    if (v === null) {
      assert.ok(name !== 'selection_winner' && !evaluationAvailable);
      findings[name] = { comparison: 'unresolved', candidate: null,
        expectedCandidate: name === 'frozen_evaluation' ? ids[selected] : null,
        score: null, population: 'unavailable' };
      continue;
    }
    const index = name === 'reselected_evaluation' ? winner(r.evaluation_scores) : selected;
    assert.equal(v.index, index, 'selected index');
    assert.equal(v.candidate, ids[index], 'selected candidate');
    const score = name === 'selection_winner' ? r.selection_scores[index] : r.evaluation_scores[index];
    assert.ok(close(v.z, score), 'score correspondence');
    assert.ok(close(v.z, observed[name][0]) && close(v.raw_one_sided_tail, observed[name][1]), 'fixed score/tail binding');
    assert.equal(v.exceeds_ordinary_threshold, v.z > t.ordinary_threshold, 'ordinary exceedance');
    const maximum = name !== 'frozen_evaluation';
    if (maximum) {
      const adjusted = -Math.expm1(64*Math.log1p(-v.raw_one_sided_tail));
      assert.ok(close(v.independent_family_tail, adjusted), 'family-tail arithmetic');
      assert.equal(v.exceeds_family_threshold, v.z > t.family_threshold, 'family exceedance');
    } else {
      assert.ok(!('independent_family_tail' in v), 'frozen result is not a selected maximum');
    }
    findings[name] = { comparison: classify(v.z, maximum ? t.family_threshold : t.ordinary_threshold),
      candidate: v.candidate, score: v.z, rawTail: v.raw_one_sided_tail,
      applicableTail: maximum ? v.independent_family_tail : v.raw_one_sided_tail,
      role: maximum ? 'selected on the reported sample' : 'evaluated after selection on the other sample' };
  }
  return { findings, selectionPopulation: 64, evaluationPopulation: evaluationAvailable ? 64 : null };
}
const cases = Object.fromEntries(['complete', 'missing-evaluation', 'contradictory'].map(name => [name, inspect(load(name))]));
assert.deepEqual(cases.complete, cases.contradictory, 'producer claims do not replace observations');
assert.deepEqual(cases.complete.findings.selection_winner, cases['missing-evaluation'].findings.selection_winner);
assert.ok(Object.values(cases.complete.findings).every(f => f.comparison === 'not met'));
assert.equal(cases['missing-evaluation'].findings.frozen_evaluation.comparison, 'unresolved');
assert.equal(cases['missing-evaluation'].findings.frozen_evaluation.expectedCandidate, 'M34', 'expected candidate remains known');
assert.equal(cases['missing-evaluation'].findings.reselected_evaluation.comparison, 'unresolved');
assert.equal(winner([1, 2, 2, -1]), 1, 'tie binding');
assert.equal(classify(1, 1), 'not met'); assert.equal(classify(1.000001, 1), 'met'); assert.equal(classify(null, 1), 'unresolved');
const mutations = [
  ['subject', p => p.subject = 'OTHER'],
  ['units', p => p.units = 'annual Sharpe ratio'],
  ['candidate order', p => p.candidate_ids.reverse()],
  ['replicate', p => p.observation.replicate = 1],
  ['search size', p => p.observation.candidate_count = 1],
  ['family probability disguised', p => p.theory.maximum_ordinary_exceedance_probability = .05],
  ['frozen candidate replaced', p => p.observation.views.frozen_evaluation.candidate = 'M24'],
  ['frozen score replaced', p => p.observation.views.frozen_evaluation.z = p.observation.views.reselected_evaluation.z],
  ['selected raw tail used as family tail', p => p.observation.views.selection_winner.independent_family_tail = p.observation.views.selection_winner.raw_one_sided_tail],
  ['candidate score omitted', p => p.observation.selection_scores.pop()],
  ['evaluation value changed', p => p.observation.evaluation_scores[0] = 0],
  ['false family exceedance', p => p.observation.views.reselected_evaluation.exceeds_family_threshold = true],
];
for (const [name, change] of mutations) {
  const p = load('complete'); change(p);
  assert.throws(() => inspect(p), { name: 'AssertionError' }, name);
}
console.log(JSON.stringify({ cases, rejectedMutations: mutations.map(([name]) => name),
  limits: 'Fixed observations and authored policy only; no general CDF, prose assessment, real investment inference or agent execution.' }, null, 2));
