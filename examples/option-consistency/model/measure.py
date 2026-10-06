"""Retain fixed option inversions and exact butterfly payoff/cost evidence."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import time

STRIKES=[80,90,105,110,130]
AUTHORED=[21,14,9,8,3]
NODES=[0]+STRIKES+[230]
SPREADS=[F(0),F(1,20),F(1,5)]


def black_call(k,s):
    if s==0:return max(100-k,0)
    d1=math.log(100/k)/s+s/2
    d2=d1-s
    normal=lambda d:math.erfc(-d/math.sqrt(2))/2
    return 100*normal(d1)-k*normal(d2)


def independent_root(k,price):
    lo,hi=0.0,4.0
    assert black_call(k,lo)<=price<=black_call(k,hi)
    for _ in range(100):
        mid=(lo+hi)/2
        if black_call(k,mid)<price:lo=mid
        else:hi=mid
    return (lo+hi)/2


def strategy(k,prices,weights):
    wl,wr=weights
    payoff=[wl*max(s-k[0],0)-max(s-k[1],0)+wr*max(s-k[2],0) for s in NODES]
    tail_slope=wl-1+wr
    assert tail_slope==0
    minimum=min(payoff)
    mid=wl*prices[0]-prices[1]+wr*prices[2]
    costs=[]
    for spread in SPREADS:
        cost=wl*(prices[0]+spread)-(prices[1]-spread)+wr*(prices[2]+spread)
        costs.append({'half_spread_usd':str(spread),'purchase_cost_usd':str(cost),
                      'negative_cost':cost<0,'nonnegative_payoff_witness':cost<0 and minimum>=0})
    return {'strikes':k,'lower_weight':str(wl),'middle_weight':'-1','upper_weight':str(wr),
            'payoff_nodes':NODES,'terminal_payoff_usd':[str(p) for p in payoff],
            'tail_slope':str(tail_slope),'minimum_payoff_usd':str(minimum),
            'payoff_nonnegative_for_all_nonnegative_underlying':minimum>=0,
            'mid_cost_usd':str(mid),'costs':costs}


def measure():
    started=time.monotonic()
    import QuantLib as ql
    import QuantLib._QuantLib as native
    controls=[]

    def check(identity,actual,expected,tolerance=0):
        passed=actual==expected if tolerance==0 else math.isfinite(actual) and abs(actual-expected)<=tolerance
        controls.append({'id':identity,'observed':actual,'reference':expected,
                         'absolute_tolerance':tolerance,'passed':passed})

    generated=[ql.blackFormula(ql.Option.Call,k,100.0,.20,1.0,0.0) for k in STRIKES]
    for k,p in zip(STRIKES,generated):check(f'constant_vol_price_{k}',p,black_call(k,.20),1e-8)
    slices=[]
    for identity,prices in [('constant_volatility',generated),('authored_quotes',AUTHORED)]:
        rows=[]
        rational_prices=[F(str(p)) for p in prices]
        for k,p in zip(STRIKES,prices):
            reference=independent_root(k,p)
            put=float(p)-100+k
            row={'strike':k,'call_mid_usd':float(p),'call_mid_exact_input':str(F(str(p))),
                 'put_from_parity_usd':put,'intrinsic_bound_usd':max(100-k,0),
                 'forward_bound_usd':100,'reference_implied_stddev':reference}
            check(identity+f'_bounds_{k}',max(100-k,0)<=p<=100,True)
            try:
                sd=ql.blackFormulaImpliedStdDev(ql.Option.Call,k,100.0,float(p),1.0,0.0,.20,1e-12,100)
                call=ql.blackFormula(ql.Option.Call,k,100.0,sd,1.0,0.0)
                native_put=ql.blackFormula(ql.Option.Put,k,100.0,sd,1.0,0.0)
                row.update(native_success=True,native_error=None,native_implied_stddev=sd,
                           native_call_usd=call,native_put_usd=native_put,
                           repricing_residual_usd=call-float(p),parity_residual_usd=call-native_put-(100-k))
                check(identity+f'_root_{k}',sd,reference,1e-9)
                check(identity+f'_repricing_{k}',call,float(p),1e-8)
                check(identity+f'_put_{k}',native_put,put,1e-8)
                check(identity+f'_parity_{k}',row['parity_residual_usd'],0,1e-8)
            except RuntimeError as error:
                row.update(native_success=False,native_error=str(error),native_implied_stddev=None,
                           native_call_usd=None,native_put_usd=None,repricing_residual_usd=None,
                           parity_residual_usd=None)
                check(identity+f'_native_solve_{k}',False,True)
            rows.append(row)
        slopes=[]
        for i in range(4):
            slope=(rational_prices[i+1]-rational_prices[i])/(STRIKES[i+1]-STRIKES[i])
            slopes.append({'strikes':STRIKES[i:i+2],'call_slope':str(slope),
                           'within_vertical_bounds':F(-1)<=slope<=0})
            check(identity+f'_vertical_{i}',F(-1)<=slope<=0,True)
        strategies=[]
        for i in range(3):
            k=STRIKES[i:i+3];p=rational_prices[i:i+3]
            for kind,weights in [('strike_aware',(F(k[2]-k[1],k[2]-k[0]),F(k[1]-k[0],k[2]-k[0]))),
                                 ('equal_wings',(F(1,2),F(1,2)))]:
                record=strategy(k,p,weights);record['id']=f'{kind}_{k[1]}'
                record['weighting']=kind
                if kind=='strike_aware':
                    check(identity+f'_{kind}_{k[1]}_nonnegative',F(record['minimum_payoff_usd'])>=0,True)
                    check(identity+f'_{kind}_{k[1]}_tail',F(record['terminal_payoff_usd'][-1])==0,True)
                for j,cost in enumerate(record['costs']):
                    expected=F(record['mid_cost_usd'])+2*SPREADS[j]
                    check(identity+f'_{kind}_{k[1]}_cost_{j}',cost['purchase_cost_usd'],str(expected))
                strategies.append(record)
        slices.append({'id':identity,'quotes':rows,'adjacent_slopes':slopes,'strategies':strategies})
    source=Path(__file__)
    inputs={'strikes':STRIKES,'authored_call_prices':AUTHORED,'constant_stddev':.20,
            'payoff_nodes':NODES,'half_spreads':[str(s) for s in SPREADS]}
    return {'recorded_at':datetime.now(timezone.utc).isoformat(),'calculation_seconds':time.monotonic()-started,
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'plan_sha256':hashlib.sha256(source.with_name('README.md').read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest(),
            'environment':{'python':platform.python_version(),'quantlib':ql.__version__,
                           'native_sha256':hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest()},
            'scope':{'forward':100,'discount':1,'time_years':1,'displacement':0,
                     'option_style':'European','underlying_domain':'nonnegative terminal values',
                     'unit':'USD per option, unit notional','market_data':False,
                     'same_underlying_maturity_settlement':True,'fractional_positions_permitted':True,
                     'simultaneous_quotes_for_quantities_assumed':True,'other_costs_or_constraints_modeled':False,
                     'global_arbitrage_free_claim':False,'price_tolerance_usd':1e-8,'stddev_tolerance':1e-9},
            'inputs':inputs,'slices':slices,'controls':controls,
            'all_controls_passed':all(c['passed'] for c in controls)}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():parser.error('Output exists; preserve the earlier observation.')
    observed=measure();args.output.write_text(json.dumps(observed,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'slices':len(observed['slices']),'controls':len(observed['controls']),
                      'all_controls_passed':observed['all_controls_passed']}))
    raise SystemExit(0 if observed['all_controls_passed'] else 1)
