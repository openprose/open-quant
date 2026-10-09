"""One fixed quote/zero-coordinate study; no network or model provider."""
import argparse
import hashlib
import json
import math
import platform
import time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import QuantLib as ql


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Output already exists')
    started = time.monotonic()
    q1, q2, h = 0.03, 0.04, 0.0001
    principal = 1_000_000
    flows = {'four_percent': [40_000, 1_040_000], 'six_percent': [60_000, 1_060_000]}
    ref = ql.Date(1, 1, 2026)
    dates = [ref, ref + 365, ref + 730]
    dc = ql.Actual365Fixed()
    ql.Settings.instance().evaluationDate = ref
    d1, d2 = 1/(1+q1), (1-q2/(1+q1))/(1+q2)
    factors = [('quote_1', 'quote', (1, 0)), ('quote_2', 'quote', (0, 1)), ('quote_parallel', 'quote', (1, 1)),
               ('zero_1', 'zero', (1, 0)), ('zero_2', 'zero', (0, 1)), ('zero_parallel', 'zero', (1, 1))]
    specs = [('base', 'base', (0, 0), 0)] + [(f'{name}_{suffix}', kind, mask, sign) for name, kind, mask in factors for suffix, sign in [('plus', 1), ('minus', -1)]]
    checks = []
    def check(name, actual, expected, tolerance):
        checks.append({'name': name, 'actual': actual, 'expected': expected, 'tolerance': tolerance, 'passed': abs(actual-expected) <= tolerance})
    records = []
    with localcontext() as context:
        context.prec = 50
        Q1, Q2, H = Decimal('0.03'), Decimal('0.04'), Decimal('0.0001')
        B1 = 1/(1+Q1)
        B2 = (1-Q2*B1)/(1+Q2)
        for name, kind, mask, sign in specs:
            targets = None
            if kind == 'quote':
                a, b = q1+sign*h*mask[0], q2+sign*h*mask[1]
                nodes = [1/(1+a), (1-b/(1+a))/(1+b)]
                A, B = Q1+sign*H*mask[0], Q2+sign*H*mask[1]
                exact_nodes = [1/(1+A), (1-B/(1+A))/(1+B)]
                targets = [a, b]
            elif kind == 'zero':
                nodes = [d1*math.exp(-sign*h*mask[0]), d2*math.exp(-2*sign*h*mask[1])]
                exact_nodes = [B1*(-sign*H*mask[0]).exp(), B2*(-2*sign*H*mask[1]).exp()]
            else:
                nodes = [d1, d2]
                exact_nodes = [B1, B2]
                targets = [q1, q2]
            curve = ql.DiscountCurve(dates, [1.0]+nodes, dc)
            observed_nodes = [curve.discount(date) for date in dates[1:]]
            implied = [1/observed_nodes[0]-1, (1-observed_nodes[1])/sum(observed_nodes)]
            values, reference_values = {}, {}
            for index, node in enumerate(observed_nodes):
                check(f'{name}:node:{index}', node, float(exact_nodes[index]), 1e-14)
                if targets is not None:
                    check(f'{name}:quote:{index}', implied[index], targets[index], 1e-12)
            for instrument, amounts in flows.items():
                leg = [ql.SimpleCashFlow(amount, date) for amount, date in zip(amounts, dates[1:])]
                value = ql.CashFlows.npv(leg, ql.YieldTermStructureHandle(curve), False, ref, ref)
                exact_value = sum(Decimal(amount)*node for amount, node in zip(amounts, exact_nodes))
                values[instrument], reference_values[instrument] = value, str(exact_value)
                check(f'{name}:value:{instrument}', value, float(exact_value), 1e-8)
            checks.append({'name':f'{name}:positive_decreasing_nodes','passed':0 < observed_nodes[1] < observed_nodes[0] < 1})
            records.append({'id':name,'coordinate':kind,'factor_mask':list(mask),'direction':sign,'shock_decimal':sign*h,'discount_nodes':observed_nodes,'implied_par_quotes':implied,'target_par_quotes':targets,'values_usd':values,'decimal_reference_values_usd':reference_values})
        index = {r['id']:r for r in records}
        x, y = F(3,100), F(4,100)
        a, b = 1/(1+x), (1-y/(1+x))/(1+y)
        dd = [[-1/(1+x)**2,F(0)], [y/((1+y)*(1+x)**2), -(1+a)/(1+y)**2]]
        dz = [[-dd[0][j]/a for j in range(2)], [-dd[1][j]/(2*b) for j in range(2)]]
        analytic, sensitivities = {}, []
        for instrument, amounts in flows.items():
            gp = [-amounts[0]*a,-2*amounts[1]*b]
            gq = [sum(F(amounts[i])*dd[i][j] for i in range(2)) for j in range(2)]
            chain = [sum(gp[i]*dz[i][j] for i in range(2)) for j in range(2)]
            checks.append({'name':f'{instrument}:exact_chain_rule','passed':gq==chain})
            analytic[instrument] = {'zero_gradient':list(map(float,gp)),'quote_gradient':list(map(float,gq)),'quote_gradient_exact':list(map(str,gq)),'chain_quote_gradient_exact':list(map(str,chain))}
            for name, kind, mask in factors:
                plus, minus = index[name+'_plus'], index[name+'_minus']
                central = (plus['values_usd'][instrument]-minus['values_usd'][instrument])/(2*h)
                decimal_central = (Decimal(plus['decimal_reference_values_usd'][instrument])-Decimal(minus['decimal_reference_values_usd'][instrument]))/(2*H)
                gradient = gp if kind == 'zero' else gq
                analytic_derivative = sum(gradient[i]*mask[i] for i in range(2))
                check(f'{name}:{instrument}:finite_reference', central, float(decimal_central), 2e-5)
                check(f'{name}:{instrument}:analytic_derivative', central, float(analytic_derivative), 0.1)
                sensitivities.append({'factor':name,'instrument':instrument,'central_derivative_usd_per_unit_rate':central,'signed_central_change_for_1bp_usd':central*h,'positive_1bp_change_usd':plus['values_usd'][instrument]-index['base']['values_usd'][instrument],'analytic_derivative_usd_per_unit_rate':float(analytic_derivative)})
        for name in ['base','quote_1_plus','quote_1_minus']:
            check(name+':par_invariant', index[name]['values_usd']['four_percent'], principal, 1e-8)
        check('year_one', dc.yearFraction(ref, dates[1]), 1, 0)
        check('year_two', dc.yearFraction(ref, dates[2]), 2, 0)
    source = Path(__file__).resolve()
    result = {'scope':'Synthetic coordinate comparison; all cash flows fixed; algebraic node calibration, native curve/NPV values; no agent or empirical performance study.',
              'source_sha256':digest(source),'plan_sha256':digest(source.with_name('PLAN.md')),
              'environment':{'python':platform.python_version(),'QuantLib':ql.__version__,'platform':platform.platform()},
              'reference_date':'2026-01-01','payment_dates':[str(d) for d in dates[1:]],'times_years':[1,2],'base_par_quotes':[q1,q2],'base_zero_rates':[-math.log(d1),-math.log(d2)/2],
              'principal_usd':principal,'cashflows_usd':flows,'shock_size_decimal':h,'records':records,'sensitivities':sensitivities,
              'analytic':analytic,'zero_quote_jacobian_exact':[[str(v) for v in row] for row in dz],'checks':checks,'elapsed_seconds':time.monotonic()-started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    failed = [c['name'] for c in checks if not c['passed']]
    print(json.dumps({'curves':len(records),'values':sum(len(r['values_usd']) for r in records),'checks':len(checks),'failed':failed}))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
