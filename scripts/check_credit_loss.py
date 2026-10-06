"""Fixed credit-loss packet controls; no QuantLib, model or arbitrary prose assessment."""
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'examples/credit-loss-review'
TIMES = [0., 1., 2., 3., 5.]
EXPOSURES = [1_000_000., 800_000., 600_000., 400_000.]
SEVERITIES = [.45, .45, .5, .5]
METHODS = ['interval_mass', 'cumulative_as_interval', 'conditional_as_unconditional',
           'hazard_times_interval', 'recovery_as_loss', 'undiscounted']
BINDINGS = ['probability', 'exposure', 'severity', 'discount']
SCOPE = {
    'reference_date': '2026-01-01', 'day_count': 'Actual/365 Fixed',
    'time_coordinates': 'exact year fractions, not calendar anniversaries',
    'hazard_per_year': .12, 'discount_rate_per_year': .03,
    'probability_basis': 'stipulated synthetic distribution',
    'default_event': 'absorbing, no cure or competing events',
    'loss_timing': 'interval end', 'currency': 'USD',
    'exposure_and_severity': 'deterministic conditional on interval default',
    'probability_tolerance': 1e-12, 'amount_tolerance_usd': 1e-7,
}
CLAIMS = [
    'All six constructions satisfy the selected method because every probability weight lies between zero and one.',
    'Conditional interval probabilities need no survival adjustment when their sum is below one.',
    'Agreement in the first interval establishes correct probability conditioning for all horizons.',
    'Recovery and loss fractions are interchangeable because they agree at 50%.',
    'Correct default probabilities are sufficient to establish the selected discounted loss.',
    'This is a market-calibrated borrower forecast and an approved accounting reserve.',
]


def within(actual, expected, tolerance):
    return abs(actual-expected) <= tolerance


def close(actual, expected, tolerance=1e-12):
    assert isinstance(actual, (float, int)) and not isinstance(actual, bool)
    assert math.isfinite(actual) and within(actual, expected, tolerance), (actual, expected)


def state(actual, expected, tolerance=1e-12):
    return 'unresolved' if expected is None else ('met' if within(actual, expected, tolerance) else 'breached')


def combine(states):
    return 'breached' if 'breached' in states else ('unresolved' if 'unresolved' in states else 'met')


def findings(packet):
    """Assess selected bindings; never replace a null requirement with an observed choice."""
    selected = packet['selected_method']
    hazard, rate = selected['scope']['hazard_per_year'], selected['scope']['discount_rate_per_year']
    reference = []
    for interval in selected['intervals']:
        a, b = interval['start_years'], interval['end_years']
        mass = math.exp(-hazard*a) * (-math.expm1(-hazard*(b-a)))
        df = math.exp(-rate*b)
        amount = None if interval['loss_fraction'] is None else mass*interval['exposure_usd']*interval['loss_fraction']*df
        reference.append({'probability': mass, 'exposure': interval['exposure_usd'],
                          'severity': interval['loss_fraction'], 'discount': df,
                          'expected_loss_usd': amount})
    output = []
    for construction in packet['observed_constructions']:
        rows = []
        for observed, expected in zip(construction['rows'], reference):
            current = dict(zip(BINDINGS, [observed['probability_weight'], observed['exposure_usd'],
                                         observed['loss_fraction_used'], observed['discount_factor_used']]))
            statuses = {key: state(current[key], expected[key], 1e-7 if key == 'exposure' else 1e-12) for key in BINDINGS}
            rows.append({'interval_id': observed['interval_id'], 'bindings': statuses,
                         'state': combine(statuses.values())})
        output.append({'id': construction['id'], 'rows': rows,
                       'state': combine([row['state'] for row in rows]),
                       'unresolved_intervals': [row['interval_id'] for row in rows if 'unresolved' in row['bindings'].values()]})
    total = None if any(row['expected_loss_usd'] is None for row in reference) else math.fsum(row['expected_loss_usd'] for row in reference)
    return {'reference_intervals': reference, 'selected_total_usd': total, 'constructions': output}


