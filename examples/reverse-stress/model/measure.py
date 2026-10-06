"""Prespecified synthetic reverse-stress calculation; no network or financial action."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
from scipy.optimize import minimize

METRICS = {'selected': ('1', '1'), 'raw-mixed-units': ('1', '1/25'),
           'raw-common-basis-points': ('1', '400')}
RUNS = [
    ('selected-negative-axis', 'selected', [-2.0, 0.0], 200),
    ('selected-positive-axis', 'selected', [4.0, 0.0], 200),
    ('selected-upper', 'selected', [-0.2, 0.8], 200),
    ('selected-lower', 'selected', [-0.2, -0.8], 200),
    ('selected-origin', 'selected', [0.0, 0.0], 200),
    ('selected-iteration-limit', 'selected', [4.0, 0.2], 1),
    ('raw-mixed-units', 'raw-mixed-units', [-0.2, 0.8], 200),
    ('raw-common-basis-points', 'raw-common-basis-points', [-2.0, 0.1], 200),
]
LOSS_TOLERANCE = 1e-8
SEVERITY_TOLERANCE = 1e-8


def loss(z):
    x, y = z
    return float(x*x + 4*y*y - 2*x)


def reference(a, b):
    a, b = Q(a), Q(b)
    if b < 2*a:
        x0 = -b / (4*a-b)
        minimum = b*(3*a-b)/(4*a-b)
        multiplier, cx, cy = b/4, a-b/4, Q(0)
        y2 = (3-x0*x0+2*x0)/4
        candidates = [[float(x0), math.sqrt(float(y2))],
                      [float(x0), -math.sqrt(float(y2))]]
    else:
        x0, minimum = Q(-1), a
        multiplier, cx, cy = a/2, a/2, b-2*a
        y2 = Q(0)
        candidates = [[-1.0, 0.0]]
    # Coefficient order x², y², x, constant; equality is exact over rationals.
    left = [a-multiplier, b-4*multiplier, 2*multiplier, 3*multiplier-minimum]
    right = [cx, cy, -2*cx*x0, cx*x0*x0]
    assert left == right and multiplier >= 0 and cx >= 0 and cy >= 0
    return {'weights': [str(a), str(b)], 'minimum': str(minimum),
            'minimum_float': float(minimum), 'lambda': str(multiplier),
            'square_x_coefficient': str(cx), 'square_y_coefficient': str(cy),
            'square_x_center': str(x0), 'minimizer_y_squared': str(y2),
            'polynomial_coefficients': [str(v) for v in left],
            'coefficient_identity_exact': True, 'minimizers': candidates}


def diagnostics(z, a, b):
    x, y = (float(v) for v in z)
    grad_f = [2*a*x, 2*b*y]
    grad_l = [2*x-2, 8*y]
    norm2 = sum(v*v for v in grad_l)
    if norm2:
        lam = sum(v*w for v, w in zip(grad_f, grad_l))/norm2
        residual = max(abs(v-lam*w) for v, w in zip(grad_f, grad_l))
        tangent = [-grad_l[1]/math.sqrt(norm2), grad_l[0]/math.sqrt(norm2)]
        curvature = (2*a-2*lam)*tangent[0]**2 + (2*b-8*lam)*tangent[1]**2
    else:
        lam = residual = curvature = None
    return {'candidate_gradient_multiplier': lam, 'stationarity_max_residual': residual,
            'tangent_lagrangian_curvature': curvature,
            'meaning': 'Analytic diagnostics at the observed candidate; neither a native QP multiplier nor a global certificate.'}


def quantities(z):
    x, y = map(float, z)
    values = {name: float(Q(a))*x*x + float(Q(b))*y*y for name, (a, b) in METRICS.items()}
    observed_loss = loss(z)
    gap = values['selected']-2/3
    return {'loss_million_usd': observed_loss, 'loss_usd': observed_loss*1e6,
            'threshold_margin_million_usd': observed_loss-3,
            'metric_values': values, 'selected_severity': math.sqrt(values['selected']),
            'selected_objective_gap': gap,
            'physical_shocks': {'rate_basis_points': 25*x,
                                'equity_return_percentage_points': 5*y,
                                'equity_return_basis_points': 500*y},
            'selected_threshold_supported': observed_loss >= 3-LOSS_TOLERANCE,
            'selected_optimum_supported': observed_loss >= 3-LOSS_TOLERANCE and abs(gap) <= SEVERITY_TOLERANCE}


def measure():
    started = time.monotonic()
    references = {name: reference(*ab) for name, ab in METRICS.items()}
    records, controls = [], []
    def check(subject, name, passed):
        controls.append({'subject': subject, 'check': name, 'passed': bool(passed)})
    for name, ref in references.items():
        a, b = map(lambda v: float(Q(v)), ref['weights'])
        check(name, 'exact_nonnegative_certificate', ref['coefficient_identity_exact'])
        for i, point in enumerate(ref['minimizers']):
            check(name, f'reference_{i}_threshold', abs(loss(point)-3) <= 1e-12)
            check(name, f'reference_{i}_objective', abs(a*point[0]**2+b*point[1]**2-ref['minimum_float']) <= 1e-12)
    for run_id, metric, start, maxiter in RUNS:
        a, b = (float(Q(v)) for v in METRICS[metric])
        objective = lambda z: float(a*z[0]**2+b*z[1]**2)
        jacobian = lambda z: np.array([2*a*z[0], 2*b*z[1]])
        options = {'ftol': 1e-12, 'maxiter': maxiter, 'disp': False}
        native = minimize(objective, start, method='SLSQP', jac=jacobian,
                          constraints=[{'type': 'ineq', 'fun': lambda z: loss(z)-3,
                                        'jac': lambda z: np.array([2*z[0]-2, 8*z[1]])}],
                          options=options)
        point = [float(v) for v in native.x]
        q = quantities(point)
        native_record = {'success': bool(native.success), 'status': int(native.status),
                         'message': str(native.message), 'iterations': int(native.nit),
                         'function_evaluations': int(native.nfev), 'gradient_evaluations': int(native.njev),
                         'candidate': point, 'objective': float(native.fun), 'gradient': native.jac.tolist(),
                         'qp_multipliers': native.multipliers.tolist() if 'multipliers' in native else None}
        records.append({'id': run_id, 'metric': metric, 'weights': list(METRICS[metric]),
                        'start': start, 'method': 'SLSQP', 'options': options, 'native': native_record,
                        'quantities': q, 'diagnostics': diagnostics(point, a, b),
                        'implemented_metric_objective_gap': float(native.fun)-references[metric]['minimum_float']})
        x, y = point
        check(run_id, 'finite_candidate', all(math.isfinite(v) for v in point))
        check(run_id, 'native_objective_matches_independent_scalar', math.isclose(float(native.fun), a*x*x+b*y*y, rel_tol=1e-12, abs_tol=1e-12))
        check(run_id, 'native_gradient_matches_independent_scalar', all(math.isclose(v, e, rel_tol=1e-12, abs_tol=1e-12) for v, e in zip(native.jac, [2*a*x, 2*b*y])))
        check(run_id, 'loss_expansion', math.isclose(q['loss_million_usd'], (x-1)**2+4*y*y-1, rel_tol=1e-12, abs_tol=1e-12))
        physical = q['physical_shocks']
        pp = (physical['rate_basis_points']/25)**2+(physical['equity_return_percentage_points']/5)**2
        bp = (physical['rate_basis_points']/25)**2+(physical['equity_return_basis_points']/500)**2
        check(run_id, 'selected_units_invariant', math.isclose(pp, bp, rel_tol=1e-12, abs_tol=1e-12) and math.isclose(pp, q['metric_values']['selected'], rel_tol=1e-12, abs_tol=1e-12))
        raw_pp = (physical['rate_basis_points']**2+physical['equity_return_percentage_points']**2)/625
        raw_bp = (physical['rate_basis_points']**2+physical['equity_return_basis_points']**2)/625
        check(run_id, 'raw_metric_recipe_identity', math.isclose(raw_pp, q['metric_values']['raw-mixed-units'], rel_tol=1e-12, abs_tol=1e-12) and math.isclose(raw_bp, q['metric_values']['raw-common-basis-points'], rel_tol=1e-12, abs_tol=1e-12))
    catalog = [{'id': f'C{i+1}', 'candidate': point, 'quantities': quantities(point)}
               for i, point in enumerate([[-1, 0], [3, 0], [0, 1], [0, -1]])]
    witness = {'id': 'outside-catalog', 'candidate': [0, 2], 'quantities': quantities([0, 2])}
    check('catalog', 'all_four_reach_threshold', all(r['quantities']['selected_threshold_supported'] for r in catalog))
    check('catalog', 'minimum_severity_exceeds_analytic_minimum', min(r['quantities']['metric_values']['selected'] for r in catalog) > references['selected']['minimum_float'])
    check('catalog', 'separate_witness_exceeds_catalog_loss', witness['quantities']['loss_million_usd'] > max(r['quantities']['loss_million_usd'] for r in catalog))
    return {'recorded_at': datetime.now(timezone.utc).isoformat(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'plan_sha256': hashlib.sha256(Path(__file__).with_name('README.md').read_bytes()).hexdigest(),
            'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': importlib.metadata.version('scipy')},
            'specification': {'factor_order': ['normalized_rate_change', 'normalized_equity_return_change'],
                              'loss_expression': 'x*x + 4*y*y - 2*x', 'loss_unit': 'USD million', 'threshold': 3,
                              'selected_severity_squared': 'x*x + y*y', 'domain': 'all real x,y',
                              'rate_scale_basis_points': 25, 'equity_scale_percentage_points': 5,
                              'loss_feasibility_tolerance': LOSS_TOLERANCE, 'selected_objective_tolerance': SEVERITY_TOLERANCE,
                              'probability_model': None, 'horizon': 'instantaneous', 'management_actions': None},
            'global_references': references, 'solver_results': records, 'catalog': catalog, 'outside_catalog_witness': witness,
            'controls': controls, 'all_controls_passed': all(c['passed'] for c in controls),
            'calculation_seconds': time.monotonic()-started,
            'scope': 'Synthetic quadratic loss; no empirical probability, real portfolio, regulatory qualification, agent execution or financial action.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; preserve the prior result')
    result = measure()
    with args.output.open('x') as handle:
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write('\n')
    print(json.dumps({'all_controls_passed': result['all_controls_passed'], 'controls': len(result['controls']),
                      'solver_results': len(result['solver_results']), 'calculation_seconds': result['calculation_seconds']}))
    raise SystemExit(0 if result['all_controls_passed'] else 1)
