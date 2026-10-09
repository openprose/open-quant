// Synthetic price-scale and coverage controls; not a valuation or prose evaluator.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const packet = JSON.parse(readFileSync(new URL('../examples/valuation-review/inputs/packet.json', import.meta.url)));
const identity = (row, source) => JSON.stringify([row.instrument, row.currency, row.settlement, source]);
const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-7, `${actual} != ${expected}`);

function compare(positions, quotes) {
  assert.equal(new Set(positions.map(row => row.id)).size, positions.length, 'position IDs must be unique');
  assert.equal(new Set(quotes.map(row => row.id)).size, quotes.length, 'quote IDs must be unique');
  const rows = positions.map(position => {
    const matches = quotes.filter(quote => identity(quote, quote.source) === identity(position, position.comparison_source));
    const unresolved = reason => ({ position: position.id, quotes: matches.map(row => row.id), finding: 'unresolved', reason });
    if (matches.length !== 1) return unresolved(matches.length ? 'ambiguous quotes' : 'missing quote');
    const quote = matches[0];
    if (position.currency !== 'USD' || position.price_unit !== 'percent_of_par' || quote.price_unit !== 'percent_of_par') return unresolved('unsupported currency or price unit');
    if (position.basis !== 'clean' || quote.basis !== 'clean') return unresolved('unsupported valuation basis');
    if (position.valuation_time !== packet.review_time || quote.valuation_time !== packet.review_time) return unresolved('incompatible valuation time');
    if (!Number.isFinite(position.par) || position.par <= 0 || !Number.isFinite(position.internal_price) || position.internal_price < 0 || !Number.isFinite(quote.price) || quote.price < 0) return unresolved('invalid numerical input');
    const internal = position.internal_price * position.par / 100;
    const comparison = quote.price * position.par / 100;
    const difference = internal - comparison;
    return { position: position.id, quotes: [quote.id], internal, comparison, difference, finding: Math.abs(difference) <= 5000 ? 'within tolerance' : 'exception' };
  });
  const comparable = rows.filter(row => row.finding !== 'unresolved');
  return {
    rows,
    coverage: { comparable: comparable.length, expected: positions.length },
    unusedQuotes: quotes.filter(quote => !positions.some(position => identity(quote, quote.source) === identity(position, position.comparison_source))).map(row => row.id),
    totalsScope: 'comparable subset only',
    signedDifference: comparable.reduce((sum, row) => sum + row.difference, 0),
    absoluteDifference: comparable.reduce((sum, row) => sum + Math.abs(row.difference), 0),
  };
}

assert.equal(packet.synthetic, true);
assert.equal(packet.positions.length, 2);
assert.equal(packet.source_metadata['SYNTHETIC-FEED'].independence_verified, false);
const reference = {
  complete: { labels: ['within tolerance', 'exception'], coverage: 2, signed: -8000, absolute: 12000 },
  missing: { labels: ['within tolerance', 'unresolved'], coverage: 1, signed: 2000, absolute: 2000 },
  stale: { labels: ['within tolerance', 'unresolved'], coverage: 1, signed: 2000, absolute: 2000 },
  'basis-mismatch': { labels: ['unresolved', 'exception'], coverage: 1, signed: -10000, absolute: 10000 },
};
const results = {};
for (const [name, expected] of Object.entries(reference)) {
  const result = compare(packet.positions, packet.cases[name]);
  assert.deepEqual(result.rows.map(row => row.finding), expected.labels, name);
  assert.deepEqual(result.coverage, { comparable: expected.coverage, expected: 2 });
  assert.deepEqual(result.unusedQuotes, []);
  close(result.signedDifference, expected.signed);
  close(result.absoluteDifference, expected.absolute);
  results[name] = result;
}
close(results.complete.rows[0].internal, 984000);
close(results.complete.rows[0].comparison, 982000);
close(results.complete.rows[1].internal, 1926000);
close(results.complete.rows[1].comparison, 1936000);
assert.equal(results.stale.rows[1].reason, 'incompatible valuation time');
assert.equal(results['basis-mismatch'].rows[0].reason, 'unsupported valuation basis');

function mutate(change, check) {
  const positions = structuredClone(packet.positions);
  const quotes = structuredClone(packet.cases.complete);
  change(positions, quotes);
  check(compare(positions, quotes));
}
mutate((positions, quotes) => { quotes[0].price = 97.9; }, result => {
  close(result.rows[0].difference, 5000);
  assert.equal(result.rows[0].finding, 'within tolerance');
});
mutate((positions, quotes) => { quotes[0].price_unit = 'USD'; }, result => assert.equal(result.rows[0].finding, 'unresolved'));
mutate((positions, quotes) => { quotes[0].currency = 'EUR'; }, result => {
  assert.equal(result.rows[0].reason, 'missing quote');
  assert.deepEqual(result.unusedQuotes, ['Q1']);
});
mutate((positions, quotes) => { quotes.push({ ...quotes[0], id: 'Q1-duplicate' }); }, result => {
  assert.equal(result.rows[0].reason, 'ambiguous quotes');
  assert.deepEqual(result.rows[0].quotes, ['Q1', 'Q1-duplicate']);
});
for (const invalid of [null, '98.2', -1]) {
  mutate((positions, quotes) => { quotes[0].price = invalid; }, result => assert.equal(result.rows[0].finding, 'unresolved'));
}
mutate(positions => { positions[0].par = 0; }, result => assert.equal(result.rows[0].finding, 'unresolved'));
mutate((positions, quotes) => { quotes[0].price = 99.4; }, result => {
  assert.equal(result.rows[0].finding, 'exception');
  close(result.rows[0].difference, -10000);
});
mutate((positions, quotes) => { quotes[0].price = 97.4; }, result => {
  assert.equal(result.rows[0].finding, 'exception');
  assert.equal(result.rows[1].finding, 'exception');
  close(result.signedDifference, 0);
  close(result.absoluteDifference, 20000);
});
assert.throws(() => compare(packet.positions, [...packet.cases.complete, packet.cases.complete[0]]), /quote IDs/);
console.log(JSON.stringify({ cases: results, mutationControls: 'passed', scope: 'Synthetic comparisons only; no market-price verification, model execution or prose evaluation.' }, null, 2));
