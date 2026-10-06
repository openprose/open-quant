"""Fixed forward-sensitivity and price-quantization study; scope in README.md."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import QuantLib as ql
import QuantLib._QuantLib as native_ql

BUMPS = [1e-6, 1e-4, .01, .1, 1.0, 5.0]
CASES = [('ATM',100.,100.,.3,2.,.05), ('OTM',60.,100.,.3,2.,.05), ('short-ATM',100.,100.,.2,1/365,.05)]
EPSILON = .005
ILLUSTRATIVE_TOLERANCE = 1e-4


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reference(forward, strike, stddev, discount):
    d1 = math.log(forward/strike)/stddev+stddev/2
    d2 = d1-stddev
    cdf = lambda x: .5*math.erfc(-x/math.sqrt(2))
    return {'value': discount*(forward*cdf(d1)-strike*cdf(d2)),
            'delta': discount*cdf(d1),
            'gamma': discount*math.exp(-d1*d1/2)/math.sqrt(2*math.pi)/(forward*stddev)}


def calculate():
    started = time.monotonic()
    checks, records = [], []

    def compare(name, actual, expected, tolerance):
        error = abs(actual-expected)
        checks.append({'name': name, 'actual': actual, 'expected': expected, 'absolute_error': error,
                       'tolerance': tolerance, 'passed': math.isfinite(actual) and error <= tolerance})

    for identity, forward, strike, sigma, maturity, rate in CASES:
        stddev, discount = sigma*math.sqrt(maturity), math.exp(-rate*maturity)
        payoff = ql.PlainVanillaPayoff(ql.Option.Call,strike)

        def measure(level):
            calculator = ql.BlackCalculator(payoff,level,stddev,discount)
            price = calculator.value()
            rounded = round(price,2)
            expected = reference(level,strike,stddev,discount)
            compare(f'{identity}/{level}/price',price,expected['value'],1e-10)
            compare(f'{identity}/{level}/rounding',rounded,price,EPSILON+1e-12)
            return {'forward': level, 'quantlib_price_usd': price, 'reference_price_usd': expected['value'],
                    'rounded_price_usd': rounded, 'rounding_error_usd': rounded-price}, calculator

        base, calculator = measure(forward)
        analytic = reference(forward,strike,stddev,discount)
        ql_greeks = {'delta': calculator.deltaForward(), 'gamma': calculator.gammaForward()}
        for metric in ['delta','gamma']:
            compare(f'{identity}/analytic/{metric}',ql_greeks[metric],analytic[metric],1e-10)
        perturbations = []
        for h in BUMPS:
            minus, _ = measure(forward-h)
            plus, _ = measure(forward+h)
            views = {}
            for name, key in [('unrounded','quantlib_price_usd'),('cent_rounded','rounded_price_usd')]:
                vm, v0, vp = minus[key], base[key], plus[key]
                delta, gamma = (vp-vm)/(2*h),(vp-2*v0+vm)/(h*h)
                views[name] = {'delta': delta, 'gamma': gamma, 'delta_error': delta-analytic['delta'],
                               'gamma_error': gamma-analytic['gamma'],
                               'delta_within_illustrative_tolerance': abs(delta-analytic['delta']) <= ILLUSTRATIVE_TOLERANCE,
                               'gamma_within_illustrative_tolerance': abs(gamma-analytic['gamma']) <= ILLUSTRATIVE_TOLERANCE,
                               'up_premium_change_usd': vp-v0, 'down_premium_change_usd': vm-v0}
            envelopes = {}
            for metric, bound in [('delta',EPSILON/h),('gamma',4*EPSILON/(h*h))]:
                difference = views['cent_rounded'][metric]-views['unrounded'][metric]
                allowance = 1e-7*max(1.,bound)
                envelopes[metric] = {'rounding_difference': difference,'bound': bound,'floating_allowance':allowance}
                compare(f'{identity}/{h}/{metric}_rounding_envelope',difference,0.,bound+allowance)
            perturbations.append({'h_usd_forward':h,'minus':minus,'plus':plus,'views':views,'rounding_envelopes':envelopes})
        records.append({'id':identity,'inputs':{'forward_usd':forward,'strike_usd':strike,'annual_volatility':sigma,
                                             'maturity_years':maturity,'continuous_rate':rate,'discount':discount,'stddev':stddev},
                        'base':base,'reference':analytic,'quantlib_analytic':ql_greeks,'perturbations':perturbations})
    return {'schema':'open-quant-sensitivity-observations-v1','observed_at':datetime.now(timezone.utc).isoformat(),
            'source_sha256':sha(__file__),
            'environment':{'python':platform.python_version(),'quantlib':ql.__version__,
                           'quantlib_binary_sha256':sha(native_ql.__file__),'platform':platform.platform()},
            'scope':{'position':'one receiving unit of synthetic European call','changed_factor':'forward',
                     'held_fixed':['strike','volatility','maturity','discount'],'recalibration':False,
                     'price_unit':'USD PV','delta_unit':'USD PV per USD forward','gamma_unit':'USD PV per squared USD forward',
                     'rounding':'Python round(price, 2)','rounding_epsilon_usd':EPSILON,
                     'bumps_usd_forward':BUMPS,'illustrative_absolute_derivative_tolerance':ILLUSTRATIVE_TOLERANCE},
            'records':records,'checks':checks,'all_checks_passed':all(c['passed'] for c in checks),
            'calculation_seconds':time.monotonic()-started}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    result=calculate()
    with args.output.open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps({'all_checks_passed':result['all_checks_passed'],'checks':len(result['checks']),
                      'cases':len(result['records']),'derivative_views':36,'calculation_seconds':result['calculation_seconds']}))
    raise SystemExit(0 if result['all_checks_passed'] else 1)
