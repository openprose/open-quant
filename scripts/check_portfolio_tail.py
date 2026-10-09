"""Fixed portfolio-tail controls, not a general risk engine or prose assessment."""
import copy
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'examples/portfolio-tail-review'
LOSSES = [0, 450_000, 500_000, 950_000]
STATES = ['00', '10', '01', '11']
ALPHAS = [F(4, 5), F(9, 10), F(19, 20), F(99, 100)]
QS = [F(0), F(1, 50), F(1, 20), F(1, 10), F(-1, 25), F(16, 125)]
IDS = ['q_0', 'q_1_50', 'q_1_20', 'q_1_10', 'rho_negative_half', 'rho_positive_nine_tenths']
CLAIMS = [
    'Every proposed joint distribution is admissible because every correlation matrix is positive definite.',
    'Equal marginal default probabilities and equal expected loss establish equal portfolio tail risk.',
    'For independent defaults, the 95% expected shortfall is the strict conditional mean of USD 950,000.',
    'All native quantiles equal the exact-rational quantile under the selected rule.',
    'When no loss exceeds VaR, the conditional mean beyond VaR and expected shortfall are both zero.',
    'These calculations establish calibrated production default forecasts and approved regulatory capital.',
]



def near(actual, expected, tolerance):
    assert isinstance(actual, (int, float)) and not isinstance(actual, bool)
    assert math.isfinite(actual) and abs(actual-expected) <= tolerance, (actual, expected)


