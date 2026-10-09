"""Enumerate synthetic default losses and compare exact and native tail measures."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import time

PA, PB = F(1, 10), F(1, 5)
LOSSES = [0, 450_000, 500_000, 950_000]
STATES = ['00', '10', '01', '11']
JOINTS = [F(0), F(1, 50), F(1, 20), F(1, 10)]
ALPHAS = [F(4, 5), F(9, 10), F(19, 20), F(99, 100)]


def probabilities(q):
    return [1-PA-PB+q, PA-q, PB-q, q]


def exact_tail(probabilities, alpha):
    cumulative = F(0)
    for loss, probability in zip(LOSSES, probabilities):
        cumulative += probability
        if cumulative >= alpha:
            var = loss
            break
    remaining = 1-alpha
    allocation = [F(0)]*4
    for i in reversed(range(4)):
        allocation[i] = min(probabilities[i], remaining)
        remaining -= allocation[i]
    assert remaining == 0
    tail_loss = sum(p*l for p,l in zip(allocation, LOSSES))/(1-alpha)
    strict_mass = sum(p for l,p in zip(LOSSES, probabilities) if l > var)
    inclusive_mass = sum(p for l,p in zip(LOSSES, probabilities) if l >= var)
    strict = None if strict_mass == 0 else sum(l*p for l,p in zip(LOSSES, probabilities) if l > var)/strict_mass
    inclusive = sum(l*p for l,p in zip(LOSSES, probabilities) if l >= var)/inclusive_mass
    return {'alpha': str(alpha), 'tail_mass': str(1-alpha), 'var_usd': var,
            'expected_shortfall_usd': str(tail_loss),
            'allocation': [str(p) for p in allocation],
            'strict_tail_probability': str(strict_mass),
            'strict_tail_mean_usd': None if strict is None else str(strict),
            'inclusive_tail_probability': str(inclusive_mass),
            'inclusive_tail_mean_usd': str(inclusive)}


def measure():
    started = time.monotonic()
    import numpy as np
    import scipy
    from scipy.stats import rv_discrete
    from scipy.optimize import linprog
    controls, candidates = [], []

    def check(identity, actual, expected, tolerance):
        controls.append({'id': identity, 'observed': actual, 'reference': expected,
                         'absolute_tolerance': tolerance,
                         'passed': math.isfinite(actual) and abs(actual-expected) <= tolerance})

    settings = [(f'q_{str(q).replace("/", "_")}', q) for q in JOINTS]
    settings += [('rho_negative_half', PA*PB-F(1, 2)*F(3, 25)),
                 ('rho_positive_nine_tenths', PA*PB+F(9, 10)*F(3, 25))]
    for identity, q in settings:
        probs = probabilities(q)
        rho = (q-PA*PB)/F(3, 25)
        eigenvalues = np.linalg.eigvalsh([[1., float(rho)], [float(rho), 1.]]).tolist()
        for i, expected in enumerate(sorted([1-rho, 1+rho])):
            check(identity+f'_eigen_{i}', eigenvalues[i], float(expected), 1e-12)
        admissible = all(0 <= p <= 1 for p in probs) and sum(probs) == 1
        candidate = {'id': identity, 'joint_default_probability': str(q),
                     'indicator_correlation': str(rho), 'correlation_eigenvalues': eigenvalues,
                     'states': [{'id': s, 'default_A': s[0] == '1', 'default_B': s[1] == '1',
                                 'probability': str(p), 'loss_usd': loss}
                                for s,p,loss in zip(STATES, probs, LOSSES)],
                     'admissible_joint_distribution': admissible,
                     'risk_summaries': []}
        if not admissible:
            candidate['expected_loss_usd'] = None
            candidate['not_calculated_reason'] = 'Negative joint-state probability; no distribution supplied to native risk calculations.'
            candidates.append(candidate)
            continue
        mean = sum(p*l for p,l in zip(probs, LOSSES))
        candidate['expected_loss_usd'] = str(mean)
        check(identity+'_marginal_A', float(probs[1]+probs[3]), float(PA), 1e-14)
        check(identity+'_marginal_B', float(probs[2]+probs[3]), float(PB), 1e-14)
        check(identity+'_additive_mean', float(mean), float(PA*LOSSES[1]+PB*LOSSES[2]), 1e-6)
        distribution = rv_discrete(values=(LOSSES, [float(p) for p in probs]))
        native_cdf = [float(distribution.cdf(loss)) for loss in LOSSES]
        candidate['native_cdf_at_losses'] = native_cdf
        for i, value in enumerate(native_cdf):
            check(identity+f'_cdf_{i}', value, float(sum(probs[:i+1])), 1e-14)
        for alpha in ALPHAS:
            reference = exact_tail(probs, alpha)
            native_var = float(distribution.ppf(float(alpha)))
            expected_float_quantile = next(loss for loss,cdf in zip(LOSSES, native_cdf) if cdf >= float(alpha))
            check(identity+f'_{alpha}_native_cdf_inverse', native_var, expected_float_quantile, 0.)
            native = linprog(-np.array(LOSSES)/1_000_000., A_eq=[[1., 1., 1., 1.]],
                             b_eq=[float(1-alpha)], bounds=[(0., float(p)) for p in probs],
                             method='highs', options={'time_limit': 5.})
            allocation = None if native.x is None else native.x.tolist()
            objective = None if native.fun is None else float(-native.fun*1_000_000./float(1-alpha))
            lp = {'success': bool(native.success), 'status': int(native.status),
                  'message': str(native.message), 'allocation': allocation,
                  'expected_shortfall_usd': objective}
            if objective is not None:
                check(identity+f'_{alpha}_es', objective, float(F(reference['expected_shortfall_usd'])), 1e-6)
            else:
                controls.append({'id': identity+f'_{alpha}_missing_lp_objective', 'passed': False})
            check(identity+f'_{alpha}_lp_success', int(native.success), 1, 0.)
            if allocation is not None:
                check(identity+f'_{alpha}_allocation_mass', math.fsum(allocation), float(1-alpha), 1e-10)
                violation = max([0.] + [-x for x in allocation] + [x-float(p) for x,p in zip(allocation, probs)])
                check(identity+f'_{alpha}_allocation_bounds', violation, 0., 1e-10)
            candidate['risk_summaries'].append({'alpha': str(alpha), 'reference': reference,
                                               'native_var_usd': native_var,
                                               'native_var_matches_exact': native_var == reference['var_usd'],
                                               'linear_program': lp})
        candidates.append(candidate)
    return {'recorded_at': datetime.now(timezone.utc).isoformat(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__},
            'scope': {'horizon': 'one year', 'currency': 'USD', 'loss_sign': 'positive loss',
                      'default_probabilities': {'A': str(PA), 'B': str(PB)},
                      'loss_on_default_usd': {'A': LOSSES[1], 'B': LOSSES[2]},
                      'probability_basis': 'stipulated synthetic joint distributions',
                      'discounting': 'none', 'mitigation_or_netting': 'none',
                      'alpha_values': [str(a) for a in ALPHAS],
                      'var_definition': 'smallest supported loss with CDF at least alpha',
                      'es_definition': 'mean of worst probability mass 1-alpha, splitting a boundary atom',
                      'lp_method': 'highs', 'lp_time_limit_seconds': 5,
                      'lp_objective_units': 'million USD before conversion to USD tail mean'},
            'candidates': candidates, 'controls': controls,
            'all_controls_passed': all(c['passed'] for c in controls),
            'calculation_seconds': time.monotonic()-started}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Output already exists; use a fresh destination.')
    observation = measure()
    with args.output.open('x') as output:
        json.dump(observation, output, indent=2, allow_nan=False); output.write('\n')
    if not observation['all_controls_passed']:
        raise SystemExit('At least one control failed; observations retained.')
