"""Retain eight native corner valuations and exact represented-value P&L bridges."""
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,itertools,json,math,platform,time
from pathlib import Path

FACTORS=['forward','volatility','maturity']
ENDPOINTS={'forward':[100,110],'volatility':[.2,.3],'maturity':[1,.75]}
INPUTS={'factors':FACTORS,'endpoints':ENDPOINTS,'strike':100,'rate':.03,'quantity':10000,'displacement':0}


def key(subset):return ''.join('1' if name in subset else '0' for name in FACTORS)


def subsets(items):
    return [tuple(s) for n in range(len(items)+1) for s in itertools.combinations(items,n)]


def reference(forward,volatility,maturity):
    stddev=volatility*math.sqrt(maturity)
    d1=math.log(forward/100)/stddev+stddev/2;d2=d1-stddev
    phi=lambda z:math.erfc(-z/math.sqrt(2))/2
    return 10000*math.exp(-.03*maturity)*(forward*phi(d1)-100*phi(d2))


def path(values,order,groups=None):
    groups=groups or {name:[name] for name in FACTORS}
    changed=set();previous='000';rows=[]
    for name in order:
        changed.update(groups[name]);current=key(changed)
        rows.append({'factor':name,'from':previous,'to':current,
                     'contribution_usd':str(values[current]-values[previous])})
        previous=current
    return {'order':list(order),'steps':rows,'sum_usd':str(sum(F(r['contribution_usd']) for r in rows))}


def measure():
    started=time.monotonic()
    import QuantLib as ql
    import QuantLib._QuantLib as native
    controls=[]
    def check(identity,actual,expected,tolerance=0):
        passed=(actual==expected) if not tolerance else type(actual) in (int,float) and math.isfinite(actual) and abs(actual-expected)<=tolerance
        controls.append({'id':identity,'observed':actual,'reference':expected,'absolute_tolerance':tolerance,'passed':passed})
    corners=[]
    for bits in itertools.product([0,1],repeat=3):
        params={name:ENDPOINTS[name][bit] for name,bit in zip(FACTORS,bits)}
        f,v,t=[params[name] for name in FACTORS]
        row={'id':''.join(map(str,bits)),'factors':params,'stddev':v*math.sqrt(t),'discount':math.exp(-.03*t),'reference_position_usd':reference(f,v,t)}
        try:
            unit=ql.blackFormula(ql.Option.Call,100,f,row['stddev'],row['discount'],0)
            total=10000*unit
            row.update(native_success=True,native_error=None,native_unit_usd=unit,native_position_usd=total,represented_position_usd=str(F(str(total))))
            check(row['id']+'_price',total,row['reference_position_usd'],1e-6)
        except RuntimeError as error:
            row.update(native_success=False,native_error=str(error),native_unit_usd=None,native_position_usd=None,represented_position_usd=None)
            check(row['id']+'_native_success',False,True)
        corners.append(row)
    attribution=None
    if all(c['native_success'] for c in corners):
        values={r['id']:F(r['represented_position_usd']) for r in corners}
        total=values['111']-values['000']
        paths=[path(values,order) for order in itertools.permutations(FACTORS)]
        for i,p in enumerate(paths):check(f'path_{i}_reconciliation',p['sum_usd'],str(total))
        standalone={name:values[key([name])]-values['000'] for name in FACTORS}
        interactions={}
        for subset in subsets(FACTORS)[1:]:
            interaction=sum((-1)**(len(subset)-len(part))*values[key(part)] for part in subsets(subset))
            interactions[key(subset)]=interaction
        for subset in subsets(FACTORS):
            reconstructed=values['000']+sum(interactions[key(part)] for part in subsets(subset)[1:])
            check('reconstruct_'+key(subset),str(reconstructed),str(values[key(subset)]))
        averages={name:sum(F(step['contribution_usd']) for p in paths for step in p['steps'] if step['factor']==name)/6 for name in FACTORS}
        allocated={name:sum(value/F(k.count('1')) for k,value in interactions.items() if k[FACTORS.index(name)]=='1') for name in FACTORS}
        for name in FACTORS:check('allocation_'+name,str(averages[name]),str(allocated[name]))
        check('allocation_total',str(sum(averages.values())),str(total))
        residual=total-sum(standalone.values())
        check('interaction_residual',str(residual),str(sum(v for k,v in interactions.items() if k.count('1')>1)))
        grouped=[path(values,order,{'forward_volatility':['forward','volatility'],'maturity':['maturity']}) for order in [('forward_volatility','maturity'),('maturity','forward_volatility')]]
        for i,p in enumerate(grouped):check(f'group_path_{i}_reconciliation',p['sum_usd'],str(total))
        group_average={name:sum(F(step['contribution_usd']) for p in grouped for step in p['steps'] if step['factor']==name)/2 for name in ['forward_volatility','maturity']}
        check('group_allocation_total',str(sum(group_average.values())),str(total))
        partition_difference=group_average['maturity']-averages['maturity']
        # Merging F and v changes the share of their three-way interaction from 1/3 to 1/2 for T.
        check('partition_difference',str(partition_difference),str(interactions['111']/6))
        attribution={'total_usd':str(total),'sequential_paths':paths,
            'standalone_usd':{k:str(v) for k,v in standalone.items()},'standalone_sum_usd':str(sum(standalone.values())),
            'interaction_residual_usd':str(residual),'subset_interactions_usd':{k:str(v) for k,v in interactions.items()},
            'average_over_orders_usd':{k:str(v) for k,v in averages.items()},
            'equal_interaction_allocation_usd':{k:str(v) for k,v in allocated.items()},
            'factor_order_ranges_usd':{name:{'min':str(min(F(step['contribution_usd']) for p in paths for step in p['steps'] if step['factor']==name)),
                                           'max':str(max(F(step['contribution_usd']) for p in paths for step in p['steps'] if step['factor']==name))} for name in FACTORS},
            'grouped_paths':grouped,'group_average_usd':{k:str(v) for k,v in group_average.items()},
            'partition_difference_maturity_usd':str(partition_difference),
            'partition_difference_forward_volatility_usd':str(group_average['forward_volatility']-averages['forward']-averages['volatility'])}
    source=Path(__file__)
    return {'recorded_at':datetime.now(timezone.utc).isoformat(),'calculation_seconds':time.monotonic()-started,
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'plan_sha256':hashlib.sha256(source.with_name('README.md').read_bytes()).hexdigest(),
            'input_sha256':hashlib.sha256(json.dumps(INPUTS,sort_keys=True).encode()).hexdigest(),'inputs':INPUTS,
            'environment':{'python':platform.python_version(),'quantlib':ql.__version__,'native_sha256':hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest()},
            'scope':{'currency':'USD','fixed_position':True,'trades_cashflows_fees':False,'market_observations':False,
                     'forward_independently_supplied':True,'arithmetic_tolerance_usd':1e-6,'causal_explanation_established':False,
                     'unique_institutional_method_established':False,'regulatory_attribution_test':False},
            'corners':corners,'attribution':attribution,'controls':controls,'all_controls_passed':all(r['passed'] for r in controls)}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():parser.error('Output exists; preserve the earlier observation.')
    observed=measure();args.output.write_text(json.dumps(observed,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'native_valuations':len(observed['corners']),'controls':len(observed['controls']),'all_controls_passed':observed['all_controls_passed']}))
    raise SystemExit(0 if observed['all_controls_passed'] else 1)