def verify(data, source_hash):
    assert data['source_sha256'] == source_hash
    assert data['subject'] == 'PORTFOLIO-TAIL-2026-10-06'
    case = data['case']
    assert case in ['complete', 'missing-allocation', 'contradictory']
    assert data['scope'] == {
        'horizon': 'one year', 'currency': 'USD', 'loss_sign': 'positive loss',
        'default_probabilities': {'A': '1/10', 'B': '1/5'},
        'loss_on_default_usd': {'A': 450_000, 'B': 500_000},
        'probability_basis': 'stipulated synthetic joint distributions',
        'discounting': 'none', 'mitigation_or_netting': 'none',
        'alpha_values': [str(a) for a in ALPHAS],
        'var_definition': 'smallest supported loss with CDF at least alpha',
        'es_definition': 'mean of worst probability mass 1-alpha, splitting a boundary atom',
        'lp_method': 'highs', 'lp_time_limit_seconds': 5,
        'lp_objective_units': 'million USD before conversion to USD tail mean'}
    assert [c['id'] for c in data['candidates']] == IDS
    mismatches, findings = [], []
    for candidate, q in zip(data['candidates'], QS):
        assert F(candidate['joint_default_probability']) == q
        rho = (q-F(1, 50))/F(3, 25)
        assert F(candidate['indicator_correlation']) == rho
        assert len(candidate['correlation_eigenvalues']) == 2
        for observed, expected in zip(candidate['correlation_eigenvalues'], sorted([1-rho, 1+rho])):
            near(observed, float(expected), 1e-12)
        probabilities = [F(7, 10)+q, F(1, 10)-q, F(1, 5)-q, q]
        assert len(candidate['states']) == 4
        for i, row in enumerate(candidate['states']):
            assert row == {'id': STATES[i], 'default_A': STATES[i][0] == '1',
                           'default_B': STATES[i][1] == '1',
                           'probability': str(probabilities[i]), 'loss_usd': LOSSES[i]}
        valid = 0 <= q <= F(1, 10)
        finding = {'id': candidate['id'], 'matrix_positive_definite': all(v > 0 for v in candidate['correlation_eigenvalues']),
                   'valid_joint_distribution': valid, 'negative_probability_states': [STATES[i] for i,p in enumerate(probabilities) if p < 0],
                   'risks': []}
        findings.append(finding)
        if not valid:
            assert candidate['expected_loss_usd'] is None and candidate['risk_summaries'] == []
            assert 'native_cdf_at_losses' not in candidate
            continue
        assert F(candidate['expected_loss_usd']) == sum(p*l for p,l in zip(probabilities, LOSSES)) == 145_000
        cumulative = [sum(probabilities[:i+1]) for i in range(4)]
        native_cdf = candidate['native_cdf_at_losses']; assert len(native_cdf) == 4
        for actual, expected in zip(native_cdf, cumulative): near(actual, float(expected), 1e-14)
        assert [r['alpha'] for r in candidate['risk_summaries']] == [str(a) for a in ALPHAS]
        for summary, alpha in zip(candidate['risk_summaries'], ALPHAS):
            var = next(loss for loss,cdf in zip(LOSSES, cumulative) if cdf >= alpha)
            strict_mass = sum(p for p,l in zip(probabilities, LOSSES) if l > var)
            inclusive_mass = sum(p for p,l in zip(probabilities, LOSSES) if l >= var)
            strict_amount = sum(p*l for p,l in zip(probabilities, LOSSES) if l > var)
            inclusive_amount = sum(p*l for p,l in zip(probabilities, LOSSES) if l >= var)
            # Independent atom-correction formula, not the measure script's greedy allocation.
            es = (strict_amount + var*(1-alpha-strict_mass))/(1-alpha)
            ref = summary['reference']
            assert ref['alpha'] == str(alpha) and ref['tail_mass'] == str(1-alpha)
            assert ref['var_usd'] == var and F(ref['expected_shortfall_usd']) == es
            assert F(ref['strict_tail_probability']) == strict_mass
            assert F(ref['inclusive_tail_probability']) == inclusive_mass
            if strict_mass == 0: assert ref['strict_tail_mean_usd'] is None
            else: assert F(ref['strict_tail_mean_usd']) == strict_amount/strict_mass
            assert F(ref['inclusive_tail_mean_usd']) == inclusive_amount/inclusive_mass
            allocation = [F(p) for p in ref['allocation']]; assert len(allocation) == 4
            assert sum(allocation) == 1-alpha
            assert all(0 <= p <= bound for p,bound in zip(allocation, probabilities))
            assert sum(p*l for p,l in zip(allocation, LOSSES))/(1-alpha) == es
            native_var = summary['native_var_usd']
            near(native_var, next(loss for loss,cdf in zip(LOSSES, native_cdf) if cdf >= float(alpha)), 0.)
            if native_var != var: mismatches.append([candidate['id'], str(alpha), native_var, var])
            lp = summary['linear_program']
            assert lp['success'] is True and lp['status'] == 0
            near(lp['expected_shortfall_usd'], float(es), 1e-6)
            absent = case == 'missing-allocation' and candidate['id'] == 'q_1_50' and alpha == F(19, 20)
            if absent:
                assert lp['allocation'] is None
            else:
                assert len(lp['allocation']) == 4
                for actual, bound in zip(lp['allocation'], probabilities):
                    assert math.isfinite(actual) and -1e-10 <= actual <= float(bound)+1e-10
                near(math.fsum(lp['allocation']), float(1-alpha), 1e-10)
                near(math.fsum(p*l for p,l in zip(lp['allocation'], LOSSES))/float(1-alpha), lp['expected_shortfall_usd'], 1e-6)
            finding['risks'].append({'alpha': str(alpha), 'exact_var_usd': var,
                                     'exact_expected_shortfall_usd': str(es),
                                     'native_quantile': 'met' if native_var == var else 'breached',
                                     'native_objective': 'met',
                                     'native_allocation': 'unresolved' if absent else 'met'})
    assert mismatches == [['q_0', '4/5', 500_000., 450_000], ['q_1_50', '4/5', 500_000., 450_000]]
    expected_claims = [{'id': f'C{i+1}', 'text': text} for i,text in enumerate(CLAIMS)] if case == 'contradictory' else []
    assert data['producer_claims'] == expected_claims
    assert sum(r['native_allocation'] == 'unresolved' for f in findings for r in f['risks']) == (1 if case == 'missing-allocation' else 0)
    return {'findings': findings, 'native_exact_quantile_differences': mismatches}


