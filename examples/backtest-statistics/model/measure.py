"""Fixed synthetic exception sequences: frequency, uncertainty and clustering."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import time

N = 250
POSITIONS = {
    'isolated_five': [25, 75, 125, 175, 225],
    'clustered_five': list(range(123, 128)),
    'boundary_cluster_five': list(range(1, 6)),
    'zero_exceptions': [],
    'isolated_ten': [13 + 25*i for i in range(10)],
    'clustered_ten': list(range(121, 131)),
}


def blocks(bits):
    return sum(x == 1 and (i == 0 or bits[i-1] == 0) for i, x in enumerate(bits))


def formula_distribution(n, k):
    if k == 0:
        return {0: 1}
    return {r: math.comb(k-1, r-1)*math.comb(n-k+1, r)
            for r in range(1, min(k, n-k+1)+1)}


def dynamic_distribution(n, k):
    # Append a bit, carrying the previous bit to count starts of blocks.
    states = {(0, 0, 0): 1}
    for length in range(n):
        following = defaultdict(int)
        for (used, previous, runs), count in states.items():
            if used + n-length-1 >= k:
                following[(used, 0, runs)] += count
            if used < k:
                following[(used+1, 1, runs + (previous == 0))] += count
        states = following
    result = defaultdict(int)
    for (used, previous, runs), count in states.items():
        if used == k:
            result[runs] += count
    return dict(sorted(result.items()))


def exact_frequency_tail(n, k):
    return Fraction(sum(math.comb(n, j)*99**(n-j) for j in range(k, n+1)), 100**n)


def binomial_sum(n, p, first, last):
    return math.fsum(math.comb(n, j)*p**j*(1-p)**(n-j)
                     for j in range(first, last+1))


def reference_interval(n, k):
    lower = 0.0
    if k:
        left, right = 0.0, 1.0
        for _ in range(100):
            middle = (left+right)/2
            if binomial_sum(n, middle, k, n) < 0.025:
                left = middle
            else:
                right = middle
        lower = (left+right)/2
    upper = 1.0
    if k < n:
        left, right = 0.0, 1.0
        for _ in range(100):
            middle = (left+right)/2
            if binomial_sum(n, middle, 0, k) > 0.025:
                left = middle
            else:
                right = middle
        upper = (left+right)/2
    return [lower, upper]


def measure():
    started = time.monotonic()
    import numpy
    import scipy
    from scipy.stats import binomtest

    controls = []

    def check(identity, actual, expected, tolerance=0):
        equal = (actual == expected if tolerance == 0 else
                 math.isfinite(actual) and abs(actual-expected) <= tolerance)
        controls.append({'id': identity, 'observed': actual, 'reference': expected,
                         'absolute_tolerance': tolerance, 'passed': equal})

    distributions = {}
    for k in (0, 5, 10):
        formula = formula_distribution(N, k)
        dynamic = dynamic_distribution(N, k)
        check(f'distribution_{k}_dynamic', dynamic, formula)
        check(f'distribution_{k}_total', sum(formula.values()), math.comb(N, k))
        distributions[str(k)] = {'formula': formula, 'dynamic': dynamic,
                                  'total': math.comb(N, k)}
    enumerated = {k: Counter() for k in range(9)}
    for bits in itertools.product((0, 1), repeat=8):
        enumerated[sum(bits)][blocks(bits)] += 1
    for k in range(9):
        reference = dict(sorted(enumerated[k].items()))
        check(f'eight_bits_{k}_formula', formula_distribution(8, k), reference)
        check(f'eight_bits_{k}_dynamic', dynamic_distribution(8, k), reference)

    sequences = []
    for identity, positions in POSITIONS.items():
        bits = [int(i in positions) for i in range(1, N+1)]
        k, r = sum(bits), blocks(bits)
        native = binomtest(k, N, p=0.01, alternative='greater')
        interval = binomtest(k, N, p=0.01, alternative='two-sided').proportion_ci(
            confidence_level=0.95, method='exact')
        exact = exact_frequency_tail(N, k)
        ci_ref = reference_interval(N, k)
        counts = formula_distribution(N, k)
        tail = Fraction(sum(count for runs, count in counts.items() if runs <= r),
                        math.comb(N, k))
        check(identity+'_count', k, len(positions))
        check(identity+'_frequency', float(native.pvalue), float(exact), 1e-12)
        check(identity+'_interval_low', float(interval.low), ci_ref[0], 1e-10)
        check(identity+'_interval_high', float(interval.high), ci_ref[1], 1e-10)
        check(identity+'_native_fraction', float(native.statistic), k/N, 1e-12)
        check(identity+'_positions', [i+1 for i, bit in enumerate(bits) if bit], positions)
        sequences.append({
            'id': identity, 'indicators': bits, 'exception_positions': positions,
            'n': N, 'exceptions': k, 'exception_fraction': k/N, 'one_runs': r,
            'frequency_test': {'null_probability': '1/100', 'alternative': native.alternative,
                               'native_pvalue': float(native.pvalue), 'exact_pvalue': str(exact),
                               'reject_at_005': float(native.pvalue) < 0.05},
            'probability_interval': {'confidence_level': 0.95, 'alternative': 'two-sided',
                                     'method': 'Clopper-Pearson',
                                     'native': [float(interval.low), float(interval.high)],
                                     'finite_sum_reference': ci_ref},
            'clustering_test': {'conditioned_on': ['n', 'exceptions'],
                                'alternative': 'fewer_one_runs', 'exact_pvalue': str(tail),
                                'pvalue': float(tail), 'reject_at_005': tail < Fraction(1, 20),
                                'timing_information': k not in (0, N)},
        })
    zero = next(row for row in sequences if row['exceptions'] == 0)
    check('zero_upper_analytic', zero['probability_interval']['native'][1],
          1-0.025**(1/N), 1e-10)
    source = Path(__file__)
    return {
        'recorded_at': datetime.now(timezone.utc).isoformat(),
        'calculation_seconds': time.monotonic()-started,
        'environment': {'python': platform.python_version(), 'numpy': numpy.__version__,
                        'scipy': scipy.__version__},
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'plan_sha256': hashlib.sha256(source.with_name('README.md').read_bytes()).hexdigest(),
        'input_sha256': hashlib.sha256(json.dumps({'n': N, 'positions': POSITIONS},
                                                  sort_keys=True).encode()).hexdigest(),
        'scope': {'constructed_indicators': True, 'real_forecast_backtest': False,
                  'null': 'Independent Bernoulli trials with constant probability.',
                  'familywise_claim': False, 'overall_model_acceptance': None,
                  'frequency_and_clustering_threshold': 0.05,
                  'clustering_limits_binomial_inference': True},
        'conditional_distributions': distributions,
        'sequences': sequences, 'controls': controls,
        'all_controls_passed': all(control['passed'] for control in controls),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; preserve the earlier observation.')
    observed = measure()
    args.output.write_text(json.dumps(observed, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'sequences': len(observed['sequences']),
                      'controls': len(observed['controls']),
                      'all_controls_passed': observed['all_controls_passed']}))
    raise SystemExit(0 if observed['all_controls_passed'] else 1)
