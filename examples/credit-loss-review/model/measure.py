"""Observe a fixed synthetic credit-loss construction; no network or model calls."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import platform
import time

TIMES = [0., 1., 2., 3., 5.]
EXPOSURES = [1_000_000., 800_000., 600_000., 400_000.]
LGD = [.45, .45, .5, .5]
HAZARD = .12
RATE = .03
METHODS = ['interval_mass', 'cumulative_as_interval',
           'conditional_as_unconditional', 'hazard_times_interval',
           'recovery_as_loss', 'undiscounted']


def measure():
    started = time.monotonic()
    import QuantLib as ql

    curve = ql.FlatHazardRate(ql.Date(1, 1, 2026),
                             ql.QuoteHandle(ql.SimpleQuote(HAZARD)),
                             ql.Actual365Fixed())
    controls = []

    def check(identity, actual, expected, tolerance):
        controls.append({'id': identity, 'observed': actual,
                         'reference': expected, 'absolute_tolerance': tolerance,
                         'passed': math.isfinite(actual) and
                         abs(actual - expected) <= tolerance})

    with localcontext() as ctx:
        ctx.prec = 50
        ref_survival = [(-Decimal('.12') * Decimal(str(t))).exp() for t in TIMES]
        ref_mass = [ref_survival[i] - ref_survival[i+1] for i in range(4)]
        ref_conditional = [ref_mass[i] / ref_survival[i] for i in range(4)]
        ref_discount = [(-Decimal('.03') * Decimal(str(t))).exp() for t in TIMES[1:]]
        nodes = []
        for i, t in enumerate(TIMES):
            survival = curve.survivalProbability(t)
            cumulative = curve.defaultProbability(t)
            nodes.append({'time_years': t, 'survival': survival,
                          'cumulative_default': cumulative,
                          'native_hazard_per_year': curve.hazardRate(t)})
            check(f'survival_{i}', survival, float(ref_survival[i]), 1e-12)
            check(f'cumulative_{i}', cumulative, float(1-ref_survival[i]), 1e-12)
            check(f'hazard_{i}', nodes[-1]['native_hazard_per_year'], HAZARD, 1e-12)

        intervals = []
        for i, (start, end) in enumerate(zip(TIMES, TIMES[1:])):
            mass = curve.defaultProbability(start, end)
            conditional = mass / nodes[i]['survival']
            discount = math.exp(-RATE * end)
            intervals.append({'id': f'I{i+1}', 'start_years': start,
                              'end_years': end, 'unconditional_default': mass,
                              'conditional_default': conditional,
                              'exposure_usd': EXPOSURES[i], 'loss_fraction': LGD[i],
                              'discount_factor': discount})
            check(f'mass_{i}', mass, float(ref_mass[i]), 1e-12)
            check(f'conditional_{i}', conditional, float(ref_conditional[i]), 1e-12)
            check(f'discount_{i}', discount, float(ref_discount[i]), 1e-12)

        constructions = []
        for method in METHODS:
            rows, references = [], []
            for i, row in enumerate(intervals):
                weight, ref_weight = row['unconditional_default'], ref_mass[i]
                if method == 'cumulative_as_interval':
                    weight = nodes[i+1]['cumulative_default']
                    ref_weight = 1-ref_survival[i+1]
                elif method == 'conditional_as_unconditional':
                    weight, ref_weight = row['conditional_default'], ref_conditional[i]
                elif method == 'hazard_times_interval':
                    weight = HAZARD * (row['end_years'] - row['start_years'])
                    ref_weight = Decimal('.12') * Decimal(str(row['end_years'] - row['start_years']))
                severity = 1-LGD[i] if method == 'recovery_as_loss' else LGD[i]
                discount = 1. if method == 'undiscounted' else row['discount_factor']
                reference_severity = 1-Decimal(str(LGD[i])) if method == 'recovery_as_loss' else Decimal(str(LGD[i]))
                reference_discount = Decimal(1) if method == 'undiscounted' else ref_discount[i]
                amount = weight * EXPOSURES[i] * severity * discount
                reference_amount = ref_weight * Decimal(str(EXPOSURES[i])) * reference_severity * reference_discount
                rows.append({'interval_id': row['id'], 'probability_weight': weight,
                             'exposure_usd': EXPOSURES[i], 'loss_fraction_used': severity,
                             'discount_factor_used': discount, 'expected_loss_usd': amount})
                references.append(reference_amount)
                check(f'{method}_{row["id"]}', amount, float(reference_amount), 1e-7)
            total = math.fsum(r['expected_loss_usd'] for r in rows)
            constructions.append({'id': method, 'rows': rows, 'total_expected_loss_usd': total,
                                  'weight_sum': math.fsum(r['probability_weight'] for r in rows),
                                  'all_weights_in_unit_interval': all(0 <= r['probability_weight'] <= 1 for r in rows)})
            check(f'{method}_total', total, float(sum(references)), 1e-7)

    selected_total = constructions[0]['total_expected_loss_usd']
    for item in constructions:
        item['difference_from_selected_usd'] = item['total_expected_loss_usd'] - selected_total
    check('disjoint_mass_sum', math.fsum(r['unconditional_default'] for r in intervals),
          nodes[-1]['cumulative_default'], 1e-12)
    return {'recorded_at': datetime.now(timezone.utc).isoformat(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'environment': {'python': platform.python_version(), 'quantlib': ql.__version__},
            'scope': {'reference_date': '2026-01-01', 'day_count': 'Actual/365 Fixed',
                      'time_coordinates': 'exact year fractions, not calendar anniversaries',
                      'hazard_per_year': HAZARD, 'discount_rate_per_year': RATE,
                      'probability_basis': 'stipulated synthetic distribution',
                      'default_event': 'absorbing, no cure or competing events',
                      'loss_timing': 'interval end', 'currency': 'USD',
                      'exposure_and_severity': 'deterministic conditional on interval default',
                      'probability_tolerance': 1e-12, 'amount_tolerance_usd': 1e-7},
            'nodes': nodes, 'intervals': intervals, 'constructions': constructions,
            'controls': controls, 'all_controls_passed': all(c['passed'] for c in controls),
            'calculation_seconds': time.monotonic() - started}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; use a fresh destination.')
    observation = measure()
    with args.output.open('x') as output:
        json.dump(observation, output, indent=2, allow_nan=False)
        output.write('\n')
    if not observation['all_controls_passed']:
        raise SystemExit('One or more controls failed; observations retained.')
