"""Prespecified synthetic optimization study; no network or operational action."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
from scipy.optimize import minimize

COVARIANCE = [[0.04, 0.002], [0.002, 0.01]]
MEANS = [0.08, 0.02]
CAPS = [0.7, 0.8]
FLOOR = 0.04
FEASIBILITY_TOLERANCE = 1e-10
OBJECTIVE_TOLERANCE = 1e-8


def reference(covariance, means, floor, caps):
    aa, ab, bb = covariance[0][0], covariance[0][1], covariance[1][1]
    a, b, c = aa - 2 * ab + bb, 2 * (ab - bb), bb
    lower, upper = max(0.0, 1.0 - caps[1]), min(1.0, caps[0])
    if floor is not None:
        assert means[0] > means[1]
        lower = max(lower, (floor - means[1]) / (means[0] - means[1]))
    record = {'coefficient_a': a, 'coefficient_b': b, 'coefficient_c': c,
              'positive_definite': aa > 0 and bb > 0 and aa * bb - ab * ab > 0,
              'feasible_interval': [lower, upper], 'feasible': lower <= upper}
    if not record['feasible']:
        return {**record, 'weights': None, 'unscaled_minimum_variance': None}
    assert a > 0
    x = min(upper, max(lower, -b / (2 * a)))
    return {**record, 'weights': [x, 1 - x], 'unscaled_minimum_variance': a * x * x + b * x + c}


def original_diagnostics(weights, selected_reference):
    x, y = weights
    variance = 0.04 * x * x + 2 * 0.002 * x * y + 0.01 * y * y
    expected_return = 0.08 * x + 0.02 * y
    constraints = {
        'full_investment': {'value': x + y, 'required': 1.0, 'violation': abs(x + y - 1)},
        'A_nonnegative': {'value': x, 'required_lower': 0.0, 'violation': max(0.0, -x)},
        'B_nonnegative': {'value': y, 'required_lower': 0.0, 'violation': max(0.0, -y)},
        'A_cap': {'value': x, 'required_upper': 0.7, 'violation': max(0.0, x - 0.7)},
        'B_cap': {'value': y, 'required_upper': 0.8, 'violation': max(0.0, y - 0.8)},
        'return_floor': {'value': expected_return, 'required_lower': 0.04, 'violation': max(0.0, 0.04 - expected_return)},
    }
    for item in constraints.values():
        item['within_tolerance'] = item['violation'] <= FEASIBILITY_TOLERANCE
    feasible = all(item['within_tolerance'] for item in constraints.values())
    gap = variance - selected_reference['unscaled_minimum_variance']
    return {'constraints': constraints, 'feasible_under_selected_policy': feasible,
            'variance': variance, 'expected_return': expected_return, 'objective_gap': gap,
            'meets_selected_optimum_tolerance': feasible and abs(gap) <= OBJECTIVE_TOLERANCE}


def measure():
    selected = reference(COVARIANCE, MEANS, FLOOR, CAPS)
    variants = [
        ('selected', COVARIANCE, MEANS, FLOOR, CAPS, 1.0, 100),
        ('omitted_return_constraint', COVARIANCE, MEANS, None, CAPS, 1.0, 100),
        ('percent_fraction_mismatch', COVARIANCE, [8.0, 2.0], FLOOR, CAPS, 1.0, 100),
        ('covariance_order_mismatch', [[0.01, 0.002], [0.002, 0.04]], MEANS, FLOOR, CAPS, 1.0, 100),
        ('scaled_objective', COVARIANCE, MEANS, FLOOR, CAPS, 1e-8, 100),
        ('infeasible_caps', COVARIANCE, MEANS, FLOOR, [0.4, 0.4], 1.0, 100),
        ('iteration_limit', COVARIANCE, MEANS, FLOOR, CAPS, 1.0, 1),
    ]
    records, controls = [], []
    start = time.monotonic()
    for name, covariance, means, floor, caps, scale, maxiter in variants:
        matrix, mu = np.array(covariance), np.array(means)
        objective = lambda w: float(scale * (w @ matrix @ w))
        gradient = lambda w: scale * 2 * matrix @ w
        constraints = [{'type': 'eq', 'fun': lambda w: float(w.sum() - 1), 'jac': lambda w: np.ones(2)}]
        if floor is not None:
            constraints.append({'type': 'ineq', 'fun': lambda w: float(w @ mu - floor), 'jac': lambda w: mu})
        options = {'ftol': 1e-12, 'maxiter': maxiter, 'disp': False}
        native = minimize(objective, [0.5, 0.5], jac=gradient, method='SLSQP',
                          bounds=[(0.0, cap) for cap in caps], constraints=constraints, options=options)
        weights = native.x.tolist()
        x, y = weights
        aa, ab, bb = covariance[0][0], covariance[0][1], covariance[1][1]
        scalar_objective = scale * (aa*x*x + 2*ab*x*y + bb*y*y)
        scalar_gradient = [scale*2*(aa*x+ab*y), scale*2*(ab*x+bb*y)]
        analytical = reference(covariance, means, floor, caps)
        checks = {
            'finite_candidate': all(math.isfinite(v) for v in weights),
            'native_objective_matches_scalar': math.isclose(float(native.fun), scalar_objective, rel_tol=1e-12, abs_tol=1e-14),
            'native_gradient_matches_scalar': all(math.isclose(float(v), e, rel_tol=1e-12, abs_tol=1e-14) for v, e in zip(native.jac, scalar_gradient)),
            'implemented_covariance_positive_definite': analytical['positive_definite'],
        }
        if name in ['selected', 'omitted_return_constraint', 'percent_fraction_mismatch', 'covariance_order_mismatch']:
            checks['candidate_matches_implemented_analytical_minimum'] = max(abs(v-e) for v,e in zip(weights, analytical['weights'])) <= 1e-7
        controls.extend({'variant': name, 'check': key, 'passed': value} for key,value in checks.items())
        record = {'id': name, 'kind': 'observed_solver_result', 'position_order': ['A', 'B'],
                  'implemented_problem': {'covariance': covariance, 'expected_returns': means, 'return_floor': floor, 'caps': caps, 'objective_scale': scale},
                  'solver': {'method': 'SLSQP', 'start': [0.5, 0.5], 'options': options, 'success': bool(native.success),
                             'status': int(native.status), 'message': str(native.message), 'iterations': int(native.nit),
                             'function_evaluations': int(native.nfev), 'gradient_evaluations': int(native.njev),
                             'weights': weights, 'objective': float(native.fun), 'gradient': native.jac.tolist(),
                             'multipliers': native.multipliers.tolist() if 'multipliers' in native else None},
                  'implemented_problem_reference': analytical,
                  'selected_problem_diagnostics': original_diagnostics(weights, selected)}
        records.append(record)
    exported = [round(w, 3) for w in records[0]['solver']['weights']]
    derived = {'id': 'rounded_export', 'kind': 'derived_weight_artifact', 'source_result': 'selected',
               'decimal_places': 3, 'weights': exported, 'solver': None,
               'selected_problem_diagnostics': original_diagnostics(exported, selected)}
    return {'recorded_at': datetime.now(timezone.utc).isoformat(),
            'environment': {'python': platform.python_version(), 'scipy': importlib.metadata.version('scipy'), 'numpy': np.__version__},
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'specification': {'position_order': ['A', 'B'], 'weights_unit': 'fraction', 'covariance': COVARIANCE,
                              'covariance_unit': 'annualized fractional-return squared', 'expected_returns': MEANS,
                              'expected_return_unit': 'annualized fraction', 'caps': CAPS, 'return_floor': FLOOR,
                              'full_investment': 1.0, 'feasibility_tolerance': FEASIBILITY_TOLERANCE,
                              'variance_objective_tolerance': OBJECTIVE_TOLERANCE, 'reference': selected},
            'solver_results': records, 'derived_candidates': [derived], 'controls': controls,
            'all_controls_passed': all(item['passed'] for item in controls),
            'calculation_seconds': time.monotonic() - start,
            'scope': 'Synthetic fixed convex construction; no financial operation, prediction evidence or agent execution.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; preserve the prior result')
    result = measure()
    with args.output.open('x') as file:
        json.dump(result, file, indent=2, allow_nan=False)
        file.write('\n')
    print(json.dumps({'all_controls_passed': result['all_controls_passed'], 'controls': len(result['controls']),
                      'solver_results': len(result['solver_results']), 'calculation_seconds': result['calculation_seconds']}))
    raise SystemExit(0 if result['all_controls_passed'] else 1)
