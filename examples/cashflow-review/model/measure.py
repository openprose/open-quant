"""Fixed synthetic coupon-leg convention controls; scope in README.md."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import QuantLib as ql
import QuantLib._QuantLib as native_ql


BOUNDARIES = ['2025-11-30', '2026-02-28', '2026-05-31', '2026-08-31', '2026-11-30']
SETTLEMENT = date(2026, 3, 2)
NOTIONAL = 1_000_000.0
RATE = .05
DISCOUNT_RATE = .04
AMOUNT_TOL = 1e-8
NPV_TOL = 1e-7


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def qdate(d):
    return ql.Date(d.day, d.month, d.year)


def iso(d):
    return date(d.year(), int(d.month()), d.dayOfMonth()).isoformat()


def following(d):
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def calculate():
    started = time.monotonic()
    checks = []

    def numeric(name, actual, expected, tolerance):
        error = abs(actual-expected)
        checks.append({'name': name, 'actual': actual, 'expected': expected,
                       'absolute_error': error, 'tolerance': tolerance, 'passed': error <= tolerance})

    def exact(name, actual, expected):
        checks.append({'name': name, 'actual': actual, 'expected': expected, 'passed': actual == expected})

    variants = {}
    with ql.SavedSettings():
        ql.Settings.instance().evaluationDate = ql.Date(27, 2, 2026)
        calendar = ql.WeekendsOnly()
        reference = qdate(SETTLEMENT)
        curve = ql.YieldTermStructureHandle(ql.FlatForward(reference, DISCOUNT_RATE, ql.Actual365Fixed(), ql.Continuous))
        for name, denominator, convention in [('selected', 360, ql.Following),
                                               ('wrong_day_count', 365, ql.Following),
                                               ('unadjusted_payment', 360, ql.Unadjusted)]:
            dc = ql.Actual360() if denominator == 360 else ql.Actual365Fixed()
            flows, leg = [], []
            for i, (start_text, end_text) in enumerate(zip(BOUNDARIES[:-1], BOUNDARIES[1:])):
                start, end = date.fromisoformat(start_text), date.fromisoformat(end_text)
                payment = calendar.adjust(qdate(end), convention)
                expected_date = end if convention == ql.Unadjusted else following(end)
                coupon = ql.FixedRateCoupon(payment, NOTIONAL, RATE, dc, qdate(start), qdate(end))
                amount = coupon.amount()
                days = (end-start).days
                expected_amount = NOTIONAL*RATE*days/denominator
                key = f'C{i+1}'
                exact(f'{name}/{key}/accrual_start', iso(coupon.accrualStartDate()), start_text)
                exact(f'{name}/{key}/accrual_end', iso(coupon.accrualEndDate()), end_text)
                exact(f'{name}/{key}/payment_date', iso(coupon.date()), expected_date.isoformat())
                numeric(f'{name}/{key}/amount', amount, expected_amount, AMOUNT_TOL)
                flows.append({'id': key, 'kind': 'coupon', 'accrual_start': start_text, 'accrual_end': end_text,
                              'accrual_days': days, 'year_fraction': coupon.accrualPeriod(),
                              'day_count_denominator': denominator, 'unadjusted_payment_date': end_text,
                              'payment_date': iso(coupon.date()), 'nominal_usd': NOTIONAL, 'annual_coupon_rate': RATE,
                              'amount_usd': amount, 'reference_amount_usd': expected_amount})
                leg.append(coupon)
            principal = ql.SimpleCashFlow(NOTIONAL, qdate(date.fromisoformat(flows[-1]['payment_date'])))
            leg.append(principal)
            flows.append({'id': 'P1', 'kind': 'principal', 'payment_date': iso(principal.date()),
                          'amount_usd': principal.amount(), 'reference_amount_usd': NOTIONAL})
            valuations = {}
            for include in [False, True]:
                rows = []
                for flow in flows:
                    payment = date.fromisoformat(flow['payment_date'])
                    admitted = payment > SETTLEMENT or (include and payment == SETTLEMENT)
                    days_to_payment = (payment-SETTLEMENT).days
                    discount = math.exp(-DISCOUNT_RATE*days_to_payment/365) if admitted else None
                    contribution = flow['reference_amount_usd']*discount if admitted else 0.0
                    rows.append({'id': flow['id'], 'payment_date': flow['payment_date'], 'included': admitted,
                                 'days_from_settlement': days_to_payment, 'reference_discount': discount,
                                 'reference_pv_usd': contribution})
                expected_npv = math.fsum(row['reference_pv_usd'] for row in rows)
                observed_npv = ql.CashFlows.npv(leg, curve, include, reference, reference)
                key = 'include_settlement' if include else 'exclude_settlement'
                numeric(f'{name}/{key}/npv', observed_npv, expected_npv, NPV_TOL)
                valuations[key] = {'include_settlement_date_flows': include, 'quantlib_npv_usd': observed_npv,
                                   'reference_npv_usd': expected_npv, 'flows': rows,
                                   'included_ids': [r['id'] for r in rows if r['included']]}
            difference = valuations['include_settlement']['quantlib_npv_usd']-valuations['exclude_settlement']['quantlib_npv_usd']
            at_settlement = math.fsum(flow['reference_amount_usd'] for flow in flows if flow['payment_date'] == SETTLEMENT.isoformat())
            numeric(f'{name}/inclusion_difference', difference, at_settlement, NPV_TOL)
            variants[name] = {'accrual_convention': dc.name(), 'payment_convention': 'Following' if convention == ql.Following else 'Unadjusted',
                              'flows': flows, 'valuations': valuations, 'include_minus_exclude_usd': difference,
                              'selected_accrual_convention_met': denominator == 360,
                              'selected_payment_convention_met': convention == ql.Following}
        comparisons = {}
        for name in ['wrong_day_count', 'unadjusted_payment']:
            comparisons[name] = {}
            for key in ['exclude_settlement', 'include_settlement']:
                delta = variants[name]['valuations'][key]['quantlib_npv_usd']-variants['selected']['valuations'][key]['quantlib_npv_usd']
                comparisons[name][key] = {'npv_difference_from_selected_usd': delta,
                                         'within_illustrative_ten_usd': abs(delta) <= 10.0}
        exact('selected/day_counts', [r['accrual_days'] for r in variants['selected']['flows'] if r['kind'] == 'coupon'], [90, 92, 92, 91])
        exact('selected/payment_dates', [r['payment_date'] for r in variants['selected']['flows'] if r['kind'] == 'coupon'],
              ['2026-03-02', '2026-06-01', '2026-08-31', '2026-11-30'])
        numeric('selected/settlement_coupon', variants['selected']['include_minus_exclude_usd'], 12500.0, NPV_TOL)
    return {'schema': 'open-quant-cashflow-observations-v1', 'observed_at': datetime.now(timezone.utc).isoformat(),
            'source_sha256': sha(__file__),
            'environment': {'python': platform.python_version(), 'quantlib': ql.__version__,
                            'quantlib_binary_sha256': sha(native_ql.__file__), 'platform': platform.platform()},
            'inputs': {'currency': 'USD', 'sign': 'receiving positive', 'notional': NOTIONAL, 'annual_coupon_rate': RATE,
                       'accrual_boundaries': BOUNDARIES, 'payment_calendar': 'WeekendsOnly',
                       'evaluation_date': '2026-02-27', 'settlement_date': SETTLEMENT.isoformat(),
                       'discount_reference_date': SETTLEMENT.isoformat(), 'continuous_discount_rate': DISCOUNT_RATE,
                       'discount_day_count': 'Actual/365 Fixed', 'quote_basis': 'absolute USD NPV, not price per 100',
                       'actual_payment_evidence': None},
            'variants': variants, 'comparisons': comparisons, 'checks': checks,
            'all_checks_passed': all(c['passed'] for c in checks), 'calculation_seconds': time.monotonic()-started}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = calculate()
    with args.output.open('x') as output:
        json.dump(result, output, indent=2, allow_nan=False)
        output.write('\n')
    print(json.dumps({'all_checks_passed': result['all_checks_passed'], 'checks': len(result['checks']),
                      'variants': len(result['variants']), 'valuations': 6, 'calculation_seconds': result['calculation_seconds']}))
    raise SystemExit(0 if result['all_checks_passed'] else 1)
