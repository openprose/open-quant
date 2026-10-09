#!/usr/bin/env python3
"""Bounded CPU study of Monte Carlo sampling units and target conventions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import signal
import sys
import time

import numpy as np
import numpy._core._multiarray_umath as np_native
import scipy
from scipy.stats import t
import QuantLib as ql
import QuantLib._QuantLib as ql_native

ROOT_SEED = 2026100601
REPLICATES = 64
SIZES = (4096, 16384)
F, K, SIGMA, T, RATE = 100., 100., .3, 2., .05
DISCOUNT = math.exp(-RATE * T)
ATOL = 1e-10


def sha(data):
    return hashlib.sha256(data).hexdigest()


def describe(values, intended, actual, recorded_rows):
    n = len(values)
    mean = float(np.mean(values))
    variance = float(np.var(values, ddof=1))
    se = math.sqrt(variance / n)
    critical = float(t.ppf(.975, n - 1))
    half_width = critical * se
    low, high = mean - half_width, mean + half_width
    return {"recorded_rows": recorded_rows, "units_used_for_uncertainty": n,
            "mean": mean, "sample_variance": variance, "ddof": 1,
            "standard_error": se, "critical_t": critical, "degrees_of_freedom": n - 1,
            "nominal_confidence": .95, "interval": [low, high],
            "contains_intended_target": low <= intended <= high,
            "contains_actual_target": low <= actual <= high,
            "intended_target_error": mean - intended}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Fresh output path required')
    assert (platform.python_version(), np.__version__, scipy.__version__, ql.__version__) == ('3.12.14', '2.5.3', '1.18.1', '1.43')
    signal.alarm(120)
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    stddev = SIGMA * math.sqrt(T)
    d1 = (math.log(F / K) + .5 * stddev * stddev) / stddev
    d2 = d1 - stddev
    cdf = lambda x: .5 * math.erfc(-x / math.sqrt(2))
    target = DISCOUNT * (F * cdf(d1) - K * cdf(d2))
    actual_undiscounted = target / DISCOUNT
    ql_target = ql.blackFormula(ql.Option.Call, K, F, stddev, DISCOUNT, 0.)
    failures = []
    if abs(target - ql_target) > ATOL:
        failures.append({'kind': 'closed-form reference disagreement', 'difference': target - ql_target})
    observations = []
    seeds = np.random.SeedSequence(ROOT_SEED).spawn(REPLICATES)
    for index, seed in enumerate(seeds):
        rng = np.random.Generator(np.random.PCG64DXSM(seed))
        z = rng.standard_normal(max(SIZES))
        all_payoffs = DISCOUNT * np.maximum(F * np.exp(-.5 * stddev * stddev + stddev * z) - K, 0.)
        for n in SIZES:
            payoffs = all_payoffs[:n]
            duplicated = np.repeat(payoffs, 2)
            groups = duplicated.reshape(n, 2).mean(axis=1)
            views = {
                'independent_units': describe(payoffs, target, target, n),
                'duplicated_naive': describe(duplicated, target, target, 2 * n),
                'duplicated_grouped': describe(groups, target, target, 2 * n),
                'omitted_discount': describe(payoffs / DISCOUNT, target, actual_undiscounted, n),
            }
            original = views['independent_units']
            checks = {
                'duplicate_mean': abs(views['duplicated_naive']['mean'] - original['mean']),
                'grouped_mean': abs(views['duplicated_grouped']['mean'] - original['mean']),
                'grouped_variance': abs(views['duplicated_grouped']['sample_variance'] - original['sample_variance']),
                'grouped_standard_error': abs(views['duplicated_grouped']['standard_error'] - original['standard_error']),
                'duplicate_standard_error_ratio': abs(views['duplicated_naive']['standard_error'] / original['standard_error'] - math.sqrt((n - 1) / (2 * n - 1))),
                'omitted_discount_mean': abs(views['omitted_discount']['mean'] - original['mean'] / DISCOUNT),
                'omitted_discount_variance': abs(views['omitted_discount']['sample_variance'] - original['sample_variance'] / DISCOUNT ** 2),
                'omitted_discount_standard_error': abs(views['omitted_discount']['standard_error'] - original['standard_error'] / DISCOUNT),
            }
            failures.extend({'replicate': index, 'sample_size': n, 'kind': key, 'absolute_discrepancy': value}
                            for key, value in checks.items() if value > ATOL)
            observations.append({'replicate': index, 'spawn_key': list(seed.spawn_key), 'sample_size': n,
                                 'draws_sha256': sha(z[:n].astype('<f8').tobytes()),
                                 'payoffs_sha256': sha(payoffs.astype('<f8').tobytes()),
                                 'array_encoding': 'little-endian float64, contiguous C order',
                                 'known_independent_units': n, 'views': views, 'algebraic_discrepancies': checks})
    summary = {}
    for n in SIZES:
        rows = [row for row in observations if row['sample_size'] == n]
        summary[str(n)] = {}
        for name in rows[0]['views']:
            values = [row['views'][name] for row in rows]
            summary[str(n)][name] = {
                'replicates': len(values),
                'intended_target_interval_count': sum(v['contains_intended_target'] for v in values),
                'actual_target_interval_count': sum(v['contains_actual_target'] for v in values),
                'mean_standard_error': math.fsum(v['standard_error'] for v in values) / len(values),
                'mean_interval_width': math.fsum(v['interval'][1] - v['interval'][0] for v in values) / len(values),
                'mean_absolute_error_intended_target': math.fsum(abs(v['intended_target_error']) for v in values) / len(values),
            }
    result = {
        'started_at': started, 'ended_at': datetime.now(timezone.utc).isoformat(),
        'duration_seconds': time.monotonic() - clock, 'timeout_seconds': 120, 'provider_calls': 0,
        'command': sys.argv,
        'source_sha256': sha(Path(__file__).read_bytes()),
        'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__, 'quantlib': ql.__version__, 'platform': platform.platform()},
        'native_extension_sha256': {'numpy': sha(Path(np_native.__file__).read_bytes()), 'quantlib': sha(Path(ql_native.__file__).read_bytes())},
        'rng': {'algorithm': 'PCG64DXSM', 'root_seed': ROOT_SEED, 'spawning': 'SeedSequence.spawn(64), sequential'},
        'inputs': {'forward_usd': F, 'strike_usd': K, 'annual_volatility': SIGMA, 'expiry_years': T, 'continuous_rate': RATE},
        'price_units': 'present-value USD per underlying unit', 'discount': DISCOUNT,
        'intended_target_price': target, 'quantlib_reference_price': ql_target, 'undiscounted_target_price': actual_undiscounted,
        'nominal_confidence': .95, 'algebraic_absolute_tolerance': ATOL,
        'observations': observations, 'summary': summary, 'failed_algebraic_checks': failures,
        'scope': 'Fixed finite synthetic simulation and constructed errors; not agent execution, general coverage certification or financial model validation.',
    }
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'summary': summary, 'failed_algebraic_checks': failures}, indent=2))
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