def verify(packet, source_hash):
    assert packet['subject'] == 'CREDIT-LOSS-2026-10-06'
    assert packet['source_sha256'] == source_hash
    case = packet['case']
    assert case in ['complete', 'missing-severity', 'contradictory']
    selected = packet['selected_method']
    assert selected['scope'] == SCOPE
    assert len(selected['intervals']) == 4
    for i, row in enumerate(selected['intervals']):
        expected = {'id': f'I{i+1}', 'start_years': TIMES[i], 'end_years': TIMES[i+1],
                    'exposure_usd': EXPOSURES[i],
                    'loss_fraction': None if case == 'missing-severity' and i == 0 else SEVERITIES[i]}
        assert row == expected
    probabilities = packet['observed_probabilities']
    assert len(probabilities['nodes']) == 5 and len(probabilities['intervals']) == 4
    survival = [math.exp(-.12*t) for t in TIMES]
    mass = [survival[i]*(-math.expm1(-.12*(TIMES[i+1]-TIMES[i]))) for i in range(4)]
    conditional = [-math.expm1(-.12*(TIMES[i+1]-TIMES[i])) for i in range(4)]
    discount = [math.exp(-.03*t) for t in TIMES[1:]]
    for i, row in enumerate(probabilities['nodes']):
        assert row['time_years'] == TIMES[i]
        close(row['survival'], survival[i])
        close(row['cumulative_default'], -math.expm1(-.12*TIMES[i]))
        close(row['native_hazard_per_year'], .12)
    for i, row in enumerate(probabilities['intervals']):
        assert row['id'] == f'I{i+1}'
        close(row['unconditional_default'], mass[i])
        close(row['conditional_default'], conditional[i])
        close(row['discount_factor'], discount[i])
    assert [c['id'] for c in packet['observed_constructions']] == METHODS
    observed_base = packet['observed_constructions'][0]['total_expected_loss_usd']
    for construction in packet['observed_constructions']:
        method = construction['id']
        assert [r['interval_id'] for r in construction['rows']] == ['I1', 'I2', 'I3', 'I4']
        amounts, weights = [], []
        for i, row in enumerate(construction['rows']):
            # These are fixed observed implementation bindings, not missing subject requirements.
            weight = mass[i]
            if method == 'cumulative_as_interval': weight = -math.expm1(-.12*TIMES[i+1])
            elif method == 'conditional_as_unconditional': weight = conditional[i]
            elif method == 'hazard_times_interval': weight = .12*(TIMES[i+1]-TIMES[i])
            severity = 1-SEVERITIES[i] if method == 'recovery_as_loss' else SEVERITIES[i]
            factor = 1. if method == 'undiscounted' else discount[i]
            close(row['probability_weight'], weight)
            assert row['exposure_usd'] == EXPOSURES[i]
            close(row['loss_fraction_used'], severity)
            close(row['discount_factor_used'], factor)
            amount = row['probability_weight']*row['exposure_usd']*row['loss_fraction_used']*row['discount_factor_used']
            close(row['expected_loss_usd'], amount, 1e-7)
            amounts.append(amount); weights.append(weight)
        close(construction['total_expected_loss_usd'], math.fsum(amounts), 1e-7)
        close(construction['weight_sum'], math.fsum(weights))
        assert construction['all_weights_in_unit_interval'] is True
        close(construction['difference_from_interval_mass_construction_usd'], math.fsum(amounts)-observed_base, 1e-7)
    expected_claims = [{'id': f'C{i+1}', 'text': text} for i, text in enumerate(CLAIMS)] if case == 'contradictory' else []
    assert packet['producer_claims'] == expected_claims
    result = findings(packet)
    assert [r['state'] for r in result['constructions']] == [('unresolved' if case == 'missing-severity' else 'met')] + ['breached']*5
    assert (result['selected_total_usd'] is None) is (case == 'missing-severity')
    for construction in result['constructions']:
        assert construction['unresolved_intervals'] == (['I1'] if case == 'missing-severity' else [])
        for i, row in enumerate(construction['rows']):
            expected = dict.fromkeys(BINDINGS, 'met')
            if case == 'missing-severity' and i == 0: expected['severity'] = 'unresolved'
            if construction['id'] in ['cumulative_as_interval', 'conditional_as_unconditional'] and i > 0: expected['probability'] = 'breached'
            if construction['id'] == 'hazard_times_interval': expected['probability'] = 'breached'
            if construction['id'] == 'recovery_as_loss' and i < 2 and expected['severity'] != 'unresolved': expected['severity'] = 'breached'
            if construction['id'] == 'undiscounted': expected['discount'] = 'breached'
            assert row['bindings'] == expected
    return result


