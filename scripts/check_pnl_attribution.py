"""Check fixed P&L records and input support; no arbitrary prose or native pricing."""
import copy,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXAMPLE=ROOT/'examples/pnl-attribution'
FACTORS=['forward','volatility','maturity']
CLAIMS=[
    'All six bridges reconcile, so their factor allocations are identical.',
    'The standalone effects explain the whole movement without an interaction residual.',
    'The average allocation establishes the economic cause of the P&L.',
    'Grouping forward and volatility before allocation leaves each allocation unchanged.',
    'A successful producer flag and downstream increments independently verify a missing corner valuation.',
    'These results fulfill the regulatory P&L attribution test and authorize an accounting posting.'
]


def close(a,b,tol=1e-6):
    assert type(a) in (int,float) and math.isfinite(a) and abs(a-b)<=tol,(a,b)


def linear(coefficients,values):
    """Only evaluate identified source values; cancel coefficients before checking gaps."""
    if any(v and values[k] is None for k,v in coefficients.items()):return None
    return sum(v*values[k] for k,v in coefficients.items() if v)


def match(value,coefficients,values):
    expected=linear(coefficients,values)
    observed=F(value)
    if expected is None:return 'unresolved'
    assert observed==expected,(observed,expected)
    return 'met'


def verify(d,source_hash):
    assert d['subject']=='PNL-ATTRIBUTION-2026-10-06' and d['source_sha256']==source_hash
    assert d['case'] in ['complete','missing-corner','contradictory']
    assert d['producer_claims']==([{'id':f'C{i+1}','text':t} for i,t in enumerate(CLAIMS)] if d['case']=='contradictory' else [])
    assert d['inputs']=={'factors':FACTORS,'endpoints':{'forward':[100,110],'volatility':[.2,.3],'maturity':[1,.75]},'strike':100,'rate':.03,'quantity':10000,'displacement':0}
    assert d['scope']=={'currency':'USD','fixed_position':True,'trades_cashflows_fees':False,'market_observations':False,'forward_independently_supplied':True,'arithmetic_tolerance_usd':1e-6,'regulatory_attribution_test':False}
    ids=[''.join(map(str,b)) for b in itertools.product([0,1],repeat=3)]
    assert [r['id'] for r in d['corners']]==ids
    values={};corner_support={}
    for row in d['corners']:
        params={f:d['inputs']['endpoints'][f][int(bit)] for f,bit in zip(FACTORS,row['id'])}
        assert row['factors']==params
        forward,vol,t=[params[f] for f in FACTORS]
        sd=vol*math.sqrt(t);discount=math.exp(-.03*t)
        close(row['stddev'],sd,1e-14);close(row['discount'],discount,1e-14)
        assert row['native_success'] is True and row['native_error'] is None
        fields=['native_unit_usd','native_position_usd','represented_position_usd','reference_position_usd']
        if d['case']=='missing-corner' and row['id']=='110':
            assert all(row[field] is None for field in fields)
            values[row['id']]=None;corner_support[row['id']]='unresolved';continue
        assert all(row[field] is not None for field in fields)
        d1=(math.log(forward/100)+.5*vol*vol*t)/sd;d2=d1-sd
        phi=lambda x:(1+math.erf(x/math.sqrt(2)))/2
        expected=10000*discount*(forward*phi(d1)-100*phi(d2))
        close(row['native_position_usd'],expected);close(row['reference_position_usd'],expected)
        close(row['native_unit_usd']*10000,row['native_position_usd'])
        assert F(row['represented_position_usd'])==F(str(row['native_position_usd']))
        values[row['id']]=F(row['represented_position_usd']);corner_support[row['id']]='met'
    a=d['reported_attribution'];total=values['111']-values['000'];assert F(a['total_usd'])==total
    paths=a['sequential_paths'];assert len(paths)==6
    samples={f:[] for f in FACTORS};path_support=[]
    for row,order in zip(paths,itertools.permutations(FACTORS)):
        assert row['order']==list(order) and len(row['steps'])==3
        bits=['0']*3;contributions=[];states=[]
        for step,f in zip(row['steps'],order):
            before=''.join(bits);bits[FACTORS.index(f)]='1';after=''.join(bits)
            assert step['factor']==f and step['from']==before and step['to']==after
            states.append(match(step['contribution_usd'],{after:F(1),before:F(-1)},values))
            value=F(step['contribution_usd']);contributions.append(value);samples[f].append(value)
        assert sum(contributions)==F(row['sum_usd'])==total
        path_support.append({'order':list(order),'internal_reconciliation':'met','source_support':'unresolved' if 'unresolved' in states else 'met','step_source_support':states})
    allocation_support={}
    for i,f in enumerate(FACTORS):
        coefficients={k:F(0) for k in ids}
        for k in ids:
            if k[i]=='1':continue
            n=k.count('1');weight=F(math.factorial(n)*math.factorial(2-n),6)
            changed=k[:i]+'1'+k[i+1:];coefficients[changed]+=weight;coefficients[k]-=weight
        allocation_support[f]=match(a['average_over_orders_usd'][f],coefficients,values)
        assert F(a['average_over_orders_usd'][f])==sum(samples[f])/6
        assert F(a['factor_order_ranges_usd'][f]['min'])==min(samples[f])
        assert F(a['factor_order_ranges_usd'][f]['max'])==max(samples[f])
    standalone={f:values['0'*i+'1'+'0'*(2-i)]-values['000'] for i,f in enumerate(FACTORS)}
    assert {k:F(v) for k,v in a['standalone_usd'].items()}==standalone
    assert F(a['standalone_sum_usd'])==sum(standalone.values())
    assert F(a['interaction_residual_usd'])==total-sum(standalone.values())
    interactions={k:F(v) for k,v in a['subset_interactions_usd'].items()};assert set(interactions)==set(ids[1:])
    interaction_support={}
    for k in ids[1:]:
        coefficients={p:F((-1)**(k.count('1')-p.count('1'))) for p in ids if all(pb=='0' or kb=='1' for pb,kb in zip(p,k))}
        interaction_support[k]=match(interactions[k],coefficients,values)
    assert sum(interactions.values())==total
    assert sum(v for k,v in interactions.items() if k.count('1')>1)==F(a['interaction_residual_usd'])
    for i,f in enumerate(FACTORS):
        split=sum(v/F(k.count('1')) for k,v in interactions.items() if k[i]=='1')
        assert F(a['equal_interaction_allocation_usd'][f])==split==F(a['average_over_orders_usd'][f])
    expected_paths=[(['forward_volatility','maturity'],['000','110','111']),(['maturity','forward_volatility'],['000','001','111'])]
    assert len(a['grouped_paths'])==2;group_support=[];group_samples={'forward_volatility':[],'maturity':[]}
    for row,(names,ks) in zip(a['grouped_paths'],expected_paths):
        assert row['order']==names and len(row['steps'])==2;states=[]
        for step,name,k0,k1 in zip(row['steps'],names,ks,ks[1:]):
            assert step['factor']==name and step['from']==k0 and step['to']==k1
            states.append(match(step['contribution_usd'],{k1:F(1),k0:F(-1)},values))
            group_samples[name].append(F(step['contribution_usd']))
        assert sum(F(s['contribution_usd']) for s in row['steps'])==F(row['sum_usd'])==total
        group_support.append({'order':names,'internal_reconciliation':'met','source_support':'unresolved' if 'unresolved' in states else 'met'})
    group={k:F(v) for k,v in a['group_average_usd'].items()}
    assert set(group)==set(group_samples)
    for name in group:assert group[name]==sum(group_samples[name])/2
    delta=group['maturity']-F(a['average_over_orders_usd']['maturity'])
    assert F(a['partition_difference_maturity_usd'])==delta==interactions['111']/6
    assert F(a['partition_difference_forward_volatility_usd'])==-delta
    assert group['forward_volatility']-F(a['average_over_orders_usd']['forward'])-F(a['average_over_orders_usd']['volatility'])==-delta
    return {'corner_source_support':corner_support,'total_source_support':'met','total_usd':a['total_usd'],
            'standalone_source_support':'met','interaction_residual_source_support':'met',
            'paths':path_support,'selected_allocation_source_support':allocation_support,
            'interaction_source_support':interaction_support,'grouped_paths':group_support,
            'reported_allocation_internal_consistency':'met','causal_identification':'not_established'}


