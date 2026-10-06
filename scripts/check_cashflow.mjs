// Fixed cash-flow observations and caller bindings, not arbitrary prose assessment.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const root = new URL('../examples/cashflow-review/', import.meta.url);
const bytes = path => readFileSync(new URL(path, root));
const hash = value => createHash('sha256').update(value).digest('hex');
const load = name => JSON.parse(bytes(`inputs/${name}.json`));
const receipt = JSON.parse(bytes('receipt.json'));
assert.equal(hash(bytes('model/measure.py')), receipt.source_sha256);
for (const [name, item] of Object.entries(receipt.projection.packets)) {
  assert.equal(item.path, `inputs/${name}.json`);
  assert.equal(hash(bytes(item.path)), item.sha256);
}
const close = (a, b, tolerance=1e-8) => assert.ok(Number.isFinite(a) && Math.abs(a-b) <= tolerance, `${a} != ${b}`);
const days = (a, b) => (Date.parse(b+'T00:00:00Z')-Date.parse(a+'T00:00:00Z'))/86400000;
const within = delta => Number.isFinite(delta) && Math.abs(delta) <= 10;
const ids = ['C1','C2','C3','C4','P1'];
const boundaries = ['2025-11-30','2026-02-28','2026-05-31','2026-08-31','2026-11-30'];
const adjusted = ['2026-03-02','2026-06-01','2026-08-31','2026-11-30','2026-11-30'];
const unadjusted = ['2026-02-28','2026-05-31','2026-08-31','2026-11-30','2026-11-30'];
const reference = '2026-03-02';
const policies = ['exclude_settlement','include_settlement'];
const names = ['selected','wrong_day_count','unadjusted_payment'];
function inspect(packet) {
  assert.equal(packet.subject, 'CASHFLOW-2026-10-06');
  assert.equal(packet.source_sha256, receipt.source_sha256);
  assert.ok(['complete','missing-schedule','contradictory'].includes(packet.case));
  const input = packet.inputs;
  assert.deepEqual(input, {
    currency: 'USD', sign: 'receiving positive', notional: 1000000, annual_coupon_rate: .05,
    accrual_boundaries: boundaries, payment_calendar: 'WeekendsOnly', evaluation_date: '2026-02-27',
    settlement_date: reference, discount_reference_date: reference, continuous_discount_rate: .04,
    discount_day_count: 'Actual/365 Fixed', quote_basis: 'absolute USD NPV, not price per 100', actual_payment_evidence: null,
  });
  assert.deepEqual(Object.keys(packet.variants), names);
  const result = {};
  for (const name of names) {
    const v = packet.variants[name], denominator = name === 'wrong_day_count' ? 365 : 360;
    const dates = name === 'unadjusted_payment' ? unadjusted : adjusted;
    assert.equal(v.accrual_convention, denominator === 360 ? 'Actual/360' : 'Actual/365 (Fixed)');
    assert.equal(v.payment_convention, name === 'unadjusted_payment' ? 'Unadjusted' : 'Following');
    assert.equal(v.selected_accrual_convention_met, denominator === 360);
    assert.equal(v.selected_payment_convention_met, name !== 'unadjusted_payment');
    const missing = packet.case === 'missing-schedule';
    const amounts = [90,92,92,91].map(x => 50000*x/denominator).concat(1000000);
    if (missing) assert.equal(v.flows, null);
    else {
      assert.deepEqual(v.flows.map(x => x.id), ids);
      v.flows.forEach((flow, i) => {
        assert.equal(flow.kind, i === 4 ? 'principal' : 'coupon');
        assert.equal(flow.payment_date, dates[i]);
        close(flow.amount_usd, amounts[i]); close(flow.reference_amount_usd, amounts[i]);
        if (i < 4) {
          assert.equal(flow.accrual_start, boundaries[i]); assert.equal(flow.accrual_end, boundaries[i+1]);
          assert.equal(flow.unadjusted_payment_date, boundaries[i+1]);
          assert.equal(flow.accrual_days, days(boundaries[i],boundaries[i+1]));
          assert.equal(flow.day_count_denominator, denominator);
          assert.equal(flow.nominal_usd, 1000000); assert.equal(flow.annual_coupon_rate, .05);
          close(flow.year_fraction, flow.accrual_days/denominator, 1e-12);
        }
      });
    }
    assert.deepEqual(Object.keys(v.valuations), policies);
    for (const key of policies) {
      const valuation = v.valuations[key], include = key === 'include_settlement';
      assert.equal(valuation.include_settlement_date_flows, include);
      close(valuation.quantlib_npv_usd, valuation.reference_npv_usd, 1e-7);
      if (missing) {
        assert.equal(valuation.flows, null); assert.equal(valuation.included_ids, null);
      } else {
        assert.deepEqual(valuation.flows.map(x=>x.id), ids);
        const included = [], pv = [];
        valuation.flows.forEach((row,i) => {
          const admitted = dates[i] > reference || (include && dates[i] === reference);
          const distance = days(reference,dates[i]);
          assert.equal(row.payment_date, dates[i]); assert.equal(row.included, admitted);
          assert.equal(row.days_from_settlement, distance);
          const discount = admitted ? Math.exp(-.04*distance/365) : null;
          if (admitted) { close(row.reference_discount, discount, 1e-12); included.push(ids[i]); }
          else assert.equal(row.reference_discount, null);
          const contribution = admitted ? amounts[i]*discount : 0;
          close(row.reference_pv_usd, contribution); pv.push(contribution);
        });
        assert.deepEqual(valuation.included_ids, included);
        close(valuation.quantlib_npv_usd, pv.reduce((a,b)=>a+b,0),1e-7);
      }
    }
    close(v.include_minus_exclude_usd, v.valuations.include_settlement.quantlib_npv_usd-v.valuations.exclude_settlement.quantlib_npv_usd,1e-7);
    result[name] = {scheduleEvidence: missing ? 'unresolved' : 'available', declaredAccrualMet: denominator===360,
      declaredPaymentMet: name!=='unadjusted_payment', paymentOccurred: 'unresolved'};
  }
  assert.deepEqual(Object.keys(packet.comparisons), names.slice(1));
  for (const name of names.slice(1)) {
    assert.deepEqual(Object.keys(packet.comparisons[name]), policies);
    for (const key of policies) {
      const c = packet.comparisons[name][key];
      const delta = packet.variants[name].valuations[key].quantlib_npv_usd-packet.variants.selected.valuations[key].quantlib_npv_usd;
      close(c.npv_difference_from_selected_usd, delta,1e-7);
      assert.equal(c.within_illustrative_ten_usd, within(delta));
    }
  }
  return result;
}
const complete = load('complete'), missing = load('missing-schedule'), contradictory = load('contradictory');
const full = inspect(complete), partial = inspect(missing);
assert.deepEqual(inspect(contradictory),full);
assert.deepEqual(contradictory.variants,complete.variants);
assert.deepEqual(contradictory.comparisons,complete.comparisons);
assert.deepEqual(complete.producer_claims,[]); assert.deepEqual(missing.producer_claims,[]);
assert.deepEqual(contradictory.producer_claims.map(x=>x.id),['P1','P2','P3','P4']);
for (const name of names) {
  assert.equal(partial[name].scheduleEvidence,'unresolved');
  for (const key of policies) close(missing.variants[name].valuations[key].quantlib_npv_usd,complete.variants[name].valuations[key].quantlib_npv_usd);
}
assert.equal(complete.comparisons.unadjusted_payment.exclude_settlement.within_illustrative_ten_usd,true);
assert.equal(full.unadjusted_payment.declaredPaymentMet,false);
assert.ok(within(10) && within(-10) && !within(10.000001) && !within(-10.000001));
const mutations = [
 ['wrong subject',x=>x.subject='OTHER'],
 ['wrong currency',x=>x.inputs.currency='EUR'],
 ['different settlement',x=>x.inputs.settlement_date='2026-03-03'],
 ['claimed payment',x=>x.inputs.actual_payment_evidence='generated schedule'],
 ['payment adjustment extends accrual',x=>x.variants.selected.flows[0].accrual_end='2026-03-02'],
 ['wrong amount',x=>x.variants.selected.flows[0].amount_usd=50000*90/365],
 ['date-only deduplication',x=>x.variants.selected.flows.pop()],
 ['wrong inclusion',x=>x.variants.selected.valuations.exclude_settlement.included_ids.unshift('C1')],
 ['incorrect NPV',x=>x.variants.selected.valuations.include_settlement.quantlib_npv_usd+=1],
 ['tolerance clears convention',x=>x.variants.unadjusted_payment.selected_payment_convention_met=true],
 ['scope flag hides schedule',x=>x.case='missing-schedule'],
 ['wrong difference sign',x=>x.comparisons.unadjusted_payment.exclude_settlement.npv_difference_from_selected_usd*=-1],
];
for (const [name,mutate] of mutations) {
  const x=structuredClone(complete); mutate(x); assert.throws(()=>inspect(x),undefined,name);
}
console.log('PASS: three fixed packets, cash-flow arithmetic, inclusion, caller bindings, aggregate boundaries and twelve adverse mutations');
console.log('Authored cases and reference report are not agent execution or payment evidence. No arbitrary prose assessment.');
