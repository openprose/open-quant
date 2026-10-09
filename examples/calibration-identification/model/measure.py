"""One bounded synthetic variance-calibration study; no live data or model API."""
import hashlib
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import lsq_linear
import QuantLib as ql


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serial(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [serial(x) for x in value]
    return value


def variance(q, t):
    return q[0] * min(t, F(1, 2)) + q[1] * max(F(0), min(t-F(1, 2), F(1, 2))) + q[2] * max(F(0), t-1)


def main(destination):
    if Path(destination).exists():
        raise FileExistsError('Use a fresh observation path; preserve earlier evidence.')
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    A = np.array([[.5, .5, 0], [.5, .5, 1]])
    b = np.array([.04, .09])
    maturities = [F(1, 2), F(1), F(3, 2), F(2)]
    controls = []

    def check(name, value, reference, tolerance=1e-9, unit='variance/year'):
        error = abs(float(value)-float(reference))
        controls.append({'id': name, 'value': float(value), 'reference': float(reference),
                         'absolute_error': error, 'absolute_tolerance': tolerance,
                         'unit': unit, 'passed': math.isfinite(error) and error <= tolerance})

    def describe(name, q, exact_reference=None):
        q_float = list(map(float, q))
        data_residual = A @ np.array(q_float)-b
        points = []
        for t in maturities:
            w = variance(q, t)
            numeric_w = float(w)
            prices = {'quantlib_call': None, 'erf_call': None, 'total_stddev': None}
            if numeric_w >= 0:
                stddev = math.sqrt(numeric_w)
                native = float(ql.blackFormula(ql.Option.Call, 100.0, 100.0, stddev, 1.0))
                reference = 100 * math.erf(stddev/(2*math.sqrt(2)))
                check(f'{name}:call:{t}', native, reference, 1e-10, 'USD')
                prices = {'quantlib_call': native, 'erf_call': reference, 'total_stddev': stddev}
            point = {'maturity_years': float(t), 'total_variance': numeric_w,
                     'exact_variance': str(w) if isinstance(w, F) else None,
                     'formula_defined': numeric_w >= 0, **prices}
            if exact_reference is not None:
                check(f'{name}:variance:{t}', numeric_w, variance(exact_reference, t), 1e-9, 'total variance')
            points.append(point)
        return {'id': name, 'variance_rates': q_float,
                'exact_rates': [str(x) for x in q] if all(isinstance(x, F) for x in q) else None,
                'rates_nonnegative': all(x >= 0 for x in q_float),
                'original_data_residual': data_residual.tolist(),
                'original_data_fit': bool(np.max(np.abs(data_residual)) <= 1e-10),
                'points': points}

    witnesses = [
        ('late-allocation', [F(0), F(2, 25), F(1, 20)]),
        ('equal-allocation', [F(1, 25), F(1, 25), F(1, 20)]),
        ('early-allocation', [F(2, 25), F(0), F(1, 20)]),
        ('negative-rate', [F(-1, 100), F(9, 100), F(1, 20)]),
    ]
    rows = []
    for name, q in witnesses:
        row = describe(name, q)
        for i, residual in enumerate(row['original_data_residual']):
            check(f'{name}:data-residual:{i}', residual, 0, 1e-10, 'total variance')
        check(f'{name}:identified-one-half-year', variance(q, F(3, 2)), F(13, 200), 1e-10, 'total variance')
        rows.append(row)

    cases = [('unregularized', None, [F(1, 25), F(1, 25), F(1, 20)])]
    for label, d in [('preference-negative', F(-3, 50)), ('preference-zero', F(0)),
                     ('preference-positive', F(3, 50)), ('preference-incompatible', F(1, 10))]:
        expected = [(F(2, 25)+d)/2, (F(2, 25)-d)/2, F(1, 20)] if d <= F(2, 25) else [F(12, 125), F(0), F(21, 500)]
        cases.append((label, d, expected))
    solves = []
    for name, d, expected in cases:
        system = A if d is None else np.vstack([A, [1., -1., 0.]])
        target = b if d is None else np.r_[b, float(d)]
        try:
            fit = lsq_linear(system, target, bounds=(0, np.inf), method='trf',
                             lsq_solver='exact', tol=1e-14, max_iter=100)
            native = {field: serial(getattr(fit, field)) for field in
                      ['success', 'status', 'message', 'x', 'cost', 'fun', 'optimality',
                       'active_mask', 'nit', 'unbounded_sol']}
            row = describe(name, fit.x.tolist(), expected)
            for i, value in enumerate(fit.x):
                check(f'{name}:rate:{i}', value, expected[i])
            expected_cost = F(1, 25000) if name == 'preference-incompatible' else F(0)
            check(f'{name}:objective', fit.cost, expected_cost, 1e-10, 'squared total variance')
            row.update({'preference_target': None if d is None else float(d),
                        'preference_target_exact': None if d is None else str(d),
                        'preference_residual': None if d is None else float(fit.x[0]-fit.x[1]-float(d)),
                        'system_rank': int(np.linalg.matrix_rank(system)), 'native': native,
                        'exact_minimizer_reference': [str(x) for x in expected]})
            solves.append(row)
        except Exception as exc:
            solves.append({'id': name, 'error': type(exc).__name__+': '+str(exc)})
    rank = int(np.linalg.matrix_rank(A))
    check('data-rank', rank, 2, 0, 'rank')
    for i, value in enumerate(A @ np.array([1., -1., 0.])):
        check(f'null-direction:{i}', value, 0, 0, 'total variance')
    outcome = {
        'study': 'calibration-identification', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'elapsed_seconds': time.perf_counter()-start,
        'source_sha256': sha(Path(__file__)), 'plan_sha256': sha(here/'README.md'),
        'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                        'scipy': scipy.__version__, 'quantlib': ql.__version__, 'platform': platform.platform()},
        'inputs': {'A': A.tolist(), 'b': b.tolist(), 'bounds': {'lower': [0, 0, 0], 'upper': None},
                   'forward_USD': 100, 'strike_USD': 100, 'discount': 1,
                   'original_data_fit_tolerance': 1e-10, 'regularization_weight': 1},
        'identification': {'original_rank': rank, 'number_of_rates': 3,
                           'original_singular_values': np.linalg.svd(A, compute_uv=False).tolist(),
                           'null_direction': [1, -1, 0], 'q1_plus_q2': '2/25', 'q3': '1/20',
                           'half_year_variance_bounds': ['0', '1/25'], 'one_half_year_variance': '13/200'},
        'witnesses': rows, 'solves': solves, 'controls': controls,
        'all_controls_pass': all(x['passed'] for x in controls),
        'all_five_solves_returned': len(solves) == 5 and all('native' in x for x in solves),
    }
    Path(destination).write_text(json.dumps(outcome, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'solves': len(solves), 'controls': len(controls),
                      'all_controls_pass': outcome['all_controls_pass'],
                      'all_five_solves_returned': outcome['all_five_solves_returned']}))


if __name__ == '__main__':
    main(sys.argv[1])