def main():
    read=lambda p:json.loads(p.read_text());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    receipt=read(EXAMPLE/'receipt.json');source_hash=digest(EXAMPLE/receipt['source_path'])
    assert receipt['source_sha256']==source_hash and receipt['plan_sha256']==digest(EXAMPLE/receipt['plan_path'])
    packets={};results={}
    for case,record in receipt['packets'].items():
        path=EXAMPLE/record['path'];assert digest(path)==record['sha256']
        packets[case]=read(path);assert packets[case]['case']==case;results[case]=verify(packets[case],source_hash)
    assert set(packets)=={'complete','missing-corner','contradictory'}
    assert results['complete']==results['contradictory']
    assert all(p['source_support']=='met' for p in results['complete']['paths'])
    missing=results['missing-corner'];assert [p['source_support'] for p in missing['paths']]==['unresolved','met','unresolved','met','met','met']
    assert [p['source_support'] for p in missing['grouped_paths']]==['unresolved','met']
    assert set(missing['selected_allocation_source_support'].values())=={'unresolved'}
    assert [k for k,v in missing['interaction_source_support'].items() if v=='unresolved']==['110','111']
    assert missing['total_usd']==results['complete']['total_usd']
    assert linear({'000':F(0),'001':F(1)},{'000':None,'001':F(3)})==3
    close(1e-6,0)
    try:close(1.0001e-6,0)
    except AssertionError:pass
    else:raise AssertionError('Exceeded tolerance unnoticed')
    def redistribute_steps(x):
        steps=x['reported_attribution']['sequential_paths'][0]['steps']
        steps[0]['contribution_usd']=str(F(steps[0]['contribution_usd'])+1)
        steps[1]['contribution_usd']=str(F(steps[1]['contribution_usd'])-1)
    def swap_means(x):
        means=x['reported_attribution']['average_over_orders_usd']
        means['forward'],means['volatility']=means['volatility'],means['forward']
    mutations=[
        ('omit_corner','complete',lambda x:x['corners'].pop()),
        ('wrong_factor_binding','complete',lambda x:x['corners'][1]['factors'].update(maturity=1)),
        ('wrong_stddev','complete',lambda x:x['corners'][1].update(stddev=.2)),
        ('wrong_discount','complete',lambda x:x['corners'][1].update(discount=1)),
        ('wrong_quantity','complete',lambda x:x['inputs'].update(quantity=1000)),
        ('wrong_native_value','complete',lambda x:x['corners'][0].update(native_position_usd=0)),
        ('wrong_represented_value','complete',lambda x:x['corners'][0].update(represented_position_usd='0')),
        ('fill_missing_corner','missing-corner',lambda x:x['corners'][6].update(native_position_usd=0)),
        ('omit_order','complete',lambda x:x['reported_attribution']['sequential_paths'].pop()),
        ('mislabel_order','complete',lambda x:x['reported_attribution']['sequential_paths'][0]['order'].reverse()),
        ('mislabel_factor','complete',lambda x:x['reported_attribution']['sequential_paths'][0]['steps'][0].update(factor='volatility')),
        ('wrong_transition','complete',lambda x:x['reported_attribution']['sequential_paths'][0]['steps'][1].update(to='111')),
        ('erase_residual','complete',lambda x:x['reported_attribution'].update(interaction_residual_usd='0')),
        ('false_standalone_total','complete',lambda x:x['reported_attribution'].update(standalone_sum_usd=x['reported_attribution']['total_usd'])),
        ('omit_interaction','complete',lambda x:x['reported_attribution']['subset_interactions_usd'].pop('111')),
        ('substitute_group_allocation','complete',lambda x:x['reported_attribution']['average_over_orders_usd'].update(maturity=x['reported_attribution']['group_average_usd']['maturity'])),
        ('erase_grouping_effect','complete',lambda x:x['reported_attribution'].update(partition_difference_maturity_usd='0')),
        ('balanced_wrong_steps','complete',redistribute_steps),
        ('swap_means_preserve_total','complete',swap_means),
        ('regulatory_claim','complete',lambda x:x['scope'].update(regulatory_attribution_test=True)),
    ]
    rejected=[]
    for name,case,change in mutations:
        altered=copy.deepcopy(packets[case]);change(altered)
        try:verify(altered,source_hash)
        except (AssertionError,KeyError,TypeError,ValueError):rejected.append(name)
        else:raise AssertionError('Undetected mutation: '+name)
    print(json.dumps({'cases':3,'corners_per_case':8,'sequential_paths_per_case':6,'mutations_rejected':rejected,'native_pricing_calls':0,'provider_calls':0}))


if __name__=='__main__':main()