def main():
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    receipt = json.loads((ROOT/'receipt.json').read_text())
    source_hash = digest(ROOT/'model/measure.py')
    assert receipt['source_sha256'] == source_hash
    packets, results = {}, {}
    for case in ['complete', 'missing-allocation', 'contradictory']:
        path = ROOT/'inputs'/f'{case}.json'
        assert receipt['packets'][case]['path'] == f'inputs/{case}.json'
        assert receipt['packets'][case]['sha256'] == digest(path)
        packets[case] = json.loads(path.read_text())
        results[case] = verify(packets[case], source_hash)
    expected = copy.deepcopy(packets['complete']); expected['case'] = 'missing-allocation'
    expected['candidates'][1]['risk_summaries'][2]['linear_program']['allocation'] = None
    assert expected == packets['missing-allocation']
    expected = copy.deepcopy(packets['complete']); expected['case'] = 'contradictory'
    expected['producer_claims'] = packets['contradictory']['producer_claims']
    assert expected == packets['contradictory']
    mutations = []

    def reject(name, case, edit):
        changed = copy.deepcopy(packets[case]); edit(changed)
        try: verify(changed, source_hash)
        except (AssertionError, KeyError, TypeError, ValueError): mutations.append(name)
        else: raise AssertionError('Undetected mutation: '+name)

    reject('omit_zero_probability_state', 'complete', lambda p: p['candidates'][0]['states'].pop())
    reject('erase_invalid_proposal', 'complete', lambda p: p['candidates'].pop())
    reject('negative_probability_clipped', 'complete', lambda p: p['candidates'][4]['states'][3].update(probability='0'))
    reject('changed_marginal', 'complete', lambda p: p['scope']['default_probabilities'].update(A='1/5'))
    reject('changed_loss_units', 'complete', lambda p: p['candidates'][0]['states'][1].update(loss_usd=450))
    reject('strict_mean_replaces_es', 'complete', lambda p: p['candidates'][1]['risk_summaries'][2]['reference'].update(expected_shortfall_usd='950000'))
    reject('zero_for_undefined_tail', 'complete', lambda p: p['candidates'][0]['risk_summaries'][2]['reference'].update(strict_tail_mean_usd='0'))
    reject('whole_boundary_atom', 'complete', lambda p: p['candidates'][1]['risk_summaries'][2]['reference'].update(allocation=['0','0','9/50','1/50']))
    reject('missing_confidence_level', 'complete', lambda p: p['candidates'][0]['risk_summaries'].pop())
    reject('native_replaced_by_exact_quantile', 'complete', lambda p: p['candidates'][0]['risk_summaries'][0].update(native_var_usd=450_000.))
    reject('reference_replaced_by_native_quantile', 'complete', lambda p: p['candidates'][0]['risk_summaries'][0]['reference'].update(var_usd=500_000))
    reject('allocation_bounds_breached', 'complete', lambda p: p['candidates'][1]['risk_summaries'][2]['linear_program'].update(allocation=[0.,0.,0.,.05]))
    reject('missing_allocation_filled', 'missing-allocation', lambda p: p['candidates'][1]['risk_summaries'][2]['linear_program'].update(allocation=[0.,0.,.03,.02]))
    reject('known_objective_erased', 'missing-allocation', lambda p: p['candidates'][1]['risk_summaries'][2]['linear_program'].update(expected_shortfall_usd=None))
    reject('producer_claim_removed', 'contradictory', lambda p: p['producer_claims'].pop())
    reject('nonfinite_objective', 'complete', lambda p: p['candidates'][1]['risk_summaries'][2]['linear_program'].update(expected_shortfall_usd=float('nan')))
    for tolerance in [1e-14, 1e-12, 1e-10, 1e-6]:
        near(tolerance, 0., tolerance)
        try: near(math.nextafter(tolerance, math.inf), 0., tolerance)
        except AssertionError: pass
        else: raise AssertionError('Tolerance boundary failed')
    missing = results['missing-allocation']['findings'][1]['risks'][2]
    assert missing['exact_expected_shortfall_usd'] == '680000'
    assert missing['native_objective'] == 'met' and missing['native_allocation'] == 'unresolved'
    print(json.dumps({'cases_checked': list(packets), 'proposals_per_case': 6,
                      'risk_summaries_per_case': 16,
                      'retained_native_exact_quantile_differences': results['complete']['native_exact_quantile_differences'],
                      'rejected_mutations': mutations, 'exact_tolerance_boundaries': 'passed',
                      'new_solver_or_provider_calls': 0}, indent=2))


if __name__ == '__main__':
    main()