def main():
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    receipt = json.loads((ROOT/'receipt.json').read_text())
    source_hash = digest(ROOT/'model/measure.py')
    assert receipt['source_sha256'] == source_hash
    packets, results = {}, {}
    for case in ['complete', 'missing-severity', 'contradictory']:
        path = ROOT/'inputs'/f'{case}.json'
        assert receipt['packets'][case]['path'] == f'inputs/{case}.json'
        assert receipt['packets'][case]['sha256'] == digest(path)
        packets[case] = json.loads(path.read_text())
        results[case] = verify(packets[case], source_hash)
    missing = copy.deepcopy(packets['complete']); missing['case'] = 'missing-severity'
    missing['selected_method']['intervals'][0]['loss_fraction'] = None
    assert missing == packets['missing-severity']
    contradiction = copy.deepcopy(packets['complete']); contradiction['case'] = 'contradictory'
    contradiction['producer_claims'] = packets['contradictory']['producer_claims']
    assert contradiction == packets['contradictory']
    mutations = []

    def reject(name, case, change):
        altered = copy.deepcopy(packets[case]); change(altered)
        try: verify(altered, source_hash)
        except (AssertionError, KeyError, TypeError, ValueError): mutations.append(name)
        else: raise AssertionError(f'Undetected mutation: {name}')

    reject('missing_interval', 'complete', lambda p: p['observed_constructions'][0]['rows'].pop())
    reject('missing_construction', 'complete', lambda p: p['observed_constructions'].pop())
    reject('changed_horizon', 'complete', lambda p: p['selected_method']['intervals'][-1].update(end_years=4.))
    reject('wrong_probability_basis', 'complete', lambda p: p['selected_method']['scope'].update(probability_basis='market implied'))
    reject('wrong_currency', 'complete', lambda p: p['selected_method']['scope'].update(currency='EUR'))
    reject('conditional_replaces_mass', 'complete', lambda p: p['observed_constructions'][0]['rows'][1].update(probability_weight=p['observed_probabilities']['intervals'][1]['conditional_default']))
    reject('recovery_replaces_loss', 'complete', lambda p: p['observed_constructions'][0]['rows'][0].update(loss_fraction_used=.55))
    reject('discount_removed', 'complete', lambda p: p['observed_constructions'][0]['rows'][1].update(discount_factor_used=1.))
    reject('amount_inconsistent', 'complete', lambda p: p['observed_constructions'][0]['rows'][0].update(expected_loss_usd=0.))
    reject('total_inconsistent', 'complete', lambda p: p['observed_constructions'][0].update(total_expected_loss_usd=0.))
    reject('withheld_requirement_restored', 'missing-severity', lambda p: p['selected_method']['intervals'][0].update(loss_fraction=.45))
    reject('actual_choice_erased', 'missing-severity', lambda p: p['observed_constructions'][0]['rows'][0].update(loss_fraction_used=None))
    reject('producer_claim_omitted', 'contradictory', lambda p: p['producer_claims'].pop())
    reject('nonfinite_probability', 'complete', lambda p: p['observed_probabilities']['nodes'][1].update(survival=float('nan')))
    for tolerance in [1e-12, 1e-7]:
        assert within(tolerance, 0., tolerance)
        assert not within(math.nextafter(tolerance, math.inf), 0., tolerance)
    # Missing intent remains unresolved even though observed inputs contain actual values.
    partial = results['missing-severity']
    assert partial['reference_intervals'][0]['expected_loss_usd'] is None
    assert all(r['expected_loss_usd'] is not None for r in partial['reference_intervals'][1:])
    print(json.dumps({'cases_checked': list(results), 'constructions_per_case': 6,
                      'intervals_per_construction': 4, 'bindings_per_interval': 4,
                      'rejected_mutations': mutations, 'exact_tolerance_boundaries': 'passed',
                      'new_quantlib_or_provider_calls': 0}, indent=2))


if __name__ == '__main__':
    main()
